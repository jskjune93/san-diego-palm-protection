# Treatment route repair diagnosis - 2026-07-26

## Pre-change state

- Production source commit: `e7027ad24e7c90b954cc2047584af12ee5438d88`
- Homepage Protection & Treatment source: `scripts/site_components.py`, rendered by `scripts/build_core_pages.py`
- Homepage destination: `./palm-stewardship-plans.html`
- Destination source: the `palm-stewardship-plans.html` page definition in `scripts/build_core_pages.py`
- Destination disposition: retained and modernized in place because it has a distinct generic Palm Protection & Treatment purpose and preserves the established URL and inbound value
- SAPW-specific treatment route: `/south-american-palm-weevil-treatment-san-diego.html`

## Root cause

The authoritative source at `e7027ad` already generated a current Palm Protection & Treatment page that states regulated treatment is available subject to assessment, credentials, authorization, label requirements, site conditions, and scope. The live custom-domain homepage was serving an older homepage generation with legacy identity and pathway language, while the destination treatment page itself was current. The inconsistency was therefore a stale production homepage/build state rather than an outdated current treatment destination.

The prior validator checked that the homepage contained a Protection & Treatment heading and scanned a limited set of obsolete phrases, but it did not:

- resolve the Protection & Treatment service-card destination;
- assert that the destination was the approved canonical route;
- assert current-treatment semantics on that destination;
- reject the wider known family of treatment-unavailable phrases; or
- flag legacy `Palm Stewardship Resources` labels in generated editorial pages.

## Repair

- Keep `/palm-stewardship-plans.html` as the canonical generic Palm Protection & Treatment page.
- Keep `/south-american-palm-weevil-treatment-san-diego.html` as the SAPW-specific discovery page that links into the canonical generic pathway.
- Replace two remaining `Palm Stewardship Resources` labels with `Palm Protection & Treatment` in authoritative Journal source.
- Add route-level and semantic treatment assertions to `scripts/validate_site.py`.
- Deploy the exact rebuilt production output so the custom-domain homepage and treatment destination come from the same validated commit.
