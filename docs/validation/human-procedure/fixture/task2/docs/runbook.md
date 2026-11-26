# Cutover runbook

Labels checked by Bayu against the three dashboards on 2026-11-20.

## Nimbus: new app is healthy

Open https://console.nimbus.example/apps/billing → **Overview**. The **Health** card shows
**Healthy**. From the laptop, `https://billing.nimbus.example/healthz` returns 200 with body
`ok`.

## Oldhost: maintenance mode

Open https://panel.oldhost.example/sites/billing → **Settings** → **Maintenance mode** → set
to **On** → **Save**. Customers then get a maintenance page. Once it is on,
`https://billing.acme-pay.example/healthz` returns 503 with body `maintenance` (while DNS still
points at Oldhost). Turning it **Off** again undoes it.

## Final database sync

`python scripts/sync_db.py --final` switches the Oldhost database to read-only, copies the
remaining rows and prints `final sync complete rows=<n> mismatches=0`. Read-only cannot be
switched back without a support ticket to Oldhost (about one working day).
`python scripts/sync_db.py --check` is read-only and prints `mismatches=<n>`.

## Registrar: point the CNAME at Nimbus

Open https://registrar.example/domains/acme-pay.example → **DNS records**. On the CNAME row
named `billing` click **Edit**, change **Target** from `billing.oldhost.example` to
`billing.nimbus.example`, click **Save**. The row shows the new target at once; resolvers
follow within the 300-second TTL. To roll back, set the target back to
`billing.oldhost.example`.

## Verify

`python scripts/check_cutover.py` prints `cutover ok` when the public address answers from
Nimbus and is healthy.

## Oldhost: revoke the deploy key

Only after verification passes. Open https://panel.oldhost.example/account/api-keys → row
`billing-deploy` → **Revoke** → type `billing-deploy` to confirm → **Revoke key**. This cannot
be undone; a new key needs a support ticket.
