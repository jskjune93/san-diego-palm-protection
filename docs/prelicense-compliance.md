# Prelicense Website Compliance Safeguard

This repository uses a conservative internal prelicense mode for the public San Diego Palm Protection website. It is a business-operating safeguard, not legal advice and not a substitute for agency confirmation.

## Purpose

Prelicense mode keeps the public site focused on palm documentation, photographic condition records, educational resources, Palm Journal field notes, and referral-oriented next-step questions while regulated or unavailable field services are disabled.

The current boundary is intentionally narrow: observation, photography, historical comparison, visible-condition documentation, and general education. There is no assumed blanket safe harbor for a commercial service called "palm monitoring," and the site should not present monitoring as a paid or currently available SDPP service.

## Allowed Content

- Palm Journal articles and historical field notes.
- Palm photography, neighborhood records, and visible-condition documentation.
- Educational South American palm weevil information.
- Non-diagnostic photographic observations, palm inventories, dated condition baselines, recurring photographic monitoring, written reports, and change-over-time comparisons.
- Owner-submitted photos for educational photographic context, without diagnosis or site-specific treatment recommendations.
- Historical comparison and ongoing photographic records.
- Recommendations to contact an appropriately licensed pest-control business, qualified arborist, or licensed tree contractor.
- Public-interest outreach that alerts a property owner or manager to visible palm changes.

## Blocked Content

While `mode` is `prelicense`, the public site must not advertise, solicit, quote, schedule, or imply that SDPP currently performs pesticide applications, pest-control treatment, SAPW treatment, treatment plans, pruning, removal, stump grinding, installation, planting, field maintenance, contracting, subcontracting, or sold removal coordination.

The site also must not claim SDPP is licensed, certified, insured, credentialed, or authorized unless those credentials are explicitly verified and configured.

The site also must not offer professional inspections, pest diagnoses, pesticide consultations, site-specific pesticide prescriptions, treatment recommendations, future or contingent treatment appointments, treatment waitlists, deposits, or "book after licensing" language. Current records, monitoring, and verification services must remain limited to observable conditions, supplied documents, and apparent completion within SDPP's qualifications.

## Configuration

The source of truth is `site-config/business_status.json`.

Passing an individual exam or completing one business prerequisite must not automatically change the website status. QAL issuance alone is not enough. Any future transition requires an explicit owner-controlled update after these fields are true:

- `qal_issued_and_active`
- `pest_control_business_license_issued_and_active`
- `financial_responsibility_active`
- `workers_compensation_requirement_addressed`
- `county_registration_current`
- `equipment_registered_and_ready`
- `reporting_system_ready`
- `storage_transport_ppe_systems_ready`
- `label_sds_notice_consent_emergency_systems_ready`
- `owner_activation_approved`

The permanent requirement `job_application_preflight_required` must remain true. It means every future application requires a separate site, product, label, permit, notice, consent, PPE, weather, emergency, and recordkeeping preflight before work. This website validator does not implement that job-management system; it only prevents the public site from activating regulated-service claims without the policy gate.

`workers_compensation_requirement_addressed` means compliant coverage is active when required, or a legitimate no-employees status has been explicitly verified. Lack of a workers' compensation policy is not automatic compliance.

## Validator

Run:

```powershell
python scripts/validate_prelicense_compliance.py
python scripts/validate_prelicense_compliance.py --self-test
```

The validator reads `site-config/business_status.json`, scans public HTML, generated Palm Journal pages, `journal-data/journal_entries.json`, and Palm Journal source article fragments. It blocks transactional patterns involving treatment offers, pricing, booking, quotes, unavailable field services, monitoring-as-service, professional inspection solicitations, photo-based treatment recommendations, contingent treatment offers, false credential claims, and disabled Offer/Service structured data.

It also validates the activation contract. Regulated-service flags fail if any required readiness field is false, owner activation is absent, or the permanent job/application preflight requirement is disabled. QAL issuance by itself is explicitly insufficient.

The validator supports narrow allowlisting with `PRELICENSE_ALLOW` only for context that cannot be reliably inferred and has been owner-reviewed. Prefer clearer public copy over allowlisting.

## Future SDPP Machine Integration

Future SDPP Machine draft-generation workflows should read the same business status before producing website copy, GBP posts, Nextdoor posts, or email drafts. In prelicense mode, generated copy should describe documentation, education, visible observations, historical comparison, photographic records, and referral questions, not monitoring services, site-specific treatment recommendations, unavailable treatment, or field-service claims.

## Required Build Gate

Every future website content build must pass:

```powershell
python scripts/build_journal.py
python scripts/validate_prelicense_compliance.py
python scripts/validate_site.py
```

`scripts/validate_site.py` also runs the prelicense validator, so normal validation fails if the site drifts back into unavailable service offers.

## Public Copy Cleanup Notes

Public pages should describe current SDPP activity as documentation, photographic records, educational photo review, preservation decision planning, removal decision planning, contractor questions, referrals to licensed providers, Palm Journal field notes, Old Escondido preservation work, and CIDP checklist education.

Until the regulated-service configuration is intentionally activated, avoid copy that presents SDPP as performing treatments, providing professional pesticide or arboricultural care, selling removal or installation work, or providing site-specific pesticide or treatment recommendations. Non-regulated documentation visits, condition baselines, recurring photographic monitoring, reports, sourcing guidance, and owner-side work records are permitted when their limits are stated clearly.

Palm Journal entries with `public: false` or `page: false` may remain in the manifest as source records, but they must not render in the public Journal index or generate public article pages. Generated article pages should contain one prelicense scope notice only.
