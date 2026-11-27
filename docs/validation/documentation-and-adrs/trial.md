# Comparison trial: documentation and ADRs

Run on 2026-11-26 and 2026-11-27. One blind run per arm on the fixture built by
[build_docs_fixture.py](build_docs_fixture.py), scored against the [rubric](rubric.md), which was
frozen (commit d09bb2c) before the candidate was written. Evidence per score is in
[scores.md](scores.md).

## Setup

- Arms:
  - Addy: `addyosmani/agent-skills:skills/documentation-and-adrs/SKILL.md` at 551c59c.
  - Current: `andino-documentation-and-adrs` at AI-RULES main 1e78323.
  - Candidate: this branch's skill folder at commit 4cf71f4 (the files as committed).
  - A no-skill control was left out by agreement with the user.
- Tasks: turn meeting notes into an ADR in a repository with its own template and a reserved
  number; document a cancellation change and write its release note; audit four module documents
  for drift (stale by both history and content, stale by history only, newer than the code but
  wrong, unordered history); clean up comments in one file without changing behaviour.
- Runners: three Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each on a fresh
  fixture build with its own copy of its guidance and the rubric's run prompt, told to read
  nothing else and to use no skills, slash commands or subagents. The Addy and Current arms ran
  first (a first attempt of both was stopped by a usage limit, discarded, and rerun on fresh
  builds); the candidate ran after the council and the rewrite.
- Between the baseline runs and the rewrite, a five-advisor council (Sonnet 5.5, medium) with
  three anonymous reviewers (Sonnet 5.5, low) read the two skills, the sibling layout and an
  unblinded summary of the baseline outputs, and chose the design: the sibling layout as one
  gated procedure, with templates and the drift method in resources and each gate's rule inline.
- Collection and blinding: `collect_run.py` captured each run's reports, git state, test run,
  full diff, a diff ignoring CR/LF changes and new files. The three collections were copied to
  folders A-C with a random mapping kept outside the grading folder and searched for guidance
  names (none found). One grader (Sonnet 5.5, medium) saw only the rubric, the builder and the
  three folders.

## Scores

| Criterion | Addy | Current | Candidate |
| --- | --- | --- | --- |
| A5 options on the same criteria | 1 | 1 | 2 |
| A8 consequences and revisit trigger | 1 | 2 | 2 |
| B3 every outcome with caller action | 1 | 1 | 2 |
| B5 side effect, once only | 1 | 1 | 2 |
| B6 release note labels the breaking change | 1 | 1 | 2 |
| C4 auth history "can't tell" | 2 | 1 | 2 |
| C5 change-log entries appended with reason | 2 | 1 | 2 |
| C6 audit report with evidence | 2 | 1 | 2 |
| D3 untracked TODO reported as follow-up | 1 | 1 | 2 |
| D5 time hazard explained from ADR-0005 | 1 | 1 | 2 |
| Other 20 criteria | 2 each | 2 each | 2 each |
| Task 1 A1-A8 (16) | 14 | 15 | 16 |
| Task 2 B1-B8 (16) | 13 | 13 | 16 |
| Task 3 C1-C6 (12) | 12 | 9 | 12 |
| Task 4 D1-D6 (12) | 10 | 10 | 12 |
| Whole run E1-E2 (4) | 4 | 4 | 4 |
| Total (of 60) | 53 | 51 | 60 |

Gate (candidate at least equal to every other arm on every criterion): PASS. The candidate scored
2 on all 30 criteria.

## Reading the result

- All three arms got the large things right: the house ADR format, number 0009 past the reserved
  0008, status proposed, the predecessor left accepted, qualifiers on the single staging run, the
  unsupported "scales to any load" claim kept out, both wrong module documents found and fixed,
  the refactor-only and unordered-history documents judged accurate from content, released
  changelog entries untouched, and behaviour unchanged in `slots.py`.
- The differences are in the steps the candidate writes as "Done when" outputs. Only the
  candidate labelled the breaking changes in the release note with the client action, gave a
  caller action for every outcome, stated that the e-mail is sent once per successful cancel,
  judged every ADR option on one named list of criteria, reported the deleted untracked TODO as
  follow-up, and turned the vague time warning into the specific hazard from ADR-0005 (host time
  zone, how far in the past a UTC host would accept).
- Addy's skill and the candidate both reported the unordered auth history as "can't tell" and
  appended dated change-log entries with a reason; the current Andino skill did neither, dated its
  entries with the code-change date and inserted one out of order. The current skill and the
  candidate both gave the ADR a revisit condition; Addy's arm did not.
- Compared with the current skill, the candidate gained on A5, B3, B5, B6, C4, C5, C6, D3 and D5
  (51 to 60) and lost no criterion. Compared with Addy's skill it gained on A5, A8, B3, B5, B6,
  D3 and D5 (53 to 60) and lost none.

## Limitations

- One run per arm and one grading, all from one model family. The grader named close calls on
  A5, A8, B3, B5, B6 and C6 for the other arms; the candidate scored 2 on each without a close call.
- The same author wrote the fixture, the rubric and the candidate, and wrote the candidate after
  reading the baseline outputs and the council's discussion of them. The rubric was frozen first,
  and template examples that resembled the fixture (a job-queue ADR, a halved refund, a
  200-to-409 retry change) were replaced with other domains before the candidate ran, but the
  candidate may still fit this fixture. No second fixture was run.
- The host's file tools rewrote LF as CRLF in every arm. The collector's CR/LF-insensitive diff
  was added after the rubric was frozen, and the grader was told to judge "byte-identical"
  criteria (B7, C5) ignoring line endings. This applied equally to all arms.
- The rubric scores written documents, reports and repository state. It does not measure how
  documents age on a real project or how well the skill triggers from its description.
