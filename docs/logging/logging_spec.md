# Logging Spec (Pilot)

Technical specification for structured logging in TG Build Bot.

## 1. Scope

Logging covers the full message-processing lifecycle across two paths:
- `online` (successful LLM response within 30 seconds)
- `queue` (timeout and deferred processing)

## 2. Format

- Record format: `JSON Lines`
- Timezone: `UTC`
- Timestamp format: ISO-8601 (`2026-02-13T13:00:00.000Z`)
- Levels: `INFO`, `WARNING`, `ERROR`

## 3. Standard Event Schema

Required fields:
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

Recommended contextual fields:
- `llm_model`
- `llm_latency_ms`
- `validation_errors_count`
- `validation_errors`
- `queue_latency_ms`
- `sheet_name`
- `sheets_row_index`
- `error_type`
- `error_message`

## 4. Event Catalog

| event | level | component | Purpose |
|---|---|---|---|
| `polling_started` | INFO | `main_polling` | polling process startup |
| `queue_worker_bootstrap_started` | INFO | `main_queue_worker` | queue worker bootstrap startup |
| `queue_worker_started` | INFO | `queue_worker` | queue worker main loop started |
| `message_received` | INFO | `telegram_polling_handler` | message entered the system |
| `llm_response_received` | INFO | `classification_orchestrator` | successful LLM response |
| `llm_timeout` | WARNING | `classification_orchestrator` | LLM timeout (30 sec) |
| `json_validation_passed` | INFO | `json_schema_validator` | JSON passed schema validation |
| `json_validation_failed` | WARNING | `json_schema_validator` | JSON failed schema validation |
| `queue_enqueued` | INFO | `queue_service` | message enqueued |
| `queue_enqueue_failed` | ERROR | `queue_service` | enqueue failed |
| `queue_dequeued` | INFO | `queue_worker` | task dequeued for processing |
| `queue_task_invalid` | ERROR | `queue_worker` | invalid queue task (missing `queue_id`) |
| `queue_processing_failed` | ERROR | `queue_worker` | queue task processing failed |
| `sheets_write_success` | INFO | `google_sheets_repository` | row successfully written |
| `sheets_write_failed` | ERROR | `google_sheets_repository` | write failed |
| `post_factum_notification_sent` | INFO | `notification_service` | post-factum notification sent |
| `classification_failed` | ERROR | `telegram_polling_handler` | online classification failed |
| `telegram_update_error` | ERROR | `telegram_polling_handler` | Telegram update handler error |

## 5. Log Security Policy

- Full `raw_text` is not logged.
- `raw_text_length` and `raw_text_sha256` are used for traceability.
- `raw_text_preview` is allowed only in local debug mode.
- Secrets (tokens, API keys) are forbidden in logs.

## 6. Correlation

- One `trace_id` per full lifecycle of a message.
- The same `trace_id` is used in both online and queue paths.
- Events must be filterable by `trace_id`, `status`, `event`.

## 7. Storage and Rotation (Pilot)

- Local file: `var/log/bot.log.jsonl`
- Rotation: `10 MB x 5`
- Retention: 30 days

## 8. Event Examples

```json
{"timestamp":"2026-02-13T13:00:00.120Z","level":"INFO","event":"message_received","component":"telegram_polling_handler","trace_id":"12345:678","chat_id":"12345","user_id":"55","message_id":"678","processing_path":"online","status":"RECEIVED","raw_text_length":86,"raw_text_sha256":"f8b7..."}
{"timestamp":"2026-02-13T13:00:01.221Z","level":"INFO","event":"llm_response_received","component":"classification_orchestrator","trace_id":"12345:678","chat_id":"12345","user_id":"55","message_id":"678","processing_path":"online","status":"PROCESSING","llm_model":"gemini-2.5-flash","llm_latency_ms":1033}
{"timestamp":"2026-02-13T13:00:01.350Z","level":"INFO","event":"json_validation_passed","component":"json_schema_validator","trace_id":"12345:678","chat_id":"12345","user_id":"55","message_id":"678","processing_path":"online","status":"PROCESSED","validation_errors_count":0}
{"timestamp":"2026-02-13T13:00:01.480Z","level":"INFO","event":"sheets_write_success","component":"google_sheets_repository","trace_id":"12345:678","chat_id":"12345","user_id":"55","message_id":"678","processing_path":"online","status":"PROCESSED","sheet_name":"data_facts","sheets_row_index":152}
```

## 9. Definition of Done for Logging

- All required events appear in the correct sequence.
- For each `trace_id`, the processing path can be reconstructed from logs.
- On timeout, the minimum chain exists: `llm_timeout` + `queue_enqueued` + later `queue_dequeued`.
- Google Sheets write errors are always logged as `ERROR`.
