from __future__ import annotations

import asyncio

from application.classification_orchestrator import ClassificationOrchestrator
from application.fallback_mapper import FallbackMapper
from application.json_schema_validator import JsonSchemaValidator
from application.llm_payload_normalizer import LLMPayloadNormalizer
from application.prompt_builder import PromptBuilder
from application.queue_worker import QueueWorker
from application.startup_preflight import StartupPreflight
from config.settings import Settings, load_settings
from dotenv import load_dotenv
from infrastructure.dictionary_repository import DictionaryRepository
from infrastructure.gemini_client import GeminiClient
from infrastructure.google_sheets_repository import GoogleSheetsRepository
from infrastructure.pending_confirmation_repository import PendingConfirmationRepository
from infrastructure.queue_repository import QueueRepository
from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext
from observability.log_events import LogEvent
from observability.logging_service import LoggingService
from observability.logging_setup import setup_logging
from presentation.notification_service import NotificationService
from telegram import Bot

def configure_logging(settings: Settings) -> LoggingService:
    return setup_logging(settings.logging)


def build_queue_worker(
    settings: Settings,
    *,
    logging_service: LoggingService,
    correlation_id_factory: CorrelationIdFactory,
) -> tuple[QueueWorker, Bot]:
    prompt_builder = PromptBuilder()
    json_schema_validator = JsonSchemaValidator()
    llm_payload_normalizer = LLMPayloadNormalizer()
    fallback_mapper = FallbackMapper()
    notification_service = NotificationService(
        logging_service=logging_service,
        correlation_id_factory=correlation_id_factory,
    )

    dictionary_repository = DictionaryRepository(settings.dictionaries)
    google_sheets_repository = GoogleSheetsRepository(
        settings.google_sheets,
        logging_service=logging_service,
        correlation_id_factory=correlation_id_factory,
    )
    queue_repository = QueueRepository(settings.queue)
    pending_confirmation_repository = PendingConfirmationRepository(settings.queue)
    gemini_client = GeminiClient(
        api_key=settings.llm.api_key,
        model=settings.llm.model,
        timeout_seconds=settings.llm.timeout_seconds,
        base_url=settings.llm.base_url,
    )

    classification_orchestrator = ClassificationOrchestrator(
        dictionary_repository=dictionary_repository,
        gemini_client=gemini_client,
        google_sheets_repository=google_sheets_repository,
        prompt_builder=prompt_builder,
        json_schema_validator=json_schema_validator,
        llm_payload_normalizer=llm_payload_normalizer,
        fallback_mapper=fallback_mapper,
        logging_service=logging_service,
        correlation_id_factory=correlation_id_factory,
        llm_model=settings.llm.model,
        classifier_version=settings.app.classifier_version,
        llm_timeout_seconds=settings.llm.timeout_seconds,
    )

    queue_worker = QueueWorker(
        queue_repository=queue_repository,
        pending_confirmation_repository=pending_confirmation_repository,
        classification_orchestrator=classification_orchestrator,
        notification_service=notification_service,
        logging_service=logging_service,
        correlation_id_factory=correlation_id_factory,
        poll_interval_seconds=settings.queue.poll_interval_seconds,
    )
    bot = Bot(token=settings.telegram.bot_token)
    return queue_worker, bot


def main() -> None:
    load_dotenv()
    settings = load_settings()
    settings.validate_for_full_pipeline()

    logging_service = configure_logging(settings)
    correlation_id_factory = CorrelationIdFactory()
    StartupPreflight(
        dictionary_repository=DictionaryRepository(settings.dictionaries),
        gemini_client=GeminiClient(
            api_key=settings.llm.api_key,
            model=settings.llm.model,
            timeout_seconds=settings.llm.timeout_seconds,
            base_url=settings.llm.base_url,
        ),
        google_sheets_repository=GoogleSheetsRepository(
            settings.google_sheets,
            logging_service=logging_service,
            correlation_id_factory=correlation_id_factory,
        ),
        logging_service=logging_service,
        processing_path="queue",
        llm_timeout_seconds=settings.llm.timeout_seconds,
    ).run()
    queue_worker, bot = build_queue_worker(
        settings,
        logging_service=logging_service,
        correlation_id_factory=correlation_id_factory,
    )

    logging_service.info(
        event=LogEvent.queue_worker_bootstrap_started,
        component="main_queue_worker",
        context=LogContext(
            trace_id="system:queue_worker_bootstrap",
            chat_id="system",
            user_id="system",
            message_id="system",
            processing_path="queue",
            status="STARTED",
        ),
        payload={
            "env": settings.app.env,
            "classifier_version": settings.app.classifier_version,
            "queue_db": str(settings.queue.db_path),
            "queue_poll_interval_seconds": settings.queue.poll_interval_seconds,
        },
    )
    asyncio.run(queue_worker.run_forever(bot=bot))


if __name__ == "__main__":
    main()
