# Universal Core of Construction and Project Scheduling

## Purpose

This document captures the initial universal core that appears repeatedly across primary sources, academic construction teaching, and leading scheduling software.

Important note: the statements below are synthesis statements. They are researcher inference unless explicitly attributed to a single source.

## 1. Initial Universal Core

Across PMI, CMU construction management teaching, AACE guidance, Primavera P6, Microsoft Project, and owner-side controls documents, the following nucleus appears to be universal:

- A schedule is built from discrete work items.
- Work items are connected by explicit logic relationships.
- Time calculations depend on calendars and constraints.
- A network has one or more controlling paths.
- Variance control requires a baseline and periodic status updates.
- Schedule usefulness depends on decomposition quality and coding quality, not only on date fields.
- Progress control requires actual dates, remaining work logic, and a defined update point.
- Different management levels require different levels of detail.
- Schedule data is not enough on its own; governance artifacts are also needed.

## 2. Universal Data Objects

The first-pass universally recurring object model is:

- work object:
  - activity / task
  - milestone
- logic object:
  - dependency / relationship
  - lag / lead
- time object:
  - calendar
  - constraint
  - dates
- control object:
  - baseline
  - status date / data date
  - actual start / actual finish
  - remaining duration
- analytical object:
  - critical path
  - float / slack
- structure object:
  - WBS or equivalent hierarchy
  - responsibility structure
  - classification / coding scheme
- capability object:
  - resource
  - crew / labor / equipment / material variants

## 3. Universal Computational Logic

The recurring computational logic includes:

- precedence logic defines allowable execution order;
- calendars translate durations into working time;
- constraints alter or limit calculated dates;
- criticality emerges from path logic and time reserve;
- variance is evaluated against baseline instances;
- forecast depends on update status and remaining work assumptions.

This logic is visible in both formal scheduling standards and mainstream scheduling software.

## 4. Universal Governance Layer

The research already shows that schedules are governed not only by fields and calculations, but also by companion artifacts and procedures. The most important early findings are:

- schedule basis
- scheduling specification
- update narrative
- review / acceptance procedure
- baseline approval logic

This means a viable schedule model for real projects must account for document-level governance, not just rows of activities.

## 5. Universal Hierarchy and Coding Logic

The universal pattern is not one single coding system, but the repeated existence of coding systems for:

- scope decomposition;
- organizational ownership;
- reporting grouping;
- location / phase / discipline segmentation.

Researcher inference: coding is structurally universal, while the exact code families are regional, sectoral, or tool-dependent.

## 6. Universal Progress-Control Loop

The common control loop found in the first-pass sources is:

1. define work scope and decomposition;
2. define logic, durations, calendars, and constraints;
3. issue or approve a baseline;
4. status the schedule at a defined data date;
5. compare current state to baseline;
6. analyze critical path, float, and variance;
7. forecast completion and decide corrective action;
8. document narrative and governance implications.

This loop holds across standards, public-owner requirements, and software support functions.

## 7. Universal Need for Multiple Schedule Views

The evidence does not support a single flat schedule as a universal best practice. Instead, recurring practice points to multiple views or levels such as:

- master or summary view;
- detailed control schedule;
- short-term look-ahead or update view;
- management / oversight reporting view.

Researcher inference: multi-view scheduling is a universal management need even when the underlying data model differs.

## 8. Universal Distinction Emerging in the Data

Even before formal regional analysis, the sources already suggest a universal boundary between:

- production-centered logic:
  - crews
  - execution sequence
  - workfront flow
  - resource coordination
- delivery-centered logic:
  - feasibility
  - approvals
  - engineering
  - procurement
  - contract milestones
  - financing
  - commissioning

This supports treating production schedule and project delivery schedule as separate research objects, not merely two names for one thing.

## 9. Risks of Oversimplification

The early evidence shows that the following simplifications would be misleading:

- assuming schedule equals activity list;
- assuming one baseline is always enough;
- assuming construction schedule starts at site mobilization;
- assuming logic and dates alone are sufficient without basis and governance;
- assuming all schedule levels use the same granularity;
- assuming resource, cost, and contract implications are secondary.

## 10. Initial Universal Entity Set

The current seed set of universal or near-universal entities is recorded in [entity_atlas_seed.md](../02_registries/entity_atlas_seed.md).

## 11. Source Basis

- `SRC-A-001` Practice Standard for Scheduling
- `SRC-A-002` Project Management for Construction
- `SRC-A-003` Primavera P6 User Guide
- `SRC-A-004` to `SRC-A-007` Microsoft Project support pages
- `SRC-A-008` to `SRC-A-013` AACE framework and recommended practices
- `SRC-A-018` to `SRC-A-022` owner / public-sector scheduling governance documents

## 12. Immediate Questions for Later Stages

- Which parts of this universal core are truly cross-regional, and which are only dominant in US/Anglo project controls culture?
- Which universal entities exist as software objects versus governance artifacts only?
- How does the universal core split between production execution and delivery realization in China and CIS practice?
