from __future__ import annotations

import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from config.settings import GoogleSheetsSettings
from infrastructure.dashboard_sheets_exporter import (
    DashboardConversionError,
    DashboardExportArtifact,
    DashboardPdfWriteError,
    DashboardRangeParseError,
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
        dashboard_worksheet_name="dashboard_visual",
        dashboard_export_range="A1:X38",
        dashboard_archive_dir=tmp_path / "dashboard_exports",
    )


def test_parse_a1_range_returns_zero_based_bounds() -> None:
    result = DashboardSheetsExporter.parse_a1_range("A1:X38")

    assert result == SheetGridRange(
        start_row_index=0,
        end_row_index=38,
        start_column_index=0,
        end_column_index=24,
    )


def test_parse_a1_range_rejects_invalid_range() -> None:
    with pytest.raises(DashboardRangeParseError):
        DashboardSheetsExporter.parse_a1_range("X38:A1")


def test_build_pdf_export_url_uses_single_page_a4_dashboard_layout() -> None:
    url = DashboardSheetsExporter.build_pdf_export_url(
        spreadsheet_id="spreadsheet-123",
        worksheet_id=987654321,
        grid_range=SheetGridRange(
            start_row_index=0,
            end_row_index=38,
            start_column_index=0,
            end_column_index=24,
        ),
    )

    assert "spreadsheets/d/spreadsheet-123/export" in url
    assert "gid=987654321" in url
    assert "r1=0" in url
    assert "c1=0" in url
    assert "r2=38" in url
    assert "c2=24" in url
    assert "size=7" in url
    assert "portrait=false" in url
    assert "scale=3" in url
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


def test_export_dashboard_preview_returns_archived_pdf_and_jpeg(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    exporter = DashboardSheetsExporter(_build_settings(tmp_path))
    monkeypatch.setattr(
        exporter,
        "_get_dashboard_worksheet",
        lambda: SimpleNamespace(title="dashboard_visual", id=123456),
    )
    monkeypatch.setattr(exporter, "_download_dashboard_pdf", lambda _url: b"%PDF-1.4")

    def _fake_convert(pdf_path: Path, image_path: Path) -> None:
        assert pdf_path.exists()
        image_path.write_bytes(b"jpeg-bytes")

    monkeypatch.setattr(exporter, "_convert_pdf_to_jpeg", _fake_convert)

    artifact = exporter.export_dashboard_preview()
    assert isinstance(artifact, DashboardExportArtifact)
    assert artifact.pdf_path.exists()
    assert artifact.image_path.exists()
    assert artifact.pdf_file_name.startswith("dashboard_visual_A1-X38_")
    assert artifact.pdf_file_name.endswith(".pdf")
    assert artifact.image_file_name.startswith("dashboard_visual_A1-X38_")
    assert artifact.image_file_name.endswith(".jpg")
    assert artifact.output_format == "jpeg"
    assert artifact.worksheet_name == "dashboard_visual"
    assert artifact.export_range == "A1:X38"
    assert artifact.archive_dir == (_build_settings(tmp_path).dashboard_archive_dir.resolve())
    assert artifact.archive_dir.exists()


def test_export_dashboard_preview_removes_partial_pdf_on_convert_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    exporter = DashboardSheetsExporter(_build_settings(tmp_path))
    monkeypatch.setattr(
        exporter,
        "_get_dashboard_worksheet",
        lambda: SimpleNamespace(title="dashboard_visual", id=123456),
    )
    monkeypatch.setattr(exporter, "_download_dashboard_pdf", lambda _url: b"%PDF-1.4")

    def _fail_convert(pdf_path: Path, image_path: Path) -> None:
        assert pdf_path.exists()
        raise DashboardConversionError("conversion failed")

    monkeypatch.setattr(exporter, "_convert_pdf_to_jpeg", _fail_convert)

    with pytest.raises(DashboardConversionError):
        exporter.export_dashboard_preview()

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
        lambda: SimpleNamespace(title="dashboard_visual", id=123456),
    )
    monkeypatch.setattr(exporter, "_download_dashboard_pdf", lambda _url: b"%PDF-1.4")
    monkeypatch.setattr(
        Path,
        "write_bytes",
        lambda self, data: (_ for _ in ()).throw(OSError("disk full")),
    )

    with pytest.raises(DashboardPdfWriteError):
        exporter.export_dashboard_preview()
