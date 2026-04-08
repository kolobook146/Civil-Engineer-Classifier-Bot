# Stage 11: Level-of-Detail Framework

## Purpose

This report defines the first deep LOD framework based on open-source regional and institute evidence.

## 1. Main Conclusion

Researcher inference:

- There is no single globally adequate LOD ladder for construction and project scheduling.
- The evidence supports at least four coexisting LOD grammars.

## 2. The Four LOD Grammars

### 2.1 Decomposition-led LOD

Strongest in:

- PMI
- GAO
- AACE
- U.S. public-control sources

Core idea:

- detail is carried through WBS depth, work-package structure, and reviewable logic quality.

### 2.2 Document-system-led LOD

Strongest in:

- CIS sources
- China construction-organization sources

Core idea:

- detail is carried through planning-document hierarchy such as POS, PPR, construction organization design, and execution-level documents.

### 2.3 Phase- and governance-led LOD

Strongest in:

- PM²
- EIB / EPEC
- FIDIC delivery and procurement guidance

Core idea:

- detail is carried through project phases, project-cycle stages, procurement packages, and gate artefacts.

### 2.4 Digital-checkpoint-led LOD

Strongest in:

- China digital-housing and digital-supervision sources

Core idea:

- detail is carried through digital checkpoints, archive keys, platform events, and lifecycle data records.

## 3. Cross-Region Mapping

| Region / institute cluster | Dominant LOD grammar | Secondary grammar |
| --- | --- | --- |
| CIS | document-system-led | decomposition-led |
| EU | phase- and governance-led | decomposition-led |
| USA | decomposition-led | review- and integrity-check-led |
| China | document-system-led + digital-checkpoint-led | phase-governance-led |
| PMI / AACE | decomposition-led | governance-led |
| PM² / EIB / EPEC / FIDIC | phase- and governance-led | document-led for artefacts |

## 4. Practical LOD Framework for This Research

The research corpus should treat LOD as a multi-axis system:

### Axis A. Management horizon

- lifecycle
- phase
- control
- look-ahead
- short interval

### Axis B. Decomposition depth

- programme / project
- phase
- WBS branch
- work package
- execution task

### Axis C. Governance/document layer

- initiation
- authorization
- planning package
- review / acceptance package
- closeout package

### Axis D. Digital checkpoint layer

- project code
- digital archive
- digital supervision checkpoint
- warning / exception object

## 5. What Changed Relative to the Previous Base

Before this pass, LOD was already recognized as important but still behaved like a generic `master / detailed / look-ahead` ladder.

After this pass:

- LOD is visibly region- and institute-dependent;
- LOD can be carried by document hierarchy, not only task depth;
- stage-gate and digital layers must be treated as LOD carriers too.

## 6. Main Modeling Implication

The later target model should not store only one `detail_level` field. It will likely need:

- schedule horizon;
- decomposition depth;
- document layer;
- governance stage;
- optional digital checkpoint layer.

## 7. Main Supporting Sources

- `SRC-A-011`
- `SRC-A-026`, `SRC-A-036`
- `SRC-A-028`, `SRC-A-029`, `SRC-A-030`
- `SRC-A-037`, `SRC-A-038`, `SRC-A-039`, `SRC-A-040`
- `SRC-A-041`, `SRC-A-044`
- `SRC-A-043`
