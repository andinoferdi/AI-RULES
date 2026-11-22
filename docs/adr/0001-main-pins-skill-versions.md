# Main pins skill versions; skill branch heads are unreleased work

Status: superseded by [ADR 0002](0002-skills-live-on-main.md), 2026-11-23. Accepted 2026-11-22.

CI, several tests and `ai-rules setup --source latest` used to read skill branch
heads (`origin/<skill>`), while main's tests and inventories followed the pins in
`release_manifest.json`. A push to a skill branch therefore changed main's CI
result without any commit on main, and reached users before any check ran. From
2026-11-07 to 2026-11-21 the daily main run failed for this reason, for example
`search-first: unexpected runtime file` and portfolio counts `59 != 31`.

The owner chose to make the pin on `main` the only version anything reads:

- CI points `origin/<skill>` at the pinned commits
  (`scripts/skill_refs.py pin`) before running `scripts/ci_checks.py`.
- `ai-rules setup --source latest` reads the pins from GitHub `main` at install
  time and installs those commits. A source repository without a main manifest
  keeps branch-head behavior.
- A pin moves only through a promote PR (`scripts/promote_skill.py`), and a
  ruleset on `main` requires a PR with green CI.

Consequences: a skill change and the main tests or data it affects land together
in one PR. Pushing to a skill branch is safe and private until promoted. Users
whose installed copy is a newer unpromoted revision keep it, and setup says so,
until main pins it. The promote PR is opened with the owner's own `gh` login, so
its CI starts without an extra token; a GitHub Actions trigger would need a PAT or
GitHub App, because PRs opened with `GITHUB_TOKEN` wait for approval before CI runs.
