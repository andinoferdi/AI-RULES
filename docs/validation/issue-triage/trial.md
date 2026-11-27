# Comparison trial: issue triage

Run on 2026-11-26. One blind run per arm on the fixture built by
[build_triage_fixture.py](build_triage_fixture.py), scored against the [rubric](rubric.md),
which was frozen (commit 8e1948d) before the candidate was written.

## Setup

- Arms:
  - Current: `andino-issue-triage` at AI-RULES main 1e78323.
  - Matt: `mattpocock/skills:skills/engineering/triage` (SKILL.md, AGENT-BRIEF.md,
    OUT-OF-SCOPE.md) at d80fa0f.
  - Candidate: this branch's skill folder at commit e897f58.
- Tasks: list what needs the maintainer's attention on a local Markdown tracker; triage five
  issues and one external pull request, with write authority for one item only (#3, if its
  bug reproduces); then, as a follow-up message, apply the maintainer's two closing decisions.
  The fixture plants a reproducible bug, a request the project already serves under another
  name, a request matching an earlier rejection in other words, a needs-info item whose
  reporter answered one of two questions, conflicting state labels, a vague crash report, an
  external pull request with gaps and a maintainer's in-flight pull request.
- Runners: three Claude Code subagents, Sonnet 5.5 at medium effort, one per arm, each on a
  fresh fixture copy with its own guidance copy and the rubric's run prompt, told to read
  nothing else and to use no skills, slash commands or subagents. All three ran after the
  rewrite (a first launch of the two baseline arms stopped on a usage limit before writing
  anything; their folders were checked clean and the arms were launched again with the user's
  approval). Matt's skill asks for the `grilling` and `domain-modeling` skills; that arm
  worked inline.
- Collection and blinding: [collect_run.py](collect_run.py) copied each run's outputs, captured
  the repository state (status, branch, stash, branch heads, the full tracked diff, untracked
  files), replaced run paths with `<RUN_DIR>` and checked for guidance names (none left). The
  runs were shuffled to letters with a random mapping kept outside the grading folder. One
  grader (Sonnet 5.5, medium) saw only the rubric, the builder and A to C. Its evidence per
  score is in [scores.md](scores.md).

## Scores

| Criterion | Current | Matt | Candidate |
| --- | --- | --- | --- |
| A1 attention buckets | 0 | 2 | 2 |
| A2 bucket membership | 1 | 1 | 1 |
| A4 counts and one-line items | 1 | 2 | 2 |
| C1 conflicting labels held for the maintainer | 1 | 1 | 2 |
| I1 needs-info notes for the vague report | 1 | 2 | 2 |
| P2 remaining work on the pull request | 1 | 1 | 1 |
| Other 19 criteria | 2 each | 2 each | 2 each |
| Total (of 50) | 43 | 47 | 48 |

Gate (candidate at least equal to every other arm on every criterion): PASS. The candidate is
higher than both other arms on C1, higher than the current skill on A1, A4 and I1, and ties
every arm on the other 21 criteria.

## Reading the result

- Every arm reproduced the CSV bug, wrote a durable brief with testable criteria, applied only
  the authorized write to #3, matched the night-mode request to the colour-themes record
  without closing it, found that "category" filtering already exists as `--tag`, did not
  re-ask the answered needs-info question, verified the pull request on its branch or a copy,
  put the disclaimer on every draft, applied both Task 3 decisions correctly (the rejection
  appended to the existing record, nothing recorded for the built feature) and left the
  repository on `main` with no product code change or commit. On this fixture the authority
  rules of the current skill already held.
- The current skill lost on the attention list: one flat table without the three buckets or
  their counts, and needs-info notes without the established/still-needed split. Both come
  from Matt's method and are now in the candidate.
- Only the candidate stopped on #10's conflicting `waiting` and `agent-ready` labels without
  drafting a brief or a state for it; Matt's arm and the current arm flagged the conflict and
  held the label change, but still wrote a brief or recommended a state.
- All three scored 1 on A2 because they listed #10 in the attention output (the candidate and
  Matt in a separate "needs a decision" group, which the grader noted as a close call), and 1 on
  P2 because none asked for the pull request's error message to become JSON under `--json`.
  The candidate's guidance does not cover that gap; it is recorded here rather than fixed
  to fit the fixture.

## Limitations

- One run per arm and one grading. The grader flagged close calls on A1, A2, O1, C1, I1, P2 and
  A4; with the alternative readings the candidate could tie Matt (C1) or every arm could gain
  on A2 and P2, but no reading puts the candidate below another arm.
- The same author wrote the fixture, the rubric and the candidate. The rubric was frozen first,
  the candidate's examples use other domains, and `tests/test_issue_triage_preservation.py`
  rejects fixture words in the skill, but the candidate may still fit this fixture. No second
  fixture was run.
- Runners and grader come from one model family. The trial measures written outputs and
  repository state, not triage quality on a live tracker or with a real maintainer.
