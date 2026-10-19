# Andino phase-readiness routing repair

Status: IN_PROGRESS
Owner: Andino Workflow / Claude Code
Date: 2026-10-19
Density: STANDARD

## Objective and acceptance

Repair the routing path that let `/andino-workflow` plus "buatkan saya web crud,
tapi saya bingung gimana" jump to design and implementation without exploring the
open product direction (ULTIMATE-PROMPT.md). Keep Andino the single orchestrator,
keep Focus, Search First, debugging, TDD, verification, thesis and UI contracts
intact, and prove the change with before/after host runs.

Authorization: local commits only on `andino-workflow` and `main`. No push, no
publication, no change to installed skills or global host configuration.

## Decisions

- Live core set (six cases) on Codex, Claude Code, OpenCode and Antigravity CLI;
  extended suite on Claude Code only. Antigravity IDE is reported separately.
- Evaluation modes `read-only` and `isolated-writable` share one contract across
  actor prompt, host permissions and record metadata.
- Verdicts stay PASS / FAIL / NOT_VERIFIED; undecidable results use NOT_VERIFIED
  with a `reason` (INCONCLUSIVE_BEHAVIOR, PROVENANCE_MISMATCH, HOST_UNAVAILABLE,
  CONTAINMENT_UNVERIFIED, SMOKE_FAILED).
- Boundary probes target only an evaluator-owned `sentinel/` directory and run
  only where containment comes from a verified mechanism.
- Each record states `coverage: routing` or `coverage: application`; PASS covers
  only that scope.
- `release_manifest.json` and lineage files stay unchanged; the local candidate is
  recorded in `docs/validation/andino-readiness/candidate.json` as
  LOCAL_CANDIDATE_UNPUBLISHED.

## CURRENT STATE

Runtime base `andino-workflow` 634585a (equals origin and the manifest pin).
Runtime worktree: `C:/Users/Lenovo/Downloads/AI-RULES-worktrees/andino-workflow`.
Main edits in the primary checkout; user file `ULTIMATE-PROMPT.md` stays untracked.
Pre-existing drift: lineage hashes in publication-lineage.json and
capability-runtime-lineage.json do not match 634585a; left as found.

## CURRENT PHASE

Harness and scenarios.

## Execution board

| Phase | Status | Evidence |
| --- | --- | --- |
| Setup and checkpoint | DONE | worktree at 634585a |
| Eval modes, host adapters, unit tests | IN_PROGRESS | |
| Readiness scenarios | IN_PROGRESS | |
| Host smoke tests | PENDING | |
| Baseline and hypothesis review | PENDING | |
| Contract test RED, routing repair | PENDING | |
| After-fix runs, regression suite | PENDING | |
| Candidate record, review, local commits | PENDING | |

## EVIDENCE

(filled as phases complete)

## NEXT ACTION

Finish evaluation-mode contract in `scripts/validate_andino_capabilities.py` and
host adapters in `scripts/run_andino_capability_eval.py`, then smoke-test hosts.
