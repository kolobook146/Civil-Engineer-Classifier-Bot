# Schedule Field Rules

Status: normative pilot field-rule catalog for the control schedule workbook.

## Purpose

This document defines the detailed rules for every field used in the pilot schedule workbook.
It is the normative source of truth for:

- field meaning;
- field data type;
- allowed values;
- entry mode;
- calculation logic;
- validation behavior;
- protection logic.

It complements:

- `docs/business/sheets/schedule_workbook.md`
- `docs/business/sheets/schedule_sheet.md`

## Calculation Basis

The pilot uses the following common rules:

- time basis = `calendar days`
- `Status Date` is one reporting date per schedule sheet version
- `schedule_baseline` may store planned progress state as of `Status Date`
- `Actual` fields store facts, not forecasts
- open-row projection lives in:
  - `Forecast Start`
  - `Forecast Finish`
  - `Remaining Duration`

For `schedule_current`, the pilot uses a hybrid actual surface:

- a one-time historical backfill was accepted as of `2026-04-08`;
- no `TODAY()`-driven actual formulas are used in `schedule_current`;
- rows with `Planned Finish < 2026-04-08` may be manually closed with `Actual = Planned`;
- open quantity-driven rows may consume quantity through a simple formula from `data_facts`;
- open non-quantity `Actual Start`, `Actual Finish`, and `Percent Complete` remain bot-maintained.

### Quantity-driven row

A row is treated as quantity-driven when all of the following are true:

- `Item Kind != wbs`
- `Planned Quantity` is filled
- `Unit` is filled
- `Planned Intensity` is filled and greater than zero

### Zero-day row

The following rows are zero-day by default:

- `milestone`
- `gate`
- same-day `event`

`wbs` is a structural row type and is excluded from operational duration logic.

## Workbook Metadata Fields

| Field | Sheet | Type | Allowed values / source | Required | Entry mode | Rule |
| --- | --- | --- | --- | --- | --- | --- |
| `Sheet Name` | `schedule_meta` | enum text | `schedule_baseline`, `schedule_current` | Yes | Manual | One row per schedule surface. |
| `Schedule ID` | `schedule_meta` | text | Stable project schedule identifier | Yes | Manual | One workbook-wide identifier for the schedule container. |
| `Schedule Purpose` | `schedule_meta` | enum text | `control` | Yes | Manual once | Fixed pilot purpose. |
| `Version Type` | `schedule_meta` | enum text | `baseline`, `current` | Yes | Manual | Distinguishes the two pilot surfaces. |
| `Version ID` | `schedule_meta` | text | Recommended: `BL-YYYY-MM-DD`, `CUR-YYYY-MM-DD` | Yes | Manual | Human-readable version identifier. |
| `Status Date` | `schedule_meta` | date | `=TODAY()` in workbook implementation | Yes | Formula | Single live data date for the whole sheet/version. |
| `Cost Currency` | `schedule_meta` | text | ISO 4217 uppercase code | Conditional | Manual | Required if cost fields are used in the workbook. |

## Used Task IDs Fields

| Field | Sheet | Type | Allowed values / source | Required | Entry mode | Rule |
| --- | --- | --- | --- | --- | --- | --- |
| `Task ID` | `used_task_ids` | text | `T` + numeric suffix | Yes | Generated | Immutable identifier register. |
| `Created In Version ID` | `used_task_ids` | text | Existing `Version ID` | Yes | Manual or generated | Stores the version where the ID first appeared. |
| `Created At` | `used_task_ids` | date or datetime | ISO date / datetime | Yes | Manual or generated | Creation timestamp of the identifier. |
| `Current State` | `used_task_ids` | enum text | `active`, `deleted`, `closed`, `superseded` | Yes | Manual | Tracks whether the identifier is still active. |
| `Comment` | `used_task_ids` | text | Free text | No | Manual | Optional explanation. |

### Task ID Creation Policy

Default pilot format:

- `T10000`
- `T10010`
- `T10020`

Portfolio-seeded project bands:

- `P01`: `T10000 - T11510`
- `P02`: `T20000 - T21510`
- `P03`: `T30000 - T31510`
- `P04`: `T40000 - T41510`
- `P05`: `T50000 - T51510`
- `P06`: `T60000 - T61510`
- `P07`: `T70000 - T71510`

Generation rule:

- within a seeded project block, next ID = previous project-band suffix + `10`
- after the seeded portfolio is in place, new projects should reserve their own `Tn0000` band rather than interleave a global sequence

Validation rules:

- a candidate new `Task ID` must not already exist in the target sheet;
- a candidate new `Task ID` must not already exist in `used_task_ids`;
- the same `Task ID` may appear in both `schedule_baseline` and `schedule_current` only when they represent the same business item across versions.

## Schedule Row Fields

### Identity and Classification

| Field | Type | Allowed values / source | Required | Entry mode | Rule / Formula |
| --- | --- | --- | --- | --- | --- |
| `Task ID` | text | `T` + numeric suffix | Yes | Generated then protected | Immutable identifier of the row. |
| `Task Name` | text | Free text | Yes | Manual | Human-readable row name. |
| `Item Kind` | enum text | `item_kinds.txt` | Yes | Manual | One of `wbs`, `activity`, `milestone`, `gate`, `event`. |
| `Item Type` | text | `item_types.txt` or blank | Conditional | Manual | Required for `Item Kind = event`; optional and usually blank otherwise. |
| `Contour` | enum text | `contours.txt` | Conditional | Manual | Required for actionable rows; may remain blank on structural `wbs` rows. |
| `Function` | controlled text | `functions.txt` | Conditional | Manual | Required for actionable rows; may remain blank on structural `wbs` rows. |
| `Stage` | controlled text | `stages.txt` | Conditional | Manual | Required for actionable rows; may remain blank on structural `wbs` rows. |
| `Work Type` | controlled text | `work_types.txt` or blank | No | Manual | Optional physical-scope refinement. |
| `Phase` | controlled text | `phases.txt` or blank | No | Manual | Portfolio phase chosen from the 7-phase dictionary. Project root rows may keep it blank. |
| `WBS Path` | text | Dot-separated structural path | Yes | Manual | Minimum hierarchy reference for every row. |
| `Package` | text | Stable coded label | No | Manual | Package / tender / contract / handover grouping. |
| `Location/System` | text | Stable coded label | No | Manual | Physical area, building part, or system context. |
| `Responsible` | controlled text | `responsibles.txt` | Conditional | Manual | Responsibility bucket, not a person name. Required for actionable rows. |

### Dependency Fields

| Field | Type | Allowed values / source | Required | Entry mode | Rule / Formula |
| --- | --- | --- | --- | --- | --- |
| `Predecessor Task IDs` | comma-separated text list | Existing same-sheet `Task ID` values | No | Manual | Explicit predecessor references. |
| `Successor Task IDs` | comma-separated text list | Existing same-sheet `Task ID` values | No | Calculated | Reverse lookup of rows whose `Predecessor Task IDs` contains current `Task ID`. |

Dependency rules:

- `wbs` rows must not participate in dependency chains;
- self-dependency is invalid;
- unresolved predecessor reference is invalid.

### Timing Fields

| Field | Type | Allowed values / source | Required | Entry mode | Rule / Formula |
| --- | --- | --- | --- | --- | --- |
| `Planned Start` | date | `YYYY-MM-DD` | Conditional | Manual | Planned start date. |
| `Planned Finish` | date | `YYYY-MM-DD` | Conditional | Manual or calculated | Manual for date-driven rows; calculated for quantity-driven and zero-day rows. |
| `Planned Duration` | non-negative integer | Calendar days | Conditional | Calculated | `0` for `milestone`, `gate`, same-day `event`; quantity-driven: `MAX(1, ROUNDUP(Planned Quantity / Planned Intensity, 0))`; otherwise `Planned Finish - Planned Start + 1`. |
| `Forecast Start` | date | `YYYY-MM-DD` | Conditional | Calculated | If `Actual Start` filled -> `Actual Start`; else if no predecessors -> `Planned Start`; else latest predecessor finish with offset rule. |
| `Forecast Finish` | date | `YYYY-MM-DD` | Conditional | Manual or calculated | `Actual Finish` if `done`; `Forecast Start` for open zero-day rows; quantity-driven: `Forecast Start + Remaining Duration - 1`; non-quantity-driven open rows: manual. |
| `Remaining Duration` | non-negative integer | Calendar days | Conditional | Calculated | `0` if `done`; `0` for open zero-day rows; quantity-driven: `MAX(0, ROUNDUP((Planned Quantity - Actual Quantity) / Planned Intensity, 0))`; otherwise derived from manual `Forecast Finish`. |
| `Actual Start` | date | `YYYY-MM-DD` | Conditional | Manual | `schedule_current`: historical rows closed by the `2026-04-08` pilot backfill may use `Planned Start`; open rows remain bot-maintained. |
| `Actual Finish` | date | `YYYY-MM-DD` | Conditional | Manual | `schedule_current`: historical rows closed by the `2026-04-08` pilot backfill may use `Planned Finish`; open rows remain bot-maintained. |
| `Actual Duration` | non-negative integer | Calendar days | No | Calculated | Blank if not `done`; `0` for completed zero-day row; otherwise `Actual Finish - Actual Start + 1`. |

#### Predecessor Offset Rule

When calculating `Forecast Start` from predecessors:

- if predecessor is completed, use predecessor `Actual Finish`;
- otherwise use predecessor `Forecast Finish`;
- if predecessor is zero-day, successor may start on the same day;
- otherwise successor starts the next day;
- if multiple predecessors exist, use the latest applicable predecessor finish.

#### Non-quantity-driven Remaining Duration

For open non-quantity-driven rows:

- `Remaining Duration = MAX(0, Forecast Finish - Status Date + 1)`

### Status, Progress, Quantity, and Cost

| Field | Type | Allowed values / source | Required | Entry mode | Rule / Formula |
| --- | --- | --- | --- | --- | --- |
| `Status` | enum text | `statuses.txt` | Conditional | Manual or calculated | `schedule_baseline`: derived from `Percent Complete`. `schedule_current`: derived from `Percent Complete` when it is filled, otherwise blank. Blank on `wbs` rows. |
| `Percent Complete` | decimal 0-100 | Numeric percent | No | Manual or calculated | `schedule_baseline`: calculated from `Status Date`. `schedule_current`: historical rows closed by the `2026-04-08` backfill use static `100`; open quantity-driven rows use `MIN(100, ROUND(Actual Quantity / Planned Quantity * 100, 1))`; open non-quantity rows remain bot-maintained. Blank on `wbs` rows. |
| `Planned Quantity` | non-negative decimal | Numeric | No | Manual | Required for quantity-driven rows. |
| `Actual Quantity` | non-negative decimal | Numeric | No | Manual or calculated | `schedule_current`: historical quantity-driven rows closed by the `2026-04-08` backfill use `Planned Quantity`; open quantity-driven rows use `SUMIFS(data_facts.volume; data_facts.stage; Stage; data_facts.function; Function; data_facts.work_type; Work Type; data_facts.unit; Unit)`. Non-quantity rows stay blank. |
| `Unit` | controlled text | `units.txt` | Conditional | Manual | Required when quantity fields are used. |
| `Planned Intensity` | positive decimal | `Unit/day` | Conditional | Manual or calculated | In baseline enrichment it may be derived as `Planned Quantity / Planned Duration`; otherwise it is maintained explicitly for quantity-driven rows. |
| `Planned Cost` | non-negative decimal | Workbook currency | No | Manual | Planned cost in `Cost Currency`, assigned using `docs/business/dictionaries/planned_cost_reference.md`. Blank on `wbs` rows in the pilot. |
| `Actual Cost` | non-negative decimal | Workbook currency | No | Manual or calculated | `schedule_current`: quantity-driven rows use `ROUND(Actual Quantity / Planned Quantity * Planned Cost, 2)`; historical non-quantity rows closed by the `2026-04-08` backfill may use `Planned Cost`; open non-quantity rows may stay blank until bot enrichment. |

#### Baseline Planned Statusing

In `schedule_baseline`, actionable non-`wbs` rows may be populated as planned state as of the sheet `Status Date`.

For non-zero-day rows:

- if `Status Date < Planned Start`, then `Percent Complete = 0`
- if `Planned Start <= Status Date < Planned Finish`, then:
  - `Percent Complete = ROUND(((Status Date - Planned Start + 1) / Planned Duration) * 100, 1)`
- if `Status Date >= Planned Finish`, then `Percent Complete = 100`

For zero-day rows:

- before the planned date, `Percent Complete = 0`
- on and after the planned date, `Percent Complete = 100`

Baseline `Status` is derived only from `Percent Complete`:

- `0` -> `not_started`
- `>0 and <100` -> `in_progress`
- `100` -> `done`

In the pilot, `wbs` rows stay blank for:

- `Status`
- `Percent Complete`

#### Current Pilot Actual Logic

For `schedule_current`, the accepted pilot logic is:

- no `TODAY()`-based actual formulas;
- a one-time manual historical backfill is applied as of `2026-04-08`;
- for every non-`wbs` row with `Planned Finish < 2026-04-08`:
  - `Status = done`
  - `Percent Complete = 100`
  - `Actual Start = Planned Start`
  - `Actual Finish = Planned Finish`
  - `Forecast Start = Planned Start`
  - `Forecast Finish = Planned Finish`
  - `Remaining Duration = 0`
- for historical quantity-driven rows:
  - `Actual Quantity = Planned Quantity`
  - `Actual Cost` may stay on the standard quantity-driven formula and therefore resolve to `Planned Cost`
- for historical non-quantity rows:
  - `Actual Quantity` stays blank
  - `Actual Cost = Planned Cost`

For open quantity-driven rows in `schedule_current`:

- `Actual Quantity` is aggregated directly from `data_facts` by:
  - `Stage`
  - `Function`
  - `Work Type`
  - `Unit`
- `Task ID` and `External Ref` are not used in this formula branch;
- if several schedule rows share the same four-field coordinate, the same summed fact quantity may appear in all of them;
- this is an accepted pilot limitation, not the target mature-state matching logic.

For open non-quantity rows in `schedule_current`:

- `Actual Start` remains bot-maintained;
- `Actual Finish` remains bot-maintained;
- `Percent Complete` remains bot-maintained.

Derived `Status` in `schedule_current` follows:

- blank if `Percent Complete` is blank
- `0` -> `not_started`
- `>0 and <100` -> `in_progress`
- `100` -> `done`

#### Baseline Quantity and Cost Enrichment

When `schedule_baseline` is enriched for planning analytics:

- `Planned Quantity` is populated only for measurable rows;
- `Planned Intensity` may be derived as `Planned Quantity / Planned Duration`;
- `Planned Cost` follows the reference logic in `docs/business/dictionaries/planned_cost_reference.md`;
- `Actual Start`, `Actual Finish`, `Actual Duration`, `Actual Quantity`, and `Actual Cost` remain blank.

#### Portfolio Phase Usage

In the current pilot portfolio baseline:

- `Phase` is entered manually from the dictionary-backed dropdown;
- project root rows keep `Phase` blank;
- all phase-root and child rows inside `.01` carry `01 Statutory planning approvals`;
- all rows inside `.02` carry `02 Concept and brief`;
- all rows inside `.03` carry `03 Surveys, design, expert review`;
- all rows inside `.04` carry `04 Tendering and contracting`;
- all rows inside `.05` carry `05 Procurement and mobilization`;
- all rows inside `.06` carry `06 Structural shell execution`;
- all rows inside `.07` carry `07 Parallel fit-out, systems, closeout`.

### External Links and Comment

| Field | Type | Allowed values / source | Required | Entry mode | Rule / Formula |
| --- | --- | --- | --- | --- | --- |
| `External System` | controlled text | `external_systems.txt` | Conditional | Manual | Part of required triplet when any external link is used. |
| `External Object Type` | controlled text | `external_object_types.txt` | Conditional | Manual | Part of required triplet when any external link is used. |
| `External Ref` | text | External object identifier | Conditional | Manual | Part of required triplet when any external link is used. |
| `Comment` | text | Free text | No | Manual | Human clarification only; not a replacement for structured fields. |

## Calculation Precedence

When multiple timing interpretations are possible, use this precedence:

1. `Actual` facts override all forecast logic for completed rows.
2. Zero-day logic overrides duration logic.
3. Quantity-driven logic overrides date-derived duration logic when the required fields are present.
4. Non-quantity-driven open rows use manual `Forecast Finish`.
5. `wbs` rows remain structural and are excluded from operational calculations.

## Validation Matrix

### Errors

- duplicate `Task ID` inside one schedule sheet
- reuse of previously issued `Task ID` as a new identifier
- invalid dictionary value in any controlled field
- unresolved predecessor reference
- self-dependency
- `wbs` row with direct dependency logic
- partial external-link triplet
- `schedule_current`: `done` without `Actual Start`
- `schedule_current`: `done` without `Actual Finish`
- `Actual Finish` present on a non-completed row
- `Item Type` empty when required by `Item Kind = event`
- missing `Unit` where quantity is used

Baseline-specific note:

- `schedule_baseline` may legitimately contain rows with `Status = done` and blank `Actual*` fields, because baseline statusing is planned-as-of-date rather than factual execution.

### Warnings

- `Actual Quantity > Planned Quantity`
- `Actual Cost > Planned Cost`
- open row without valid forecast logic
- physical-scope row without `Responsible`
- physical-scope row without `Package` or `Location/System`

## Editability and Protection Matrix

### Editable by user

- `Task Name`
- `Item Kind`
- `Item Type`
- `Contour`
- `Function`
- `Stage`
- `Work Type`
- `WBS Path`
- `Package`
- `Location/System`
- `Responsible`
- `Predecessor Task IDs`
- `Planned Start`
- `Planned Finish` for date-driven rows
- `Actual Start`
- `Actual Finish`
- `Status`
- `Percent Complete` for non-quantity-driven rows
- `Planned Quantity`
- `Actual Quantity`
- `Unit`
- `Planned Intensity`
- `Planned Cost`
- `Actual Cost`
- `External System`
- `External Object Type`
- `External Ref`
- `Comment`

### Calculated by sheet

- `Task ID` next-value generation support
- `Successor Task IDs`
- `Planned Duration`
- `Planned Finish` for quantity-driven rows
- `Forecast Start`
- `Forecast Finish` for quantity-driven and completed rows
- `Remaining Duration`
- `Actual Duration`
- `Percent Complete` for quantity-driven rows

### Protected after publication

- all fields in `schedule_baseline`
- calculated fields in `schedule_current`
- `schedule_meta` values that define the published baseline version

## Relationship to Other Documents

This field-rule catalog is the detailed implementation-oriented companion to:

- `docs/business/schedule_model.md`
- `docs/business/sheets/schedule_workbook.md`
- `docs/business/sheets/schedule_sheet.md`
- `docs/business/dictionaries/planned_cost_reference.md`
