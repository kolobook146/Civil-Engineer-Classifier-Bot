# Monthly Controls A4 Reference Index

Purpose: keep the `monthly_controls_a4` layout tied to mature construction / capital-project controls practice without turning the pilot into a heavy enterprise PMO pack.

## Adopted Design Pattern

The pilot sheet uses a one-page PMO monthly controls pack pattern:

- top KPI band for reporting period, full-month planned workload, month-to-date EVA and delay signal;
- main integrated controls view by project, using `PV MTD / EV MTD / AC MTD`;
- milestone and gate watch for near-term schedule governance;
- schedule movement view for started / completed / in-progress / delayed work;
- exception list and operational watch cards for management attention;
- one short management headline.

## Reference Sources

| Source | Type | What To Borrow | Pilot Use |
| --- | --- | --- | --- |
| GSA Kahua Monthly Status Report | Owner / PMIS operating guidance | Monthly status reporting, milestone baseline / estimated / actual logic, risks on dashboard | `Milestones & Gates Watch`, PMIS-driven current state |
| GSA Project Management Information System | Owner-side PMIS model | Single control environment for project management data and reporting | Dashboards read from workbook control surfaces, not raw `data_facts` |
| DOE Monthly Project Dashboard Performance Metrics | Owner / federal project controls dashboard | Monthly performance against approved baselines and RAG status | KPI band, schedule/cost signal, exception escalation |
| DOE PARS II User Guide | Owner / capital project controls system | Cost performance reports, schedule dashboards, CPI / SPI and time-phased control | `PV / EV / AC`, CPI/SPI, project-level controls chart |
| Oracle P6 Project Earned Value Dashboard | PMIS / EVM product documentation | Earned value dashboard structure with SPI/CPI and detailed drill-down | `Monthly Integrated Controls by Project` |
| UK GovS 002 Project Delivery Standard | Official governance standard | Factual reporting, baseline reference, risks/issues/decisions discipline | Monthly controls tone and headline discipline |
| UK Teal Book Chapter 20 Risk Management | Official project delivery guidance | Risk ownership, escalation, risk matrix / exception logic | `Top Exceptions`, `Operational Watch` |

## Implementation Notes

- `PV This Month` is a workload signal for the full reporting month.
- `PV MTD` is the month-to-date planned value denominator for monthly `SPI`.
- `EV MTD` and `AC MTD` are model-derived month-to-date values based on the current schedule actual window.
- `BAC / Total Planned Cost` is intentionally not used as plan-to-date.
- Reference material is stored as links and annotations, not copied images, to avoid copyright and provenance issues.
