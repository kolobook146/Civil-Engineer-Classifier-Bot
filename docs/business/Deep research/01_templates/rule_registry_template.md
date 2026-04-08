# Rule Registry Template

## Required Fields

| Field | Description |
| --- | --- |
| `rule_id` | Stable unique identifier. |
| `rule_name` | Canonical rule name. |
| `rule_kind` | Structural, computational, governance, contractual, reporting, update, coding. |
| `scope` | Universal, regional, software-specific, institution-specific, project-specific. |
| `trigger_or_context` | When the rule applies. |
| `rule_statement` | Short formal description. |
| `affected_entities` | Entities affected by the rule. |
| `source_ids` | Supporting sources. |
| `notes` | Differences, constraints, or caveats. |

## Rule Card Template

```md
### {rule_id} - {rule_name}

- Rule kind:
- Scope:
- Trigger or context:
- Rule statement:
- Affected entities:
- Evidence:
- Exceptions or caveats:
- Notes:
```
