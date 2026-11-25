# Payments service

Node 22, Express 4, TypeScript 5, Postgres 16. Zod 3 is already a dependency.

## Consumers

- **Mobile app v3** (iOS and Android). About 40% of users cannot update for at least
  90 days. It calls `POST /api/payments/create` and `GET /api/payments`. On create it
  sends `requestId`, a UUID it generates once per checkout screen and reuses when it
  retries; it sends no `Idempotency-Key` header. It reads `id`, `amount_cents`,
  `currency`, `status` (it switches on the strings `"pending"`, `"paid"`, `"failed"`)
  and `created_at`, and it parses the `GET /api/payments` body as a JSON array.
- **Web dashboard** ships in the same deploy as the API and can change in the same
  release.
- **Partners** use `sdk/client.ts`, published to npm as `@acme/payments-sdk` 2.x.

## Gateway (PayCo)

- `POST https://api.payco.example/v1/charges` accepts an `Idempotency-Key` header and
  deduplicates on it for 24 hours.
- `POST https://api.payco.example/v1/refunds` takes `{ charge_id, amount }` and accepts
  an `Idempotency-Key`. Partial refunds are allowed; the total refunded cannot exceed the
  charge.
- Our calls to PayCo time out after 10 seconds. A timeout does not tell us whether the
  charge happened.
- PayCo sends webhooks (`charge.succeeded`, `charge.failed`, `refund.succeeded`), each with
  a unique `event.id`, signed in the `PayCo-Signature` header (HMAC-SHA256 of the raw
  body). PayCo retries a webhook for up to 3 days, and events can arrive out of order.
- Webhook processing goes through our queue. Its dead-letter queue is replayed by hand,
  up to 7 days later.

## Incidents

- 2026-09: a customer was charged twice when the SDK retried after a timeout.
- Customers with 3,000+ payments make the mobile payment list hang.

## Product ask

Refunds, full and partial, from the web dashboard and from partners through the SDK.
Charging must be safe to retry.

## Notifications

`src/notifications/` is called from `src/routes/payments.ts`, `src/routes/webhooks.ts`
and `src/jobs/dunning.ts`. All three are in this repository.

## PaymentStatusBadge

`web/PaymentStatusBadge.tsx` is rendered in 12 places in `web/`. The web team owns all of
them and they deploy together with the API.
