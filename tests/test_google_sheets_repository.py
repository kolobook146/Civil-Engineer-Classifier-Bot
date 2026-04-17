from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from domain.enums import ProcessingStatus
from domain.models import AuditFields, ClassificationResult, DataFactRecord
from infrastructure.google_sheets_repository import GoogleSheetsRepository


class _WorksheetStub:
    def __init__(self, headers: list[str]) -> None:
        self._headers = headers
        self.updated: list[tuple[str, list[list[str]]]] = []

    def row_values(self, _row: int) -> list[str]:
        return self._headers

    def update(self, range_name: str, values: list[list[str]]) -> None:
        self.updated.append((range_name, values))


def test_build_row_payload_includes_row_local_verification_formula() -> None:
    record = DataFactRecord(
        raw_text="Installed 12 m2 facade",
        classification=ClassificationResult(
            volume=Decimal("12"),
            unit="m2",
            work_type="Facade works",
            stage="Execution",
            function="Construction and installation works",
            comment=None,
        ),
        audit=AuditFields(
            timestamp=datetime(2026, 4, 16, tzinfo=UTC),
            user_id="55",
            chat_id="12345",
            message_id="901",
            model="gemini-2.5-flash",
            classifier_version="pilot-v1",
            status=ProcessingStatus.PROCESSED,
        ),
    )

    payload = GoogleSheetsRepository._build_row_payload(record)

    assert payload["verification"].startswith("=IF(INDEX($A:$A,ROW())=")
    assert "fact_verification_helper!$A:$C" in payload["verification"]
    assert "not verified" in payload["verification"]
    assert "verified" in payload["verification"]


def test_ensure_headers_adds_verification_column() -> None:
    worksheet = _WorksheetStub(
        [
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
        ]
    )

    repository = GoogleSheetsRepository.__new__(GoogleSheetsRepository)

    headers = repository._ensure_headers(worksheet)

    assert headers[-1] == "verification"
    assert worksheet.updated == [("A1", [headers])]
