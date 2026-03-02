from __future__ import annotations

from application.startup_preflight import StartupPreflight
from config.settings import Settings, load_settings
from dotenv import load_dotenv
from infrastructure.dictionary_repository import DictionaryRepository
from infrastructure.gemini_client import GeminiClient
from infrastructure.google_sheets_repository import GoogleSheetsRepository
from main_polling import build_application, configure_logging
from observability.correlation_id_factory import CorrelationIdFactory
from observability.log_context import LogContext
from observability.log_events import LogEvent


def _normalize_webhook_path(path: str) -> str:
    normalized = path.strip().strip("/")
    if not normalized:
        raise RuntimeError("WEBHOOK_PATH must not be empty")
    return normalized


def _build_webhook_url(settings: Settings) -> tuple[str, str]:
    url_path = _normalize_webhook_path(settings.webhook.path)
    public_base_url = settings.webhook.public_base_url.strip().rstrip("/")
    if not public_base_url.startswith("https://"):
        raise RuntimeError("WEBHOOK_PUBLIC_BASE_URL must start with https://")
    return url_path, f"{public_base_url}/{url_path}"


def main() -> None:
    load_dotenv()
    settings = load_settings()
    settings.validate_for_webhook()

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
        processing_path="online",
        llm_timeout_seconds=settings.llm.timeout_seconds,
    ).run()
    application = build_application(
        settings,
        logging_service=logging_service,
        correlation_id_factory=correlation_id_factory,
    )
    url_path, webhook_url = _build_webhook_url(settings)

    logging_service.info(
        event=LogEvent.webhook_started,
        component="main_webhook",
        context=LogContext(
            trace_id="system:webhook",
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
            "listen_host": settings.webhook.listen_host,
            "listen_port": settings.webhook.listen_port,
            "url_path": url_path,
            "webhook_url": webhook_url,
            "drop_pending_updates": settings.webhook.drop_pending_updates,
            "max_connections": settings.webhook.max_connections,
            "allowed_updates": settings.telegram.allowed_updates,
            "secret_token_configured": bool(settings.webhook.secret_token),
        },
    )

    application.run_webhook(
        listen=settings.webhook.listen_host,
        port=settings.webhook.listen_port,
        url_path=url_path,
        webhook_url=webhook_url,
        allowed_updates=settings.telegram.allowed_updates,
        drop_pending_updates=settings.webhook.drop_pending_updates,
        max_connections=settings.webhook.max_connections,
        secret_token=settings.webhook.secret_token or None,
    )


if __name__ == "__main__":
    main()
