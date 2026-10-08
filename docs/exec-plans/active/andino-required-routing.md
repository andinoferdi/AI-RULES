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

CURRENT PHASE: publication and local setup verification.
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
| Publication, setup and local alignment | IN_PROGRESS | Runtime pushed; main release pin/report and package repair pending |

## NEXT ACTION

Publish main release metadata and evidence, replace broken editable ai-rules install
with the reviewed ordinary package, then verify installed CLI and unchanged WebBased.
Behavioral follow-up remains: activation-order failures and blocked fixture operations;
see docs/validation/andino-workflow/required-routing-review.md. Do not claim all-host PASS.
