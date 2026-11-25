# threejs-game-changelog

Design, implement, backfill, audit, and release in-game changelogs with contiguous versioning, deployment provenance, menu-state navigation, accessible toggle, close, and Escape behavior, and responsive release-ledger UI. Use when Codex needs to add or revise a changelog or version screen in a game, reconstruct release history from deployments and Git, define version-bump rules, keep displayed versions synchronized with live builds, or test changelog mechanics across desktop and mobile.

This is an internal method bundled in `threejs-skills`, not an individual installer
choice or native skill. Read [GUIDE.md](GUIDE.md) for the method; its supporting
resources remain relative to this directory. Install the complete family:

```sh
ai-rules setup --host codex --capability threejs-skills --scope project --project-root . --source latest
```

Use "threejs-skills, specifically threejs-game-changelog" or let the family select by need.
With Andino, return evidence/results to its single task context. Preserve supplied
notices, observe project versions, and get task authorization for paid services.
Update the family through the existing CLI; modified/unmanaged targets are preserved.
