# Production Schedule vs Project Delivery Schedule

## Purpose

This document establishes the initial two-contour model requested for the research program:

- construction production schedule;
- investment-construction project delivery schedule.

The goal is not to force a binary split in practice, but to preserve a necessary analytical distinction.

## 1. Initial Conclusion

Researcher inference from the first-pass sources:

- A production schedule is centered on execution of physical work.
- A project delivery schedule is centered on realization of the project as an investment and contractual lifecycle.
- In mature projects, these two contours overlap and exchange milestones, but they are not the same model.

## 2. Production Schedule

### 2.1 Main focus

- work sequence on site;
- crews and production capability;
- equipment and material readiness;
- workfront access;
- short- and medium-range control;
- daily or weekly execution reliability.

### 2.2 Dominant entities

- activity
- milestone
- relationship
- lag / lead
- calendar
- resource
- crew
- location or area segment
- production constraint
- look-ahead package

### 2.3 Strongest current sources

- `SRC-A-002`
- `SRC-A-003`
- `SRC-A-018`
- `SRC-A-022`

## 3. Project Delivery Schedule

### 3.1 Main focus

- feasibility and project definition;
- approvals and formal review;
- design and engineering;
- procurement and contracting;
- financing and funding events;
- construction execution;
- commissioning, handover, and closeout.

### 3.2 Dominant entities

- phase
- gate
- approval event
- procurement package
- contract event
- funding milestone
- baseline
- reporting package
- delivery workstream

### 3.3 Strongest current sources

- `SRC-A-016`
- `SRC-A-020`
- `SRC-A-023`
- `SRC-A-024`
- `SRC-A-025`

## 4. Key Differences

| Dimension | Production schedule | Project delivery schedule |
| --- | --- | --- |
| Primary object | Physical work execution | End-to-end project realization |
| Dominant time logic | Work sequence and site constraints | Lifecycle sequencing and governance events |
| Main resource view | Labor, crews, equipment, materials | Organizations, packages, approvals, funding, contracts |
| Main users | Site team, contractor, superintendent, project controls | Owner, PMO, project manager, commercial team, public authority |
| Typical horizon | Detailed, look-ahead, short interval | Lifecycle, phase, integrated control |
| Core success question | Can the work be executed on time and in sequence? | Can the project be realized and handed over on time? |

## 5. Shared Layer

The two contours overlap in:

- major construction milestones;
- baseline logic;
- status and forecast cycle;
- critical path or controlling path thinking;
- WBS or equivalent hierarchy;
- schedule coding and reporting;
- owner-contractor review interfaces.

## 6. Typical Exchange Points Between the Two Contours

The project delivery schedule often feeds the production schedule through:

- notice to proceed;
- permit receipt;
- design issue dates;
- procurement release and delivery dates;
- interface milestones;
- commissioning readiness criteria.

The production schedule feeds the delivery schedule through:

- actual progress;
- slippage and recovery;
- resource and access constraints;
- forecast completion;
- handover readiness.

## 7. Why This Separation Matters

Without this separation, research tends to create one of two errors:

- reducing delivery logic to a construction-only timeline;
- diluting production planning into an over-broad program timeline.

Both errors make later business modeling weaker.

## 8. Initial Modeling Implication

The target model should probably support at least:

- shared universal schedule entities;
- contour-specific entities and rules;
- linkage objects between delivery milestones and production execution;
- different levels of detail and update rhythms for each contour.

This is not yet the final target-model decision, only an implication from the research.

## 9. Current Evidence Base

- `SRC-A-002`
- `SRC-A-003`
- `SRC-A-016`
- `SRC-A-018`
- `SRC-A-020`
- `SRC-A-022`
- `SRC-A-023`
- `SRC-A-024`
- `SRC-A-025`
