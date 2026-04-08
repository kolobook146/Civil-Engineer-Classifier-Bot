# Stage 23: Full PMIS Report

## Scope

This report studies PMIS as a full enterprise project operating system rather than as "schedule software plus dashboards."

Primary evidence base:

- `SRC-A-085` to `SRC-A-089`
- `SRC-A-105` to `SRC-A-117`
- `SRC-A-125`
- `SRC-A-126`
- `SRC-A-127`
- `SRC-A-130` to `SRC-A-133`

## Main Conclusion

PMIS is the broadest and most important deferred subsystem.
In real enterprise delivery, PMIS is often the actual system-of-record around the schedule, not a thin integration shell.

Research interpretation:
the schedule is one major governed object inside PMIS, alongside cost, change, payment, documents, approvals, reports, and action workflows.

## What Counts as PMIS in Practice

The current corpus shows three strong PMIS archetypes.

### 1. Owner-mandated PMIS

Strongest in:

- USA owner guidance
- Middle East owner practice

Signature:

- periodic submissions;
- required master schedule structures;
- cost and change integration;
- dashboard and KPI obligations;
- formal review cycles and PMO ownership.

### 2. Configurable enterprise PMIS platform

Strongest in:

- Oracle Primavera Unifier
- PMWeb

Signature:

- shells or project workspaces;
- configurable business-process records;
- workflow runtime;
- cost sheets and commercial records;
- document and transmittal modules;
- role-based permissions and inboxes.

### 3. Collaboration-led project platform with PMIS behavior

Strongest in:

- Procore
- Autodesk Construction Cloud

Signature:

- broader collaboration footprint;
- strong field adoption;
- less explicit classical PMIS language;
- still exposes PMIS-like objects through submittals, issues, cost approvals, forms, logs, and review workflows.

## Core PMIS Object Model

Across the evidence base, the recurring PMIS object stack is:

- portfolio / programme / project / shell hierarchy;
- workflow-enabled business process record;
- controlled cost ledger or cost sheet;
- budget / funding / commitment / change / invoice records;
- master schedule reference or schedule import;
- document / transmittal / submittal references;
- issue / observation / RFI / action registers;
- dashboard, report, and KPI objects;
- user-role, permission, and inbox / action queue objects.

The key discovery is that the PMIS "record" is often more central than the schedule activity.

## Strong Evidence from Official Product Documentation

### Oracle Primavera Unifier

`SRC-A-125`, `SRC-A-126`, and `SRC-A-127` show a mature PMIS grammar:

- shell-driven project structures;
- configurable business processes;
- cost-type forms and schedule-of-values behavior;
- project and shell administration;
- document-manager structures;
- workflow-enabled record routing.

Unifier is one of the clearest openly inspectable examples of PMIS as a runtime operating system rather than a passive repository.

### PMWeb

`SRC-A-130` to `SRC-A-133` show a similar but slightly more record-centric grammar:

- requisitions;
- transmittals;
- submittals;
- change events;
- linked records and workflow routing.

PMWeb makes the PMIS structure legible because it exposes project records as strongly typed operational objects.

## Regional Signals

### USA

The U.S. evidence base remains strongest on owner PMO and integrated project controls.
PMIS here is closely tied to:

- IMS discipline;
- cost / schedule integration;
- PMO review cycles;
- enterprise stewardship.

### Middle East

The Middle East is the strongest region in the corpus for explicit PMIS requirements.
Owner-side material shows:

- Project Master Schedule obligations;
- PMDS / APMS operating environments;
- cost-loaded control expectations;
- change, payment, KPI, and document governance;
- PMO and TPMO style delivery systems.

### China

China strengthens the platformized interpretation of PMIS.
PMIS-like logic is often fused with:

- smart-site cockpit;
- digital supervision;
- unified digital coding;
- lifecycle digital governance.

### EU and CIS

EU and CIS sources show more variation.
The PMIS layer is often expressed through:

- programme governance systems;
- controlled planning handbooks;
- document and digital-control platforms;
- large-enterprise digital oversight environments.

## Relationship Between PMIS and Schedule

PMIS does not replace the schedule.
But it changes the schedule's operational role.

Inside PMIS, the schedule becomes:

- one governed source object among others;
- one input to workflows, dashboards, and review cycles;
- one trigger for cost, change, payment, readiness, and reporting actions.

This is why PMIS cannot be reduced to:

- imported schedule file metadata;
- a few governance columns;
- or generic comments.

## Implication for the Target Model

The pilot core should still not become a full PMIS clone.
However, Stage 23 makes several implications explicit:

- PMIS should be named as a bounded external subsystem;
- `ExternalObjectLink` must support PMIS record identity, type, and lifecycle status;
- `GovernanceRecord` should remain able to represent PMIS review and approval outcomes;
- hierarchy and coding should remain capable of carrying PMIS portfolio / programme / shell context.

## Bottom-Line Result

PMIS is not optional enterprise decoration.
It is the strongest evidence that real-world schedule practice is embedded in a broader operating system.
That confirms the Stage 21-22 choice to keep the core small, but it also proves that future enterprise expansion should begin with PMIS boundaries first.
