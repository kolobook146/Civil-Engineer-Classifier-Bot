from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

from application.message_preprocessor import MessagePreprocessor
from infrastructure.dashboard_sheets_exporter import (
    DASHBOARD_REPORTS,
    DashboardConversionError,
    DashboardExportArtifact,
    DashboardPdfArtifact,
    DashboardPdfNotFoundError,
    DashboardReportNotFoundError,
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
        self.calls: list[tuple] = []

    async def send_report_selector(self, *, target_message, reply_markup) -> None:
        labels = [button.text for row in reply_markup.inline_keyboard for button in row]
        self.calls.append(("selector", labels))

    async def send_dashboard_preparing(self, *, target_message, report_title: str) -> None:
        self.calls.append(("preparing", report_title))

    async def send_dashboard_preview(
        self,
        *,
        target_message,
        image_path: Path,
        report_title: str,
        worksheet_name: str,
        export_range: str,
        reply_markup,
    ) -> None:
        labels = [button.text for row in reply_markup.inline_keyboard for button in row]
        callbacks = [button.callback_data for row in reply_markup.inline_keyboard for button in row]
        self.calls.append(
            (
                "preview",
                image_path.name,
                report_title,
                worksheet_name,
                export_range,
                labels,
                callbacks,
            )
        )

    async def send_dashboard_pdf(self, *, target_message, pdf_path: Path) -> None:
        self.calls.append(("pdf", pdf_path.name))

    async def send_dashboard_pdf_unavailable(self, *, target_message) -> None:
        self.calls.append(("pdf_unavailable", target_message))

    async def send_dashboard_unavailable(self, *, target_message) -> None:
        self.calls.append(("unavailable", target_message))

    async def send_input_instruction(self, **kwargs) -> None:
        self.calls.append(("input", kwargs))

    async def send_help(self, **kwargs) -> None:
        self.calls.append(("help", kwargs))

    async def send_welcome(self, **kwargs) -> None:
        self.calls.append(("welcome", kwargs))


class _DashboardExporterStub:
    output_format = "jpeg"

    def __init__(
        self,
        *,
        artifact: DashboardExportArtifact | None = None,
        error: Exception | None = None,
        pdf_artifact: DashboardPdfArtifact | None = None,
        pdf_error: Exception | None = None,
    ) -> None:
        self._artifact = artifact
        self._error = error
        self._pdf_artifact = pdf_artifact
        self._pdf_error = pdf_error
        self.requested_report_id: str | None = None
        self.requested_export_id: str | None = None

    def available_reports(self):
        return DASHBOARD_REPORTS

    def get_report(self, report_id: str):
        for report in DASHBOARD_REPORTS:
            if report.report_id == report_id:
                return report
        raise DashboardReportNotFoundError(report_id)

    def export_dashboard_preview(self, *, report_id: str) -> DashboardExportArtifact:
        self.requested_report_id = report_id
        if self._error is not None:
            raise self._error
        assert self._artifact is not None
        return self._artifact

    def resolve_dashboard_pdf(self, *, export_id: str) -> DashboardPdfArtifact:
        self.requested_export_id = export_id
        if self._pdf_error is not None:
            raise self._pdf_error
        assert self._pdf_artifact is not None
        return self._pdf_artifact


@dataclass
class _DummyMessage:
    text: str = ""
    message_id: int = 101
    date: datetime = datetime(2026, 4, 8, tzinfo=UTC)


@dataclass
class _DummyCallbackQuery:
    data: str
    message: _DummyMessage | None = field(default_factory=_DummyMessage)
    answers: list[str | None] = field(default_factory=list)
    cleared: bool = False

    async def answer(self, text: str | None = None) -> None:
        self.answers.append(text)

    async def edit_message_reply_markup(self, *, reply_markup=None) -> None:
        self.cleared = reply_markup is None


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


def _build_update(*, message=None, callback_query=None):
    return SimpleNamespace(
        effective_message=message,
        callback_query=callback_query,
        effective_chat=_DummyChat(),
        effective_user=_DummyUser(),
    )


def test_processing_error_reason_detects_gemini_overload() -> None:
    exc = Exception(
        "503 UNAVAILABLE. This model is currently experiencing high demand."
    )

    assert TelegramPollingHandler._processing_error_reason(exc) == "model_overloaded"


@pytest.mark.asyncio
async def test_get_reports_button_sends_report_selector() -> None:
    notification_service = _NotificationStub()
    sink = _RecordingSink()
    handler = _build_handler(
        notification_service,
        _DashboardExporterStub(),
        LoggingService([sink]),
    )
    update = _build_update(message=_DummyMessage(text="Get Reports"))

    await handler.free_text_handler(update, None)

    assert notification_service.calls == [
        (
            "selector",
            ["Company Overview", "Monthly Controls", "Departments Overview", "Main Menu"],
        )
    ]


@pytest.mark.asyncio
async def test_dashboard_report_callback_sends_preview_and_logs_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    temp_dir = tmp_path / "artifact"
    temp_dir.mkdir()
    image_path = temp_dir / "company_overview_dashboard_visual_A1-X32_20260408T104535Z_abc123ef.jpg"
    image_path.write_bytes(b"jpeg-bytes")
    artifact = DashboardExportArtifact(
        export_id="20260408T104535Z_abc123ef",
        report_id="company_overview",
        report_title="Company Overview",
        pdf_path=temp_dir / "company_overview_dashboard_visual_A1-X32_20260408T104535Z_abc123ef.pdf",
        image_path=image_path,
        pdf_file_name="company_overview_dashboard_visual_A1-X32_20260408T104535Z_abc123ef.pdf",
        image_file_name=image_path.name,
        output_format="jpeg",
        worksheet_name="dashboard_visual",
        export_range="A1:X32",
        archive_dir=temp_dir,
    )
    artifact.pdf_path.write_bytes(b"%PDF-1.4")
    notification_service = _NotificationStub()
    sink = _RecordingSink()
    exporter = _DashboardExporterStub(artifact=artifact)
    handler = _build_handler(notification_service, exporter, LoggingService([sink]))

    async def _inline_to_thread(func, /, *args, **kwargs):
        return func(*args, **kwargs)

    monkeypatch.setattr(asyncio, "to_thread", _inline_to_thread)

    query = _DummyCallbackQuery(data="dashboard_report:company_overview")
    update = _build_update(callback_query=query)

    await handler.dashboard_report_callback(update, None)

    assert query.cleared is True
    assert query.answers == ["Preparing Company Overview..."]
    assert exporter.requested_report_id == "company_overview"
    assert notification_service.calls[0] == ("preparing", "Company Overview")
    assert notification_service.calls[1] == (
        "preview",
        image_path.name,
        "Company Overview",
        "dashboard_visual",
        "A1:X32",
        ["Get PDF", "Main Menu"],
        ["dashboard_pdf:20260408T104535Z_abc123ef", "main_menu"],
    )
    assert any(record["event"] == "dashboard_export_requested" for record in sink.records)
    success_log = next(
        record
        for record in sink.records
        if record["event"] == "dashboard_export_succeeded"
    )
    assert success_log["report_id"] == "company_overview"
    assert success_log["report_title"] == "Company Overview"
    assert success_log["export_id"] == "20260408T104535Z_abc123ef"
    assert success_log["pdf_file_name"] == artifact.pdf_file_name
    assert success_log["image_file_name"] == artifact.image_file_name


@pytest.mark.asyncio
async def test_dashboard_report_callback_handles_export_failure_and_logs_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    notification_service = _NotificationStub()
    sink = _RecordingSink()
    handler = _build_handler(
        notification_service,
        _DashboardExporterStub(error=DashboardConversionError("conversion failed")),
        LoggingService([sink]),
    )

    async def _inline_to_thread(func, /, *args, **kwargs):
        return func(*args, **kwargs)

    monkeypatch.setattr(asyncio, "to_thread", _inline_to_thread)

    query = _DummyCallbackQuery(data="dashboard_report:company_overview")
    update = _build_update(callback_query=query)

    await handler.dashboard_report_callback(update, None)

    assert notification_service.calls[0] == ("preparing", "Company Overview")
    assert notification_service.calls[1][0] == "unavailable"
    assert any(record["event"] == "dashboard_export_requested" for record in sink.records)
    failure_log = next(
        record for record in sink.records if record["event"] == "dashboard_export_failed"
    )
    assert failure_log["report_id"] == "company_overview"
    assert failure_log["failure_stage"] == "jpeg_convert"


@pytest.mark.asyncio
async def test_dashboard_pdf_callback_sends_archived_pdf_and_returns_to_main_menu(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pdf_path = tmp_path / "company_overview_dashboard_visual_A1-X32_20260408T104535Z_abc123ef.pdf"
    pdf_path.write_bytes(b"%PDF-1.4")
    pdf_artifact = DashboardPdfArtifact(
        export_id="20260408T104535Z_abc123ef",
        pdf_path=pdf_path,
        pdf_file_name=pdf_path.name,
        archive_dir=tmp_path,
    )
    notification_service = _NotificationStub()
    sink = _RecordingSink()
    exporter = _DashboardExporterStub(pdf_artifact=pdf_artifact)
    handler = _build_handler(notification_service, exporter, LoggingService([sink]))

    async def _inline_to_thread(func, /, *args, **kwargs):
        return func(*args, **kwargs)

    monkeypatch.setattr(asyncio, "to_thread", _inline_to_thread)

    query = _DummyCallbackQuery(data="dashboard_pdf:20260408T104535Z_abc123ef")
    update = _build_update(callback_query=query)

    await handler.dashboard_pdf_callback(update, None)

    assert query.cleared is True
    assert query.answers == ["Sending PDF..."]
    assert exporter.requested_export_id == "20260408T104535Z_abc123ef"
    assert notification_service.calls[0] == ("pdf", pdf_path.name)
    assert notification_service.calls[1][0] == "welcome"
    assert any(record["event"] == "dashboard_pdf_requested" for record in sink.records)
    success_log = next(record for record in sink.records if record["event"] == "dashboard_pdf_sent")
    assert success_log["export_id"] == "20260408T104535Z_abc123ef"
    assert success_log["pdf_file_name"] == pdf_path.name


@pytest.mark.asyncio
async def test_dashboard_pdf_callback_handles_missing_pdf_and_returns_to_main_menu(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    notification_service = _NotificationStub()
    sink = _RecordingSink()
    handler = _build_handler(
        notification_service,
        _DashboardExporterStub(pdf_error=DashboardPdfNotFoundError("missing")),
        LoggingService([sink]),
    )

    async def _inline_to_thread(func, /, *args, **kwargs):
        return func(*args, **kwargs)

    monkeypatch.setattr(asyncio, "to_thread", _inline_to_thread)

    query = _DummyCallbackQuery(data="dashboard_pdf:20260408T104535Z_abc123ef")
    update = _build_update(callback_query=query)

    await handler.dashboard_pdf_callback(update, None)

    assert notification_service.calls[0][0] == "pdf_unavailable"
    assert notification_service.calls[1][0] == "welcome"
    failure_log = next(record for record in sink.records if record["event"] == "dashboard_pdf_failed")
    assert failure_log["export_id"] == "20260408T104535Z_abc123ef"
    assert failure_log["failure_stage"] == "pdf_lookup"
