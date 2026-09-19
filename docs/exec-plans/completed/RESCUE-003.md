# RESCUE-003 - Andino rescue integration

Status: DONE
Plan Depth: STANDARD
Current Phase: Phase 3 - Verification and handoff
Last Updated: 2026-09-19

## Executive Snapshot

Phase 3 implemented: one specialist route and lifecycle boundary (11 added lines),
five routing scenarios and invocation guidance (34 added lines). Ten existing tests
pass; full validator retains the six legacy failures. Live routing is UNVERIFIED.
Branch ai-codebase-rescue, HEAD dfdd251, was clean on entry; an intervening commit
already contained prior artifacts/user edits. README and rescue methodology remain
unchanged. Stop for PM review before Phase 4.

## Objective

Route justified bounded rescue to ai-codebase-rescue while keeping ordinary bugs
local and Andino the sole lifecycle owner. No distribution or live invocation work.

## Acceptance Criteria

- [x] Inspect repository drift and current routing/scenarios.
- [x] Add narrow positive triggers, evidence/provenance boundaries and shared-plan semantics.
- [x] Document rescue A/B/J, explicit and vague invocation cases and safe user guidance.
- [x] Preserve all rescue methodology, completed plans and prior user changes.
- [x] Validate actual changes and report legacy failures separately from live routing.
- [x] Stop for PM review before GRAND-PLAN Phase 4.

## Baseline / Decisions

- `git status --short --branch`: ai-codebase-rescue with no modifications.
- `git log` / `git show --stat HEAD`: dfdd251 follows f3210ca and includes prior
  rescue artifacts, GRAND-PLAN and four previously dirty user files. This ticket
  neither created that commit nor infers remote push from its subject "push".
- Current routing table supports adding one specialist without lifecycle changes.
- docs/routing-scenarios.md is existing clean routing documentation; add invocation
  examples there. README edits are unnecessary even though it is now clean.
- Existing A-H scenarios are unrelated identifiers; label additions Rescue A/B/J
  to avoid conflating them with the accepted rescue validation matrix.
- Six existing Markdown link failures remain outside scope. Live host selection
  remains UNVERIFIED; canonical routing text is not proof of installed behavior.

## Scope

Edit skills/andino-workflow/references/routing.md and docs/routing-scenarios.md.
No rescue methodology changes, README edits, sync scripts, generated/live installs,
host invocation policy, dependencies, commits, push, PR, merge or deployment.

## Execution Board

| Phase | Status | Evidence |
| --- | --- | --- |
| Phase 1 - Baseline | DONE | Clean status; intervening commit inspected; target docs read. |
| Phase 2 - Routing and scenarios | DONE | Minimal specialist route and five scenarios. |
| Phase 3 - Verification and handoff | DONE | Diff reviewed; 10 tests PASS; legacy failures disclosed. |

## Phase 1 - Baseline

Status: DONE

### Result / Evidence

Current repository supersedes stale dirty-state facts. No collision or lifecycle
change is needed. Accepted previous tickets remain completed and untouched.

## Phase 2 - Routing and scenarios

Status: DONE

### Result / Evidence

- [Canonical routing](../../../skills/andino-workflow/references/routing.md): one
  table entry plus a short boundary paragraph. Eligibility, provenance separation,
  smallest justified surface and Andino-owned plan/acceptance remain explicit.
- [Scenarios and invocation guidance](../../routing-scenarios.md): Rescue A/B/J,
  explicit and vague invocation cases; examples conditional on host availability.
- Use existing clean scenario documentation instead of README. No sibling-skill
  filesystem link added to installed routing: host catalog resolution remains the
  existing mechanism, avoiding a distribution dependency.

## Phase 3 - Verification and handoff

Status: DONE

### Result / Evidence

- `python -B -X utf8 -m unittest discover -s scripts -p validate.py -v`: all
  10 existing adapter/plan tests PASS in 0.624s, including install/reference
  resolution without source and idempotence/drift protection, in temporary homes.
  These do not test model selection or prove live invocation.
- `git diff --check`: exit 0; diff reviewed, only 45 additions across the two
  approved existing documents. Prior user changes and rescue artifacts unchanged.
- `python -B -X utf8 scripts/validate.py`: exit 1 on exactly the same six legacy
  links, with no new failure: AGENTS.md -> put-in-your-projects/Agents.md;
  prompt-awal.md -> put-in-your-projects/1. First-prompt.md; README.md -> both
  missing paths; put-in-your-projects/ai-rules/2. Send-to-every-prompt.md -> task.md
  and brd.md. Its test suite is not reached; unittest ran separately above.

## Manual Contract Review

Written-rule inspection only: Rescue A stays ordinary; B requires eligibility and
engineering evidence; J reuses the existing plan; explicit invocation obeys native
availability, lifecycle and authorization; vague authorship/cleanup requests do not
select rescue/remake automatically. No new disposition, independent DONE or second
checkpoint. All positive triggers requested by PM are represented in the route.
Actual host/implicit routing remains UNVERIFIED. No live installs were changed.

## DEVELOPER HANDOFF

GRAND-PLAN Phase 3 ready for PM review. Two edited documents plus this new completed
ticket; README safely avoided via existing routing documentation. The clean HEAD
dfdd251 baseline supersedes prior dirty-state facts without changing ownership or
authorization. No Phase 1/2 drift, sync, generated-install edits, host configuration,
commit/push/PR/merge/deploy or Phase 4 work.

## NEXT ACTION

PM: review actual routing.md and routing-scenarios.md changes and verification
limits above; return GO or REVISE before any managed multi-skill distribution work.
