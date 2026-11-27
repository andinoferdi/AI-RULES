# Comparison trial: learning-workspace

Run on 2026-11-26 and 2026-11-27. One blind run per arm on the eight checkpoints in `fixture/`,
scored against the [rubric](rubric.md), which was frozen (with the fixture) before the candidate
was written. Evidence per score is in [scores.md](scores.md) (round 1),
[scores-rerun.md](scores-rerun.md) (round 2) and [scores-round3.md](scores-round3.md) (round 3).
The upgrade plan is [plan.md](plan.md).

## Setup

- Arms: no skill; Matt Pocock's `teach` (mattpocock/skills ad5400b, `skills/productivity/teach`
  with its four format files); the current `andino-learning-workspace` (AI-RULES main at
  1e78323); the candidate rewrite (branch `skill/learning-workspace-upgrade`).
- Runners: Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own run
  folder made by `setup_run.py`, with the rubric's run prompt. Web search and fetch were allowed
  for every arm. A first baseline wave was stopped by a usage limit before it finished and was
  discarded; the three baseline runs used here started from fresh folders.
- Between the baseline runs and the rewrite, a five-advisor council (Sonnet 5.5, medium; waves of
  three and two) with three anonymous reviewers (Haiku 5.5, low) chose the design. All five
  advisors picked the sibling-layout rewrite with format, lesson and pedagogy resources; all
  three reviewers ranked the Executor's answer first. The risk every advisor named was the agent
  creating files for quick requests; the verdict was to flip back to grafting the formats onto
  the old body if the candidate wrote files on t1, t2 or t7.
- Collection and blinding: `collect_run.py` produced each run's replies, user folders, diff,
  file list and transcript; `export_transcript.py` replaced run paths with `<RUN>` and removed
  guidance text. Each round shuffled the four runs to new letters with the mapping kept outside
  the grading folder. One grader per round (Sonnet 5.5, medium) saw only the rubric, the fixture
  and A to D. No transcript showed a Skill, slash command or subagent call.

## Scores

The three baseline arms were graded in every round from the same runs; the candidate was rerun
after each text fix.

| Round | Candidate text | No skill | teach | Current | Candidate | Criteria where the candidate was below teach or current |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | first draft | 62 | 62 | 60 | 71 | G3 (reply length: t1 asked to be short, t7 used two examples) |
| 2 | length limits for quick lessons and repairs | 61 | 60 | 61 | 70 | L2 (one source in `RESOURCES.md`), G1 (workspace labels in messages) |
| 3 | two-source minimum, plain words in messages | 62 | 60 | 60 | 71 | L14 (hand-over message 242 words with an extra caveat) |

Maximum 72. The final text adds a length limit to the hand-over (step 7) after round 3; that
change has not been run.

Gate (candidate at least equal to teach and to the current skill on every criterion): not met in
any single round. Each round the candidate dropped one point on a different criterion, and each
of those criteria scored 2 for the candidate in the other rounds: G3 in rounds 2 and 3, L2 and
G1 in rounds 1 and 3, L14 in rounds 1 and 2. Every miss was fixed in the text after the round
that showed it.

## Reading the result

- The candidate leads every round by 9 to 11 points. It is the only arm that wrote a reference
  sheet with the first lesson (L9: the other three arms scored 0 in every round), suggested a
  concrete community for the practitioner-judgment question (S2), and ended the quick lesson on
  a retrieval question every time (Q3).
- It kept the current skill's strengths: no file on the quick lesson, the factual question or the
  repair in any round; the dangerous `EXPLAIN ANALYZE` on `DELETE` belief corrected first with a
  safe alternative and a source; no pose sequence for the herniated disc.
- teach's arm researched widely and wrote strong lessons, but carried the community opt-out from
  the t4 learner into the t6 learner's workspace, wrote no record for the corrected
  misconception, and gave no retrieval question in the quick lesson.
- The current skill asked five questions at once instead of one why-question (M1), produced a
  quiz whose correct option was the longest (L6), and named no community (S2).
- With one run per arm, a one-point difference can be noise; the moving single-point misses
  across rounds look like that.
