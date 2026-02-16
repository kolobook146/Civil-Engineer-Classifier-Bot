from __future__ import annotations

import sqlite3
from datetime import UTC, datetime

from config.settings import QueueSettings
from domain.models import QueueTask

class QueueRepository:
    """SQLite-backed queue for deferred classification tasks."""

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
                    received_at, enqueued_at, status, last_error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', NULL)
                """,
                (
                    task.user_id,
                    task.chat_id,
                    task.message_id,
                    task.raw_text,
                    task.normalized_text,
                    self._to_iso(task.received_at),
                    self._to_iso(task.enqueued_at),
                ),
            )
            queue_id = int(cursor.lastrowid)

        return queue_id

    def dequeue(self) -> QueueTask | None:
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                """
                SELECT id, user_id, chat_id, message_id, raw_text, normalized_text, received_at, enqueued_at
                FROM queue_tasks
                WHERE status = 'pending'
                ORDER BY id
                LIMIT 1
                """
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
        )
        return task

    def mark_done(self, queue_id: int) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM queue_tasks WHERE id = ?", (queue_id,))

    def requeue(self, queue_id: int, *, error: str) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE queue_tasks
                SET status = 'pending', last_error = ?
                WHERE id = ?
                """,
                (error[:1024], queue_id),
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
                    status TEXT NOT NULL,
                    last_error TEXT NULL
                )
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
