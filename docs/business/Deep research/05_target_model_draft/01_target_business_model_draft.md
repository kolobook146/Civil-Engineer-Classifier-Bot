# Target Business Model Draft

## Purpose

This draft selects the target schedule business model directly from the comparative synthesis rather than from any single region, methodology, or software product.

## Evidence Anchor

The main evidence path for this draft is:

- `../02_registries/comparative_synthesis_matrix_stage_19.md`
- `../04_research_package/01_narrative_report.md`
- `../04_research_package/02_comparative_matrix_pack.md`
- `../04_research_package/03_catalog_pack.md`
- `../04_research_package/04_software_report_pack.md`
- `07_decision_traceability_matrix.md`

## 1. Design Stance

The target model should be:

- simple enough for an initial implementation;
- broad enough to support both production and project-delivery schedules;
- explicit about governance and digital links;
- configuration-first where regional or client variability is high;
- extensible without forcing a redesign when PMIS, handover, or authority-governance layers appear later.

## 2. Main Design Choice

The target model is a unified hybrid schedule model with five built-in families:

1. `decomposition`
2. `document-system`
3. `stage-gate`
4. `report/log`
5. `digital-governance`

It does not create five separate systems. It creates one core model that can express all five families through typed entities, hierarchies, codes, governance records, and external links.

## 3. Canonical Core Entities

| Entity | Role in target model | Why selected |
| --- | --- | --- |
| `Schedule` | Main container for one schedule context | Needed to support project, contract, programme, or portfolio schedules. |
| `ScheduleVersion` | Immutable published or saved schedule revision | Required because software and enterprise practice treat versions as first-class. |
| `BaselineDesignation` | Formal designation of one version as a baseline type | Selected to preserve the distinction between version and baseline. |
| `ScheduleItem` | Unified work/governance item | Chosen instead of separate task/milestone/gate tables to support both production and delivery logic. |
| `Dependency` | Logic relation between schedule items | Universal requirement across all regions and tools. |
| `Calendar` | Time-calculation context | Universal and necessary for date math. |
| `HierarchyNode` | Roll-up and decomposition container | Needed to represent WBS, stage, package, location/system, handover, and document-container structures. |
| `CodeDimension / CodeValue / ItemCodeAssignment` | Flexible classification layer | Needed because code families vary by region, client, and software. |
| `ResourceAssignment` | Resource, crew, role, subcontractor, or group assignment | Needed to preserve production and controls capability without overbuilding a full resource engine. |
| `ProgressRecord` | Time-stamped progress fact for a schedule item | Needed to separate schedule structure from observed progress state. |
| `GovernanceRecord` | Typed status, issue, change, decision, KPI, approval, or completion record | Needed to represent the report/log family without building multiple workflow engines up front. |
| `ExternalObjectLink` | Link to PMIS, EDMS, BIM, permit, issue, payment, authority, or other external records | Needed because enterprise and software evidence repeatedly shows the schedule living in a linked ecosystem. |
| `AttributeValue` | Configurable extension field on a target entity | Needed to absorb software-style configured fields and region/client extensions without schema explosion. |

## 4. What `ScheduleItem` Must Support

`ScheduleItem` is the main target-model work object. It must support:

- activity;
- milestone;
- approval gate;
- procurement event;
- permit event;
- payment event;
- handover or readiness event;
- reporting or control event where required by the business model.

Required target fields:

- stable item key across versions;
- name;
- item kind;
- contour: `production`, `delivery`, or `cross-project`;
- stream: `engineering`, `procurement`, `construction`, `commissioning`, `governance`, `authority`, or `commercial`;
- planned start / finish / duration;
- actual start / finish;
- remaining duration;
- percent complete;
- status;
- calendar reference;
- primary hierarchy reference.

## 5. What Is Deliberately Modeled Through Generic Patterns

The model deliberately avoids creating one dedicated entity for every regional or software artifact. Instead:

- `approval gates`, `phase exits`, `payment milestones`, `permit events`, and `handover events` are represented as `ScheduleItem` kinds;
- `POS`, `PPR`, construction organization design, and schedule sheets are represented through `HierarchyNode`, `GovernanceRecord`, and `ExternalObjectLink`;
- `issue`, `change`, `decision`, `status report`, `KPI record`, and `completion record` are represented through typed `GovernanceRecord`;
- PMIS, BIM, EDMS, permit systems, and authority platforms are represented through `ExternalObjectLink`;
- client- or region-specific fields are represented through `AttributeValue`.

This is the main pilot-oriented simplification in the draft.

## 6. Mandatory Model Principles

### Principle 1

Separate `ScheduleVersion` from `BaselineDesignation`.

### Principle 2

Separate hierarchy from coding:

- hierarchy for roll-up and parent-child logic;
- coding for reusable classification.

### Principle 3

Keep `production` and `delivery` as explicit contours on items and schedules.

### Principle 4

Treat governance records and external links as first-class, not as free-text notes only.

### Principle 5

Keep facts append-only and time-stamped through `ProgressRecord` and `GovernanceRecord`.

### Principle 6

Use configuration rather than hard-coded regional tables wherever possible.

## 7. Regional and Comparative Rationale

### Why this is not a pure U.S. CPM model

Because the comparative synthesis showed that a task-only CPM file would lose:

- CIS document-system logic;
- EU stage-gate and handover logic;
- China smart-site and digital-governance logic;
- Middle East PMIS and authority-governance logic.

### Why this is not a pure document model

Because the same synthesis showed that universal schedule math and enterprise controls remain essential.

### Why this is not a software-clone model

Because Stage 19 showed that software objects encode execution grammar, but not necessarily the full operating governance or regional meaning.

## 8. Selected LOD Direction

The target model uses one canonical LOD ladder:

- `L0` portfolio / programme / global master
- `L1` project master / contract / phase / approval
- `L2` control / package / system / work package
- `L3` detailed execution
- `L4` short-interval / commitment / crew-facing control

This is not meant to erase regional variation. It is a working crosswalk.

## 9. Selected Boundary for Initial Implementation

Included in the target model:

- hybrid schedule structure;
- governance-aware item model;
- hierarchy and code layers;
- progress and fact linkage;
- external ecosystem linkage;
- pilot-safe configurability.

Not included as full dedicated subsystems yet:

- full document-management engine;
- full permit-management engine;
- full PMIS workflow engine;
- full resource optimization engine;
- full payment-management engine.

## 10. Result

The selected target model is a governance-aware, hybrid schedule core that is intentionally smaller than the full research universe, but structurally broad enough to support:

- production schedules;
- project-delivery schedules;
- enterprise controls;
- software-native traceability;
- future regional and authority extensions.
