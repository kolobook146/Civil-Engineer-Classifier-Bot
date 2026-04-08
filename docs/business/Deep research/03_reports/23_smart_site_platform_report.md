# Stage 23: Smart-Site Platform Report

## Scope

This report studies smart-site platforms and related field-operational systems.

Primary evidence base:

- `SRC-A-099`
- `SRC-A-102`
- `SRC-A-103`
- `SRC-A-104`
- `SRC-A-137`
- `SRC-A-140`
- `SRC-A-152`
- `SRC-A-153`

## Main Conclusion

Smart-site platforms are event-and-monitoring systems.
Their central objects are not CPM activities, but field observations, telemetry, forms, labor, equipment, and alerts.

Research interpretation:
smart-site is the strongest `report/log + digital-governance` family in the Stage 23 layer.

## Core Smart-Site Object Model

The recurring object model is:

- observation or issue;
- daily log or site report;
- form or inspection record;
- labor-attendance or workforce record;
- equipment or device record;
- sensor or telemetry event;
- quality / safety / environment / progress alert;
- corrective action;
- dashboard or cockpit view;
- location or monitored zone.

## Strong Evidence from Regional Enterprise Practice

### China

China is the strongest zone in the corpus for full smart-site grammar.

`SRC-A-102`, `SRC-A-103`, `SRC-A-152`, and `SRC-A-153` show:

- cockpit and smart-site platforms;
- lifecycle coverage;
- integration of labor, machinery, materials, quality, safety, and progress;
- digital twin or central integrated platform logic;
- labor management and risk warning at enterprise and project levels.

This is much richer than ordinary mobile field reporting.

### CIS

`SRC-A-099` shows a strong digital site-control interpretation:

- real-time progress and quality control;
- geo-tagged issue tracking;
- drawings in the live control environment.

This reinforces that smart-site is not only a China-specific phenomenon.

### Global collaborative platforms

`SRC-A-137` and `SRC-A-140` show lighter but still important smart-site behavior in Autodesk and Procore:

- daily logs;
- forms;
- activity logs;
- observations;
- field-capture workflows.

These platforms are not as sensor-heavy as the strongest China examples, but they clearly share the same field-event grammar.

## Why Smart-Site Is Not Just "Actual Progress"

A naive model would treat smart-site data as a source of actual progress only.
The corpus shows that this is too narrow.

Smart-site platforms often track:

- quality nonconformities;
- safety incidents or observations;
- equipment status;
- labor presence;
- environmental conditions;
- service and site logistics;
- corrective-action closure.

So the system is broader than progress reporting.

## Relationship to Schedule

Smart-site platforms relate to schedule in three main ways:

1. they provide evidence for progress, delay, and readiness interpretation;
2. they create governance events that may change what work can proceed;
3. they provide dashboards and alerts that influence control decisions.

But they usually do not own the master schedule logic itself.

## Target-Model Implication

The current pilot core should preserve:

- links from schedule items to field evidence;
- governance records for observations, alerts, and issue closure;
- coded references for smart-site domains and locations.

It should not yet absorb:

- telemetry streams;
- device management;
- alert engines;
- full field issue lifecycle.

## Bottom-Line Result

Smart-site platforms materially change how operational truth is observed on projects.
They should remain a separate subsystem, but Stage 23 confirms that future progress and fact workflows will eventually need cleaner bridges to smart-site data than the pilot currently requires.
