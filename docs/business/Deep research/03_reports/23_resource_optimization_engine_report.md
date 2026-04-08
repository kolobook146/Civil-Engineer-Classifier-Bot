# Stage 23: Resource Optimization Engine Report

## Scope

This report studies resource optimization, capacity, and assignment systems as a distinct subsystem family.

Primary evidence base:

- `SRC-A-142`
- `SRC-A-143`
- `SRC-A-144`
- `SRC-A-145`
- `SRC-A-141`
- `SRC-A-153`
- `SRC-A-082`
- `SRC-A-087`

## Main Conclusion

Resource optimization is not just a set of resource columns on schedule activities.
It is a subsystem that reasons over:

- demand;
- pool availability;
- assignment feasibility;
- conflicts and overallocation;
- reassignment and balancing.

Research interpretation:
this is the clearest Stage 23 example of an engine that is schedule-derived but not schedule-contained.

## Core Resource-Engine Object Model

Across the evidence base, the recurring objects are:

- resource or role;
- resource pool;
- team or crew;
- skill / job title / certification;
- assignment;
- request;
- capacity / availability view;
- calendar and units;
- engagement or approval to use a resource;
- balancing or overallocation signal.

## Strong Evidence from Official Documentation

### Microsoft Project / Project Online

`SRC-A-142` and `SRC-A-143` show a classical capacity and balancing grammar:

- resource workload views;
- overallocation indicators;
- remaining availability;
- capacity planning across projects;
- shared resource pools.

The Microsoft evidence is especially strong because it exposes the analytical logic of demand versus capacity clearly.

### Oracle Primavera Cloud

`SRC-A-144` and `SRC-A-145` show a cloud-native resource model:

- hierarchical resource and role dictionaries;
- assignment lists;
- workspace- and project-level ownership;
- resource and role analysis;
- assignment operations inside a broader enterprise object model.

This confirms that modern enterprise tools treat resource structures as first-class data, not simple task fields.

### Procore Resource Planning

`SRC-A-141` shows a field-operations resource-planning grammar:

- people list;
- assignable versus login-capable users;
- requests and fills;
- assignment alerts;
- company and project sync;
- labor / equipment / materials direction of travel.

This is important because it demonstrates that resource engines increasingly live outside classical schedulers.

### Labor-control platforms

`SRC-A-153` extends the picture with labor governance:

- attendance;
- contract and wage management;
- enterprise and project views;
- risk-warning and identity-control logic.

## Relationship to Schedule

The schedule expresses planned demand.
The resource engine determines whether the demand is feasible under actual pool conditions.

This is a different business question.

Examples:

- the schedule can say an activity should start;
- the resource engine determines whether the right crew, role, or certified person is available;
- the schedule can express multiple simultaneous tasks;
- the resource engine determines whether the shared pool makes that possible.

## Why It Should Stay Outside the Pilot Core

A full resource engine would require the project to manage:

- resource master data;
- shared pools;
- availability over time;
- conflict resolution rules;
- assignment approval logic;
- balancing algorithms.

This is materially heavier than the current pilot scope.

## Target-Model Implication

The pilot core should continue to support:

- resource-aware schedule items;
- crew / role / subcontractor references;
- external links to resource systems;
- coded fields for resource group, job title, or responsibility.

It should not yet absorb:

- full cross-project capacity logic;
- leveling algorithms;
- enterprise resource-pool governance.

## Bottom-Line Result

Resource optimization is a true adjacent engine, not a detail setting.
If the project eventually moves from schedule representation into execution-feasibility optimization, this subsystem will need a dedicated architecture rather than incremental field growth inside the schedule sheet.
