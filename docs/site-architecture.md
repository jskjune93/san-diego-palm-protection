# SDPP public website architecture

## Four service pillars

1. Palm Portfolio Stewardship
2. Protection & Treatment
3. Documentation & Planning
4. Response, Removal & Renewal Coordination

The homepage and service overview present the pillars as one lifecycle. Residential
and managed-property routes are audience pathways into the same services.

## Primary navigation

- Services
- Residential
- Managed Properties
- Palm Decline
- Palm Journal
- Sample Work
- Request Assessment

This exact information architecture is generated for core pages and Palm Journal
pages. Mobile behavior uses the same links, order, labels, and conversion target.

## Proof architecture

The website never reads Machine private records. It accepts only separately approved,
versioned public bundles in `proof-data/approved/`, validated against
`proof-data/schema.json`. The public sample page has a privacy-safe empty state until
such a bundle exists.

An approved sanitized Karrie derivative may populate sample-assessment and monitoring
proof components after Machine approval/export. The private Karrie report, client
identity, address, contact/access details, and unapproved media remain outside the
repository.

## Measurement and conversion

Canonical `mailto:` and `tel:` actions remain usable without JavaScript. `site.js`
emits `sdpp:conversion` and pushes to an existing `dataLayer` when present. It does not
invent or replace an analytics or advertising identifier.
