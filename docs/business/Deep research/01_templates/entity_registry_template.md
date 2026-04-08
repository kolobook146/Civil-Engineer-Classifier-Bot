# Entity Registry Template

## Required Fields

| Field | Description |
| --- | --- |
| `entity_id` | Stable unique identifier. |
| `canonical_name` | Canonical entity name used in this research corpus. |
| `entity_class` | Task, milestone, dependency, calendar, code, document, view, baseline, etc. |
| `universality_status` | Universal, frequent, regional, software-specific, emerging. |
| `representation_forms` | Ways the entity appears across sources. |
| `main_functions` | Why the entity exists in schedule practice. |
| `source_ids` | Sources where the entity appears. |
| `notes` | Clarifications, differences, caveats. |

## Entity Card Template

```md
### {entity_id} - {canonical_name}

- Entity class:
- Universality status:
- Representation forms:
- Main functions:
- Typical fields or attributes:
- Common schedule contexts:
- Source IDs:
- Notes:
```
