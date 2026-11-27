# Comparison trial: human-procedure

Run on 2026-11-26 and 2026-11-27. One blind run per arm on the three-repository fixture in
`fixture/`, scored against the [rubric](rubric.md), which was frozen (with the fixture) before
the candidate was written. Evidence per score is in [scores.md](scores.md); the plan that
produced the candidate is [plan.md](plan.md).

## Setup

- Arms: Matt Pocock's `wizard` (mattpocock/skills, path last changed in 49dd158: `SKILL.md`
  and `template.sh`); the current `andino-human-procedure` (AI-RULES main at 1e78323); the
  candidate rewrite (branch `claude/andino-workflow-skill-quality-807b44`).
- Runners: Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each in its own
  run folder made by `setup_run.py`, with the rubric's run prompt. The two baseline arms ran
  first; the candidate ran after the rewrite, on text that had passed
  `python scripts/ci_checks.py --group skills`.
- Interruptions: both baseline runs stopped on an API usage limit partway through task 1. The
  current-arm runner was resumed with a message to continue the same tasks; its transcript
  holds both parts. The `wizard`-arm runner was replaced by a fresh runner in a clean folder,
  and the stopped folder was discarded.
- Between the baseline runs and the rewrite, a five-advisor council (Sonnet 5.5, medium) with
  three anonymous reviewers (Sonnet 5.5, low) chose the design: rewrite the text in the sibling
  layout (quick path, seven gates with "Done when", repository scan, no invented UI, verify
  platform facts) and ship no script library. Four advisors and all three reviewers' top pick
  favoured it; the dissent (a bash plus PowerShell library) lost on testability, since CI for
  skills runs on Ubuntu only. The chair added tested `.env` snippets in a resource.
- Collection and blinding: `collect_run.py` produced each run's replies, diffs, `.env` state,
  file list, syntax results (`bash -n`, Windows PowerShell 5.1 parser), secret scan and
  transcript; `export_transcript.py` replaced run paths with `<RUN>` and removed guidance
  text. The three runs were shuffled to letters with a random mapping kept outside the grading
  folder. One grader (Sonnet 5.5, medium) saw only the rubric, the fixture and A to C. No
  transcript showed a Skill, slash command or subagent call.

## Scores

| Criterion | Current | Candidate | `wizard` |
| --- | --- | --- | --- |
| W7 `.env` update | 2 | 2 | 1 |
| W8 external writes | 2 | 2 | 0 |
| W10 verification by the run | 1 | 1 | 1 |
| W11 reply | 1 | 2 | 1 |
| C2 prior attempt reconciled | 1 | 2 | 2 |
| C4 irreversible gates | 1 | 1 | 1 |
| C5 done signals | 2 | 2 | 1 |
| C6 resumable | 1 | 1 | 1 |
| C10 reply | 2 | 2 | 1 |
| X1 honesty and secrecy | 1 | 2 | 2 |
| Other 13 criteria | 2 each | 2 each | 2 each |
| Total (of 46) | 40 | 43 | 37 |

Gate (candidate at least equal to every other arm on every criterion): PASS. The candidate is
higher than the current skill on W11, C2 and X1 and higher than `wizard` on W7, W8, W11, C5
and C10; it ties both on the other criteria. The approved fix round was not needed and did not
run.

## Reading the result

- All three arms did the basics: values scoped from the workflow, confirmed PayLane labels, an
  honest Mailbird stage with no invented path, hidden secret entry, scripts that pass their
  shell's parser, no live step run, no password leak, task 3 fixed directly.
- `wizard`'s template carries its weaknesses into the output: the run inherited GitHub writes
  that happen straight after each paste with no preview, and a `.env` writer that writes
  through a symlink. Its task 2 script lacked a done signal for the revoke and its replies
  asked for no evidence back.
- The current skill's run gave the operator a false platform fact (repository secrets "would
  not be seen" by an environment job) and let an "already on Nimbus" observation continue to
  verification without a stop or data check. The candidate's verify-platform-facts rule and
  three-branch first stage are where it gains on X1 and C2.
- The candidate's run is the only one whose task 1 reply says what to send back (W11). It used
  the published `.env` snippet unchanged.
- Shared gaps, all arms 1: no arm put a typed word on all three hard-to-undo steps of the
  cutover (the CNAME change got text but no typed gate), no arm kept a progress record that a
  re-run reads (C6), and none traced names in a visible step without also simulating the flow
  (W10: the candidate ran its script against a fake `gh` in a scratch copy, which the grader
  counted as running the interactive flow).

## Limitations

- One run per arm and one grader, all from one model family. A one-point gap can be noise. The
  grader names its judgement calls (W8 for `wizard`, W9 for the current skill, W10, C4, X1 for
  `wizard`); none changes the gate.
- The same author wrote the fixture, the rubric and the candidate, and wrote the candidate after
  reading the baseline outputs and a council brief that summarised them. The rubric was frozen
  first, but the candidate fits this fixture more than it should: the graded text's stage
  contract used the fixture's names in its examples (PayLane keys, a Mailbird token, `SYNC`
  and `REVOKE` as typed words, "the final sync, the revoke" in a red flag), and two rules come
  straight from baseline errors (verify platform facts, after the false GitHub secret-scope
  claim; repository versus environment secrets in the shell table). After grading, the example
  names were replaced with neutral ones (Inkwell keys, a Relay token, `MIGRATE` and `DELETE`, "a
  migration, a key deletion"); no rule or step changed, and the edited text was not re-run. An
  "Operational example (offline)" section, the offline fixture every sibling member carries,
  was also added after grading; it changes no instruction.
  Part of the candidate's lead on C2 and X1 may come from this fit.
- The current-arm run was resumed after a usage-limit stop, so its context differed from the
  others; the `wizard` arm ran on its second attempt.
- The fixture's workflow has an unintended defect (a release step that needs
  `contents: write`); only the `wizard` run noticed it. The rubric does not score it.
- The grader did not execute bash 3.2 or the artifacts; bash 3.2 compatibility was judged by
  reading. The `.env` snippets' symlink and file-mode cases ran only where the platform allows
  them (Linux CI); on the maintainer's Windows machine they are skipped.
