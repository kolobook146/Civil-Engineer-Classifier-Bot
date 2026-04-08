# Stage 13: Task and Resource Property Catalog

## Purpose

Stage 13 consolidates the task, resource, control, report, and digital properties that appear across regional schools, global institutes, and software documentation. The key result is that the property model is not one homogeneous task-field list. It is a multi-family structure.

## Main Conclusion

The property layer now clearly separates into five confirmed families:

1. `Decomposition`
2. `Document-system`
3. `Stage-gate`
4. `Report/log`
5. `Digital-governance`

This is a stronger model than the earlier task-centric seed because it explains why different regions and products expose different "must-have" fields.

## Family View

### 1. Decomposition family

Typical properties:

- task ID, name, duration, planned dates
- actual dates, remaining duration, percent complete
- predecessor/successor, relationship type, lag
- WBS assignment, WBS depth
- resource assignment, cost loading
- baseline dates and baseline duration

Main evidence:

- universal and institute layer: `SRC-A-001`, `SRC-A-031`, `SRC-A-041`, `SRC-A-044`
- software layer: `SRC-A-003`, `SRC-A-045`, `SRC-A-049`, `SRC-A-056`

Interpretation:

This family remains the backbone of scheduling, especially in U.S.-driven CPM and project-controls practice. It is strongest in Primavera P6, Primavera Cloud, Microsoft Project, and Deltek Open Plan.

### 2. Document-system family

Typical properties:

- schedule sheet / template reference
- schedule source file / import origin
- custom calendar selection
- note category
- sheet-level role assignment
- governed container linkage

Main evidence:

- regional base: CIS `POS/PPR` and China construction organization design (`SRC-A-026`, `SRC-A-033`)
- software layer: `SRC-A-047`, `SRC-A-048`, `SRC-A-052`, `SRC-A-055`

Interpretation:

The schedule is often not just a table of tasks. It may live inside a governed planning document, schedule sheet, or template hierarchy. This family is especially important for CIS and China alignment, and in software it is clearest in Unifier and Asta.

### 3. Stage-gate family

Typical properties:

- deliverable reference
- assumption / constraint reference
- approval / permit reference
- procurement package reference
- phase / stage field
- work-plan or acceptance-plan linkage

Main evidence:

- institute layer: `SRC-A-037`, `SRC-A-038`, `SRC-A-039`, `SRC-A-042`
- EU public-delivery layer: `SRC-A-028`, `SRC-A-029`, `SRC-A-030`
- software layer: `SRC-A-064`, `SRC-A-065`, `SRC-A-070`

Interpretation:

This family is much stronger in project-delivery models than in pure production scheduling. It links the schedule to project authorization, deliverable acceptance, procurement, and phase exits.

### 4. Report/log family

Typical properties:

- narrative / update comment
- status-report linkage
- issue / change / decision log linkage
- version summary / change summary
- root cause of delay
- audit timestamp / actor / changed value
- note category

Main evidence:

- institute layer: `SRC-A-037`, `SRC-A-042`
- software layer: `SRC-A-057`, `SRC-A-058`, `SRC-A-059`, `SRC-A-063`

Interpretation:

Software documentation strongly confirms that reporting and logging are not just external outputs. They are embedded properties and object relationships inside the scheduling environment.

### 5. Digital-governance family

Typical properties:

- digital archive / project code reference
- item reference / linked object ID
- external document hyperlink
- import-source reference
- role assignment
- resource-group reference

Main evidence:

- China digital layer: `SRC-A-034`, `SRC-A-043`
- software layer: `SRC-A-058`, `SRC-A-060`, `SRC-A-073`, `SRC-A-075`

Interpretation:

This family becomes dominant when the schedule is embedded in a platform that also stores models, drawings, issues, inspections, and digital supervision records.

## What Software Documentation Added

The software stage materially expanded the property model:

- `Primavera Cloud` added configured fields, formula fields, codes, roles, work packages, locations, and synchronized object boundaries.
- `Unifier` added sheet-centric governance, audit behavior, and governed schedule containers.
- `Microsoft Project` strengthened custom fields, formulas, lookup tables, WBS coding, and readable WBS-based predecessor logic.
- `Asta Powerproject` added work-pattern and custom-table depth.
- `Deltek Open Plan / PM Compass` strengthened control-account, work-package, and structured note mapping.
- `Autodesk Build` added commitment state, `Percent Plan Complete (PPC)`, root causes for delay, linked objects, and version comparison.
- `Procore` added calendar items, lookahead-facing schedule use, editable constraints, and collaborative grouping views.
- `Zoho`, `Backlog`, `Glodon`, and `TAPD` widened the model toward configurable schemas, issue-parent structures, linked digital objects, and platform integration.

## Regional and Institute Reconciliation

### CIS

The property catalog now explains why CIS scheduling cannot be represented only by activity fields. `POS`, `PPR`, and organization-of-work artifacts require document-container and planning-basis properties in addition to task math.

### EU

The EU and institute layer pushes the catalog toward stage, authorization, deliverable, checklist, and report-linked properties. This is closer to a governed delivery model than to a site-only production model.

### USA

The U.S. layer remains the strongest for decomposition, control, baseline, quality, and control-account linked properties.

### China

China is the strongest source for digital archive and digital-governance properties, especially when combined with Glodon and MOHURD digital sources.

### Global institutes

- `PMI` reinforces decomposition properties.
- `AACE` reinforces control and statusing properties.
- `PM²` reinforces artefact-linked and stage-gate properties.
- `FIDIC` reinforces contract-event and delivery-process properties.
- `GAO` reinforces traceability, completeness, and integrity properties.

## Result

The working property catalog now spans `PRP-001` to `PRP-065`. The important shift is not only catalog growth. It is the recognition that different property clusters belong to different schedule grammars and therefore should not be forced into one flat generic task schema too early.
