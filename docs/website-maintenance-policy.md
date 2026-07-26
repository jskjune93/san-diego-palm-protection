# SDPP website maintenance policy

This policy is the permanent change-control standard for the public San Diego Palm Protection website.

## Source of truth

- Generate core routes through `scripts/build_core_pages.py`, Journal routes through `scripts/build_journal.py`, and shared navigation, footer, inquiry, and metadata through `scripts/site_components.py`.
- Treat `site-config/business_status.json` as authoritative for credential and service-availability wording.
- Treat `site-config/inquiry.json` as authoritative for inquiry delivery mode. A direct-submission form must not be enabled until an approved first-party endpoint, delivery destination, abuse controls, privacy handling, and secure upload storage are configured.
- Preserve `site-config/ufmp_resource.json` and the exact policy-controlled UFMP wording. Never imply City endorsement.
- Publish evidence only through approved, sanitized proof exports. Do not copy private reports, client records, local paths, QA artifacts, or working files into public source.

## Conversion and measurement

- Maintain distinct homeowner and organization inquiry paths.
- An email-fallback form must say that the visitor still needs to review and send the message. Do not label preparation as a submitted or verified lead.
- Use `data-conversion` action names for CTA initiation, calls, email preparation, and approved PDF views. A verified-lead conversion may fire only after a confirmed first-party submission response.
- Preserve existing analytics and Google Ads integration points. Never invent, replace, or duplicate measurement identifiers.

## Claims, trust, reviews, and pricing

- Publish credentials, insurance, licensing, treatment availability, and regulated-work language only when supported by the authoritative business-status configuration.
- Publish reviews only from an owner-approved exact quote and source. Never paraphrase a customer review or expose a private client.
- Publish owner biography facts, service areas, civic participation, and affiliations only from an approved source record.
- Publish a price only when its amount, scope, geography, exclusions, and current approval are documented. Otherwise explain the variables that determine scope and price.
- Never imply guaranteed outcomes, hidden-work verification, municipal approval, diagnosis from photographs, or capabilities outside the documented scope.

## Route and design control

- Every public route must retain a defined conversion, service, trust, evidence, or educational purpose in `docs/route-inventory.md`.
- Reuse the shared navigation, components, colors, typography, spacing, and responsive rules. Fix shared generators rather than adding route-specific override layers.
- New routes require canonical metadata, sitemap inclusion, shared navigation, responsive inspection, internal-link validation, and a production-output allowlist decision.

## Required release checks

Before merging or deploying:

1. Synchronize and validate business credentials and prelicense/commercial status.
2. Regenerate all pages and run the production build from a clean `dist`.
3. Run site, link, anchor, canonical, sitemap, schema, privacy, proof-boundary, and production-allowlist validators.
4. Validate inquiry mode: direct submission and uploads must remain disabled unless their approved infrastructure exists; email fallback must remain explicit.
5. Render all routes at 360×800, 390×844, 768×1024, 1366×768, and 1920×1080; check navigation, focus, overflow, anchors, and touch targets.
6. Search public source and `dist` for private identifiers, local paths, localhost/test endpoints, internal notes, QA artifacts, unapproved proof, and obsolete credential or service language.
7. Confirm the protected untracked `7_21_2006.jpg` remains untouched unless the owner separately approves its use.
8. Record the starting commit, final commit, commands, results, working-tree status, deployment identifier, and rollback point.
