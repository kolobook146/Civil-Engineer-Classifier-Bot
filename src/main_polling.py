from __future__ import annotations

from application.classification_orchestrator import ClassificationOrchestrator
from application.fallback_mapper import FallbackMapper
from application.json_schema_validator import JsonSchemaValidator
from application.llm_payload_normalizer import LLMPayloadNormalizer
from application.message_preprocessor import MessagePreprocessor
from application.prompt_builder import PromptBuilder
from config.settings import Settings, load_settings
from dotenv import load_dotenv
from infrastructure.dictionary_repository import DictionaryRepository
from infrastructure.gemini_client import GeminiClient
from infrastructure.google_sheets_repository import GoogleSheetsRepository
from infrastructure.queue_repository import QueueRepository
from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext
from observability.log_events import LogEvent
from observability.logging_service import LoggingService
from observability.logging_setup import setup_logging
from presentation.notification_service import NotificationService
from presentation.telegram_polling_handler import TelegramPollingHandler
from telegram.ext import Application, ApplicationBuilder

def configure_logging(settings: Settings) -> LoggingService:
    return setup_logging(settings.logging)


def build_application(
    settings: Settings,
    *,
    logging_service: LoggingService,
    correlation_id_factory: CorrelationIdFactory,
) -> Application:
    application = ApplicationBuilder().token(settings.telegram.bot_token).build()

    notification_service = NotificationService(
        logging_service=logging_service,
        correlation_id_factory=correlation_id_factory,
    )
    message_preprocessor = MessagePreprocessor()
    prompt_builder = PromptBuilder()
    json_schema_validator = JsonSchemaValidator()
    llm_payload_normalizer = LLMPayloadNormalizer()
    fallback_mapper = FallbackMapper()
    dictionary_repository = DictionaryRepository(settings.dictionaries)
    google_sheets_repository = GoogleSheetsRepository(
        settings.google_sheets,
        logging_service=logging_service,
        correlation_id_factory=correlation_id_factory,
    )
    queue_repository = QueueRepository(settings.queue)
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
    telegram_handler = TelegramPollingHandler(
        notification_service=notification_service,
        message_preprocessor=message_preprocessor,
        classification_orchestrator=classification_orchestrator,
        queue_repository=queue_repository,
        logging_service=logging_service,
        correlation_id_factory=correlation_id_factory,
    )
    telegram_handler.register(application)

    return application


def main() -> None:
    load_dotenv()
    settings = load_settings()
    settings.validate_for_full_pipeline()

    logging_service = configure_logging(settings)
    correlation_id_factory = CorrelationIdFactory()
    application = build_application(
        settings,
        logging_service=logging_service,
        correlation_id_factory=correlation_id_factory,
    )

    logging_service.info(
        event=LogEvent.polling_started,
        component="main_polling",
        context=LogContext(
            trace_id="system:polling",
            chat_id="system",
            user_id="system",
            message_id="system",
            processing_path="online",
            status="STARTED",
        ),
        payload={
            "env": settings.app.env,
            "classifier_version": settings.app.classifier_version,
            "llm_timeout_seconds": settings.llm.timeout_seconds,
            "poll_interval_seconds": settings.telegram.poll_interval_seconds,
            "allowed_updates": settings.telegram.allowed_updates,
        },
    )

    application.run_polling(
        poll_interval=settings.telegram.poll_interval_seconds,
        timeout=settings.telegram.polling_timeout_seconds,
        allowed_updates=settings.telegram.allowed_updates,
    )


if __name__ == "__main__":
    main()
