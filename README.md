# San Diego Palm Protection Website

Authoritative static source for `https://www.sandiegopalmprotection.com`, deployed through Vercel from this repository.

## Build and validation

Core HTML pages are generated from `scripts/build_core_pages.py`. Palm Journal pages and the sitemap are generated from `journal-data/`. Vercel deploys only the allowlisted `dist/` output produced by `scripts/build-production.mjs`.

```powershell
python scripts/sync_business_credentials.py
python scripts/build_core_pages.py
python scripts/build_journal.py
python scripts/validate_active_service_state.py --self-test
node scripts/build-production.mjs
python scripts/validate_operational_status.py
python scripts/validate_site.py
python scripts/validate_production_claims.py
```

Vercel runs the production build declared in `vercel.json` and serves `dist/`. The build rejects treatment-unavailable regressions and missing operational/commercial markers before an artifact can deploy.

## Sources of truth

- Business/compliance status and approved public credential wording: `site-config/business_status.json`
- Credential rendering and synchronization: `scripts/business_credentials.py` and `scripts/sync_business_credentials.py`
- Palm Journal records: `journal-data/journal_entries.json`
- Approved Journal article bodies: `journal-data/articles/`
- Journal, Documented Loss, and sitemap generation: `scripts/build_journal.py`
- Redirects and headers: `vercel.json`

Do not hand-edit generated files or duplicate credential wording. Update the controlling source and regenerate.
