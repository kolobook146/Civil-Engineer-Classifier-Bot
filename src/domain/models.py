from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from .enums import ProcessingStatus


@dataclass(frozen=True, slots=True)
class TelegramMessageMeta:
    user_id: str
    chat_id: str
    message_id: str
    timestamp: datetime


@dataclass(frozen=True, slots=True)
class ClassificationResult:
    volume: str | None
    unit: str | None
    work_type: str | None
    stage: str | None
    function: str | None
    comment: str | None

    def as_json_dict(self) -> dict[str, str | None]:
        return {
            "volume": self.volume,
            "unit": self.unit,
            "workType": self.work_type,
            "stage": self.stage,
            "function": self.function,
            "comment": self.comment,
        }


@dataclass(frozen=True, slots=True)
class AuditFields:
    timestamp: datetime
    user_id: str
    chat_id: str
    message_id: str
    model: str
    classifier_version: str
    status: ProcessingStatus


@dataclass(frozen=True, slots=True)
class DataFactRecord:
    raw_text: str
    classification: ClassificationResult
    audit: AuditFields


@dataclass(frozen=True, slots=True)
class ClassificationRunResult:
    record: DataFactRecord
    llm_raw_response: str
    dictionary_version: str


@dataclass(frozen=True, slots=True)
class QueueTask:
    queue_id: int | None
    user_id: str
    chat_id: str
    message_id: str
    raw_text: str
    normalized_text: str | None
    received_at: datetime
    enqueued_at: datetime


def build_message_meta(
    *,
    user_id: str,
    chat_id: str,
    message_id: str,
    timestamp: datetime | None = None,
) -> TelegramMessageMeta:
    return TelegramMessageMeta(
        user_id=user_id,
        chat_id=chat_id,
        message_id=message_id,
        timestamp=timestamp or datetime.now(tz=UTC),
    )


def build_queue_task(
    *,
    user_id: str,
    chat_id: str,
    message_id: str,
    raw_text: str,
    normalized_text: str | None,
    received_at: datetime | None = None,
    enqueued_at: datetime | None = None,
) -> QueueTask:
    now = datetime.now(tz=UTC)
    return QueueTask(
        queue_id=None,
        user_id=user_id,
        chat_id=chat_id,
        message_id=message_id,
        raw_text=raw_text,
        normalized_text=normalized_text,
        received_at=received_at or now,
        enqueued_at=enqueued_at or now,
    )
