# Decision Traceability Matrix

## Purpose

This matrix shows how the Stage 21 target-model draft is derived from:

- the Stage 19 comparative synthesis;
- the Stage 20 assembled package;
- the underlying registry and report corpus.

It is not a source registry replacement. It is the design-traceability layer for the target-model draft.

## Interpretation Rule

- `Stage 19 anchors` identify the main synthesis rows that materially drove the decision.
- `Stage 20 package anchors` identify the assembled reading paths used to interpret the synthesis.
- `Target-model landing zone` shows where the decision lives in the Stage 21 draft.
- `Decision class` distinguishes `core`, `configurable`, and `deferred`.

## Matrix

| Decision ID | Target-model decision | Stage 19 anchors | Stage 20 package anchors | Target-model landing zone | Decision class | Why this decision was selected |
| --- | --- | --- | --- | --- | --- | --- |
| `TM-001` | Use one hybrid schedule model rather than a task-only CPM file or a document-only system. | `IMP-001`, `IMP-005`, `SYN-003`, `SYN-004`, `SYN-005`, `SYN-006` | `01_narrative_report.md` sections 3, 5, 7; `02_comparative_matrix_pack.md` | `01_target_business_model_draft.md` sections 2, 7, 10 | `core` | Comparative evidence showed that no single region or software grammar covers the whole schedule universe. |
| `TM-002` | Keep `production`, `delivery`, and `cross-project` as explicit contours. | `PD-001`, `PD-003`, `PD-004`, `IMP-004` | `01_narrative_report.md` sections 3-4; `03_catalog_pack.md` | `01_target_business_model_draft.md` sections 4, 6; `04_coding_lod_and_rule_draft.md` rule set | `core` | The research repeatedly showed two overlapping schedule universes plus shared governance processes. |
| `TM-003` | Separate `ScheduleVersion` from `BaselineDesignation`. | `UNI-001`, `SYN-002`, `SYN-006`, `DIV-001` | `01_narrative_report.md` sections 2, 6-7; `04_software_report_pack.md` | `01_target_business_model_draft.md` section 3; `04_coding_lod_and_rule_draft.md` rules A-B | `core` | USA, Middle East, and software evidence all require version discipline distinct from baseline designation. |
| `TM-004` | Use one unified `ScheduleItem` with typed semantics instead of separate task, gate, payment, and handover engines. | `UNI-001`, `REG-002`, `DIV-002`, `PD-001` | `03_catalog_pack.md`; `01_narrative_report.md` sections 3, 6-7 | `01_target_business_model_draft.md` sections 3-5; `02_entity_selection_and_mapping.md` sections 2-4 | `core` | A typed item model preserves universality while still supporting delivery-governance and non-physical schedule objects. |
| `TM-005` | Keep hierarchy separate from coding. | `PD-002`, `REG-001`, `REG-002`, `IMP-003` | `03_catalog_pack.md`; `02_comparative_matrix_pack.md` | `01_target_business_model_draft.md` principle 2; `04_coding_lod_and_rule_draft.md` sections 1-5 | `core` | Regional evidence showed that roll-up structures and classification layers vary independently and cannot be collapsed safely. |
| `TM-006` | Support multiple hierarchy types through one `HierarchyNode` pattern. | `PD-002`, `REG-001`, `REG-002`, `SYN-004`, `SYN-005` | `03_catalog_pack.md`; `01_narrative_report.md` sections 3-5 | `01_target_business_model_draft.md` sections 3, 8; `04_coding_lod_and_rule_draft.md` section 1 | `core` | The model must represent WBS, stage, package, location/system, handover, and document-container structures together. |
| `TM-007` | Use configurable code dimensions rather than a single hard-coded task-code list. | `UNI-002`, `LAY-003`, `DIG-001`, `IMP-005` | `03_catalog_pack.md`; `04_software_report_pack.md` | `01_target_business_model_draft.md` section 3; `04_coding_lod_and_rule_draft.md` section 2 | `configurable` | Code families differ by region, client, and software; configurability is safer than cloning one vendor grammar. |
| `TM-008` | Promote `GovernanceRecord` to a first-class entity. | `LAY-002`, `DIV-003`, `DIV-004`, `REG-002` | `01_narrative_report.md` sections 6-7; `03_catalog_pack.md` | `01_target_business_model_draft.md` sections 3, 5, 6; `05_fact_linkage_draft.md` sections 2, 4, 7 | `core` | Enterprise and delivery layers depend on approvals, issues, change, KPI, completion, and review facts that are stronger than free-text notes. |
| `TM-009` | Promote `ExternalObjectLink` to a first-class entity. | `LAY-003`, `DIG-001`, `DIV-005`, `SYN-005`, `SYN-006`, `SYN-007` | `04_software_report_pack.md`; `03_catalog_pack.md`; `05_source_register_pack.md` | `01_target_business_model_draft.md` sections 3, 5, 6; `05_fact_linkage_draft.md` sections 4-7 | `core` | The live schedule sits inside a wider ecosystem of PMIS, BIM, EDMS, permit, smart-site, and authority records. |
| `TM-010` | Preserve configurable extension fields through `AttributeValue`. | `LAY-003`, `IMP-005`, `SYN-007`, `SYN-008` | `04_software_report_pack.md`; `03_catalog_pack.md` | `01_target_business_model_draft.md` sections 3, 5; `03_field_and_property_selection.md` sections 3-4 | `configurable` | Software evidence repeatedly showed configured fields as a durable pattern; this prevents schema explosion in the pilot. |
| `TM-011` | Normalize facts into `ProgressRecord` and `GovernanceRecord` rather than overwriting structure. | `DIV-003`, `DIV-005`, `PD-003`, `IMP-002` | `01_narrative_report.md` sections 2, 6-8; `03_catalog_pack.md`; `04_software_report_pack.md` | `03_field_and_property_selection.md`; `05_fact_linkage_draft.md` | `core` | This preserves lineage, statusing history, and auditability while keeping source-system signals distinguishable from schedule structure. |
| `TM-012` | Use one canonical LOD ladder with regional crosswalks. | `PD-002`, `SYN-002`, `SYN-004`, `SYN-005`, `SYN-006` | `01_narrative_report.md` sections 3-5; `03_catalog_pack.md`; `02_comparative_matrix_pack.md` | `01_target_business_model_draft.md` section 8; `04_coding_lod_and_rule_draft.md` section 3 | `core` | Regional LOD grammars differ, but the model still needs one usable implementation crosswalk. |
| `TM-013` | Represent `POS`, `PPR`, construction-organization, and schedule sheets through hierarchy, governance, and links rather than dedicated core engines. | `REG-001`, `LAY-003`, `IMP-003`, `IMP-005` | `03_catalog_pack.md`; `01_narrative_report.md` sections 4-7 | `01_target_business_model_draft.md` section 5; `02_entity_selection_and_mapping.md` sections 4-5 | `configurable` | The evidence confirms their importance, but a direct subsystem clone would overfit the pilot and increase complexity too early. |
| `TM-014` | Defer full PMIS, EDMS, permit, authority, smart-site, resource-optimization, and payment engines. | `IMP-001`, `IMP-002`, `IMP-005`, `DIV-005` | `01_narrative_report.md` sections 7-8; `04_software_report_pack.md`; `05_source_register_pack.md` | `01_target_business_model_draft.md` section 9; `06_deferred_extensions.md` | `deferred` | These layers are structurally important but too heavy to absorb as first-class subsystems in the initial target business core. |

## Main Outcome

The Stage 21 draft is therefore traceable in both directions:

- from synthesis to target-model choice;
- from target-model choice back to comparative evidence and package reading paths.

This keeps the target model grounded in research rather than in a single regional habit, enterprise template, or software product.
