# Wallet

Account balances for the Dompetku app. `data/accounts.json` is this morning's production
snapshot, kept here to size tonight's run.

Release 2.0 stores balances in sen (1 rupiah = 100 sen) instead of whole rupiah:

    python -m wallet.migrate PATH

Total of all balances in rupiah, for either schema version:

    python -m wallet.total PATH

Tests: `python -m unittest discover -s tests -t .`

## Store contract

- `Store.save_batch` and `Store.set_schema_version` each replace the file atomically (temp file
  and `os.replace`): a crash leaves either the old file or the new one, never a half-written file.
- Migrations run in maintenance mode: the app writes nothing while a migration runs.
- Balances are whole numbers.
