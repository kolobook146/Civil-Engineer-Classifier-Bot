# Stage-Function Model

Status: central business model, working draft.

## Purpose

This document defines the core semantic relationship between `function` and `stage`.
It is the most important business model in the pilot because it provides the common coordinate system for both schedule tasks and recorded facts.

## Core Definitions

### Function

`Function` is the functional workstream of the project.
It answers the question:
`What is being delivered, managed, or advanced?`

A function is a stable management or delivery stream, not a single event and not a task status.

Examples:
- Project Management & Controls
- Permits & Authority Approvals
- Design Management
- Material & Technical Supply
- Construction Execution

### Stage

`Stage` is the lifecycle gate within a function.
It answers the question:
`Where is this function right now in its process?`

A stage is a standardized process position that can be reused across different functions.
It is not a progress percentage and not a generic completion status.

Examples:
- Initial data
- Technical brief
- Approvals
- Tender
- Contract
- Design and survey works
- Advance payment
- Procurement
- Execution
- Control
- Closeout & Handover

## Matrix Logic

The schedule model uses a matrix-style interpretation:

- `function` = horizontal business/workstream dimension
- `stage` = lifecycle/process dimension within that workstream

Together they form the core semantic coordinate of a task or fact.

This means:
- one function can pass through multiple stages;
- one stage can appear inside multiple functions;
- not every function must use every stage;
- the same stage name may have different practical content depending on the function, but the lifecycle meaning remains comparable.

## Why This Model Matters

The project is not only about construction activities.
It includes broader investment and delivery processes such as:
- land and permits,
- design,
- expert review,
- procurement,
- contracting,
- construction,
- commissioning.

A single list of work types is not enough to describe this project model.
The schedule therefore needs a workstream axis (`function`) and a lifecycle axis (`stage`).

## Difference Between Function, Stage, and Work Type

### Function

Represents the project workstream.
Examples:
- Design Management
- Construction Execution

### Stage

Represents the lifecycle gate within that workstream.
Examples:
- Tender
- Procurement
- Execution

### Work Type

Represents the physical construction scope.
Examples:
- Concreting
- Roofing
- Electrical Installation Works

## Practical Example

The phrase `Pouring 120 m3 of concrete` should not be modeled only as `Concreting`.
A business-complete interpretation is:
- `function` = Construction Execution
- `stage` = Execution
- `work_type` = Concreting

The phrase `Tender package for ventilation equipment issued` should not be modeled as a construction work type.
A business-complete interpretation is:
- `function` = Material & Technical Supply
- `stage` = Tender
- `work_type` = empty

## Common Project Processes in the Matrix

General project processes are not secondary notes. They are first-class schedule streams.
This means design, permits, procurement, approvals, payments, and handover should live in the same matrix logic as construction work.

Examples:
- `Permits & Authority Approvals` + `Approvals`
- `Design Management` + `Design and survey works`
- `Material & Technical Supply` + `Advance payment`
- `Commissioning & Handover` + `Closeout & Handover`

## Pilot Interpretation Rules

1. Every structured fact must have one `function`.
2. Every structured fact must have one `stage`.
3. `function` and `stage` must be selected from dictionaries only.
4. New values must not be invented outside dictionaries.
5. `work_type` may remain empty if evidence is weak or the event is not a physical construction scope.
6. `work_type` refines the scope but does not replace the `function`-`stage` coordinate.

## Interpretation of the Current Stage Set

The current pilot stage list is intentionally broad and reusable across multiple functions.
Some stages are classical process stages, while others act as control or business gates.

Important examples:
- `Advance payment` is treated as a project/business gate, not just a financial note.
- `Control` is treated as a distinct control stage, not merely a generic status.
- `Closeout & Handover` represents the completion and transfer logic of the function.
- `Design and survey works` currently acts as the pilot label for the documentation-development stage across functions that require formal deliverables or technical packages.

## Business Consequence

The pair `function + stage` is the minimum business coordinate of the model.
Without it, facts cannot be reliably placed into the project matrix and later connected to the schedule logic.
