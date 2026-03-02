from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"0", "false", "no", "off"}


def _get_env(name: str, default: str = "") -> str:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip()


def _get_int_env(name: str, default: int) -> int:
    raw = _get_env(name, str(default))
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer, got: {raw!r}") from exc


def _get_float_env(name: str, default: float) -> float:
    raw = _get_env(name, str(default))
    try:
        return float(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be a float, got: {raw!r}") from exc


def _get_bool_env(name: str, default: bool) -> bool:
    raw = _get_env(name, "true" if default else "false").lower()
    if raw in _TRUE_VALUES:
        return True
    if raw in _FALSE_VALUES:
        return False
    raise RuntimeError(f"{name} must be boolean-like (true/false, 1/0), got: {raw!r}")


def _parse_allowed_updates(raw: str) -> list[str] | None:
    stripped = raw.strip()
    if not stripped:
        return None

    items = [item.strip() for item in stripped.split(",") if item.strip()]
    if not items:
        return None

    if "message" not in items:
        items.append("message")
    if "callback_query" not in items:
        items.append("callback_query")

    return items


@dataclass(frozen=True)
class AppSettings:
    env: str
    classifier_version: str


@dataclass(frozen=True)
class TelegramSettings:
    bot_token: str
    polling_timeout_seconds: int
    poll_interval_seconds: float
    allowed_updates: list[str] | None


@dataclass(frozen=True)
class LLMSettings:
    base_url: str
    api_key: str
    model: str
    timeout_seconds: int


@dataclass(frozen=True)
class DictionarySettings:
    directory: Path
    work_types_file: Path
    stages_file: Path
    functions_file: Path
    units_file: Path


@dataclass(frozen=True)
class GoogleSheetsSettings:
    service_account_file: Path
    spreadsheet_id: str
    worksheet_name: str


@dataclass(frozen=True)
class QueueSettings:
    db_path: Path
    poll_interval_seconds: int


@dataclass(frozen=True)
class LoggingSettings:
    level: str
    json: bool
    file_path: Path
    max_bytes: int
    backup_count: int
    raw_text_preview_enabled: bool


@dataclass(frozen=True)
class Settings:
    app: AppSettings
    telegram: TelegramSettings
    llm: LLMSettings
    dictionaries: DictionarySettings
    google_sheets: GoogleSheetsSettings
    queue: QueueSettings
    logging: LoggingSettings

    def validate_for_polling(self) -> None:
        if not self.telegram.bot_token:
            raise RuntimeError("TG_BOT_TOKEN is required")

    def validate_for_full_pipeline(self) -> None:
        self.validate_for_polling()

        if not self.llm.api_key:
            raise RuntimeError("LLM_API_KEY is required")
        if not self.llm.model:
            raise RuntimeError("LLM_MODEL is required")

        if not self.google_sheets.spreadsheet_id:
            raise RuntimeError("GOOGLE_SHEETS_SPREADSHEET_ID is required")


def load_settings() -> Settings:
    dictionaries_dir = Path(_get_env("DICTIONARIES_DIR", "dictionaries"))

    return Settings(
        app=AppSettings(
            env=_get_env("APP_ENV", "dev"),
            classifier_version=_get_env("CLASSIFIER_VERSION", "pilot-v1"),
        ),
        telegram=TelegramSettings(
            bot_token=_get_env("TG_BOT_TOKEN", ""),
            polling_timeout_seconds=_get_int_env("TG_POLLING_TIMEOUT_SECONDS", 30),
            poll_interval_seconds=_get_float_env("TG_POLL_INTERVAL_SECONDS", 1.0),
            allowed_updates=_parse_allowed_updates(_get_env("TG_ALLOWED_UPDATES", "message")),
        ),
        llm=LLMSettings(
            base_url=_get_env("LLM_BASE_URL", ""),
            api_key=_get_env("LLM_API_KEY", ""),
            model=_get_env("LLM_MODEL", "gemini-2.5-flash"),
            timeout_seconds=_get_int_env("LLM_TIMEOUT_SECONDS", 30),
        ),
        dictionaries=DictionarySettings(
            directory=dictionaries_dir,
            work_types_file=Path(_get_env("WORK_TYPES_FILE", str(dictionaries_dir / "work_types.txt"))),
            stages_file=Path(_get_env("STAGES_FILE", str(dictionaries_dir / "stages.txt"))),
            functions_file=Path(_get_env("FUNCTIONS_FILE", str(dictionaries_dir / "functions.txt"))),
            units_file=Path(_get_env("UNITS_FILE", str(dictionaries_dir / "units.txt"))),
        ),
        google_sheets=GoogleSheetsSettings(
            service_account_file=Path(
                _get_env("GOOGLE_SERVICE_ACCOUNT_FILE", "secrets/google-service-account.json")
            ),
            spreadsheet_id=_get_env("GOOGLE_SHEETS_SPREADSHEET_ID", ""),
            worksheet_name=_get_env("GOOGLE_SHEETS_WORKSHEET_NAME", "data_facts"),
        ),
        queue=QueueSettings(
            db_path=Path(_get_env("QUEUE_DB_PATH", "var/queue/queue.sqlite3")),
            poll_interval_seconds=_get_int_env("QUEUE_POLL_INTERVAL_SECONDS", 5),
        ),
        logging=LoggingSettings(
            level=_get_env("LOG_LEVEL", "INFO"),
            json=_get_bool_env("LOG_JSON", True),
            file_path=Path(_get_env("LOG_FILE_PATH", "var/log/bot.log.jsonl")),
            max_bytes=_get_int_env("LOG_MAX_BYTES", 10_485_760),
            backup_count=_get_int_env("LOG_BACKUP_COUNT", 5),
            raw_text_preview_enabled=_get_bool_env("RAW_TEXT_PREVIEW_ENABLED", False),
        ),
    )
