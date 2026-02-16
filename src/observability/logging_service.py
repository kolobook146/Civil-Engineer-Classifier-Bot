from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Protocol, Sequence

from .log_context import LogContext
from .log_events import LogEvent


class LogLevel(StrEnum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class LogSink(Protocol):
    def emit(self, record: dict[str, Any]) -> None:
        ...


@dataclass(frozen=True, slots=True)
class StructuredLogRecord:
    timestamp: str
    level: str
    event: str
    component: str
    trace_id: str
    chat_id: str
    user_id: str
    message_id: str
    processing_path: str
    status: str
    payload: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        data = {
            "timestamp": self.timestamp,
            "level": self.level,
            "event": self.event,
            "component": self.component,
            "trace_id": self.trace_id,
            "chat_id": self.chat_id,
            "user_id": self.user_id,
            "message_id": self.message_id,
            "processing_path": self.processing_path,
            "status": self.status,
        }
        data.update(self.payload)
        return data


class LoggingService:
    """Emits structured logs according to logging_spec.md contract."""

    def __init__(self, sinks: Sequence[LogSink]) -> None:
        self._sinks = list(sinks)

    def info(
        self,
        *,
        event: LogEvent,
        component: str,
        context: LogContext,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self._emit(
            level=LogLevel.INFO,
            event=event,
            component=component,
            context=context,
            payload=payload,
        )

    def warning(
        self,
        *,
        event: LogEvent,
        component: str,
        context: LogContext,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self._emit(
            level=LogLevel.WARNING,
            event=event,
            component=component,
            context=context,
            payload=payload,
        )

    def error(
        self,
        *,
        event: LogEvent,
        component: str,
        context: LogContext,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self._emit(
            level=LogLevel.ERROR,
            event=event,
            component=component,
            context=context,
            payload=payload,
        )

    def _emit(
        self,
        *,
        level: LogLevel,
        event: LogEvent,
        component: str,
        context: LogContext,
        payload: dict[str, Any] | None,
    ) -> None:
        record = StructuredLogRecord(
            timestamp=self._timestamp(),
            level=level.value,
            event=event.value,
            component=component,
            trace_id=context.trace_id,
            chat_id=context.chat_id,
            user_id=context.user_id,
            message_id=context.message_id,
            processing_path=context.processing_path,
            status=context.status,
            payload=payload or {},
        ).as_dict()

        for sink in self._sinks:
            sink.emit(record)

    @staticmethod
    def _timestamp() -> str:
        return datetime.now(tz=UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")
