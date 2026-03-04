from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from functools import partial

from domain.enums import ProcessingStatus
from domain.models import build_message_meta
from infrastructure.gemini_client import LLMTimeoutError
from infrastructure.pending_confirmation_repository import PendingConfirmationRepository
from infrastructure.queue_repository import QueueRepository
from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext
from observability.log_events import LogEvent
from observability.logging_service import LoggingService
from presentation.notification_service import NotificationService
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

from .classification_orchestrator import ClassificationOrchestrator

class QueueWorker:
    """Processes deferred queue tasks and sends post-factum notifications."""

    def __init__(
        self,
        *,
        queue_repository: QueueRepository,
        pending_confirmation_repository: PendingConfirmationRepository,
        classification_orchestrator: ClassificationOrchestrator,
        notification_service: NotificationService,
        logging_service: LoggingService,
        correlation_id_factory: CorrelationIdFactory,
        poll_interval_seconds: int = 5,
    ) -> None:
        self._queue_repository = queue_repository
        self._pending_confirmation_repository = pending_confirmation_repository
        self._classification_orchestrator = classification_orchestrator
        self._notification_service = notification_service
        self._logging_service = logging_service
        self._correlation_id_factory = correlation_id_factory
        self._poll_interval_seconds = poll_interval_seconds

    @staticmethod
    def _build_confirmation_keyboard(confirmation_id: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Confirm",
                        callback_data=f"confirm:{confirmation_id}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Edit",
                        callback_data=f"edit:{confirmation_id}",
                    ),
                    InlineKeyboardButton(
                        text="Cancel",
                        callback_data=f"cancel:{confirmation_id}",
                    ),
                ],
            ]
        )

    async def run_forever(self, *, bot: Bot) -> None:
        self._logging_service.info(
            event=LogEvent.queue_worker_started,
            component="queue_worker",
            context=LogContext(
                trace_id="system:queue_worker",
                chat_id="system",
                user_id="system",
                message_id="system",
                processing_path="queue",
                status="STARTED",
            ),
            payload={
                "poll_interval_seconds": self._poll_interval_seconds,
                "queue_size": self._queue_repository.size(),
            },
        )
        while True:
            processed = await self.process_once(bot=bot)
            if not processed:
                await asyncio.sleep(self._poll_interval_seconds)

    async def process_once(self, *, bot: Bot) -> bool:
        task = await asyncio.to_thread(self._queue_repository.dequeue)
        if task is None:
            return False
        if task.queue_id is None:
            self._logging_service.error(
                event=LogEvent.queue_task_invalid,
                component="queue_worker",
                context=LogContext(
                    trace_id="unknown:unknown",
                    chat_id="unknown",
                    user_id="unknown",
                    message_id="unknown",
                    processing_path="queue",
                    status=ProcessingStatus.QUEUED.value,
                ),
                payload={"error_message": "Queue task without id cannot be processed"},
            )
            return True

        trace_id = self._correlation_id_factory.build_trace_id(task.chat_id, task.message_id)
        queue_latency_ms = max(0, int((datetime.now(tz=UTC) - task.enqueued_at).total_seconds() * 1000))
        self._logging_service.info(
            event=LogEvent.queue_dequeued,
            component="queue_worker",
            context=LogContext(
                trace_id=trace_id,
                chat_id=task.chat_id,
                user_id=task.user_id,
                message_id=task.message_id,
                processing_path="queue",
                status=ProcessingStatus.QUEUED.value,
            ),
            payload={
                "queue_id": task.queue_id,
                "queue_latency_ms": queue_latency_ms,
                "attempt_count": task.attempt_count,
                "next_attempt_at": task.next_attempt_at.astimezone(UTC)
                .isoformat(timespec="milliseconds")
                .replace("+00:00", "Z"),
            },
        )

        meta = build_message_meta(
            user_id=task.user_id,
            chat_id=task.chat_id,
            message_id=task.message_id,
            timestamp=task.received_at,
        )

        try:
            run_result = await asyncio.to_thread(
                self._classification_orchestrator.classify_from_queue,
                raw_text=task.raw_text,
                normalized_text=task.normalized_text,
                meta=meta,
            )
        except LLMTimeoutError:
            retry_result = await asyncio.to_thread(
                partial(
                    self._queue_repository.requeue,
                    task.queue_id,
                    error="llm_timeout",
                )
            )
            self._logging_service.info(
                event=LogEvent.queue_enqueued,
                component="queue_service",
                context=LogContext(
                    trace_id=trace_id,
                    chat_id=task.chat_id,
                    user_id=task.user_id,
                    message_id=task.message_id,
                    processing_path="queue",
                    status=ProcessingStatus.QUEUED.value,
                ),
                payload={
                    "queue_id": retry_result.queue_id,
                    "requeue_reason": "llm_timeout",
                    "attempt_count": retry_result.attempt_count,
                    "retry_delay_seconds": retry_result.retry_delay_seconds,
                    "next_attempt_at": retry_result.next_attempt_at.astimezone(UTC)
                    .isoformat(timespec="milliseconds")
                    .replace("+00:00", "Z"),
                },
            )
            return True
        except Exception as exc:
            retry_result = await asyncio.to_thread(
                partial(
                    self._queue_repository.requeue,
                    task.queue_id,
                    error=f"{type(exc).__name__}: {exc}",
                )
            )
            self._logging_service.error(
                event=LogEvent.queue_processing_failed,
                component="queue_worker",
                context=LogContext(
                    trace_id=trace_id,
                    chat_id=task.chat_id,
                    user_id=task.user_id,
                    message_id=task.message_id,
                    processing_path="queue",
                    status=ProcessingStatus.QUEUED.value,
                ),
                payload={
                    "queue_id": retry_result.queue_id,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                    "attempt_count": retry_result.attempt_count,
                    "retry_delay_seconds": retry_result.retry_delay_seconds,
                    "next_attempt_at": retry_result.next_attempt_at.astimezone(UTC)
                    .isoformat(timespec="milliseconds")
                    .replace("+00:00", "Z"),
                },
            )
            return True

        try:
            pending_confirmation = await asyncio.to_thread(
                self._pending_confirmation_repository.create,
                run_result.record,
            )
            await self._notification_service.send_post_factum_confirmation_request(
                bot=bot,
                chat_id=task.chat_id,
                user_id=task.user_id,
                message_id=task.message_id,
                classification_payload=run_result.record.classification.as_json_dict(),
                status=run_result.record.audit.status.value,
                reply_markup=self._build_confirmation_keyboard(
                    pending_confirmation.confirmation_id
                ),
            )
        except Exception as exc:
            if "pending_confirmation" in locals():
                await asyncio.to_thread(
                    self._pending_confirmation_repository.delete,
                    pending_confirmation.confirmation_id,
                )
            retry_result = await asyncio.to_thread(
                partial(
                    self._queue_repository.requeue,
                    task.queue_id,
                    error=f"notification_failed: {type(exc).__name__}: {exc}",
                )
            )
            self._logging_service.error(
                event=LogEvent.queue_processing_failed,
                component="queue_worker",
                context=LogContext(
                    trace_id=trace_id,
                    chat_id=task.chat_id,
                    user_id=task.user_id,
                    message_id=task.message_id,
                    processing_path="queue",
                    status=ProcessingStatus.QUEUED.value,
                ),
                payload={
                    "queue_id": retry_result.queue_id,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                    "failure_stage": "post_factum_confirmation_request",
                    "attempt_count": retry_result.attempt_count,
                    "retry_delay_seconds": retry_result.retry_delay_seconds,
                    "next_attempt_at": retry_result.next_attempt_at.astimezone(UTC)
                    .isoformat(timespec="milliseconds")
                    .replace("+00:00", "Z"),
                },
            )
            return True

        await asyncio.to_thread(self._queue_repository.mark_done, task.queue_id)
        return True
