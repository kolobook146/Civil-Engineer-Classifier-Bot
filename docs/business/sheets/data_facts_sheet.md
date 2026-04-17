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
15. `verification`

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
- `verification`: workbook-level business verification result, either `verified` or `not verified`.

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

## Verification Convention

`verification` is not the same as `status`.

- `status` is the technical processing state of the fact pipeline.
- `verification` is the business check against the current schedule model.

In the pilot workbook, `verification` is calculated from a hidden helper sheet
`fact_verification_helper`:

- facts are matched to formula-fed `schedule_current` rows by
  `stage + function + work_type + unit`;
- if no eligible `schedule_current` row exists, the fact is `not verified`;
- if cumulative `volume` for that same four-field key exceeds available schedule
  capacity, all facts for that key are `not verified`;
- otherwise the fact is `verified`.

For physical quantity rows, capacity is the summed `Planned Quantity` of eligible
schedule rows. For non-physical rows without planned quantity, capacity is the count
of eligible rows because the bot writes `volume = 1` as a binary completion marker.

This is a pilot verification signal, not a full approval workflow.
