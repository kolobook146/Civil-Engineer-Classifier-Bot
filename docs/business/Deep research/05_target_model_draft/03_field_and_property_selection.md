# Field and Property Selection

## Purpose

This document narrows the broad research property universe into a target-model field set for the draft stage.

## 1. Field Selection Levels

- `Mandatory`
- `Recommended`
- `Extension-ready`
- `Deferred`

## 2. Mandatory Core Fields

### Schedule

- `schedule_id`
- `context_type`
- `schedule_purpose`
- `contour_scope`
- `status`
- `default_calendar_id`
- `source_system`

### ScheduleVersion

- `schedule_version_id`
- `schedule_id`
- `version_no`
- `version_role`
- `status_date`
- `published_at`
- `change_summary`
- `source_file_ref`

### ScheduleItem

- `schedule_item_id`
- `schedule_version_id`
- `lineage_key`
- `name`
- `item_kind`
- `contour`
- `stream`
- `planned_start`
- `planned_finish`
- `duration`
- `actual_start`
- `actual_finish`
- `remaining_duration`
- `percent_complete`
- `status`
- `calendar_id`
- `primary_hierarchy_node_id`

### Dependency

- `dependency_id`
- `predecessor_item_id`
- `successor_item_id`
- `relationship_type`
- `lag`
- `dependency_scope`

### ProgressRecord

- `progress_record_id`
- `schedule_item_id`
- `status_date`
- `percent_complete`
- `remaining_duration`
- `source_system`
- `evidence_ref`

## 3. Recommended Fields

### ScheduleItem recommended

- `constraint_type`
- `constraint_date`
- `responsibility_ref`
- `deliverable_ref`
- `approval_ref`
- `procurement_package_ref`
- `wbs_level`
- `critical_flag`

### ResourceAssignment recommended

- `resource_type`
- `resource_ref`
- `resource_group_ref`
- `units`
- `productivity_assumption`
- `cost_loading_ref`

### GovernanceRecord recommended

- `record_type`
- `record_date`
- `status`
- `summary`
- `linked_item_id`
- `linked_version_id`
- `linked_external_id`

### ExternalObjectLink recommended

- `external_system`
- `object_type`
- `external_object_id`
- `link_role`
- `link_status`

## 4. Extension-Ready Fields

These should not be mandatory in the draft, but the model should support them without redesign:

- configured custom attributes;
- formula-backed attributes;
- lookup-backed attributes;
- KPI period fields;
- completion certificate references;
- professional qualification status;
- permit-platform transaction state;
- issue root-cause classification;
- version comparison metadata;
- PMIS workflow state.

## 5. Deferred Fields

These are intentionally deferred from the target core:

- detailed resource-curve logic;
- full earned-value calculation engine;
- detailed payment-certificate engine;
- deep permit-workflow status machine;
- full document revision lifecycle engine;
- authority qualification scoring formulas.

## 6. Selection Rationale

The draft field set favors:

- universality;
- cross-region compatibility;
- enterprise and PMIS relevance;
- software-compatible extensibility.

It intentionally avoids turning the first target model into a full PMIS or ERP replacement.
