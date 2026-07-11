# Prelicense Website Compliance Safeguard

This repository uses a conservative internal prelicense mode for the public San Diego Palm Protection website. It is a business-operating safeguard, not legal advice and not a substitute for agency confirmation.

## Purpose

Prelicense mode keeps the public site focused on palm documentation, photographic condition records, educational resources, Palm Journal field notes, and referral-oriented next-step questions while regulated or unavailable field services are disabled.

## Allowed Content

- Palm Journal articles and historical field notes.
- Palm photography, neighborhood records, and visible-condition documentation.
- Educational South American palm weevil information.
- Non-diagnostic photographic observations.
- Owner-submitted photos for an educational first look.
- Recommendations to contact an appropriately licensed pest-control business, qualified arborist, or licensed tree contractor.
- Public-interest outreach that alerts a property owner or manager to visible palm changes.

## Blocked Content

While `mode` is `prelicense`, the public site must not advertise, solicit, quote, schedule, or imply that SDPP currently performs pesticide applications, pest-control treatment, SAPW treatment, treatment plans, pruning, removal, stump grinding, installation, planting, field maintenance, contracting, subcontracting, or sold removal coordination.

The site also must not claim SDPP is licensed, certified, insured, credentialed, or authorized unless those credentials are explicitly verified and configured.

## Configuration

The source of truth is `site-config/business_status.json`.

Passing an individual exam or completing one business prerequisite must not automatically change the website status. Any future transition requires an explicit owner-controlled update after all applicable business licenses, registrations, insurance or financial-responsibility requirements, and operating prerequisites have been confirmed.

## Validator

Run:

```powershell
python scripts/validate_prelicense_compliance.py
python scripts/validate_prelicense_compliance.py --self-test
```

The validator reads `site-config/business_status.json`, scans public HTML, generated Palm Journal pages, `journal-data/journal_entries.json`, and Palm Journal source article fragments. It blocks transactional patterns involving treatment offers, pricing, booking, quotes, unavailable field services, false credential claims, and disabled Offer/Service structured data.

The validator supports narrow allowlisting with `PRELICENSE_ALLOW` only for context that cannot be reliably inferred and has been owner-reviewed. Prefer clearer public copy over allowlisting.

## Future SDPP Machine Integration

Future SDPP Machine draft-generation workflows should read the same business status before producing website copy, GBP posts, Nextdoor posts, or email drafts. In prelicense mode, generated copy should describe documentation, education, visible observations, photo review, and referral questions, not unavailable treatment or field-service claims.

## Required Build Gate

Every future website content build must pass:

```powershell
python scripts/build_journal.py
python scripts/validate_prelicense_compliance.py
python scripts/validate_site.py
```

`scripts/validate_site.py` also runs the prelicense validator, so normal validation fails if the site drifts back into unavailable service offers.
