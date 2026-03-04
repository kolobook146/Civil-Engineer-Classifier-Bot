from __future__ import annotations

import asyncio
import hashlib

from application.classification_orchestrator import ClassificationOrchestrator
from application.message_preprocessor import MessagePreprocessor
from domain.enums import ProcessingStatus
from domain.models import build_message_meta, build_queue_task
from infrastructure.gemini_client import LLMTimeoutError
from infrastructure.pending_confirmation_repository import PendingConfirmationRepository
from infrastructure.queue_repository import QueueRepository
from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext
from observability.log_events import LogEvent
from observability.logging_service import LoggingService
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
)
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

    _BUTTON_REPORT = "Report Progress"
    _BUTTON_HELP = "Help"
    _BUTTON_MAIN_MENU = "Main Menu"

    _CALLBACK_REPORT = "report_execution"
    _CALLBACK_MAIN_MENU = "main_menu"
    _CALLBACK_SHOW_EXAMPLE = "show_example"
    _CALLBACK_CANCEL_INPUT = "cancel_input"
    _CALLBACK_CONFIRM_PREFIX = "confirm:"
    _CALLBACK_EDIT_PREFIX = "edit:"
    _CALLBACK_CANCEL_PREFIX = "cancel:"

    def __init__(
        self,
        notification_service: NotificationService,
        message_preprocessor: MessagePreprocessor,
        classification_orchestrator: ClassificationOrchestrator,
        queue_repository: QueueRepository,
        pending_confirmation_repository: PendingConfirmationRepository,
        logging_service: LoggingService,
        correlation_id_factory: CorrelationIdFactory,
    ) -> None:
        self._notification_service = notification_service
        self._message_preprocessor = message_preprocessor
        self._classification_orchestrator = classification_orchestrator
        self._queue_repository = queue_repository
        self._pending_confirmation_repository = pending_confirmation_repository
        self._logging_service = logging_service
        self._correlation_id_factory = correlation_id_factory

    def register(self, application: Application) -> None:
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(
            CallbackQueryHandler(self.report_execution_callback, pattern=rf"^{self._CALLBACK_REPORT}$")
        )
        application.add_handler(
            CallbackQueryHandler(self.main_menu_callback, pattern=rf"^{self._CALLBACK_MAIN_MENU}$")
        )
        application.add_handler(
            CallbackQueryHandler(self.show_example_callback, pattern=rf"^{self._CALLBACK_SHOW_EXAMPLE}$")
        )
        application.add_handler(
            CallbackQueryHandler(self.cancel_input_callback, pattern=rf"^{self._CALLBACK_CANCEL_INPUT}$")
        )
        application.add_handler(
            CallbackQueryHandler(self.confirm_record_callback, pattern=rf"^{self._CALLBACK_CONFIRM_PREFIX}")
        )
        application.add_handler(
            CallbackQueryHandler(self.edit_record_callback, pattern=rf"^{self._CALLBACK_EDIT_PREFIX}")
        )
        application.add_handler(
            CallbackQueryHandler(self.cancel_record_callback, pattern=rf"^{self._CALLBACK_CANCEL_PREFIX}")
        )
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.free_text_handler))
        application.add_error_handler(self.error_handler)

    @classmethod
    def _build_main_menu_keyboard(cls) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=cls._BUTTON_REPORT), KeyboardButton(text=cls._BUTTON_HELP)],
            ],
            resize_keyboard=True,
        )

    @classmethod
    def _build_input_action_keyboard(cls) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text="Show Example", callback_data=cls._CALLBACK_SHOW_EXAMPLE),
                InlineKeyboardButton(text="Cancel", callback_data=cls._CALLBACK_CANCEL_INPUT),
            ]]
        )

    @classmethod
    def _build_confirmation_keyboard(cls, confirmation_id: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Confirm", callback_data=f"{cls._CALLBACK_CONFIRM_PREFIX}{confirmation_id}")],
                [
                    InlineKeyboardButton(text="Edit", callback_data=f"{cls._CALLBACK_EDIT_PREFIX}{confirmation_id}"),
                    InlineKeyboardButton(text="Cancel", callback_data=f"{cls._CALLBACK_CANCEL_PREFIX}{confirmation_id}"),
                ],
            ]
        )

    @classmethod
    def _build_success_keyboard(cls) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text="Report Another", callback_data=cls._CALLBACK_REPORT),
                InlineKeyboardButton(text="Main Menu", callback_data=cls._CALLBACK_MAIN_MENU),
            ]]
        )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if update.effective_message is None:
            return

        await self._notification_service.send_welcome(
            target_message=update.effective_message,
            reply_markup=self._build_main_menu_keyboard(),
        )

    async def main_menu_callback(
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
        await self._safe_clear_inline_markup(query)
        await self._notification_service.send_welcome(
            target_message=query.message,
            reply_markup=self._build_main_menu_keyboard(),
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

        await self._notification_service.send_input_instruction(
            target_message=query.message,
            reply_markup=self._build_input_action_keyboard(),
        )

    async def show_example_callback(
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

        await self._notification_service.send_example(target_message=query.message)

    async def cancel_input_callback(
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

        await self._safe_clear_inline_markup(query)
        await self._notification_service.send_input_cancelled(
            target_message=query.message,
            reply_markup=self._build_main_menu_keyboard(),
        )

    async def free_text_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        message = update.effective_message
        if message is None or message.text is None:
            return

        stripped_text = message.text.strip()
        if stripped_text == self._BUTTON_REPORT:
            await self._notification_service.send_input_instruction(
                target_message=message,
                reply_markup=self._build_input_action_keyboard(),
            )
            return
        if stripped_text == self._BUTTON_HELP:
            await self._notification_service.send_help(
                target_message=message,
                reply_markup=self._build_main_menu_keyboard(),
            )
            return
        if stripped_text == self._BUTTON_MAIN_MENU:
            await self._notification_service.send_welcome(
                target_message=message,
                reply_markup=self._build_main_menu_keyboard(),
            )
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

        try:
            pending_confirmation = await asyncio.to_thread(
                self._pending_confirmation_repository.create,
                run_result.record,
            )
            await self._notification_service.send_confirmation_request(
                target_message=message,
                classification_payload=run_result.record.classification.as_json_dict(),
                status=run_result.record.audit.status.value,
                reply_markup=self._build_confirmation_keyboard(pending_confirmation.confirmation_id),
            )
        except Exception as exc:
            if "pending_confirmation" in locals():
                await asyncio.to_thread(
                    self._pending_confirmation_repository.delete,
                    pending_confirmation.confirmation_id,
                )
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
                    "failure_stage": "pending_confirmation_request",
                },
            )
            await self._notification_service.send_processing_error(target_message=message)

    async def confirm_record_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        del context
        query = update.callback_query
        if query is None:
            return

        confirmation_id = self._extract_confirmation_id(query.data, self._CALLBACK_CONFIRM_PREFIX)
        if confirmation_id is None:
            await query.answer()
            return

        pending_confirmation = await asyncio.to_thread(
            self._pending_confirmation_repository.get,
            confirmation_id,
        )
        if pending_confirmation is None:
            await query.answer("This record was already handled or has expired.")
            return

        await query.answer("Saving the record...")
        try:
            await asyncio.to_thread(
                self._classification_orchestrator.persist_record,
                pending_confirmation.record,
            )
        except Exception:
            if query.message is not None:
                await self._notification_service.send_processing_error(target_message=query.message)
            return

        await asyncio.to_thread(
            self._pending_confirmation_repository.delete,
            confirmation_id,
        )
        await self._safe_clear_inline_markup(query)
        if query.message is None:
            return
        await self._notification_service.send_record_saved(
            target_message=query.message,
            classification_payload=pending_confirmation.record.classification.as_json_dict(),
            status=pending_confirmation.record.audit.status.value,
            reply_markup=self._build_success_keyboard(),
        )

    async def edit_record_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        del context
        query = update.callback_query
        if query is None:
            return

        confirmation_id = self._extract_confirmation_id(query.data, self._CALLBACK_EDIT_PREFIX)
        if confirmation_id is None:
            await query.answer()
            return

        deleted = await asyncio.to_thread(
            self._pending_confirmation_repository.delete,
            confirmation_id,
        )
        if not deleted:
            await query.answer("This draft is no longer available.")
            return

        await query.answer("Send the corrected message.")
        await self._safe_clear_inline_markup(query)
        if query.message is None:
            return
        await self._notification_service.send_input_instruction(
            target_message=query.message,
            reply_markup=self._build_input_action_keyboard(),
            prefix_text="The draft was removed. Send the corrected message.",
        )

    async def cancel_record_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        del context
        query = update.callback_query
        if query is None:
            return

        confirmation_id = self._extract_confirmation_id(query.data, self._CALLBACK_CANCEL_PREFIX)
        if confirmation_id is None:
            await query.answer()
            return

        deleted = await asyncio.to_thread(
            self._pending_confirmation_repository.delete,
            confirmation_id,
        )
        if not deleted:
            await query.answer("This draft is no longer available.")
            return

        await query.answer("The record was cancelled.")
        await self._safe_clear_inline_markup(query)
        if query.message is None:
            return
        await self._notification_service.send_pending_cancelled(
            target_message=query.message,
            reply_markup=self._build_main_menu_keyboard(),
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

    @staticmethod
    def _extract_confirmation_id(data: str | None, prefix: str) -> str | None:
        if data is None or not data.startswith(prefix):
            return None
        confirmation_id = data[len(prefix):].strip()
        return confirmation_id or None

    @staticmethod
    async def _safe_clear_inline_markup(query) -> None:
        try:
            await query.edit_message_reply_markup(reply_markup=None)
        except Exception:
            return
