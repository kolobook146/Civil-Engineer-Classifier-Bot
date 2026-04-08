# Source Registry Template

## Required Fields

| Field | Description |
| --- | --- |
| `source_id` | Stable unique identifier. |
| `trust_level` | A, B, or C. |
| `source_kind` | Standard, regulation, handbook, software doc, university text, contract guide, paper, etc. |
| `curator_zone` | Institution and governance zone. |
| `country_or_region` | Primary country, region, or international scope. |
| `organization` | Issuing organization. |
| `title` | Official title. |
| `edition_or_version` | If stated. |
| `year_or_last_update` | If stated. |
| `link` | URL or stable document link. |
| `access_status` | Public, paywalled, summary-only, partial sample, etc. |
| `relevance_stages` | Research stages materially informed by the source. |
| `focus_topics` | What the source covers. |
| `evidence_strength_note` | Why it is useful and what its limits are. |

## Source Card Template

```md
### {source_id} - {title}

- Trust level:
- Source kind:
- Curator zone:
- Country / region:
- Organization:
- Edition / version:
- Year / last update:
- Link:
- Access status:
- Relevance stages:
- Focus topics:
- Evidence strength note:
- Extraction notes:
```
