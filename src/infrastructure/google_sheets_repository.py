from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Final

import gspread
from gspread.exceptions import WorksheetNotFound

from config.settings import GoogleSheetsSettings
from domain.enums import ProcessingStatus
from domain.models import DataFactRecord
from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext, ProcessingPath
from observability.log_events import LogEvent
from observability.logging_service import LoggingService

_DEFAULT_COLUMNS: Final[tuple[str, ...]] = (
    "raw_text",
    "volume",
    "unit",
    "work_type",
    "stage",
    "function",
    "comment",
    "timestamp",
    "user_id",
    "chat_id",
    "message_id",
    "model",
    "classifier_version",
    "status",
)
_LEGACY_HEADER_ALIASES: Final[dict[str, str]] = {
    "workType": "work_type",
}


@dataclass(frozen=True, slots=True)
class AppendResult:
    updated_range: str | None


class GoogleSheetsRepository:
    """Persists classification facts to Google Sheets worksheet `data_facts`."""

    def __init__(
        self,
        settings: GoogleSheetsSettings,
        *,
        logging_service: LoggingService,
        correlation_id_factory: CorrelationIdFactory,
    ) -> None:
        self._settings = settings
        self._logging_service = logging_service
        self._correlation_id_factory = correlation_id_factory
        self._worksheet = None

    def append_data_fact(self, record: DataFactRecord) -> AppendResult:
        try:
            worksheet = self._get_or_create_worksheet()
            headers = self._ensure_headers(worksheet)
            row_payload = self._build_row_payload(record)
            row_values = [row_payload.get(column, "") for column in headers]

            response = worksheet.append_row(row_values, value_input_option="USER_ENTERED")
            updated_range = None
            if isinstance(response, dict):
                updates = response.get("updates", {})
                if isinstance(updates, dict):
                    updated_range = updates.get("updatedRange")
            sheets_row_index = self._extract_row_index(updated_range)

            self._logging_service.info(
                event=LogEvent.sheets_write_success,
                component="google_sheets_repository",
                context=self._build_context(record),
                payload={
                    "sheet_name": worksheet.title,
                    "updated_range": updated_range,
                    "sheets_row_index": sheets_row_index,
                },
            )
            return AppendResult(updated_range=updated_range)
        except Exception as exc:
            self._logging_service.error(
                event=LogEvent.sheets_write_failed,
                component="google_sheets_repository",
                context=self._build_context(record),
                payload={
                    "sheet_name": self._settings.worksheet_name,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
            raise

    def appendDataFact(self, record: DataFactRecord) -> AppendResult:
        """Compatibility alias with UML naming."""
        return self.append_data_fact(record)

    def _get_or_create_worksheet(self):
        if self._worksheet is not None:
            return self._worksheet

        service_account_path = self._resolve_service_account_path(self._settings.service_account_file)
        if not service_account_path.exists():
            raise FileNotFoundError(
                f"Google service account file not found: {service_account_path}"
            )

        client = gspread.service_account(filename=str(service_account_path))
        spreadsheet = client.open_by_key(self._settings.spreadsheet_id)

        try:
            worksheet = spreadsheet.worksheet(self._settings.worksheet_name)
        except WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(
                title=self._settings.worksheet_name,
                rows=1000,
                cols=32,
            )

        self._worksheet = worksheet
        return worksheet

    @staticmethod
    def _resolve_service_account_path(path: Path) -> Path:
        return path.expanduser().resolve()

    def _ensure_headers(self, worksheet) -> list[str]:
        header_row = worksheet.row_values(1)
        if not header_row:
            headers = list(_DEFAULT_COLUMNS)
            worksheet.update("A1", [headers])
            return headers

        original_headers = [cell.strip() for cell in header_row if cell.strip()]
        headers = self._normalize_headers(original_headers)
        missing_columns = [column for column in _DEFAULT_COLUMNS if column not in headers]
        if missing_columns:
            headers.extend(missing_columns)

        if headers != original_headers:
            worksheet.update("A1", [headers])

        return headers

    @staticmethod
    def _normalize_headers(headers: list[str]) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()
        for column in headers:
            canonical = _LEGACY_HEADER_ALIASES.get(column, column)
            if canonical in seen:
                continue
            normalized.append(canonical)
            seen.add(canonical)
        return normalized

    @staticmethod
    def _build_row_payload(record: DataFactRecord) -> dict[str, str]:
        classification = record.classification
        audit = record.audit

        timestamp = audit.timestamp
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=UTC)

        return {
            "raw_text": record.raw_text,
            "volume": GoogleSheetsRepository._format_volume(classification.volume),
            "unit": classification.unit or "",
            "work_type": classification.work_type or "",
            "stage": classification.stage or "",
            "function": classification.function or "",
            "comment": classification.comment or "",
            "timestamp": GoogleSheetsRepository._iso8601(timestamp),
            "user_id": audit.user_id,
            "chat_id": audit.chat_id,
            "message_id": audit.message_id,
            "model": audit.model,
            "classifier_version": audit.classifier_version,
            "status": audit.status.value,
        }

    @staticmethod
    def _format_volume(value: Decimal | None) -> str:
        if value is None:
            return ""
        text = format(value, "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        return text

    @staticmethod
    def _iso8601(value: datetime) -> str:
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _extract_row_index(updated_range: str | None) -> int | None:
        if not updated_range:
            return None

        # Example: "data_facts!A152:N152"
        tail = updated_range.split("!")[-1]
        match = re.search(r"[A-Z]+(\d+)(?::[A-Z]+(\d+))?$", tail)
        if match is None:
            return None
        return int(match.group(1))

    def _build_context(self, record: DataFactRecord) -> LogContext:
        status = record.audit.status
        processing_path: ProcessingPath
        if status in (
            ProcessingStatus.PROCESSED_FROM_QUEUE,
            ProcessingStatus.PROCESSED_FROM_QUEUE_FALLBACK,
            ProcessingStatus.QUEUED,
        ):
            processing_path = "queue"
        else:
            processing_path = "online"

        return LogContext(
            trace_id=self._correlation_id_factory.build_trace_id(
                record.audit.chat_id, record.audit.message_id
            ),
            chat_id=record.audit.chat_id,
            user_id=record.audit.user_id,
            message_id=record.audit.message_id,
            processing_path=processing_path,
            status=record.audit.status.value,
        )
