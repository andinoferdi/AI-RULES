# Documentation and ADR quality

Status: IN_PROGRESS
Current phase: Setup distribution
Base: workflow 8ecb810, main d6aa6fa.

## Decisions

No historical output supplied. Compare explicit guidance on three synthetic
cases against baseline Andino and Addy. Assess artifact choice, concrete
rationale or consumer impact, preservation of constraints and verification.
Use direct review with zero workers. This measures guidance coverage, not
independent model performance.

## T1 — Artifact guidance

Readiness: READY. Dependencies: none. Status: DONE.

In `skills/documentation-and-adrs/{SKILL,GUIDE}.md`, replace the broad numbered
Procedure with evidence and artifact selection, ADR convention and lifecycle,
consumer contract, prose preservation and scoped verification steps. Keep the
existing operational probe and its fixed outputs, permissions, provenance and
domain vocabulary routing. Both entrypoints link `resources/worked-example.md`.
That new resource contains:

- Existing ADR-004 RST → proposed ADR-005 RST. Preserve 50 requests/minute as
  a measured operating point with its uncertainty. Prior status changes only
  after acceptance. Show rejected alternatives and an observable revisit trigger.
- A public API adding a verified 409 conflict outcome. Record retry semantics
  and distinguish an observed response from an unchecked example.
- A small README correction using a verified command. Edit the canonical
  quickstart and preserve its prerequisites. No ADR.

Run `git diff --check`, check both entrypoint links and compare the example
against these conditions. Run the existing Addy operational checker against
this workflow checkout with its output directed to a temporary file.

Evidence: Both entrypoint links resolved and the scoped whitespace check
passed. The ADR checker passed its normal, dropped-qualifier and reused-number
cases. The broader legacy checker reported failures in ten other methods.
Direct comparison found that both baselines cover the three artifact families.
The revised guidance adds proposed-versus-accepted status handling, consumer
retry and side-effect checks, and an explicit distinction between source checks
and execution. The Addy guide also gives a full README and OpenAPI specimen.

## T2 — Setup distribution

Readiness: READY. Dependencies: T1. Status: IN_PROGRESS.

Commit and push the skill and checkpoint to `origin/andino-workflow`. In an
isolated worktree from `origin/main`, update
`src/ai_rules/release/data/release_manifest.json`. Advance root and workflow
`release_sequence` from 28 to 29 and pin the new workflow commit. Leave
existing main checkout edits intact. Run `ai-rules setup` against disposable
Codex project roots for bundled and latest. Compare both installed entrypoints
and worked example against the workflow source, normalizing CRLF only.
Commit and push the manifest. Record exact setup evidence here.

## NEXT ACTION

Publish the scoped workflow change, then verify and publish its setup pin.
