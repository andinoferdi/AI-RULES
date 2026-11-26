# invoicekit

Invoice tools for the finance team. Python 3.10+, standard library only.

Run the tests from the repository root:

    python -m unittest -q

## CSV export

    python -m invoicekit.export --out invoices.csv

Writes the invoices as `;`-separated CSV for the accounting import (issue 412).
