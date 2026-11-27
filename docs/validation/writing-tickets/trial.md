# Comparison trial: writing tickets

Run on 2026-11-27. One run per arm on the fixture built by
[build_tickets_fixture.py](build_tickets_fixture.py), scored against the [rubric](rubric.md),
which was frozen (commit 195541c) before the candidate skill text was written.

## Setup

- Arms:
  - None: no guidance, the runner's own judgement.
  - Matt: `mattpocock/skills:skills/engineering/to-tickets/SKILL.md` at 9e2abf8, with the
    repository's tracker document standing in for its setup skill.
  - Candidate: `skills/andino-workflow/skills/writing-tickets/` at commit c837768 (SKILL.md,
    resources, references and scripts; GUIDE.md is a mirror and was left out).
- Tasks: four requests on one fixture repository (a room-booking command-line tool): S1 tickets
  from a spec and a chat that holds an exclusion, an expiry rule, an undecided question with a
  named owner and a duplicated check; S2 a wide rename that reaches stored data and exported
  output; S3 an existing ticket folder whose spec gained two items; S4 a horizontal,
  path-heavy implementation plan with an open blocked item.
- Runners: three Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each on a
  fresh fixture copy with its own guidance copy and the rubric's run prompt, told to read
  nothing else and to use no skills, slash commands, subagents, network or `gh`. The None and
  Matt arms ran before the candidate text existed; the candidate ran after.
- Collection: [collect_run.py](collect_run.py) copied `out/`, `.scratch/` and the repository
  state and replaced run paths and guidance names.

## Rulings made during the trial

- The host's Write tool refused `out/report.md` for the Matt and Candidate runners (the None
  runner's write went through). Both runners returned the report text in their final message;
  it was saved verbatim as `out/report.md` in the grading folder. The Candidate runner's first
  final message said the file was written; asked again, it said the write was refused and gave
  the text. Cost if wrong: F1 for those two arms rests on message text, not on a file the
  runner wrote.
- The Matt runner wrote its proposal files to `roomy/out/` instead of `<RUN_DIR>/out/`. They
  were copied into the grading folder for Q1 and the misplacement is scored under S0.
- The run prompt says the export spec changed "in the last commit"; it changed in the commit
  before. All three runners found the right commit and said so. The wording is kept frozen.

## Scores

Full evidence per score is in [scores.md](scores.md).

| Criterion | None | Matt | Candidate |
| --- | --- | --- | --- |
| V4 open decision held for its owner | 1 | 2 | 2 |
| A1 checkable acceptance criteria | 1 | 1 | 2 |
| D1 no paths or line numbers | 0 | 2 | 2 |
| T1 tracker conventions | 1 | 2 | 2 |
| W1 expand-contract | 0 | 2 | 2 |
| W3 batches by area | 0 | 2 | 2 |
| P1 plan recut into slices | 0 | 2 | 2 |
| P2 plan's open item carried | 2 | 1 | 2 |
| S0 nothing outside the tracker | 2 | 1 | 2 |
| Other 10 criteria | 2 each | 2 each | 2 each |
| Total (of 38) | 27 | 35 | 38 |

Gate (candidate at least equal to every other arm on every criterion): PASS. The candidate is
higher than Matt's skill on A1, P2 and S0, higher than no guidance on seven criteria, and ties
both on the other ten.

## Reading the result

- Both guided arms kept tickets durable and recut the plan into slices; without guidance the
  runner copied paths, line numbers and the plan's horizontal tasks into tickets.
- The candidate's clearest gains over Matt's skill are where its additions aim: every open
  decision became a `human-ready` ticket with an owner that blocks nothing it should not (Matt's
  arm left two of three decisions only as sentences), and every criterion names a command or
  stored state with its expected value.
- Matt's skill already handled the rerun, expand-contract and prefactor cases well; the
  candidate kept those behaviours.

## Limits

- One run per arm on one fixture; model variance is not measured.
- The grader wrote the candidate and knew the mapping. The scores cite their evidence so an
  independent grader can redo them from the collected folders.
- The S0 and F1 effects of the host's file-write refusals are recorded above, not removed.
- Discovery probes (rubric): NOT RUN. Prompts to run on a fresh session with the member
  installed: "Break this approved spec into tracker tickets an agent can pick up." (must load
  `andino-writing-tickets`) and "Write the implementation plan for this spec so I can build it
  in this session." (must load `andino-planning`, not this member). The routing evals in
  `evals/andino-method-routing.json` carry the same two prompts.
- Remote publishing to GitHub was not exercised; the endpoints it names were checked to exist
  with read-only requests (`issues/<n>/sub_issues`, `issues/<n>/dependencies/blocked_by`).
