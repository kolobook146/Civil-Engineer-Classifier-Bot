# Comparative Matrix Template

This document defines the comparison schema to be reused across regions, standards, schools, and software systems.

## 1. Region / School / Standard Matrix

| Field | Description |
| --- | --- |
| `comparison_id` | Unique row ID. |
| `scope_group` | Universal, International, CIS, EU, USA, China, Software, Academic, Cross-project. |
| `curator_zone` | Organization or governance zone behind the practice. |
| `country_or_jurisdiction` | Country, region, or international body. |
| `source_id` | Reference to the source registry. |
| `source_level` | A, B, or C. |
| `practice_family` | CPM, contract governance, owner controls, EPC controls, academic model, etc. |
| `schedule_type` | Master, phase, detailed, engineering, procurement, commissioning, look-ahead, delivery, etc. |
| `application_domain` | Production, delivery, contract admin, PMO, claims, resource planning, etc. |
| `project_phase` | Development, design, procurement, construction, commissioning, closeout. |
| `management_level` | Executive, program, project, contract, site, workfront, crew. |
| `planning_horizon` | Long-range, phase, detailed, rolling wave, look-ahead, daily/weekly control. |
| `level_of_detail_model` | How the source describes decomposition or schedule levels. |
| `core_entities` | Main entities explicitly present. |
| `cross_project_processes` | Non-SMR processes included in schedule logic. |
| `coding_structures` | WBS, OBS, CBS, location codes, system codes, etc. |
| `resource_model` | Resource loading, leveling, crews, materials, equipment, subcontractors. |
| `cost_schedule_integration` | Whether and how cost interacts with schedule. |
| `baseline_actual_logic` | Baseline, actuals, status date, progress update logic. |
| `governance_logic` | Review, approval, acceptance, contractual requirements, schedule specs. |
| `notes` | Short analytical note. |

## 2. Software Product Matrix

| Field | Description |
| --- | --- |
| `software_row_id` | Unique row ID. |
| `product_name` | Product name. |
| `vendor` | Vendor or maintainer. |
| `curator_zone` | Country or zone of product governance. |
| `deployment_model` | Desktop, cloud, hybrid, enterprise suite. |
| `primary_market` | Construction, EPC, general PM, infrastructure, owner side, etc. |
| `activity_model` | Core task/activity representation. |
| `dependency_model` | Relationship types, inter-project links, lag/lead support. |
| `calendar_model` | Project, resource, shift, exception calendars. |
| `resource_model` | Labor, equipment, material, crews, roles, costs. |
| `baseline_model` | Number and handling of baselines. |
| `actuals_model` | Actual dates, remaining duration, percent complete, status date. |
| `coding_model` | WBS, OBS, activity codes, custom fields, tags. |
| `lod_support` | Multi-level scheduling support. |
| `reporting_model` | Native reports, dashboards, export surfaces. |
| `strong_sides` | What the product is structurally good at. |
| `limitations` | Known model constraints or implementation caveats. |
| `source_ids` | Supporting source IDs. |

## 3. Entity / Rule Traceability Matrix

| Field | Description |
| --- | --- |
| `trace_id` | Unique row ID. |
| `item_type` | Entity or Rule. |
| `item_id` | Entity ID or Rule ID. |
| `item_name` | Canonical item name. |
| `source_id` | Source where it appears. |
| `representation` | Task, field, code, document, procedure, calculation, view, etc. |
| `mandatory_or_optional` | Mandatory, common, optional, inferred. |
| `context` | Production, delivery, contract, software, academic, oversight. |
| `notes` | Trace note. |

## 4. Minimal Comparison Rules

- One source may generate multiple comparison rows.
- One row should capture one meaningful unit of comparison.
- If a source spans several schedule types, split the row.
- If a software product has materially different models in desktop and cloud products, separate them.
- If an item is inferred rather than explicit, mark it in `notes`.
