# Research Charter

## 1. Research Objective

Build a broad, evidence-based, and implementation-neutral research corpus on how investment construction project schedules are defined, structured, governed, maintained, and used across regions, institutions, academic schools, and software systems.

This phase is intentionally not constrained by future pilot simplification.

## 2. Primary Research Question

What practices, entities, rules, properties, coding systems, governance layers, levels of detail, and software data structures are used to compose and manage schedules in investment construction projects across major scheduling schools and operating regions?

## 3. In Scope

- Construction and project scheduling concepts, methods, and governance.
- Universal scheduling core.
- Schedule typology.
- Production schedule versus project delivery schedule.
- Regional schools:
  - CIS
  - European Union
  - United States
  - China
- International best practices outside regional segmentation.
- Software data models and scheduling workflows.
- Academic formalization and educational logic.
- Cross-project processes represented in schedules:
  - development
  - design
  - permitting
  - procurement
  - finance
  - mobilization
  - quality
  - HSE
  - commissioning
  - handover
  - closeout
- Open search for emergent entities, fields, codings, and rules.

## 4. Out of Scope in This Phase

- Choosing the final target business model.
- Simplifying the research to match MVP, pilot, or sheet limitations.
- Modifying existing `docs/business` artifacts outside this folder.
- Technical implementation inside application code.

## 5. Core Definitions Used in This Research

### 5.1 Schedule

A structured representation of planned, controlled, and updated temporal logic for project or production execution, including dates, sequence logic, constraints, status, and often resource or cost context.

### 5.2 Production Schedule

A schedule centered on physical execution of works, workfront logic, crews, site sequence, equipment, material availability, and near-to-mid-range construction control.

### 5.3 Project Delivery Schedule

A broader project lifecycle schedule covering the investment-construction process, including development, approvals, engineering, procurement, contracts, finance, construction, commissioning, and closeout.

### 5.4 Entity

A persistent modeled object used in schedule data or governance, such as task, milestone, dependency, calendar, activity code, baseline, approval gate, or work package.

### 5.5 Rule

A repeatable scheduling instruction, requirement, convention, or algorithm that affects data structure, update logic, governance, contractual compliance, or analysis.

### 5.6 Coding Structure

A formal classification or identifier system used to group, filter, aggregate, trace, or govern schedule data, such as WBS, OBS, CBS, location codes, system codes, or discipline codes.

### 5.7 Level of Detail

The depth of decomposition and control used in a schedule, usually linked to management level, planning horizon, project phase, and use case.

## 6. Required Separations

This research must explicitly preserve the following distinctions:

- Universal principles versus regional specifics.
- Schedule type versus application domain.
- Production schedule versus project delivery schedule.
- Academic teaching logic versus field practice.
- Contractual schedule governance versus internal planning practice.
- Data entities versus visual reporting views.
- Software-native structures versus process conventions imposed by organizations.

## 7. Analysis Axes

Each source, region, standard, or software product should be studied against these axes where applicable:

- curator zone
- country or jurisdiction
- project type
- sector
- schedule type
- application domain
- project phase
- management level
- planning horizon
- level of detail
- entities present
- rule set
- coding structures
- resource model
- cost/schedule integration
- progress and status model
- baseline and actual logic
- governance and approval logic
- reporting and control outputs

## 8. Source Hierarchy

### Level A

Primary and practice-significant sources:

- standards
- regulations
- official methodological documents
- university textbooks and course materials
- official software documentation
- owner / contractor scheduling requirements
- professional institute publications
- peer-reviewed papers
- official materials of major contractors, developers, EPC firms, and project controls organizations

### Level B

Strong secondary sources:

- academic books
- industry handbooks
- strong training material
- serious analytical overviews
- high-quality explanatory educational material

### Level C

Auxiliary sources:

- professional articles
- blogs
- forum discussions
- practical notes
- presentations
- non-official summaries

## 9. Evidence Capture Rules

- Every source gets a source ID and trust level.
- Every reusable entity gets an entity ID.
- Every reusable rule gets a rule ID.
- Unexpected findings are logged even if they do not fit the current working model.
- Synthesis statements must be traceable back to one or more recorded sources.
- If a claim is inferred rather than directly stated, it must be marked as researcher inference.

## 10. Deliverables for This Research Program

- source registry
- comparative matrix by region
- comparative matrix by software product
- entity atlas
- task and resource property catalog
- coding and hierarchy catalog
- cross-project process map
- dedicated China report
- dedicated Asia software report
- emergent findings register
- narrative synthesis reports by stage

## 11. Quality Controls

- Prefer Level A before Level B before Level C.
- Avoid overstating universality when evidence is regional.
- Do not treat software UI labels as universal business semantics without cross-checking.
- Do not treat academic definitions as real practice defaults without field evidence.
- Do not treat one contract family as globally dominant without noting jurisdictional and sector boundaries.

## 12. Initial Execution Decision

The first execution pass in this folder covers:

- Stage 0: charter formalization
- Stage 1: template and matrix design
- Stage 2: initial universal core synthesis
- Stage 3: initial international best-practice synthesis
- seed registries for sources, entities, comparative matrices, and emergent findings
