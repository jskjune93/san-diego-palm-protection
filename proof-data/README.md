# Approved public proof boundary

This directory accepts only versioned, separately approved public or sanitized proof
bundles exported by the canonical SDPP Machine.

Place an export manifest in `proof-data/approved/` only when all of these are true:

- the artifact type is in `proof-data/schema.json`;
- the artifact status and publication approval are `approved`;
- the export fingerprint matches the approved artifact fingerprint;
- the privacy class is `public` or `sanitized`;
- the publication target is `website`;
- the Machine privacy scan passed;
- every referenced image has explicit public-use approval;
- the bundle contains no client identity, address, contact, access, or local-path data.

`scripts/validate_proof_exports.py` fails closed. An empty approved directory is valid.
Private source reports—including the private Karrie assessment—must never be copied
here or into HTML, JSON, metadata, images, or generated source.
