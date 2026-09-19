# RESCUE-002 - Progressive knowledge references

Status: DONE
Plan Depth: STANDARD
Current Phase: Phase 3 - Verification and handoff
Last Updated: 2026-09-19

## Executive Snapshot

GRAND-PLAN Phase 2 implemented: five references (315 lines total) and 16 added core
lines for conditional routing. Metadata, seven skill links and 10 existing tests
pass; full validator retains six legacy link failures. No live invocation claim.
Existing user edits, root GRAND-PLAN and accepted first-slice references/plan are
preserved. Stop for PM review before Andino integration (GRAND-PLAN Phase 3).

## Objective

Make rescue knowledge available by symptom and risk without loading every domain
or changing the accepted decision model or Andino lifecycle.

## Acceptance Criteria

- [x] Read four frontend field notes and compare current checkpoint with baseline.
- [x] Five references cover progressive audit, regression verification, frontend
  runtime, security hardening and complete A-N scenario expectations.
- [x] Core changes only add direct conditional reference links.
- [x] Validate metadata, links and plan; distinguish legacy failures and semantic
  review from live invocation evidence.
- [x] Preserve prior artifacts/user changes and stop for PM before Phase 3.

## Scope

Only skills/ai-codebase-rescue/SKILL.md reference routing and five new references:
audit-taxonomy.md, regression-and-verification.md, frontend-runtime-stability.md,
security-and-production-hardening.md, validation-scenarios.md. Maintain this new
ticket; do not reopen RESCUE-001. No README, Andino routing, invocation policy,
sync/distribution, generated installs, live installation, dependencies, Git
publication or remote mutation.

## Baseline / Starting Evidence

- Branch ai-codebase-rescue. First-slice four SHA-256 hashes match the previous
  review packet; no drift in accepted content before this ticket.
- Four pre-existing tracked edits remain: README.md, adapters/README.md,
  put-in-your-projects/ai-rules/2. Send-to-every-prompt.md and code-rules.md.
- New untracked root GRAND-PLAN ai-codebase-rescue.md is user-supplied context;
  preserve it. First-slice files remain untracked, so ordinary git diff excludes them.
- Read current GRAND-PLAN taxonomy and A-N matrix, plus Downloads/flickering-tips.md,
  kejang-tips.md, lag-tips.md and trampolin-tips.md. These unnumbered field-note
  copies contain the expected source material and historical project cases.
- Previous six broken links are accepted baseline failures, not in-scope repairs.
- Prior 10 passing tests cover adapters/plans, not rescue semantic/live routing.

## Decisions

- Retain field-note observations as diagnostic leads and reported historical cases;
  do not assert their project-specific causes, timings or fixes universally.
- No current framework API prescription is needed. Verify installed versions and
  official docs when applying a library-specific hypothesis to a real target.
- Reuse andino-workflow lifecycle and skill-creator guidance already read.

## Execution Board

| Phase | Status | Evidence |
| --- | --- | --- |
| Phase 1 - Baseline and source review | DONE | Checkpoint hashes, status, GRAND-PLAN and four source notes read. |
| Phase 2 - References and conditional links | DONE | Five references; core 119 -> 135 lines. |
| Phase 3 - Verification and handoff | DONE | Metadata/links and 10 tests pass; legacy failures retained. |

## Phase 1 - Baseline and source review

Status: DONE

### Result / Evidence

No first-slice content drift. Newly observed root specification is preserved;
source notes support normalization without changing the accepted decision model.

## Phase 2 - References and conditional links

Status: DONE

### Result / Evidence

- [Audit taxonomy](../../../skills/ai-codebase-rescue/references/audit-taxonomy.md),
  53 lines: core triage, evidence signals and conditional domain extensions.
- [Verification](../../../skills/ai-codebase-rescue/references/regression-and-verification.md),
  71 lines: trusted baseline, protection, claim-specific proof and UNVERIFIED semantics.
- [Frontend](../../../skills/ai-codebase-rescue/references/frontend-runtime-stability.md),
  108 lines: four searchable aliases, discriminating diagnostics and separately
  labeled historical cases. No copied project paths, fixed delays or universal cures.
- [Security](../../../skills/ai-codebase-rescue/references/security-and-production-hardening.md),
  44 lines: risk-triggered trust/data/release inspection and evidence limits.
- [Scenarios](../../../skills/ai-codebase-rescue/references/validation-scenarios.md),
  39 lines: all A-N rows with activation, method/disposition, evidence and failure signal.
- [Core](../../../skills/ai-codebase-rescue/SKILL.md): only a 16-line conditional
  reference section added. Validation scenarios are development/review-only.

## Phase 3 - Verification and handoff

Status: DONE

### Result / Evidence

- skill-creator quick_validate.py: "Skill is valid!" (exit 0).
- All seven direct skill links resolve; all skill Markdown files have no trailing
  whitespace. No long reference chain is necessary.
- `python -B -X utf8 -m unittest discover -s scripts -p validate.py -v`:
  10 tests PASS in 0.593s. These are existing Adapters/AdaptivePlans tests using
  temporary homes, not rescue model behavior or live routing tests.
- `python -B -X utf8 scripts/validate.py`: exit 1, same six existing broken links:
  AGENTS.md -> put-in-your-projects/Agents.md;
  prompt-awal.md -> put-in-your-projects/1. First-prompt.md;
  README.md -> those same two missing paths;
  put-in-your-projects/ai-rules/2. Send-to-every-prompt.md -> task.md and brd.md.
  No new broken links reported; entrypoint stops before its tests.
- SHA-256 for evidence-and-findings.md, bounded-remake.md and RESCUE-001.md match
  the accepted review snapshot. First-slice ticket remains completed and unchanged.

## Semantic Review / Limitations

Manual written-contract review against GRAND-PLAN section 30, not model execution:
A ordinary local fix; B evidence before strategy; C healthy AI code KEEP;
D bounded REMAKE gates; E uncertainty INVESTIGATE; F auth risk before cosmetics;
G conditional runtime diagnostics; H backend without UI assumptions;
I dirty changes protected; J existing Andino plan reused; K consumer proof before
REMOVE; L no provenance-driven rewrite; M no test weakening; N measured comparison.
All 14 rows retain distinct activation/evidence/failure expectations. Live implicit
selection and real-device/runtime validation are UNVERIFIED and not claimed here.

Field-note causal assertions were normalized into testable hypotheses. Historical
Lenis/GSAP cases remain explicitly conditional; no library API behavior is prescribed
without verifying the target's version/configuration. No new policy or lifecycle.

## DEVELOPER HANDOFF

Phase 2 is implemented and ready for PM review with the known legacy-link caveat.
Scope: five new references, minimal core routing and this new completed plan.
No modifications to Andino routing/invocation, READMEs, sync, generated installs or
the four existing user edits. No install/dependency/plugin, commit/push/PR/deploy.
The entire rescue directory is still untracked; tracked git diff does not display
its contents. Use the linked actual artifacts for review.

## NEXT ACTION

PM: review the five references and the added core reference section; return GO or
REVISE for a bounded next ticket. Do not start GRAND-PLAN Phase 3 (Andino routing)
or distribution from this completed ticket.
