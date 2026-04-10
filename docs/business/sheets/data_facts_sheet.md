# Data Facts Sheet Specification

Status: current pilot sheet specification.

## Sheet Purpose

The `data_facts` sheet stores confirmed progress facts reported through the bot.

## Current Column Order

1. `raw_text`
2. `volume`
3. `unit`
4. `work_type`
5. `stage`
6. `function`
7. `comment`
8. `timestamp`
9. `user_id`
10. `chat_id`
11. `message_id`
12. `model`
13. `classifier_version`
14. `status`

## Business Meaning of Columns

- `raw_text`: original user message.
- `volume`: reported decimal quantity when present; for non-physical pilot facts the bot may write `1` as a binary completion marker.
- `unit`: canonical measurement unit.
- `work_type`: optional construction scope refinement.
- `stage`: mandatory lifecycle gate.
- `function`: mandatory workstream.
- `comment`: residual useful text or ambiguity note.
- `timestamp`: time of fact persistence.
- `user_id`: reporting user.
- `chat_id`: Telegram chat identifier.
- `message_id`: Telegram message identifier.
- `model`: LLM model used for extraction.
- `classifier_version`: classifier version identifier.
- `status`: processing state of the fact.

## Business Role of This Sheet

This is the operational evidence register of reported progress.
It supports audit, later re-interpretation, analytics, and future schedule linkage.

## Current Pilot Fact Convention

For the current workbook pilot:

- physical rows continue to use measured `volume`;
- non-physical rows may use `volume = 1`;
- `timestamp` remains the persisted fact time and is used by the workbook as the source of:
  - earliest matching fact date for `Actual Start`;
  - latest matching fact date for `Actual Finish` once the row is complete.
