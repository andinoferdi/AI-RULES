# Deploying the members service

- Releases go out with `make release`, which first runs `python scripts/migrate.py up`
  against production and then rolls the API instances one at a time.
- A rollout takes 20 to 30 minutes. During that window old and new API instances serve
  traffic side by side against the same database.
- Rolling back a release redeploys the previous code. It does not run any `down` migration;
  a `down` has to be run by hand.
- Production holds about 1.2 million members.
