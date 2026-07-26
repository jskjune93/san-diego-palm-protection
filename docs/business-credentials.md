# Business status and public claims

`site-config/business_status.json` is the authoritative website source for operating status and public wording.

Current owner-confirmed prelicense status, effective July 26, 2026:

- California Pest Control Business License: inactive / not issued
- DPR Qualified Applicator License, Category B: not represented as issued or active without independent verification
- Financial responsibility / applicable insurance: not represented as active without independent verification
- Commercial pesticide treatment: disabled
- Job-specific application preflight: remains required for any future activation

The public site uses:

- **Status label:** “Current service scope”
- **Service summary:** “Documentation, monitoring, reporting, sourcing, and coordination are available now.”
- **Exact status:** “SDPP is not currently offering pesticide applications.”

Passing an examination does not establish that a QAL has been issued. The site must not collapse examination results, business licensing, individual QAL status, insurance, and job-specific authorization into one ambiguous claim. Prelicense pages may provide general educational treatment information but must not advertise, solicit, quote, book, or accept deposits for pesticide applications.

## Owner workflow

1. Verify any status change against authoritative business records.
2. Update `site-config/business_status.json` only after owner authorization.
3. Run `python scripts/sync_business_credentials.py`.
4. Regenerate core pages and the Palm Journal.
5. Build the production allowlist.
6. Run `python scripts/validate_site.py` and `python scripts/validate_production_claims.py`.
7. Review visible copy, metadata, structured data, forms, footers, and generated pages before deployment.

Never manually edit generated status blocks between the `BUSINESS_CREDENTIALS` markers.
