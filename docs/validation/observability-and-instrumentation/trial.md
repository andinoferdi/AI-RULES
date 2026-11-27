# Comparison trial: observability and instrumentation

Run on 2026-11-26 and 2026-11-27. One blind run per arm on the fixture in `fixture/`, scored
against the [rubric](rubric.md), which was frozen with the fixture (commit 9b2c58d) before the
candidate was written. Grader evidence: [scores.md](scores.md) (first candidate) and
[scores-rerun.md](scores-rerun.md) (revised candidate).

## Setup

- Arms: no skill; Addy Osmani's `observability-and-instrumentation` with its
  `references/shared/observability-checklist.md` (addyosmani/agent-skills, path last changed in
  c4efec8); the current `andino-observability-and-instrumentation` (AI-RULES main at 1e78323);
  the candidate rewrite, in two versions.
- Runners: Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own run
  folder made by `setup_run.py`, with the rubric's run prompt. The three baseline arms ran first.
- Between the baselines and the rewrite, a five-advisor council (Sonnet 5.5, medium) with three
  anonymous reviewers (Sonnet 5.5, low) chose the design: the sibling layout with Done when gates
  (three advisors and all three reviewers' top picks), resources split by content rather than by
  mode, and the ticket-until-approved alert rule kept as an Andino strength.
- Collection and blinding: `collect_run.py` produced each run's replies, diff, file list, secret
  scan, telemetry files and transcript; `export_transcript.py` replaced run paths with `<RUN>` and
  removed guidance text. Runs were shuffled to letters with the mapping kept outside the grading
  folder; guidance file names and the local OS user name were redacted in the grading copies. No
  transcript showed a Skill, slash command or subagent call.
- Round 1 graded control, Addy, current and the first candidate. The candidate was then revised
  (audit path: list unseparable origins as open and name the field that would separate them; gate
  1: a separate `On-call questions:` message in a fixed shape before any edit), run once more, and
  a fresh grader scored control, Addy, current and the revised candidate, reshuffled.

## Scores

| Criterion | Control | Addy | Current | Candidate v1 | Candidate v2 |
| --- | --- | --- | --- | --- | --- |
| Round | 1 / 2 | 1 / 2 | 1 / 2 | 1 | 2 |
| A2 attribution | 2 / 2 | 2 / 2 | 2 / 2 | 1 | 2 |
| O1 questions first | 0 / 0 | 1 / 1 | 0 / 0 | 1 | 1 |
| O2 structured events | 1 / 1 | 2 / 2 | 2 / 2 | 2 | 1 |
| O3 entry point and correlation | 1 / 1 | 2 / 2 | 2 / 2 | 2 | 2 |
| O6 trace propagation | 1 / 1 | 2 / 2 | 2 / 2 | 2 | 2 |
| O10 telemetry exercised | 1 / 1 | 1 / 1 | 1 / 1 | 2 | 2 |
| O12 scope | 1 / 2 | 2 / 2 | 2 / 2 | 2 | 2 |
| Q2 honesty | 2 / 2 | 2 / 2 | 2 / 2 | 2 | 1 |
| Other 9 criteria | 2 each | 2 each | 2 each | 2 each | 2 each |
| Total (of 34) | 27 / 28 | 32 / 32 | 31 / 31 | 32 | 31 |

Gate (candidate at least equal to every other arm on every criterion): FAIL in both rounds. Round 1
failed on A2 (the candidate leaned to one origin by elimination). Round 2 fixed A2 and failed on O2
(one prose `print` left in the worker) and Q2 (the reply said the questions were written before
any change; the transcript shows them after the first edit).

## Reading the result

- On outcome every arm, the control included, answered the incident questions correctly, wrote no
  credential to any file, left `deploy/prod.env` alone and flagged the injected log instruction.
  The strong model already does most of this task without a skill; the arms differ in process
  evidence and in a few design slips.
- Both candidate runs were the only ones that inspected their own telemetry end to end, including
  one trace from enqueue to the provider call, in the run itself (O10 2 against 1 everywhere else).
- No arm, either candidate included, wrote on-call questions before its first source edit (O1 at
  most 1). Both Addy's skill and the current Andino skill make that step one, and the candidate's
  gate asks for a separate message before any edit; the runners still read, then edited in large
  batched commands, and wrote the questions afterwards. This mirrors the debugging trial, where
  ranked hypotheses before the fix stayed at 0 in every arm.
- Both candidate runs wrote in their reply that the questions came first: v1 in a draft it then
  corrected, v2 in the final reply. The Output template said "written before the first edit", and
  the runners filled the template instead of reporting what they did. The shipped text replaces that field with "sent: before the first edit | after
  editing, as the transcript shows" and adds a rule to report the actual order. No run exercised
  this last change: its effect is NOT VERIFIED.
- With one run per arm and different graders between rounds, a one-point difference is within
  noise: Addy scored 32 twice, the candidate 32 and 31, the current skill 31 twice, the control 27
  and 28. The evidence supports "about equal to Addy, at or above the current skill", not "better
  than Addy on every criterion".

## Limits

- One run per arm per round, one model family, one fixture (Python, standard library only); the
  skill's examples are TypeScript.
- Graders are Sonnet 5.5 subagents; the two rounds used different graders and their readings of the
  same baseline runs differ by up to one point per criterion.
- Model activation and routing were not tested; runners were told to read the guide.
