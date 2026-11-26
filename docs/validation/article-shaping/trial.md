# Comparison trial: article shaping

Run on 2026-11-26. Scripted sessions on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen (commit fe04e62) before the candidate was written.

## Setup

- Arms: Matt Pocock's `writing-beats` and `writing-shape` together (mattpocock/skills commit
  6f7f783); the current `andino-article-shaping` (AI-RULES main at 49ad00b); the candidate
  rewrite on branch `skill/article-shaping-upgrade`, run twice: run 1 on skill snapshot
  `624cfec5ae23fd0a`, run 2 after the fixes below on snapshot `0426c33d586c530e` (sha256 over
  the sorted file hashes of the copied skill folder; run 2's snapshot equals the committed
  folder).
- Runners: Claude Code subagents, Sonnet 5.5 at medium effort, one per arm and run, each
  with the rubric's run prompt, its own skill copy and its own run folder, told to read
  nothing else and to use no skills, slash commands or subagents. The parent played the
  author strictly by the rubric's author policy and appended the scripted author line after
  the first block was written.
- Blinding: each grading round shuffled the runs to letters and checked them for guidance
  names and run paths (none left). Each grader, one Sonnet 5.5 subagent at medium effort,
  saw only the rubric, the fixture and the three lettered run folders.
- Records: `runs/matt/`, `runs/current/`, `runs/candidate/` (run 1),
  `runs/candidate-rerun/` (run 2); grader evidence in [scores.md](scores.md) (round 1) and
  [scores-rerun.md](scores-rerun.md) (round 2).

## Round 1 (candidate run 1)

Letters: A Matt, B candidate, C current. Totals of 40: Matt 34, candidate 35, current 28.
Gate (candidate at least equal to Matt and to the current skill on every criterion): FAIL on
S3 (candidate 1, both others 2), W2 (candidate 1, Matt 2) and D2 (candidate 1, current 2).

Three skill-text defects explained the misses: step 4 allowed openings that differ only in
entry point; step 5 wrote the approved block verbatim even after the author's added line
made part of it repeat; step 7 asked for a format argument only "when more than prose is
plausible", where Matt argues the form of every block. The fixes: one named thesis per
opening, stop and rework a block that would repeat or contradict new author text, form and
reason per candidate, and no unreachable candidates (a grounding remedy instead).

Two current-arm records and one Matt snapshot turned into NUL bytes when first copied into
`docs/` (cause unknown; the scratchpad originals were intact and were recopied). The round 1
grader saw those three files as unreadable; the criteria they bear on (W1, E3, and A's
"no article yet" snapshot) were already at the maximum, so the round 1 gate did not depend
on them. Round 2 graded intact copies.

## Round 2 (candidate run 2, all three re-graded)

Letters: A current, B candidate, C Matt.

| Criterion | Matt | Current | Candidate |
| --- | --- | --- | --- |
| S1 reader first | 2 | 0 | 2 |
| S5 paths shown | 1 | 1 | 2 |
| W2 author edit kept | 2 | 0 | 2 |
| W3 next candidates | 1 | 1 | 2 |
| W5 block size | 1 | 2 | 2 |
| E1 no invention | 1 | 1 | 2 |
| D2 format choice | 1 | 1 | 1 |
| P1 natural Indonesian | 1 | 1 | 1 |
| P2 rhythm | 1 | 1 | 2 |
| P3 messages to the author | 1 | 0 | 2 |
| Other 10 criteria | 2 each | 2 each | 2 each |
| Total (of 40) | 32 | 28 | 38 |

Gate: PASS. The candidate is at least equal to Matt and to the current skill on all 20
criteria, and higher than Matt on S5, W3, W5, E1, P2 and P3.

## Limits

- One run per arm and round; a one-point difference can be noise. The two rounds graded
  Matt 34 then 32 and the current skill 28 then 28 on the same records, which shows the
  grader's own spread.
- In run 2 the candidate's first final message was a report about its work instead of a
  reply to the author. The parent sent one harness message (not an author message) asking
  for the reply as the author would read it, and graded the resent reply; the transcript
  records the note.
- D2 stayed at 1 for every arm: the candidate argued no block's form with a reason, although
  step 7 now asks for it. The rule is in the skill; compliance with it is not shown.
- Section pacing (Mode B) and raw-capture were not exercised. The author was simulated by a
  fixed policy; no real author was observed.
