# Task and Resource Property Catalog Seed

This is the initial seed catalog for task and resource properties observed in the first-pass sources. It is intentionally broader than a future implementation model.

| Property ID | Property | Category | Typical scope | Seen in | Notes |
| --- | --- | --- | --- | --- | --- |
| `PRP-001` | Task ID | Task identity | Task | `SRC-A-003`, `SRC-A-022` | Identifier logic often becomes part of coding strategy. |
| `PRP-002` | Task name | Task identity | Task | `SRC-A-001`, `SRC-A-003`, `SRC-A-004` | Basic but not sufficient for control. |
| `PRP-003` | Duration | Time | Task | `SRC-A-001`, `SRC-A-003` | Calendar-dependent interpretation matters. |
| `PRP-004` | Planned start | Time | Task / milestone | `SRC-A-001`, `SRC-A-003` | Often baseline-relevant. |
| `PRP-005` | Planned finish | Time | Task / milestone | `SRC-A-001`, `SRC-A-003` | Often baseline-relevant. |
| `PRP-006` | Actual start | Status | Task / milestone | `SRC-A-003`, `SRC-A-013` | Core status input. |
| `PRP-007` | Actual finish | Status | Task / milestone | `SRC-A-003`, `SRC-A-013` | Core status input. |
| `PRP-008` | Remaining duration | Status / forecast | Task | `SRC-A-001`, `SRC-A-013` | Key forecast driver. |
| `PRP-009` | Percent complete | Status | Task | `SRC-A-001`, `SRC-A-003`, `SRC-A-013` | Needs later decomposition by physical, duration, and units-based methods. |
| `PRP-010` | Status date / data date | Status control | Schedule | `SRC-A-013`, `SRC-A-019`, `SRC-A-022` | Schedule updates require a cutoff convention. |
| `PRP-011` | Calendar assignment | Time model | Task / resource / project | `SRC-A-003`, `SRC-A-006` | Calendar semantics materially affect date math. |
| `PRP-012` | Constraint type | Time control | Task | `SRC-A-006` | Important hidden driver of non-network dates. |
| `PRP-013` | Constraint date | Time control | Task | `SRC-A-006` | Works together with constraint type. |
| `PRP-014` | Predecessor link | Logic | Task | `SRC-A-003`, `SRC-A-005` | Can be internal or external. |
| `PRP-015` | Successor link | Logic | Task | `SRC-A-003`, `SRC-A-005` | Needed for network traceability. |
| `PRP-016` | Relationship type | Logic | Link | `SRC-A-003`, `SRC-A-005` | FS, FF, SS, SF. |
| `PRP-017` | Lag / lead | Logic | Link | `SRC-A-001`, `SRC-A-003` | Important for real execution models. |
| `PRP-018` | Critical flag / criticality threshold | Analysis | Task / schedule | `SRC-A-007` | Tool- and policy-dependent interpretation. |
| `PRP-019` | Total float | Analysis | Task | `SRC-A-001`, `SRC-A-007` | Frequently used for control and claims. |
| `PRP-020` | Free float | Analysis | Task | `SRC-A-001` | Less universally operationalized than total float. |
| `PRP-021` | Baseline start | Control | Task | `SRC-A-004`, `SRC-A-021` | Requires baseline-instance context. |
| `PRP-022` | Baseline finish | Control | Task | `SRC-A-004`, `SRC-A-021` | Requires baseline-instance context. |
| `PRP-023` | Baseline duration | Control | Task | `SRC-A-004` | Derived but operationally important. |
| `PRP-024` | WBS assignment | Hierarchy | Task | `SRC-A-003`, `SRC-A-019`, `SRC-A-020` | Links activity to scope decomposition. |
| `PRP-025` | Responsibility assignment | Hierarchy / governance | Task / work package | `SRC-A-003`, `SRC-A-021` | OBS, control account, contractor, team, or owner. |
| `PRP-026` | Activity code / classification | Coding | Task | `SRC-A-003`, `SRC-A-022` | May encode phase, area, discipline, contractor, and more. |
| `PRP-027` | Resource assignment | Resource | Task | `SRC-A-001`, `SRC-A-002`, `SRC-A-003`, `SRC-A-008` | Broad property family rather than single field. |
| `PRP-028` | Labor resource | Resource | Assignment | `SRC-A-002`, `SRC-A-003` | Needs later treatment of craft and crew structure. |
| `PRP-029` | Equipment resource | Resource | Assignment | `SRC-A-002`, `SRC-A-003` | Important for production schedules. |
| `PRP-030` | Material resource | Resource | Assignment | `SRC-A-002`, `SRC-A-003` | Stronger in procurement-linked planning. |
| `PRP-031` | Crew / gang | Resource | Assignment / workfront | `SRC-A-002` | Important in production-oriented schools. |
| `PRP-032` | Productivity assumption | Resource / basis | Task / resource | `SRC-A-002`, `SRC-A-012` | Often hidden in duration logic rather than explicit as a field. |
| `PRP-033` | Cost loading | Cost / control | Task / assignment | `SRC-A-008`, `SRC-A-021` | Important where integrated controls are mature. |
| `PRP-034` | Procurement package reference | Delivery | Task / milestone | `SRC-A-016`, `SRC-A-023`, `SRC-A-024` | Strongly relevant outside pure production models. |
| `PRP-035` | Approval / permit reference | Delivery | Task / milestone / gate | `SRC-A-020`, `SRC-A-024` | Important for project realization schedules. |
| `PRP-036` | Narrative / update comment | Governance | Schedule / update package | `SRC-A-019`, `SRC-A-022` | Not always a task field, but often a required companion property set. |
| `PRP-037` | WBS level / decomposition depth | Hierarchy / LOD | Task / work package | `SRC-A-041`, `SRC-A-044`, `SRC-A-031` | Important bridge between entity structure and level of detail. |
| `PRP-038` | Deliverable / output reference | Governance / scope | Task / work package | `SRC-A-038`, `SRC-A-041` | Important where schedule is output- and deliverable-driven rather than purely activity-driven. |
| `PRP-039` | Assumption / constraint reference | Governance | Task / phase / programme | `SRC-A-038`, `SRC-A-039`, `SRC-A-012` | Important for traceable schedule basis and stage-gate planning. |
| `PRP-040` | Status-report linkage | Governance / reporting | Task / milestone / package | `SRC-A-037`, `SRC-A-042` | Supports structured periodic reporting rather than free-text reporting only. |
| `PRP-041` | Issue / change / decision log linkage | Governance | Task / package / gate | `SRC-A-037`, `SRC-A-042` | Important when schedule changes are formally governed. |
| `PRP-042` | Digital archive / project code reference | Digital governance | Task / package / project | `SRC-A-043`, `SRC-A-034` | Important for China digital lifecycle traceability. |
| `PRP-043` | Custom field / configured field value | Extension schema | Task / phase / project / issue | `SRC-A-045`, `SRC-A-049`, `SRC-A-064`, `SRC-A-067` | Software documentation confirms configurable schema values as mainstream, not exceptional. |
| `PRP-044` | Formula-based field value | Extension schema / calculation | Task / project | `SRC-A-045`, `SRC-A-049` | Important where business logic is embedded in configured fields. |
| `PRP-045` | Lookup / list field value | Extension schema / classification | Task / phase / issue | `SRC-A-049`, `SRC-A-064`, `SRC-A-067` | Bridges custom fields and controlled coding vocabularies. |
| `PRP-046` | Baseline type / baseline instance | Control | Task / schedule / project | `SRC-A-045`, `SRC-A-053`, `SRC-A-063` | Important because software often separates multiple baseline instances or current baseline logic. |
| `PRP-047` | Baseline variance / slippage / finish variance | Control / analysis | Task / schedule | `SRC-A-059`, `SRC-A-063` | Strong software evidence that variance properties are first-class output fields. |
| `PRP-048` | Deadline / deadline variance | Time control / analysis | Task | `SRC-A-061`, `SRC-A-062` | Useful in collaborative systems where deadlines and constraints coexist. |
| `PRP-049` | Version summary / change summary | Governance / traceability | Schedule version | `SRC-A-059` | Important for change visibility between schedule versions. |
| `PRP-050` | Schedule source file / import origin | Integration / document-system | Schedule / project | `SRC-A-058`, `SRC-A-060`, `SRC-A-047` | Important when the active schedule is imported or synchronized from another system. |
| `PRP-051` | Item reference / linked object ID | Digital governance | Task / issue / plan item | `SRC-A-058`, `SRC-A-073` | Links schedule objects to models, drawings, issues, or locations. |
| `PRP-052` | Task commitment state | Collaborative production control | Task / plan item | `SRC-A-058` | Distinguishes committed tasks from ordinary planned tasks. |
| `PRP-053` | Percent Plan Complete (PPC) | Collaborative production metric | Plan / crew / period | `SRC-A-058` | Important field-planning metric rarely visible in classical CPM sources. |
| `PRP-054` | Root cause of delay / failure reason | Report / log / analytics | Task / plan item | `SRC-A-058` | Strong report-log layer property in modern collaborative tools. |
| `PRP-055` | Audit timestamp / actor / old-new value | Governance / audit | Change event / schedule object | `SRC-A-047`, `SRC-A-059` | Makes schedule changes traceable at object or version level. |
| `PRP-056` | Custom calendar selection | Time model | Task / schedule sheet / project | `SRC-A-047`, `SRC-A-052` | Important beyond classic project calendars because some tools assign calendars per governed container. |
| `PRP-057` | Work pattern / dominant work pattern | Time model | Calendar / task | `SRC-A-052` | Stronger time-model detail than a simple working/non-working calendar. |
| `PRP-058` | Resource group / crew group reference | Resource | Task / plan / issue | `SRC-A-060`, `SRC-A-073` | Collaborative systems often group resources at the team level rather than individual-level loading only. |
| `PRP-059` | Role assignment | Responsibility / governance | Task / assignment / project | `SRC-A-045`, `SRC-A-047` | Important in cloud and document-system platforms. |
| `PRP-060` | Note category / activity note | Report / log | Activity / status entry | `SRC-A-057` | Confirms that note categories are part of structured data mapping, not only free text. |
| `PRP-061` | Control account / work package link | Control hierarchy | Activity / work package | `SRC-A-056`, `SRC-A-057` | Strongly relevant for enterprise cost-schedule integration. |
| `PRP-062` | Schedule sheet / template reference | Document-system | Task / schedule / project | `SRC-A-047`, `SRC-A-048` | Key property when the schedule lives in a governed sheet system. |
| `PRP-063` | Grouping / filter dimension | Reporting / coding | Task / issue / schedule view | `SRC-A-068`, `SRC-A-060`, `SRC-A-067` | Important for how end users actually navigate the schedule. |
| `PRP-064` | Parent issue / parent task / summary parent reference | Hierarchy | Issue / task | `SRC-A-068`, `SRC-A-069`, `SRC-A-060` | Shows schedule structure may be expressed through issue hierarchies as well as WBS. |
| `PRP-065` | External document hyperlink | Digital linkage | Task / custom record | `SRC-A-055` | Important in extended document-system models and digital-governance contexts. |
| `PRP-066` | Earned value / performance measure | Cost-control / analysis | Task / work package / project | `SRC-A-078`, `SRC-A-082`, `SRC-A-087` | Academic and owner practice both confirm that schedule control often couples with EV-style measures. |
| `PRP-067` | Planned versus actual expenditure linkage | Cost-control / reporting | Task / package / project | `SRC-A-078`, `SRC-A-095`, `SRC-A-105` | Strong bridge between schedule control and enterprise cost reporting. |
| `PRP-068` | KPI submission period / contractor KPI record | Governance / reporting | Contract / package / period | `SRC-A-105`, `SRC-A-108` | PMIS-led owner systems frequently require periodic KPI submissions. |
| `PRP-069` | Handover readiness / completion status | Delivery governance | System / package / project | `SRC-A-097`, `SRC-A-111`, `SRC-A-115` | Important because enterprise practice governs completion and readiness explicitly. |
| `PRP-070` | Revision / checker / approver metadata | Document-system / governance | Document / schedule / submittal | `SRC-A-098`, `SRC-A-106`, `SRC-A-100` | Important for controlled environments where schedule-linked documents are formally reviewed. |
| `PRP-071` | Interface / stakeholder dependency reference | Governance / logic | Task / package / milestone | `SRC-A-094`, `SRC-A-097`, `SRC-A-116` | Enterprise megaprojects often manage dependencies at interface and handover boundaries, not only task-to-task logic. |
| `PRP-072` | PMIS / system-of-record reference | Digital governance | Task / package / report / issue | `SRC-A-105`, `SRC-A-099`, `SRC-A-115` | Important where the authoritative operational state lives in PMIS rather than the planning file itself. |
| `PRP-073` | Engineering firm classification / grade | Governance / authority | Firm / contractor / consultant | `SRC-A-120`, `SRC-A-121`, `SRC-A-123` | Important where eligibility and evaluation are tied to classification status. |
| `PRP-074` | Completion-certificate planned vs actual reference | Completion governance | Project / contract / system | `SRC-A-121` | Important because authority-side evaluation can compare planned and actual completion evidence. |
| `PRP-075` | Professional qualification / engineer competency status | Governance / professionalization | Engineer / role / organization | `SRC-A-120`, `SRC-A-123` | Important where regulated qualification affects who can participate in delivery. |
| `PRP-076` | Permit-platform transaction / workflow state | Digital governance / authority | Project / permit / package | `SRC-A-122`, `SRC-A-123` | Important where digital permit platforms become part of project and compliance workflow. |
| `PRP-077` | Workflow step / current assignee / ball-in-court | Workflow governance | PMIS record / document / approval case | `SRC-A-126`, `SRC-A-128`, `SRC-A-135` | Strong Stage 23 property because runtime ownership is explicit in enterprise workflow systems. |
| `PRP-078` | Workflow due date / SLA / time allowed | Workflow governance | Workflow step / review / approval | `SRC-A-128`, `SRC-A-135` | Important because review timing is often managed per step rather than only by overall finish date. |
| `PRP-079` | Shell / workspace / project-context reference | Enterprise container | Record / document / schedule / dashboard | `SRC-A-125`, `SRC-A-127`, `SRC-A-141` | Key PMIS and resource-planning bridge property. |
| `PRP-080` | Cost-sheet code / fund row / ledger reference | Commercial / PMIS | Cost record / change / payment item | `SRC-A-125`, `SRC-A-126`, `SRC-A-105` | Important where cost and funding state live in structured sheets or ledgers. |
| `PRP-081` | Document number / revision / status triad | Document-system | Document register entry / transmittal line | `SRC-A-129`, `SRC-A-130`, `SRC-A-136` | Canonical EDMS property cluster. |
| `PRP-082` | Transmittal reason / sender / recipient / distribution metadata | Document governance | Transmittal / mail / workflow | `SRC-A-129`, `SRC-A-132`, `SRC-A-136` | Important because transfer context affects traceability and obligations. |
| `PRP-083` | Regulatory gateway / authority / submission type | Permit governance | Permit case / submission package | `SRC-A-149`, `SRC-A-150`, `SRC-A-122` | Important where approval routing depends on gateway and agency. |
| `PRP-084` | Submission fee / proof-of-payment / finance verification status | Permit / authority | Permit case / fee record | `SRC-A-149`, `SRC-A-150` | Important because unverified payments can delay authority processing. |
| `PRP-085` | Review-comment disposition / resubmission count | Review governance | Permit case / document workflow / submittal | `SRC-A-128`, `SRC-A-149`, `SRC-A-150` | Captures iterative review loops rather than one-pass approval assumptions. |
| `PRP-086` | Observation type / severity / assignee / due date | Smart-site / field governance | Observation / issue / daily log item | `SRC-A-137`, `SRC-A-140`, `SRC-A-152` | Strong property cluster for field event control. |
| `PRP-087` | Sensor threshold / alert status / event timestamp | Digital monitoring | Sensor / alert / cockpit record | `SRC-A-102`, `SRC-A-152`, `SRC-A-153` | Important because smart-site alerts often rely on thresholds and event timing. |
| `PRP-088` | Resource request role / quantity / date window | Resource planning | Request / assignment candidate | `SRC-A-141`, `SRC-A-145` | Important because demand is time-bounded and role-specific. |
| `PRP-089` | Resource availability / max units / overallocation indicator | Resource capacity | Resource / pool / assignment | `SRC-A-142`, `SRC-A-143`, `SRC-A-144` | Core capacity-management property cluster. |
| `PRP-090` | Skill / tag / certification / assignable-user status | Resource governance | Person / crew / resource profile | `SRC-A-141`, `SRC-A-153` | Important where assignment feasibility depends on competency and user state. |
| `PRP-091` | Billing period / SOV amount / billed-to-date / retainage / net due | Commercial | Payment application / requisition / invoice line | `SRC-A-131`, `SRC-A-139`, `SRC-A-148` | Strong commercial-engine property cluster. |
| `PRP-092` | Hold reason / compliance status / waiver state | Commercial governance | Payment / invoice / subcontract record | `SRC-A-146`, `SRC-A-147` | Important because payment eligibility often depends on legal-document compliance. |
| `PRP-093` | Change-event budget impact / cost impact / linked change-order status | Commercial change governance | Change event / exposure / change order | `SRC-A-134` | Important because commercial state often matures through exposure before approval. |
