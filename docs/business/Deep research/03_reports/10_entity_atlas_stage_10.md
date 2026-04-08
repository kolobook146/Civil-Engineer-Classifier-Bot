# Stage 10: Entity Atlas

## Purpose

This report rebuilds the entity layer using the regional artifacts already found in Stages 6-9 and extends them with open-source institute artefacts gathered in the current research pass.

## 1. Main Conclusion

Researcher inference:

- A realistic schedule model for investment construction projects is not limited to tasks, milestones, dependencies, calendars, and resources.
- The open-source evidence now clearly supports a much wider entity universe that includes:
  - planning documents;
  - stage-gate objects;
  - acceptance artefacts;
  - control logs;
  - project-cycle stages;
  - digital archive and checkpoint objects.

## 2. Five Entity Families Now Evident

### 2.1 Core network and execution entities

- activity / task
- milestone
- dependency
- lag / lead
- calendar
- critical path
- float
- resource

### 2.2 Hierarchy and decomposition entities

- WBS
- work package
- OBS / responsibility structure
- activity code
- WBS element / decomposition node
- level-of-detail designation

### 2.3 Governance and planning-document entities

- POS
- PPR
- construction organization design
- schedule basis
- scheduling specification
- business case
- project charter
- project work plan

### 2.4 Delivery and stage-gate entities

- project cycle stage
- procurement package
- approval gate
- PPP phase
- deliverables acceptance plan
- phase-exit checklist
- project status report / progress report
- issue / decision / change log

### 2.5 Digital-governance entities

- digital supervision archive
- progress-warning object
- unified digital project code
- digital checkpoint

## 3. Region-Native Entity Contributions

| Region | Most distinctive entities |
| --- | --- |
| CIS | POS, PPR, linear graph / cyclogram, weekly-daily schedule |
| EU | project cycle stage, procurement package, PPP gate, work-plan artefacts through PM² |
| USA | IMS, schedule quality criteria, schedule review package, baseline control artefacts |
| China | construction organization design, engineering network plan, digital supervision archive, digital project code |

## 4. Institute-Native Entity Contributions

| Institute / system | Strongest entity additions |
| --- | --- |
| PMI | WBS and decomposition-centered entities |
| AACE | schedule basis, scheduling specification, statusing artefacts |
| PM² | business case, project charter, work plan, acceptance artefacts, logs, checklists |
| FIDIC | contract-lifecycle events, notices, progress meetings, closeout tasks |
| EIB / EPEC | project-cycle stages, procurement and PPP governance artefacts |
| GAO | IMS quality and review-oriented entity class |

## 5. What Changed Relative to the Previous Base

Before this pass, the research base already included region-specific artifacts such as POS/PPR, IMS, project-cycle stage, construction organization design, and digital supervision archive.

After this pass:

- those artifacts are no longer isolated curiosities;
- they now sit inside larger entity families;
- institute artefacts confirm that document, gate, checklist, and log objects are structurally legitimate schedule-model entities.

## 6. Main Modeling Implication

The entity model should probably be layered, not flat:

- network layer;
- hierarchy layer;
- governance-document layer;
- delivery-process layer;
- digital-governance layer.

If the model keeps only task-like rows, it will fail to represent much of the real scheduling practice found in the open-source evidence.

## 7. Main Supporting Sources

- `SRC-A-026`, `SRC-A-027`, `SRC-A-036`
- `SRC-A-031`, `SRC-A-041`, `SRC-A-044`
- `SRC-A-037`, `SRC-A-038`, `SRC-A-039`, `SRC-A-040`
- `SRC-A-042`
- `SRC-A-043`
