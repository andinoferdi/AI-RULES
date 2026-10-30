# Illustrative execution trace and consumer pressure cases

This is a synthetic scenario, not observed output from the user's repository.
Actual commands, hashes and results must be recorded by the consumer in its plan.

## Trace

An accepted CSV plan has T1 quoting names and T2 exact case-sensitive filtering.
T2 consumes T1's row interface. Local implementation is authorized; push is not.
An unrelated user note and an unfinished test are already present.

1. Read plan/spec, status and task BASE; attribute partial work and preserve notes.
   Compare T1's produced row shape with T2's consumer and checkpoint the result.
2. Run T1's existing test. If already GREEN, inspect literal assertions and actual
   CSV parsing before accepting existing behavior. Otherwise observe a meaningful
   assertion RED, implement the smallest quoting change, observe GREEN and appropriate
   regression. Missing imports require setup repair before behavioral RED.
3. Record actual command/directory/result, counts and source/test hashes. Never invent
   a later commit hash when no commit occurred. Mark T1 DONE only with acceptance.
4. T2's action lowercases names although accepted requirements specify case sensitivity.
   Record the smallest spec-grounded ruling and cost if wrong, then test one matching
   behavior RED to GREEN. Propagate any interface correction to consumers.
5. A check exits 0 but finds zero tests: keep acceptance incomplete, correct discovery
   and inspect the real result before marking T2 DONE.
6. Review baseline-to-current content including staged, unstaged and owned new tests.
   Read full diff and relevant files; --stat is only an index. Keep unrelated notes
   outside owned review/staging. Supply actual evidence and rulings to an authorized
   reviewer, or disclose a separate self-review.
7. An important empty-input defect survives a first repair. Keep acceptance incomplete,
   diagnose the new failure and rerun affected checks; a pass count does not grant DONE.
   Defer optional wording polish with a reason.
8. Publish only with actual authorization. If prior authorization exists, proceed and
   verify the remote ref. Otherwise checkpoint that blocker and finish independent local
   work. When setup is requested, compare installed content with the reviewed revision.

## Fresh consumer pressure cases

Ask a fresh consumer for concrete next actions, observations and checkpoint state.
Assess decisions rather than keyword mentions.

| Pressure | Required outcome |
| --- | --- |
| Prior PASS lacks identity | Revalidate; missing fields cannot authorize reuse. |
| Producer changed, unrelated docs unchanged | Reopen affected consumers; preserve independent evidence. |
| Meaningful test already GREEN | Inspect coverage and preserve satisfied behavior. |
| RED is import error | Repair setup before claiming behavioral RED. |
| Exit 0 with zero cases | Keep verification incomplete. |
| Required artifact check unavailable | Exact criterion stays NOT_VERIFIED; continue independent work. |
| Dirty user file plus owned new test | Preserve user bytes and include owned test in review. |
| Push authorized earlier | Proceed within scope and verify remote state. |
| Delegation or push forbidden | Respect restriction; continue independent permitted work. |
| Important finding survives repair | Acceptance remains incomplete with concrete NEXT ACTION. |
| Static guide correction | Artifact/consumer checks; no artificial code RED. |
| Installed native member differs from nested | Setup acceptance fails until reviewed bytes match. |

## Evidence limits

The guide's runnable drift example proves only that bounded algorithm. Consumer cases
support qualitative assessment when actually run. Link checks and synthetic traces
cannot establish general superiority over another skill.
