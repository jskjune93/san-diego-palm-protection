# SDPP website guardrails

- Preserve the three service pillars: Monitoring & Documentation; Protection & Treatment; Response, Removal & Replacement.
- Treat `site-config/business_status.json` as the only source of truth for licensing, qualification, insurance, and service availability.
- Use `scripts/business_credentials.py` and `scripts/sync_business_credentials.py`; do not duplicate credential wording manually.
- Keep the Pest Control Business License, DPR Qualified Applicator License, insurance, and job-specific authorization conceptually separate.
- Never imply that insurance or licensing guarantees an outcome.
- Preserve diagnostic and certainty boundaries: observed, possible, consistent with, presumed, and confirmed only when supportable.
- Preserve the Machine/website boundary. Publish only approved, sanitized proof exports; never add private client data.
- Use the approved UFMP wording without implying endorsement: “San Diego Palm Protection submitted mature-palm documentation for consideration during the City of Escondido Urban Forest Management Plan process.”
- Do not create duplicate navigation or styling systems.
- Do not add a route without a clear role.
- Preserve valuable URLs, analytics, forms, redirects, Palm Journal, Documented Loss, sitemap, and robots behavior.
- Update Journal sources and generators rather than hand-editing generated pages.
- Render user-facing changes at 360×800, 390×844, 768×1024, 1366×768, and 1920×1080.
- Fix root causes and report every changed route and source file.
