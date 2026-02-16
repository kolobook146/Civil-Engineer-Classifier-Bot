from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ProcessingPath = Literal["online", "queue"]


@dataclass(frozen=True, slots=True)
class LogContext:
    trace_id: str
    chat_id: str
    user_id: str
    message_id: str
    processing_path: ProcessingPath
    status: str
