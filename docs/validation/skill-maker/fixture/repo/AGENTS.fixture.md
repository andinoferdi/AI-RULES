# Ledgerly

Ledgerly is the double-entry ledger service behind our billing. Python 3.12, PostgreSQL 16,
Django 5.

## Commands

- `make test`: unit tests.
- `make lint`: ruff check and ruff format --check. CI runs it on every push.
- `make migrate-check`: dry-runs pending migrations against last night's production snapshot
  and reports the locks each one takes. Needs `SNAPSHOT_URL`, which only works on the office
  network or the VPN, so CI cannot run it yet.

## Working here

- Branch from `main` and open a PR. Two approvals are needed for anything under `migrations/`.
- Production incidents go to #ledger-oncall.
- Skills for agents live in `skills/<name>/SKILL.md`. Follow `skills/README.md` when adding or
  changing one.
