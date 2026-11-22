# Skill promotion gate
Status: IN_PROGRESS
Plan Depth: STANDARD
Current Phase: Phase 1 — Pins as the only source
Last Updated: 2026-11-22

## Executive Snapshot
Main CI went red without main commits because CI, several tests and
`ai-rules setup --source latest` read skill branch heads (`origin/<skill>`), while
main's tests and inventories follow the pins in
`src/ai_rules/release/data/release_manifest.json`. Observed failures
(runs 44897390384, 43256444235, 44988078285): `search-first: unexpected runtime
file`, `59 != 31` portfolio counts, `not a valid object name: andino-workflow`
(local branch name absent in CI) and capability registry drift.

Owner decisions (2026-11-22): local command trigger; ruleset on `main` requiring
PR plus CI; setup installs main's pins read live from GitHub; first real trial is
`natural-writing`; the four other branches ahead of their pins are promoted next so
users are not downgraded. Owner also asked for `AGENTS.md`, `CONTEXT.md` and
`docs/adr`, `docs/specs` (and `docs/agents` only if needed) on main, modelled on
the billing-backend layout. Commit, push, PR, merge and ruleset still need the
owner's go-ahead at each step.

## Objective
A skill change reaches `main` and `ai-rules setup` only through a promote PR whose
CI is green, started by one command.

## Acceptance Criteria
- [ ] R1: Main CI, its schedule and every test read only pinned commits; a push to
      a skill branch cannot change a main CI result.
- [ ] R2: `python scripts/promote_skill.py <skill>` pins the branch head on a fresh
      branch from `origin/main`, runs the same checks as CI, and opens a PR only
      when they pass.
- [ ] R3: `ai-rules setup` (default `--source latest`) installs the commit pinned on
      remote `main`, not the branch head; sources without a main manifest keep
      branch-head behavior.
- [ ] R4: Adding or removing a skill without updating catalog, manifest and
      validator lists fails with a message naming the missing place.
- [ ] R5: `AGENTS.md`, `CONTEXT.md`, an ADR and a spec explain the flow to an AI.
- [ ] R6: Ruleset on `main` requires PR and the CI checks.
- [ ] R7: `natural-writing` promoted through the command; main CI green after merge.

## Approach and Constraints
One pin file stays authoritative (`release_manifest.json`); `WebBased` gets a pin
under a new `validation_refs` key. A new `scripts/skill_refs.py` points
`refs/remotes/origin/<branch>` (and in CI/disposable clones `refs/heads/<branch>`)
at the pinned commits, so existing validators and tests that read those names read
pins without per-test rewrites. One check list, `scripts/ci_checks.py`, is used by
CI and by the promote command. Never rewrite local `refs/heads/*` in a developer's
checkout: the promote command runs checks in its own clone at
`.git/promote/<skill>` (a worktree would share refs with the user's branches).
No new dependency.

## Execution Board
| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — Pins as the only source | DONE | R1, R4 | T1–T3 | `test_skill_refs` 5/5, `test_skill_registry_consistency` 5/5 (Python 3.12 venv) |
| Phase 2 — Setup installs pins | DONE | R3 | T4 | `test_live_updates` 36/36 incl. two new pin tests |
| Phase 3 — Promote command | DONE | R2 | T5 | `test_promote_skill` 7/7; clone lives in `.git/promote/<skill>` (worktrees share refs) |
| Phase 4 — Agent docs | DONE | R5 | T6 | AGENTS.md, CLAUDE.md (`@AGENTS.md`), CONTEXT.md, ADR 0001, spec; docs/agents not needed |
| Phase 5 — Rollout | TODO | R6, R7 | T7 | Needs owner go-ahead |

## Coverage
| Requirement / failure case | Task | Check |
| --- | --- | --- |
| R1 branch head moves past pin | T1/T2 | `tests/test_skill_refs.py`: refs equal pins after `pin` |
| R1 CI uses pins | T2 | workflow uses `skill_refs.py pin` + `ci_checks.py`; CI run on PR |
| R4 catalog/manifest/validator mismatch | T3 | `tests/test_skill_registry_consistency.py` |
| R3 pin on main differs from head | T4 | `test_latest_installs_commit_pinned_on_main` |
| R3 no main manifest | T4 | existing `tests/installer/test_live_updates.py` stay green |
| R2 checks fail -> no PR | T5 | `tests/test_promote_skill.py` with stubbed runner |
| R2 manifest edit | T5 | same test: commit, sequence +1, date |
| R7 | T7 | PR CI + main push CI conclusions |

## Detailed Execution

### T1 — Pin refs helper
Status: TODO · Readiness: READY · Requirements: R1 · Depends on: none
Owns: proposed `scripts/skill_refs.py`; Test proposed `tests/test_skill_refs.py`;
Modify `release_manifest.json` (add `validation_refs.WebBased`).
Interfaces (proposed): `pins(manifest) -> dict[branch, commit]` (first_party +
validation_refs); `pin(repo: Path, remote='origin', local_branches=False,
fetch=True) -> dict`; CLI `pin [--local-branches] [--no-fetch]` and `drift`.
`pin` fetches each branch to `refs/remotes/<remote>/<branch>`, fetches the pinned
SHA directly when missing, then `update-ref` the remote ref (and `refs/heads/<b>`
when asked) to the pin. `drift` prints `skill pin head ahead` and always exits 0.
Test: temp repo with two commits on `focus`; manifest pins the first; after
`pin(..., fetch=False, local_branches=True)` both refs equal the first commit.

### T2 — CI reads pins through one check list
Status: TODO · Readiness: READY · Requirements: R1 · Depends on: T1
Owns: `.github/workflows/validate-skills.yml`; proposed `scripts/ci_checks.py`;
`docs/ci-coverage.md`.
`ci_checks.py` runs, in order and stopping at the first failure, exactly the six
commands of the current `validate` job (validate_skills with WebBased/threejs refs,
validate_threejs_family, validate_andino_capabilities, unittest discover,
validate_skripsi_traceability, build_release --stage-only into a new temp dir).
Workflow `validate` job: replace the hardcoded fetch with
`python scripts/skill_refs.py pin`, then `python scripts/ci_checks.py`,
then a non-failing `python scripts/skill_refs.py drift >> $GITHUB_STEP_SUMMARY`.
Installer matrix: add the same pin step before its unittest run.

### T3 — Registry consistency test
Status: TODO · Readiness: READY · Requirements: R4 · Depends on: T1
Owns: proposed `tests/test_skill_registry_consistency.py`.
Assert: first-party catalog ids == manifest `first_party` keys; each manifest
`branch` equals catalog `source.branch`; `validate_skills.RUNTIME_SKILLS` plus
`threejs-skills` == manifest keys; every profile capability exists in the catalog;
`everything` lists all first-party ids. Messages name the file to edit.

### T4 — Setup installs main's pins
Status: TODO · Readiness: READY · Requirements: R3 · Depends on: none
Owns: `src/ai_rules/release/latest.py::LatestSources.__init__`, `cli.py` help text;
Test `tests/installer/test_live_updates.py`.
After fetching a repository's branches, also try `+refs/heads/main:refs/heads/main`.
If `git show refs/heads/main:src/ai_rules/release/data/release_manifest.json`
parses and has `first_party[identifier]` with the same branch, use its `commit`
(fetch the SHA if absent; fail with a clear error if it still cannot be read).
Any failure to fetch main or read the file keeps the branch head. New test: fake
repo with `main` pinning commit A while the skill branch is at B; setup installs A.

### T5 — Promote command
Status: TODO · Readiness: READY · Requirements: R2 · Depends on: T1, T2
Owns: proposed `scripts/promote_skill.py`, `tests/test_promote_skill.py`, `.gitignore`.
Flow: refuse unknown skill (not in manifest) with a pointer to AGENTS.md "Adding a
skill"; `git fetch origin`; target = `origin/<branch>` head or `--ref`; worktree
clone `.git/promote/<skill>` on `promote/<skill>` from `origin/main` (reused while
its PR is open or it holds uncommitted fixes, so test fixes ship with the pin); update entry
`commit`, entry and top-level `release_sequence` = top + 1, top `verified_at` = today;
in the clone run `skill_refs.py pin` then
`ci_checks.py`; on failure print the failing step and keep the worktree, no push;
on success commit `Promote <skill> to <sha7>`, push, `gh pr create` with the
skill's `git log --oneline pin..target`; `--auto-merge` adds `gh pr merge --auto --squash`.
`--dry-run` stops before commit. Test the manifest edit and the "failed checks ->
no push" branch with a stubbed command runner.

### T6 — Agent docs
Status: TODO · Readiness: READY · Requirements: R5 · Depends on: T2, T4, T5
Owns: proposed `AGENTS.md`, `CONTEXT.md`, `docs/adr/0001-main-pins-skill-versions.md`,
`docs/specs/skill-promotion.md`; README pointer.

### T7 — Rollout
Status: TODO · Readiness: WAITING_ON owner go-ahead for commit/push/PR/merge
1. PR `skill-promotion-gate` -> green -> owner merges -> main push CI green.
2. Ruleset `main`: pull request required, required checks `validate` and the three
   `Installer (...)` jobs, block force push and deletion.
3. `python scripts/promote_skill.py natural-writing` -> PR green -> merge -> main CI green.
4. Same for search-first, threejs-skills, skripsi-skill, ai-codebase-rescue.

## Evidence (2026-11-22, local, Python 3.12 venv, disposable clone)
- Baseline origin/main at branch heads: unittest OK (skipped=5).
- Change set on pins: `ci_checks.py` all six steps PASS, 433 tests OK (skipped=5).
- New pin tests fail on the old code (RED): old setup installs the unpromoted head.
- First pinned run exposed `docs/threejs/inventory.json` matching the threejs head,
  not its pin; threejs pin moved to `4fe9d9c` (README-only diff).
- Not verified: GitHub runners (PR CI), ruleset, a real promote PR.

## NEXT ACTION
Owner go-ahead for T7.1: commit `skill-promotion-gate`, push, open PR, watch CI.
