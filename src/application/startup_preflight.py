from __future__ import annotations

from dataclasses import dataclass

from infrastructure.dictionary_repository import DictionaryRepository
from infrastructure.gemini_client import GeminiClient
from infrastructure.google_sheets_repository import GoogleSheetsRepository
from observability.log_context import LogContext, ProcessingPath
from observability.log_events import LogEvent
from observability.logging_service import LoggingService


@dataclass(frozen=True, slots=True)
class StartupPreflightResult:
    dictionary_version: str
    work_types_count: int
    stages_count: int
    functions_count: int
    units_count: int
    llm_model: str
    llm_preflight_timeout_seconds: int
    worksheet_name: str
    header_count: int


class StartupPreflight:
    """Runs fail-fast infrastructure checks before starting long-running processes."""

    _GEMINI_MIN_PREFLIGHT_TIMEOUT_SECONDS = 10

    def __init__(
        self,
        *,
        dictionary_repository: DictionaryRepository,
        gemini_client: GeminiClient,
        google_sheets_repository: GoogleSheetsRepository,
        logging_service: LoggingService,
        processing_path: ProcessingPath,
        llm_timeout_seconds: int,
    ) -> None:
        self._dictionary_repository = dictionary_repository
        self._gemini_client = gemini_client
        self._google_sheets_repository = google_sheets_repository
        self._logging_service = logging_service
        self._processing_path = processing_path
        self._llm_timeout_seconds = llm_timeout_seconds

    def run(self) -> StartupPreflightResult:
        self._logging_service.info(
            event=LogEvent.startup_preflight_started,
            component="startup_preflight",
            context=self._context(status="STARTED"),
        )

        payload: dict[str, object] = {}
        try:
            dictionary = self._dictionary_repository.preflight_check()
            payload.update(
                {
                    "dictionary_version": dictionary.version,
                    "work_types_count": len(dictionary.work_types),
                    "stages_count": len(dictionary.stages),
                    "functions_count": len(dictionary.functions),
                    "units_count": len(dictionary.units),
                }
            )

            llm_timeout_seconds = self._GEMINI_MIN_PREFLIGHT_TIMEOUT_SECONDS
            llm_payload = self._gemini_client.preflight_check(timeout_seconds=llm_timeout_seconds)
            payload.update(llm_payload)

            sheets_payload = self._google_sheets_repository.preflight_check()
            payload.update(sheets_payload)
        except Exception as exc:
            self._logging_service.error(
                event=LogEvent.startup_preflight_failed,
                component="startup_preflight",
                context=self._context(status="FAILED"),
                payload={
                    **payload,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
            raise

        result = StartupPreflightResult(
            dictionary_version=str(payload["dictionary_version"]),
            work_types_count=int(payload["work_types_count"]),
            stages_count=int(payload["stages_count"]),
            functions_count=int(payload["functions_count"]),
            units_count=int(payload["units_count"]),
            llm_model=str(payload["llm_model"]),
            llm_preflight_timeout_seconds=int(payload["llm_preflight_timeout_seconds"]),
            worksheet_name=str(payload["worksheet_name"]),
            header_count=int(payload["header_count"]),
        )

        self._logging_service.info(
            event=LogEvent.startup_preflight_passed,
            component="startup_preflight",
            context=self._context(status="PASSED"),
            payload=payload,
        )
        return result

    def _context(self, *, status: str) -> LogContext:
        trace_id = f"system:startup_preflight:{self._processing_path}"
        return LogContext(
            trace_id=trace_id,
            chat_id="system",
            user_id="system",
            message_id="system",
            processing_path=self._processing_path,
            status=status,
        )
