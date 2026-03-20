# Project Always-Loaded Context

Status: prepared as a project memory source; not yet injected into the live prompt.

## Purpose

This file stores the shortest stable context that should remain consistent across prompt revisions. It is not a replacement for dictionaries, examples, or full prompt instructions. It is the minimal project frame that keeps the classifier aligned with the intended business model.

## Core Project Context

- The bot converts free-form Telegram progress messages into a structured record for a construction project reporting and scheduling workflow.
- The result is reviewed by the user before it is written to Google Sheets.
- `raw_text` must always be preserved, even if the parse is incomplete.
- Auditability is required: timestamp, user ID, chat ID, message ID, model, classifier version, and processing status are part of the working data model.

## Classification Semantics

- `function` = functional workstream: what is being delivered, managed, or advanced within the project.
- `stage` = lifecycle gate within a function: where that workstream is now.
- `stage` and `function` are mandatory classification outputs.
- `work_type` is a controlled dictionary value and may be empty if evidence is insufficient.
- `volume` is a decimal quantity when present.
- `unit` must be normalized to one canonical dictionary key when present.
- Any text that cannot be mapped into the structured fields must be preserved in `comment`.

## Operational Rules

- The pilot uses project-local text dictionaries as the source of truth.
- The pilot keeps a single selected value or no value for `work_type`; multi-select is not allowed.
- The pilot does not support editing previously saved records after confirmation.
- If online processing cannot complete in time, the task may move to the queue and the user must receive a later confirmation card.

## Prompt Design Guidance

- Keep this context short and stable.
- Do not duplicate full dictionaries in this file.
- Do not place volatile implementation details here.
- If a rule changes often, it belongs in the active prompt builder or a dedicated dictionary/alias layer, not in the always-loaded context.
