# Changing, adding and removing skills

Every first-party skill is a folder in `skills/<id>/` on `main`. Merging a PR to
`main` is the release. See [ADR 0002](../adr/0002-skills-live-on-main.md).

## Changing a skill

1. Branch from `origin/main` and edit `skills/<id>/`.
2. Run `ai-rules setup` from the clone to try it (it reads `skills/` from disk).
3. In the same commit, update whatever the change affects: inventories
   (`docs/threejs/inventory.json`), counts or allow-lists in
   `scripts/validate_skills.py`, `evals/<id>.json`, and the tests in `tests/`.
4. Run `python scripts/ci_checks.py --group skills`, then open a PR.

## Adding a skill

One PR:

1. `skills/<id>/` with `SKILL.md` (`name: <id>`) and `README.md`.
2. `src/ai_rules/catalog/data/capabilities.json`: copy an existing first-party
   entry; set `id`, and `source` to `branch` `main`, `subpath` `skills/<id>`.
3. `src/ai_rules/profiles/data/profiles.json`: add the id to `everything` and to
   any profile that should install it.
4. `scripts/validate_skills.py`: add the id to `RUNTIME_SKILLS` (a family with
   internal methods gets its own validator instead, like `threejs-skills`).
5. `evals/<id>.json`: at least one `behavior` and one `negative-trigger` case.
6. `docs/ci-coverage.md` coverage map and the README tables.

Done when `python -m unittest tests/test_skill_registry_consistency.py` and
`python scripts/ci_checks.py` pass.

## Removing a skill

Reverse the six steps in one PR, and delete tests and fixtures that exist only
for that skill (`tests/test_<id>.py`, `tests/installer/test_<id>.py`,
`evals/<id>*.json`). Installed copies stay on users' machines; setup no longer
offers the skill. Done under the same two checks.
