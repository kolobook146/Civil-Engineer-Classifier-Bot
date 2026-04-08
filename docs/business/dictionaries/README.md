# Business Dictionaries

Status: active pilot vocabularies.

## Purpose

These files contain the controlled business vocabularies used by the pilot classifier and by the business documentation.

## Dictionaries

- `functions.txt`
  Functional workstreams of the project.
- `stages.txt`
  Standardized lifecycle gates that can occur within a function.
- `item_kinds.txt`
  Primary row types used in the pilot schedule sheet.
- `item_types.txt`
  Extensible subtype vocabulary used where a row needs additional business meaning.
- `contours.txt`
  Project contours separating production, delivery, and cross-project logic.
- `statuses.txt`
  Controlled operational status values used by the schedule.
- `work_types.txt`
  First-level construction and installation work classification.
- `phases.txt`
  Controlled portfolio-phase classification used on schedule rows.
- `responsibles.txt`
  Controlled responsibility buckets used instead of person names.
- `external_systems.txt`
  Named external systems linked from schedule rows.
- `external_object_types.txt`
  Generic external object classes linked from schedule rows.
- `units.txt`
  Canonical measurement units and descriptions.
- `planned_cost_reference.md`
  Normative cost-assignment reference for `Planned Cost`; this is not a controlled vocabulary file.

## Business Role of Each Dictionary

### Functions

Functions answer the question:
`What project workstream is being delivered, managed, or advanced?`

Examples:
- Design Management
- Material & Technical Supply
- Construction Execution
- Commissioning & Handover

### Stages

Stages answer the question:
`At which lifecycle gate is this workstream right now?`

Examples:
- Initial data
- Tender
- Procurement
- Execution
- Control

### Work Types

Work types answer the question:
`What physical construction scope is being performed?`

Examples:
- Earthworks
- Concreting
- Ventilation
- Landscaping

### Phases

Phases answer the question:
`Which of the 7 portfolio phases does this schedule row belong to?`

Examples:
- `01 Statutory planning approvals`
- `04 Tendering and contracting`
- `07 Parallel fit-out, systems, closeout`

### Item Kinds

Item kinds answer the question:
`What primary row kind is this in the pilot schedule?`

Examples:
- `activity`
- `milestone`
- `gate`
- `event`
- `wbs`

### Item Types

Item types answer the question:
`Which subtype should be attached to this row when the primary kind alone is not enough?`

Examples:
- `procurement`
- `permit`
- `payment`
- `handover`
- `control`

### Contours

Contours answer the question:
`In which project universe does this row mainly live?`

Examples:
- `production`
- `delivery`
- `cross-project`

### Statuses

Statuses answer the question:
`What is the current operational state of this row?`

Examples:
- `not_started`
- `in_progress`
- `done`
- `blocked`
- `cancelled`

### Responsibles

Responsibles answer the question:
`Which business unit or external responsibility bucket owns this row?`

Examples:
- `Project Controls`
- `Design Management`
- `General Contractor`
- `Authority Interface`

### Units

Units answer the question:
`In which canonical measurable unit should the volume or quantity be expressed?`

### Planned Cost Reference

The planned-cost reference answers the question:
`Where should the direct planned cost live, and on what basis should it be assigned?`

It is used to:

- assign `Planned Cost` consistently across delivery, procurement, execution, and control rows;
- prevent double counting between procurement and execution layers;
- keep the pilot on one normalized cost basis.

## Important Distinctions

- `function` is not the same as `stage`.
- `function` is not the same as `work_type`.
- `phase` is not the same as `stage`.
- `stage` is not the same as task status.
- `item_kind` is not the same as `item_type`.
- `work_type` does not replace the project workstream; it only refines the scope of work.

## Pilot Rules

- Dictionaries are the source of allowed values.
- `planned_cost_reference.md` is a normative reference catalog, not a controlled-value list.
- The pilot allows one selected value or no value for `work_type`.
- The pilot allows one selected value or no value for `phase`; project root rows may keep it blank.
- The pilot allows one selected value or no value for `item_type`, except rows that explicitly require subtype detail.
- The pilot requires exactly one `function` and one `stage` for each structured fact.
- `responsible` must be chosen from controlled responsibility buckets rather than entered as a person name.
