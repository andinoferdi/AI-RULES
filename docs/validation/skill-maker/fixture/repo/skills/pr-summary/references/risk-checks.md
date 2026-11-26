# Risk checks for a PR

Name each one that applies, with one line on why.

- Touches `migrations/`: say which tables and whether `make migrate-check` was run.
- Changes money rounding or currency handling (`ledger/money.py`).
- Changes a public API response shape (`api/serializers/`).
- Adds or changes a setting read from the environment.
- Changes a background job's schedule or retry policy.
