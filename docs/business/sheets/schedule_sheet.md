# Schedule Sheet Specification

Status: normative pilot row schema for `schedule_baseline` and `schedule_current`.

## Sheet Purpose

This document defines the row-level schema used by the two pilot schedule sheets:

- `schedule_baseline`
- `schedule_current`

Each row represents one governed schedule item inside one sheet version.

The workbook-level structure is defined in:

- `docs/business/sheets/schedule_workbook.md`

Detailed field behavior is defined in:

- `docs/business/sheets/schedule_field_rules.md`

## Target Column Order

| # | Column | Requiredness | Entry mode | Business meaning |
| --- | --- | --- | --- | --- |
| 1 | `Task ID` | Yes | Generated then protected | Immutable business identifier of the row. |
| 2 | `Task Name` | Yes | Manual | Human-readable item name. |
| 3 | `Item Kind` | Yes | Manual | Primary row kind: `wbs`, `activity`, `milestone`, `gate`, or `event`. |
| 4 | `Item Type` | Conditional | Manual | Optional subtype field; required for `event` rows. |
| 5 | `Contour` | Conditional | Manual | `production`, `delivery`, or `cross-project`. |
| 6 | `Function` | Conditional | Manual | Pilot workstream coordinate from the controlled dictionary. |
| 7 | `Stage` | Conditional | Manual | Pilot lifecycle coordinate from the controlled dictionary. |
| 8 | `Work Type` | No | Manual | Physical work-scope or physical-scope support refinement where relevant. |
| 9 | `Phase` | No | Manual | Portfolio-phase coordinate selected from the controlled 7-phase dictionary; project root rows may keep it blank. |
| 10 | `WBS Path` | Yes | Manual | Minimum hierarchy path for roll-up and grouping. |
| 11 | `Package` | No | Manual | Package, tender, contract, procurement, work, or handover grouping where relevant. |
| 12 | `Location/System` | No | Manual | Physical area, zone, building part, or system context where relevant. |
| 13 | `Responsible` | Conditional | Manual | Controlled responsibility bucket. |
| 14 | `Predecessor Task IDs` | No | Manual | Upstream dependency references entered as comma-separated `Task ID` values. |
| 15 | `Successor Task IDs` | No | Calculated | Derived downstream dependency references. |
| 16 | `Planned Start` | Conditional | Manual | Planned start date. |
| 17 | `Planned Finish` | Conditional | Manual or calculated | Planned finish date. |
| 18 | `Planned Duration` | Conditional | Calculated | Planned total duration in calendar days. |
| 19 | `Forecast Start` | Conditional | Calculated | Start used for open-row projection. |
| 20 | `Forecast Finish` | Conditional | Manual or calculated | Current projected finish for open rows. |
| 21 | `Remaining Duration` | Conditional | Calculated | Remaining calendar days to completion. |
| 22 | `Actual Start` | Conditional | Manual | Actual start fact. |
| 23 | `Actual Finish` | Conditional | Manual | Actual finish fact. |
| 24 | `Actual Duration` | No | Calculated | Final actual duration for completed rows only. |
| 25 | `Status` | Conditional | Manual or calculated | Current business status. In `schedule_baseline` it may be derived from planned `% complete`; `wbs` rows remain blank in the pilot. |
| 26 | `Percent Complete` | No | Manual or calculated | Operational progress indicator from 0 to 100. In `schedule_baseline` it may represent planned progress as of `Status Date`; `wbs` rows remain blank in the pilot. |
| 27 | `Planned Quantity` | No | Manual | Planned quantified scope where applicable. |
| 28 | `Actual Quantity` | No | Manual | Actual completed or installed quantity. |
| 29 | `Unit` | Conditional | Manual | Canonical measurement unit. |
| 30 | `Planned Intensity` | Conditional | Manual or calculated | Planned output rate in `Unit/day` for quantity-driven rows. In baseline enrichment it may be derived from quantity and duration. |
| 31 | `Planned Cost` | No | Manual | Planned cost assigned using the normative planned-cost reference. |
| 32 | `Actual Cost` | No | Manual | Actual cost reflected in the current control view. |
| 33 | `External System` | Conditional | Manual | Linked external system such as `PMIS`, `EDMS`, `Permit`, `Payment`, `BIM`, or `SmartSite`. |
| 34 | `External Object Type` | Conditional | Manual | External object class such as `Case`, `Document`, `Invoice`, `Package`, `Issue`, or `Record`. |
| 35 | `External Ref` | Conditional | Manual | External object identifier. |
| 36 | `Comment` | No | Manual | Free text for human clarification only. |

## Core Row Rules

- `Task ID` is the single surfaced pilot identifier and must remain stable after creation.
- The same `Task ID` may appear in both `schedule_baseline` and `schedule_current` when they represent the same business item.
- `Task ID` must not be reused after deletion or closure.
- `Item Type` is required for `event` rows and optional elsewhere.
- `Phase` is a controlled manual portfolio coordinate and does not replace `Stage`.
- `WBS Path` is the minimum mandatory hierarchy field for every row.
- `Successor Task IDs` must be derived from predecessor links and protected from manual editing.
- `wbs` rows are structural summary rows and must not participate in direct dependency chains or operational actual logic.

## Business Conventions

- Date format must be `YYYY-MM-DD`.
- Time basis is `calendar days`.
- `Status Date` is stored once per sheet/version in `schedule_meta` and is implemented as `=TODAY()` in the current workbook.
- In `schedule_baseline`, non-`wbs` rows may store planned progress and derived status as of the sheet `Status Date`.
- Dependency fields use comma-separated `Task ID` values.
- `Work Type` may be filled for direct execution rows and for delivery or support rows tied to a physical work scope.
- `Actual` fields are factual only.
- `wbs` rows remain blank for `Status` and `Percent Complete` in the pilot.
- Open-row projection uses `Forecast Start`, `Forecast Finish`, and `Remaining Duration`.
- `Planned Intensity` is measured in `Unit/day`.
- `Planned Cost` assignment follows `docs/business/dictionaries/planned_cost_reference.md`.
- If one external-link field is filled, all three external-link fields must be filled.

## Relationship to the Schedule Model

The row schema is the pilot control-sheet projection of:

- `ScheduleItem`
- explicit dependency references
- selected timing, quantity, cost, progress, and external-link fields

The broader normative business model remains defined in:

- `docs/business/schedule_model.md`
- `docs/business/sheets/schedule_workbook.md`
- `docs/business/sheets/schedule_field_rules.md`
