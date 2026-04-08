# Deferred Extensions

## Purpose

This document records important capabilities evidenced by the research corpus that are intentionally not promoted to full first-class subsystems in the Stage 21 draft.

## 1. Deferred for Post-Draft Expansion

### PMIS workflow engine

Deferred because:

- enterprise practice proves its importance;
- but the target business core should not become a full PMIS clone at the draft stage.

### Full document-management and EDMS lifecycle

Deferred because:

- document-system logic is important;
- but full revision, approval, and storage workflows can remain external initially.

### Full permit and authority workflow engine

Deferred because:

- Middle East evidence shows its relevance;
- but a full authority-process subsystem is too specialized for the first target-model draft.

### Full issue / change / decision management platform

Deferred because:

- the target model only needs typed governance records and references at this stage.

### Full smart-site / cockpit platform

Deferred because:

- China, CIS enterprise, and parts of Middle East practice show its importance;
- but external links and governed facts are sufficient for the draft stage.

### Full resource optimization and leveling engine

Deferred because:

- research supports resource importance;
- but the draft needs resource-aware structure, not necessarily an optimization subsystem.

### Full payment and commercial-management engine

Deferred because:

- delivery practice frequently ties schedule to payment;
- but the first target draft only needs payment-event and governance linkage support.

## 2. Why Deferral Is Not Rejection

These items are deferred because they are:

- structurally important;
- but too heavy to absorb cleanly into the first target-model core.

The draft keeps explicit extension hooks so these layers can be added later without re-architecting the core.

## 3. Extension Hooks Preserved

The following target constructs preserve future extensibility:

- `HierarchyNode`
- `CodeDimension / CodeValue / ItemCodeAssignment`
- `GovernanceRecord`
- `ExternalObjectLink`
- `AttributeValue`

## 4. Stage 23 Clarification

Stage 23 deepened these deferred families and confirmed that they are real subsystem classes:

- PMIS
- EDMS / CDE / document workflow
- permit / authority engine
- smart-site platform
- resource optimization engine
- payment / commercial engine

They remain deferred from the pilot core.
But they should no longer be treated as vague future possibilities.
They are now documented as named bounded contexts with explicit bridge patterns.

## 5. Draft Rule

Any future extension should plug into these generic patterns first. A dedicated subsystem should only be added where the generic pattern becomes provably insufficient.
