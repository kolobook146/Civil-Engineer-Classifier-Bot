from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from observability.correlation_id_factory import CorrelationIdFactory
from observability.logging_service import LoggingService
from presentation.notification_service import NotificationService


@dataclass
class _PhotoCall:
    caption: str
    reply_markup: InlineKeyboardMarkup


class _DummyMessage:
    def __init__(self) -> None:
        self.photo_calls: list[_PhotoCall] = []
        self.text_calls: list[str] = []

    async def reply_text(self, text: str, **kwargs) -> None:
        del kwargs
        self.text_calls.append(text)

    async def reply_photo(
        self,
        *,
        photo,
        caption: str,
        reply_markup: InlineKeyboardMarkup,
    ) -> None:
        self.photo_calls.append(_PhotoCall(caption=caption, reply_markup=reply_markup))


@pytest.mark.asyncio
async def test_dashboard_preview_caption_hides_sheet_and_range(tmp_path: Path) -> None:
    image_path = tmp_path / "report.jpg"
    image_path.write_bytes(b"jpeg-bytes")
    target_message = _DummyMessage()
    service = NotificationService(
        logging_service=LoggingService([]),
        correlation_id_factory=CorrelationIdFactory(),
    )
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Get PDF", callback_data="dashboard_pdf:export-id")]]
    )

    await service.send_dashboard_preview(
        target_message=target_message,
        image_path=image_path,
        report_title="Company Overview",
        worksheet_name="dashboard_visual",
        export_range="A1:X32",
        reply_markup=reply_markup,
    )

    assert target_message.photo_calls[0].caption == (
        "Company Overview preview.\n"
        "Send PDF version?"
    )
    assert "Sheet:" not in target_message.photo_calls[0].caption
    assert "Range:" not in target_message.photo_calls[0].caption
    assert target_message.photo_calls[0].reply_markup is reply_markup


@pytest.mark.asyncio
async def test_processing_error_explains_gemini_overload() -> None:
    target_message = _DummyMessage()
    service = NotificationService(
        logging_service=LoggingService([]),
        correlation_id_factory=CorrelationIdFactory(),
    )

    await service.send_processing_error(
        target_message=target_message,
        reason="model_overloaded",
    )

    assert target_message.text_calls == [
        "Gemini is temporarily overloaded. Please try again in a minute."
    ]
