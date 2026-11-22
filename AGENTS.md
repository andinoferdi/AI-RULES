# AGENTS.md — AI-RULES

`main` holds the `ai-rules` installer, validators, tests and the version pins.
Every skill lives on its own orphan branch (`council`, `focus`, `search-first`, ...).
Words used here are defined in [CONTEXT.md](CONTEXT.md); where each kind of
document lives is in [docs/agents/domain.md](docs/agents/domain.md).

## Where truth lives

1. `src/ai_rules/release/data/release_manifest.json` on `main` pins the exact
   commit of every skill. CI, the tests and `ai-rules setup` read only these pins
   ([ADR 0001](docs/adr/0001-main-pins-skill-versions.md)).
2. The skill branch holds the skill's content. A commit there reaches users only
   after it is promoted.
3. `src/ai_rules/catalog/data/capabilities.json` and `profiles/data/profiles.json`
   list the skills `setup` offers.

## Changing a skill

1. Edit and commit on the skill branch, in its own worktree:
   `git worktree add .worktrees/<skill> <skill>`. Push the branch.
2. From a checkout of `main`, run `python scripts/promote_skill.py <skill>`.
   It pins the branch head on a `promote/<skill>` branch, runs
   `scripts/ci_checks.py` against the new pins, and opens a PR only when every
   check passes. Done when it prints `PR: <url>`.
3. If it prints `FAIL at '<step>'`: a skill problem is fixed on the skill branch
   (push, rerun). Out-of-date main tests or data (counts, inventories,
   allow-lists) are fixed inside the printed `.git/promote/<skill>` clone; rerun
   and the edits ship in the same PR.
4. The owner merges the PR after its checks are green. Done when the `main` push
   run of "Validate skills" is green.

Changes to the installer, validators or tests themselves use a normal branch
from `origin/main` and a PR. `main` accepts changes only through a PR with green CI.

## Adding or removing a skill

Follow [docs/specs/skill-promotion.md](docs/specs/skill-promotion.md#adding-a-skill)
in one PR to `main`. `tests/test_skill_registry_consistency.py` names any file the
change missed.

## Checks

- Run everything CI runs: `python scripts/skill_refs.py pin`, then
  `python scripts/ci_checks.py` (the promote command does both in its clone).
  `pin` moves only `origin/<skill>`; the next `git fetch` moves them back.
- `python scripts/skill_refs.py drift` lists skill branches with unpromoted commits.
- What CI proves and what it cannot: [docs/ci-coverage.md](docs/ci-coverage.md).
