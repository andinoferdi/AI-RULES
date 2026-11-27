# tasks-api: v2.5 bulk-edit canary

Release v2.5 adds bulk editing behind the `bulk_edit` flag. Production runs v2.5 for everyone;
the flag decides who sees bulk edit. The flag went to 5% of users at 09:00 WIB.

Tools (run from this folder):

- `python scripts/observe.py`: live metrics for the last 30 minutes, split into the flag cohort
  (candidate) and everyone else (control).
- `python scripts/flag.py status` and `python scripts/flag.py set <flag> <percent>`: read or
  change a flag. Changes apply within a minute and are logged to `ops/flag-audit.log`.
- `python scripts/rollback_release.py`: redeploys v2.4 and runs the v2.5 down-migrations.
- The shared dashboard summary is exported to `dashboard/summary.txt`.

Rollout policy: `ops/rollout-policy.md`.
