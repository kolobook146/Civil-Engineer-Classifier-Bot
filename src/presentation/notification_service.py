from __future__ import annotations

from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext
from observability.log_events import LogEvent
from observability.logging_service import LoggingService
from telegram import Bot, InlineKeyboardMarkup, Message


class NotificationService:
    """Outbound user messages for Telegram interactions."""
    _FIELD_ORDER: tuple[str, ...] = (
        "volume",
        "unit",
        "workType",
        "stage",
        "function",
        "comment",
    )
    _MAX_COMMENT_PREVIEW_CHARS = 700

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
        classification_payload: dict[str, str | int | float | None],
        status: str,
    ) -> None:
        formatted_payload = self._format_payload_for_user(classification_payload)
        await target_message.reply_text(
            f"Recorded data:\n{formatted_payload}\n"
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
        classification_payload: dict[str, str | int | float | None],
        status: str,
    ) -> None:
        formatted_payload = self._format_payload_for_user(classification_payload)
        chat_ref: int | str = int(chat_id) if chat_id.lstrip("-").isdigit() else chat_id
        await bot.send_message(
            chat_id=chat_ref,
            text=(
                "Queued message has been recorded.\n"
                f"Recorded data:\n{formatted_payload}\n"
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

    @classmethod
    def _format_payload_for_user(cls, payload: dict[str, str | int | float | None]) -> str:
        lines: list[str] = []
        for field in cls._FIELD_ORDER:
            value = payload.get(field)
            if field == "comment":
                display = cls._format_comment_preview(value)
            else:
                display = cls._format_scalar(value)
            lines.append(f"- {field}: {display}")
        return "\n".join(lines)

    @staticmethod
    def _format_scalar(value: str | int | float | None) -> str:
        if value is None:
            return "null"
        if isinstance(value, (int, float)):
            return str(value)
        normalized = value.strip()
        return normalized if normalized else "null"

    @classmethod
    def _format_comment_preview(cls, value: str | int | float | None) -> str:
        scalar = cls._format_scalar(value)
        if scalar == "null":
            return scalar

        single_line = scalar.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " | ")
        if len(single_line) <= cls._MAX_COMMENT_PREVIEW_CHARS:
            return single_line

        omitted = len(single_line) - cls._MAX_COMMENT_PREVIEW_CHARS
        preview = single_line[: cls._MAX_COMMENT_PREVIEW_CHARS].rstrip()
        return f"{preview} ... [truncated {omitted} chars]"
