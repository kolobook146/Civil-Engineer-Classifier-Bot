from __future__ import annotations

import logging
from typing import Sequence

from config.settings import LoggingSettings

from .log_sink_file import FileLogSink
from .log_sink_stdout import StdoutLogSink
from .logging_service import LogSink, LoggingService


def setup_logging(settings: LoggingSettings) -> LoggingService:
    """
    Creates structured logging service and configures root logger for non-structured
    third-party warnings/errors.
    """
    _configure_root_logger(settings.level)
    sinks: Sequence[LogSink] = (
        StdoutLogSink(),
        FileLogSink(
            file_path=settings.file_path,
            max_bytes=settings.max_bytes,
            backup_count=settings.backup_count,
        ),
    )
    return LoggingService(sinks=sinks)


def _configure_root_logger(level_name: str) -> None:
    level = getattr(logging, level_name.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
