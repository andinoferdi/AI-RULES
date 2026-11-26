# Ledger

Prints a page of ledger entries from `data/entries.json`.

    python -m ledger.cli --page 1

The page size defaults to `ledger.config.DEFAULT_PAGE_SIZE`; `--size N` overrides it up to
`ledger.config.MAX_PAGE_SIZE`.

Tests: `python -m unittest discover -s tests -t .`
