# Vehicles.dev examples

Small, runnable server-side examples for the official Vehicles.dev TypeScript
and Python SDKs. Each language includes the same three flows:

- decode a VIN and print selected vehicle fields;
- search active listings and print counts; and
- intentionally order a durable history report, wait for it, and print only its
  section names.

The listing examples privately decode `VEHICLES_VIN` to derive optional make
and model filters. No example prints an API key, VIN, history report ID, or full
API payload.

## Package status

The SDKs are not yet published to npm or PyPI. These starters install the
immutable `v0.1.1` GitHub tags:

- TypeScript repository: `vehicles-dev/typescript-sdk`
  (`github:vehicles-dev/typescript-sdk#v0.1.1`)
- Python repository: `vehicles-dev/python-sdk`
  (`vehicles-dev @ git+https://github.com/vehicles-dev/python-sdk.git@v0.1.1`)

No registry release workflow lives in this repository. The dependency
declarations can move to package registries after official publishing is
enabled.

## Server-side setup

Clone the examples, create a private environment file, and load it into your
current shell:

```sh
git clone https://github.com/vehicles-dev/examples.git
cd examples
cp .env.example .env
chmod 600 .env
# Edit .env and set VEHICLES_API_KEY and VEHICLES_VIN.
set -a
. ./.env
set +a
```

`.env` is ignored by Git. Keep these values in a server-side secret manager in
deployed applications. Never use public/client-prefixed environment variables,
embed a credential in frontend JavaScript, or pass one to browser or mobile
code.

### TypeScript (Node.js 22+)

```sh
cd typescript
npm install
npm run example:decode
npm run example:listings
cd ..
```

### Python (Python 3.11+)

```sh
python3 -m venv python/.venv
. python/.venv/bin/activate
python -m pip install -r python/requirements.txt
python python/decode_vin.py
python python/search_listings.py
```

## Billable history report

Ordering a history report can incur a charge. Before running either history
example:

1. Generate one UUID yourself, for example with `uuidgen`.
2. Save that UUID as `VEHICLES_IDEMPOTENCY_KEY` in the ignored `.env` file.
3. Persist and reuse that exact UUID for every retry or restart of this one
   logical order. Generate a new UUID only when you deliberately want a new
   order.
4. Review the intended VIN and account, then set the confirmation to `yes` only
   for the command that should place the order.

Run the TypeScript example:

```sh
cd typescript
VEHICLES_CONFIRM_BILLABLE_REPORT=yes npm run example:history
cd ..
```

Or run the Python example:

```sh
VEHICLES_CONFIRM_BILLABLE_REPORT=yes python python/order_history_report.py
```

The code never generates an idempotency key. It refuses to order unless the key
is a UUID and `VEHICLES_CONFIRM_BILLABLE_REPORT` is exactly `yes`. The
confirmation is a local accident-prevention guard, not a billing waiver.

If submission times out or its outcome is unknown, do not rotate the key and
blindly submit again: reuse the same key for that logical order. The SDK wait
helpers poll with the API's retry cadence and a bounded wait. Avoid custom tight
polling loops; a timeout does not imply that server-side work stopped.

## Privacy and data handling

VINs, report identifiers, report contents, and listing records can be sensitive
or regulated data. Collect only what you are permitted to use, keep retention
short, restrict access, and follow the Vehicles.dev API terms and applicable
law. The examples intentionally print only selected decoded fields, aggregate
listing counts, or history report section names. Application logs, traces,
error reporting, and analytics must preserve the same boundary.

## Offline checks

Tests exercise environment and billing guards only; they never contact the
API. After installing dependencies, run:

```sh
(cd typescript && npm run check)
python -m unittest discover -s python -p 'test_*.py'
python -m compileall -q python
PYTHONPATH=python python -c 'import common, decode_vin, order_history_report, search_listings'
```

## License and API terms

The examples are MIT licensed. The [license rider](LICENSE) clarifies that the
software license does not grant API access or rights to Vehicles.dev services,
responses, reports, or data; those remain subject to separate API terms.
