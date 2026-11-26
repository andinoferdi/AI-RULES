# Spec: order export

Status: accepted by the shop owner on 2026-11-22.

## Goal

Admins export orders for accounting from the command line, as CSV or JSON, or as a
short-lived download link they can paste into the accounting tool.

## Behaviour

1. `shopline export [--format json|csv] --since YYYY-MM-DD [--locale en|id|de] [--link]`.
   `--format` defaults to `json`; `--locale` defaults to `en`.
2. `--since` is a calendar date in the shop's timezone, `Asia/Jakarta`. Orders created at or
   after 00:00 of that date in Jakarta are exported. Internally the date is converted to UTC.
3. Every exported order has: `id`, `created_at` (ISO 8601, UTC, `Z` suffix), `customer`,
   `currency`, `total`, `status`. `total` is always produced by `money.format_price`.
4. JSON output is a list of objects with exactly those keys, in that order, `total` as a
   string. An empty result is `[]`.
5. CSV output has a header row whose labels come from the message catalogue keys
   `export.header.id`, `export.header.created_at`, `export.header.customer`,
   `export.header.currency`, `export.header.total` and `export.header.status` in the chosen
   locale, then one row per order. Fields are quoted as RFC 4180 requires (a total such as
   `1,234.50` is quoted). An empty result is the header row only.
6. With `--link`, nothing is printed except one URL:
   `https://shop.example/exports/<token>`. The token names the exported order ids and is
   valid for 15 minutes (900 seconds). It is signed with HMAC-SHA256 using the existing
   `SECRET`; signatures are compared in constant time. A token is rejected when it is
   tampered with or older than 900 seconds; clock-skew leeway is at most 30 seconds.
7. Existing commands keep their current behaviour.

## Global constraints

- No new runtime dependency, except `tzdata` for Windows admin machines, declared as
  `tzdata; sys_platform == "win32"`.
- No network access at runtime.
- Amounts shown to people always go through `money.format_price`.
- Python 3.12 standard library only for CSV and JSON (`csv`, `json`).
