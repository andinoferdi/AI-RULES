# Comparison trial: code simplification

Run on 2026-11-26. One blind run per arm on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen (commit fbdbfe3) before the candidate was written and
amended once (commit df74070) before the candidate was written. Evidence per score:
[scores.md](scores.md).

## Setup

- Arms: Addy Osmani's `code-simplification` (addyosmani/agent-skills, skill last changed in
  f1f6fbf); the current `andino-code-simplification` (AI-RULES main at 49ad00b); an unguided
  control with no skill; the candidate rewrite (branch `skill/code-simplification-upgrade`,
  skill folder exported from commit 4d89629, which became beabab0 when the branch was
  rebased onto main; the skill folder, fixture and rubric bytes are identical in both).
- Runners: four Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each with the
  rubric's run prompt, its own copy of the fixture and (skill arms) its own skill copy, told to
  read nothing else and to use no skills, slash commands or subagents. The three baseline arms
  ran first; the candidate ran after the rewrite.
- Oracle: `fixture/oracle/check.py` replays the original and the edited code over the same
  cases (targeted pricing families, 300 random orders, the tax table, the export job, the
  snippet's functions including a service that throws synchronously), diffs the run's
  repository against the fixture and compares the protected block.
- Blinding: the four outputs were copied to shuffled folders (A unguided, B candidate, C Addy,
  D current), checked for mentions of the guidance used (none found), and scored by one Sonnet
  5.5 subagent at medium effort that saw only the rubric, the fixture with its oracle and the
  four folders.
- Report channel: in the candidate run the host refused the subagent's writes of
  `out/task1/REPORT.md` and `out/task3/REPORT.md` ("Subagents should return findings as text,
  not write report files"); the baseline runs were not refused. The runner returned both
  reports as text and the chair copied them into the run folder unchanged, except that "as
  above" in the task 1 checks line was replaced by the SHA-256 the runner had stated just above
  its report.

## Scores

| Criterion | Unguided (A) | Addy (C) | Current (D) | Candidate (B) |
| --- | --- | --- | --- | --- |
| T10 dead weight and comments | 1 | 2 | 1 | 2 |
| T11 speculative abstraction | 1 | 2 | 1 | 2 |
| T13 characterization tests | 0 | 0 | 1 | 2 |
| J5 verification honesty | 1 | 1 | 2 | 2 |
| Q1 change report | 1 | 1 | 2 | 2 |
| Q2 honesty | 1 | 1 | 2 | 2 |
| Other 17 criteria | 2 each | 2 each | 2 each | 2 each |
| Task 1 (T1-T13, of 26) | 22 | 24 | 23 | 26 |
| Task 2 (J1-J5, of 10) | 9 | 9 | 10 | 10 |
| Task 3 (X1-X2, of 4) | 4 | 4 | 4 | 4 |
| Quality (Q1-Q3, of 6) | 4 | 4 | 6 | 6 |
| Total (of 46) | 39 | 41 | 43 | 46 |

Gate (candidate at least equal to Addy and to the current skill on every criterion): PASS. The
candidate scored 2 on all 23 criteria; it is higher than Addy on T13, J5, Q1 and Q2 and higher
than the current skill on T10, T11 and T13.

## Reading the result

- Behavior: every arm, the unguided control included, preserved behavior on every oracle case.
  On this fixture the model already keeps behavior without guidance; the skills differ in what
  they leave behind and in what they claim.
- The current skill's arm left unused imports and an unused one-strategy factory ("a named
  domain concept"). The candidate's evidence rule for removal fixed both (T10, T11).
- The Addy and unguided arms flattened around the protected block and then reported it as
  unchanged byte for byte, which was false. The candidate and the current skill kept the bytes
  and quoted matching hashes (Q2).
- Only the candidate added characterization tests to the repository (19 tests, run green on
  the old code first); the current skill's arm kept a differential script outside the
  repository (T13).
- An oracle gap the scores do not show: the Addy and unguided arms turned
  `include_tax == True` into `if include_tax`, which changes results for truthy non-boolean
  values such as `"yes"` or `2`. The oracle only passes booleans and `0`/`1`, so it did not
  catch this. The candidate kept the comparison, explained it in a comment and pinned it with
  characterization tests.

## Change after grading

The self-review after grading added `x == True` to the strict-versus-truthy trap in
`SKILL.md` ("Preserve behavior exactly"), next to `is True` and `=== true`, because that is the
change the Addy and unguided arms made without noticing. The candidate arm already kept that
comparison. This one-line addition was not re-run.

## Limitations

- One run per arm and one grading, so a one-point difference can be noise. The chair's earlier
  unblinded reading of the three baseline arms (about 42, 42 and 40) differs from the blind
  grade (41, 43, 39) by one to two points per arm.
- The same author wrote the fixture, the rubric and the candidate, and the candidate was
  written after reading the baseline outputs. The rubric was frozen first, but rules such as
  the characterization-test row and the removal evidence rule target exactly the gaps this
  fixture exposed, so the candidate may fit this fixture better than it generalizes.
- Runners and grader come from one model family.
- The rubric was amended once (T6 and T8 could not both score 2 in Python); the amendment was
  made after reading only the unguided control's output and before any candidate change.
- The rubric scores code, tests and reports in one Python repository and one JavaScript
  snippet. Hot-path and compliance gates were exercised only through the tax module.
