# Business status and public claims

`site-config/business_status.json` is the authoritative website source for operating status and public wording.

Current owner-confirmed operational status, effective August 2, 2026:

- John Krause is the owner.
- California Qualified Applicator License No. 175295 is active.
- Category B — Landscape Maintenance.
- San Diego Palm Protection's California Pest Control Business License is active. No business-license number is published because none is recorded in the repository's authoritative status file.
- SDPP is insured and provides palm assessment, monitoring, documentation, protection and pesticide treatment services as applicable.
- Recurring stewardship is available for residential and managed properties.
- Treatment remains subject to the pesticide label, applicable law, site conditions, agreed scope, and job-specific preflight.

The public site uses:

- **Status label:** “Owner-led palm care”
- **Service summary:** Owner-led palm portfolio stewardship for managed properties and valuable mature palms, including individual-palm records, recurring care planning, licensed treatment when appropriate, documentation, decline response, and qualified-contractor coordination.
- **Primary growth path:** Managed-property palm portfolios with stable identities, condition and service histories, recurring plans, licensed treatment within scope, and coordinated next action.
- **Residential path:** Selective assessment, protection, treatment, and recurring care for mature and valuable palms.

Every public page uses this synchronized statement:

> San Diego Palm Protection — California Pest Control Business License active. John Krause, California Qualified Applicator License No. 175295, Category B — Landscape Maintenance. Insured.

## Owner workflow

1. Verify any status change against authoritative business records.
2. Update `site-config/business_status.json` only after owner authorization.
3. Run `python scripts/sync_business_credentials.py`.
4. Regenerate core pages and the Palm Journal.
5. Build the production allowlist.
6. Run `python scripts/validate_site.py` and `python scripts/validate_production_claims.py`.
7. Review visible copy, metadata, structured data, forms, footers, and generated pages before deployment.

Never manually edit generated status blocks between the `BUSINESS_CREDENTIALS` markers.
