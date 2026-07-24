# San Diego Palm Protection Website

Authoritative static source for `https://www.sandiegopalmprotection.com`, deployed through Vercel from this repository.

## Build and validation

The root HTML pages are hand-maintained. Palm Journal pages and the sitemap are generated from `journal-data/`.

```powershell
python scripts/sync_business_credentials.py
python scripts/build_journal.py
python scripts/validate_prelicense_compliance.py --self-test
python scripts/validate_site.py
```

Vercel serves the static repository according to `vercel.json`; there is no package manager or compilation step.

## Sources of truth

- Business/compliance status and approved public credential wording: `site-config/business_status.json`
- Credential rendering and synchronization: `scripts/business_credentials.py` and `scripts/sync_business_credentials.py`
- Palm Journal records: `journal-data/journal_entries.json`
- Approved Journal article bodies: `journal-data/articles/`
- Journal, Documented Loss, and sitemap generation: `scripts/build_journal.py`
- Redirects and headers: `vercel.json`

Do not hand-edit generated files or duplicate credential wording. Update the controlling source and regenerate.
