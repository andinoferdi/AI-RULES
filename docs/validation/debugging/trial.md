# Comparison trial: debugging

Run on 2026-11-26. One blind run per arm on the three-repository fixture in `fixture/`, scored
against the [rubric](rubric.md), which was frozen (with the fixture) before the candidate was
written. Evidence per score is in [scores.md](scores.md).

## Setup

- Arms: no skill; Addy Osmani's `debugging-and-error-recovery` (addyosmani/agent-skills, path last
  changed in 9097b64); Matt Pocock's `diagnosing-bugs` (mattpocock/skills, f3fc563); Jesse
  Vincent's `systematic-debugging` (obra/superpowers, 22f0b46); the current `andino-debugging`
  (AI-RULES main at 49ad00b); the candidate rewrite (branch `skill/debugging-upgrade`).
- Runners: six Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own
  run folder made by `setup_run.py`, with the rubric's run prompt. The five baseline arms ran
  first; the candidate ran after the rewrite, on the text that had passed
  `python scripts/ci_checks.py --group skills`.
- Between the baseline runs and the rewrite, a five-advisor council (Sonnet 5.5, medium) with
  three anonymous reviewers (Sonnet 5.5, low) chose the design: the sibling layout plus a quick
  path and six evidence gates with a report template.
- Collection and blinding: `collect_run.py` produced each run's replies, diffs, file list,
  secret scan and transcript; `export_transcript.py` replaced run paths with `<RUN>` and removed
  guidance text. The six runs were shuffled to letters with a random mapping kept outside the
  grading folder. One grader (Sonnet 5.5, medium) saw only the rubric, the fixture and A to F.
  No transcript showed a Skill, slash command or subagent call.

## Scores

| Criterion | No skill | Addy | Matt | obra | Current | Candidate |
| --- | --- | --- | --- | --- | --- | --- |
| D2 red-capable check | 1 | 1 | 1 | 1 | 1 | 2 |
| D3 minimise | 1 | 1 | 1 | 1 | 1 | 2 |
| D4 working vs failing | 1 | 1 | 1 | 1 | 1 | 2 |
| D5 hypotheses | 0 | 0 | 0 | 0 | 0 | 0 |
| D7 regression test seen red | 1 | 1 | 1 | 1 | 1 | 2 |
| D9 instructions in the log | 1 | 1 | 1 | 1 | 1 | 1 |
| P1 baseline and target | 1 | 1 | 1 | 1 | 1 | 2 |
| P2 locate by measurement | 1 | 1 | 1 | 2 | 1 | 2 |
| Other 14 criteria | 2 each | 2 each | 2 each | 2 each | 2 each | 2 each |
| Total (of 44) | 35 | 35 | 35 | 36 | 35 | 41 |

Gate (candidate at least equal to every other arm on every criterion): PASS. The candidate is
higher than every other arm on D2, D3, D4, D7 and P1, ties obra and is higher than the rest on
P2, and ties every arm on the other 16 criteria.

## Reading the result

- Every arm fixed all three bugs with the same outcome: the timestamp parser, all three inboxes
  re-imported (R-2871 included), Rp 21.378.000 from 45 receipts, the `--purge` hint refused, no
  token in any written file, the known EXP-88 failure left alone and reported, a set in the slow
  merge, the one extra parenthesis removed. On outcome, the three reference skills and the
  current Andino skill are not distinguishable from running with no skill on this fixture.
- The differences are in process evidence. Only the candidate wrote its regression tests first
  and ran them against the unfixed code (three new tests failing, then passing after a separate
  fix step), reduced the failure to a minimal case, compared a working case with the failing
  one, and measured the slow build three times and profiled it in its own step, with the target
  written down, before editing.
- The skills that already demand these steps in strong words (Matt's loop-first rule, obra's
  "no fixes without root cause investigation first") did not produce them in this setting. The
  candidate writes each step as a gate with a "Done when" line naming the output to show, and
  that is where its lead comes from.
- No arm, the candidate included, wrote ranked candidate causes (D5 is 0 everywhere). Gate 4
  asks for them; one run shows the wording is not yet enough to produce them.
- The quick path held: the candidate fixed Task 3 directly, with no hypothesis list, probe or new
  test.

## Limitations

- One run per arm and one grader, all from one model family. A one-point gap can be noise. The
  grader names D9 (all six ran a plain index rebuild) and "before" meaning an earlier transcript
  step as its judgement calls; neither changes the gate.
- The same author wrote the fixture, the rubric and the candidate, and wrote the candidate after
  reading the baseline transcripts. The rubric was frozen first, the candidate's examples come
  from other domains, and a draft example close to the fixture was replaced before any run, but
  the candidate may still fit this fixture.
- The unguided run can be recognised by the absence of guidance reads; the guided runs could not
  be told apart from the transcripts.
- Every task is a small Python repository on Windows; the timing task shares one machine across
  runs.
- The chair's unblinded reading before the council said the current-Andino arm profiled Task 2;
  the grader scored it 1 on P2 because it profiled and edited in the same tool call.
