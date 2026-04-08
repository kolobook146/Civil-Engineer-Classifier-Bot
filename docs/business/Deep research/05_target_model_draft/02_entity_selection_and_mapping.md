# Entity Selection and Mapping

## Purpose

This document explains how the Stage 10-19 entity universe is translated into the Stage 21 target model.

## 1. Selection Logic

Each researched entity is assigned to one of four outcomes:

- `Core entity`
- `Represent through type or subtype`
- `Represent through hierarchy / code / external link`
- `Deferred as dedicated subsystem`

## 2. Core Entity Mapping

| Research entity cluster | Target-model decision | Target construct | Rationale |
| --- | --- | --- | --- |
| Activity / Task / Milestone | Core | `ScheduleItem` | Universal and non-negotiable. |
| Dependency / Lag / External dependency | Core | `Dependency` | Universal logic primitive. |
| Calendar | Core | `Calendar` | Required for time math. |
| Baseline | Core | `BaselineDesignation` + `ScheduleVersion` | Preserves baseline/version distinction. |
| WBS and decomposition nodes | Core | `HierarchyNode` | Required for roll-up and LOD. |
| Resource / crew / role / subcontractor assignment | Core | `ResourceAssignment` | Needed for production and controls relevance. |
| Status / progress / actuals | Core | `ProgressRecord` | Needed for fact linkage and update history. |
| Status report / issue / change / decision / KPI / completion record | Core | `GovernanceRecord` | Needed for the report/log family. |
| PMIS / BIM / EDMS / permit / issue / authority reference | Core | `ExternalObjectLink` | Needed for enterprise and digital-governance reality. |
| Configured fields / custom properties | Core | `AttributeValue` | Needed for flexible extensibility. |

## 3. Represent Through Type or Subtype

| Research entity | Target-model decision | Pattern |
| --- | --- | --- |
| Approval gate | `ScheduleItem` subtype | `item_kind = gate` |
| Procurement package event | `ScheduleItem` subtype | `item_kind = procurement_event` |
| Payment milestone / contractual event | `ScheduleItem` subtype | `item_kind = payment_event` |
| Permit event | `ScheduleItem` subtype or `GovernanceRecord` | Chosen by use case granularity |
| Handover / readiness plan | `ScheduleItem` subtype plus `GovernanceRecord` | Supports both date logic and evidence record |
| Project Master Schedule | `Schedule` subtype | `schedule_purpose = master` |
| IMS / master programme | `Schedule` subtype | Treated as contextual schedule type |
| Schedule version / version history | `ScheduleVersion` subtype | Version roles, publication states |

## 4. Represent Through Hierarchy / Code / External Link

| Research entity | Target-model decision | Pattern |
| --- | --- | --- |
| POS / PPR | Represent through document hierarchy and links | `HierarchyNode(document_container)` + `ExternalObjectLink(document)` |
| Construction organization design | Represent through document hierarchy and links | Same pattern |
| Project cycle stage / phase code | Represent through hierarchy and code | `HierarchyNode(stage)` and/or phase code dimension |
| Work package / control account | Represent through hierarchy plus code | `HierarchyNode(work_package)` + code assignment |
| Location / system / area | Represent through hierarchy and code | `HierarchyNode(location_system)` + code assignment |
| Digital archive key / smart-site object | Represent through link plus attributes | `ExternalObjectLink` + `AttributeValue` |
| Authority classification records | Represent through governance/code/link cluster | `GovernanceRecord` + code + external link |

## 5. Deferred as Dedicated Subsystems

| Research entity cluster | Current Stage 21 decision | Reason |
| --- | --- | --- |
| Full PMIS workflow engine | Deferred | Needed later, but not required to define the schedule business core. |
| Full permit-management engine | Deferred | Too specialized for the first target-model draft. |
| Full document-management engine for POS/PPR/EDMS | Deferred | Links and governance records are enough for the initial business model. |
| Full issue / change / decision workflow platform | Deferred | Typed governance records are enough for the draft stage. |
| Full qualification / classification management system | Deferred | Regional authority support is important, but a dedicated subsystem is premature. |
| Full smart-site / cockpit operating platform | Deferred | External linking is sufficient for the first draft. |

## 6. Main Modeling Outcome

The target model intentionally keeps the number of first-class entities smaller than the full research universe. This is a deliberate design move:

- broad enough to preserve comparative evidence;
- small enough to remain implementable.
