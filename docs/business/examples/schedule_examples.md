# Schedule Examples

Status: normative pilot examples for the control schedule workbook.

## Purpose

These examples show how the current pilot schedule model appears in:

- `schedule_baseline`
- `schedule_current`

Only the most relevant columns are shown.

Assumed `schedule_baseline` `Status Date` in the examples:

- `=TODAY()`
- example snapshot shown below assumes `TODAY() = 2026-04-08`

## Example Set

| Sheet | Task ID | Task Name | Item Kind | Item Type | Contour | Function | Stage | Work Type | Phase | WBS Path | Package | Location/System | Responsible | Planned Start | Planned Finish | Planned Duration | Forecast Start | Forecast Finish | Remaining Duration | Actual Start | Actual Finish | Status | Percent Complete | Planned Quantity | Actual Quantity | Unit | Planned Intensity | Planned Cost | Actual Cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `schedule_baseline` | `T10000` | `P01 Residential High-Rise Project` | `wbs` |  |  |  |  |  |  | `P01` | `P01-GEN` | `P01-PROJECT` |  | `2024-01-15` | `2026-10-31` | `1021` |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `schedule_baseline` | `T10240` | `Secure building permit` | `event` | `permit` | `delivery` | `Permits & Authority Approvals` | `Approvals` |  | `03 Surveys, design, expert review` | `P01.03.07` | `P01-GEN` | `P01-PROJECT` | `Authority Interface` | `2024-12-10` | `2024-12-10` | `0` | `2024-12-10` | `2024-12-10` | `0` |  |  | `done` | `100` |  |  |  |  | `45000` |  |
| `schedule_baseline` | `T10470` | `Procure concreting package` | `activity` |  | `delivery` | `Material & Technical Supply` | `Procurement` | `Concreting` | `05 Procurement and mobilization` | `P01.05.01` | `P01-CONC` | `P01-PROJECT` | `Supply Chain & Logistics` | `2025-03-16` | `2025-04-20` | `36` | `2025-03-16` | `2025-04-20` | `36` |  |  | `done` | `100` |  |  |  |  | `1850000` |  |
| `schedule_baseline` | `T10960` | `Install facade insulation` | `activity` |  | `production` | `Construction Execution` | `Execution` | `Facade works` | `07 Parallel fit-out, systems, closeout` | `P01.07.14` | `P01-FACADE` | `P01-ENVELOPE` | `Facade Subcontractor` | `2026-03-10` | `2026-05-15` | `67` | `2026-03-10` | `2026-05-15` | `67` |  |  | `in_progress` | `43.3` | `9800` |  | `m2` | `146.3` | `294000` |  |
| `schedule_baseline` | `T20960` | `Install facade insulation` | `activity` |  | `production` | `Construction Execution` | `Execution` | `Facade works` | `07 Parallel fit-out, systems, closeout` | `P02.07.14` | `P02-FACADE` | `P02-ENVELOPE` | `Facade Subcontractor` | `2026-09-30` | `2026-12-05` | `67` | `2026-09-30` | `2026-12-05` | `67` |  |  | `not_started` | `0` | `9800` |  | `m2` | `146.3` | `294000` |  |
| `schedule_current` | `T10750` | `Place structural concrete` | `activity` |  | `production` | `Construction Execution` | `Execution` | `Concreting` | `06 Structural shell execution` | `P01.06.19` | `P01-CONC` | `P01-STRUCTURE` | `Structural Works Management` | `2025-10-29` | `2026-01-31` | `95` | `2025-10-29` | `2026-01-31` | `0` | `2025-10-29` | `2026-01-31` | `done` | `100` | `24500` | `24500` | `m3` | `257.9` | `3552500` | `3552500` |
| `schedule_current` | `T10960` | `Install facade insulation` | `activity` |  | `production` | `Construction Execution` | `Execution` | `Facade works` | `07 Parallel fit-out, systems, closeout` | `P01.07.14` | `P01-FACADE` | `P01-ENVELOPE` | `Facade Subcontractor` | `2026-03-10` | `2026-05-15` | `67` | `2026-03-10` | `2026-05-15` | `67` |  |  | `not_started` | `0` | `13200` | `0` from formula-fed `SUMIFS` when no matching facts exist yet | `m2` | `197.0` | `396000` | `0` from `ROUND(Actual Quantity / Planned Quantity * Planned Cost, 2)` |

## Reading Notes

- The same `Task ID` may appear in both sheets when the business item is compared across baseline and current control views.
- `Task ID` follows project-banded pilot ranges such as `T1xxxx`, `T2xxxx`, and `T7xxxx`, and remains immutable.
- `Item Type` is used to subtype `event` rows and may remain empty for most non-event rows.
- `Phase` is a manual portfolio coordinate and does not replace `Stage`.
- `wbs` is a structural row kind used in the flattened sheet projection.
- In `schedule_baseline`, `Percent Complete` may represent planned statusing as of the sheet `Status Date`.
- In `schedule_baseline`, `Status` may be derived from `Percent Complete`.
- `wbs` rows stay blank for `Status` and `Percent Complete` in the pilot.
- `Forecast Start`, `Forecast Finish`, and `Remaining Duration` represent open-row control logic.
- `Actual Start`, `Actual Finish`, and `Actual Duration` remain factual.
- In `schedule_current`, a one-time historical backfill is accepted as of `2026-04-08`.
- In `schedule_current`, open quantity-driven `Actual Quantity` may be fed by a direct `SUMIFS` bridge from `data_facts`.
- In that pilot bridge, the same fact sum may appear in multiple rows when `Stage + Function + Work Type + Unit` is identical.
- In `schedule_current`, quantity-driven `Actual Cost` may use the proportional pilot formula `ROUND(Actual Quantity / Planned Quantity * Planned Cost, 2)`.
- In `schedule_current`, open non-quantity `Actual Start`, `Actual Finish`, and `Percent Complete` remain bot-maintained.
- `Responsible` uses a controlled responsibility bucket rather than a person name.
- `Planned Intensity` may be derived as `Planned Quantity / Planned Duration` during baseline enrichment.
- `Planned Cost` follows `docs/business/dictionaries/planned_cost_reference.md`.
- The first production-grade baseline is assembled as a fully detailed `P01` template before later cloning into `P02-P07`.
- In the implemented portfolio baseline, `Status Date` is live through `=TODAY()`.
