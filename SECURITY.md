# Security policy

These examples are server-side only. Never put `VEHICLES_API_KEY` in browser,
mobile, desktop-client, or other user-distributed code. Treat VINs, history
report IDs, and report payloads as private data.

## Report a vulnerability

Please use [GitHub private vulnerability reporting](https://github.com/vehicles-dev/examples/security/advisories/new).
Do not open a public issue for a suspected vulnerability, and do not include a
real API key, VIN, history report ID, or report payload in the report. Use
clearly synthetic placeholders and describe how the maintainers can reproduce
the issue safely.

If a credential may have been exposed, revoke or rotate it immediately through
the Vehicles.dev account controls rather than waiting for the report to be
reviewed.

Security fixes are made on the default branch. Users should track the latest
tag or commit until a formal support policy is published.
