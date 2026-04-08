from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

from application.message_preprocessor import MessagePreprocessor
from infrastructure.dashboard_sheets_exporter import (
    DashboardConversionError,
    DashboardExportArtifact,
)
from observability.correlation_id_factory import CorrelationIdFactory
from observability.logging_service import LoggingService
from presentation.telegram_polling_handler import TelegramPollingHandler


class _RecordingSink:
    def __init__(self) -> None:
        self.records: list[dict[str, object]] = []

    def emit(self, record: dict[str, object]) -> None:
        self.records.append(record)


class _NotificationStub:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    async def send_dashboard_preparing(self, *, target_message) -> None:
        self.calls.append(("preparing", target_message))

    async def send_dashboard_preview(
        self,
        *,
        target_message,
        image_path: Path,
        worksheet_name: str,
        export_range: str,
    ) -> None:
        self.calls.append(("preview", image_path.name, worksheet_name, export_range))

    async def send_dashboard_unavailable(self, *, target_message) -> None:
        self.calls.append(("unavailable", target_message))

    async def send_input_instruction(self, **kwargs) -> None:
        self.calls.append(("input", kwargs))

    async def send_help(self, **kwargs) -> None:
        self.calls.append(("help", kwargs))

    async def send_welcome(self, **kwargs) -> None:
        self.calls.append(("welcome", kwargs))


class _DashboardExporterStub:
    worksheet_name = "dashboard_visual"
    export_range = "A1:X38"
    output_format = "jpeg"

    def __init__(
        self,
        *,
        artifact: DashboardExportArtifact | None = None,
        error: Exception | None = None,
    ) -> None:
        self._artifact = artifact
        self._error = error

    def export_dashboard_preview(self) -> DashboardExportArtifact:
        if self._error is not None:
            raise self._error
        assert self._artifact is not None
        return self._artifact


@dataclass
class _DummyMessage:
    text: str
    message_id: int = 101
    date: datetime = datetime(2026, 4, 8, tzinfo=UTC)


@dataclass
class _DummyChat:
    id: int = 12345


@dataclass
class _DummyUser:
    id: int = 55


def _build_handler(
    notification_service,
    dashboard_exporter,
    logging_service: LoggingService,
) -> TelegramPollingHandler:
    return TelegramPollingHandler(
        notification_service=notification_service,
        message_preprocessor=MessagePreprocessor(),
        classification_orchestrator=SimpleNamespace(),
        dashboard_exporter=dashboard_exporter,
        queue_repository=SimpleNamespace(),
        pending_confirmation_repository=SimpleNamespace(),
        logging_service=logging_service,
        correlation_id_factory=CorrelationIdFactory(),
    )


@pytest.mark.asyncio
async def test_dashboard_button_sends_preview_and_logs_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    temp_dir = tmp_path / "artifact"
    temp_dir.mkdir()
    image_path = temp_dir / "dashboard_visual_A1-X38.jpg"
    image_path.write_bytes(b"jpeg-bytes")
    artifact = DashboardExportArtifact(
        pdf_path=temp_dir / "dashboard_visual_A1-X38.pdf",
        image_path=image_path,
        pdf_file_name="dashboard_visual_A1-X38.pdf",
        image_file_name=image_path.name,
        output_format="jpeg",
        worksheet_name="dashboard_visual",
        export_range="A1:X38",
        archive_dir=temp_dir,
    )
    artifact.pdf_path.write_bytes(b"%PDF-1.4")
    notification_service = _NotificationStub()
    sink = _RecordingSink()
    logging_service = LoggingService([sink])
    handler = _build_handler(
        notification_service,
        _DashboardExporterStub(artifact=artifact),
        logging_service,
    )

    async def _inline_to_thread(func, /, *args, **kwargs):
        return func(*args, **kwargs)

    monkeypatch.setattr(asyncio, "to_thread", _inline_to_thread)

    update = SimpleNamespace(
        effective_message=_DummyMessage(text="Dashboard"),
        effective_chat=_DummyChat(),
        effective_user=_DummyUser(),
    )

    await handler.free_text_handler(update, None)

    assert notification_service.calls[0][0] == "preparing"
    assert notification_service.calls[1] == (
        "preview",
        "dashboard_visual_A1-X38.jpg",
        "dashboard_visual",
        "A1:X38",
    )
    assert any(record["event"] == "dashboard_export_requested" for record in sink.records)
    success_log = next(
        record
        for record in sink.records
        if record["event"] == "dashboard_export_succeeded"
    )
    assert success_log["archive_dir"] == str(temp_dir)
    assert success_log["pdf_file_name"] == "dashboard_visual_A1-X38.pdf"
    assert success_log["image_file_name"] == "dashboard_visual_A1-X38.jpg"
    assert temp_dir.exists()
    assert artifact.image_path.exists()
    assert artifact.pdf_path.exists()


@pytest.mark.asyncio
async def test_dashboard_button_handles_export_failure_and_logs_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    notification_service = _NotificationStub()
    sink = _RecordingSink()
    logging_service = LoggingService([sink])
    handler = _build_handler(
        notification_service,
        _DashboardExporterStub(error=DashboardConversionError("conversion failed")),
        logging_service,
    )

    async def _inline_to_thread(func, /, *args, **kwargs):
        return func(*args, **kwargs)

    monkeypatch.setattr(asyncio, "to_thread", _inline_to_thread)

    update = SimpleNamespace(
        effective_message=_DummyMessage(text="Dashboard"),
        effective_chat=_DummyChat(),
        effective_user=_DummyUser(),
    )

    await handler.free_text_handler(update, None)

    assert notification_service.calls[0][0] == "preparing"
    assert notification_service.calls[1][0] == "unavailable"
    assert any(record["event"] == "dashboard_export_requested" for record in sink.records)
    assert any(record["event"] == "dashboard_export_failed" for record in sink.records)
