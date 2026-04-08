# Fact Linkage Draft

## Purpose

This draft defines how schedule structure should connect to factual project signals in the target model.

## 1. Main Principle

Facts should be linked to schedule without destroying schedule lineage.

This means:

- schedule structure lives in `Schedule`, `ScheduleVersion`, `ScheduleItem`, and related entities;
- factual state lives in `ProgressRecord`, `GovernanceRecord`, and `ExternalObjectLink`;
- baseline and fact layers remain distinguishable.

## 2. Fact Families to Support

The target model should support at least these fact families:

- progress facts;
- actual start / finish facts;
- quantity or work-complete signals;
- resource and crew facts where available;
- cost and expenditure linkage where available;
- approval and permit status facts;
- issue, change, and decision facts;
- payment and contractual-event facts;
- completion, readiness, and handover facts;
- KPI and performance-review facts.

## 3. Preferred Matching Order

Facts should match to schedule using this priority:

1. `lineage_key` on `ScheduleItem`
2. `ExternalObjectLink`
3. hierarchy plus code tuple
4. fallback review queue for unresolved matches

This preserves both precision and auditability.

## 4. Selected Fact-Carrying Entities

| Entity | Fact role |
| --- | --- |
| `ProgressRecord` | Time-stamped operational progress state |
| `GovernanceRecord` | Status, issue, change, KPI, approval, completion, authority, and review facts |
| `ExternalObjectLink` | Traceability to source systems and evidence objects |

## 5. Required Traceability Fields

Every fact-like record should carry:

- `source_system`
- `source_record_id` or external object reference
- `record_timestamp`
- `effective_date` or `status_date`
- `evidence_ref` where available
- `ingestion_or_capture_mode`

## 6. Relationship to PMIS and External Systems

The target model is not trying to absorb whole external systems. Instead:

- PMIS remains a source-of-truth for some operational states;
- BIM, EDMS, permit, issue, and authority systems remain external;
- the target model stores enough linkage and normalized fact structure to support schedule intelligence and business logic.

## 7. Draft Fact-Linkage Rules

### Rule 1

Actual dates must be stored as facts linked to a schedule item and status date, not only as mutable latest values.

### Rule 2

Issue, change, approval, and completion facts should be represented as typed governance records even if their detailed workflow remains external.

### Rule 3

PMIS or authority records should be linkable without forcing their internal schema into the schedule core.

### Rule 4

Unmatched facts should remain visible in an exception queue rather than being silently dropped.

## 8. Draft Outcome

The target model will support fact linkage as a first-class concern from the start, but through a controlled normalization layer rather than a monolithic enterprise data copy.
