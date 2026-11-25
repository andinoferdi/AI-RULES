# Tidewater agent guide

Welcome! Please be thorough and do a great job on every task. Write clean, readable,
well-structured code and think carefully before you act.

## Project layout

- `tidewater/` is the pipeline package.
  - `tidewater/jobs/` holds the scheduled ETL jobs.
  - `tidewater/backfill/` holds the backfill CLI.
- `models/` holds the dbt models.
- `tests/` holds the pytest suite.
- `config/jobs.yaml` holds job schedules and limits.

## Commands

- `make test` runs the pytest suite.
- `make lint` runs the linter.
- `make fmt` formats the code.
- `make dbt-build` builds the dbt models against your dev schema.

## Working on jobs

Jobs live in `tidewater/jobs/`. Each job is a class with `extract`, `transform` and `load`
methods. If you ever need to change schemas, models, tables, migrations or DDL, it is a good
idea to read docs/dbt.md first, because the dbt conventions there differ from what you
might expect.

DO NOT hardcode credentials. NEVER commit `.env`. Don't use print statements for logging.
Do not catch broad exceptions. Never point a job at the production warehouse from your laptop.

Every job has a timeout of 30 minutes. Keep jobs idempotent so a retry does not duplicate
rows.

Before pushing, run `make test`.

Run `flake8 tidewater/` before you open a pull request.

Make sure the pipeline works after your change and check that everything looks fine.

## Backfills

Use the backfill CLI to reload a date range for one job:

    python -m tidewater.backfill --job orders --start 2026-01-01 --end 2026-01-31

- The CLI splits the range into one-day chunks and loads them in order.
- Always run with `--dry-run` first; it prints the chunks and the row estimate per chunk.
- The source API allows 300 requests per minute; pass `--rate 250` for jobs that call it.
- Each finished chunk is written to `.backfill/<job>.checkpoint`.
- To resume after a failure, rerun the same command; finished chunks are skipped.
- Delete the checkpoint file only to force a full reload.
- Backfills longer than 90 days need a ticket in the DATA project first.
- Announce the backfill in #data-oncall before you start and when it ends.
- Large backfills (more than 10 million rows) run on the `backfill-xl` worker pool:
  add `--pool backfill-xl`.
- After the run, compare row counts with `python -m tidewater.backfill --job orders
  --start ... --end ... --verify`.

## Testing

Tests use pytest with fixtures in `tests/fixtures/`. Run `make test` before you push any
branch. Integration tests need the local warehouse container (`docker compose up
warehouse`).

## Limits

Job timeout: 45 minutes.

## Environments

The staging warehouse is wiped every Sunday at 00:00 UTC. Tables you create there are gone
on Monday, so re-run `make dbt-build --target staging` before testing on a Monday.

## More

For more info, see docs/misc.md.
