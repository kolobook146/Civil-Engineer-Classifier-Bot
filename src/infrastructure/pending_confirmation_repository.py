from __future__ import annotations

import secrets
import sqlite3
from datetime import UTC, datetime
from decimal import Decimal

from config.settings import QueueSettings
from domain.enums import ProcessingStatus
from domain.models import AuditFields, ClassificationResult, DataFactRecord, PendingConfirmation


class PendingConfirmationRepository:
    """Persists pending user confirmations in the shared SQLite file."""

    def __init__(self, settings: QueueSettings) -> None:
        self._db_path = settings.db_path.expanduser().resolve()
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def create(self, record: DataFactRecord) -> PendingConfirmation:
        for _ in range(5):
            confirmation_id = secrets.token_urlsafe(12)
            created_at = datetime.now(tz=UTC)
            try:
                with self._connect() as connection:
                    connection.execute(
                        """
                        INSERT INTO pending_confirmations (
                            confirmation_id, created_at, raw_text, volume, unit, work_type,
                            stage, function, comment, timestamp, user_id, chat_id, message_id,
                            model, classifier_version, status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            confirmation_id,
                            self._to_iso(created_at),
                            record.raw_text,
                            self._format_volume(record.classification.volume),
                            record.classification.unit,
                            record.classification.work_type,
                            record.classification.stage,
                            record.classification.function,
                            record.classification.comment,
                            self._to_iso(record.audit.timestamp),
                            record.audit.user_id,
                            record.audit.chat_id,
                            record.audit.message_id,
                            record.audit.model,
                            record.audit.classifier_version,
                            record.audit.status.value,
                        ),
                    )
            except sqlite3.IntegrityError:
                continue

            return PendingConfirmation(
                confirmation_id=confirmation_id,
                record=record,
                created_at=created_at,
            )

        raise RuntimeError("Failed to allocate unique confirmation id")

    def get(self, confirmation_id: str) -> PendingConfirmation | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT confirmation_id, created_at, raw_text, volume, unit, work_type, stage, function,
                       comment, timestamp, user_id, chat_id, message_id, model, classifier_version, status
                FROM pending_confirmations
                WHERE confirmation_id = ?
                """,
                (confirmation_id,),
            ).fetchone()

        if row is None:
            return None

        return self._build_pending_confirmation(row)

    def delete(self, confirmation_id: str) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM pending_confirmations WHERE confirmation_id = ?",
                (confirmation_id,),
            )
        return cursor.rowcount > 0

    def _init_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS pending_confirmations (
                    confirmation_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    raw_text TEXT NOT NULL,
                    volume TEXT NULL,
                    unit TEXT NULL,
                    work_type TEXT NULL,
                    stage TEXT NULL,
                    function TEXT NULL,
                    comment TEXT NULL,
                    timestamp TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    chat_id TEXT NOT NULL,
                    message_id TEXT NOT NULL,
                    model TEXT NOT NULL,
                    classifier_version TEXT NOT NULL,
                    status TEXT NOT NULL
                )
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._db_path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _build_pending_confirmation(row: sqlite3.Row) -> PendingConfirmation:
        raw_volume = row["volume"]
        volume = Decimal(str(raw_volume)) if raw_volume not in (None, "") else None
        record = DataFactRecord(
            raw_text=str(row["raw_text"]),
            classification=ClassificationResult(
                volume=volume,
                unit=(str(row["unit"]) if row["unit"] is not None else None),
                work_type=(str(row["work_type"]) if row["work_type"] is not None else None),
                stage=(str(row["stage"]) if row["stage"] is not None else None),
                function=(str(row["function"]) if row["function"] is not None else None),
                comment=(str(row["comment"]) if row["comment"] is not None else None),
            ),
            audit=AuditFields(
                timestamp=PendingConfirmationRepository._from_iso(str(row["timestamp"])),
                user_id=str(row["user_id"]),
                chat_id=str(row["chat_id"]),
                message_id=str(row["message_id"]),
                model=str(row["model"]),
                classifier_version=str(row["classifier_version"]),
                status=ProcessingStatus(str(row["status"])),
            ),
        )
        return PendingConfirmation(
            confirmation_id=str(row["confirmation_id"]),
            record=record,
            created_at=PendingConfirmationRepository._from_iso(str(row["created_at"])),
        )

    @staticmethod
    def _format_volume(value: Decimal | None) -> str | None:
        if value is None:
            return None
        return format(value, "f")

    @staticmethod
    def _to_iso(value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _from_iso(value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
