from __future__ import annotations

import random
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Final

from config.settings import QueueSettings
from domain.models import QueueTask


@dataclass(frozen=True, slots=True)
class RequeueResult:
    queue_id: int
    attempt_count: int
    next_attempt_at: datetime
    retry_delay_seconds: int


class QueueRepository:
    """SQLite-backed queue for deferred classification tasks."""

    _RETRY_BASE_DELAYS_SECONDS: Final[tuple[int, ...]] = (60, 300, 900)
    _RETRY_JITTER_RATIO: Final[float] = 0.1

    def __init__(self, settings: QueueSettings) -> None:
        self._settings = settings
        self._db_path = settings.db_path.expanduser().resolve()
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def enqueue(self, task: QueueTask) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO queue_tasks (
                    user_id, chat_id, message_id, raw_text, normalized_text,
                    received_at, enqueued_at, attempt_count, next_attempt_at, status, last_error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', NULL)
                """,
                (
                    task.user_id,
                    task.chat_id,
                    task.message_id,
                    task.raw_text,
                    task.normalized_text,
                    self._to_iso(task.received_at),
                    self._to_iso(task.enqueued_at),
                    task.attempt_count,
                    self._to_iso(task.next_attempt_at),
                ),
            )
            queue_id = int(cursor.lastrowid)

        return queue_id

    def dequeue(self) -> QueueTask | None:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                """
                SELECT id, user_id, chat_id, message_id, raw_text, normalized_text,
                       received_at, enqueued_at, attempt_count, next_attempt_at
                FROM queue_tasks
                WHERE status = 'pending'
                  AND datetime(COALESCE(next_attempt_at, enqueued_at)) <= datetime(?)
                ORDER BY datetime(COALESCE(next_attempt_at, enqueued_at)), id
                LIMIT 1
                """,
                (self._to_iso(datetime.now(tz=UTC)),),
            ).fetchone()
            if row is None:
                connection.commit()
                return None

            connection.execute(
                """
                UPDATE queue_tasks
                SET status = 'processing', last_error = NULL
                WHERE id = ?
                """,
                (row["id"],),
            )
            connection.commit()

        task = QueueTask(
            queue_id=int(row["id"]),
            user_id=str(row["user_id"]),
            chat_id=str(row["chat_id"]),
            message_id=str(row["message_id"]),
            raw_text=str(row["raw_text"]),
            normalized_text=(str(row["normalized_text"]) if row["normalized_text"] is not None else None),
            received_at=self._from_iso(str(row["received_at"])),
            enqueued_at=self._from_iso(str(row["enqueued_at"])),
            attempt_count=int(row["attempt_count"]),
            next_attempt_at=self._from_iso(str(row["next_attempt_at"])),
        )
        return task

    def mark_done(self, queue_id: int) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM queue_tasks WHERE id = ?", (queue_id,))

    def requeue(self, queue_id: int, *, error: str) -> RequeueResult:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT attempt_count FROM queue_tasks WHERE id = ?",
                (queue_id,),
            ).fetchone()
            if row is None:
                connection.commit()
                raise RuntimeError(f"Queue task not found: {queue_id}")

            next_attempt_count = int(row["attempt_count"]) + 1
            retry_delay_seconds = self._calculate_retry_delay_seconds(next_attempt_count)
            next_attempt_at = datetime.now(tz=UTC) + timedelta(seconds=retry_delay_seconds)
            connection.execute(
                """
                UPDATE queue_tasks
                SET status = 'pending',
                    last_error = ?,
                    attempt_count = ?,
                    next_attempt_at = ?
                WHERE id = ?
                """,
                (
                    error[:1024],
                    next_attempt_count,
                    self._to_iso(next_attempt_at),
                    queue_id,
                ),
            )
            connection.commit()
        return RequeueResult(
            queue_id=queue_id,
            attempt_count=next_attempt_count,
            next_attempt_at=next_attempt_at,
            retry_delay_seconds=retry_delay_seconds,
        )

    def size(self) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS total FROM queue_tasks WHERE status IN ('pending', 'processing')"
            ).fetchone()
        return int(row["total"]) if row is not None else 0

    def _init_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS queue_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    chat_id TEXT NOT NULL,
                    message_id TEXT NOT NULL,
                    raw_text TEXT NOT NULL,
                    normalized_text TEXT NULL,
                    received_at TEXT NOT NULL,
                    enqueued_at TEXT NOT NULL,
                    attempt_count INTEGER NOT NULL DEFAULT 0,
                    next_attempt_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    last_error TEXT NULL
                )
                """
            )
            self._ensure_column(
                connection,
                column_name="attempt_count",
                definition="INTEGER NOT NULL DEFAULT 0",
            )
            self._ensure_column(
                connection,
                column_name="next_attempt_at",
                definition="TEXT NULL",
            )
            connection.execute(
                """
                UPDATE queue_tasks
                SET attempt_count = COALESCE(attempt_count, 0)
                """
            )
            connection.execute(
                """
                UPDATE queue_tasks
                SET next_attempt_at = enqueued_at
                WHERE next_attempt_at IS NULL OR TRIM(next_attempt_at) = ''
                """
            )
            # Recover tasks left in processing state after worker crash/restart.
            connection.execute(
                "UPDATE queue_tasks SET status = 'pending' WHERE status = 'processing'"
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._db_path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _to_iso(value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(UTC).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _from_iso(value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    @staticmethod
    def _ensure_column(connection: sqlite3.Connection, *, column_name: str, definition: str) -> None:
        columns = {
            str(row["name"])
            for row in connection.execute("PRAGMA table_info(queue_tasks)").fetchall()
        }
        if column_name in columns:
            return
        connection.execute(f"ALTER TABLE queue_tasks ADD COLUMN {column_name} {definition}")

    def _calculate_retry_delay_seconds(self, attempt_count: int) -> int:
        base_delay = self._retry_base_delay_seconds(attempt_count)
        jitter_span = max(1, int(round(base_delay * self._RETRY_JITTER_RATIO)))
        jitter_seconds = random.randint(-jitter_span, jitter_span)
        return max(1, base_delay + jitter_seconds)

    def _retry_base_delay_seconds(self, attempt_count: int) -> int:
        index = max(0, min(attempt_count - 1, len(self._RETRY_BASE_DELAYS_SECONDS) - 1))
        return self._RETRY_BASE_DELAYS_SECONDS[index]
