# Fact-to-Schedule Mapping

Status: normative Stage 22 mapping model.

## Purpose

This document defines how the confirmed fact register may connect to the schedule model without destroying schedule lineage or evidence integrity.

## Core Principle

Facts and schedule items are related but not identical.

- `data_facts` stores confirmed operational evidence.
- `schedule` stores governed planning and control structure.

Mapping is therefore:

- deliberate;
- traceable;
- safe-by-default.

## Current Pilot Position

At the Stage 22 pilot stage:

- facts are persisted to `data_facts`;
- the schedule is maintained as a separate model;
- there is still no exact row-level automatic mutation from a new fact;
- however, selected rows in `schedule_current` may consume aggregated quantity through a formula branch.

This remains intentional.
The project first needs reliable evidence and reliable schedule structure before introducing exact row-level automation.

## Shared Business Coordinates

The minimum shared business coordinate between a fact and a schedule item is:

- `function`
- `stage`

Additional context that may improve matching:

- `work_type`
- time window
- responsible party
- package
- location/system
- explicit `Task ID` hint in the source text

## Preferred Matching Order

Stage 22 adopts the following matching precedence:

1. explicit `Task ID` hint
2. explicit `External Ref` or another external object reference
3. `function + stage + work_type + date window`
4. hierarchy and code context such as `WBS Path`, `Package`, `Location/System`, and `Responsible`
5. review queue if no safe match exists

This order is intentionally conservative.

## Formula-Fed Pilot Branch

The implemented pilot accepts one intentionally weaker bridge for assigned open rows in `schedule_current`.

That branch does not try to prove an exact row-level match from the fact itself.
Instead it first chooses one project clone per template row through `fact_collection_map`, then aggregates `Actual Quantity` from `data_facts` by the shared operational coordinate:

- `stage`
- `function`
- `work_type`
- `unit`

This means:

- `Task ID` is not used in that formula branch;
- `External Ref` is not used in that formula branch;
- time-window logic is not used in that formula branch;
- only the assigned project clone is allowed to collect the summed fact quantity for a given template row;
- rows with `Planned Finish < 2026-04-08` keep historical fixed semantics instead of live formula collection;
- non-physical rows may also use the branch when the bot writes `volume = 1`.

This is an accepted pilot limitation.
It is suitable for the current pilot because it is simple, transparent, and reversible, but it is not a strong mature-state matching model.

## Formula-Fed Fact Verification

The workbook also calculates a lightweight `data_facts.verification` signal.

Verification uses the same four-field pilot coordinate as the formula-fed quantity
branch:

- `stage`
- `function`
- `work_type`
- `unit`

A fact is `verified` only when:

- the four-field key exists in an eligible formula-fed `schedule_current` row;
- cumulative `data_facts.volume` for that key is less than or equal to the available
  schedule capacity.

Available capacity is calculated from the eligible current-schedule rows:

- physical quantity rows contribute their `Planned Quantity`;
- non-physical rows without planned quantity contribute `1`, matching the bot convention
  that `volume = 1` is a binary completion marker.

A fact is `not verified` when no eligible schedule row exists or when cumulative volume
for the same key exceeds capacity. This is a review signal, not a rejection of the
original evidence.

## Mapping Outcomes

| Outcome | Meaning | Typical result |
| --- | --- | --- |
| `Linked progress` | The fact safely supports progress on an existing schedule item. | Used to inform a `ProgressRecord` or the current schedule view. |
| `Linked governance` | The fact safely supports an approval, issue, payment, KPI, completion, or similar control event. | Used to inform a `GovernanceRecord`. |
| `Linked evidence only` | The fact can be linked to a schedule item for traceability but not yet change business state. | Retained as evidence and context. |
| `Suggested gap` | The fact indicates a likely missing schedule item. | Triggers review and schedule-maintenance action. |
| `Informational only` | The fact is useful but not safely linkable to one schedule item. | Kept in the fact register without schedule mutation. |
| `Review queue` | The fact is too ambiguous for safe automated or assisted mapping. | Held for human decision. |

## Mapping by Fact Family

| Fact family | Typical target | Main caution |
| --- | --- | --- |
| Physical progress | Production `ScheduleItem` + `ProgressRecord` | Avoid matching by `work_type` only. |
| Actual start / finish | Existing schedule item + statused actual-date update | Do not overwrite baseline timing. |
| Design, permit, approval | Delivery item or gate + `GovernanceRecord` | Governance events may not carry quantities. |
| Procurement / supply | Delivery item + progress or governance record | Package context matters. |
| Issue / change / decision | `GovernanceRecord` linked to the relevant schedule item | One issue must not be mistaken for task completion. |
| Payment / contract | Event item or governance record | Commercial events are not the same as production progress. |
| Control / KPI / inspection | Governance record and possibly linked item | Inspection does not automatically mean progress complete. |
| Readiness / handover | Handover item + governance evidence | Often needs cross-project linkage. |

## Safety Rules

- A fact must never overwrite a baseline directly.
- A fact must never silently disappear because no match was found.
- A low-confidence match must become a review case, not a hidden update.
- The schedule may consume evidence, but the original fact record must remain preserved.
- The formula-fed quantity bridge is allowed only for rows whose project clone matches the template assignment in `fact_collection_map`.
- The formula-fed quantity bridge still relies only on `Stage + Function + Work Type + Unit`, so it remains weaker than a mature row-identity model.
- For non-physical rows, the pilot treats bot-written `volume = 1` as a binary completion signal.

## Stage 22 Result

Stage 22 formalizes a controlled bridge:

- facts stay immutable evidence;
- the schedule stays a governed structure;
- exact mapping remains a deliberate business layer rather than an implicit side effect;
- a narrow one-project formula-fed quantity branch is allowed as a pilot compromise for `schedule_current`.
