from __future__ import annotations

import re
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest
import requests

from config.settings import GoogleSheetsSettings
from infrastructure.dashboard_sheets_exporter import (
    DASHBOARD_REPORTS,
    DashboardConversionError,
    DashboardExportArtifact,
    DashboardPdfNotFoundError,
    DashboardPdfWriteError,
    DashboardRangeParseError,
    DashboardReportNotFoundError,
    DashboardSheetsExporter,
    SheetGridRange,
)


def _build_settings(tmp_path: Path) -> GoogleSheetsSettings:
    service_account_file = tmp_path / "service-account.json"
    service_account_file.write_text("{}", encoding="utf-8")
    return GoogleSheetsSettings(
        service_account_file=service_account_file,
        spreadsheet_id="spreadsheet-123",
        worksheet_name="data_facts",
        dashboard_archive_dir=tmp_path / "dashboard_exports",
    )


def test_report_registry_contains_pilot_reports() -> None:
    reports = {report.report_id: report for report in DASHBOARD_REPORTS}

    assert set(reports) == {"company_overview", "monthly_controls", "departments"}
    assert reports["company_overview"].worksheet_name == "dashboard_visual"
    assert reports["company_overview"].export_range == "A1:X32"
    assert reports["company_overview"].title == "Company Overview"
    assert reports["company_overview"].pdf_scale == "2"
    assert reports["monthly_controls"].worksheet_name == "monthly_controls_a4"
    assert reports["monthly_controls"].export_range == "A1:AA38"
    assert reports["monthly_controls"].title == "Monthly Controls"
    assert reports["monthly_controls"].pdf_scale == "4"
    assert reports["departments"].worksheet_name == "departments_a4"
    assert reports["departments"].export_range == "A1:Z36"
    assert reports["departments"].title == "Departments Overview"
    assert reports["departments"].pdf_scale == "4"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (
            "A1:X32",
            SheetGridRange(
                start_row_index=0,
                end_row_index=32,
                start_column_index=0,
                end_column_index=24,
            ),
        ),
        (
            "A1:AA38",
            SheetGridRange(
                start_row_index=0,
                end_row_index=38,
                start_column_index=0,
                end_column_index=27,
            ),
        ),
        (
            "A1:Z36",
            SheetGridRange(
                start_row_index=0,
                end_row_index=36,
                start_column_index=0,
                end_column_index=26,
            ),
        ),
    ],
)
def test_parse_a1_range_returns_zero_based_bounds(
    value: str,
    expected: SheetGridRange,
) -> None:
    assert DashboardSheetsExporter.parse_a1_range(value) == expected


def test_parse_a1_range_rejects_invalid_range() -> None:
    with pytest.raises(DashboardRangeParseError):
        DashboardSheetsExporter.parse_a1_range("X38:A1")


def test_get_report_rejects_unknown_report_id() -> None:
    with pytest.raises(DashboardReportNotFoundError):
        DashboardSheetsExporter.get_report("unknown")


def test_build_pdf_export_url_uses_report_specific_single_page_a4_layout() -> None:
    url = DashboardSheetsExporter.build_pdf_export_url(
        spreadsheet_id="spreadsheet-123",
        worksheet_id=987654321,
        grid_range=SheetGridRange(
            start_row_index=0,
            end_row_index=32,
            start_column_index=0,
            end_column_index=24,
        ),
        scale="2",
    )

    assert "spreadsheets/d/spreadsheet-123/export" in url
    assert "gid=987654321" in url
    assert "r1=0" in url
    assert "c1=0" in url
    assert "r2=32" in url
    assert "c2=24" in url
    assert "size=7" in url
    assert "portrait=false" in url
    assert "scale=2" in url
    assert "left_margin=0" in url
    assert "right_margin=0" in url
    assert "fitw=" not in url


def test_convert_pdf_to_jpeg_maps_sips_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    exporter = DashboardSheetsExporter(_build_settings(tmp_path))
    pdf_path = tmp_path / "dashboard.pdf"
    image_path = tmp_path / "dashboard.jpg"
    pdf_path.write_bytes(b"%PDF-1.4")

    def _raise(*args, **kwargs):
        raise subprocess.CalledProcessError(returncode=1, cmd=args[0], stderr="boom")

    monkeypatch.setattr(subprocess, "run", _raise)

    with pytest.raises(DashboardConversionError):
        exporter._convert_pdf_to_jpeg(pdf_path, image_path)


def test_convert_pdf_to_jpeg_uses_extended_sips_timeout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    exporter = DashboardSheetsExporter(_build_settings(tmp_path))
    pdf_path = tmp_path / "dashboard.pdf"
    image_path = tmp_path / "dashboard.jpg"
    pdf_path.write_bytes(b"%PDF-1.4")

    def _fake_run(*args, **kwargs):
        assert kwargs["timeout"] == 120
        image_path.write_bytes(b"jpeg-bytes")
        return subprocess.CompletedProcess(args=args[0], returncode=0)

    monkeypatch.setattr(subprocess, "run", _fake_run)

    exporter._convert_pdf_to_jpeg(pdf_path, image_path)

    assert image_path.exists()


def test_download_dashboard_pdf_uses_extended_http_timeout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    exporter = DashboardSheetsExporter(_build_settings(tmp_path))

    class _Credentials:
        token = "token-123"

        def refresh(self, request) -> None:
            return None

    class _Response:
        content = b"%PDF-1.4"
        status_code = 200

        def raise_for_status(self) -> None:
            return None

    monkeypatch.setattr(exporter, "_build_readonly_credentials", lambda: _Credentials())

    def _fake_get(*args, **kwargs):
        assert kwargs["timeout"] == 120
        assert kwargs["headers"] == {"Authorization": "Bearer token-123"}
        return _Response()

    monkeypatch.setattr(requests, "get", _fake_get)

    assert exporter._download_dashboard_pdf("https://example.test/export") == b"%PDF-1.4"


def test_export_dashboard_preview_returns_archived_pdf_and_jpeg(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    exporter = DashboardSheetsExporter(_build_settings(tmp_path))
    monkeypatch.setattr(
        exporter,
        "_get_dashboard_worksheet",
        lambda worksheet_name: SimpleNamespace(title=worksheet_name, id=123456),
    )
    monkeypatch.setattr(exporter, "_download_dashboard_pdf", lambda _url: b"%PDF-1.4")
    monkeypatch.setattr(
        "infrastructure.dashboard_sheets_exporter.secrets.token_hex",
        lambda _bytes_count: "abc123ef",
    )

    def _fake_convert(pdf_path: Path, image_path: Path) -> None:
        assert pdf_path.exists()
        image_path.write_bytes(b"jpeg-bytes")

    monkeypatch.setattr(exporter, "_convert_pdf_to_jpeg", _fake_convert)

    artifact = exporter.export_dashboard_preview(report_id="company_overview")
    assert isinstance(artifact, DashboardExportArtifact)
    assert artifact.pdf_path.exists()
    assert artifact.image_path.exists()
    assert re.fullmatch(r"\d{8}T\d{6}Z_abc123ef", artifact.export_id)
    assert artifact.report_id == "company_overview"
    assert artifact.report_title == "Company Overview"
    assert artifact.pdf_file_name.startswith("company_overview_dashboard_visual_A1-X32_")
    assert artifact.pdf_file_name.endswith("_abc123ef.pdf")
    assert artifact.image_file_name.startswith("company_overview_dashboard_visual_A1-X32_")
    assert artifact.image_file_name.endswith("_abc123ef.jpg")
    assert artifact.output_format == "jpeg"
    assert artifact.worksheet_name == "dashboard_visual"
    assert artifact.export_range == "A1:X32"
    assert artifact.archive_dir == (_build_settings(tmp_path).dashboard_archive_dir.resolve())
    assert artifact.archive_dir.exists()


def test_export_dashboard_preview_removes_partial_files_on_convert_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    exporter = DashboardSheetsExporter(_build_settings(tmp_path))
    monkeypatch.setattr(
        exporter,
        "_get_dashboard_worksheet",
        lambda worksheet_name: SimpleNamespace(title=worksheet_name, id=123456),
    )
    monkeypatch.setattr(exporter, "_download_dashboard_pdf", lambda _url: b"%PDF-1.4")

    def _fail_convert(pdf_path: Path, image_path: Path) -> None:
        assert pdf_path.exists()
        image_path.write_bytes(b"partial-jpeg")
        raise DashboardConversionError("conversion failed")

    monkeypatch.setattr(exporter, "_convert_pdf_to_jpeg", _fail_convert)

    with pytest.raises(DashboardConversionError):
        exporter.export_dashboard_preview(report_id="company_overview")

    archive_dir = _build_settings(tmp_path).dashboard_archive_dir.resolve()
    assert archive_dir.exists()
    assert list(archive_dir.iterdir()) == []


def test_export_dashboard_preview_maps_pdf_write_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    exporter = DashboardSheetsExporter(_build_settings(tmp_path))
    monkeypatch.setattr(
        exporter,
        "_get_dashboard_worksheet",
        lambda worksheet_name: SimpleNamespace(title=worksheet_name, id=123456),
    )
    monkeypatch.setattr(exporter, "_download_dashboard_pdf", lambda _url: b"%PDF-1.4")
    monkeypatch.setattr(
        Path,
        "write_bytes",
        lambda self, data: (_ for _ in ()).throw(OSError("disk full")),
    )

    with pytest.raises(DashboardPdfWriteError):
        exporter.export_dashboard_preview(report_id="company_overview")


def test_resolve_dashboard_pdf_returns_archive_file(tmp_path: Path) -> None:
    exporter = DashboardSheetsExporter(_build_settings(tmp_path))
    archive_dir = _build_settings(tmp_path).dashboard_archive_dir.resolve()
    archive_dir.mkdir(parents=True)
    pdf_path = archive_dir / "company_overview_dashboard_visual_A1-X32_20260415T091523Z_abc123ef.pdf"
    pdf_path.write_bytes(b"%PDF-1.4")

    artifact = exporter.resolve_dashboard_pdf(export_id="20260415T091523Z_abc123ef")

    assert artifact.export_id == "20260415T091523Z_abc123ef"
    assert artifact.pdf_path == pdf_path
    assert artifact.pdf_file_name == pdf_path.name
    assert artifact.archive_dir == archive_dir


@pytest.mark.parametrize("export_id", ["../secret", "20260415T091523Z", "bad_abc123ef"])
def test_resolve_dashboard_pdf_rejects_invalid_export_id(
    tmp_path: Path,
    export_id: str,
) -> None:
    exporter = DashboardSheetsExporter(_build_settings(tmp_path))

    with pytest.raises(DashboardPdfNotFoundError):
        exporter.resolve_dashboard_pdf(export_id=export_id)


def test_resolve_dashboard_pdf_rejects_missing_archive_file(tmp_path: Path) -> None:
    exporter = DashboardSheetsExporter(_build_settings(tmp_path))

    with pytest.raises(DashboardPdfNotFoundError):
        exporter.resolve_dashboard_pdf(export_id="20260415T091523Z_abc123ef")
