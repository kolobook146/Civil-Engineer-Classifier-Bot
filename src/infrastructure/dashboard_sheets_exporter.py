from __future__ import annotations

import re
import secrets
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlencode

import gspread
import requests
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from gspread.exceptions import WorksheetNotFound

from config.settings import GoogleSheetsSettings

_READONLY_SCOPES = (
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
)


@dataclass(frozen=True, slots=True)
class SheetGridRange:
    start_row_index: int
    end_row_index: int
    start_column_index: int
    end_column_index: int


@dataclass(frozen=True, slots=True)
class DashboardReportSpec:
    report_id: str
    title: str
    worksheet_name: str
    export_range: str
    pdf_scale: str


@dataclass(slots=True)
class DashboardExportArtifact:
    export_id: str
    report_id: str
    report_title: str
    pdf_path: Path
    image_path: Path
    pdf_file_name: str
    image_file_name: str
    output_format: str
    worksheet_name: str
    export_range: str
    archive_dir: Path


@dataclass(frozen=True, slots=True)
class DashboardPdfArtifact:
    export_id: str
    pdf_path: Path
    pdf_file_name: str
    archive_dir: Path


class DashboardExportError(RuntimeError):
    """Base dashboard export failure."""


class DashboardReportNotFoundError(DashboardExportError):
    """Requested report is not registered."""


class DashboardRangeParseError(DashboardExportError):
    """Invalid dashboard export range."""


class DashboardWorksheetNotFoundError(DashboardExportError):
    """Dashboard worksheet is missing."""


class DashboardPdfDownloadError(DashboardExportError):
    """Failed to download dashboard PDF."""


class DashboardPdfWriteError(DashboardExportError):
    """Failed to save dashboard PDF."""


class DashboardConversionError(DashboardExportError):
    """Failed to convert PDF to JPEG."""


class DashboardPdfNotFoundError(DashboardExportError):
    """Requested dashboard PDF archive artifact is missing."""


DASHBOARD_REPORTS: tuple[DashboardReportSpec, ...] = (
    DashboardReportSpec(
        report_id="company_overview",
        title="Company Overview",
        worksheet_name="dashboard_visual",
        export_range="A1:X32",
        pdf_scale="2",
    ),
    DashboardReportSpec(
        report_id="monthly_controls",
        title="Monthly Controls",
        worksheet_name="monthly_controls_a4",
        export_range="A1:AA38",
        pdf_scale="4",
    ),
    DashboardReportSpec(
        report_id="departments",
        title="Departments Overview",
        worksheet_name="departments_a4",
        export_range="A1:Z36",
        pdf_scale="4",
    ),
)

_DASHBOARD_REPORTS_BY_ID = {report.report_id: report for report in DASHBOARD_REPORTS}


class DashboardSheetsExporter:
    """Exports registered Google Sheets report ranges as JPEG previews."""

    _A1_RANGE_RE = re.compile(r"^\s*([A-Za-z]+)(\d+):([A-Za-z]+)(\d+)\s*$")
    _EXPORT_ID_RE = re.compile(r"^\d{8}T\d{6}Z_[0-9a-f]{8}$")
    _PDF_TIMEOUT_SECONDS = 120
    _SIPS_TIMEOUT_SECONDS = 120

    def __init__(self, settings: GoogleSheetsSettings) -> None:
        self._settings = settings
        self._worksheets_by_name = {}

    @property
    def output_format(self) -> str:
        return "jpeg"

    @property
    def archive_dir(self) -> Path:
        return self._settings.dashboard_archive_dir

    @classmethod
    def available_reports(cls) -> tuple[DashboardReportSpec, ...]:
        return DASHBOARD_REPORTS

    @classmethod
    def get_report(cls, report_id: str) -> DashboardReportSpec:
        try:
            return _DASHBOARD_REPORTS_BY_ID[report_id]
        except KeyError as exc:
            raise DashboardReportNotFoundError(f"Dashboard report not found: {report_id}") from exc

    def export_dashboard_preview(self, *, report_id: str) -> DashboardExportArtifact:
        report = self.get_report(report_id)
        worksheet = self._get_dashboard_worksheet(report.worksheet_name)
        grid_range = self.parse_a1_range(report.export_range)
        export_url = self.build_pdf_export_url(
            spreadsheet_id=self._settings.spreadsheet_id,
            worksheet_id=worksheet.id,
            grid_range=grid_range,
            scale=report.pdf_scale,
        )
        pdf_bytes = self._download_dashboard_pdf(export_url)
        archive_dir = self._resolve_archive_dir(self._settings.dashboard_archive_dir)
        export_id, file_stub = self._build_file_stub(report=report, worksheet_name=worksheet.title)
        pdf_path = archive_dir / f"{file_stub}.pdf"
        image_path = archive_dir / f"{file_stub}.jpg"
        created_paths = [pdf_path, image_path]

        try:
            pdf_path.write_bytes(pdf_bytes)
        except OSError as exc:
            self._cleanup_partial_files(created_paths)
            raise DashboardPdfWriteError("Failed to save dashboard PDF to archive") from exc

        try:
            self._convert_pdf_to_jpeg(pdf_path, image_path)
        except DashboardConversionError:
            self._cleanup_partial_files(created_paths)
            raise

        return DashboardExportArtifact(
            export_id=export_id,
            report_id=report.report_id,
            report_title=report.title,
            pdf_path=pdf_path,
            image_path=image_path,
            pdf_file_name=pdf_path.name,
            image_file_name=image_path.name,
            output_format=self.output_format,
            worksheet_name=worksheet.title,
            export_range=report.export_range,
            archive_dir=archive_dir,
        )

    def resolve_dashboard_pdf(self, *, export_id: str) -> DashboardPdfArtifact:
        if self._EXPORT_ID_RE.match(export_id) is None:
            raise DashboardPdfNotFoundError(f"Invalid dashboard export id: {export_id!r}")

        archive_dir = self._resolve_archive_dir(self._settings.dashboard_archive_dir)
        matches = sorted(archive_dir.glob(f"*_{export_id}.pdf"))
        if not matches:
            raise DashboardPdfNotFoundError(f"Dashboard PDF not found for export id: {export_id}")

        pdf_path = matches[-1].resolve()
        if pdf_path.parent != archive_dir:
            raise DashboardPdfNotFoundError(f"Dashboard PDF is outside archive: {export_id}")
        if not pdf_path.exists() or pdf_path.stat().st_size == 0:
            raise DashboardPdfNotFoundError(f"Dashboard PDF is empty or missing: {export_id}")

        return DashboardPdfArtifact(
            export_id=export_id,
            pdf_path=pdf_path,
            pdf_file_name=pdf_path.name,
            archive_dir=archive_dir,
        )

    @classmethod
    def parse_a1_range(cls, value: str) -> SheetGridRange:
        match = cls._A1_RANGE_RE.match(value)
        if match is None:
            raise DashboardRangeParseError(
                f"Dashboard export range must use A1 notation like A1:X32, got: {value!r}"
            )

        start_col, start_row, end_col, end_row = match.groups()
        start_row_num = int(start_row)
        end_row_num = int(end_row)
        start_col_num = cls._column_name_to_index(start_col)
        end_col_num = cls._column_name_to_index(end_col)

        if start_row_num <= 0 or end_row_num <= 0:
            raise DashboardRangeParseError(f"Row indexes must be positive in range: {value!r}")
        if start_row_num > end_row_num:
            raise DashboardRangeParseError(f"Start row must not exceed end row in range: {value!r}")
        if start_col_num > end_col_num:
            raise DashboardRangeParseError(
                f"Start column must not exceed end column in range: {value!r}"
            )

        return SheetGridRange(
            start_row_index=start_row_num - 1,
            end_row_index=end_row_num,
            start_column_index=start_col_num - 1,
            end_column_index=end_col_num,
        )

    @classmethod
    def build_pdf_export_url(
        cls,
        *,
        spreadsheet_id: str,
        worksheet_id: int,
        grid_range: SheetGridRange,
        scale: str,
    ) -> str:
        params = {
            "format": "pdf",
            "gid": worksheet_id,
            "size": "7",
            "portrait": "false",
            "scale": scale,
            "fzr": "true",
            "gridlines": "false",
            "printtitle": "false",
            "sheetnames": "false",
            "pagenum": "UNDEFINED",
            "attachment": "true",
            "top_margin": "0.25",
            "bottom_margin": "0.25",
            "left_margin": "0",
            "right_margin": "0",
            "r1": grid_range.start_row_index,
            "c1": grid_range.start_column_index,
            "r2": grid_range.end_row_index,
            "c2": grid_range.end_column_index,
        }
        return (
            f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?"
            f"{urlencode(params)}"
        )

    def _get_dashboard_worksheet(self, worksheet_name: str):
        if worksheet_name in self._worksheets_by_name:
            return self._worksheets_by_name[worksheet_name]

        service_account_path = self._resolve_service_account_path(
            self._settings.service_account_file
        )
        if not service_account_path.exists():
            raise FileNotFoundError(
                f"Google service account file not found: {service_account_path}"
            )

        client = gspread.authorize(self._build_readonly_credentials())
        spreadsheet = client.open_by_key(self._settings.spreadsheet_id)
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except WorksheetNotFound as exc:
            raise DashboardWorksheetNotFoundError(
                f"Dashboard worksheet not found: {worksheet_name}"
            ) from exc

        self._worksheets_by_name[worksheet_name] = worksheet
        return worksheet

    def _download_dashboard_pdf(self, export_url: str) -> bytes:
        credentials = self._build_readonly_credentials()
        credentials.refresh(Request())
        try:
            response = requests.get(
                export_url,
                headers={"Authorization": f"Bearer {credentials.token}"},
                timeout=self._PDF_TIMEOUT_SECONDS,
            )
        except requests.RequestException as exc:
            raise DashboardPdfDownloadError("Dashboard PDF export request failed") from exc
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise DashboardPdfDownloadError(
                f"Dashboard PDF export failed with HTTP {response.status_code}"
            ) from exc

        if not response.content:
            raise DashboardPdfDownloadError("Dashboard PDF export returned an empty response")

        return response.content

    def _convert_pdf_to_jpeg(self, pdf_path: Path, image_path: Path) -> None:
        try:
            subprocess.run(
                [
                    "/usr/bin/sips",
                    "-s",
                    "format",
                    "jpeg",
                    "-s",
                    "formatOptions",
                    "best",
                    str(pdf_path),
                    "--out",
                    str(image_path),
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=self._SIPS_TIMEOUT_SECONDS,
            )
        except (
            FileNotFoundError,
            subprocess.CalledProcessError,
            subprocess.TimeoutExpired,
        ) as exc:
            raise DashboardConversionError(
                "Failed to convert dashboard PDF to JPEG via sips"
            ) from exc

        if not image_path.exists() or image_path.stat().st_size == 0:
            raise DashboardConversionError("Dashboard JPEG was not created by sips")

    @staticmethod
    def _resolve_service_account_path(path: Path) -> Path:
        return path.expanduser().resolve()

    @staticmethod
    def _resolve_archive_dir(path: Path) -> Path:
        archive_dir = path.expanduser().resolve()
        archive_dir.mkdir(parents=True, exist_ok=True)
        return archive_dir

    @staticmethod
    def _cleanup_partial_files(paths: list[Path]) -> None:
        for path in reversed(paths):
            try:
                if path.exists():
                    path.unlink()
            except OSError:
                continue

    @classmethod
    def _build_file_stub(
        cls,
        *,
        report: DashboardReportSpec,
        worksheet_name: str,
    ) -> tuple[str, str]:
        timestamp = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
        export_id = f"{timestamp}_{secrets.token_hex(4)}"
        normalized_range = report.export_range.replace(":", "-")
        return (
            export_id,
            "_".join(
                [
                    cls._safe_filename_part(report.report_id),
                    cls._safe_filename_part(worksheet_name),
                    cls._safe_filename_part(normalized_range),
                    export_id,
                ]
            ),
        )

    def _build_readonly_credentials(self) -> Credentials:
        return Credentials.from_service_account_file(
            str(self._resolve_service_account_path(self._settings.service_account_file)),
            scopes=_READONLY_SCOPES,
        )

    @staticmethod
    def _column_name_to_index(value: str) -> int:
        result = 0
        for char in value.upper():
            if not ("A" <= char <= "Z"):
                raise DashboardRangeParseError(f"Invalid column name in export range: {value!r}")
            result = result * 26 + (ord(char) - ord("A") + 1)
        return result

    @staticmethod
    def _safe_filename_part(value: str) -> str:
        return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "unknown"
