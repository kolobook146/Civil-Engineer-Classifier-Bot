# Stage 23: Full EDMS / Document Workflow Report

## Scope

This report studies EDMS, CDE, and document workflow systems as full delivery subsystems.

Primary evidence base:

- `SRC-A-098`
- `SRC-A-106`
- `SRC-A-117`
- `SRC-A-127`
- `SRC-A-128`
- `SRC-A-129`
- `SRC-A-135`
- `SRC-A-136`
- `SRC-A-138`

## Main Conclusion

EDMS is not a file store.
It is a controlled project-record system with explicit revision, review, transmittal, and archive logic.

Research interpretation:
the canonical object is not "file attachment," but a governed document record with status lineage.

## Core EDMS Grammar

Across the source base, the recurring object model is:

- document register entry;
- document number and metadata;
- revision and revision date;
- status;
- transmittal;
- review workflow;
- package or bundle;
- archive / immutable project record;
- role and permission model;
- mail and notification trail.

This makes EDMS one of the clearest `document-system` families in the entire research corpus.

## Strong Evidence from Official Documentation

### Oracle Aconex

`SRC-A-128`, `SRC-A-129`, and `SRC-A-130` show a mature document-workflow grammar:

- start a workflow from a controlled template;
- lock documents during workflow processing;
- transmit controlled documents through transmittals;
- preserve an un-alterable project record;
- update the register through new revisions instead of uncontrolled duplicates.

This is one of the strongest open demonstrations that document workflow is a state machine, not a passive storage service.

### Oracle Primavera Unifier

`SRC-A-127` shows EDMS behavior embedded inside PMIS:

- shell document-manager structure;
- governed templates;
- permissions;
- admin-controlled container setup.

This is important because it demonstrates that EDMS may either be standalone or PMIS-embedded.

### Autodesk Construction Cloud

`SRC-A-135`, `SRC-A-136`, and `SRC-A-137` show a modern collaborative document-governance layer:

- configurable approval workflows;
- review-step routing;
- transmittals tied to file versions;
- activity logs and audit trail;
- strong traceability between review and issued-document behavior.

### Procore

`SRC-A-138` shows that collaborative platforms also grow explicit document workflow objects:

- submittals;
- submitter / approver roles;
- submittal packages;
- revision handling;
- related-item linkage.

## Regional Signals

### EU

The EU layer is especially strong on controlled information management and delivery governance.
The region does not always expose one universal EDMS application, but the logic of:

- controlled documents;
- review lineage;
- approved issue;
- archive discipline

is especially visible.

### Middle East

The Middle East makes EDMS operationally explicit through owner requirements and consultancy practice:

- EDMS and PMIS are often required together;
- review, approval, and record-control discipline is contractual rather than optional.

### CIS and China

CIS and China reinforce the document-system family through:

- planning-document traditions;
- document-container logic;
- digital supervision archives;
- lifecycle digital record systems.

## Relationship to Schedule

The schedule depends on EDMS for:

- issued design packages;
- review and approval evidence;
- submittal and transmittal deadlines;
- document-controlled gates;
- archive-grade traceability.

But EDMS is still not reducible to the schedule.
Its primary unit is the information container and its review lifecycle.

## Target-Model Implication

The Stage 22 core should still not host a full EDMS lifecycle.
However, Stage 23 clarifies what the bridge must preserve:

- document identity;
- revision and status;
- workflow / review outcome;
- transmittal or package reference;
- immutable external record linkage.

## Bottom-Line Result

EDMS is one of the most mature and structurally explicit extension families in the research corpus.
If the project ever outgrows the current pilot hooks, EDMS is one of the first subsystems that should be promoted to a dedicated integration layer.
