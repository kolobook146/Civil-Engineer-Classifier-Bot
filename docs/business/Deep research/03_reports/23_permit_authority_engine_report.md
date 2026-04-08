# Stage 23: Permit / Authority Engine Report

## Scope

This report studies digital permit and authority systems as full regulatory workflow engines rather than simple permit-date trackers.

Primary evidence base:

- `SRC-A-060`
- `SRC-A-061`
- `SRC-A-120`
- `SRC-A-121`
- `SRC-A-122`
- `SRC-A-123`
- `SRC-A-149`
- `SRC-A-150`
- `SRC-A-151`

## Main Conclusion

Permit / authority systems are not just milestone producers.
They are external case-management engines with their own:

- gateways;
- agencies;
- submission packages;
- fee and proof logic;
- comment / resubmission loops;
- approval and certification outcomes.

Research interpretation:
this is one of the clearest `stage-gate + digital-governance` families in the whole corpus.

## Core Permit / Authority Object Model

The recurring object model is:

- project registration record;
- permit or approval case;
- submission gateway;
- agency / authority participant;
- submission package;
- supporting document or model set;
- fee / payment / proof-of-payment record;
- review comments and return notes;
- resubmission package;
- approval, permit, occupancy, or completion certificate.

## Strong Evidence from Official Sources

### Singapore CORENET X

`SRC-A-149` and `SRC-A-150` provide one of the strongest openly inspectable authority-system grammars in the corpus.

What stands out:

- multi-agency regulatory submissions;
- key submission gateways;
- explicit submission-preparation rules;
- BIM and model-based information requirements;
- implementation circulars tied directly to project timeline impact;
- allowance for concurrent gateway processing to shorten approvals.

This is not a "permit list."
It is a structured national submission engine.

### Middle East Authority Platforms

`SRC-A-120` to `SRC-A-123` show a different but equally strong authority grammar:

- professional qualification and classification records;
- permit-platform project records;
- authority-run evaluation and certification;
- workflow and service procedures;
- classification-linked participation rights.

This expands the permit family beyond plan approval into regulated project participation and completion evaluation.

### China Digital Housing and Approval Systems

`SRC-A-151` shows a national digital-governance direction:

- full-lifecycle digital project management;
- project coding rules;
- interconnection across approval, market supervision, quality and safety supervision, and service platforms;
- stronger integration between approval systems and broader construction governance.

## Relationship to Schedule

Permit engines affect the delivery schedule in at least five ways:

1. they create external critical-path dependencies;
2. they often define mandatory gates before design, piling, construction, occupancy, or closeout;
3. they can create rework loops through returned comments and resubmissions;
4. they may require fee confirmation or proof-of-payment before processing;
5. they can enable parallel gateways, which changes schedule logic materially.

This means permit logic is schedule-relevant, but not schedule-native.

## Regional Strength

The strongest current evidence comes from:

- Singapore for multi-agency digital submission governance;
- Middle East for authority-platform and professionalization overlays;
- China for lifecycle digital approval and supervision integration.

The permit / authority family is therefore genuinely international, but regionally diverse in grammar.

## Implication for the Target Model

The Stage 22 core should continue to model:

- permit-related schedule items;
- governance records for permit outcomes;
- external links to authority cases.

It should not yet absorb:

- full regulatory case state;
- multi-agency package management;
- fee handling;
- resubmission workflow logic.

## Bottom-Line Result

Permit / authority engines are among the hardest external dependencies in delivery scheduling.
They should remain outside the pilot core, but they now require explicit recognition as a separate subsystem class with strong schedule consequences.
