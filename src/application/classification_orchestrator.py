from __future__ import annotations

import time
from typing import Any

from domain.enums import ProcessingStatus
from domain.models import (
    AuditFields,
    ClassificationResult,
    ClassificationRunResult,
    DataFactRecord,
    TelegramMessageMeta,
)
from infrastructure.dictionary_repository import DictionaryRepository
from infrastructure.gemini_client import GeminiClient, LLMTimeoutError
from infrastructure.google_sheets_repository import GoogleSheetsRepository
from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext, ProcessingPath
from observability.log_events import LogEvent
from observability.logging_service import LoggingService

from .fallback_mapper import FallbackMapper
from .json_schema_validator import JsonSchemaValidator
from .prompt_builder import PromptBuilder


class ClassificationOrchestrator:
    """Pilot message classification pipeline based on dictionaries and Gemini."""

    def __init__(
        self,
        *,
        dictionary_repository: DictionaryRepository,
        gemini_client: GeminiClient,
        google_sheets_repository: GoogleSheetsRepository,
        prompt_builder: PromptBuilder,
        json_schema_validator: JsonSchemaValidator,
        fallback_mapper: FallbackMapper,
        logging_service: LoggingService,
        correlation_id_factory: CorrelationIdFactory,
        llm_model: str,
        classifier_version: str,
        llm_timeout_seconds: int = 30,
    ) -> None:
        self._dictionary_repository = dictionary_repository
        self._gemini_client = gemini_client
        self._google_sheets_repository = google_sheets_repository
        self._prompt_builder = prompt_builder
        self._json_schema_validator = json_schema_validator
        self._fallback_mapper = fallback_mapper
        self._logging_service = logging_service
        self._correlation_id_factory = correlation_id_factory
        self._llm_model = llm_model
        self._classifier_version = classifier_version
        self._llm_timeout_seconds = llm_timeout_seconds

    def classify(
        self,
        *,
        raw_text: str,
        normalized_text: str | None = None,
        meta: TelegramMessageMeta,
    ) -> ClassificationRunResult:
        return self._classify(
            raw_text=raw_text,
            normalized_text=normalized_text,
            meta=meta,
            from_queue=False,
        )

    def classify_from_queue(
        self,
        *,
        raw_text: str,
        normalized_text: str | None = None,
        meta: TelegramMessageMeta,
    ) -> ClassificationRunResult:
        return self._classify(
            raw_text=raw_text,
            normalized_text=normalized_text,
            meta=meta,
            from_queue=True,
        )

    def classifyFromQueue(
        self,
        *,
        raw_text: str,
        normalized_text: str | None = None,
        meta: TelegramMessageMeta,
    ) -> ClassificationRunResult:
        """Compatibility alias with UML naming."""
        return self.classify_from_queue(
            raw_text=raw_text,
            normalized_text=normalized_text,
            meta=meta,
        )

    def _classify(
        self,
        *,
        raw_text: str,
        normalized_text: str | None,
        meta: TelegramMessageMeta,
        from_queue: bool,
    ) -> ClassificationRunResult:
        dictionary = self._dictionary_repository.load_from_text_files()
        text_for_classification = normalized_text if normalized_text is not None else raw_text
        prompt = self._prompt_builder.build(raw_text=text_for_classification, dictionary=dictionary)
        processing_path: ProcessingPath = "queue" if from_queue else "online"
        trace_id = self._correlation_id_factory.build_trace_id(meta.chat_id, meta.message_id)

        llm_start = time.perf_counter()
        try:
            llm_raw_response = self._gemini_client.classify(
                prompt=prompt,
                timeout_seconds=self._llm_timeout_seconds,
            )
        except LLMTimeoutError:
            self._logging_service.warning(
                event=LogEvent.llm_timeout,
                component="classification_orchestrator",
                context=LogContext(
                    trace_id=trace_id,
                    chat_id=meta.chat_id,
                    user_id=meta.user_id,
                    message_id=meta.message_id,
                    processing_path=processing_path,
                    status=ProcessingStatus.QUEUED.value,
                ),
                payload={"llm_model": self._llm_model},
            )
            raise

        llm_latency_ms = int((time.perf_counter() - llm_start) * 1000)
        self._logging_service.info(
            event=LogEvent.llm_response_received,
            component="classification_orchestrator",
            context=LogContext(
                trace_id=trace_id,
                chat_id=meta.chat_id,
                user_id=meta.user_id,
                message_id=meta.message_id,
                processing_path=processing_path,
                status="PROCESSING",
            ),
            payload={
                "llm_model": self._llm_model,
                "llm_latency_ms": llm_latency_ms,
            },
        )

        validation_result = self._json_schema_validator.validate(
            result_json=llm_raw_response,
            dictionary=dictionary,
        )
        has_errors = not validation_result.is_valid

        if has_errors:
            status = (
                ProcessingStatus.PROCESSED_FROM_QUEUE_FALLBACK
                if from_queue
                else ProcessingStatus.PROCESSED_WITH_FALLBACK
            )
            classification = self._fallback_mapper.map_invalid(raw_llm_response=llm_raw_response)
            self._logging_service.warning(
                event=LogEvent.json_validation_failed,
                component="json_schema_validator",
                context=LogContext(
                    trace_id=trace_id,
                    chat_id=meta.chat_id,
                    user_id=meta.user_id,
                    message_id=meta.message_id,
                    processing_path=processing_path,
                    status=status.value,
                ),
                payload={
                    "validation_errors_count": len(validation_result.errors),
                    "validation_errors": list(validation_result.errors),
                },
            )
        else:
            status = ProcessingStatus.PROCESSED_FROM_QUEUE if from_queue else ProcessingStatus.PROCESSED
            classification = self._build_result(validation_result.payload)
            self._logging_service.info(
                event=LogEvent.json_validation_passed,
                component="json_schema_validator",
                context=LogContext(
                    trace_id=trace_id,
                    chat_id=meta.chat_id,
                    user_id=meta.user_id,
                    message_id=meta.message_id,
                    processing_path=processing_path,
                    status=status.value,
                ),
                payload={"validation_errors_count": 0},
            )

        record = DataFactRecord(
            raw_text=raw_text,
            classification=classification,
            audit=AuditFields(
                timestamp=meta.timestamp,
                user_id=meta.user_id,
                chat_id=meta.chat_id,
                message_id=meta.message_id,
                model=self._llm_model,
                classifier_version=self._classifier_version,
                status=status,
            ),
        )
        self._google_sheets_repository.append_data_fact(record)

        return ClassificationRunResult(
            record=record,
            llm_raw_response=llm_raw_response,
            dictionary_version=dictionary.version,
        )

    @staticmethod
    def _build_result(payload: dict[str, Any]) -> ClassificationResult:
        return ClassificationResult(
            volume=payload["volume"],
            unit=payload["unit"],
            work_type=payload["workType"],
            stage=payload["stage"],
            function=payload["function"],
            comment=payload["comment"],
        )
