# Schedule Baseline Template

Status: implementation template for the first full baseline project `P01` and its portfolio clones `P02-P07`.

## Purpose

This document defines the first production-grade baseline template used to populate `schedule_baseline`.

The first project is assembled as:

- one full residential high-rise investment-construction project `P01`;
- one reusable business structure;
- one reference schedule that can later be cloned and time-shifted into `P02-P07`.

The accepted portfolio implementation keeps `P01` as the source template and creates `P02-P07` by deterministic date shifts and project-code rewrites.

## Project Structure

Top-level WBS:

- `P01` Project root
- `P01.01` Statutory planning approvals
- `P01.02` Concept and brief
- `P01.03` Surveys, design, expert review
- `P01.04` Tendering and contracting
- `P01.05` Procurement and mobilization
- `P01.06` Structural shell execution
- `P01.07` Parallel fit-out, systems, closeout

## Row-Count Variants

The `P01` template supports two acceptable pilot variants:

- normalized variant:
  - `135` rows in `schedule_baseline`
  - useful for a compact first pass
- extended variant:
  - `152` rows in `schedule_baseline`
  - keeps additional delivery, trade, and commissioning variations

The currently accepted richer implementation variant uses:

- project root: `1`
- `P01.01`: `8` rows total
- `P01.02`: `8` rows total
- `P01.03`: `11` rows total
- `P01.04`: `18` rows total
- `P01.05`: `10` rows total
- `P01.06`: `26` rows total
- `P01.07`: `70` rows total

Total:

- `152` rows in `schedule_baseline`
- rows `2:153`

The richer variant preserves:

- one additional financing/control variation in `P01.04`;
- one additional earthworks logistics row in `P01.06`;
- additional late-phase delivery, door, air-conditioning, finishing, and system-testing rows in `P01.07`.

## Portfolio Clone Layout

Accepted portfolio layout in `schedule_baseline`:

- `P01`: rows `2:153`
- `P02`: rows `154:305`
- `P03`: rows `306:457`
- `P04`: rows `458:609`
- `P05`: rows `610:761`
- `P06`: rows `762:913`
- `P07`: rows `914:1065`

Accepted portfolio phase coverage on `TODAY() = 2026-04-07`:

- `P01` -> `07 Parallel fit-out, systems, closeout`
- `P02` -> `06 Structural shell execution`
- `P03` -> `05 Procurement and mobilization`
- `P04` -> `04 Tendering and contracting`
- `P05` -> `03 Surveys, design, expert review`
- `P06` -> `02 Concept and brief`
- `P07` -> `01 Statutory planning approvals`

Accepted project date shifts relative to `P01`:

- `P01`: `+0 days`
- `P02`: `+204 days`
- `P03`: `+357 days`
- `P04`: `+433 days`
- `P05`: `+569 days`
- `P06`: `+691 days`
- `P07`: `+768 days`

Accepted project windows:

- `P01`: `2024-01-15` to `2026-10-31`
- `P02`: `2024-08-06` to `2027-05-23`
- `P03`: `2025-01-06` to `2027-10-23`
- `P04`: `2025-03-23` to `2028-01-07`
- `P05`: `2025-08-06` to `2028-05-22`
- `P06`: `2025-12-06` to `2028-09-21`
- `P07`: `2026-02-21` to `2028-12-07`

Accepted project-specific `Task ID` bands:

- `P01`: `T10000 - T11510`
- `P02`: `T20000 - T21510`
- `P03`: `T30000 - T31510`
- `P04`: `T40000 - T41510`
- `P05`: `T50000 - T51510`
- `P06`: `T60000 - T61510`
- `P07`: `T70000 - T71510`

## Function-Stage Coverage

`P01` must cover every function in every logically real stage.

| Function | Stages to include | Work Type behavior |
| --- | --- | --- |
| `Project Management & Controls` | `Initial data`, `Technical brief`, `Concept development`, `Design and survey works`, `Tender`, `Control`, `Closeout & Handover` | blank |
| `Investment & Financing` | `Technical brief`, `Concept development`, `Contract`, `Advance payment`, `Control` | blank |
| `Legal & Contract Management` | `Tender`, `Contract`, `Advance payment` | split by selected major packages only at `Contract` |
| `Sales & Marketing` | `Technical brief`, `Concept development`, `Closeout & Handover` | blank |
| `Land & Cadastral Management` | `Initial data`, `State planning approvals` | blank |
| `Permits & Authority Approvals` | `State planning approvals`, `Approvals`, `Closeout & Handover` | blank |
| `Utility Connections Management` | `Initial data`, `State planning approvals`, `Approvals`, `Execution`, `Closeout & Handover` | blank |
| `Engineering Surveys` | `Design and survey works` | blank |
| `Master Planning & Concept Development` | `Technical brief`, `Concept development` | blank |
| `Design Management` | `Technical brief`, `Design and survey works`, `Tender`, `Execution` | blank except selected support rows |
| `Expert Review & Compliance` | `Approvals`, `Execution`, `Closeout & Handover` | blank |
| `Material & Technical Supply` | `Tender`, `Procurement`, `Advance payment`, `Execution` | selected package split at `Tender` and `Procurement`, full split in `Execution` |
| `Construction Execution` | `Contract`, `Execution`, `Control`, `Closeout & Handover` | full split in `Execution` |
| `Commissioning & Handover` | `Execution`, `Control`, `Closeout & Handover` | system-driven rows where relevant |
| `Quality, HSE & Technical Supervision` | `Contract`, `Execution`, `Control`, `Closeout & Handover` | blank |

## Selected Early-Delivery Work Type Split

Only the following major packages are split by `Work Type` in early delivery phases:

- `Concreting`
- `Steel structures`
- `Facade works`
- `Power supply`
- `Final finishing`

This split is used in:

- `Tender`
- `Contract`
- `Procurement`

All other `Work Type` values are fully unfolded only in `Execution`.

## Execution Work Type Library

### Structural shell

- `Earthworks`: excavation `m3`, haulage `t`, backfill `m3`, compaction `m2`
- `Piling`: piles installation `m`, reinforcement `t`, pile concrete `m3`, testing `pcs`
- `Foundation works`: blinding concrete `m3`, reinforcement `t`, formwork `m2`, concrete `m3`, protection `m2`
- `Waterproofing`: primer `m2`, membrane `m2`, protection layer `m2`
- `Concreting`: reinforcement installation `t`, formwork installation `m2`, concrete placement `m3`
- `Steel structures`: steel erection `t`, bolted assemblies `pcs`, fire protection `m2`
- `Roofing`: vapor barrier `m2`, insulation `m2`, membrane `m2`, drainage items `pcs`

### Envelope

- `Building envelope`: masonry works `m3`, envelope wall system installation `m2`
- `Windows`: window units installation `pcs`, window glazing area `m2`, perimeter sealing `m`
- `Facade works`: facade brackets installation `pcs`, facade insulation installation `m2`, facade cladding / glazing installation `m2`
- `Doors`: door sets installation `pcs`, frames and hardware installation `pcs`, door perimeter sealing `m`

### Systems

- `Elevators`: guide rails `m`, elevator equipment `pcs`, commissioning set `set`
- `Power supply`: trays/conduits `m`, cable laying `m`, panels `pcs`, testing `system`
- `Low-current systems`: cable laying `m`, devices `pcs`, cabinets/racks `pcs`, testing `system`
- `Water supply`: piping `m`, fittings/valves `pcs`, fixtures `pcs`, testing `system`
- `Sewerage`: piping `m`, fittings/manholes `pcs`, testing `system`
- `Heating`: piping `m`, terminal units `pcs`, balancing `system`
- `Ventilation`: ducts `m2`, air terminals `pcs`, equipment `pcs`, balancing `system`
- `Air conditioning`: piping `m`, equipment `pcs`, insulation `m`
- `Gas supply`: piping `m`, valves/regulators `pcs`, testing `system`

### Interiors and external works

- `Internal walls and partitions`: masonry/blockwork `m3`, drywall partitions `m2`, plaster preparation `m2`
- `Rough finishing`: plastering `m2`, screed `m2`, suspended ceiling substrate `m2`
- `Final finishing`: painting `m2`, floor finish `m2`, wall tiling `m2`, sanitary accessories `pcs`
- `Landscaping`: paving `m2`, curbs `m`, topsoil `m3`, planting `pcs`

## Naming Conventions

### `Task Name`

Use:

- `{Verb} {object} {scope}`

Examples:

- `Obtain statutory planning approval package`
- `Issue concreting tender package`
- `Install facade brackets`
- `Complete ventilation balancing`
- `Gate: design documentation approved`

### `WBS Path`

Use numeric hierarchical paths only:

- `P01`
- `P01.01`
- `P01.01.01`
- `P01.04.07`
- `P01.07.33`

Do not encode trade or package mnemonics into `WBS Path`.

### `Package`

Use compact package codes:

- `P01-GEN`
- `P01-CONC`
- `P01-STEEL`
- `P01-FACADE`
- `P01-POWER`
- `P01-FFIN`
- `P01-MEP`
- `P01-HANDOVER`

### `Location/System`

Use broad template buckets:

- `P01-PROJECT`
- `P01-SITE`
- `P01-STRUCTURE`
- `P01-ENVELOPE`
- `P01-MEP`
- `P01-INTERIORS`
- `P01-EXTERNAL`
- `P01-HANDOVER`

## Baseline Defaults

For actionable non-`wbs` baseline rows:

- `Forecast Start = Planned Start`
- `Forecast Finish = Planned Finish`
- `Remaining Duration = Planned Duration`
- `Percent Complete` may be populated as planned state as of sheet `Status Date`
- `Status` is derived from `Percent Complete`
- `Actual Start`, `Actual Finish`, `Actual Duration`, `Actual Quantity`, `Actual Cost` remain blank
- `Phase` is selected manually from the 7-phase dictionary

For structural `wbs` rows:

- no `Percent Complete`
- no `Status`
- no `Planned Cost`
- no actual fields
- no dependency fields
- project-root rows keep `Phase` blank

## Quantitative Enrichment Basis

When the baseline is enriched with quantities and planned cost, use:

- residential high-rise basis
- `2 residential sections`
- about `48,000 m2 GFA`
- `Global USD 2026`
- `hybrid split` cost attribution

For `Planned Cost`:

- use `docs/business/dictionaries/planned_cost_reference.md`
- keep `wbs` rows blank
- use `0` for pure gates and pure internal control rows without direct spend
