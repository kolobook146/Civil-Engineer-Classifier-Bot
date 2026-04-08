# Stage 23: Extension Systems Overview

## Scope and Purpose

Stage 23 revisits the Stage 21 deferred-extension list after Stage 22 formalization.
The goal is not to promote these subsystems into the pilot core automatically.
The goal is to understand them deeply enough that the project can:

- describe them precisely;
- preserve clean boundaries to them;
- know what evidence would justify future promotion.

The Stage 23 deep pass covers:

1. full PMIS
2. full EDMS / document workflow
3. permit / authority engine
4. smart-site platform
5. resource optimization engine
6. payment / commercial engine

## Main Conclusion

These are not "additional fields around the schedule."
They are six distinct operating systems that interact with the schedule while keeping their own:

- first-class business objects;
- workflow state machines;
- role and permission models;
- audit and traceability records;
- integration boundaries.

Research interpretation:
the Stage 21 decision to keep them out of the pilot core remains correct.
However, Stage 23 shows that they are too important to remain vague.
They now need named architectural boundaries and explicit extension hooks.

## Stage 23 Method

This pass combines:

- previously collected regional and enterprise evidence from Stage 6-19;
- official open software documentation;
- official authority-system documents;
- product help centers and public user guides where field and workflow detail is inspectable.

Priority was given to sources that reveal actual object and workflow structure rather than marketing-only claims.

## The Six System Families

### 1. PMIS

PMIS is the broadest project operating environment.
It usually wraps:

- cost;
- change;
- payment;
- schedule;
- document;
- issue;
- reporting;
- workflow inbox logic.

### 2. EDMS / CDE / document workflow

This family governs controlled information containers and the project record.
Its center of gravity is:

- document register;
- revision and status control;
- transmittals;
- review workflows;
- archive traceability.

### 3. Permit / authority engine

This family governs external regulatory progression.
Its grammar is based on:

- submission cases;
- gateways;
- agencies;
- payments and proofs;
- returned comments;
- re-submissions;
- approvals and certificates.

### 4. Smart-site platform

This family captures the operational site pulse.
Its core logic is:

- observations;
- forms;
- daily logs;
- sensor / device events;
- alerts;
- corrective actions;
- dashboards.

### 5. Resource optimization engine

This family is about feasibility of execution.
Its core logic is:

- demand;
- capacity;
- pools;
- assignments;
- availability;
- leveling;
- reassignment.

### 6. Payment / commercial engine

This family governs financial-commercial execution.
Its core logic is:

- commitments and contracts;
- schedule of values;
- requisitions and invoices;
- change orders;
- compliance documents;
- holds;
- payment release and reconciliation.

## How Stage 23 Changes the Research Picture

Before Stage 23, the research already showed that the schedule core could not safely be reduced to a flat task list.
After Stage 23, the stronger conclusion is:

- the schedule core is still only one subsystem inside a broader project operating architecture;
- the pilot model should stay hybrid but bounded;
- the project now needs an explicit extension architecture rather than an implicit "external systems exist" note.

## Cross-System Pattern

Across all six families, the recurring structure is:

1. a governed container
2. typed records
3. a routing / approval state machine
4. a role / permission model
5. an audit trail
6. a reporting or dashboard layer
7. explicit link points back to schedule dates, milestones, packages, or versions

This is the main reason they cannot be represented by one generic `AttributeValue` bag alone.

## Relationship to the Stage 21 Hooks

Stage 21 kept the right extension hooks:

- `HierarchyNode`
- `CodeDimension / CodeValue / ItemCodeAssignment`
- `GovernanceRecord`
- `ExternalObjectLink`
- `AttributeValue`

Stage 23 conclusion:

- these hooks are still adequate for the pilot core;
- but they must now be interpreted as explicit subsystem-bridge patterns, not just generic extensibility mechanisms.

## Output of Stage 23

Stage 23 produces:

- one extension-systems matrix;
- six subsystem reports;
- one synthesis report;
- updates to source, entity, property, coding, process, and emergent-finding registries;
- a bounded extension-architecture reflection in normative business documentation.
