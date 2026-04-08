# Extension Architecture

Status: normative post-Stage-23 extension-boundary note.

## Purpose

This document records the heavy project subsystems that were researched after Stage 22 but remain outside the current pilot core.
Its role is to prevent two opposite mistakes:

- pretending these subsystems do not exist;
- prematurely absorbing them into the pilot schedule model.

## Named Extension Families

The project now recognizes the following bounded extension families:

1. `PMIS`
2. `EDMS / CDE / document workflow`
3. `permit / authority engine`
4. `smart-site platform`
5. `resource optimization engine`
6. `payment / commercial engine`

## Normative Position

These families are structurally important.
They are not rejected.
They are also not part of the mandatory pilot core.

The current normative position is:

- keep the pilot core hybrid and bounded;
- treat these families as external bounded systems;
- connect to them through controlled bridge patterns;
- promote a family into a dedicated subsystem only when pilot evidence proves the generic bridge insufficient.

## Bridge Patterns Preserved in the Current Model

The current project model should connect to extension families through:

- `GovernanceRecord`
- `ExternalObjectLink`
- `CodeDimension / CodeValue / ItemCodeAssignment`
- `HierarchyNode`
- `AttributeValue`

These are bridge patterns, not placeholders for unlimited ad hoc schema growth.

## What the Core May Store

The current core may store:

- extension-related schedule items such as permit events, payment events, review gates, or control events;
- governance outcomes such as approvals, holds, reviews, KPI signals, and comment resolutions;
- external record identity and reference context;
- selected coded context such as package, authority, responsibility, or document class.

## What the Core Must Not Try to Recreate

The current core must not try to recreate:

- full PMIS workflow runtime;
- full EDMS revision and transmittal engine;
- full regulatory case-management engine;
- full smart-site telemetry and alert engine;
- full cross-project resource balancing engine;
- full billing, compliance, hold, and disbursement engine.

## Promotion Trigger

A family should only be promoted beyond the current bridge model if at least one of the following becomes true:

1. pilot workflows cannot be executed safely without first-class runtime state from that family;
2. the volume or frequency of extension records makes manual bridging unreliable;
3. business decisions depend on subsystem-native state that cannot be represented faithfully through current hooks;
4. integration ambiguity creates repeated operational errors or unacceptable reconciliation work.

## Current Practical Reading

The Stage 23 research suggests the most likely future expansion order is:

1. `PMIS`
2. `EDMS / CDE`
3. `payment / commercial`
4. `permit / authority`
5. `smart-site`
6. `resource optimization`

This ordering is informative, not mandatory.
Actual promotion still depends on pilot evidence.
