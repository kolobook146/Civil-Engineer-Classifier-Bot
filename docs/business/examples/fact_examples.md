# Fact Examples

Status: illustrative examples.

## Example 1: Physical Execution Fact

Raw text:
`Poured 173.17 m3 of concrete in section A.`

Structured interpretation:
- `volume`: 173.17
- `unit`: m3
- `function`: Construction Execution
- `stage`: Execution
- `work_type`: Concreting

## Example 2: Procurement Fact

Raw text:
`Issued tender package for ventilation equipment.`

Structured interpretation:
- `volume`: empty
- `unit`: empty
- `function`: Material & Technical Supply
- `stage`: Tender
- `work_type`: empty

## Example 3: Permit/Approval Fact

Raw text:
`Authority comments resolved, package sent for approval.`

Structured interpretation:
- `volume`: empty
- `unit`: empty
- `function`: Permits & Authority Approvals
- `stage`: Approvals
- `work_type`: empty
