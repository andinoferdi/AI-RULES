# tasks-api

Task tracker backend. Production runs the latest deployed tag (currently `v2.3`).

- Tests: `python -m unittest discover -s tests -v`
- Deploy: `python scripts/deploy.py --env prod --version <tag>`. It applies every migration in
  `migrations/` and then switches all traffic to the new version. See `ops/runbook.md`.
- Feature flags live in `config/production.json`. They are read when the service starts, so a
  flag change means editing that file and redeploying (about 15 minutes end to end).
- Service level objective, error budget, backups and on-call: `ops/`.
- Release owner: Bima (product lead). On-call engineer this week: Sari.
