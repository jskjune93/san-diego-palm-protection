# Palm Journal Data

This folder is the local source of truth for the static Palm Journal architecture.

- `journal_entries.json` contains one record per journal item.
- `articles/*.html` contains approved article body HTML for records with `page: true`.
- Run `python scripts/build_journal.py` after changing records or article snippets.
- Run `python scripts/validate_site.py` before committing.

Commercial mode is the only production mode under `site-config/business_status.json`. The backward-compatible validation command now enforces active licensing and rejects former restrictive language. Palm Journal source fragments may discuss pests, treatment history, pruning, or removal in educational or historical context, but must preserve diagnostic, label, licensing-scope, and outcome boundaries.

Keep draft or unapproved content out of public output by leaving `status` as `draft` until owner approval.
