# Palm Journal Data

This folder is the local source of truth for the static Palm Journal architecture.

- `journal_entries.json` contains one record per journal item.
- `articles/*.html` contains approved article body HTML for records with `page: true`.
- Run `python scripts/build_journal.py` after changing records or article snippets.
- Run `python scripts/validate_site.py` before committing.

Prelicense mode is active. After building, run `python scripts/validate_prelicense_compliance.py` as well. Palm Journal source fragments may discuss pests, treatment history, pruning, or removal in educational or historical context, but must not solicit treatment, pricing, booking, field-service visits, pruning, removal, installation, or pesticide applications by SDPP while prelicense mode remains active.

Keep draft or unapproved content out of public output by leaving `status` as `draft` until owner approval.
