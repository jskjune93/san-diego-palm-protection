# Business credentials and public claims

`site-config/business_status.json` is the authoritative website source for operating status and public credential wording.

Current owner-authorized commercial status, effective July 22, 2026:

- California Pest Control Business License: issued and active
- DPR Qualified Applicator License, Category B: issued and active
- Financial responsibility / applicable insurance: active
- County registration and operating-readiness gates: current
- Job-specific application preflight: always required

The public site therefore uses:

- **Plain-language status:** “California licensed, qualified, and insured”
- **Service summary:** “DPR Qualified Applicator License (QAL), Category B · Insured”
- **Exact status:** “DPR Qualified Applicator License (QAL) #175295, Category B, active · Insured”

The site must not collapse the business license, individual QAL qualification, insurance, and job-specific authorization into one ambiguous claim. It must not imply that insurance guarantees outcomes. Regulated work remains subject to the product label, site conditions, licensing scope, and job-specific preflight.

## Owner workflow

1. Verify any status change against authoritative business records.
2. Update `site-config/business_status.json` only after owner authorization.
3. Run `python scripts/sync_business_credentials.py`.
4. Run `python scripts/build_journal.py`.
5. Run `python scripts/validate_site.py`.
6. Review visible copy, metadata, structured data, forms, footers, and generated pages before deployment.

Never manually edit the generated credential blocks between the `BUSINESS_CREDENTIALS` markers.
