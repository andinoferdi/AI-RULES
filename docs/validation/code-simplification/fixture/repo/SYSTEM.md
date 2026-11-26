# orders

A small order-pricing library used by the checkout API and by a nightly export job.

- Python 3.11 or newer, standard library only.
- Run the tests from the repository root: `python -m unittest discover -s tests -t .`
- `price_order` is the only name other code imports from `orders/pricing.py`. The checkout
  API calls `price_order(order, customer, audit)`; `orders/legacy_export.py` calls it with
  `include_tax=False` as the fourth positional argument. Nothing imports the discount classes.
- `PricingError` messages are returned verbatim to API clients, and clients match on them.
- The checkout API stores the `audit` list with every pricing attempt, failed attempts included.
- Money is `Decimal`. Code style is snake_case.
- Past production incidents are recorded in `docs/incidents.md`.
