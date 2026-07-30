# Business status and public claims

`site-config/business_status.json` is the authoritative website source for operating status and public wording.

Current owner-confirmed prelicense status, effective July 26, 2026:

- California Pest Control Business License: inactive / not issued
- DPR Qualified Applicator License, Category B: not represented as issued or active without independent verification
- Financial responsibility / applicable insurance: not represented as active without independent verification
- Protection and treatment services: available as applicable
- Job-specific application preflight: remains required for any future activation

The public site uses:

- **Status label:** “Current service scope”
- **Service summary:** “Documentation, monitoring, reporting, sourcing, and coordination are available now.”
- **Current services:** Palm assessments, monitoring, documentation, protection and treatment services, decline response, and removal or contractor coordination as applicable.

Public copy identifies John Krause as the owner, states his California Qualified Applicator License No. 175295 and Category B — Landscape Maintenance credential, and states that SDPP is insured.

## Owner workflow

1. Verify any status change against authoritative business records.
2. Update `site-config/business_status.json` only after owner authorization.
3. Run `python scripts/sync_business_credentials.py`.
4. Regenerate core pages and the Palm Journal.
5. Build the production allowlist.
6. Run `python scripts/validate_site.py` and `python scripts/validate_production_claims.py`.
7. Review visible copy, metadata, structured data, forms, footers, and generated pages before deployment.

Never manually edit generated status blocks between the `BUSINESS_CREDENTIALS` markers.
