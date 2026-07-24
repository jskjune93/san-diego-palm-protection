# Post-reconstruction adversarial audit

## Scope

All 39 final public routes were rendered at 360×800, 390×844, 768×1024,
1366×768, and 1920×1080. The 195 viewport screenshots are stored in
`docs/audit-screenshots/`.

Each render was checked for exact viewport application, horizontal overflow, one H1,
the canonical primary navigation, and the skip-link main target. The mobile menu was
opened and dismissed with Escape; `aria-expanded`, scroll lock, and focus return were
verified. The Report a Palm form was checked for required permissions, a separately
optional public-use permission, and absence of file-upload controls.

## Defects found and corrected

- The old homepage first viewport positioned SDPP too narrowly around treatment.
  Replaced it with assessment, documentation, monitoring, protection, and response.
- Root pages had competing navigation and visual systems. Core routes and generated
  Journal routes now use the same header, footer, tokens, and interaction script.
- Journal skip links initially lacked `main` targets after the shared header was
  introduced. Every generated Journal page now has `id="main"`.
- The first generated Report a Palm route omitted the established permission and
  email-handoff safeguards. The permissioned form and its explicit delivery/privacy
  limits were restored in the canonical generator.
- Primary credential markers initially used a new marker name, which would have
  bypassed the accepted synchronization contract. The accepted
  `BUSINESS_CREDENTIALS` and `BUSINESS_CREDENTIALS_CONTACT` markers were restored.
- Preserved sourcing, specimen, and Documented Loss routes were initially too far
  from the primary service journey. Direct links were restored from homepage and
  service overview.
- Responsive automation initially captured the browser default before the viewport
  override settled. The batch was discarded and rerun after verifying `innerWidth`
  and `innerHeight` at every requested size.

## Result

Static validation, credential synchronization, credential validation, commercial
language validation, proof-boundary validation, and adversarial validation pass.
Browser checks found no horizontal overflow at any required route/viewport pair.

## Remaining limitations

- No approved sanitized proof bundle currently exists, so the public proof page shows
  an explicit privacy-safe empty state.
- The contact workflows remain email handoffs; there is no form backend or upload
  service. The UI states this before submission and does not claim delivery.
- No analytics or Google Ads identifier exists in repository source. The existing
  integration point and data-layer-compatible conversion event are preserved without
  inventing identifiers.
- Visual assessment and contractor verification remain limited to their documented
  evidence, access, and scope.
