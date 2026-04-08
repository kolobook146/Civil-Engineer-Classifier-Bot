# Stage 22: Project Business Documentation Formalization

## Purpose

Stage 22 transfers the selected Stage 21 target model from the research corpus into normative project business documentation.

## Main Result

The following project-facing files were formalized or rebuilt:

- `docs/business/README.md`
- `docs/business/schedule_model.md`
- `docs/business/rule_catalog.md`
- `docs/business/sheets/schedule_sheet.md`
- `docs/business/examples/schedule_examples.md`
- `docs/business/fact_model.md`
- `docs/business/fact_to_schedule_mapping.md`
- `docs/business/business_decision_log.md`

## Main Formalization Moves

### 1. Research archive vs normative project docs

The project now explicitly separates:

- `docs/business/*` as normative business documentation
- `docs/business/Deep research/*` as the evidentiary and comparative archive

### 2. Hybrid schedule model formalized

The Stage 21 target-model draft is now expressed as the project schedule business model:

- hybrid rather than task-only
- versioned rather than mutable-only
- governance-aware rather than date-only
- extensible through hierarchy, coding, governance, link, and attribute patterns

### 3. Pilot semantics preserved

The formalization intentionally preserves the existing pilot semantic anchor:

- `function`
- `stage`
- optional `work_type`

This avoids unnecessary disruption while still upgrading the schedule model structurally.

### 4. Sheet projection clarified

The schedule sheet is now explicitly documented as:

- a flattened projection of the business model
- not the whole schedule ontology

### 5. Fact model and mapping clarified

Facts remain:

- immutable confirmed evidence
- separate from schedule structure
- mapped deliberately rather than automatically

## Result

The project now has a completed Stage 22 first-pass formalization:

- comparative research remains preserved;
- the selected target model is now normative in project documentation;
- implementation can align against `docs/business/*` without re-reading the whole research corpus each time.
