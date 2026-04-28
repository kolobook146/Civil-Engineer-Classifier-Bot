# Civil Engineer's Classifier Bot

Telegram bot:  
https://t.me/TavridaDevelopmentBot

Live Google Sheets workbook and dashboards:  
https://docs.google.com/spreadsheets/d/17AASCMKd6DtSUjoheuF1MrPVm6iSzBHq--p7Rc4jd1s/edit?usp=sharing

A Telegram bot and Google Sheets pilot that turns free-form construction progress messages into verified schedule intelligence for an investment-construction portfolio.

The core business idea is a three-dimensional semantic control model:
- `Function`: business workstream.
- `Stage`: lifecycle position inside the workstream.
- `Work Type`: scope detail.

Together with `Unit`, `Volume`, `Date`, and project context, this coordinate lets a field fact flow into `data_facts`, pass workbook-level verification, update eligible rows in `schedule_current`, and feed executive dashboards without corrupting `schedule_baseline`.

## 1. Project Goal

Build a pilot system that:
- accepts user messages about completed work in free-form text;
- extracts structured fields based on project dictionaries;
- stores both structured data and the original message text;
- asks the user for confirmation before writing to Google Sheets, including post-factum after queued processing;
- uses the workbook to verify facts against the current schedule model;
- exposes portfolio reporting through A4 dashboard sheets and bot-exported previews.

## 2. Pilot Scope

In scope for the pilot:
- Telegram `polling` by default, plus an optional built-in `webhook` mode for local development via `ngrok`;
- LLM classification using Google Gemini (`gemini-2.5-flash`) via the native `google-genai` SDK with a 30-second timeout;
- strict JSON validation of the LLM output before persistence;
- fallback logic for invalid JSON;
- writing data to Google Sheets (`data_facts`) only after explicit user confirmation;
- workbook-calculated `data_facts.verification` based on eligible `schedule_current` rows and cumulative volume capacity;
- separate `schedule_baseline` and `schedule_current` workbook surfaces, with the active pilot portfolio covering `P01-P07`;
- formula-fed actual progress in `schedule_current` for assigned open rows, using the pilot coordinate `Stage + Function + Work Type + Unit`;
- a deferred-processing queue with bounded retry/backoff (`1/5/15 minutes` with jitter);
- on-demand report export for three dashboard sheets to a local archive (`PDF + JPEG`), with JPEG preview and optional PDF delivery in Telegram;
- post-factum confirmation cards for queued messages.

Out of scope for the pilot (post-pilot):
- idempotent writes by unique message key;
- DLQ / parking flow for non-recoverable queue tasks;
- logging of confidence values and reasons for empty fields;
- operational monitoring (timeouts, queue size, persistence errors);
- dictionary schema expansion to `code`, `label`, `description` (currently only `label` is used);
- full approval workflow for fact verification;
- production financing-source register for real loan drawdown / treasury schedules.

## 3. Functional Requirements

### 3.1 User Interaction Flow

1. The user opens a chat with the bot.
2. The user presses `/start`.
3. The bot sends a welcome message and offers `Report Progress`, `Get Reports`, and `Help`.
4. The user either:
   - presses `Report Progress`, receives input instructions, and submits a free-form message; or
   - presses `Get Reports`, chooses a report, and receives a JPEG preview with an optional `Get PDF` action.

### 3.2 Message Processing

1. The bot receives updates via Telegram `polling` or built-in `webhook`.
2. Text preprocessing is applied:
   - `trim`;
   - whitespace normalization.
3. Dictionaries are loaded from project text files:
   - units;
   - work types;
   - stages;
   - functions.
4. The orchestrator builds the LLM request (via `google-genai`) with:
   - full original text (`raw_text`);
   - dictionary content;
   - instructions to return strictly structured JSON;
   - pilot-specific prompt clarification: `stage` = process/project stage, `function` = functional work block.
5. Gemini is called through `google-genai` with a 30-second timeout.

### 3.3 Classification Rules

The LLM must return JSON with the following fields:
- `volume` (optional, decimal `number`);
- `unit` (optional, one dictionary value or `null`);
- `workType` (one dictionary value or `null`);
- `stage` (required, exactly one dictionary value, not `null`);
- `function` (required, exactly one dictionary value, not `null`);
- `comment` (unmapped/free text or `null`).

### 3.4 Validation and Fallback

1. LLM output is validated against a strict JSON schema.
2. If JSON is valid:
   - a record is created with status `PROCESSED`.
3. If JSON is invalid:
   - invalid includes schema violations such as missing or `null` `stage` / `function`;
   - the full LLM output is stored in `comment`;
   - the record is marked as `PROCESSED_WITH_FALLBACK`.

### 3.5 Google Sheets Persistence

Data is written to the `data_facts` sheet and always includes:
- `raw_text` (required);
- classification fields;
- audit fields:
  - `timestamp`,
  - `user_id`,
  - `chat_id`,
  - `message_id`,
  - `model`,
  - `classifier_version`,
  - `status`.
- workbook-calculated field:
  - `verification`.
- Online and queued records are written only after explicit user confirmation.
- `verification` is a business verification signal (`verified` / `not verified`), not a replacement for technical processing `status`.

### 3.6 Workbook Schedule and Dashboard Logic

The workbook is part of the implemented pilot logic, not just a passive storage file.

- `data_facts` is the immutable evidence register written by the bot after user confirmation.
- `schedule_baseline` is the governed comparison surface.
- `schedule_current` is the operational schedule twin.
- `schedule_meta` stores live `Status Date = TODAY()` for both schedule surfaces.
- The active portfolio uses project-banded `Task ID` ranges for `P01-P07` (`T1xxxx` to `T7xxxx`).
- `Phase` is a manual dictionary-backed portfolio coordinate on schedule rows and does not replace `Stage`.
- `fact_collection_map` assigns each template task to no more than one project clone for formula-fed fact collection.
- For physical rows, `Actual Quantity` may aggregate measured `data_facts.volume`.
- For non-physical pilot rows, the bot convention is `volume = 1` as a binary progress/completion signal.
- Open formula-fed rows may derive `Actual Start` from the earliest matching fact date and `Actual Finish` from the latest matching fact date after the completion rule is met.
- Quantity-driven `Actual Cost` uses the pilot proportional formula `ROUND(Actual Quantity / Planned Quantity * Planned Cost, 2)`.
- `data_facts.verification` is calculated from the same four-field coordinate and cumulative capacity in eligible `schedule_current` rows.
- Dashboard sheets read the controlled schedule surfaces, not raw `data_facts` directly.

The main visible reporting surfaces are:

- `dashboard_visual`: executive visual dashboard with portfolio progress, EVA / cost-control signals, schedule signal, and a pilot 12-month funding need / sources chart.
- `monthly_controls_a4`: monthly PMO controls pack.
- `departments_a4`: responsibility / workstream accountability dashboard.

### 3.7 Queue and Deferred Processing

If the LLM does not respond within 30 seconds:
1. The message is queued with status `QUEUED`.
2. The user is notified that the message is queued.
3. A queue worker processes the message later via the same classification pipeline:
   - LLM -> normalization -> schema validation -> fallback (if needed).
4. After successful queued classification, the user receives a post-factum confirmation card.
5. Google Sheets write happens only after the user explicitly confirms that card.
6. If queued processing fails, the task is retried with bounded backoff (`1/5/15 minutes` with jitter).

### 3.8 Report Preview Export

- The bot exposes an on-demand `Get Reports` menu action.
- `Get Reports` opens an inline selector with three pilot reports:
  - `Company Overview`: `dashboard_visual!A1:X32`
  - `Monthly Controls`: `monthly_controls_a4!A1:AA38`
  - `Departments Overview`: `departments_a4!A1:Z36`
- Export flow:
  - selected Google Sheets range -> PDF export
  - PDF -> local archive
  - PDF -> JPEG conversion via macOS `sips`
  - JPEG -> local archive
  - JPEG -> Telegram `photo`
  - optional `Get PDF` -> archived PDF -> Telegram `document`
- Successful exports are archived locally in `var/dashboard_exports/` by default.
- Archive retention in v1 is unlimited; files are not auto-pruned.
- This is a read-only reporting path and does not mutate the workbook.
- Dashboard values change through `schedule_current` after facts are confirmed and consumed by workbook formulas.

## 4. Non-Functional Requirements

### 4.1 Reliability

- Messages must not be lost when LLM timeouts occur.
- `raw_text` must always be persisted, even with partial or failed parsing.
- The queue must guarantee eventual processing of deferred messages.
- Queued tasks must retry with bounded backoff instead of hot-looping on transient failures.

### 4.2 Performance

- Online LLM timeout: 30 seconds.
- If timeout is exceeded, the system must quickly return a queued status to the user.

### 4.3 Data Quality

- Strict JSON validation before persistence.
- `unit` and `workType` must be single-value (`one value or null`) and must belong to their dictionaries.
- `stage` and `function` must be single-value, non-null, and must belong to their dictionaries.
- `verification` marks whether a persisted fact is consumable by the current schedule model and within cumulative volume capacity.
- `verification = not verified` is a review signal; the original evidence remains preserved in `data_facts`.

### 4.4 Maintainability

- Dictionaries must be updatable without code changes (via text files).
- Classifier version (`classifier_version`) must be stored in every record.

### 4.5 Observability (Pilot Baseline)

- Key events are logged:
  - message received,
  - LLM response/timeout,
  - validation result,
  - Google Sheets write result,
  - queue enqueue/dequeue,
  - report export request/success/failure and optional PDF delivery.
- Detailed logging specification: `docs/logging/logging_spec.md`.

## 5. Target Audience

- Construction project managers.
- Site supervisors and foremen.
- Technical office engineers/analysts who need operational progress tracking.
- Project participants submitting daily/shift reports via Telegram.

## 6. Platforms

- Client: Telegram (iOS, Android, Desktop, Web).
- Backend: Python service (Linux/macOS).
- Storage integration: Google Sheets API.
- LLM provider: Google Gemini API (`gemini-2.5-flash`) via native `google-genai` SDK.
- Reporting preview: Google Sheets PDF export + local JPEG conversion (`sips`) for Telegram photo delivery, plus optional archived PDF delivery.

## 7. Pilot Constraints

- `polling` is the default runtime mode; webhook requires a public HTTPS endpoint (for local dev, e.g. `ngrok`).
- No roles or access control.
- No edit/cancel flow for previously recorded entries.
- No deduplication by `chat_id + message_id`.
- Unit canonicalization is limited to known dictionary aliases; full unit conversion remains out of scope.
- `volume` is stored as `Decimal` in the domain model and persisted as normalized decimal text in Google Sheets.
- Report JPEG previews in v1 rely on macOS `sips` for PDF-to-image conversion on the bot host.
- Report exports are archived as runtime files in `var/dashboard_exports/` and are not auto-cleaned in v1.

## 8. Preferred Technologies

- Language: Python 3.11+.
- Telegram: `python-telegram-bot` (polling mode and built-in webhook mode).
- Schema validation: `jsonschema` or `pydantic`.
- LLM SDK: `google-genai` (native Gemini SDK).
- Google Sheets: `gspread` + Google service account.
- Pilot queue: SQLite/file-backed queue + separate worker process.
- Logging: standard `logging` (JSON logs preferred).

## 9. Architecture Artifacts

- BPMN: `docs/bpmn/reporting_flow.bpmn`
- UML Activity: `docs/uml/reporting_activity.puml`
- UML Class: `docs/uml/reporting_class_diagram.puml`
- Logging spec: `docs/logging/logging_spec.md`
- Business model: `docs/business/README.md`
- Schedule workbook rules: `docs/business/sheets/schedule_workbook.md`
- Fact-to-schedule mapping: `docs/business/fact_to_schedule_mapping.md`

## 10. Pilot Acceptance Criteria

1. A user free-form message results in a confirmation card and is persisted to `data_facts` only after explicit confirmation.
2. `raw_text` is always present in `data_facts`.
3. With valid JSON, fields are correctly populated according to the schema, including non-null `stage` and `function`.
4. With invalid JSON, raw LLM output is written to `comment`.
5. On a 30-second timeout, the message is queued and later processed with bounded retry/backoff.
6. After queue processing, the user receives a post-factum confirmation card before any Google Sheets write.
7. Persisted facts include a row-local `verification` formula in `data_facts`.
8. On `Get Reports`, the user can choose one of three reports and receive a JPEG preview.
9. After receiving a JPEG preview, the user can request the matching archived PDF via `Get PDF`.

## 11. Run Process

### 11.1 Prerequisites

- Python 3.11+
- Telegram bot token
- Gemini API key
- Google service account JSON key file
- Access granted to the target Google Sheets document for the service account
- macOS host with `/usr/bin/sips` available if report JPEG preview is enabled
- Writable local runtime directory for report archive storage (`var/dashboard_exports/` by default)

### 11.2 Setup

1. Install project dependencies:

```bash
python3 -m pip install -e .
```

2. Create environment file from template:

```bash
cp .env.example .env
```

3. Fill required values in `.env`:
- `TG_BOT_TOKEN`
- `LLM_API_KEY`
- `GOOGLE_SHEETS_SPREADSHEET_ID`

Optional report export override:
- `STARTUP_PREFLIGHT_ENABLED` (`false` for pilot runtime, `true` before production rollout)
- `GOOGLE_SHEETS_DASHBOARD_ARCHIVE_DIR` (default `var/dashboard_exports`)
- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_SERVICE_ACCOUNT_FILE`
- `LLM_PREFLIGHT_ENABLED` (`false` for active dev/debug with frequent restarts, `true` before production rollout)

### 11.3 Start the Services

Run in two separate terminals from the project root.

Terminal 1 (Telegram polling bot):

```bash
cd "/Users/kolobook/Documents/TG Build Bot"
PYTHONPATH=src python3 src/main_polling.py
```

Terminal 2 (queue worker):

```bash
cd "/Users/kolobook/Documents/TG Build Bot"
PYTHONPATH=src python3 src/main_queue_worker.py
```

### 11.4 Optional Webhook Mode (Local Development via ngrok)

Use this mode if you want Telegram to push updates to a local built-in webhook server instead of polling.

1. Start the queue worker in Terminal 1:

```bash
cd "/Users/kolobook/Documents/TG Build Bot"
PYTHONPATH=src python3 src/main_queue_worker.py
```

2. Start an HTTPS tunnel to the local webhook port in Terminal 2:

```bash
ngrok http 8080
```

3. Copy the public `https://...` URL shown by `ngrok` and set it in `.env`:
- `WEBHOOK_PUBLIC_BASE_URL=https://<your-ngrok-domain>`

4. Start the webhook bot in Terminal 3:

```bash
cd "/Users/kolobook/Documents/TG Build Bot"
PYTHONPATH=src python3 src/main_webhook.py
```

5. Telegram will now send updates to:
- `https://<your-ngrok-domain>/telegram/webhook`

Notes:
- If the `ngrok` URL changes, update `WEBHOOK_PUBLIC_BASE_URL` and restart `src/main_webhook.py`.
- `WEBHOOK_SECRET_TOKEN` is optional but recommended.
- The local server listens on `WEBHOOK_LISTEN_HOST:WEBHOOK_LISTEN_PORT` (default `127.0.0.1:8080`).

### 11.5 Stop

- Press `Ctrl + C` in each terminal.

## 12. Contacts

- Telegram: `@kolobook146`
- E-mail: `galaxykolodkin@gmail.com`
- Phone: `+7 (952) 652-09-07`
