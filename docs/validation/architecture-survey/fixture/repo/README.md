# billing-service

Subscription billing for the web app: HTTP routes for renewing and changing plans, a nightly
renewal job, an admin CLI for manual renewals, refunds, and the PayGate payment webhook.

- Postgres in production; tests use Jest (`npm test`).
- Domain terms are in `GLOSSARY.md`; architecture decisions in `docs/adr/`.

```
src/
  routes/        HTTP handlers (Express)
  jobs/          scheduled jobs
  cli/           admin scripts
  renewals/      renewal steps
  ledger/        customer ledger
  refunds/       refunds
  proration/     proration math
  pricing/       plan prices and VAT
  money/         money arithmetic
  mail/          outbound email
  webhooks/      payment provider webhooks
  invoices/      invoice summaries
  legacy/        old exports
tests/
```
