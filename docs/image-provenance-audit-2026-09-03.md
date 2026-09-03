# Visible-image provenance audit — 2026-09-03

## Result

Every media asset referenced by a public HTML route was inventoried, fingerprinted, and assigned a source basis in `site-config/image_provenance.json`. The audit covers hero backgrounds, inline images, Open Graph images, responsive `srcset` variants, the SDPP logo, the two credited university marks, and the published field-record video.

The review found one disallowed third-party image: `background.jpg`. It visibly contains a Coastline Palms watermark and was still the homepage hero and Open Graph image. It was removed from the generated homepage, removed from the repository, and placed on a permanent denylist in `scripts/validate_image_provenance.py` and the production build. The legacy public URL permanently redirects to the approved replacement so an older cached asset path cannot continue presenting the third-party image.

## Replacement and presentation

The homepage now uses `images/old-escondido-ufmp/john-krause-with-mature-cidp.jpg`, an approved owner/SDPP field photograph from the Old Escondido documentation set. The hero identifies it as an SDPP field photograph from Old Escondido.

The homepage now leads with owner-led field work—dated photographs, written findings, evidence boundaries, licensed treatment when appropriate, and clear next steps—rather than an abstract portfolio-stewardship claim over borrowed scenery. The Field Work page now opens with four approved local record images and captions that distinguish observation, known outcome, inference, and client-status boundaries.

## Durable control

`scripts/validate_image_provenance.py` walks every public route, resolves visible media references, verifies each file against the exact SHA-256 recorded in the provenance manifest, rejects unapproved assets, rejects changed fingerprints, rejects stale approvals, and explicitly rejects `background.jpg`. `scripts/validate_site.py` runs this check as part of the normal validation suite.

The source bases used in the manifest are:

- `sdpp_field_repository`: SDPP repository field photography reviewed for visible third-party marks and consistent with the site's approved local field sets and captions.
- `approved_owner_field_record`: the expressly approved, privacy-reviewed Old Escondido, Las Palmas, SAPW, and journal field-record sets documented elsewhere in the repository.
- `owner_identity`: John Krause portrait variants.
- `sdpp_brand`: SDPP logo.
- `credited_education_mark`: university marks shown as biographical education references, not as endorsements.

No other visible asset showed third-party supplier branding during the complete contact-sheet review. Future visible media cannot pass validation until it is deliberately added to the exact-fingerprint manifest.
