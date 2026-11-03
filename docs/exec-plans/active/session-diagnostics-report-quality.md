# Session diagnostics report quality

Phase: complete. Scope: report quality, verification and public setup.

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

T2: runtime `f06888212814f68a95ed7711f8a2a4aff9662cab` was pushed to
andino-workflow. Main `b3ad4d230c45300ea13801b567b88814a1ab1e35` published
stable sequence 34 with the reviewed pin and unchanged sibling pins. The new
workflow pin also includes intervening commits already on the remote workflow
branch. Original worktrees were left intact.

Fresh public-source Codex project setup ran in the isolated release worktree
with `python -m ai_rules setup --host codex --scope project --project-root
<temporary-project> --state-dir <temporary-state> --capability andino-workflow
--yes --non-interactive`. Exit 0, three installs, zero failures. The installed
native entrypoint and report resource matched the reviewed source after CRLF
normalization. Installed SHA-256 for report.md:
`373ea595175dac49b9feb4538df568667526d1deeb7d16ff0467686d02262899`.
This verifies installation and file content. Native invocation and independent
model performance were outside the executed checks.

NEXT ACTION: None — delivery complete.
