# Palm Journal Data

This folder is the local source of truth for the static Palm Journal architecture.

- `journal_entries.json` contains one record per journal item.
- `articles/*.html` contains approved article body HTML for records with `page: true`.
- Run `python scripts/build_journal.py` after changing records or article snippets.
- Run `python scripts/validate_site.py` before committing.

Commercial mode is active under `site-config/business_status.json`. The historical prelicense validator remains a fail-closed compliance gate and validates the activation contract. Palm Journal source fragments may discuss pests, treatment history, pruning, or removal in educational or historical context, but must preserve diagnostic, licensing, scope, and outcome boundaries.

Keep draft or unapproved content out of public output by leaving `status` as `draft` until owner approval.
