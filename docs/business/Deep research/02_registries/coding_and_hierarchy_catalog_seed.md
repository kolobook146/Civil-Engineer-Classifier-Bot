# Coding and Hierarchy Catalog Seed

This seed catalog records coding and hierarchy structures already visible in the first-pass materials.

| Code ID | Coding / hierarchy structure | Class | Seen in | Typical use | Notes |
| --- | --- | --- | --- | --- | --- |
| `COD-001` | WBS | Hierarchy | `SRC-A-001`, `SRC-A-003`, `SRC-A-019`, `SRC-A-020` | Scope decomposition and roll-up | Most common structural backbone observed so far. |
| `COD-002` | OBS | Hierarchy | `SRC-A-003`, `SRC-A-021` | Organizational ownership and reporting | Often paired with WBS. |
| `COD-003` | EPS / enterprise project hierarchy | Hierarchy | `SRC-A-003` | Multi-project organization | Software-specific but important in enterprise environments. |
| `COD-004` | Activity code | Coding | `SRC-A-003`, `SRC-A-022` | Filtering and grouping across many dimensions | Strong candidate for one-to-many code families. |
| `COD-005` | Milestone coding | Coding | `SRC-A-019`, `SRC-A-022` | Control-point grouping | Likely more common in owner oversight than in academic texts. |
| `COD-006` | Responsibility code | Coding | `SRC-A-003`, `SRC-A-021` | Assignment of accountable party | May live as OBS, custom code, or contract responsibility. |
| `COD-007` | Phase code | Coding | `SRC-A-022`, `SRC-A-024` | Lifecycle segmentation | Strongly relevant to delivery schedules. |
| `COD-008` | Location / area code | Coding | `SRC-A-003` | Site segmentation and production control | Needs deeper evidence in later EPC and industrial sources. |
| `COD-009` | Discipline code | Coding | `SRC-A-003` | Engineering, civil, MEP, commissioning segmentation | Common in software practice; needs more regional evidence. |
| `COD-010` | Contract / package code | Coding | `SRC-A-016`, `SRC-A-023`, `SRC-A-024` | Procurement and contract segmentation | Important for delivery-level schedules. |
| `COD-011` | Funding / program segment | Coding | `SRC-A-020`, `SRC-A-024` | Public investment and program-level reporting | Likely important in owner-side public projects. |
| `COD-012` | Task ID logic | Identity | `SRC-A-003`, `SRC-A-022` | Stable or semi-stable row identity | Needs later analysis of renumbering and traceability rules. |
| `COD-013` | WBS decomposition level | Hierarchy | `SRC-A-041`, `SRC-A-044`, `SRC-A-031` | Control granularity and roll-up | Strong candidate for cross-region LOD alignment. |
| `COD-014` | Phase / stage code | Coding | `SRC-A-028`, `SRC-A-029`, `SRC-A-037` | Lifecycle and stage-gate segmentation | Strong in EU and institute methodologies. |
| `COD-015` | Document-system hierarchy (POS / PPR / organization design) | Hierarchy | `SRC-A-026`, `SRC-A-027`, `SRC-A-033` | Planning-document layering | Important in CIS and China schools. |
| `COD-016` | Digital project code / archive key | Coding | `SRC-A-043`, `SRC-A-034` | Cross-system digital traceability | Important for China digital governance models. |
| `COD-017` | Code library / code-library entry | Coding | `SRC-A-054`, `SRC-A-055`, `SRC-A-014` | Shared classification vocabularies across schedules and reports | Software confirms that coding often lives in reusable libraries, not only row-level text values. |
| `COD-018` | Outline number | Hierarchy | `SRC-A-050` | Built-in hierarchical numbering | Important where the visible schedule hierarchy doubles as a code system. |
| `COD-019` | Project code prefix | Identity / coding | `SRC-A-050` | Prefix-based numbering for project hierarchy | Useful for stable multi-project identity design. |
| `COD-020` | EPS / schedule-sheet hierarchy / multi-sheet hierarchy | Hierarchy | `SRC-A-003`, `SRC-A-047`, `SRC-A-048` | Enterprise grouping of projects or sheets | Shows that hierarchy may be project-centric or document-container-centric. |
| `COD-021` | Work package / control account mapping code | Control hierarchy | `SRC-A-056`, `SRC-A-057` | Cost-schedule integration and accountability | Strong U.S. enterprise-controls structure. |
| `COD-022` | Resource group hierarchy | Hierarchy | `SRC-A-060`, `SRC-A-073` | Team-level assignment and analysis | Important in collaborative field-planning platforms. |
| `COD-023` | Location / space / zone tree | Hierarchy | `SRC-A-073`, `SRC-A-058` | Digital spatial segmentation and location-based control | Strongly aligned with digital-construction workflows. |
| `COD-024` | Version / milestone hierarchy | Hierarchy / coding | `SRC-A-067`, `SRC-A-068`, `SRC-A-059` | Versioned or milestone-grouped views | Important in issue-driven and version-driven systems. |
| `COD-025` | Layout / field-schema hierarchy | Schema hierarchy | `SRC-A-064`, `SRC-A-049` | Field-group organization and reusable layouts | Confirms that schema design itself can become a hierarchy layer. |
| `COD-026` | Import-source hierarchy | Integration hierarchy | `SRC-A-058`, `SRC-A-060`, `SRC-A-047` | Organizing imported schedules and synchronization sources | Important where software is an integration shell rather than the original authoring tool. |
| `COD-027` | Tag / label / category code | Coding | `SRC-A-067`, `SRC-A-076` | Lightweight classification, search, workflow routing | More common in collaborative platforms than in heavy CPM tools. |
| `COD-028` | Item-reference namespace / linked-object ID | Digital linkage coding | `SRC-A-058`, `SRC-A-073` | Cross-platform object linkage | Key in digital-governance and BIM-linked environments. |
| `COD-029` | Note category / audit category | Coding / governance | `SRC-A-057`, `SRC-A-047` | Structured logs, mapped notes, audit grouping | Important where report/log layers are explicit parts of the schedule system. |
| `COD-030` | Portfolio / programme code | Hierarchy / coding | `SRC-A-089`, `SRC-A-105`, `SRC-A-114` | Portfolio and programme segmentation in PMIS or PMO systems | Enterprise practice often needs an above-project hierarchy, not only project-level WBS. |
| `COD-031` | Handover / systems-completion breakdown | Hierarchy | `SRC-A-097`, `SRC-A-111`, `SRC-A-115` | Segmentation by system, readiness, or handover package | Important where completion and commissioning are a major control layer. |
| `COD-032` | Interface / stakeholder code | Coding | `SRC-A-094`, `SRC-A-116` | Managing complex interfaces across contracts, systems, or stakeholders | Megaproject delivery often needs explicit interface-coded control. |
| `COD-033` | PMIS workflow / status code | Coding / governance | `SRC-A-105`, `SRC-A-099`, `SRC-A-102` | Workflow routing, issue state, digital approval status | Important in enterprise PMIS and smart-site systems. |
| `COD-034` | Revision / checker / approver trace code | Coding / document governance | `SRC-A-098`, `SRC-A-106`, `SRC-A-100` | Controlled review and approval traceability | Document-system practice adds review lineage as a structured coding layer. |
| `COD-035` | Engineering firm classification / discipline category code | Governance coding | `SRC-A-120`, `SRC-A-121`, `SRC-A-123` | Firm classification, eligibility, evaluation grouping | Important in authority-governed regional systems. |
| `COD-036` | Professional qualification / engineer grade code | Governance coding | `SRC-A-120`, `SRC-A-123` | Engineer competency and professional grade segmentation | Important where qualification is formalized and system-managed. |
| `COD-037` | Permit-platform workflow / transaction code | Digital-governance coding | `SRC-A-122`, `SRC-A-123` | Permit lifecycle and digital workflow routing | Important when permitting and compliance records intersect with project delivery systems. |
| `COD-038` | PMIS portfolio / programme / shell hierarchy | Hierarchy | `SRC-A-125`, `SRC-A-127`, `SRC-A-105` | Organizing enterprise records above the project and within controlled containers | Important because PMIS often requires a container hierarchy independent of WBS. |
| `COD-039` | Business-process type / workflow schema code | Coding / workflow design | `SRC-A-126`, `SRC-A-127`, `SRC-A-130` | Distinguishing PMIS record families and routes | Important where workflow behavior depends on record type. |
| `COD-040` | Cost-sheet / fund / ledger code | Coding / commercial hierarchy | `SRC-A-125`, `SRC-A-126`, `SRC-A-105` | Budget, funding, or cost-control segmentation | Commercial and PMIS systems frequently use ledger-style segment codes. |
| `COD-041` | Document number and revision-status schema | Coding / document governance | `SRC-A-129`, `SRC-A-130`, `SRC-A-136` | Controlled document identity and revision lineage | Canonical EDMS coding family. |
| `COD-042` | Transmittal reason / distribution code | Coding / document governance | `SRC-A-129`, `SRC-A-132`, `SRC-A-136` | Reason-for-issue, recipient routing, communication classification | Important because document issue context is strongly structured in mature EDMS. |
| `COD-043` | Review workflow template / step code | Coding / workflow governance | `SRC-A-128`, `SRC-A-135`, `SRC-A-138` | Routing templates and review-step semantics | Helps separate workflow design from instance records. |
| `COD-044` | Permit gateway / authority / submission code | Coding / regulatory governance | `SRC-A-149`, `SRC-A-150`, `SRC-A-122` | Segmentation by gateway, authority, and submission family | Strong permit-engine coding cluster. |
| `COD-045` | Smart-site domain code | Coding / digital governance | `SRC-A-099`, `SRC-A-140`, `SRC-A-152` | Quality, safety, progress, labor, equipment, environment, logistics | Important because smart-site events are often routed and reported by domain. |
| `COD-046` | Device / sensor / monitored-location namespace | Coding / digital monitoring | `SRC-A-102`, `SRC-A-152`, `SRC-A-153` | Device identity and monitored-zone linkage | Needed when telemetry becomes part of project control. |
| `COD-047` | Resource group / craft / skill / certification code | Coding / resource governance | `SRC-A-141`, `SRC-A-143`, `SRC-A-153` | Grouping by pool, craft, competency, or assignability | Important because resource engines classify capability, not only people. |
| `COD-048` | Billing / draw / SOV / retainage code | Coding / commercial | `SRC-A-131`, `SRC-A-139`, `SRC-A-148` | Billing package, line-item, retainage, and commercial segmentation | Strong payment-engine coding family. |
| `COD-049` | Payment hold / compliance / waiver status code | Coding / commercial governance | `SRC-A-146`, `SRC-A-147` | Commercial eligibility, legal-document status, hold-release logic | Important because commercial workflow state is more granular than approved / paid. |
