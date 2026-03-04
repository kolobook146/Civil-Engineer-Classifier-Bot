from __future__ import annotations

from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext
from observability.log_events import LogEvent
from observability.logging_service import LoggingService
from telegram import (
    Bot,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


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
            "Main menu.\n"
            "Choose an action below. "
            "The bot can accept a progress report, show guidance, and provide an example."
        )
        self._help_text = (
            "How to use the bot:\n"
            "1. Press \"Report Progress\".\n"
            "2. Send one free-form text report.\n"
            "3. Review the extracted data.\n"
            "4. Confirm the record or correct the message."
        )
        self._input_instruction_text = (
            "Send one free-form progress update in a single message.\n"
            "For example: \"Poured 20 m3 of concrete in gridlines 3-5.\"\n"
            "Use the regular Telegram message field ⌨️ and the standard Send button. "
            "The buttons below only help: show an example or cancel input."
        )
        self._example_text = (
            "Example messages:\n"
            "• Poured 20 m3 of concrete in gridlines 3-5.\n"
            "• Completed the marketing tender.\n"
            "• Finished electrical installation for 12 m2 in room A."
        )

    async def send_welcome(
        self,
        *,
        target_message: Message,
        reply_markup: ReplyKeyboardMarkup,
    ) -> None:
        await target_message.reply_text(
            text=self._welcome_text,
            reply_markup=reply_markup,
        )

    async def send_help(
        self,
        *,
        target_message: Message,
        reply_markup: ReplyKeyboardMarkup,
    ) -> None:
        await target_message.reply_text(
            text=self._help_text,
            reply_markup=reply_markup,
        )

    async def send_input_instruction(
        self,
        *,
        target_message: Message,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | None = None,
        prefix_text: str | None = None,
    ) -> None:
        text = self._input_instruction_text
        if prefix_text:
            text = f"{prefix_text}\n\n{text}"
        if isinstance(reply_markup, InlineKeyboardMarkup):
            await target_message.reply_text(
                text=text,
                reply_markup=ReplyKeyboardRemove(),
            )
            await target_message.reply_text(
                text="Quick actions:",
                reply_markup=reply_markup,
            )
            return

        await target_message.reply_text(text=text, reply_markup=reply_markup)

    async def send_example(self, *, target_message: Message) -> None:
        await target_message.reply_text(self._example_text)

    async def send_input_cancelled(
        self,
        *,
        target_message: Message,
        reply_markup: ReplyKeyboardMarkup,
    ) -> None:
        await target_message.reply_text(
            "Input cancelled. You can return to the main menu or start a new entry later.",
            reply_markup=reply_markup,
        )

    async def send_confirmation_request(
        self,
        *,
        target_message: Message,
        classification_payload: dict[str, str | int | float | None],
        status: str,
        reply_markup: InlineKeyboardMarkup,
    ) -> None:
        formatted_payload = self._format_payload_for_user(classification_payload)
        await target_message.reply_text(
            "Review the data before writing to Google Sheets:\n"
            f"{formatted_payload}\n"
            f"Classification status: {status}",
            reply_markup=reply_markup,
        )

    async def send_processing_error(self, *, target_message: Message) -> None:
        await target_message.reply_text(
            "The message could not be processed. Please send it again."
        )

    async def send_queued_notice(self, *, target_message: Message) -> None:
        await target_message.reply_text(
            "The LLM is busy, so the message has been queued. "
            "Once processing is complete, I will send a confirmation card before saving."
        )

    async def send_record_saved(
        self,
        *,
        target_message: Message,
        classification_payload: dict[str, str | int | float | None],
        status: str,
        reply_markup: InlineKeyboardMarkup,
    ) -> None:
        formatted_payload = self._format_payload_for_user(classification_payload)
        await target_message.reply_text(
            "The data has been saved to Google Sheets:\n"
            f"{formatted_payload}\n"
            f"Status: {status}",
            reply_markup=reply_markup,
        )

    async def send_post_factum_confirmation_request(
        self,
        *,
        bot: Bot,
        chat_id: str,
        user_id: str,
        message_id: str,
        classification_payload: dict[str, str | int | float | None],
        status: str,
        reply_markup: InlineKeyboardMarkup,
    ) -> None:
        formatted_payload = self._format_payload_for_user(classification_payload)
        chat_ref: int | str = int(chat_id) if chat_id.lstrip("-").isdigit() else chat_id
        await bot.send_message(
            chat_id=chat_ref,
            text=(
                "The queued message has been processed. "
                "Review the data and confirm writing to Google Sheets:\n"
                f"{formatted_payload}\n"
                f"Classification status: {status}"
            ),
            reply_markup=reply_markup,
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

    async def send_pending_cancelled(
        self,
        *,
        target_message: Message,
        reply_markup: ReplyKeyboardMarkup,
    ) -> None:
        await target_message.reply_text(
            "The record was cancelled. You can return to the main menu or send a new report.",
            reply_markup=reply_markup,
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
