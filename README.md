# Civil Engineer's Classifier Bot

A Telegram bot (@TavridaDevelopmentBot) that classifies any free-form project update into a strict, predefined lifecycle schedule structure for an investment construction project, based on a selected coding framework, and writes the data to Google Sheets.

Google Sheets reference (pilot data dictionary):  
https://docs.google.com/spreadsheets/d/17AASCMKd6DtSUjoheuF1MrPVm6iSzBHq--p7Rc4jd1s/edit?usp=sharing

For the pilot, the baseline structure is built around three top-level coding groups:
- Functions: typical functions required to deliver a project (Financing, Marketing, Design, Construction).
- Stages: standardized stages used to produce results within each function (Terms of Reference, Tender, Contract, Procurement, Execution).
- Work Types: first-level classification of construction and installation work types (Earthworks, Piling, Concreting, Electrical Installation Works, Landscaping, etc.).

This structure enables end-to-end analytics, cost control across project delivery, operational planning, and comparison of alternative development scenarios for management decision-making.

## 1. Project Goal

Build a pilot system that:
- accepts user messages about completed work in free-form text;
- extracts structured fields based on project dictionaries;
- stores both structured data and the original message text;
- notifies the user either immediately or post-factum (if the message is queued).

## 2. Pilot Scope

In scope for the pilot:
- Telegram `polling` (not webhook);
- LLM classification using Google Gemini (`gemini-2.5-flash`) via the native `google-genai` SDK with a 30-second timeout;
- strict JSON validation of the LLM output before persistence;
- fallback logic for invalid JSON;
- writing data to Google Sheets (`data_facts`);
- a deferred-processing queue with post-factum user notification.

Out of scope for the pilot (post-pilot):
- idempotent writes by unique message key;
- retry policy (1/5/15 minutes) and DLQ;
- logging of confidence values and reasons for empty fields;
- operational monitoring (timeouts, queue size, persistence errors);
- dictionary schema expansion to `code`, `label`, `description` (currently only `label` is used).

## 3. Functional Requirements

### 3.1 User Interaction Flow

1. The user opens a chat with the bot.
2. The user presses `/start`.
3. The bot sends a welcome message and offers `Report Progress`.
4. The user presses `Report Progress`.
5. The bot sends instructions for free-form input.
6. The user submits a free-form message.

### 3.2 Message Processing

1. The bot receives updates via Telegram `polling`.
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
- `stage` (one dictionary value or `null`);
- `function` (one dictionary value or `null`);
- `comment` (unmapped/free text or `null`).

### 3.4 Validation and Fallback

1. LLM output is validated against a strict JSON schema.
2. If JSON is valid:
   - a record is created with status `PROCESSED`.
3. If JSON is invalid:
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

### 3.6 Queue and Deferred Processing

If the LLM does not respond within 30 seconds:
1. The message is queued with status `QUEUED`.
2. The user is notified that the message is queued.
3. A queue worker processes the message later via the same pipeline:
   - LLM -> validation -> fallback (if needed) -> write to `data_facts`.
4. After successful persistence, the user receives a post-factum notification:
   - `Queued message has been recorded`.

## 4. Non-Functional Requirements

### 4.1 Reliability

- Messages must not be lost when LLM timeouts occur.
- `raw_text` must always be persisted, even with partial or failed parsing.
- The queue must guarantee eventual processing of deferred messages.

### 4.2 Performance

- Online LLM timeout: 30 seconds.
- If timeout is exceeded, the system must quickly return a queued status to the user.

### 4.3 Data Quality

- Strict JSON validation before persistence.
- `unit`, `workType`, `stage`, and `function` must be single-value (`one value or null`) and must belong to their dictionaries.

### 4.4 Maintainability

- Dictionaries must be updatable without code changes (via text files).
- Classifier version (`classifier_version`) must be stored in every record.

### 4.5 Observability (Pilot Baseline)

- Key events are logged:
  - message received,
  - LLM response/timeout,
  - validation result,
  - Google Sheets write result,
  - queue enqueue/dequeue.
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

## 7. Pilot Constraints

- `polling` only (no webhook).
- No roles or access control.
- No edit/cancel flow for previously recorded entries.
- No deduplication by `chat_id + message_id`.
- Unit aliases normalization is still out of scope (verification is done against the units dictionary).
- `volume` is stored as `Decimal` in the domain model and persisted as normalized decimal text in Google Sheets.

## 8. Preferred Technologies

- Language: Python 3.11+.
- Telegram: `python-telegram-bot` (polling mode).
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

## 10. Pilot Acceptance Criteria

1. A user free-form message is persisted to `data_facts`.
2. `raw_text` is always present in `data_facts`.
3. With valid JSON, fields are correctly populated according to the schema.
4. With invalid JSON, raw LLM output is written to `comment`.
5. On a 30-second timeout, the message is queued and later processed.
6. After queue processing, the user receives a post-factum notification.

## 11. Run Process

### 11.1 Prerequisites

- Python 3.11+
- Telegram bot token
- Gemini API key
- Google service account JSON key file
- Access granted to the target Google Sheets document for the service account

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
- `GOOGLE_SERVICE_ACCOUNT_FILE`

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

### 11.4 Stop

- Press `Ctrl + C` in each terminal.

## 12. Contacts

- Telegram: `@kolobook146`
- E-mail: `galaxykolodkin@gmail.com`
- Phone: `+7 (952) 652-09-07`
