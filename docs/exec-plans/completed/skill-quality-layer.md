# Skill quality layer

Status: DONE
Plan Depth: STANDARD
Current Phase: Phase 5 — Stage review snapshot
Last Updated: 2026-09-20

## Executive Snapshot

Local `main` points to the former `WebBased` HEAD (`89c8ffc`). A complete staged snapshot now contains 19 intended distribution deletions, the control-plane README, and eight quality-layer files. There are no relevant untracked files or staged generated caches. Local structural validation and six unit tests pass. Live behavioral execution remains unverified; no commit or remote action occurred.

## Objective

Make both skills' structure and key behavioral expectations reviewable and mechanically checkable without expanding either runtime package.

## Acceptance Criteria

- [x] Both skills have positive and negative evaluation cases covering the requested invariants.
- [x] Standard-library validation rejects malformed metadata, broken internal links, and invalid evaluation structure.
- [x] CI is configured to run the deterministic checks against both branch heads; its scheduled trigger depends on the default branch.
- [x] Local validation ran and results are recorded; live behavior is reported separately.
- [x] Runtime branch contents remain unchanged; no commit, push, merge, release, or deploy.

## Scope

Preserve the existing quality layer on local `main` and stage the complete control-plane tree for review. Do not alter the three distribution branches' installation contracts.

## Baseline / Starting Evidence

- `WebBased` clean at `89c8ffc`; each skill branch has only `README.md`, `SKILL.md`, and `references/`.
- No existing repository evaluation or CI files were found in either skill branch.
- `ai-codebase-rescue/references/validation-scenarios.md` is a review oracle, not executed live evaluation.

## Decisions Log

- D-001 — Superseded by reviewer REVISE: placing development tooling on `WebBased` was an inference, not a repository decision.
- D-002 — Use JSON cases and Python standard library. They can be checked in CI without a model provider or new dependency.
- D-003 — The reviewer resolved the branch decision: create non-orphan `main` from `WebBased` history and remove Web/chat distribution files only from `main`'s intended tree. No remote action is authorized.
- D-004 — Stage only the eight inspected quality-layer files and README; keep generated Python cache files ignored. This prepares review evidence without authorizing commit.

## Execution Board

| Phase | Status | Goal | Evidence / Result |
| --- | --- | --- | --- |
| Phase 1 — Inspect | DONE | Confirm branch layout and constraints | Clean `WebBased`; two separate skill branch trees inspected. |
| Phase 2 — Implement checks and cases | DONE | Add quality layer | Two JSON case files, Python validator, unit tests, and workflow added. |
| Phase 3 — Verify and handoff | DONE | Run checks, inspect diff, report limits | Local validator and six unit tests passed; live behavior not run. |
| Phase 4 — Verify local main | DONE | Prepare `main` and validate preserved quality layer | Local `main` shares `89c8ffc` with `WebBased`; Web/chat files removed only from its tree; validator, six tests, and diff check pass. |
| Phase 5 — Stage review snapshot | DONE | Make index match intended control-plane tree | Nine control-plane files and 19 distribution deletions staged; no relevant untracked or generated files; cached diff check passes. |

## Verification

- `python scripts/validate_skills.py`: PASS for both skill branches; live behavior NOT VERIFIED.
- `python -m unittest discover -s tests`: six tests PASS, including malformed metadata, broken link, and unexpected runtime file rejection.
- CI workflow is configured but has not run remotely.
- `git diff --check HEAD`: PASS on local `main`.
- GitHub default remains `WebBased`; scheduled workflow on `main` cannot run until a separately authorized default-branch change.
- `git diff --cached --check`: PASS; index contains only the intended control-plane tree.

## NEXT ACTION

None — staged snapshot is ready for reviewer verdict. Commit, push, and default-branch changes remain separate future decisions.

## Post-push verification

- `main` was pushed; GitHub now reports `main` as the default branch.
- Remote workflow `Validate skills` run [35496824578](https://github.com/andinoferdi/AI-RULES/actions/runs/35496824578) completed successfully for commit `f95b7701722ddbef85675e017d067ec775300bf1`.
- `Fetch skill branches`, `Validate`, and `Test validator failure cases` all passed in that run.
- Live behavioral evaluation remains NOT VERIFIED.
