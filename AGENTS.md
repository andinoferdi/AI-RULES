# AGENTS.md — AI-RULES

`main` holds everything: the `ai-rules` installer, validators, tests and every
skill in `skills/<id>/`. The only other long-lived branch is `WebBased`
(A. PRIORITAS and daily modules for web chatbots); change it only when a task
targets it. Words used here are defined in [CONTEXT.md](CONTEXT.md); where each
kind of document lives is in [docs/agents/domain.md](docs/agents/domain.md).

## Where truth lives

1. `skills/<id>/` is the skill. What is in this folder on `main` is what users get.
2. `src/ai_rules/catalog/data/capabilities.json` and
   `src/ai_rules/profiles/data/profiles.json` list the skills `setup` offers.
   Every first-party entry reads `main` at `subpath` `skills/<id>`.
3. `src/ai_rules/release/data/release_manifest.json` pins one thing only: the
   `WebBased` commit used by the Focus reference check. Skills have no pins
   ([ADR 0002](docs/adr/0002-skills-live-on-main.md)).

## Changing a skill

1. Edit `skills/<id>/` on a branch from `origin/main`.
2. Try it: run `ai-rules setup` from the clone. Inside a clone setup reads
   `skills/` from disk (uncommitted edits included) and prints
   `Skill source: local folder ...`.
3. Update the tests or data the change affects (counts, inventories,
   allow-lists, evals) in the same commit, then run
   `python scripts/ci_checks.py --group skills`.
4. Open a PR to `main`. Merging it is the release: `ai-rules setup` outside a
   clone installs `main:skills/<id>` from GitHub.

Changes to the installer, validators or tests use the same branch-and-PR flow.
`main` accepts changes only through a PR with green CI.

## What goes in the repository

Commit only files that the skills, the installer, the checks or the people using
them need. Design notes, plans, trial and review records stay out of both `main`
and `WebBased`: keep them in the conversation or in `docs/exec-plans/`
(ignored), and delete them once the work is merged. `.gitignore` keeps
`docs/specs/` and `docs/validation/` closed for that reason; the files still
tracked there are `docs/specs/changing-skills.md` and data the checks read
(add a new data file with `git add -f` only when a check reads it). A lasting
owner decision gets one dated entry in `docs/DECISIONS.md`, without links to
notes that are not in the repository.

## Adding or removing a skill

Follow [docs/specs/changing-skills.md](docs/specs/changing-skills.md) in one PR.
`tests/test_skill_registry_consistency.py` names any file the change missed.

## Checks

- `python scripts/ci_checks.py --group skills`: skill packages, validators and
  every test in `tests/` (they read real skill content). Needs
  `git fetch origin WebBased` once for the Focus reference check.
- `python scripts/ci_checks.py --group installer`: `tests/installer/`, the
  installer with fixture data. CI runs it on Linux, Windows and macOS only when
  installer files change, plus nightly, on manual dispatch and on release.
- `python scripts/ci_checks.py` runs both. The full run takes about 13 minutes.
- To install a pushed branch before it is merged, run setup outside a clone with
  `AI_RULES_SOURCE_BRANCH=<branch>` set.
- What CI proves and what it cannot: [docs/ci-coverage.md](docs/ci-coverage.md).
