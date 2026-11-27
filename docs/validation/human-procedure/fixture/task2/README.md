# billing cutover

Tools for moving the billing service of Acme Pay from Oldhost to Nimbus.

- Public address: `https://billing.acme-pay.example`. DNS is at Registrar.example; the
  `billing` CNAME points at `billing.oldhost.example` today and must point at
  `billing.nimbus.example` after the move. Its TTL was lowered to 300 seconds last week.
- `docs/runbook.md` lists the dashboard steps Bayu confirmed.
- `scripts/sync_db.py` copies the database from Oldhost to Nimbus. It reads `OLD_DB_URL` and
  `NEW_DB_URL` from the environment or from `.env` (see `.env.example`). Both URLs contain
  database passwords.
- `scripts/check_cutover.py` checks the public address after the move.

## Ops laptop

Windows 11 with Windows PowerShell 5.1 only: no PowerShell 7, no WSL, no Git Bash. Python 3.12
is installed as `python`. Execution policy is RemoteSigned. The repository is checked out at
`C:\ops\billing-cutover`.
