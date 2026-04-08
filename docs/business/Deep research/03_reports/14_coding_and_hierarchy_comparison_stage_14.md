# Stage 14: Coding and Hierarchy Comparison

## Purpose

Stage 14 consolidates how schedules are structured and coded across regions, institutes, and software systems. The result is that coding and hierarchy are not minor implementation details. They are one of the main differentiators between scheduling schools.

## Main Conclusion

The current research base confirms five hierarchy grammars that map closely to the five family model used in Stages 10-15:

1. `Decomposition hierarchy`
2. `Document-system hierarchy`
3. `Stage-gate hierarchy`
4. `Report/log hierarchy`
5. `Digital-governance hierarchy`

These hierarchies coexist; they are not mutually exclusive.

## Core Coding Structures

### 1. Decomposition hierarchy

Typical structures:

- WBS
- outline number
- work package node
- project code prefix
- control account / work package mapping

Strongest sources:

- `SRC-A-041`, `SRC-A-044`, `SRC-A-031`
- `SRC-A-003`, `SRC-A-045`, `SRC-A-049`, `SRC-A-050`, `SRC-A-056`

Interpretation:

This remains the dominant hierarchy grammar in U.S. controls practice and in enterprise CPM software.

### 2. Document-system hierarchy

Typical structures:

- `POS -> PPR -> execution-level plans`
- construction organization design layers
- schedule sheet and master schedule sheet hierarchy
- template and governed-sheet structures

Strongest sources:

- `SRC-A-026`, `SRC-A-027`, `SRC-A-033`
- `SRC-A-047`, `SRC-A-048`

Interpretation:

This hierarchy is underrepresented in generic PM teaching but highly important in CIS, China, and some enterprise systems.

### 3. Stage-gate hierarchy

Typical structures:

- phase code
- stage code
- project-cycle stage
- procurement package hierarchy
- acceptance and phase-exit structures

Strongest sources:

- `SRC-A-028`, `SRC-A-029`, `SRC-A-030`
- `SRC-A-037`, `SRC-A-038`, `SRC-A-039`
- `SRC-A-064`, `SRC-A-065`, `SRC-A-070`

Interpretation:

This is a delivery-governance hierarchy more than a production hierarchy. It is strongest in EU and institutional methodologies.

### 4. Report / log hierarchy

Typical structures:

- version / milestone hierarchy
- note category
- audit category
- tag / label / category code

Strongest sources:

- `SRC-A-057`, `SRC-A-059`, `SRC-A-067`, `SRC-A-068`

Interpretation:

Collaborative systems often use lighter but operationally powerful hierarchy layers for navigation, review, and traceability.

### 5. Digital-governance hierarchy

Typical structures:

- digital project code
- archive key
- location / space / zone tree
- linked-object namespace
- import-source hierarchy

Strongest sources:

- `SRC-A-043`, `SRC-A-034`
- `SRC-A-058`, `SRC-A-060`, `SRC-A-073`

Interpretation:

This hierarchy becomes essential when the schedule is embedded in BIM-, issue-, inspection-, and document-linked platforms.

## What Software Documentation Added

Software documentation materially strengthened the hierarchy model:

- `Primavera P6` and `Primavera Cloud` confirmed enterprise hierarchy stacks: EPS, WBS, codes, work packages, roles, locations.
- `Unifier` confirmed sheet-centric hierarchy and master/child schedule-sheet organization.
- `Microsoft Project` clarified WBS masks, prefixes, sequence rules, separators, and WBS-based predecessor display.
- `Asta` exposed reusable code libraries, rich spreadsheet fields, and custom linked tables.
- `Deltek` strengthened work-package and control-account mapping in a cost-schedule environment.
- `Autodesk Build` and `Glodon` strengthened location-tree and linked-object hierarchy.
- `Backlog` showed lightweight milestone/version/category hierarchies.

## Regional Alignment

### CIS

The coding model must leave room for document-system hierarchy. A flat WBS-only design would underrepresent `POS/PPR` logic.

### EU

The most important hierarchy layer is often not WBS depth but lifecycle stage, approval package, procurement package, and governance artefact structure.

### USA

The U.S. layer remains strongest for decomposition-led, control-led, and mapping-led hierarchies.

### China

China combines organization-design hierarchy with digital code and digital archive hierarchy more strongly than any other region in the current corpus.

### Global institutes

- `PMI` and `GAO` reinforce decomposition hierarchy.
- `AACE` reinforces control mapping and schedule-basis structures.
- `PM²`, `EIB/EPEC`, and `FIDIC` reinforce phase, package, gate, and lifecycle segmentation.

## Result

The working coding and hierarchy catalog now spans `COD-001` to `COD-029`. The central insight is that hierarchy design is not secondary modeling hygiene. It determines what the schedule is allowed to represent: work decomposition only, governed documents, delivery gates, digital platform objects, or all of them together.
