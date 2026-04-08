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
- however, open quantity-driven rows in `schedule_current` may consume aggregated quantity through a formula branch.

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

The implemented pilot also accepts one intentionally weaker bridge for open quantity-driven rows in `schedule_current`.

That branch does not try to prove an exact row-level match.
Instead it aggregates `Actual Quantity` from `data_facts` by the shared operational coordinate:

- `stage`
- `function`
- `work_type`
- `unit`

This means:

- `Task ID` is not used in that formula branch;
- `External Ref` is not used in that formula branch;
- time-window logic is not used in that formula branch;
- if several schedule rows share the same four-field coordinate, the same summed quantity may appear in all of them.

This is an accepted pilot limitation.
It is suitable for the current pilot because it is simple, transparent, and reversible, but it is not a strong mature-state matching model.

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
- The formula-fed quantity bridge may duplicate the same fact sum across multiple schedule rows that share the same coordinate.
- The formula-fed quantity bridge is allowed only for open quantity-driven rows in `schedule_current`.

## Stage 22 Result

Stage 22 formalizes a controlled bridge:

- facts stay immutable evidence;
- the schedule stays a governed structure;
- exact mapping remains a deliberate business layer rather than an implicit side effect;
- a narrow formula-fed quantity branch is allowed as a pilot compromise for `schedule_current`.
