# Comparison trial: code review

Run on 2026-11-26. One blind run per arm on the fixture built by
[build_review_fixture.py](build_review_fixture.py), scored against the [rubric](rubric.md),
which was frozen (commit 2444a35) before the candidate was written.

## Setup

- Arms:
  - Control: no skill.
  - Current: `andino-code-review` at AI-RULES main 49ad00b.
  - Addy: `addyosmani/agent-skills:skills/code-review-and-quality` at e997ac5, with its
    `references/shared/` checklists.
  - Matt: `mattpocock/skills:skills/engineering/code-review` at 6f7f783.
  - obra: `obra/superpowers:skills/requesting-code-review` (SKILL.md and code-reviewer.md)
    and `skills/receiving-code-review` at 22f0b46.
  - Candidate: this branch's skill folder, content hash a6d43445 (the files as committed).
- Tasks: review the `feature/partial-refunds` branch; act as the author on six reviewer
  comments; write the request for an independent reviewer. The fixture plants ten defects,
  five precision traps, an unrelated uncommitted draft and untracked secret and customer
  files.
- Runners: six Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each on a
  fresh fixture copy with its own skill copy and the rubric's run prompt, told to read
  nothing else and to use no skills, slash commands or subagents. The five baseline arms ran
  before the council and the rewrite; the candidate ran after it. Matt's and obra's skills
  ask for reviewer subagents; those arms worked inline.
- Blinding: outputs were copied to folders A-F, absolute paths naming an arm were replaced
  with `<RUN_DIR>`, and the outputs were searched for guidance names (none left). Each arm's
  repository state was captured after its run. The grader, one Sonnet 5.5 subagent at medium
  effort, saw only the rubric, the builder, the six folders and the state captures. Its
  evidence per score is in [scores.md](scores.md).

## Scores

| Criterion | Control | Current | Addy | Matt | obra | Candidate |
| --- | --- | --- | --- | --- | --- | --- |
| T10 unspecified harm (double submit) | 0 | 0 | 0 | 0 | 0 | 2 |
| S2 repository left as found | 2 | 2 | 2 | 2 | 0 | 2 |
| S3 evidence from the reviewed bytes | 1 | 1 | 2 | 1 | 1 | 2 |
| S7 honest verification split | 2 | 2 | 2 | 1 | 2 | 2 |
| F8 reply quality | 1 | 2 | 1 | 2 | 2 | 2 |
| Q1 pinned change with patch bytes | 1 | 1 | 1 | 1 | 1 | 2 |
| Q2 sensitive files kept out | 1 | 2 | 2 | 2 | 2 | 2 |
| Q4 verification split in the request | 2 | 2 | 2 | 1 | 1 | 2 |
| Q5 reviewer instructions | 1 | 2 | 2 | 2 | 2 | 2 |
| Other 29 criteria | 2 each | 2 each | 2 each | 2 each | 2 each | 2 each |
| Task 1 findings T1-T10 (20) | 18 | 18 | 18 | 18 | 18 | 20 |
| Task 1 precision P1-P5 (10) | 10 | 10 | 10 | 10 | 10 | 10 |
| Task 1 process S1-S8 (16) | 15 | 15 | 16 | 14 | 13 | 16 |
| Task 2 F1-F9 (18) | 17 | 18 | 17 | 18 | 18 | 18 |
| Task 3 Q1-Q6 (12) | 9 | 11 | 11 | 10 | 10 | 12 |
| Total (of 76) | 69 | 72 | 72 | 70 | 69 | 76 |

Gate (candidate at least equal to every other arm on every criterion): PASS. The candidate
scored 2 on all 38 criteria.

## Reading the result

- Every arm, including the one with no skill, found the seven main planted defects and
  avoided all five precision traps. On this fixture the skills differ in method, not in
  defect finding.
- The candidate was the only arm to report that a retried or double-submitted refund creates
  a second refund (T10). It found it with the Spec pass's state-changing-path questions and
  confirmed it with a probe (refund ids 1 and 2 for the same body).
- The candidate and Addy were the only arms to test on a clean `git archive` export of the
  reviewed head and to show surviving mutants. The current skill ran tests on the dirty
  checkout without saying so.
- The obra arm switched the review repository to `main` and left it there; the candidate
  recorded its starting state and compared the end state.
- The candidate was the only arm whose review request carried the exact patch; the current
  skill's arm sent a partial diff with elisions.
- Compared with the current skill, the candidate gained on T10, S3 and Q1 (72 to 76) and
  lost no criterion.

## Limitations

- One run per arm and one grading. The grader flagged close calls on S6, F8, F9, T8 and T9
  for other arms; none of them changes the gate, because the candidate scored 2 everywhere.
- The same author wrote the fixture, the rubric and the candidate. The rubric was frozen
  first and the skill's rules are generic (no fixture domain in them), but the candidate may
  still fit this fixture. No second fixture was run.
- Runners and grader come from one model family.
- The candidate ran after a council read the baseline outputs, so it benefits from knowing
  where the baseline arms fell short.
- The rubric scores written reviews, replies and repository states. It does not measure
  long-run review quality on real pull requests.
