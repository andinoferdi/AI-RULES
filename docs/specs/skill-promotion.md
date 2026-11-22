# Skill promotion

Specification for how a skill change reaches `main` and `ai-rules setup`.
Decision record: [ADR 0001](../adr/0001-main-pins-skill-versions.md).

## Flow

```text
edit + push skill branch
        |
python scripts/promote_skill.py <skill>
        |  clone at .git/promote/<skill>, branch promote/<skill> from origin/main
        |  pin = origin/<skill> head (or --ref), release_sequence + 1
        |  skill_refs.py pin; ci_checks.py
        |
   checks fail ---> nothing pushed; fix skill branch or main tests in the clone; rerun
        |
   checks pass ---> push promote/<skill>, gh pr create  (--auto-merge: gh pr merge --auto)
        |
PR CI green ---> owner merges ---> main CI green ---> setup installs the new pin
```

Options: `--ref <commit>` pins a commit other than the branch head, `--dry-run`
runs the checks without committing or pushing, `--auto-merge` lets GitHub merge
once required checks pass. Rerunning while the PR is open, or while the clone has
uncommitted fixes, reuses the clone; otherwise the clone restarts from
`origin/main`. A skill already pinned at the target prints `nothing to promote`.

Requirements on the machine: Git, `gh` logged in with push access, and Python with
this repository's dependencies (`python -m pip install -e .`).

## What each gate guarantees

| Gate | Guarantee | Owner |
| --- | --- | --- |
| `ci_checks.py` in the promote clone | The new pin passes main's checks before anything is pushed | `scripts/promote_skill.py` |
| PR CI (`validate`, three `Installer (...)` jobs) | Same checks on GitHub's runners, on three operating systems | `.github/workflows/validate-skills.yml` |
| Ruleset on `main` | Only a PR with those checks green changes `main` | Repository settings |
| `setup --source latest` | Installs `main`'s pin, read live from GitHub | `src/ai_rules/release/latest.py::main_pins` |
| Daily CI run | The pins still pass on a fresh runner; drift listed in the run summary | `validate-skills.yml` schedule |

Model behavior of a skill stays outside these gates; see [CI coverage](../ci-coverage.md).

## Adding a skill

One PR from a branch of `origin/main`, after the new skill branch is pushed:

1. `src/ai_rules/catalog/data/capabilities.json`: add an entry with
   `source.branch` equal to the skill branch and `update_policy.model`
   `release_manifest` (copy an existing first-party entry).
2. `src/ai_rules/release/data/release_manifest.json`: add a `first_party` entry
   with `branch`, `ref` `origin/<branch>`, the 40-character `commit`, and
   `release_sequence` one above the top-level value; raise the top-level value too.
3. `src/ai_rules/profiles/data/profiles.json`: add the id to `everything` and to
   any profile that should install it.
4. `scripts/validate_skills.py`: add the id to `RUNTIME_SKILLS` (a family with
   internal methods gets its own validator instead, like `threejs-skills`).
5. `evals/<skill>.json`: at least one `behavior` and one `negative-trigger` case.
6. `docs/ci-coverage.md` coverage map and the README profile table.

Done when `python -m unittest tests.test_skill_registry_consistency` passes and
`python scripts/ci_checks.py` passes in a pinned clone.

## Removing a skill

Reverse the six steps above in one PR, and delete tests and fixtures that exist
only for that skill (`tests/installer/test_<skill>.py`, `evals/<skill>*.json`).
Leave the branch on GitHub; installed copies stay on users' machines and setup no
longer offers the skill. Done under the same two checks.
