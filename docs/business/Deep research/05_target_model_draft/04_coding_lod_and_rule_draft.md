# Coding, LOD, and Rule Draft

## Purpose

This document defines the first target-model decisions for coding, hierarchy, level of detail, and core business rules.

## 1. Selected Hierarchy Strategy

The target model will support multiple hierarchy types through one `HierarchyNode` pattern.

Selected hierarchy types:

- `wbs`
- `stage`
- `package`
- `location_system`
- `handover_system`
- `document_container`

## 2. Selected Code Strategy

The target model will support configurable code dimensions rather than one hard-coded task-code list.

Selected priority code dimensions:

- `responsibility`
- `discipline`
- `contract_package`
- `funding_programme`
- `authority_classification`
- `issue_or_note_category`

## 3. LOD Crosswalk

| LOD | Meaning in target model | Typical regional alignments |
| --- | --- | --- |
| `L0` | Portfolio / programme / global master | USA enterprise, EU programme, Middle East PMIS portfolio |
| `L1` | Project master / contract / approval level | USA IMS/master, EU delivery phases, Middle East master schedule |
| `L2` | Control package / phase / system / work package | USA controls, EU handover systems, China organization layers |
| `L3` | Detailed execution | CIS object and work-package planning, China detailed site control, contractor schedules |
| `L4` | Short-interval / commitment / crew-facing control | CIS weekly-daily logic, collaborative software, field planning |

## 4. Mandatory Coding and LOD Rules

### Rule 1

Every `ScheduleItem` must belong to at least one `wbs` hierarchy path.

### Rule 2

Every delivery-oriented item must have a `stage` or equivalent lifecycle classification.

### Rule 3

Every detailed production item should have either:

- a `location_system` reference;
- a `package` reference;
- or both.

### Rule 4

Handover and readiness items should use `handover_system` hierarchy where commissioning or system turnover is relevant.

### Rule 5

Authority and permit objects should be represented through code and external-link patterns, not by overloading task IDs.

## 5. Core Business Rules

### Rule A

Versions are immutable after publication.

### Rule B

Baselines are formal designations on versions, not overwritten working schedules.

### Rule C

Facts and status updates do not overwrite the baseline layer.

### Rule D

Schedule item type, schedule contour, and schedule purpose are separate concepts and must not be conflated.

### Rule E

Hierarchy and code are separate structures and must not be merged into one overloaded field.

### Rule F

Governance records and external links are first-class and must not be reduced to free-text comments.

## 6. Why This Rule Set Was Chosen

The rule set is directly driven by the comparative synthesis:

- USA and Middle East require strong baseline, PMIS, and governance separation;
- CIS and China require non-flat hierarchy support;
- EU requires lifecycle and handover support;
- software requires version, configured attribute, and link-friendly structures.

## 7. Draft Outcome

The selected coding and rule model is intentionally stricter than a spreadsheet-only task list, but significantly lighter than a full enterprise PMIS platform.
