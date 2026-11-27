# pricing service

Quotes prices for the coffee-supply catalog. Python 3 standard library only.

- `pricing/catalog.py`: unit prices in rupiah (some carry sen, for example 12500.50).
- `pricing/legacy.py`: the original quote function, served as `/v1/quote`.
- `pricing/v2.py`: the replacement, served as `/v2/quote` since release 2.0 (August 2026).
- `web/routes.py`: the HTTP routes. `python -m web.routes v2/quote sku=KOPI-250 qty=3`
  prints what a caller of `/v2/quote` receives.
- `reports/monthly_invoice.py`: the invoice run on the 1st of each month
  (`python -m reports.monthly_invoice data/orders-2026-10.csv`).
- `python -m unittest discover -s tests` runs the tests.

See `docs/CHANGELOG.md` and `docs/partners.md` for what was announced to whom.

Today is Thursday 2026-11-26.
