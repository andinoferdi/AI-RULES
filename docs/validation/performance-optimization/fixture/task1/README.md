# orders

Back end for the tenant dashboard. `orders.summary.tenant_summary(db, tenant)` builds the
summary the dashboard shows: one row per order with the customer name, the line items and the
order total, newest first.

`orders.billing.issue_invoices(db, tenant)` reuses `tenant_summary` to invoice every open
order. Finance requires invoices to include every order placed up to the moment the run starts.

## Local database

`orders.db.Database` wraps an in-memory SQLite database seeded by `orders.seed`. Production
talks to PostgreSQL in another zone, so every round-trip costs about 0.4 ms of network time;
the local adapter adds the same 0.4 ms to every `query` call so timings match production.
`Database.query_count` counts round-trips.

## Commands

- `python -m orders.bench [--tenant acme] [--runs 5]` times `tenant_summary` and prints one
  line per run plus the query count and a checksum of the result.
- `python -m unittest` runs the tests.

## Helpers

`orders.cache.TTLCache` is a small in-process cache used for the product catalogue page.
