from __future__ import annotations

from pathlib import Path

from telegram import (
    Bot,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext
from observability.log_events import LogEvent
from observability.logging_service import LoggingService


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
    _FIELD_LABELS: dict[str, str] = {
        "volume": "Volume",
        "unit": "Unit",
        "workType": "Work type",
        "stage": "Stage",
        "function": "Function",
        "comment": "Comment",
    }
    _MAX_COMMENT_PREVIEW_CHARS = 700

    def __init__(
        self,
        *,
        logging_service: LoggingService,
        correlation_id_factory: CorrelationIdFactory,
    ) -> None:
        self._logging_service = logging_service
        self._correlation_id_factory = correlation_id_factory
        self._help_text = (
            "Use Report Progress to send one fact.\n"
            "Use Get Reports to receive dashboard previews and optional PDFs.\n"
            "Next: tap Report Progress or Get Reports."
        )
        self._input_instruction_text = (
            "Send one progress fact in a single message ⌨️\n"
            "Next: type your report and press Send."
        )
        self._example_text = (
            "Example: Poured 20 m3 of concrete in gridlines 3-5.\n"
            "Next: send your own report."
        )
        self._welcome_text = (
            "Select an action.\n"
            "Next: choose Report Progress, Get Reports, or Help."
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
            sent = await target_message.reply_text(text=text, reply_markup=ReplyKeyboardRemove())
            try:
                await sent.edit_reply_markup(reply_markup=reply_markup)
            except Exception:
                await target_message.reply_text(
                    text="Quick actions.",
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
            "Cancelled.\nNext: choose an action.",
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
            "Review before saving to Google Sheets.\n"
            f"{formatted_payload}\n"
            f"Status: {status}\n"
            "Next: choose Confirm, Edit, or Cancel.",
            reply_markup=reply_markup,
        )

    async def send_processing_error(self, *, target_message: Message) -> None:
        await target_message.reply_text("Could not process. Try again.")

    async def send_report_selector(
        self,
        *,
        target_message: Message,
        reply_markup: InlineKeyboardMarkup,
    ) -> None:
        await target_message.reply_text(
            "Choose a report to export.",
            reply_markup=reply_markup,
        )

    async def send_dashboard_preparing(
        self,
        *,
        target_message: Message,
        report_title: str,
    ) -> None:
        await target_message.reply_text(f"Preparing {report_title} preview...")

    async def send_dashboard_unavailable(self, *, target_message: Message) -> None:
        await target_message.reply_text("Could not prepare the selected report. Try again.")

    async def send_dashboard_preview(
        self,
        *,
        target_message: Message,
        image_path: Path,
        report_title: str,
        worksheet_name: str,
        export_range: str,
        reply_markup: InlineKeyboardMarkup,
    ) -> None:
        with image_path.open("rb") as image_stream:
            await target_message.reply_photo(
                photo=image_stream,
                caption=(
                    f"{report_title} preview.\n"
                    "Send PDF version?"
                ),
                reply_markup=reply_markup,
            )

    async def send_dashboard_pdf(
        self,
        *,
        target_message: Message,
        pdf_path: Path,
    ) -> None:
        with pdf_path.open("rb") as pdf_stream:
            await target_message.reply_document(
                document=pdf_stream,
                filename=pdf_path.name,
                caption="PDF version.",
            )

    async def send_dashboard_pdf_unavailable(self, *, target_message: Message) -> None:
        await target_message.reply_text("Could not send the PDF. Generate the report again.")

    async def send_queued_notice(self, *, target_message: Message) -> None:
        await target_message.reply_text("Queued. I'll send a confirmation card when ready.")

    async def send_record_saved(
        self,
        *,
        target_message: Message,
        classification_payload: dict[str, str | int | float | None],
        status: str,
        reply_markup: InlineKeyboardMarkup,
    ) -> None:
        await target_message.reply_text(
            f"Saved.\nStatus: {status}\nNext: choose Report Another or Main Menu.",
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
                "Review before saving to Google Sheets.\n"
                f"{formatted_payload}\n"
                f"Status: {status}\n"
                "Next: choose Confirm, Edit, or Cancel."
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
            "Cancelled.\nNext: choose an action.",
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
            if display is None:
                continue
            label = cls._FIELD_LABELS.get(field, field)
            lines.append(f"- {label}: {display}")
        return "\n".join(lines) if lines else "- No structured fields extracted."

    @staticmethod
    def _format_scalar(value: str | int | float | None) -> str | None:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return str(value)
        normalized = value.strip()
        return normalized if normalized else None

    @classmethod
    def _format_comment_preview(cls, value: str | int | float | None) -> str | None:
        scalar = cls._format_scalar(value)
        if scalar is None:
            return None

        single_line = scalar.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " | ")
        if len(single_line) <= cls._MAX_COMMENT_PREVIEW_CHARS:
            return single_line

        omitted = len(single_line) - cls._MAX_COMMENT_PREVIEW_CHARS
        preview = single_line[: cls._MAX_COMMENT_PREVIEW_CHARS].rstrip()
        return f"{preview} ... [truncated {omitted} chars]"
