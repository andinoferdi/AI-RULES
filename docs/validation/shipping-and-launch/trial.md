# Comparison trial: shipping and launch

Run on 2026-11-26 and 2026-11-27. One blind run per arm on the three-repository fixture in
`fixture/`, scored against the [rubric](rubric.md), which was frozen with the fixture (460529b)
before the candidate was written. Evidence per score is in [scores.md](scores.md).

## Setup

- Arms: Addy Osmani's `shipping-and-launch` with its four shared checklists
  (addyosmani/agent-skills, path last changed in 3d78ead); the current
  `andino-shipping-and-launch` (AI-RULES main at 1e78323); the candidate rewrite (branch commit
  8d6b111).
- Runners: three Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its
  own run folder made by `setup_run.py`, with the rubric's run prompt and told to use no skills,
  slash commands or subagents. The two baseline arms ran first; the candidate ran after the
  rewrite, on text that had passed `python scripts/ci_checks.py --group skills`.
- Between the baselines and the rewrite, a five-advisor council (Sonnet 5.5, medium) with three
  anonymous reviewers (Sonnet 5.5, low) chose the design. The council brief summarised the rubric
  and the chair's reading of both baseline replies, so the candidate was designed knowing the
  criteria; this is a limit of the trial, as in the earlier trials. The council chose a
  sibling-layout rewrite with one procedure, the minimum fields of the stage table, rollback plan,
  monitoring and flag lifecycle written into `SKILL.md` rather than only in resources, a sizing
  step for small changes, and a rule for fixing blockers locally.
- Fixture overlap was checked: example numbers in the candidate that matched the fixture (26 of
  1,920, 6.8x) and a worked case that resembled task 3 were replaced before the run.
- Collection: `collect_run.py` produced replies, diffs (side branches included, line endings
  normalised after a checkout rewrote them), action markers, a secret scan and the transcript.
  The collector was fixed for those two cases after the baselines ran (8808f8b); the rubric did
  not change. Run folders were shuffled to A to C with a mapping kept outside the grading folder,
  and dates were replaced with `<DATE>` because the candidate's flag audit log carried a later
  date. One grader (Sonnet 5.5, medium) saw only the rubric, the fixture and A to C.

## First candidate run

| Arm | Total (of 46) |
| --- | --- |
| Addy | 38 |
| Current | 38 |
| Candidate | 44 |

The candidate scored higher than both baselines on L4, L9, L10 and L13, higher than the current
skill on L3 and K5 and higher than Addy's on K4. It scored lower than the current skill on Q2:
its reply stated the default error-budget bands ("below 20%, only slow rollouts") as if the
repository had that policy, while marking its other defaults as defaults. All three arms scored
1 on L11: none named saturation or database signals. The candidate also left out the flag's
owner and removal date that its own record template asks for.

**Gate: not passed** (the candidate is below the current skill on Q2). With one run per arm a
one-point difference can be noise; this one has a clear cause in the reply.

## Change after the first run

The defaults section now requires every number in the reply to name its source (a project file,
or "default"), the budget bands included; the record template gained a `Policy used` line, a
monitoring line that lists error rate by endpoint, p95, saturation and database, client errors
and the user outcome, and a flag line with a named owner and removal date; step 8 is done only
when every template line is present; the verification checklist checks all three (commit
7eb6684).

## Candidate rerun

With the user's approval, one new runner (Sonnet 5.5, medium) ran the revised candidate on a
fresh copy of the fixture with the same prompt. The two baseline runs were reused unchanged. The
three runs were shuffled again and graded by a new grader (Sonnet 5.5, medium) with the same
material. Evidence is in [scores-rerun.md](scores-rerun.md).

| Arm | Total (of 46) |
| --- | --- |
| Addy | 39 |
| Current | 40 |
| Candidate | 46 |

**Gate: passed.** The candidate scored at least every other arm on all 23 criteria, and higher
than both on L9 (stage contract), L10 (rollback plan), L11 (monitoring and first hour) and L13
(flag lifecycle); higher than the current skill on L3 and higher than Addy's on K4 and Q2. On
Q2 it wrote that the 20% budget line is a default, not the team's policy.

## Limits

- One run per arm, and one grader per grading round. The baselines' totals moved by one or two
  points between the two graders (Addy 38 then 39, current 38 then 40), which is the size of
  the noise; the candidate's lead (six or seven points) sits mostly in L9 to L13.
- The candidate was designed with knowledge of the rubric, and its first run informed the
  revision that the rerun tested. The rerun is a second sample of the revised text, not of the
  first one.
- Sonnet 5.5 at medium effort on Claude Code only; other hosts and models are NOT VERIFIED.
- No arm tested the flag's off state explicitly in task 1, said the 212 rows must be reconciled
  before a later down-migration, or named a person as owner of the canary fix; the rubric gave
  credit for the weaker forms.
