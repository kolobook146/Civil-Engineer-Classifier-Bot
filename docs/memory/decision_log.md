# Decision Log

Status: active project decision memory.

Purpose: keep compact records of project decisions that should survive prompt rewrites, refactors, and restarts. Dates below are backfilled from the current project state where exact decision dates were not formally recorded.

## Decision Format

- `id`: stable decision identifier.
- `status`: `accepted`, `superseded`, or `proposed`.
- `decision`: what we decided.
- `rationale`: why we decided it.
- `impact`: what parts of the project rely on it.

## Decisions

| id | status | decision | rationale | impact |
|---|---|---|---|---|
| DEC-001 | accepted | Use project-local text files as the pilot source of truth for dictionaries. | The pilot needs transparent, editable, low-friction dictionary management without adding external services. | `docs/business/dictionaries/*`, prompt assembly, classification consistency. |
| DEC-002 | accepted | Keep `function` and `stage` mandatory in classification output. | The schedule model depends on every fact having a workstream and lifecycle position. | Prompt rules, validation rules, downstream schedule logic. |
| DEC-003 | accepted | Preserve `raw_text` for every fact, including incomplete or fallback parses. | Source traceability is required for audit, debugging, and future reprocessing. | Google Sheets payload, logs, troubleshooting, prompt improvement. |
| DEC-004 | accepted | Use explicit user confirmation before writing facts to Google Sheets. | This reduces accidental persistence of ambiguous or partially correct parses. | Pending confirmation flow, Telegram UX, queue completion flow. |
| DEC-005 | accepted | Use Google Sheets as the pilot business-facing register. | The target audience needs a familiar, collaborative reporting surface with minimal onboarding. | `data_facts`, schedule publication, operational workflows. |
| DEC-006 | accepted | Use Gemini through the native `google-genai` SDK. | The pilot already has Gemini access and benefits from a supported provider-native integration path. | `src/infrastructure/gemini_client.py`, environment configuration, dependency set. |
| DEC-007 | accepted | Keep `volume` as a decimal quantity in the domain and schema contract. | Construction facts can include fractional quantities and different decimal separators. | Schema, normalization, validation, Sheets export, analytics. |
| DEC-008 | accepted | Treat `function` as a workstream and `stage` as a lifecycle gate within that workstream. | This reflects the project's matrix model for schedule construction and dependency mapping. | Prompt semantics, dictionaries, future dependency matrix. |
| DEC-009 | accepted | Use queue-based deferred processing when online classification cannot complete in time. | User-facing responsiveness is more important than blocking the Telegram flow on heavy processing. | Queue worker, timeout handling, post-factum confirmation flow. |
| DEC-010 | accepted | Keep always-loaded context short and stable instead of turning it into a large knowledge base. | Long static prompt blocks increase token cost and become hard to maintain. | Prompt design, memory strategy, future context injection. |

## How To Use This File

- Add a new row when a project-level technical or product decision is made.
- Mark old rows as `superseded` instead of deleting them.
- Store implementation details in code or docs, not in the decision text itself.
- If a prompt rule exists because of a specific project decision, link that rule back to a decision ID in future revisions.
