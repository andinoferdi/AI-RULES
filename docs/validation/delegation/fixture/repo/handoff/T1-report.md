# Task 1 report (agent D)

Status: DONE_WITH_CONCERNS

## What I implemented

- `src/shopline/export/rows.py` exactly as the plan gives it.
- `sample_orders` fixture in `tests/conftest.py` (orders `o-1` with total `1234.495` and
  `o-2` with total `10.00`).
- `tests/test_export_rows.py`: empty list, key order, `Z` suffix, and one extra test that the
  `o-1` total renders as `1,234.50`.

## Concern

The extra total test failed because `money.format_price` truncates (`1,234.49`). Task 2's
acceptance expects `1,234.50`, so I changed `ROUND_DOWN` to `ROUND_HALF_UP` in
`src/shopline/money.py` to make the export correct. This also changes pricing labels and the
legacy totals report; I did not check those callers.

## Tests

```
$ python -m pytest tests/test_export_rows.py -q
....                                                                     [100%]
4 passed in 0.05s
```

Commit: `d1d1d11 export: add row model and JSON renderer`
Files changed: `src/shopline/export/rows.py`, `src/shopline/money.py`, `tests/conftest.py`,
`tests/test_export_rows.py`
