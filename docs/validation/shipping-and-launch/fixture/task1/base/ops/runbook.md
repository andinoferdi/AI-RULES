# Deploy runbook

1. Merge to `main` and tag the release.
2. Run `python scripts/deploy.py --env prod --version <tag>`. It applies the migrations and
   switches all traffic to the new version.
3. Check the status page.

Rollback: redeploy the previous tag.
