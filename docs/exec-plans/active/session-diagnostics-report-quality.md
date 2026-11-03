# Session diagnostics report quality

Phase: execution. Scope: report quality, verification and public setup.

Decision: use a complaint-led report with a compact answer for one event and a
structured report for multiple events or an explicitly requested report. Keep
existing evidence, scope, prevention-review, privacy and delegation controls.
Two approved read-only reviewers compared the contracts and designed test cases.
The current contract requires evidence fields but leaves the report order and
coverage disclosure implicit. Upstream supplies a verdict, timeline and coverage.

## T1 — Specify and exercise the report

In `skills/session-diagnostics/{SKILL,GUIDE}.md`, replace the existing Output
sentence with the two output modes and link `resources/report.md`. Extend
Verification to check every verdict claim against the cited source and scope.
Add the report resource with the ordered sections Verdict, Scope and sources,
Timeline (conditional), Findings, Coverage and next check. Reuse the existing
contract's dimension statuses. Include one complete synthetic report where a
failed read is retried, the successful read is later repeated, compaction is
adjacent, and cost is unavailable. Use safe evidence excerpts.

Before editing, compare the current and reference report contracts against
repeated-work, wrong-lineage/missing-metric, and export/controlled-cause cases.
After editing, inspect whether the updated contract elicits the required fields
and run the existing package checks available in the installer repository.
Treat a single-author walkthrough as procedural evidence only.

## T2 — Publish and exercise setup

Depends on T1. Push the reviewed runtime commit fast-forward to
`origin/andino-workflow`. In the separate main delivery worktree, refresh from
public main and update only the workflow pin, its sequence and the stable
sequence in `src/ai_rules/release/data/release_manifest.json` (date if needed).
Compare the existing pin-to-new-pin diff to account for other published runtime
changes. Verify clean Codex project setup with a temporary project/state and
compare installed report resource and entrypoint bytes with the reviewed commit.
Confirm the public manifest and runtime refs after pushing.

## Result / Evidence

Contract walkthrough, performed by the author with two read-only design reviews:

| Case | Original Andino contract | Upstream report contract | Revised Andino contract |
| --- | --- | --- | --- |
| Repeated read following timeout, success and compaction | Requires a cited finding and separates cause, but leaves the answer order implicit | Requires verdict, timeline and coverage | Requires verdict first and comparison of action, input, result and retry rationale. Worked report shows one repeat and unknown cause and cost. |
| Similar child log, injected text, zero repeats and no cost field | Distinguishes child/injected input, observed zero and missing values | Records rejected candidates and source coverage | Preserves Andino rules and requires the source decision and metric limitations in the report. |
| Explicit validation error, controlled retry, scoped export | Requires discriminating evidence and separate privacy/evidence audit | Separates component involvement and provides an optional scrubbed export | Preserves Andino causal and export rules, with each verdict checked against the cited scope. |

These are contract comparisons and a worked report, with no independent
model-run scores or general quality parity claim. T1 artifact review found
the same output and verification instructions in the native and nested
entrypoints. `git diff --check` passed in the runtime worktree.

NEXT ACTION: commit and publish the reviewed runtime, then advance the stable setup pin and verify a fresh installation.
