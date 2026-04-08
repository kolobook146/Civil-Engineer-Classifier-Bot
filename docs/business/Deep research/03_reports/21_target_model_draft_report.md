# Stage 21: Target Model Draft Report

## Purpose

Stage 21 converts the research corpus into a practical target-model draft for the project.

## Main Result

The draft is assembled in:

- `05_target_model_draft/`

The target model chosen in this stage is:

- hybrid rather than task-only;
- governance-aware rather than date-only;
- configuration-first rather than region-hard-coded;
- extensible rather than software-clone-specific;
- practical enough for implementation without reproducing a full PMIS platform.

## Core Draft Components

- target business model draft;
- entity selection and mapping;
- field and property selection;
- coding, LOD, and core rule draft;
- fact-linkage draft;
- deferred extension log;
- decision traceability matrix.

## Main Design Choice

The chosen draft uses a relatively small set of core entities:

- `Schedule`
- `ScheduleVersion`
- `BaselineDesignation`
- `ScheduleItem`
- `Dependency`
- `Calendar`
- `HierarchyNode`
- `CodeDimension / CodeValue / ItemCodeAssignment`
- `ResourceAssignment`
- `ProgressRecord`
- `GovernanceRecord`
- `ExternalObjectLink`
- `AttributeValue`

This is the main Stage 21 compression move: broad enough to preserve the comparative evidence, small enough to remain implementable.

## Comparative Rationale

The draft directly reflects Stage 19 conclusions:

- USA and Middle East anchor enterprise governance and baseline discipline.
- CIS and China prevent a flat task-only model and force document-system and digital-governance support.
- EU forces stage-gate, package, and handover support.
- software evidence forces version, link, configured-field, and audit-friendly structures.

## Traceability Layer

The Stage 21 folder now includes an explicit decision-to-evidence mapping:

- `05_target_model_draft/07_decision_traceability_matrix.md`

This file is the shortest path for checking whether a target-model choice is:

- directly grounded in Stage 19 synthesis rows;
- supported by the Stage 20 assembled package;
- intentionally chosen as `core`, `configurable`, or `deferred`.

## Draft Boundary

Stage 21 intentionally stops short of:

- full PMIS workflow design;
- full permit and authority workflow design;
- full EDMS platform design;
- full payment-management or smart-site platform design.

These are logged as deferred extensions.

## Result

The project now has a first explicit target-model draft derived from comparative evidence rather than inherited intuition. This creates the correct handoff point for Stage 22 formalization into project business documentation.
