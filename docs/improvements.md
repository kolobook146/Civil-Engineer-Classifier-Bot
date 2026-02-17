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
| IMP-001 | Idempotent write to Google Sheets using a unique message key (`chat_id + message_id`) | P1 | post-pilot | planned | TBD | Prevent duplicates during reprocessing |
| IMP-002 | Queue retry policy (1/5/15 minutes) and DLQ | P1 | post-pilot | planned | TBD | Improve reliability during temporary LLM/Sheets failures |
| IMP-003 | Log confidence and reasons for empty classification fields | P2 | post-pilot | planned | TBD | Improve prompt and dictionary quality |
| IMP-004 | Monitoring: LLM timeouts, queue size, invalid JSON rate, Sheets errors | P1 | post-pilot | planned | TBD | Metrics + alerts |
| IMP-005 | Expand dictionary structure to `code`, `label`, `description` | P1 | post-pilot | planned | TBD | Currently only `label` is used |
| IMP-006 | Normalize measurement units via a dedicated units and aliases dictionary | P2 | post-pilot | planned | TBD | Unit variation is currently delegated to the LLM |
| IMP-007 | Deduplicate incoming messages by `chat_id + message_id` at ingestion layer | P2 | post-pilot | planned | TBD | Separate from idempotent persistence |
| IMP-008 | Access roles (who can submit execution facts) | P2 | post-pilot | planned | TBD | Pilot access is open |
| IMP-009 | User edit/cancel flow for previously recorded entries | P3 | post-pilot | planned | TBD | Requires UX and versioning model |
| IMP-010 | Synonyms/abbreviations catalog for dictionaries (e.g., HVAC, WSS, C&I works, commissioning) | P2 | post-pilot | planned | TBD | Improve mapping accuracy to `label` |
| IMP-011 | Upgrade runtime Python environment to `3.11` | P0 | pilot | planned | TBD | Required for compatibility (e.g., `StrEnum`) |
| IMP-012 | Run integration smoke test with real `GOOGLE_SERVICE_ACCOUNT_FILE` and `GOOGLE_SHEETS_SPREADSHEET_ID` | P0 | pilot | planned | TBD | Confirm end-to-end writes to `data_facts` |
| IMP-013 | Fix pilot operational mode: queue runs without retry/DLQ | P2 | pilot | planned | TBD | Intentionally simplified mode for an audience of ~5 users |

## Next Candidates for Implementation

1. `IMP-011` (upgrade Python to `3.11`).
2. `IMP-012` (Google Sheets write smoke test).
3. `IMP-005` (dictionary structure `code/label/description`).
