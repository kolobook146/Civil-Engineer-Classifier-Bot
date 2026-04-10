# Fact Model

Status: normative Stage 22 fact business model.

## Purpose

This document defines the business model of a confirmed fact received through the Telegram workflow.
A fact is the smallest persisted unit of operational evidence about project progress, event occurrence, or control signal.

## Core Principle

Facts are evidence first.
They do not become schedule structure automatically.

Stage 22 therefore distinguishes between:

1. `data_facts`
   The immutable confirmed evidence register.

2. Normalized schedule-facing interpretation
   The later business use of evidence as progress or governance input for schedule logic.

## What a Fact Is

A fact is:

- derived from a free-form human message;
- structured by the pilot workflow;
- confirmed before persistence;
- preserved as evidence with its original text and context.

## What a Fact Is Not

A fact is not automatically:

- a schedule item;
- a baseline update;
- a schedule version;
- a full issue-management workflow;
- a full site diary;
- a PMIS record replacement.

## Current Persisted Fact Structure

The current pilot persists the following fields in `data_facts`:

- `raw_text`
- `volume`
- `unit`
- `work_type`
- `stage`
- `function`
- `comment`
- `timestamp`
- `user_id`
- `chat_id`
- `message_id`
- `model`
- `classifier_version`
- `status`

This is the current evidence-sheet representation.
It remains valid in Stage 22.

## Current Pilot Bot Convention

The current pilot also accepts one explicit bot convention for non-physical schedule items:

- when the bot reports completion evidence for a non-physical row, it writes `volume = 1`;
- the fact still keeps the same core coordinate:
  - `function`
  - `stage`
  - optional `work_type`
  - `unit`, including the accepted blank-unit case;
- this lets non-physical rows participate in the same formula-fed `Actual Quantity` bridge as physical rows.

Under this convention:

- `volume = 1` is not a physical quantity;
- it is a binary completion marker for the current pilot only.

## Recommended Business Interpretation of Facts

Stage 22 interprets persisted facts as belonging to one of these business families:

1. physical progress
2. actual start or finish
3. design, permit, or approval event
4. procurement or supply event
5. issue, change, or decision signal
6. payment or contract event
7. control, KPI, or inspection signal
8. readiness, completion, or handover event

The current pilot may not store `fact_kind` as a separate column yet, but the business model should interpret facts through one of these families.

## Mandatory Fact Coordinates

Every persisted fact must keep:

- `raw_text`
- `function`
- `stage`
- `timestamp`
- `status`

Where available, a fact should also keep:

- `volume`
- `unit`
- `work_type`
- relevant residual `comment`

## Why `Function` and `Stage` Stay Mandatory

The fact register is not only a text archive.
It is the evidence layer of the same business matrix used by the schedule.

Without `function + stage`, the fact cannot be safely aligned with schedule meaning later.

## Fact Atomicity

One fact should ideally describe:

- one meaningful progress event;
- one control event;
- or one tightly related cluster of evidence about the same business occurrence.

The pilot accepts free-form text, but the strongest evidence quality comes from one message describing one fact.

## Fact Status and Trust

Facts move through operational states such as:

- received
- queued
- processed
- processed with fallback
- processed from queue
- processed from queue with fallback

These are not schedule statuses.
They are evidence-processing statuses.

## Relationship to the Schedule Model

Later, a fact may be used to:

- support a `ProgressRecord`;
- support a `GovernanceRecord`;
- strengthen an external traceability link;
- stay informational if no safe schedule mapping exists.

This means the same fact register supports schedule intelligence without becoming the schedule itself.

## Current Stage 22 Boundary

The current pilot keeps `data_facts` as the operational source evidence layer.
It does not yet require:

- automatic schedule mutation;
- a separate stored normalized fact table;
- a full PMIS-style event engine.

Those are later extensions, not prerequisites of the Stage 22 business model.

The current pilot also does not require:

- a separate completion-flag column;
- a dedicated fact-to-task identity field;
- a full event-type taxonomy inside `data_facts`.

Instead, the current workbook may derive:

- `Actual Start` from the earliest matching fact date;
- `Actual Finish` from the latest matching fact date once the completion rule is met.
