# Required capability routing and setup delivery

Status: IMPLEMENTATION_DELIVERED; behavioral acceptance PARTIAL
Owner: Andino Workflow / Codex
Date: 2026-10-08
Density: LITE

## Objective and acceptance

Apply the approved three runtime-file patches and backed-up global Claude contract.
Preserve one router/lifecycle and native permissions. Run structural validators,
existing regression tests and ten isolated behavioral scenarios with honest evidence.
Publish runtime and setup metadata, verify remote setup and align local installations.
User explicitly authorized commit/push in the final instruction; no force push.

## Current state

CURRENT PHASE: implementation/publication delivered; behavioral acceptance remains partial.
Runtime baseline: effc3b8d7326d121317da86aff205de7c0bb0e80.
Main baseline: 20b840f059a6c6c25b41dfe498119735caa30c9f.
WebBased checkout remains untouched and clean. Separate managed worktrees:
`andino-routing/AI-RULES` and `andino-setup-release/AI-RULES`.
EVIDENCE: runtime 6cb04a4 pushed; 124 unit/regression tests and structural validators
pass. Ten final-runtime Codex cases: 4 scoped PASS, 2 FAIL, 4 NOT_VERIFIED. Exact
hash and reasons are in required-routing-review.md and the reviewed JSON records.
Claude authentication expired; no native permission bypass performed. Both setup
sources and five host target artifacts pass installation/NO_OP checks. Global
installed skill clones updated with backups and repeated setup reports NO_OP.
Decisions: approved runtime scope only; quality-plane evidence and release pins are
additional distribution work explicitly requested. No delegated development agents.
Live actor processes are isolated test executions, not implementation delegation.

## Execution board

| Phase | Status | Evidence |
| --- | --- | --- |
| Drift inspection and isolated checkouts | DONE | Remote refs, clean WebBased and local clones checked |
| Approved patches and verification | DONE | Runtime/global patch; 124 tests PASS; ten live samples reviewed with honest limits |
| Publication, setup and local alignment | DONE | Runtime 6cb04a4 and main delivery 9d4a1cb pushed; installed CLI verified from WebBased; all five local targets match commit/hash and report NO_OP |

## NEXT ACTION

Behavioral follow-up: on an authenticated host permitting fixture reads/writes,
rerun the two activation-order failures and four NOT_VERIFIED cases from
evals/andino-required-routing.json with hidden oracles. Compare native activation
events against the current commit and retain failures. See
docs/validation/andino-workflow/required-routing-review.md. No implementation,
publication or local setup action remains; do not claim all-host behavioral PASS.
