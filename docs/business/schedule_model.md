# Schedule Model

Status: normative Stage 22 schedule business model.

## Purpose

This document defines the formal business model of the project schedule.
The schedule is the structured representation of planned, governed, and tracked work across the investment construction lifecycle.

## Design Position

The project schedule is not modeled as a flat task list only.
It is a hybrid schedule model that must simultaneously support:

- production planning and control;
- project-delivery planning and governance;
- baseline and version discipline;
- explicit hierarchy and coding;
- progress, governance, and external-system linkage.

## Scope

The schedule covers both:

- `production` logic: physical works, workfronts, sequencing, quantities, crews, and short-interval control;
- `delivery` logic: design, permits, tenders, contracts, procurement, payments, approvals, commissioning, and handover;
- `cross-project` logic: PMO, reporting, KPI, decision, and other governance objects that touch both contours.

## Pilot Semantic Coordinates

The project keeps the existing pilot matrix logic:

- `function` = business workstream;
- `stage` = lifecycle position inside that workstream;
- `work_type` = optional physical scope refinement.

In the Stage 22 target model:

- `function` is the pilot workstream vocabulary used on schedule items;
- `stage` is the lifecycle classification used for delivery and governance logic;
- `work_type` remains optional and is mainly relevant for physical work scope and its support.

## Canonical Schedule Entities

| Entity | Business role | Stage 22 interpretation |
| --- | --- | --- |
| `Schedule` | Main schedule container | One governed planning context such as a project master, contract schedule, or look-ahead schedule. |
| `ScheduleVersion` | Immutable schedule revision | A published or saved revision tied to a `status_date` and change context. |
| `BaselineDesignation` | Formal baseline marker | Explicit designation of a version as `initial`, `current`, `contract`, or other baseline role. |
| `ScheduleItem` | Core work or governance object | Unified item for activities, milestones, gates, and generic event rows with subtype detail. |
| `Dependency` | Sequencing logic | Explicit predecessor-successor logic between schedule items. |
| `Calendar` | Time-calculation context | Calendar rules used for schedule math. |
| `HierarchyNode` | Roll-up structure | WBS, stage, package, location/system, handover-system, or document-container structure. |
| `CodeDimension / CodeValue / ItemCodeAssignment` | Reusable classification | Configurable coding for function, discipline, package, responsibility, authority, and other business dimensions. |
| `ResourceAssignment` | Resource context | Role, crew, subcontractor, or resource-group assignment attached to a schedule item. |
| `ProgressRecord` | Time-stamped progress fact | Operational progress state associated with a schedule item. |
| `GovernanceRecord` | Approval, issue, change, KPI, completion, or review fact | First-class governance layer for non-physical project control signals. |
| `ExternalObjectLink` | External traceability | Link to PMIS, EDMS, BIM, permit, authority, payment, issue, or other external records. |
| `AttributeValue` | Configurable extension field | Flexible extension point for client-, region-, or workflow-specific fields. |

## What Counts as a Schedule Item

`ScheduleItem` is the main business object of the model.
It may represent:

- `activity`
- `milestone`
- `gate`
- `event`

The model intentionally does not create a separate entity table for each of these.

In the current pilot row schema, `Item Type` acts as the extensible subtype slot for event-like detail such as:

- `procurement`
- `permit`
- `payment`
- `handover`
- `control`

The flattened pilot sheet also allows `wbs` summary rows as structural carriers.
These are sheet-level structural rows rather than standalone operational schedule items.

## Mandatory Schedule-Item Meaning

In the current pilot business model, every actionable schedule item should carry:

- an immutable `Task ID`;
- a `Task Name`;
- an `item_kind`;
- an optional `item_type` when subtype detail is needed;
- a `contour`;
- a `function`;
- a `stage`;
- at least one usable hierarchy reference, with `WBS Path` as the minimum pilot form;
- planned timing fields appropriate to the item type;
- status information.

`work_type` remains optional and should be used where the row belongs to a physical work scope or directly supports it.

## Production and Delivery Contours

The model explicitly supports two overlapping but different schedule universes.

### Production contour

Typical attributes:

- `function = Construction Execution`
- `stage = Execution` or another control-relevant lifecycle position
- `work_type`, quantity, unit, package, location/system, and planned intensity become especially important

### Delivery contour

Typical attributes:

- functions such as permits, design, procurement, contracts, financing, or commissioning
- lifecycle gates such as approvals, tender, contract, procurement, control, and closeout
- not every item has a physical `work_type`, but delivery rows tied to a physical scope may still use it

### Cross-project contour

Used for:

- PMO and control events
- KPI and review logic
- readiness and handover coordination
- governance items that span both production and delivery

## Hierarchy and Coding

Stage 22 formalizes a strict separation:

- hierarchy is for parent-child structure and roll-up;
- coding is for reusable classification.

The current target hierarchy types are:

- `wbs`
- `stage`
- `package`
- `location_system`
- `handover_system`
- `document_container`

The current priority coding dimensions are:

- `function`
- `discipline`
- `contract_package`
- `responsibility`
- `authority_classification`
- `issue_or_note_category`

## Versioning and Baseline

The schedule is versioned.
This means:

- a working change creates or updates a `ScheduleVersion`;
- publication freezes that version as an immutable revision;
- baseline is not the same thing as version in the conceptual model;
- the pilot workbook represents this through two explicit surfaces: `baseline` and `current`.

This is the formal replacement for the earlier idea of mixing baseline and actual in one mutable row set.

## Progress and Governance

The schedule must support both:

- operational progress;
- governance and control context.

Therefore:

- progress belongs in `ProgressRecord`;
- approvals, issues, change, KPI, completion, and similar events belong in `GovernanceRecord`;
- external systems remain linked through `ExternalObjectLink`.

At the pilot sheet level, the current projection also separates:

- planned versus actual quantity;
- planned versus actual cost;
- final actual duration versus open-row projection through `Forecast Start`, `Forecast Finish`, and `Remaining Duration`.

## Current Pilot Sheet Representation

The current pilot workbook projection of this model is documented in:

- `docs/business/sheets/schedule_workbook.md`

The row-level schedule schema is documented in:

- `docs/business/sheets/schedule_sheet.md`

The current pilot workbook uses:

- `schedule_baseline` as the frozen comparison surface;
- `schedule_current` as the active control surface;
- `used_task_ids` as the non-reuse register for immutable identifiers.

It also uses:

- one `Status Date` per sheet/version;
- immutable `Task ID` values in the default `T10000`-series format;
- `Item Kind` plus optional `Item Type` to separate primary row meaning from subtype detail.

The row schema is a flattened business representation of:

- one sheet version at a time;
- many `ScheduleItem` rows;
- selected hierarchy, dependency, timing, quantity, cost, progress, forecast, and external-link fields.

It is a projection of the business model, not the whole ontology.

## Deliberate Boundary

The Stage 22 schedule model does not yet define full dedicated subsystems for:

- PMIS workflow management;
- permit workflow management;
- EDMS lifecycle management;
- smart-site operations;
- resource optimization;
- payment management.

These remain extension areas rather than core schedule entities.
The named bounded-extension position is recorded in:

- `docs/business/extension_architecture.md`

## Relationship to Facts

Facts remain a separate evidence register.
They may later:

- support progress updates on schedule items;
- create governance evidence around schedule items;
- remain informational if no safe schedule linkage exists.

The mapping logic is defined in:

- `docs/business/fact_to_schedule_mapping.md`
