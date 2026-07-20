# Report a Palm delivery and intake

`report-a-palm.html` uses a transparent email handoff because the production site has no form or upload backend. It does not store or upload data. The visitor must send the prepared message from their own email application and attach photographs there.

The future Machine intake contract is defined in `report-a-palm-submission-schema.json`. Every submission begins as `needs_review`; public-use permission defaults to false, and no submission may become public automatically.
