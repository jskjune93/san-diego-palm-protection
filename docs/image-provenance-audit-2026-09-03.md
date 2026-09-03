# Visible-image provenance audit — 2026-09-03

## Result

Every media asset referenced by a public HTML route was inventoried, fingerprinted, and assigned one of the six requested provenance classifications in `site-config/image_provenance.json`. The audit covers hero backgrounds, inline images, Open Graph images, responsive `srcset` variants, the SDPP logo, and the published field-record video.

The post-correction production inventory contains 112 visible assets: 44 are confirmed original SDPP material supported by repository approval/release records, and 68 are older repository uploads whose ownership, license, and non-AI origin cannot be proved from the available files. Those 68 are classified `unverified_or_uncertain`, not “our work,” and approved only as existing location/species/editorial context pending source confirmation. No image is classified as confirmed licensed stock. No AI-generated image was confirmed; AI origin cannot be conclusively excluded for stripped-metadata uncertain uploads.

The review found one disallowed third-party image: `background.jpg`. It visibly contains a Coastline Palms watermark and was still the homepage hero and Open Graph image. It was removed from the generated homepage, removed from the repository, and placed on a permanent denylist in `scripts/validate_image_provenance.py` and the production build. The legacy public URL permanently redirects to the approved replacement so an older cached asset path cannot continue presenting the third-party image.

## Replacement and presentation

The homepage now uses `images/old-escondido-ufmp/john-krause-with-mature-cidp.jpg`, an approved owner/SDPP field photograph from the Old Escondido documentation set. The hero identifies it as an SDPP field photograph from Old Escondido.

The homepage now leads with owner-led field work—dated photographs, written findings, evidence boundaries, licensed treatment when appropriate, and clear next steps—rather than an abstract portfolio-stewardship claim over borrowed scenery. The Field Work page now opens with four approved local record images and captions that distinguish observation, known outcome, inference, and client-status boundaries.

## Durable control

`scripts/validate_image_provenance.py` walks every public route, resolves visible media references, verifies each file against the exact SHA-256 recorded in the provenance manifest, rejects unapproved assets, rejects changed fingerprints, rejects stale approvals, and explicitly rejects `background.jpg`. `scripts/validate_site.py` runs this check as part of the normal validation suite.

The confirmed-original basis is limited to the expressly approved, privacy-reviewed Old Escondido, Las Palmas, SAPW, newer Journal field sets, John Krause portrait variants, and the SDPP brand asset. Older top-level uploads receive the separate uncertain classification even when their subject and location appear consistent with surrounding editorial copy.

No other visible asset showed third-party supplier branding during the complete contact-sheet review. Future visible media cannot pass validation until it is deliberately classified and added to the exact-fingerprint manifest.

## Explicit files requested for review

`huntington1.jpg`, `huntington2.jpg`, and `treatment.jpg` have no usable EXIF ownership, date, copyright, or license metadata. Git establishes only that they were uploaded and later optimized. All three are therefore `unverified_or_uncertain`. They are not referenced by public HTML and are not copied into the Vercel production output.

## Third-party marks

The University of Minnesota and Indiana University SVG marks are third-party institutional assets rather than SDPP photography. They were removed from the About page; the already-supported biographical degree and service text remains.

## Remaining confirmation work

The 68 uncertain legacy images need an owner-supplied source ledger or original files with reliable provenance before they can be upgraded to confirmed original or confirmed licensed. Until then, the manifest prevents them from being described as completed SDPP work, customer inventory, treatment evidence, or an SDPP installation. New proof-led features should use only the approved owner/SDPP field sets.
