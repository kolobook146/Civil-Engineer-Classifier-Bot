# Stage 15: Global Software Practice Report

## Scope and Method

This report profiles eight globally relevant scheduling or schedule-adjacent products using official and openly inspectable documentation. The selection rule was:

- high relevance to construction and project scheduling;
- strong enough open documentation to inspect entities, fields, codes, hierarchy, and governance behavior;
- not restricted to pure market share.

Profiled set:

1. Oracle Primavera P6 Professional
2. Oracle Primavera Cloud
3. Oracle Primavera Unifier Schedule Manager
4. Microsoft Project
5. Asta Powerproject
6. Deltek Open Plan
7. Autodesk Build Schedule and Workplan
8. Procore Scheduling

## Product Profiles

### 1. Primavera P6 Professional

Primary sources: `SRC-A-003`

Observed model:

- classical enterprise CPM authoring model;
- activity-centered schedule with explicit WBS, OBS, calendars, relationships, lag, baselines, and activity codes;
- strong separation between hierarchy, coding, logic, and control layers.

Research interpretation:

P6 remains the clearest reference product for the decomposition family. It is the strongest benchmark for any target model that needs industrial-strength CPM, coding depth, and enterprise controls alignment.

### 2. Primavera Cloud

Primary sources: `SRC-A-045`, `SRC-A-046`

Observed model:

- cloud-native enterprise schedule model;
- activities coexist with work packages, locations, roles, resources, rates, budgets, configured fields, codes, baselines, and risks;
- integration documentation exposes which business objects are first-class and synchronizable.

Research interpretation:

Primavera Cloud is the broadest openly inspectable object model in the current corpus. It demonstrates that modern enterprise scheduling is no longer only a network of activities; it is a configurable cloud data model with operational integration boundaries.

### 3. Primavera Unifier Schedule Manager

Primary sources: `SRC-A-047`, `SRC-A-048`

Observed model:

- schedule managed through governed schedule sheets;
- master schedule sheet can consolidate subordinate schedule sheets;
- audit and permissions behavior is visible in the help system.

Research interpretation:

Unifier is crucial because it validates the document-system family inside enterprise software. It aligns especially well with CIS and China traditions where schedules live inside governed planning-document structures.

### 4. Microsoft Project

Primary sources: `SRC-A-004`, `SRC-A-005`, `SRC-A-006`, `SRC-A-007`, `SRC-A-049`, `SRC-A-050`, `SRC-A-051`

Observed model:

- task-centered planning with mainstream CPM semantics;
- strong WBS masks, outline numbers, custom fields, formulas, and lookup tables;
- support guidance is unusually clear for configurable fields and hierarchy masks.

Research interpretation:

Microsoft Project is not the richest enterprise-controls environment in the current set, but it is one of the clearest open sources for the configurable task/WBS/field grammar that many organizations actually use.

### 5. Asta Powerproject

Primary sources: `SRC-A-052`, `SRC-A-053`, `SRC-A-054`, `SRC-A-055`

Observed model:

- contractor-oriented planning tool with strong calendar and work-pattern modeling;
- good visibility into spreadsheet fields, code libraries, baselines, and custom linked tables;
- extension model is pragmatic and data-rich.

Research interpretation:

Asta is particularly important for Stage 13-14 because its documentation exposes actual usable field inventories rather than only conceptual descriptions. It bridges production planning and practical coding better than many more generic PM tools.

### 6. Deltek Open Plan

Primary sources: `SRC-A-056`, `SRC-A-057`

Observed model:

- control-account and work-package aware planning environment;
- explicit field mapping to PM Compass and note-category mapping;
- resource scheduling and project codes are visible in the official guide.

Research interpretation:

Deltek is the strongest open source in the current corpus for cost-schedule integration structures. It materially strengthens the case for modeling control-account and work-package linkages as first-class rather than optional.

### 7. Autodesk Build Schedule and Workplan

Primary sources: `SRC-A-058`, `SRC-A-059`

Observed model:

- imported schedule plus field-facing workplan layer;
- activities can be linked to relevant platform objects;
- version compare, commitment tracking, `Percent Plan Complete (PPC)`, and root-cause metrics are explicit.

Research interpretation:

Autodesk Build is the strongest example of a collaborative production-control schedule model in the current global set. It materially expands the report/log and digital-governance families beyond classical CPM.

### 8. Procore Scheduling

Primary sources: `SRC-A-060`, `SRC-A-061`, `SRC-A-062`

Observed model:

- schedule exists both as imported schedule and editable collaborative schedule;
- support for dependencies, constraints, lookahead use, calendar items, and shared field visibility;
- stronger on collaboration and field consumption than on heavy control-account structures.

Research interpretation:

Procore reinforces the idea that real schedule practice often needs an integration shell and a field-consumption layer, not only a heavyweight authoring engine.

## Cross-Product Archetypes

### Enterprise CPM and controls

Products:

- Primavera P6
- Primavera Cloud
- Deltek Open Plan

Shared traits:

- strongest decomposition grammar;
- richest code systems;
- strongest baseline/control integration;
- better fit for owner/contractor controls and industrial EPC.

### Document-system and governed-container models

Products:

- Primavera Unifier
- Asta Powerproject

Shared traits:

- schedules live inside governed sheets, code libraries, tables, or structured planning containers;
- stronger fit for environments where planning documentation is itself governed.

### Collaborative field-planning and digital linkage

Products:

- Autodesk Build
- Procore

Shared traits:

- imported schedule coexistence with field-execution layers;
- stronger report/log, linked-object, and short-interval planning behavior;
- better visibility for teams, commitments, and practical field consumption.

### Mainstream configurable task platforms

Products:

- Microsoft Project

Shared traits:

- strong task/WBS/custom-field grammar;
- accessible support documentation;
- weaker native enterprise traceability than the heaviest controls suites.

## Best-in-Class by Dimension

| Dimension | Strongest current products | Why |
| --- | --- | --- |
| Classical CPM structure | Primavera P6, Primavera Cloud | Deepest enterprise scheduling semantics. |
| Configurable field model | Primavera Cloud, Microsoft Project | Strong configured fields, formulas, lookup behavior. |
| Cost-schedule integration signals | Deltek Open Plan, Primavera Cloud | Stronger explicit control-account and mapped field logic. |
| Sheet / governed-container model | Primavera Unifier | Best explicit schedule-sheet governance model. |
| Calendar and work-pattern depth | Asta Powerproject | Best open evidence of rich calendar/work-pattern handling. |
| Report / log / version governance | Autodesk Build, Unifier | Explicit versioning, audit, change summaries, and governed updates. |
| Collaborative production control | Autodesk Build, Procore | Strongest field-facing schedule execution layer. |
| Mainstream WBS/custom-field clarity | Microsoft Project | Best open support content for WBS masks and custom fields. |

## Main Research Outcome

Official software documentation materially changes the shape of the target research universe:

- the schedule is not always a file of activities;
- governed sheets, configured fields, versions, logs, item references, and linked digital objects are real parts of software-native schedule systems;
- software confirms the five-family model:
  - `decomposition`
  - `document-system`
  - `stage-gate`
  - `report/log`
  - `digital-governance`

## Watchlist

Bentley SYNCHRO, Planisware, Safran Planner, and Smartsheet remain relevant but are still outside the deep-profile set because their open official documentation was less directly inspectable or less field-schema-explicit in the current pass.
