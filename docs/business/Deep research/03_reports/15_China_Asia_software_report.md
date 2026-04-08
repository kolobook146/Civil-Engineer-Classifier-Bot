# Stage 15: China and Asia Software Report

## Scope and Method

This report profiles five China and Asia products or ecosystems using official and openly inspectable documentation. The main analytical caution is that documentation depth is uneven. In several products, ecosystem and workflow visibility is stronger than exact field-schema visibility.

Profiled set:

1. Glodon digital construction ecosystem
2. 8Manage PPM / PMO
3. Zoho Projects
4. Backlog
5. TAPD

Supplementary watchlist:

- Teambition

## Product Profiles

### 1. Glodon digital construction ecosystem

Primary sources: `SRC-A-072`, `SRC-A-073`, `SRC-A-074`

Observed model:

- digital construction platform rather than a narrow standalone scheduler;
- strong linkage among locations, drawings, BIM models, issues, checklists, workflows, notifications, and reporting;
- tracks time, resources, and trade performance within a broader platform context.

Research interpretation:

Glodon is the strongest software-side confirmation of the China digital-governance layer already visible in MOHURD sources. It is especially important for linked-object, location-tree, and digital site-control modeling.

### 2. 8Manage PPM / PMO

Primary sources: `SRC-A-070`, `SRC-A-071`

Observed model:

- official brochures indicate project charter, scope baseline, portfolio/project governance, and commitment-management orientation;
- stronger PMO and governance narrative than raw field-schema publication.

Research interpretation:

8Manage fits the Asia governance-heavy planning family. It appears closer to a PMO-integrated portfolio/project system than to a pure site-production scheduler. Confidence is medium because public technical schema detail is thin.

### 3. Zoho Projects

Primary sources: `SRC-A-063`, `SRC-A-064`, `SRC-A-065`, `SRC-A-066`

Observed model:

- clear WBS hierarchy of milestone -> task list -> task;
- baselines, slippage/variance, and configurable phase fields are explicitly documented;
- dependency settings are openly described.

Research interpretation:

Zoho is the strongest Asia-origin SaaS source in the corpus for openly inspectable decomposition plus configurable schema. It is not construction-specific, but it is structurally informative.

### 4. Backlog

Primary sources: `SRC-A-067`, `SRC-A-068`, `SRC-A-069`

Observed model:

- planning represented through issue, parent issue, versions/milestones, categories, and custom fields;
- Gantt view and CSV import schema are open and practical.

Research interpretation:

Backlog shows a different planning grammar: issue-centric and milestone-centric rather than classical CPM-centric. This is valuable because real project software in Asia does not always expose planning through a heavyweight schedule table.

### 5. TAPD

Primary sources: `SRC-A-075`, `SRC-A-076`

Observed model:

- strong open-platform and integration stance;
- release notes indicate schedule-related evolution such as predecessor-successor events and related configuration behavior;
- public open evidence is stronger for platform extensibility than for one stable schedule schema.

Research interpretation:

TAPD is most valuable as evidence for open-platform and digital-governance capability. It is less useful than Zoho or Oracle for field-by-field schedule schema extraction.

## Cross-Product Interpretation

### Asia software archetypes

#### Platform and ecosystem layer

Products:

- Glodon
- TAPD

Traits:

- stronger on linked objects, integrations, workflows, and digital context;
- weaker on openly published raw field schemas.

#### Governance and PMO layer

Products:

- 8Manage

Traits:

- stronger on project/portfolio governance, charter, baseline, PMO logic;
- weaker on openly inspectable data-field depth.

#### Lightweight explicit SaaS schema layer

Products:

- Zoho Projects
- Backlog

Traits:

- clearer open documentation for hierarchy, fields, baselines, categories, import schema;
- less construction-specific, but highly useful for explicit object and field comparison.

## Comparison with the Regional Base

### China

The software layer strongly reinforces the previously identified China dual-track model:

- legacy organization and planning standards;
- digital supervision and linked-object platform logic.

Glodon is especially important because it operationalizes the digital-governance direction signaled by `SRC-A-034` and `SRC-A-043`.

### Wider Asia

The wider Asia software layer shows more heterogeneity than the U.S. enterprise-scheduler layer:

- less one shared CPM grammar;
- more platform, SaaS, PMO, and issue-centric planning forms;
- more uneven documentation depth.

## Confidence Rule

The Asia software findings should be read with two separate confidence dimensions:

- `capability confidence`: what the platform clearly says it can do;
- `field-schema confidence`: how precisely open docs expose entities, fields, and coding rules.

This distinction is necessary to avoid false precision when public documentation is product-marketing-heavy or ecosystem-heavy.

## Watchlist Note

Teambition (`SRC-A-077`) publicly confirms Gantt chart, milestone management, risk management, resource management, and automation. However, the open technical schema is too thin for a full deep profile in this pass.
