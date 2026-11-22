# Decisions

- 2026-11-22: Main's `release_manifest.json` is the only version anything reads.
  CI, the tests and `ai-rules setup --source latest` use the pinned skill commits;
  a skill branch head reaches users only after a promote PR passes CI and is
  merged. Promotion is started locally with `python scripts/promote_skill.py
  <skill>` under the owner's `gh` login. A ruleset on `main` requires a PR with
  green CI. `natural-writing` is the first real promotion; the other branches
  ahead of their pins follow so users are not downgraded. See
  [ADR 0001](adr/0001-main-pins-skill-versions.md) and the
  [promotion spec](specs/skill-promotion.md).

- 2026-11-22: `threejs-skills` is pinned at `4fe9d9c` instead of `7ff3f57`, because
  `docs/threejs/inventory.json` on main already describes `4fe9d9c` (README-only
  changes). Pinning the older commit made the inventory check fail.

- 2026-11-22: CI and the promote clone pin only `origin/<skill>`, as CI always had.
  Tests that read a local branch name keep skipping on runners; reviving them is
  tracked in [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).
