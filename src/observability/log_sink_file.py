from __future__ import annotations

import json
from logging import INFO, LogRecord
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any


class FileLogSink:
    """Writes structured log records to a rotating JSONL file."""

    def __init__(self, *, file_path: Path, max_bytes: int, backup_count: int) -> None:
        resolved = file_path.expanduser().resolve()
        resolved.parent.mkdir(parents=True, exist_ok=True)
        self._handler = RotatingFileHandler(
            filename=resolved,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )

    def emit(self, record: dict[str, Any]) -> None:
        line = json.dumps(record, ensure_ascii=False, separators=(",", ":"), default=str)
        log_record = LogRecord(
            name="tg_build_bot.structured",
            level=INFO,
            pathname="",
            lineno=0,
            msg=line,
            args=(),
            exc_info=None,
        )
        self._handler.emit(log_record)
