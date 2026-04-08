# Business Documentation

Status: normative Stage 22 business documentation with Stage 23 extension-boundary supplement.

## Purpose

This folder contains the project business model that should be used for implementation, sheet design, and validation logic.
It formalizes the Stage 21 target-model draft into project-facing business documentation.

## Normative Position

- `docs/business/*` is the normative project business source of truth.
- `docs/business/Deep research/*` is the evidence archive and research rationale layer.
- If a research document and a project business document differ, the normative interpretation lives in `docs/business/*`.

## Core Business Model

The project uses two separate but connected business registers:

1. `schedule`
   The governance-aware hybrid schedule register.
   It represents both production and project-delivery logic through versions, items, dependencies, hierarchy, coding, progress, and governance context.

2. `data_facts`
   The confirmed operational evidence register.
   It stores immutable fact records received through the Telegram workflow before controlled mapping into schedule logic.

The key pilot semantic coordinate remains:

- `function` as the business workstream;
- `stage` as the lifecycle position inside that workstream.

In the broader Stage 22 model, `function` is the pilot workstream vocabulary used on schedule items and facts, while the schedule itself is no longer treated as a flat task list only.

## Source-of-Truth Hierarchy

1. `docs/business/dictionaries/*`
   Controlled vocabularies and canonical labels.
2. `docs/business/dictionaries/phases.txt`
   Controlled 7-phase portfolio coordinate used on schedule rows.
3. `docs/business/dictionaries/planned_cost_reference.md`
   Normative reference for `Planned Cost` assignment.
4. `docs/business/stage_function_model.md`
   Central semantic coordinate system for `function` and `stage`.
5. `docs/business/schedule_model.md`
   Normative schedule business model.
6. `docs/business/sheets/schedule_workbook.md`
   Pilot workbook structure for baseline/current schedule control.
7. `docs/business/sheets/schedule_field_rules.md`
   Detailed field behavior, formulas, validation, and protection rules for the pilot workbook.
8. `docs/business/extension_architecture.md`
   Named bounded extension families and promotion criteria beyond the pilot core.
9. `docs/business/rule_catalog.md`
   Stable rule set governing the model.
10. `docs/business/sheets/schedule_sheet.md`
   Flattened pilot row schema used by the baseline/current schedule sheets.
11. `docs/business/examples/schedule_examples.md`
   Worked schedule examples.
12. `docs/business/examples/schedule_baseline_template.md`
    Reference template of the first full baseline project `P01`.
13. `docs/business/fact_model.md`
   Normative fact business model.
14. `docs/business/fact_to_schedule_mapping.md`
   Controlled business bridge between facts and the schedule.
15. `docs/business/sheets/data_facts_sheet.md`
    Current pilot evidence-sheet specification.
16. `docs/business/examples/fact_examples.md`
    Worked fact examples.
17. `docs/business/business_decision_log.md`
    Accepted business decisions and rationale.
18. `docs/business/Deep research/*`
    Supporting evidence base used to derive the current model.

## Folder Structure

- `dictionaries/`
  Pilot dictionaries and controlled value sets.
- `dictionaries/planned_cost_reference.md`
  Normative reference for baseline and current planned-cost assignment.
- `dictionaries/phases.txt`
  Controlled portfolio-phase coordinate for schedule rows.
- `stage_function_model.md`
  Core semantic model for `function` and `stage`.
- `schedule_model.md`
  Normative schedule business model derived from Stage 21.
- `sheets/schedule_workbook.md`
  Pilot workbook structure for baseline/current control.
- `sheets/schedule_field_rules.md`
  Detailed field behavior, formulas, validation, and protection rules.
- `extension_architecture.md`
  Normative boundary for heavy extension families beyond the pilot core.
- `fact_model.md`
  Normative fact and evidence model.
- `fact_to_schedule_mapping.md`
  Mapping logic between facts and schedule interpretation.
- `rule_catalog.md`
  Stable business rules with IDs.
- `business_decision_log.md`
  Accepted business decisions.
- `sheets/`
  Sheet-level pilot projections of the business model.
- `examples/`
  Worked examples for interpretation and onboarding.
- `examples/schedule_baseline_template.md`
  Reference-template baseline structure used to assemble the first full project `P01`.
- `Deep research/`
  Research corpus, comparative evidence, and target-model drafting history.

## Current Position

- The schedule model is now formally defined as a hybrid model rather than a flat task list.
- `function + stage` remains the minimum pilot business coordinate, but it now sits inside a broader schedule structure.
- The pilot schedule workbook now uses separate `schedule_baseline` and `schedule_current` surfaces.
- The live workbook now also includes a compact `dashboard_portfolio` sheet for executive portfolio reporting.
- The live workbook also includes a `dashboard_visual` sheet that turns the compact portfolio dashboard into management-facing charts.
- The portfolio dashboard includes a compact earned value analysis (`BAC`, `PV`, `EV`, `AC`, `CV`, `SV`, `CPI`, `SPI`, `EAC`, `VAC`) based on schedule cost fields.
- The first baseline implementation is assembled as one full residential high-rise template project `P01`, after which additional projects are cloned and time-shifted into `P02-P07`.
- `schedule_baseline` may store planned `% complete` and derived `Status` as of the sheet `Status Date` for actionable non-`wbs` rows.
- `wbs` rows stay blank for pilot `% complete`, `Status`, and `Planned Cost`.
- `Task ID` is the single immutable pilot identifier, uses project-banded ranges such as `T1xxxx` to `T7xxxx`, and is never reused.
- `Status Date` is a single sheet-level control date for each workbook surface and is implemented as `=TODAY()` in the live workbook.
- `Phase` is a manual dictionary-backed portfolio coordinate and does not replace `Stage`.
- Baseline and current control are separated through workbook surfaces and fact logic rather than mixed into one mutable task record.
- The portfolio dashboard is a reporting surface only and reads from baseline/current/meta/validation without becoming a third schedule register.
- Planned and actual quantity-cost values are stored separately, and in-progress timing uses `Forecast Start`, `Forecast Finish`, and `Remaining Duration`.
- `Planned Cost` uses the normalized `Global USD 2026` hybrid-split reference documented in `dictionaries/planned_cost_reference.md`.
- `Item Kind` and `Item Type` now separate primary row meaning from optional subtype detail.
- `Responsible` is controlled through responsibility-bucket dictionaries rather than person names.
- Governance, approvals, payments, handover, and external system linkage are part of the schedule business model, not comments around it.
- Facts remain controlled evidence first; schedule mutation remains deliberate and traceable rather than automatic.
- Stage 23 clarified that PMIS, EDMS, permit, smart-site, resource, and payment systems are researched bounded extensions, not undefined future scope.
