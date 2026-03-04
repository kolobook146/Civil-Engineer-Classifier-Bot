# Improvements Backlog

Goal: a single list of improvements for transitioning from pilot to post-pilot.

## Maintenance Rules

- `priority`: `P0` (critical), `P1` (high), `P2` (medium), `P3` (low).
- `target_phase`: `pilot` or `post-pilot`.
- `status`: `planned`, `in_progress`, `done`, `rejected`.
- `owner`: responsible role or name.

## Backlog

| id | idea | priority | target_phase | status | owner | notes |
|---|---|---|---|---|---|---|
| IMP-001 | Idempotent write to Google Sheets using a unique message key (`chat_id + message_id`) | P1 | post-pilot | planned | TBD | Reason: duplicates are possible on retries/restarts (current `append_row` path in `src/infrastructure/google_sheets_repository.py`). Result: one fact per message. |
| IMP-002 | Queue retry model (`attempt_count`, `next_attempt_at`, jitter) | P1 | pilot | done | TBD | Implemented in `src/infrastructure/queue_repository.py` and `src/application/queue_worker.py`: queue tasks now persist `attempt_count` and `next_attempt_at`, requeue uses bounded backoff (1/5/15 minutes) with jitter, and dequeue picks only due tasks. Result: controlled retries instead of repeatedly hitting the same task. |
| IMP-003 | Log confidence and reasons for empty classification fields | P2 | post-pilot | planned | TBD | Improve prompt and dictionary quality |
| IMP-004 | Observability upgrade to SLI/SLO metrics (timeouts, fallback rate, queue lag, Sheets errors) | P1 | post-pilot | planned | TBD | Reason: event logs exist but no aggregated telemetry/alerts. Result: faster operational control and incident response. |
| IMP-005 | Expand dictionary structure to `code`, `label`, `description` | P1 | post-pilot | planned | TBD | Currently only `label` is used |
| IMP-006 | Add explicit units aliases dictionary with normalization to canonical key | P1 | post-pilot | planned | TBD | Reason: aliases are described in text, while validation is strict by dictionary key (`src/application/json_schema_validator.py`). Result: stable normalization for variants like `кубов`/`м³`/`м3`. |
| IMP-007 | Deduplicate incoming messages by `chat_id + message_id` at ingestion layer | P2 | post-pilot | planned | TBD | Separate from idempotent persistence |
| IMP-008 | Access roles (who can submit execution facts) | P2 | post-pilot | planned | TBD | Pilot access is open |
| IMP-009 | User edit/cancel flow for previously recorded entries | P3 | post-pilot | planned | TBD | Requires UX and versioning model |
| IMP-010 | Synonyms/abbreviations catalog for dictionaries (e.g., HVAC, WSS, C&I works, commissioning) | P2 | post-pilot | planned | TBD | Improve mapping accuracy to `label` |
| IMP-011 | Upgrade runtime Python environment to `3.11` | P0 | pilot | done | TBD | Completed: the project now runs on Python 3.11, `pyproject.toml` requires `>=3.11`, and the current runtime/dependencies are aligned with that baseline. |
| IMP-012 | Run integration smoke test with real `GOOGLE_SERVICE_ACCOUNT_FILE` and `GOOGLE_SHEETS_SPREADSHEET_ID` | P0 | pilot | planned | TBD | Confirm end-to-end writes to `data_facts` |
| IMP-013 | Fix pilot operational mode: queue runs without retry/DLQ | P2 | pilot | planned | TBD | Intentionally simplified mode for an audience of ~5 users |
| IMP-014 | Protect queue worker from hot-loop on LLM timeouts | P0 | pilot | done | TBD | Implemented in `src/application/queue_worker.py`: on `LLMTimeoutError` the task is requeued, the event is logged with `timeout_backoff_seconds`, and the worker sleeps before the next dequeue. Result: no API spam and lower load spikes. |
| IMP-015 | Add DLQ/parking flow for non-recoverable tasks | P1 | post-pilot | planned | TBD | Reason: the same task can return to `pending` indefinitely. Result: stable queue and explicit manual triage path. |
| IMP-016 | Ask the user for confirmation before writing data to Google Sheets | P1 | pilot | done | TBD | Implemented in `src/presentation/telegram_polling_handler.py`, `src/presentation/notification_service.py`, `src/infrastructure/pending_confirmation_repository.py`, and `src/application/queue_worker.py`: parsed records are now stored as pending confirmations, the bot shows `Confirm / Edit / Cancel`, and Google Sheets write happens only after explicit user confirmation. |
| IMP-017 | Improve fallback to preserve valid fields instead of nulling all structure | P1 | post-pilot | planned | TBD | Reason: current fallback nulls all classification fields (`src/application/fallback_mapper.py`). Result: higher data completeness under partial validation failures. |
| IMP-018 | Sanitize/limit fallback `comment` before writing to Sheets | P1 | pilot | done | TBD | Implemented in `src/application/fallback_mapper.py`: fallback comment now strips control noise, compacts whitespace, stores only a bounded raw-response preview, and truncates the final text to a safe length before persistence. Result: lower write-failure risk and cleaner reporting data. |
| IMP-019 | Cache dictionaries and dictionary version (mtime/hash strategy) | P0 | post-pilot | planned | TBD | Reason: dictionaries are reloaded and version is recalculated per message (`src/application/classification_orchestrator.py`, `src/infrastructure/dictionary_repository.py`). Result: lower latency and I/O. |
| IMP-020 | Reduce prompt cost via prefix cache and compact dictionary codes | P2 | post-pilot | planned | TBD | Reason: full dictionaries are sent in each prompt (`src/application/prompt_builder.py`). Result: fewer tokens/cost and more stable classification behavior. |
| IMP-021 | Optimize Google Sheets writes (header cache, batch append, strict column control) | P1 | post-pilot | planned | TBD | Reason: `_ensure_headers` is called for each append (`src/infrastructure/google_sheets_repository.py`). Result: fewer API calls and higher throughput. |
| IMP-022 | Add SQLite indexes for queue (`status`, `enqueued_at`, message key) | P1 | post-pilot | planned | TBD | Reason: queue table is currently created without indexes (`src/infrastructure/queue_repository.py`). Result: predictable performance as queue grows. |
| IMP-023 | Add structured event `payload_persisted` (without `raw_text`) | P2 | post-pilot | planned | TBD | Reason: success logs confirm write but not saved classification payload (`src/application/classification_orchestrator.py`). Result: easier investigation of partial extraction cases. |
| IMP-024 | Add startup preflight checks (LLM, Sheets, dictionaries, worksheet) | P1 | pilot | done | TBD | Implemented via `src/application/startup_preflight.py`: both `main_polling` and `main_queue_worker` now run fail-fast checks before startup for dictionaries, Gemini availability, and Google Sheets worksheet/header access. Result: fail-fast startup and fewer runtime user-facing errors. |
| IMP-025 | Introduce CI quality gate (`pytest`, `ruff`, `mypy`) | P1 | pilot | planned | TBD | Reason: no tests in repo and static checks are not part of pipeline yet. Result: safer changes and fewer regressions. |
| IMP-026 | Clean workspace artifacts and extend `.gitignore` (including `*.swp`) | P2 | pilot | planned | TBD | Reason: swap artifacts can be accidentally committed (e.g., `.llm_payload_normalizer.py.swp`). Result: cleaner repository hygiene. |
| IMP-027 | Remove duplicated bootstrap/wiring between `main_polling` and `main_queue_worker` | P2 | post-pilot | planned | TBD | Reason: both entrypoints duplicate service construction logic. Result: simpler maintenance and lower configuration drift risk. |
| IMP-028 | Add Telegram button-based menu for main user actions | P2 | pilot | done | TBD | Implemented in `src/presentation/telegram_polling_handler.py` and `src/presentation/notification_service.py`: the bot now exposes persistent main-menu buttons, inline input helpers, and post-save action buttons for a clearer guided UX. |
| IMP-029 | Build and publish the project schedule sheet in Google Sheets | P2 | post-pilot | planned | TBD | Reason: the pilot currently stores facts but does not publish a structured schedule view. Result: stakeholders get a readable planning/reporting sheet for direct use in Google Sheets. |
| IMP-030 | Add bot search and query flow over the project schedule | P2 | post-pilot | planned | TBD | Reason: the bot currently supports reporting only and cannot retrieve facts from the schedule. Result: users can query recorded data and get schedule information directly in Telegram. |
| IMP-031 | Introduce hybrid webhook ingress: handle `/start`, buttons, and short callbacks inline, but enqueue free-form progress reports immediately for worker-side processing | P1 | post-pilot | planned | TBD | Reason: this is a practical compromise for webhook mode without a full architecture split. Result: Telegram gets a fast webhook response, lightweight UX actions stay immediate, and heavy LLM/Sheets processing moves off the HTTP request path. |

## Next Candidates for Implementation

1. `IMP-019` (cache dictionaries and dictionary version).
2. `IMP-021` (Google Sheets write-path optimization).
3. `IMP-017` (preserve valid fields during fallback instead of nulling all structure).
