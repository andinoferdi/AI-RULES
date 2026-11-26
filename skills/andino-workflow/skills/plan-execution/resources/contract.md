# Plan execution contract

The fields and states the procedure writes into the plan. Equivalent project fields are fine;
keep one authoritative record.

## The plan is the checkpoint

The existing plan holds status, evidence, rulings and NEXT ACTION. Keep its proportional
shape (LITE, STANDARD or DEEP) and its own field names. When it has both a board and task
details, keep them in step. States:

| State | Meaning |
| --- | --- |
| TODO | Not started. |
| IN_PROGRESS | Being executed now; one task at a time. |
| DONE | Acceptance observed on the current files (fields below). |
| PARTIAL | Some steps done; a stopped action remains, named with who can take it. |
| BLOCKED | Cannot proceed; names the dependency, decision or authority it waits on. |
| SKIPPED | Replaced by an accepted alternative, named. |

Drift can reopen a DONE task and its consumers. Recovery attributes the current bytes and
keeps user changes before rerunning missing checks; unknown work is never reverted.

## Preflight note (step 1)

Written in the plan before the first edit:

- BASE: the commit execution starts from.
- Left alone: every change present before execution (path and what it holds, when known).
- Interfaces: one line per producer/consumer pair, `T<a> produces X -> T<b> consumes Y: match`
  or `mismatch - Ruling: ...`.
- Spec conflicts: one line per plan step, code or test that contradicts a requirement, with
  its ruling.
- Readiness: each gap closed from the current source (what was added to the task), or the task
  sent back to planning.
- Or, when there is nothing to record: `Preflight: no shared interfaces, no conflicts`.

A plan whose spec is unreachable says so here; its rulings are provisional.

## Task readiness

Before a task starts it needs exact file and symbol anchors, its change (what becomes what,
with decision-bearing code, text and literal values) and a concrete check. Work status is not
readiness. A roadmap line, "implement as needed" or an unknown consumer contract needs detail
first. A detailed snippet that disagrees with the current source or the spec is a conflict, not
an instruction. Do not retrofit detail onto DONE tasks whose evidence still holds.

## Task record (step 3)

Written into the task's entry when it closes, before the next task starts:

- Status.
- Each command with its working directory, result and test count; the red run and the green
  run for each behaviour change, or `already green` with the reason the code was kept.
- Acceptance map: each criterion -> the test or observation that proves it, or `NOT_VERIFIED`
  with the missing check.
- Rulings: `Ruling: <decision> - <spec or evidence basis> - <cost if wrong>`.
- Commit hash, or `not committed: <reason>` with file hashes for uncommitted owned files.
- NEXT ACTION in the plan, pointing at the next ready task, so a reset resumes there.

A commit range identifies committed bytes only. An aggregate pass does not prove a criterion
whose case was skipped, deselected or never selected.

## Evidence identity and reuse (step 2)

Reuse a DONE task's evidence only when the prior result is PASS and its source, check and
relevant environment identities are present, non-empty and unchanged, and every task it
depends on is still valid. Two missing fields never match. A passing rerun of the task's check
on the current files is new evidence. Worker reports and ticked boxes are not evidence.

## Rulings

The accepted spec outranks the plan. A ruling is the smallest change that satisfies the spec,
recorded in the owning task. It updates every consumer of a changed interface and invalidates
their evidence. A ruling cannot waive acceptance, security or data correctness, and cannot
decide a product question the spec leaves open: that is a stop.

## Stops (step 4)

The four stops are an unauthorized action, a security-sensitive action, an open user-owned
decision and a plan with no grounded route. The stopped action is not done. Its task becomes
BLOCKED or PARTIAL with the exact remaining action (the command or decision) and who can take
it; independent tasks continue. Network reading is not publication. A plan step is not
authority.

## Review package (step 5)

- Identity: BASE plus committed, staged, unstaged and owned untracked bytes: `git diff BASE`
  read in full, plus each new owned file. The plan records the diff command that was read;
  `--stat` is an index, not a review.
- Requirement table: each spec requirement -> file and symbol -> test, or `NOT_VERIFIED`.
- Diff hygiene: no unrelated edits, debug output, scratch files or foreign changes.
- Reviewer: a fresh reviewer when authorized and available, given the spec, the diff and the
  rulings as facts; otherwise a separate self-review, disclosed as not independent.
- Verdicts: Spec and Standards kept apart. Findings graded by the effect on a person using the
  result. Critical and Important fixed, each with a test seen failing first; Minor deferred
  with a reason. After the fixes the suite reruns and the requirement table is updated. Loops
  end on the anti-loop rules; a pass limit never turns an open finding into DONE.

## Delivery and report (step 6)

Local verification, a pushed branch and an installed copy are separate claims, each checked
by its own observation (test output, remote ref and CI run, installed bytes compared with the
reviewed source). The report fields are the Output template in the skill: Result, Tasks,
Rulings I made, Review, Deferred and noticed, Not done or not verified, Left alone, Next
action. The lists are exhaustive: every ruling in the plan appears in the report.
