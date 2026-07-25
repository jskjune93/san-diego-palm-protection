# Owner-led website correction report

## Recovery and scope

- Starting release candidate: `dd74a221bf41d5eb65cc8de149de9869a1531079`
- Local correction branch: `correction/owner-led-palm-protection`
- Annotated recovery tag: `recovery/pre-owner-led-correction-20260724`
- Pre-redesign reference: `871d3b7`
- No push, merge, deployment, hosting change, Machine change, dependency, framework, or environment change was made.
- The pre-existing untracked `7_21_2006.jpg` was not added, moved, modified, or deleted.

## Correction

The correction retains the generated 39-route architecture, credential synchronization, proof-export gate, Palm Journal, Documented Loss, canonical metadata, sitemap, robots, forms, analytics hooks, responsive navigation, and production allowlist. It changes the public emphasis from a records consultancy to an owner-led local palm-protection service.

The homepage now uses authentic field imagery and leads with mature palm protection in North County San Diego, an Old Escondido identity, direct assessment and phone actions, and the synchronized concise credential block. Its content is limited to five substantive sections before the inquiry band.

The shared three-pillar language is:

1. Assessment, Monitoring & Documentation
2. Protection & Treatment
3. Decline Response, Removal & Replacement

Residential assessment, treatment, SAPW, Old Escondido, managed property, decline response, Field Work, Palm Journal, and Documented Loss retain distinct visitor purposes. Field Work now presents existing approved public observations and example-report structure; the private-to-public export boundary remains intact as a lower-page safeguard.

## Generated route disposition

All 39 canonical routes remain public and retain their existing URLs. No route was removed, archived, redirected, or newly added.

- 20 core commercial/educational routes were regenerated from `scripts/build_core_pages.py`.
- 1 Palm Journal library and 17 Journal article routes were regenerated from `scripts/build_journal.py`.
- 1 Documented Loss index remains part of the Journal output.

## Validation

- Production build: 39 routes, 129 allowlisted files.
- Business credential validation: pass.
- Commercial/prelicense contradiction validation: pass.
- Proof-boundary validation: pass, with zero approved public bundles.
- Site validation: pass for 39 HTML files, 18 manifest entries, 17 Journal articles, legacy anchors, sitemap, and robots.
- Adversarial audit: pass.
- Browser inspection: six core journeys at 360×800, 390×844, 768×1024, 1366×768, and 1920×1080 (30 checks), with no horizontal overflow, missing assessment CTA, missing hero image, or mobile contact-bar failure.
- Mobile menu: expanded state, focus-visible treatment, canonical links, and viewport width verified at 390×844.

The rendered inspection found and corrected one defect: CSS custom-property background URLs resolved relative to `site-assets/site.css`, hiding hero photographs. Hero URLs now resolve from the public site root.

## Visual evidence

Before screenshots are retained in `docs/audit-screenshots/`, including `390x844__index.png` and `1366x768__index.png`.

After screenshots are in `docs/owner-led-correction-evidence/after/` for:

- homepage;
- residential assessment;
- protection and treatment;
- managed properties;
- decline/removal/replacement;
- Field Work;

at all five required viewports.

## Rollback

To inspect or restore the exact pre-correction release state without changing the current branch:

```powershell
git switch --detach recovery/pre-owner-led-correction-20260724
```

To abandon the local correction branch before it is merged, switch back to `main`. Do not use a destructive reset while the preserved untracked photograph is present.
