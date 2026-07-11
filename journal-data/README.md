# Palm Journal Data

This folder is the local source of truth for the static Palm Journal architecture.

- `journal_entries.json` contains one record per journal item.
- `articles/*.html` contains approved article body HTML for records with `page: true`.
- Run `python scripts/build_journal.py` after changing records or article snippets.
- Run `python scripts/validate_site.py` before committing.

Keep draft or unapproved content out of public output by leaving `status` as `draft` until owner approval.
