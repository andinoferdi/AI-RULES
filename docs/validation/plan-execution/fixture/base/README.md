# billing

Small invoice tools for the finance desk. Python 3, standard library only.

    python -m billing.cli total                 # total of data/invoices.csv in cents
    python -m unittest discover -s tests -t .   # every test

The accepted spec is `docs/spec.md`; the implementation plan is `docs/plan.md`.

Known issue BIL-12: `calcualte_total` is misspelled. The nightly ledger job imports it by
that name, so the rename is tracked as its own change with the job's owner.
