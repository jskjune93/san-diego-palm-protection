# Palm Journal Architecture

The Palm Journal has been refactored from a single continuously expanding page into a static library plus individual article pages.

## Source of truth

- `journal-data/journal_entries.json` stores one structured record per journal entry.
- `journal-data/articles/*.html` stores approved article body HTML for entries that have an individual page.
- `scripts/build_journal.py` generates:
  - `palm-journal-new.html`
  - `palm-journal/*.html`
  - Palm Journal article URLs in `sitemap.xml`
- `scripts/validate_site.py` checks the generated architecture and broader site safety rules.

The generated files include a comment naming `scripts/build_journal.py`. Do not hand-edit generated journal pages unless the change is later moved back into the manifest or article snippet.

## Future entry workflow

1. Add a published article record to `journal-data/journal_entries.json`.
2. Add the approved article body to `journal-data/articles/<slug>.html`.
3. Confirm all image paths are public-safe and present in the website repository.
4. Run `python scripts/build_journal.py`.
5. Run `python scripts/validate_site.py`.
6. Review the generated diff before committing.

Commercial mode is currently active under the owner-authorized business-status configuration. Every Palm Journal build must still pass `python scripts/validate_prelicense_compliance.py`; the historical validator now acts as a fail-closed activation and claims gate, and `scripts/validate_site.py` runs it automatically. Keep Journal copy documentary and non-diagnostic, and preserve licensing, scope, certainty, and outcome boundaries.

Draft entries must remain `status: draft`; the build and validation workflow prevents draft records from appearing publicly.

## SDPP Machine integration later

The SDPP Machine should eventually write only to the journal source files after owner approval:

- add or update a single manifest record;
- add a matching article HTML snippet;
- place approved public-safe images in the website image convention;
- run the build and validation scripts;
- stop for owner review before commit, push, or deployment.

It should not edit generated article pages directly as the source of truth.

## Migration map

| Legacy anchor | New article slug | Decision | Notes |
| --- | --- | --- | --- |
| `classic-old-escondido-canary-island-date-palm` | `classic-old-escondido-canary-island-date-palm` | Individual page | Approved residential baseline record. |
| `monitoring-mature-cidp-after-palm-weevil-activity` | `monitoring-mature-cidp-after-palm-weevil-activity` | Individual page | Distinct dated monitoring note. |
| `old-escondido-mexican-fan-palm-curve` | `old-escondido-mexican-fan-palm-curve` | Individual page | Distinct Old Escondido fan palm observation. |
| `old-escondido-albert-h-beach-house-palms` | `old-escondido-albert-h-beach-house-palms` | Individual page | Historic property and mature palm context. |
| `old-escondido-cidp-icons-and-change` | `old-escondido-cidp-icons-and-change` | Individual page | Distinct photo set and neighborhood contrast. |
| `old-escondido-adult-sapw-declining-cidp` | `old-escondido-adult-sapw-declining-cidp` | Individual page | Distinct SAPW documentation. |
| `old-escondido-historic-canary-island-date-palm` | `old-escondido-historic-canary-island-date-palm` | Individual page | Preservation and historic landscape value. |
| `old-escondido-palm-weevils` | `old-escondido-palm-weevils` | Individual page | Distinct adult weevil documentation. |
| `poway-old-winery-cidp` | `poway-old-winery-cidp` | Individual page | Distinct Poway location and photo set. |
| `las-palmas-cidp` | none | Legacy library card only | Not promoted to a new article during this architecture task; future Las Palmas production entry requires separate approved copy. |
| `old-escondido-cidp-collection` | `old-escondido-cidp-collection` | Individual page | Broad but substantial Old Escondido photo collection. |
| `grand-ave-old_escondido` | `grand-ave-old-escondido` | Individual page | Legacy anchor retained on the library card; slug normalized for URL safety. |
| `grand-ave-cidp` | `grand-ave-cidp` | Individual page | Distinct historic district walk note. |
| `rancho-santa-fe-palm-walk` | `rancho-santa-fe-palm-walk` | Individual page | Former section had no public anchor; compatibility anchor added. |
| `healthy-palm-growth` | `healthy-palm-growth` | Individual page | Educational reference retained as a page. |
| `cidp-assessment-local-palm-health-concerns` | `cidp-assessment-local-palm-health-concerns` | Individual page | Former section had no public anchor; compatibility anchor added. |

## Retained resource cards

The old callout sections for the Old Escondido initiative, CIDP risk checklist, removal planning, and contact/photographic condition review actions were not migrated as journal articles. Their destinations remain available through the library navigation, related links, site navigation, or photographic condition review call to action.

## Redirect note

The existing site does not currently use per-anchor redirects. Legacy anchor compatibility is preserved by retaining anchor IDs on visible library cards. Cleaner redirects could be considered later only after testing the deployment configuration.
