# Review, fix rounds and finishing

Internal Andino resource for `andino-delegation`. Review exists to produce proof, not to fill a
quota of reviewers or rounds. The parent owns acceptance. Prompts for every reviewer role are in
[briefs and prompts](subagent-brief-and-report-schemas.md); severity and ruling rules are in
[the rules](contract.md).

## Who reviews what

- **The parent, every task.** Read the task's complete owned diff and its proof yourself. A
  reviewer's verdict never replaces this.
- **One reviewer, for risk.** Add one reviewer listed in the envelope when the task touches
  security, concurrency or races, state machines, migrations, money, data integrity, or renderer
  and 3D work, or when the plan names a risk. One reviewer covers both tracks: spec compliance
  first, then quality.
- **Spec track.** For each requirement: the value or behavior, the file or symbol that meets it,
  the observation that proves it, and PASS, FAIL or UNVERIFIED. Look for missing, extra and
  misunderstood behavior.
- **Quality track.** Real consequences: correctness, edge cases, error paths, collaborators that
  are really exercised, tests that would catch the defect they claim to cover.

## Pin the change

Give a reviewer the exact change, as files:

- `python scripts/review_package.py PLAN BASE HEAD` (from the installed skill folder) packages a
  nonempty committed range: log, stat and diff. Record BASE before the task starts; never use
  `HEAD~1`, which drops all but the last commit of a multi-commit task.
- The package covers commits only. Staged, unstaged and untracked owned files go in a separate
  snapshot with their hashes. Never claim an empty or old commit range covers work in progress, and
  never make commits only to feed the helper.
- The package also does not separate another lane's commits; check ownership before handing it
  over. A reviewer may read narrow callers to check a named contract.

## Fix rounds

A round starts when the review reports a spec FAIL, a Critical or Important finding, or an
UNVERIFIED item you confirmed as a real gap.

1. **Route before the loop.** Minor findings go to the journal as deferred
   (`Task 3: minor (deferred): ...`) and never enter the loop. A finding that contradicts the spec or
   a recorded ruling is yours to rule on now; record the ruling, then act. A finding the plan
   mandates is still a finding: rule on it against the spec, do not dismiss it because the plan
   says so.
2. **Send the open findings verbatim** to the same worker when it is listed in the envelope and idle
   after returning normally. Its context is intact. If it stopped, failed or hit a usage limit, ask
   before resuming it, or take the task over inline once ownership has moved.
3. **The worker fixes**, reruns the tests that cover the change and appends a fix report: what
   changed, the command, the output. Check that all three are there before the re-review.
4. **Scoped re-review** of the fix diff only (package from the head the last review saw). It
   verdicts each finding ADDRESSED or NOT ADDRESSED and reports new breakage in the fix. Issues
   outside the fix go to the journal as deferred; they do not extend the loop.
5. **Record the round**: `Task 3: fix round 1/5 (2 addressed, 1 open: <one-liners>; commits a1b2c3d..e4f5a6b)`.

Five rounds is a ceiling, never an allowance. Stop earlier when a round brings no new evidence. A
stronger model, a fresh agent or more effort is a new ask, never automatic at a round number.

When you fix inline yourself, the fix gets the same check: rerun the covering tests and give the
fix diff the same scoped review, or a disclosed self-review when no reviewer is listed.

## Items the reviewer cannot verify

A reviewer reports requirements it could not check from the diff (they live in unchanged code or
span tasks). Resolve each one yourself before accepting: you hold the cross-task context. A real gap
joins the open findings. An item that belongs to a later task becomes part of that task's
acceptance, recorded in the plan.

## At the cap

When round five leaves findings open, stop sending fixes and rule on each one:

- **The reviewer is wrong or the point is contestable**: close it with the code or test evidence,
  as a ruling.
- **Real, optional, nothing builds on it**: defer it with its consequence, as a ruling.
- **Real and required, or a later task builds on it**: the task stays incomplete. Rule on the
  smallest change that unblocks the dependent work and carry it into the next dispatch, or revise
  the plan, or ask the user for the missing decision. Never mark it DONE.

An interface change updates the producer and consumer contracts and invalidates their evidence
before any dependent task runs.

## Final review and finish

1. **Integration gate.** After every task is accepted, run the plan's real public checks on the
   combined files and record their identity. A worker's local pass does not show the joint result.
   Read the outputs for assumptions two tasks made differently, even when their files are disjoint.
   Reuse evidence that is unchanged instead of rerunning every suite per task.
2. **One whole-change review.** Either your own two-track pass, disclosed as not independent, or one
   reviewer listed in the envelope and justified by risk, at the lowest adequate tier. Point it at
   the journal's deferred findings and rulings so it can say which must be fixed before merge.
3. **One fix wave.** Send all its findings to one fixer (a listed worker or yourself), never one
   fixer per finding, then run one scoped re-review. There is no second wave: rule on what remains,
   and what you cannot rule on goes to the user.
4. **Report.** What changed, the evidence, what is not verified, deferred findings, and "Rulings I
   made": every ruling from the plan and journal, in order, each with its cost if wrong. A ruling
   missing from that list was a decision made in secret.
