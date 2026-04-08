# Planned Cost Reference

Status: normative pilot reference for `Planned Cost` assignment in the schedule workbook.

## Purpose

This document defines how `Planned Cost` should be assigned in the pilot baseline and current schedule surfaces.
It is not a controlled dictionary.
It is a reference catalog for:

- cost basis;
- cost attribution logic;
- anti-double-counting rules;
- indicative cost ranges used for expert row-level population.

## Cost Basis

The pilot uses:

- `Global USD 2026`
- typical residential high-rise
- `2 residential sections`
- about `48,000 m2 GFA`

This is a normalized business basis rather than a country-specific estimate.
It is intentionally suitable for a portable pilot baseline, not for tendering or formal BOQ pricing.

## Allocation Logic

The pilot uses a `hybrid split` model.

### Delivery / service rows

These rows may carry direct service cost when the row itself represents paid scope:

- engineering surveys;
- concept and design packages;
- expert review / compliance support;
- permit and authority fee-bearing actions;
- utility-interface support;
- mobilization or logistics support when budgeted as a direct line item;
- commissioning and handover services.

### Procurement rows

These rows may carry the supply-heavy cost share of selected packages when that avoids double counting later in execution.

Typical candidates:

- facade package supply portion;
- power-supply equipment and material package;
- finishing material package;
- other long-lead or equipment-heavy package rows.

### Execution rows

These rows carry direct installation / site-execution cost.
Where no earlier procurement row carries a separated supply share, the execution row may carry the full direct scope cost.

### Tender / contract / payment / control rows

Default treatment:

- `Planned Cost = 0`

Exception:

- if the row itself represents a paid direct service or fee.

### WBS rows

Pilot treatment:

- `Planned Cost = blank`

## Anti-Double-Counting Rules

- If a procurement row carries a package supply share, the related execution rows must carry installation / site-execution share only.
- If no procurement row carries separated supply cost for that work type, the execution rows may carry full direct cost.
- Gates, pure approvals, and pure internal control checkpoints must not be used as hidden budget containers.
- Internal management effort is not fully loaded into every row. Only direct task-level cost is assigned in the pilot.

## Zero-Cost Row Classes

Use `0` for rows that are actionable but do not represent standalone direct spend:

- pure control checkpoints;
- pure gates;
- pure internal approval events;
- pure payment release events;
- pure contract-signature events;
- pure PM coordination rows without external paid support.

Use blank only for:

- `wbs` rows;
- rows intentionally excluded from cost treatment pending later modeling.

## Physical Work-Type Reference

Indicative direct-cost ranges below are suitable for expert pilot population.
They are not formal estimate norms.

| Work Type | Representative Row | Typical Cost Layer | Unit | Reference Cost Range (USD 2026) | Recommended P01 Bias | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `Earthworks` | Excavation | full direct scope | `m3` | `18-28` | lower-mid | Typical open site excavation. |
| `Earthworks` | Haulage of excavated material | full direct scope | `t` | `8-16` | mid | Includes loading and disposal haul cycle. |
| `Earthworks` | Backfill | full direct scope | `m3` | `12-20` | mid | Includes handling and placement. |
| `Earthworks` | Soil compaction | full direct scope | `m2` | `3-7` | mid | Area-based finish layer treatment. |
| `Piling` | Piles installation | full direct scope | `m` | `300-650` | mid | Depends on pile type and depth. |
| `Piling` | Pile reinforcement | full direct scope | `t` | `950-1600` | mid | Includes material and fixing in pilot terms. |
| `Piling` | Pile concrete | full direct scope | `m3` | `160-280` | mid | Direct placed concrete basis. |
| `Piling` | Pile testing | service / specialist scope | `pcs` | `1500-4000` | mid | Testing and reporting service. |
| `Foundation works` | Blinding concrete | full direct scope | `m3` | `110-180` | mid | Lean concrete base layer. |
| `Foundation works` | Reinforcement | full direct scope | `t` | `950-1600` | mid | Includes material and installation. |
| `Foundation works` | Formwork | full direct scope | `m2` | `35-70` | mid | Repetitive RC foundation works. |
| `Foundation works` | Concrete placement | full direct scope | `m3` | `170-300` | mid | Includes placing and vibrating. |
| `Foundation works` | Protection layer | full direct scope | `m2` | `10-22` | lower-mid | Protection board / layer basis. |
| `Waterproofing` | Primer | full direct scope | `m2` | `3-7` | mid | Thin preparatory layer. |
| `Waterproofing` | Membrane | full direct scope | `m2` | `18-35` | mid | Includes material and application. |
| `Waterproofing` | Protection layer | full direct scope | `m2` | `8-18` | mid | Pilot direct cost basis. |
| `Concreting` | Structural reinforcement | hybrid: execution-heavy | `t` | `900-1450` | mid | Use execution share only if package supply is separated elsewhere. |
| `Concreting` | Structural formwork | execution-heavy | `m2` | `45-90` | mid | Mostly site labor and reusable system effort. |
| `Concreting` | Structural concrete placement | hybrid: execution-heavy | `m3` | `180-320` | mid | Use lower half if concrete supply cost sits on procurement row. |
| `Steel structures` | Steel erection | execution-heavy | `t` | `700-1200` | mid | Supply may already sit on procurement row. |
| `Steel structures` | Bolted assemblies | execution-heavy | `pcs` | `20-60` | mid | Assembly and fixing effort. |
| `Steel structures` | Fire protection | full direct scope | `m2` | `15-35` | mid | Coating / protection application. |
| `Roofing` | Vapor barrier | full direct scope | `m2` | `4-8` | mid | Membrane preparatory layer. |
| `Roofing` | Insulation | full direct scope | `m2` | `18-35` | mid | Includes material and placement. |
| `Roofing` | Membrane | full direct scope | `m2` | `20-40` | mid | Waterproof final layer. |
| `Roofing` | Drainage items | full direct scope | `pcs` | `120-350` | mid | Roof drain fittings and placement. |
| `Building envelope` | Masonry works | full direct scope | `m3` | `100-220` | mid | Walling direct installed basis. |
| `Building envelope` | Envelope wall system installation | full direct scope | `m2` | `55-110` | mid | Excludes high-end facade package scope. |
| `Windows` | Window units installation | full direct scope | `pcs` | `350-900` | mid | Installed unit basis. |
| `Windows` | Window glazing area | full direct scope | `m2` | `90-220` | mid | Area-based glazing component. |
| `Windows` | Perimeter sealing | full direct scope | `m` | `4-12` | mid | Sealant and labor. |
| `Facade works` | Facade brackets installation | execution-heavy | `pcs` | `30-80` | mid | Supply share may sit on procurement row. |
| `Facade works` | Facade insulation installation | execution-heavy | `m2` | `22-45` | mid | Installation-oriented share. |
| `Facade works` | Facade cladding / glazing installation | execution-heavy | `m2` | `90-220` | mid | Use execution share only if package supply is separated. |
| `Doors` | Door sets installation | full direct scope | `pcs` | `350-1200` | mid | Installed direct basis. |
| `Doors` | Frames and hardware installation | full direct scope | `pcs` | `60-180` | mid | Fittings and installation. |
| `Doors` | Door perimeter sealing | full direct scope | `m` | `4-12` | mid | Seal and firestopping basis. |
| `Elevators` | Guide rails | execution-heavy | `m` | `45-110` | mid | Installation basis. |
| `Elevators` | Elevator equipment | hybrid equipment-heavy | `pcs` | `90000-180000` | mid | Use lower portion if major supply sits elsewhere. |
| `Elevators` | Commissioning set | service scope | `set` | `15000-35000` | mid | Specialist service basis. |
| `Power supply` | Trays and conduits | execution-heavy | `m` | `12-35` | mid | Installation share. |
| `Power supply` | Cable laying | execution-heavy | `m` | `8-22` | mid | Installation share. |
| `Power supply` | Panels and switchboards | hybrid equipment-heavy | `pcs` | `1500-7000` | mid | Use execution share if equipment supply is separated. |
| `Power supply` | Testing | service scope | `system` | `15000-45000` | mid | Testing and records. |
| `Low-current systems` | Cable laying | full direct scope | `m` | `6-16` | mid | Full direct when no package split exists. |
| `Low-current systems` | Devices | full direct scope | `pcs` | `40-250` | mid | Device installation basis. |
| `Low-current systems` | Cabinets and racks | full direct scope | `pcs` | `600-4000` | mid | Supply + install in pilot terms. |
| `Low-current systems` | Testing | service scope | `system` | `10000-30000` | mid | Integration and test support. |
| `Water supply` | Piping | full direct scope | `m` | `18-40` | mid | Installed piping basis. |
| `Water supply` | Fittings and valves | full direct scope | `pcs` | `20-120` | mid | Direct installed basis. |
| `Water supply` | Fixtures | full direct scope | `pcs` | `120-600` | mid | Pilot installed direct basis. |
| `Water supply` | Testing | service scope | `system` | `5000-15000` | mid | Pressure / acceptance tests. |
| `Sewerage` | Piping | full direct scope | `m` | `20-45` | mid | Installed direct basis. |
| `Sewerage` | Fittings / manholes | full direct scope | `pcs` | `80-600` | mid | Depends on element type. |
| `Sewerage` | Testing | service scope | `system` | `4000-12000` | mid | Testing and records. |
| `Heating` | Piping | full direct scope | `m` | `22-55` | mid | Installed direct basis. |
| `Heating` | Terminal units | full direct scope | `pcs` | `150-700` | mid | Radiator / FCU class mix. |
| `Heating` | Balancing | service scope | `system` | `8000-25000` | mid | Specialist commissioning service. |
| `Ventilation` | Ducts | full direct scope | `m2` | `35-90` | mid | Fabrication + installation pilot basis. |
| `Ventilation` | Air terminals | full direct scope | `pcs` | `45-200` | mid | Installed direct basis. |
| `Ventilation` | Equipment | full direct scope | `pcs` | `2000-15000` | mid | Moderate equipment class. |
| `Ventilation` | Balancing | service scope | `system` | `12000-30000` | mid | Test and balancing service. |
| `Air conditioning` | Piping | full direct scope | `m` | `20-55` | mid | Installed piping basis. |
| `Air conditioning` | Equipment | full direct scope | `pcs` | `1500-12000` | mid | Installed equipment basis. |
| `Air conditioning` | Insulation | full direct scope | `m` | `4-12` | mid | Pipe insulation basis. |
| `Gas supply` | Piping | full direct scope | `m` | `25-60` | mid | Installed direct basis. |
| `Gas supply` | Valves / regulators | full direct scope | `pcs` | `120-900` | mid | Direct installed basis. |
| `Gas supply` | Testing | service scope | `system` | `7000-20000` | mid | Acceptance and safety testing. |
| `Rough finishing` | Plastering | full direct scope | `m2` | `8-18` | mid | Direct installed basis. |
| `Rough finishing` | Screed | full direct scope | `m2` | `12-26` | mid | Direct installed basis. |
| `Rough finishing` | Suspended ceiling substrate | full direct scope | `m2` | `10-28` | mid | Substructure only. |
| `Final finishing` | Painting | execution-heavy | `m2` | `5-12` | mid | Use installation share where finish materials are split earlier. |
| `Final finishing` | Floor finish | execution-heavy | `m2` | `10-28` | mid | Material-heavy share may sit on procurement row. |
| `Final finishing` | Wall tiling | execution-heavy | `m2` | `18-45` | mid | Installation-oriented share. |
| `Final finishing` | Sanitary accessories | full direct scope | `pcs` | `80-300` | mid | Installed accessories basis. |
| `Landscaping` | Paving | full direct scope | `m2` | `25-60` | mid | External works basis. |
| `Landscaping` | Curbs | full direct scope | `m` | `12-30` | mid | Installed linear basis. |
| `Landscaping` | Topsoil | full direct scope | `m3` | `10-25` | mid | Soil placement basis. |
| `Landscaping` | Planting | full direct scope | `pcs` | `25-120` | mid | Tree/shrub mix basis. |

## Delivery and Governance Cost Reference

| Function | Stage | Typical Cost Nature | Reference Cost Basis | Recommended P01 Treatment | Notes |
| --- | --- | --- | --- | --- | --- |
| `Land & Cadastral Management` | `Initial data`, `State planning approvals` | legal / cadastral support | `30000-180000` per package | direct cost where row is an actual package; otherwise `0` | Use cost only on real external-service scope. |
| `Permits & Authority Approvals` | `State planning approvals`, `Approvals`, `Closeout & Handover` | permit fees / authority support | `20000-150000` per row | direct cost on fee-bearing rows | Gates stay `0`. |
| `Utility Connections Management` | `Initial data`, `Approvals`, `Execution`, `Closeout & Handover` | utility application / tie-in support | `20000-250000` per row | direct cost on application, tie-in, or acceptance rows | Internal coordination rows may be `0`. |
| `Engineering Surveys` | `Design and survey works` | specialist survey package | `150000-400000` per package | direct cost | Usually one of the clearer fee-bearing rows. |
| `Master Planning & Concept Development` | `Technical brief`, `Concept development` | concept and planning design services | `200000-900000` per row | direct cost | Split between brief and concept rows where relevant. |
| `Design Management` | `Technical brief`, `Design and survey works`, `Tender`, `Execution` | consultant design / clarification services | `50000-1500000` per row | direct cost on real consultant-deliverable rows, `0` on pure internal coordination rows | Detailed design row usually carries the largest share. |
| `Expert Review & Compliance` | `Approvals`, `Execution`, `Closeout & Handover` | expert review / compliance support | `25000-250000` per row | direct cost | Internal review checkpoint rows may be `0`. |
| `Project Management & Controls` | `Technical brief`, `Control`, `Closeout & Handover` | PM / controls support | `0-75000` per row | mostly `0`; use cost only where external PM service is explicit | Pilot avoids fully loading internal overhead. |
| `Investment & Financing` | `Technical brief`, `Contract`, `Advance payment`, `Control` | financial advisory / transaction support | `0-120000` per row | usually `0`, direct cost only where external advisory is explicit | Payment release events normally stay `0`. |
| `Legal & Contract Management` | `Tender`, `Contract`, `Advance payment` | tender/legal service support | `0-120000` per row | strategy or complex contract rows may carry direct service cost; simple events stay `0` | Do not load contract value here. |
| `Material & Technical Supply` | `Tender`, `Procurement`, `Advance payment`, `Execution` | procurement admin or supply package | `0` or package-specific | procurement rows may carry supply-heavy cost share | Use hybrid split carefully. |
| `Construction Execution` | `Contract`, `Execution`, `Closeout & Handover` | mobilization / physical execution / closeout support | row-specific | execution rows carry direct site scope; non-physical contract rows usually `0` | Mobilization may carry direct cost. |
| `Quality, HSE & Technical Supervision` | `Contract`, `Execution`, `Control`, `Closeout & Handover` | supervision / inspection / QA support | `10000-150000` per row | direct cost on real paid supervision rows, `0` on pure internal checkpoints | Use service logic. |
| `Commissioning & Handover` | `Execution`, `Control`, `Closeout & Handover` | testing / commissioning / handover support | `10000-200000` per row | direct cost on testing, commissioning, handover service rows | Handover event itself may still be `0`. |
| `Sales & Marketing` | `Technical brief`, `Concept development`, `Closeout & Handover` | product / customer readiness support | `0-80000` per row | usually `0`; use direct cost only for real customer-facing deliverables | Internal readiness rows can stay `0`. |

## Examples of Hybrid Split

### Facade package

- procurement row may carry:
  - supply-heavy facade package portion
- execution rows carry:
  - brackets installation
  - insulation installation
  - cladding / glazing installation as site-execution share

### Power supply package

- procurement row may carry:
  - equipment and material supply share
- execution rows carry:
  - trays / conduits
  - cable laying
  - panel installation effort

### Work type without separated procurement split

If no earlier procurement row carries supply cost, execution rows may carry the full direct cost.

Typical examples in the pilot:

- `Waterproofing`
- `Windows`
- `Doors`
- `Water supply`
- `Sewerage`
- `Heating`
- `Ventilation`
- `Landscaping`
