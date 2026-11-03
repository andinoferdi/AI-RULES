# Plan execution acceptance evidence and provenance

Status: IN_PROGRESS
Phase: Delivery
BASE: 915d5e9306c96dd5d854d312e48f3348708951c3
Branch: andino-workflow
Date: 2026-11-03

## Decision and baseline

Extend the existing checkpoint and review contracts. Superpowers compares expected
results per task. Addy Osmani keeps increments independently verifiable. Existing
Andino handles zero-test commands and maps acceptance to evidence, but its explicit
skip rule only covers empty or wholly skipped discovery. In a synthetic case with
12 passing tests and the one required contract case skipped, existing prose makes
the per-criterion disposition implicit. Existing prose already handles stale plan
rulings and drift, so keep those behaviors. This is a source walkthrough, not a
fresh model benchmark. Council is unnecessary for this bounded decision.

## Tasks

1. DONE — In plan-execution GUIDE and synchronized SKILL body, step 4,
   require an observed matching assertion or equivalent proof for each criterion.
   If the required case was skipped, keep that criterion NOT_VERIFIED even if
   unrelated cases pass. Block only dependent tasks and keep one checkpoint.
   Mirror this in resources/contract.md and add a partially skipped run and an
   equivalent-proof case to resources/worked-example.md.
2. DONE — In references/license.md, identify Matt Pocock's historical source path
   as historical and link the verified root MIT license pinned to the inspected
   upstream revision. Preserve the notices for all three sources. Point the main
   entrypoints at the notice and clarify local task provenance. GitHub API returned
   MIT and LICENSE blob f1dd2c09108dde1a5f56097cee8461b3ea834499. Current old path 404.
3. IN_PROGRESS — Review full owned diff, run main's verify-execution.py against this
   worktree, check positive and negative consumer scenarios, then commit and push.
   Use latest setup, verify installed nested and standalone Codex member files
   against the reviewed revision. Main checkout has unrelated changes. Use its
   validator read-only. Update setup code only if observed integration requires it.

## Result / Evidence

- Drift audit: branch advanced during work, with no intervening changes to
  plan-execution. Scope staging to the owned files. Preserve concurrent edits.
- Structured self-review of the scoped diff: Spec PASS for the content changes
  and Standards PASS for entrypoint consistency and local resource layout.
  GUIDE lacked the existing resource selection table. Both entrypoints now use it.
- verify-execution.py passed entrypoint sync, drift fixture, missing/empty identity
  and mutation assertions. Full validator failed on an unrelated Search First
  allowlist mismatch. Direct package_files validation of the workflow returned
  no errors. git diff --check passed for owned skill changes.
- Latest Codex setup dry run resolved three targets with one planned update.

NEXT ACTION: Commit and push scoped workflow changes, then run setup and compare
installed files. Advance the main release manifest if needed for future bundles.
