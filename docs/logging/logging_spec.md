# Logging Spec (Pilot)

Техническая спецификация структурированного логгирования для TG Build Bot.

## 1. Scope

Логгирование покрывает полный цикл обработки сообщения в двух путях:
- `online` (успешный ответ LLM до 30 секунд)
- `queue` (таймаут и отложенная обработка)

## 2. Формат

- Формат записи: `JSON Lines`
- Часовой пояс: `UTC`
- Формат времени: ISO-8601 (`2026-02-13T13:00:00.000Z`)
- Уровни: `INFO`, `WARNING`, `ERROR`

## 3. Стандартная схема события

Обязательные поля:
- `timestamp` (string)
- `level` (string)
- `event` (string)
- `component` (string)
- `trace_id` (string, `chat_id:message_id`)
- `chat_id` (string)
- `user_id` (string)
- `message_id` (string)
- `processing_path` (`online`|`queue`)
- `status` (string)

Рекомендуемые контекстные поля:
- `llm_model`
- `llm_latency_ms`
- `validation_errors_count`
- `validation_errors`
- `queue_latency_ms`
- `sheet_name`
- `sheets_row_index`
- `error_type`
- `error_message`

## 4. Каталог событий

| event | level | component | Назначение |
|---|---|---|---|
| `polling_started` | INFO | `main_polling` | старт polling-процесса |
| `queue_worker_bootstrap_started` | INFO | `main_queue_worker` | старт bootstrap queue-worker |
| `queue_worker_started` | INFO | `queue_worker` | рабочий цикл queue-worker запущен |
| `message_received` | INFO | `telegram_polling_handler` | вход сообщения в систему |
| `llm_response_received` | INFO | `classification_orchestrator` | успешный ответ LLM |
| `llm_timeout` | WARNING | `classification_orchestrator` | таймаут LLM (30 сек) |
| `json_validation_passed` | INFO | `json_schema_validator` | JSON соответствует схеме |
| `json_validation_failed` | WARNING | `json_schema_validator` | JSON не соответствует схеме |
| `queue_enqueued` | INFO | `queue_service` | постановка в очередь |
| `queue_enqueue_failed` | ERROR | `queue_service` | ошибка постановки в очередь |
| `queue_dequeued` | INFO | `queue_worker` | взятие задачи в работу |
| `queue_task_invalid` | ERROR | `queue_worker` | некорректная задача очереди (без `queue_id`) |
| `queue_processing_failed` | ERROR | `queue_worker` | ошибка обработки задачи очереди |
| `sheets_write_success` | INFO | `google_sheets_repository` | успешная запись строки |
| `sheets_write_failed` | ERROR | `google_sheets_repository` | ошибка записи |
| `post_factum_notification_sent` | INFO | `notification_service` | уведомление после queue |
| `classification_failed` | ERROR | `telegram_polling_handler` | ошибка online-классификации |
| `telegram_update_error` | ERROR | `telegram_polling_handler` | ошибка обработчика Telegram update |

## 5. Политика безопасности логов

- Полный `raw_text` не логируется.
- Для трассировки используются `raw_text_length` и `raw_text_sha256`.
- `raw_text_preview` разрешен только в локальном debug-режиме.
- Секреты (tokens, API keys) в логах запрещены.

## 6. Корреляция

- Один `trace_id` на весь жизненный цикл конкретного сообщения.
- В online и queue-пути используется один и тот же `trace_id`.
- События должны быть пригодны для фильтрации по `trace_id`, `status`, `event`.

## 7. Хранение и ротация (pilot)

- Локальный файл: `var/log/bot.log.jsonl`
- Ротация: `10 MB x 5`
- Retention: 30 дней

## 8. Пример событий

```json
{"timestamp":"2026-02-13T13:00:00.120Z","level":"INFO","event":"message_received","component":"telegram_polling_handler","trace_id":"12345:678","chat_id":"12345","user_id":"55","message_id":"678","processing_path":"online","status":"RECEIVED","raw_text_length":86,"raw_text_sha256":"f8b7..."}
{"timestamp":"2026-02-13T13:00:01.221Z","level":"INFO","event":"llm_response_received","component":"classification_orchestrator","trace_id":"12345:678","chat_id":"12345","user_id":"55","message_id":"678","processing_path":"online","status":"PROCESSING","llm_model":"gemini-2.5-flash","llm_latency_ms":1033}
{"timestamp":"2026-02-13T13:00:01.350Z","level":"INFO","event":"json_validation_passed","component":"json_schema_validator","trace_id":"12345:678","chat_id":"12345","user_id":"55","message_id":"678","processing_path":"online","status":"PROCESSED","validation_errors_count":0}
{"timestamp":"2026-02-13T13:00:01.480Z","level":"INFO","event":"sheets_write_success","component":"google_sheets_repository","trace_id":"12345:678","chat_id":"12345","user_id":"55","message_id":"678","processing_path":"online","status":"PROCESSED","sheet_name":"data_facts","sheets_row_index":152}
```

## 9. Definition of Done for logging

- Все обязательные события появляются в корректной последовательности.
- Для каждого `trace_id` путь обработки воспроизводим из логов.
- При таймауте есть минимум: `llm_timeout` + `queue_enqueued` + позднее `queue_dequeued`.
- Ошибки записи в Sheets всегда фиксируются как `ERROR`.
