from __future__ import annotations

import json

from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext
from observability.log_events import LogEvent
from observability.logging_service import LoggingService
from telegram import Bot, InlineKeyboardMarkup, Message


class NotificationService:
    """Outbound user messages for Telegram interactions."""

    def __init__(
        self,
        *,
        logging_service: LoggingService,
        correlation_id_factory: CorrelationIdFactory,
    ) -> None:
        self._logging_service = logging_service
        self._correlation_id_factory = correlation_id_factory
        self._welcome_text = (
            "Hello! I am a bot for recording completed construction work. "
            "Send a progress fact in free form, and I will extract volume, unit, "
            "work type, stage, function, and comment, then write the record to the sheet. "
            "Press \"Report Progress\" to begin."
        )
        self._input_instruction_text = (
            "Describe completed work in one free-form message. "
            "Example: \"Completed twenty cubic meters of concrete in axes 3-5.\" "
            "or \" Finished the tender for marketing activities \" "
            "You may write numbers in words and informal units; I will normalize them."
        )

    async def send_welcome(
        self,
        *,
        target_message: Message,
        reply_markup: InlineKeyboardMarkup,
    ) -> None:
        await target_message.reply_text(
            text=self._welcome_text,
            reply_markup=reply_markup,
        )

    async def send_input_instruction(self, *, target_message: Message) -> None:
        await target_message.reply_text(self._input_instruction_text)

    async def send_immediate_confirmation(
        self,
        *,
        target_message: Message,
        classification_payload: dict[str, str | None],
        status: str,
    ) -> None:
        formatted_payload = json.dumps(classification_payload, ensure_ascii=False)
        await target_message.reply_text(
            f"Recorded data: {formatted_payload}\n"
            f"Status: {status}"
        )

    async def send_processing_error(self, *, target_message: Message) -> None:
        await target_message.reply_text(
            "Failed to process the message. Please send it again."
        )

    async def send_queued_notice(self, *, target_message: Message) -> None:
        await target_message.reply_text(
            "LLM is busy, your message is queued. We will notify you once it is recorded."
        )

    async def send_post_factum_notification(
        self,
        *,
        bot: Bot,
        chat_id: str,
        user_id: str,
        message_id: str,
        classification_payload: dict[str, str | None],
        status: str,
    ) -> None:
        formatted_payload = json.dumps(classification_payload, ensure_ascii=False)
        chat_ref: int | str = int(chat_id) if chat_id.lstrip("-").isdigit() else chat_id
        await bot.send_message(
            chat_id=chat_ref,
            text=(
                "Queued message has been recorded.\n"
                f"Recorded data: {formatted_payload}\n"
                f"Status: {status}"
            ),
        )
        self._logging_service.info(
            event=LogEvent.post_factum_notification_sent,
            component="notification_service",
            context=LogContext(
                trace_id=self._correlation_id_factory.build_trace_id(chat_id, message_id),
                chat_id=chat_id,
                user_id=user_id,
                message_id=message_id,
                processing_path="queue",
                status=status,
            ),
        )
