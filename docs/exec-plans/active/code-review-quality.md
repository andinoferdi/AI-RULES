# Code review quality

Status: DONE
Depth: STANDARD
Current Phase: Delivery

## Executive Snapshot

The existing skill separates Spec and Standards, reads tests early, and limits
feedback disputes to one evidence cycle. Its scope rule includes local edits
even for commit-only requests. Its reviewer handoff lists local changes while
providing only committed-diff commands. Establish a fresh-context baseline
before changing the skill.

## Objective and acceptance

- Preserve the two axes, early test inspection, severity labels, and evidence-based reception.
- Verify scope selection, evidence-backed findings, missing-spec handling, and a clean review on reproducible cases.
- Match the surrounding Andino member layout and preserve the installed skill ID.
- Publish the verified revision and confirm a clean setup resolves and installs its content.

## Execution Board

| Phase | Status | Evidence or exit |
| --- | --- | --- |
| Initial audit | DONE | Local source and all four upstream skill entrypoints inspected. |
| Baseline | DONE | Both agents found both real defects and cleared the clean case. The current skill respected the explicit commit scope despite contradictory instructions, disclosed the missing spec, and counted the transaction defect on both axes. The unguided output omitted the missing-spec limit. |
| Plan and implementation | DONE | Candidate found both defects, reported the refund issue once, marked missing Spec as unverified and returned no findings for the clean case. It distinguished reported CI from checks run. SQLite reproduced and verified rollback. Markdown links and whitespace checks passed. |
| Delivery | DONE | Workflow published at `e858427`. Both setup sources installed six exact files in each of the native and nested Codex project copies. Main published the bundled pin at `d6aa6fa`. |

## Decisions

- Use synthetic fixtures because no historical review failure was supplied.
- Leave unrelated edits in the separate main checkout intact. Its capability
  catalog already identifies the andino-workflow branch as the family source.
- Run baseline evaluation with the same model and effort across conditions.
  Independent runs require explicit wave approval.

## NEXT ACTION

None. Delivery complete.

## Verification limits

- One independent sample per condition across three synthetic cases. This
  evaluates the specified review behaviors, with no general ranking against
  the upstream skills.
- The full package validator rejected the existing search-first file
  `references/consolidation-provenance.json` on both the previous pin and the
  candidate. The focused review and real setup checks passed.
- Setup verification compared installed files in disposable Codex projects.
  It did not evaluate native discovery in a new Codex session.

## Implementation tasks

### T1 — Review contract (READY)

Owned paths are `skills/code-review/SKILL.md` and its existing GUIDE and
resources. Replace the fixed merge-base/WIP prerequisite with explicit scope
selection. Use two-dot for an explicit endpoint comparison, merge-base for
branch or PR review, and staged/unstaged/in-scope untracked content for WIP.
Record actual content or a reproducible snapshot for handoffs. Carry the same
selection in the agent brief, with dispatch subject to delegation approval.

Keep both axes and the four core severity prefixes. Report one finding per
root cause with a primary axis and a cross-reference when relevant. Use the
report order `Scope`, findings (highest severity first, tagged by axis),
`Axis verdicts`, `Verification and limits`, and `Declined to Judge`.
Each finding includes a changed location, reachable trigger, consequence,
evidence and practical remedy. Missing specification or incomplete required
evidence makes the applicable axis unverified. Confirmed blockers still block.
Preserve verified feedback and the one-cycle dispute boundary. Keep the
existing companion layout, replacing the inconsistent example with a refund
case backed by a runnable transaction failure check.

Check from the workflow checkout with `git diff --check`, run the worked
example with Python, and validate relative links. Use the three recorded
scenarios for candidate evaluation with the same model and effort as baseline.

### T2 — Setup distribution (depends on T1 and candidate evaluation)

Push the owned workflow paths to `andino-workflow`. In an isolated checkout of
`origin/main`, update only the release manifest's workflow pin and advance
its release metadata using the existing convention. Preserve changes in the
shared main checkout. Verify both latest and bundled setup with a disposable
Codex project and byte comparison of the native and nested skill copies to
the workflow Git tree. Push the verified manifest update.

## Baseline cases

1. Committed-only refund review. The spec requires an atomic refund and audit
   entry. The commit writes the refund, then writes the audit entry separately.
   The happy-path test passes. The working tree has an unrelated draft that
   would remove an authorization check. Expect one blocker for the partial
   write, the failure trigger and a test that injects an audit-write failure.
   Keep the local draft outside the verdict.
2. Work-in-progress review. The tracked diff adds a route that calls a new
   untracked handler. The handler reads a tenant by request ID without scoping
   it to the authenticated tenant. No spec is available. Expect a supported
   cross-tenant finding and an explicit limit on Spec coverage.
3. Clean refactor. A rename updates all callers and preserves behavior under
   existing tests. The requested working-tree scope is complete. Expect zero
   blockers and no invented issue or test execution claim.

Score scope, true positives, false positives, evidence and verification
limits separately. Read evaluator responses in full. Keep sample counts and
distinguish a small case comparison from a general quality claim.
