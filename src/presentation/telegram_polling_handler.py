from __future__ import annotations

import asyncio
import hashlib

from application.classification_orchestrator import ClassificationOrchestrator
from domain.enums import ProcessingStatus
from application.message_preprocessor import MessagePreprocessor
from domain.models import build_message_meta, build_queue_task
from infrastructure.gemini_client import LLMTimeoutError
from infrastructure.queue_repository import QueueRepository
from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext
from observability.log_events import LogEvent
from observability.logging_service import LoggingService
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .notification_service import NotificationService

class TelegramPollingHandler:
    """Receives Telegram updates and routes them to the pilot interaction flow."""

    def __init__(
        self,
        notification_service: NotificationService,
        message_preprocessor: MessagePreprocessor,
        classification_orchestrator: ClassificationOrchestrator,
        queue_repository: QueueRepository,
        logging_service: LoggingService,
        correlation_id_factory: CorrelationIdFactory,
    ) -> None:
        self._notification_service = notification_service
        self._message_preprocessor = message_preprocessor
        self._classification_orchestrator = classification_orchestrator
        self._queue_repository = queue_repository
        self._logging_service = logging_service
        self._correlation_id_factory = correlation_id_factory

    def register(self, application: Application) -> None:
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(
            CallbackQueryHandler(self.report_execution_callback, pattern=r"^report_execution$")
        )
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.free_text_handler))
        application.add_error_handler(self.error_handler)

    @staticmethod
    def _build_report_keyboard() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Report Progress", callback_data="report_execution")]]
        )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if update.effective_message is None:
            return

        await self._notification_service.send_welcome(
            target_message=update.effective_message,
            reply_markup=self._build_report_keyboard(),
        )

    async def report_execution_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        del context
        query = update.callback_query
        if query is None:
            return

        await query.answer()
        if query.message is None:
            return

        await self._notification_service.send_input_instruction(target_message=query.message)

    async def free_text_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        message = update.effective_message
        if message is None or message.text is None:
            return

        raw_text = message.text
        normalized_text = self._message_preprocessor.normalize(raw_text)

        chat_id = str(update.effective_chat.id) if update.effective_chat else "unknown"
        user_id = str(update.effective_user.id) if update.effective_user else "unknown"
        message_id = str(message.message_id)
        trace_id = self._correlation_id_factory.build_trace_id(chat_id, message_id)
        raw_text_sha256 = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()

        self._logging_service.info(
            event=LogEvent.message_received,
            component="telegram_polling_handler",
            context=LogContext(
                trace_id=trace_id,
                chat_id=chat_id,
                user_id=user_id,
                message_id=message_id,
                processing_path="online",
                status=ProcessingStatus.RECEIVED.value,
            ),
            payload={
                "raw_text_length": len(raw_text),
                "raw_text_sha256": raw_text_sha256,
            },
        )

        meta = build_message_meta(
            user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            timestamp=message.date,
        )

        try:
            run_result = await asyncio.to_thread(
                self._classification_orchestrator.classify,
                raw_text=raw_text,
                normalized_text=normalized_text,
                meta=meta,
            )
        except LLMTimeoutError:
            queue_task = build_queue_task(
                user_id=user_id,
                chat_id=chat_id,
                message_id=message_id,
                raw_text=raw_text,
                normalized_text=normalized_text,
                received_at=message.date,
            )
            try:
                queue_id = await asyncio.to_thread(self._queue_repository.enqueue, queue_task)
            except Exception as exc:
                self._logging_service.error(
                    event=LogEvent.queue_enqueue_failed,
                    component="queue_service",
                    context=LogContext(
                        trace_id=trace_id,
                        chat_id=chat_id,
                        user_id=user_id,
                        message_id=message_id,
                        processing_path="online",
                        status=ProcessingStatus.QUEUED.value,
                    ),
                    payload={
                        "error_type": type(exc).__name__,
                        "error_message": str(exc),
                    },
                )
                await self._notification_service.send_processing_error(target_message=message)
                return

            self._logging_service.info(
                event=LogEvent.queue_enqueued,
                component="queue_service",
                context=LogContext(
                    trace_id=trace_id,
                    chat_id=chat_id,
                    user_id=user_id,
                    message_id=message_id,
                    processing_path="online",
                    status=ProcessingStatus.QUEUED.value,
                ),
                payload={"queue_id": queue_id},
            )
            await self._notification_service.send_queued_notice(target_message=message)
            return
        except Exception as exc:
            self._logging_service.error(
                event=LogEvent.classification_failed,
                component="telegram_polling_handler",
                context=LogContext(
                    trace_id=trace_id,
                    chat_id=chat_id,
                    user_id=user_id,
                    message_id=message_id,
                    processing_path="online",
                    status="FAILED",
                ),
                payload={
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
            await self._notification_service.send_processing_error(target_message=message)
            return

        await self._notification_service.send_immediate_confirmation(
            target_message=message,
            classification_payload=run_result.record.classification.as_json_dict(),
            status=run_result.record.audit.status.value,
        )

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        del update
        self._logging_service.error(
            event=LogEvent.telegram_update_error,
            component="telegram_polling_handler",
            context=LogContext(
                trace_id="unknown:unknown",
                chat_id="unknown",
                user_id="unknown",
                message_id="unknown",
                processing_path="online",
                status="FAILED",
            ),
            payload={
                "error_type": type(context.error).__name__ if context.error is not None else "UnknownError",
                "error_message": str(context.error),
            },
        )
