# PR 212: store balances in sen

Converts every balance from rupiah to sen in batches of 500, then sets `schema_version` to 2.

Safe to re-run: the migration checks the schema version first, so if anything goes wrong we just
run it again. Covered by `test_second_run_is_noop`.

Plan: run on production tonight at 22:00, in maintenance mode.
