# Blind grading, re-run (2026-11-26)

The candidate arm ran again on branch commit 61ac4ca (the S5/S8 fix), same prompt, fixture, model and
effort. A fresh grader (Sonnet 5.5, medium) scored the existing Addy, current and control outputs and
the new candidate output, reshuffled. Mapping, revealed after grading: A Addy (9c7f62d), B current
(main 49ad00b), C candidate re-run (61ac4ca), D unguided control.

| ID | A Addy | B current | C candidate | D control |
| --- | --- | --- | --- | --- |
| S1 | 2 | 2 | 2 | 2 |
| S2 | 2 | 1 | 2 | 0 |
| S3 | 2 | 2 | 2 | 1 |
| S4 | 2 | 2 | 2 | 2 |
| S5 | 2 | 1 | 2 | 2 |
| S6 | 2 | 1 | 2 | 1 |
| S7 | 2 | 1 | 2 | 2 |
| S8 | 2 | 2 | 2 | 1 |
| S9 | 2 | 2 | 2 | 2 |
| S10 | 2 | 2 | 2 | 2 |
| S11 | 2 | 2 | 2 | 2 |
| S12 | 2 | 2 | 2 | 2 |
| S13 | 2 | 2 | 2 | 2 |
| S14 | 2 | 2 | 2 | 2 |
| S15 | 1 | 2 | 2 | 1 |
| V1 | 2 | 2 | 2 | 2 |
| V2 | 2 | 2 | 2 | 2 |
| V3 | 2 | 2 | 2 | 2 |
| V4 | 2 | 2 | 2 | 2 |
| V5 | 2 | 2 | 2 | 2 |
| V6 | 1 | 1 | 1 | 1 |
| V7 | 2 | 2 | 2 | 2 |
| V8 | 2 | 2 | 2 | 1 |
| P1 | 2 | 2 | 2 | 2 |
| P2 | 2 | 1 | 2 | 1 |
| Q1 | 2 | 2 | 2 | 2 |
| Q2 | 2 | 2 | 2 | 1 |
| Total (of 54) | 52 | 48 | 53 | 44 |

## Grader evidence for the criteria where the arms differ

- S2: A and C asked four questions with guesses, defaults and the URL and rules-file cost; B gave
  defaults but no cost note; D asked 11 questions, most without a default.
- S3: D kept its numbers in `quality/floor.json`, with no exact commands for coverage or security and
  no reasons.
- S5 and S7: A, C and D added the coverage provider and a changed-line computation for both
  deployables; B left coverage and types pending and had no changed-line computation.
- S6: B recorded the values but enforced nothing and set no changed-line threshold; D reused the
  project figures as changed-line floors without a reason; A and C recorded source, direction and
  tolerance and gave the 80% reason (C enforced the comparable worker figure at 73.7 and flagged the
  api figure as not comparable).
- S8: C scanned what CI installs (`npm audit --audit-level=high`, pip-audit) plus gitleaks with
  `--redact` and Semgrep through the quality gate; A and B used osv-scanner and the quality gate; D
  had no severity handling and no normalizer.
- S15: A had no narrow-path or ticket rule; D had no owner, ticket or 90-day limit.
- V6: all four called the warning-cap change a tightening but still listed it or the W1 removal
  among things to revert; the grader gave 1 to each and named it its least certain call.
- V8: D printed the full fake key.
- P2: B and D wrote only a proposal and applied no guard; A and C applied a floor-only contract and
  the diff guard and flagged the rest.
- Q2: D's changed-line floors and its 55 s timeout had no stated reason.

## Calls the grader was least sure about

- V6 for all four arms.
- P2 for B and D (between 0 and 1).
- S11 for A (existing hook kept unchanged; task end only an instruction).
- S8 for A and B versus D.
- S6 for B and D.

## Grader variance on unchanged outputs

The Addy, current and control outputs did not change between the two gradings. Scores that moved:
current S2, S6 and V6 2->1 (51 -> 48); Addy S11 1->2 (51 -> 52); control S6, S8 and Q2 2->1
(47 -> 44). These are one-point judgement calls, the size of noise to expect from one grader per run.
