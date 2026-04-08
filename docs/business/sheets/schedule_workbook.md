# Schedule Workbook Specification

Status: normative pilot workbook specification for the control schedule.

## Purpose

This document defines the workbook-level business structure used to store the pilot schedule in Google Sheets.
It complements:

- `docs/business/sheets/schedule_sheet.md`
- `docs/business/sheets/schedule_field_rules.md`

The pilot workbook is a control-oriented business surface for:

- schedule planning;
- schedule statusing;
- baseline-versus-current comparison;
- dashboard extraction;
- Telegram bot lookup.

## Design Position

The pilot workbook is intentionally simpler than a full enterprise PMIS.
It keeps one bounded schedule core and does not duplicate heavy extension systems inside Google Sheets.

The workbook is built around two comparable schedule surfaces:

- `schedule_baseline`
- `schedule_current`

Both sheets use the same row schema and are compared directly by immutable `Task ID`.

The baseline is assembled in two steps:

1. build one complete reference-template project `P01`;
2. clone and time-shift that template into additional projects later when portfolio-style coverage is needed.

The accepted pilot portfolio implementation uses:

- `P01-P07` in one `schedule_baseline`;
- one new manual field `Phase` on schedule rows;
- `Status Date = TODAY()` for both schedule surfaces.

## Workbook Tabs

### `schedule_meta`

One row per schedule surface.

Required fields:

- `Sheet Name`
- `Schedule ID`
- `Schedule Purpose`
- `Version Type`
- `Version ID`
- `Status Date`
- `Cost Currency`

Business meaning:

- `Schedule Purpose` is fixed to `control` in the current pilot.
- `Version Type` is either `baseline` or `current`.
- `Version ID` is the human-readable version identifier.
- `Status Date` is the single reporting date of that sheet version and is implemented as `=TODAY()` in the workbook.
- `Cost Currency` is the workbook-level currency for planned and actual cost values.

### `schedule_baseline`

Frozen baseline surface used for comparison.

Business rules:

- rows are not edited as a working schedule;
- the sheet is replaced only through controlled baseline publication;
- calculated values should be frozen on publication;
- it is used for variance reading, dashboards, and comparison against the current control view.
- it may also store planned progress state as of the sheet `Status Date` for non-`wbs` rows;
- `wbs` rows remain blank for progress and status in the pilot baseline;
- the first implementation baseline is a fully detailed reference-template project `P01` for a residential high-rise investment-construction project;
- later `P02-P07` branches should be created by cloning and time-shifting the approved `P01` template instead of inventing separate business structures;
- the active portfolio baseline uses all `P01-P07` branches in one sheet so that all 7 macro phases are represented on one live control date.

### `schedule_current`

Active control surface used for ongoing work.

Business rules:

- this is the main operational schedule sheet in the pilot;
- current status, actuals, and open-row projection values live here;
- facts still remain separately governed in `data_facts`.

### `used_task_ids`

Append-only register of all issued `Task ID` values.

Required fields:

- `Task ID`
- `Created In Version ID`
- `Created At`
- `Current State`
- `Comment`

Allowed `Current State` values:

- `active`
- `deleted`
- `closed`
- `superseded`

Business role:

- prevents `Task ID` reuse;
- preserves identifier discipline even when rows are removed from the working schedule;
- supports stable bot lookup and dashboard comparison;
- acts as the source for the next generated `Task ID`.

### `dicts`

Controlled dictionaries used by validation and sheet entry.

Minimum pilot dictionaries:

- `Function`
- `Stage`
- `Phase`
- `Item Kind`
- `Item Type`
- `Contour`
- `Work Type`
- `Status`
- `Responsible`
- `Unit`
- `External System`
- `External Object Type`

### `validation`

Non-editable diagnostics surface.

It is used to detect:

- duplicate `Task ID` within one schedule sheet;
- attempted creation of a new row with a `Task ID` already present in `used_task_ids`;
- invalid dictionary values;
- broken predecessor references;
- self-dependencies;
- invalid `wbs` row behavior;
- incomplete external-link triplets;
- invalid planned/actual/forecast combinations;
- schema mismatch between baseline and current sheets.

### `dashboard_portfolio`

Compact executive dashboard surface built on top of:

- `schedule_baseline`
- `schedule_current`
- `schedule_meta`
- `validation`

Business role:

- shows one-page portfolio health at the current `Status Date`;
- compares baseline versus current weighted progress;
- includes compact earned value analysis (`BAC`, `PV`, `EV`, `AC`, `CV`, `SV`, `CPI`, `SPI`, `EAC`, `VAC`);
- summarizes cost, overdue items, and validation health;
- provides compact project-level and phase-level control views;
- surfaces upcoming control dates and a queue of rows still awaiting bot actualization.

Pilot design notes:

- the sheet is intentionally compact and reporting-oriented rather than PMIS-heavy;
- progress is reported mainly through weighted portfolio, project, and phase indicators;
- earned value uses `Planned Cost` from `schedule_baseline` as budget basis and `Actual Cost` from `schedule_current` as pilot actual-cost proxy;
- `Actual Cost` on the dashboard inherits the pilot proxy semantics used in `schedule_current`;
- the dashboard is an extraction and reporting surface, not an editing surface.

### `dashboard_visual`

Presentation-layer dashboard sheet built on top of:

- `dashboard_portfolio`
- `schedule_baseline`
- `schedule_current`

Business role:

- turns compact dashboard tables into management-facing charts;
- highlights portfolio progress and cost-control signals visually;
- keeps the visual layer separate from the calculation layer.

Pilot design notes:

- it uses a small set of high-signal charts instead of many decorative visuals;
- preferred visuals are project-progress comparison, EVA cost comparison by project, and phase cost comparison;
- a true time-phased EVA S-curve is intentionally deferred because the pilot workbook stores current snapshot actuals, not a historical periodized actual-cost ledger.

### `README`

Human-oriented workbook instructions.

It should explain:

- how `Task ID` values are issued;
- which tabs are editable;
- how baseline publication works;
- how dashboards should compare baseline and current values;
- which fields are manual and which are calculated.

## Version Semantics

The pilot workbook uses simplified version semantics.

Required metadata fields:

- `Schedule Purpose`
- `Version Type`
- `Version ID`
- `Status Date`
- `Cost Currency`

The pilot deliberately does not keep separate workbook metadata fields for:

- `Version No`
- `Version Role`
- `Baseline Tag`

Reason:

- in the current pilot, only two operational surfaces are needed: `baseline` and `current`;
- additional version-role layering would add complexity without meaningful pilot benefit.

Recommended `Version ID` examples:

- `BL-2026-03-27`
- `CUR-2026-03-27`

The pilot may keep static `Version ID` values while using a live `Status Date = TODAY()`.

## Task ID Policy

`Task ID` is the single surfaced pilot identifier of a schedule row.

Default format:

- `T10000`
- `T10010`
- `T10020`

Portfolio seed ranges:

- `P01`: `T10000 - T11510`
- `P02`: `T20000 - T21510`
- `P03`: `T30000 - T31510`
- `P04`: `T40000 - T41510`
- `P05`: `T50000 - T51510`
- `P06`: `T60000 - T61510`
- `P07`: `T70000 - T71510`

Rules:

- `Task ID` is immutable after creation;
- `Task ID` identifies one business item and may appear in both baseline and current sheets for that same item;
- `Task ID` is never reused;
- row reorder, WBS regrouping, package regrouping, or rename must not trigger `Task ID` renumbering.

Generation rule:

- within a seeded project block, next `Task ID` = previous project-band suffix + `10`
- after seeded portfolio creation, new projects should reserve their own `Tn0000` block

Validation rule:

- a candidate new `Task ID` must not already exist in the target schedule sheet;
- a candidate new `Task ID` must not already exist in `used_task_ids`.

Implications:

- predecessor links remain stable over time;
- comparison between `schedule_baseline` and `schedule_current` is performed by `Task ID`;
- a deleted row does not release its identifier for future reuse.

Split / merge interpretation in the pilot:

- if an old row is deleted, its `Task ID` remains recorded in `used_task_ids`;
- if one row becomes several new rows, new rows receive new `Task ID` values;
- if a row is merely reinterpreted or renamed, the existing `Task ID` may remain.

The pilot does not introduce a separate lineage-bridge subsystem for split / merge cases.

## Dependency Policy

Dependency entry is one-directional.

Rules:

- users manually maintain `Predecessor Task IDs`;
- `Successor Task IDs` are derived from predecessor references;
- successor lists must not be manually maintained;
- `wbs` rows must not participate in direct dependency chains.

Reason:

- maintaining both directions manually creates avoidable inconsistency;
- one-directional dependency entry is sufficient for pilot governance and dashboard use.

## Timing Policy

The workbook uses one `Status Date` per sheet/version.

Rules:

- `Actual` fields are facts, not forecast fields;
- open-row projection uses `Forecast Start`, `Forecast Finish`, and `Remaining Duration`;
- the pilot uses calendar-day logic rather than a working-day calendar engine.

## External-System Boundary

Heavy extension systems remain external to the pilot workbook.

The workbook stores only lightweight links through:

- `External System`
- `External Object Type`
- `External Ref`

Examples of external systems:

- `PMIS`
- `EDMS`
- `Permit`
- `Payment`
- `BIM`
- `SmartSite`
- `Issue`

The workbook must not introduce standalone internal pilot tabs for:

- PMIS workflow replication;
- EDMS lifecycle replication;
- permit case state machines;
- smart-site event storage;
- resource optimization engines;
- payment / commercial ledgers.

## Relationship to the Business Model

This workbook structure is the pilot control projection of:

- `Schedule`
- `ScheduleVersion`
- `ScheduleItem`
- selected `Dependency` behavior
- selected progress, forecast, and external-link behavior

The broader normative model remains defined in:

- `docs/business/schedule_model.md`
- `docs/business/sheets/schedule_field_rules.md`
