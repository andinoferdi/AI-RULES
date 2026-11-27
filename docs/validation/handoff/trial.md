# Comparison trial: handoff

Run on 2026-11-26. One blind run per arm on the fixture in `fixture/`, scored against the
[rubric](rubric.md), which was frozen (with the fixture) before the candidate was written.
Evidence per score is in [scores.md](scores.md); the rewrite's coverage of the old rules is in
[preservation.md](preservation.md).

## Setup

- Arms: no skill; Matt Pocock's `handoff` (mattpocock/skills, path last changed in 0f5e033)
  with the phase-boundary section of `ask-matt` and its `PHASE-BOUNDARIES.md` (954ee7f)
  appended, because Matt's handoff relies on that page to decide when to hand off; Addy
  Osmani's `context-engineering` (addyosmani/agent-skills, 583df9a); the current
  `andino-handoff` (AI-RULES main at 1e78323); the candidate rewrite (branch
  `claude/handoff-skill-quality-99e0da`).
- Runners: Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own
  run folder made by `setup_run.py`, with the rubric's run prompt. The four baseline arms ran
  first. Three of them stopped midway on an account usage limit and were resumed from where
  they stopped with the user's approval; their transcripts are continuous.
- Between the baseline runs and the rewrite, a five-advisor council (Sonnet 5.5, medium) with
  three anonymous reviewers (Sonnet 5.5, low) chose the design: all five advisors picked the
  full rewrite in the sibling layout with one plain context-packing guide, and all three
  reviewers ranked the same response first. Their blind spots were adopted: explicit cues for
  the compact and subagent boundaries, a concrete mechanism for work that exists only on the
  sender's machine, and a rerun on the fixture before calling it done.
- Collection and blinding: `collect_run.py` produced each run's replies, written files, diffs
  against the starting working tree, git state, secret scan and transcript (exported with
  `../debugging/export_transcript.py`, which replaces run paths with `<RUN>` and removes
  guidance text). The runs were shuffled to letters with a mapping kept outside the grading
  folder. One grader (Sonnet 5.5, medium) saw only the rubric, the fixture and A to E. No
  transcript showed a Skill, slash command or subagent call. The no-skill arm's transcript
  shows that its guide folder was missing; the grader was told not to favour or penalise that.

## Scores

| Criterion | No skill | Addy | Matt | Current | Candidate |
| --- | --- | --- | --- | --- | --- |
| H1 repository state | 1 | 1 | 2 | 2 | 2 |
| H4 decisions with reasons | 2 | 2 | 1 | 2 | 2 |
| H8 suggested skills | 0 | 0 | 2 | 0 | 1 |
| H10 instruction inside the issue | 2 | 2 | 2 | 1 | 2 |
| H12 checked from the recipient's side | 0 | 0 | 0 | 0 | 0 |
| B1 continue after the interview | 1 | 2 | 2 | 2 | 2 |
| B3 subagent for the unattended review | 2 | 1 | 2 | 2 | 2 |
| B4 handoff for the side task | 1 | 1 | 2 | 1 | 2 |
| B5 compact at 170k tokens | 1 | 1 | 2 | 1 | 2 |
| Q1 reply content | 2 | 2 | 1 | 2 | 2 |
| Q2 honesty and register | 2 | 2 | 2 | 1 | 2 |
| Other 15 criteria | 2 each | 2 each | 2 each | 2 each | 2 each |
| Total (of 52) | 44 | 44 | 48 | 44 | 49 |

## Reading

- Every arm wrote and received handoffs well: repository state, the push the fresh clone
  needs, decisions, the open question, the secret, drift on receipt, test-first jitter and the
  checkpoint all scored 2 almost everywhere. The difference was in the boundary decision and
  the extras Matt asks for.
- The current skill lost on the side-task and compact boundaries (B4, B5), suggested skills
  (H8), flagging the injected issue comment (H10) and one overclaim (Q2).
- The candidate matched or beat every arm except Matt on H8: it named one skill without "if
  installed". No arm, the candidate included, checked its handoff from the recipient's side
  (H12), although the candidate's step 6 asks for it: the runner went from writing the file
  to writing the reply.
- With one run per arm a one-point difference can be noise.

## Gate

The candidate must score at least every other arm on every criterion. First round: not met
on H8 (1 against Matt's 2); H12 is 0 for all arms.

## Rerun

Both misses were omissions, so the fix was a structural slot rather than a new rule: the
template's "Before you start" gained a "Checked from your side" line that must hold a command
run after writing and its result, step 6 says to run it after writing and before replying,
and "Suggested skills" became one line per step with "if installed". The revised candidate ran
once more (Sonnet 5.5, medium) on a fresh run folder; the four baseline runs were reused
unchanged. All five were reshuffled to new letters and scored by a fresh blind grader
(Sonnet 5.5, medium). Evidence is in [scores-rerun.md](scores-rerun.md).

| Criterion | No skill | Addy | Matt | Current | Candidate |
| --- | --- | --- | --- | --- | --- |
| H1 repository state | 1 | 1 | 2 | 2 | 2 |
| H2 work only on the sender's machine | 2 | 2 | 1 | 2 | 2 |
| H4 decisions with reasons | 2 | 2 | 1 | 2 | 2 |
| H8 suggested skills | 0 | 0 | 2 | 0 | 2 |
| H10 instruction inside the issue | 2 | 2 | 2 | 1 | 2 |
| H12 checked from the recipient's side | 0 | 0 | 0 | 0 | 2 |
| B1 continue after the interview | 1 | 2 | 2 | 2 | 2 |
| B3 subagent for the unattended review | 1 | 0 | 2 | 2 | 2 |
| B4 handoff for the side task | 1 | 1 | 2 | 1 | 2 |
| B5 compact at 170k tokens | 1 | 1 | 2 | 1 | 2 |
| Q2 honesty and register | 2 | 2 | 2 | 1 | 2 |
| Other 15 criteria | 2 each | 2 each | 2 each | 2 each | 2 each |
| Total (of 52) | 43 | 43 | 48 | 44 | 52 |

The revised candidate wrote a git bundle of the branch, a patch of the tracked changes and
copies of the untracked files beside the handoff, cloned the bundle, applied the patch and
reran the suite to the recorded counts before replying. It meets the gate: at least every
other arm on all 26 criteria.

Limits: one run per arm and one grader per round. The two graders differed by one point on
three baseline cells (Matt H2, Addy B3, no-skill B3), which is the size of the noise; the
candidate's lead on H12 and on the boundary criteria B4 and B5 over the current skill is
larger than that. Model behaviour on other hosts and models is not verified. After the rerun
one example in the Rules section changed from a fixture name ("reported by Andi") to a
placeholder ("reported by <who>"); no instruction changed, and it was not re-run.
