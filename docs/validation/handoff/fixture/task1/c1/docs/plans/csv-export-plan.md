# Plan: CSV export (issue 412)

Spec: docs/specs/csv-export.md

| Step | Work | Status |
| --- | --- | --- |
| 1 | Spec agreed with Andi | done |
| 2 | `invoicekit/csv_export.py`: `write_csv(invoices, fh)` with tests | in progress |
| 3 | Header order exactly as the spec | todo |
| 4 | Credit notes per Budi's answer | blocked: waiting for Budi |
| 5 | CLI `python -m invoicekit.export --out invoices.csv` | todo |
| 6 | QA against Budi's sample file | todo |

## Checkpoint

Updated 2026-11-24. Working on step 2. NEXT ACTION: write `write_csv` and its tests.
