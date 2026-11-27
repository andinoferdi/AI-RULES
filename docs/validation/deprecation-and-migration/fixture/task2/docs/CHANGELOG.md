# Changelog

## 2.2 (2026-10-20)
- Faster catalog loading.

## 2.1 (2026-09-14)
- `/v2/quote` returns 400 for a quantity of zero or less.

## 2.0 (2026-08-04)
- Added `/v2/quote` (`pricing.v2.quote_v2`): totals keep sen, unknown SKUs return 404.
- `/v1/quote` is deprecated. It keeps working; partners will get notice before it is
  removed. No removal date has been set.
