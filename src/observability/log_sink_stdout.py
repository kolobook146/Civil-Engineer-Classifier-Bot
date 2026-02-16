from __future__ import annotations

import json
import sys
from threading import Lock
from typing import Any


class StdoutLogSink:
    """Writes structured log records to stdout in JSON Lines format."""

    def __init__(self) -> None:
        self._lock = Lock()

    def emit(self, record: dict[str, Any]) -> None:
        line = json.dumps(record, ensure_ascii=False, separators=(",", ":"), default=str)
        with self._lock:
            sys.stdout.write(f"{line}\n")
            sys.stdout.flush()
