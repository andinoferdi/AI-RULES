# Expenses

Expense receipts for the Jakarta office. Office time is WIB (UTC+7) and monthly
reports follow office time.

Receipts arrive from two sources:

- CSV uploads from the finance portal (`data/uploads/`), in office wall-clock time.
- The mobile app (`data/inbox/`, one JSON object per line), pulled by the nightly sync.

`scripts/ingest.py` imports a file into `data/store.jsonl`, which keeps one record per
receipt id. Importing a receipt that is already stored skips it unless `--replace` is
given. `scripts/run_report.py` prints the monthly report from the store.

    python scripts/ingest.py --source mobile --file data/inbox/mobile-2026-03.jsonl
    python scripts/run_report.py --month 2026-03 --ids

`scripts/rebuild_index.py` regenerates `data/month_index.json` for the finance dashboard.

Tests: `python -m unittest discover -s tests -t .`

## Mobile app releases

- 4.9: current stable app until March.
- 5.0: beta group from 25 February 2026, everyone from 16 March 2026.

## Known issues

- EXP-88: `tests/test_vendors.py::test_keeps_legal_prefix` fails because legal prefixes
  such as "PT" are title-cased. Procurement owns `expenses/vendors.py` and replaces it
  with the vendor master next sprint. Leave it as it is.
