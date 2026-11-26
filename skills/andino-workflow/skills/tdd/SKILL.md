---
name: andino-tdd
description: Use when a feature, bug fix or behavior change needs a test that fails before the change, when a regression test is requested for behavior that already works, or when code is pasted with a request to change it or test it. Operates under Andino Workflow governance.
---

# Build each behavior through a test you watched fail

Internal method ID: `andino-tdd` (alias: `tdd`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

Deliver a behavior change in thin vertical slices, each one a tracer bullet through the public
seam: one test, seen red for the reason you predicted, then the smallest change that turns it
green. A test you never saw fail may not test anything, so every test either fails before its
change or is shown failing against the code before the fix. The deliverable is the change, its
tests, and a test record another person can check without repeating the session.

## Trigger and non-trigger

Use when:

- a feature or rule is added or changed;
- a bug is reported and its cause is known or visible, including in pasted code;
- a regression test is requested for behavior that already works, such as a fix that shipped
  without one;
- an accepted plan task changes behavior.

Do not select for:

- A failure whose cause is unknown: `debugging` proves the cause first, and its gate 5 uses this
  skill's red-to-green step.
- Restructuring green code without changing behavior: `code-simplification`.
- Prose, static content or reversible configuration with no behavioral effect.
- Migrating TypeScript test fixtures: the typed-fixtures resource below.

## Select a resource, not a second lifecycle

Load only the resource the current need names. It runs inside this procedure and current
authority; it starts no second plan.

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| Choosing the seam, the test level, the doubles, the expected values or the boundary cases; UI, HTTP, browser, database or asynchronous tests | [test design](resources/test-design.md) | The slice list already names seam, example and break for every row |
| Record fields, the refactor gate in detail, and the invariants the gates rest on | [supporting contract](resources/contract.md) | The gates and the Output template are already clear |
| One task end to end: two rules and a regression guard, with real output | [worked example](resources/worked-example.md) | The gates are already clear |
| Partial or deliberately invalid TypeScript test fixtures (`as Type`, shoehorn) | [typed-fixtures](resources/typed-fixtures/guide.md) | Ordinary test writing |

## Prerequisites

- Find how this repository tests: the README, CONTRIBUTING, CI workflow and any wrapper script
  (`scripts/test.py`, `make test`, `./gradlew test`). Write down the focused command for one test
  and the full-suite command, and use them for every run. A plain `pytest` or `npm test` is a
  guess until the repository confirms it.
- Run the full suite once before changing anything and record which tests already fail.
  Gate 6 compares against this run.
- Read the glossary, ADRs and neighbouring tests for the area, so test names and fixtures use
  the project's words and helpers.
- For a reported bug, run the reporter's command and keep the output that shows the symptom.

## Procedure

Six gates, in order. Gates 2 and 3 repeat once per row of the slice list; gate 4 applies to any
test that passed on its first run. Write each gate's output where it shows now (your message or
notes), not only in the final reply, and carry it into the record.

1. **Write the slice list before any test.** List one row per observable behavior, in the order you
   will build them: each rule or case the request names, each reported symptom, and each boundary a
   rule creates (the exact threshold and just past it, a value that rounds on the half, a cap or
   limit, empty or invalid input). Two rules in one request are two rows. Each row has four fields:
   the behavior in the requester's words; the public seams a caller uses (the entry point, endpoint
   or command, never a private helper; always including any entry point the requester names, such
   as the command or endpoint they call); a literal example worked out by hand from the rule
   (`returned 3 days late -> Rp 1.500`), never computed with the code or a copy of its formula; and
   the break, meaning the production change that should make this test fail. For a reported bug the
   first row is the reporter's own case. Mark a row `already works` when current code should pass
   it. Done when: the list is written before the first test file is touched, every rule, symptom
   and boundary in the request has its own row, and every row has all four fields.
2. **Red: one row, its tests, seen failing.** Take the first open row only. Write its test at each
   of the row's seams with the row's literal expectation, using the project's existing fakes for
   slow or external boundaries. Every test that will guard this row is written now, before its
   production change; a test added later has no red of its own. Before running it, write the test
   name and the failure you expect (`expected 1500, got 0`). Run the focused command. A collection,
   import, syntax, name or fixture error is not red: fix it and rerun. Done when: the output shows
   each of the row's tests failing on an assertion that matches your prediction, and no production
   file has changed for this row yet. An `already works` row, or a test that passes here, goes to
   gate 4.
3. **Green: the smallest change for that row.** In this step edit production code only, and only as
   far as this row needs; tests were written in gate 2, and the next row's behavior waits for its
   own red. A test you realise is missing goes back through gate 2 for its own row. Rerun the same
   focused command, then the tests of the module you touched. Done when: this row's tests pass,
   every earlier row still passes, and the row is marked done in the list. Then return to gate 2
   with the next open row; write no test for a later row before this one is green.
4. **Prove a test that passed at once.** This gate is for an `already works` row and for a test
   that passed at its own gate-2 run; it never stands in for gate 2 on a test written after its
   row's production change. A test that never failed proves nothing until you see it fail on wrong
   code. When the repository history holds the code before the fix, run the new test against it in
   isolation: `git worktree add <temp-dir> <pre-fix-commit>`, copy the test file in, run it there,
   then `git worktree remove --force <temp-dir>` (the copied test makes the temporary tree dirty).
   Without such a revision, make the row's break by hand as a one-line edit of production code, run
   the test, and undo the edit at once; that temporary break is the only production edit this gate
   makes. Done when: the output shows the test failing on the old code or the break and passing on
   the current code, and `git worktree list` and `git status` show no worktree, stash, commit or
   production change left from the proof. A test that cannot be made to fail is too weak:
   strengthen it and repeat, or record the gap.
5. **Refactor, only after every row is green.** Refactoring is optional and separate. Name the
   problem you saw (duplication, an unclear name, a tangled branch), change one thing, rerun the
   suite, and repeat. Keep the seam, outputs, errors and side-effect order unchanged. Done when:
   each refactor step was followed by a green suite run, or you recorded that no refactor was
   needed. Stop and leave the code as it is if a test would have to change.
6. **Verify the whole change.** Run the full suite with the repository's command and compare it
   with the run from Prerequisites, naming every failure and whether it failed before your change.
   For a bug, rerun the reporter's command and compare with what they expected. Read the diff for
   anything outside the change and its tests: scratch files, debug prints, a disabled or weakened
   test, an unrequested feature. Done when: the suite result and the reporter's command (for a bug)
   are shown, every failure is named as old or new, and the diff holds only the rows' changes,
   their tests and any documentation the change needs.

**A row that turns out wrong.** When red fails for a reason other than the one you predicted,
or green needs more than the row describes, stop and rewrite the row before writing more code.
When a test reveals a failure whose cause you cannot explain, switch to `debugging`.

## Rules for every slice

- **One behavior per test.** A test name says what the caller observes ("a loan with a waiting hold
  cannot be renewed"), not how the code works. "And" in a name means two tests.
- **Literal expectations.** Expected values are literals or hand-checked fixtures. A value
  computed with the code under test, its helpers or a restatement of its formula passes by
  construction.
- **Public seams.** Tests call what a caller calls and check what a caller sees. Verify through
  the same interface (create, then fetch), not through a database query or a private attribute.
- **Real collaborators.** Use your own modules for real. Replace only boundaries that are slow,
  external, unsafe or nondeterministic (network, email, payment, clock, randomness), preferably
  with the project's existing fakes, and know the real boundary's side effects and full response
  shape before you replace it. Assert outcomes; assert calls only when the call itself is the
  contract.
- **Tests stay honest.** Change an existing test's assertion only after showing that the contract
  it encodes is wrong. A failing test owned by someone else stays as it is and is named in the
  record. A skipped or deleted test is never the way to green.
- **Your code, the user's code.** Keep code the user wrote, even when it came before its test;
  prove it with gate 4 instead. Redesigning architecture inside a behavior change is a separate
  request.
- **No ceremonial reruns.** Run again after a change that can affect the result; a second run
  of unchanged code adds nothing.

## Shortcuts that break TDD

| Shortcut | What happens |
| --- | --- |
| "Both rules are small, I'll write all the tests first." | Tests written ahead describe imagined behavior and all fail together, so no red is tied to one change. One row, one red, one green. |
| "I'll write the test after the code works." | A test written after passes at once and proves nothing. Gate 4, or start the row again. |
| "The expected value is easiest to compute the way the code does." | The test then agrees with any bug. Work the example out by hand. |
| "It passed first time, good." | It may not reach the behavior. Make it fail on old code (gate 4). |
| "I'll mock the price lookup to isolate checkout." | Internal mocks test the mock. Replace only slow or external boundaries. |
| "`npm test` will do." | Use the command the repository's README or CI runs. |
| "That failing test isn't mine, so all tests pass." | Name every failure and whether it failed before your change. |
| "While I'm here I'll tidy this up." | Refactoring waits until every row is green (gate 5). |
| "Code written before the test must be deleted." | Keep it; prove it with gate 4. |

## Red flags

Return to the gate you skipped when you notice:

- a production edit with no red run of its row before it;
- tests for two rows added in the same step;
- a red that is an import, name or setup error;
- an expected value built from the code under test;
- a mock of your own module, or an assertion on a mock;
- a new test that has never failed;
- a known failure left out of the report, or a test skipped to get green.

## Ownership and permission boundary

Andino coordinates selection, shared progress and final status from evidence; this skill owns
its procedure, resources and checks, which coordinator brevity never truncates. It authorizes
no commit, push, merge, publication, installation, destructive cleanup or external message: use
the host's tools within the session's authority and disclose what was not done.

## Output

End every reply after the gates with this record, also when the requester is not technical:
open with the result in their terms (what now happens, the corrected figure, what they need to
do), then add the record under its own heading, and copy it into the commit or PR message when
you commit.

```text
Test commands: focused <command>; full suite <command>
Slices:
  1. <behavior> | seam <entry point> | example <input -> expected>
     red: <test name> -> <failing assertion line>
     green: <change> -> <passing run>
  2. ...
Proof for tests that passed at once: <test> fails on <pre-fix commit or break> (<line>);
  passes on current code; restored: <git status>
Refactor: <what changed, suite run after> or none
Verification: suite <counts; each failure named "failed before the change" or "new">;
  reporter's command -> <result> (bugs)
Not done or not verified: <items, including choices made for the requester to confirm>
```

## Verification

Before calling the change done, confirm:

- [ ] the slice list was written before the first test and has a row for every rule, symptom
      and boundary in the request;
- [ ] every row has a red run that came before its production edit, or a gate-4 proof;
- [ ] each red was the predicted assertion, never a setup error;
- [ ] expected values are literals worked out by hand;
- [ ] doubles replace only slow or external boundaries, and assertions check outcomes;
- [ ] the full suite ran with the repository's command and every failure is named old or new;
- [ ] the diff holds no scratch file, debug output, skipped test or unrequested change;
- [ ] the reply ends with the record.

## Worked example and anti-pattern

[The worked example](resources/worked-example.md) takes a library's two renewal rules and a
regression guard through all six gates and ends with the filled record.

Anti-pattern: a request with two rules gets one commit with six new tests, all written first,
one red run, and both rules implemented together. Every test passes, yet no single red run shows
which change made which test pass, and a test that could never fail hides among them.

## Fallback

- No seam reaches the behavior: write the missing-seam finding and a bounded reproduction (the
  command and its output); do not claim a shallow test protects it.
- Behavior already satisfied and no red can be produced, not even by a temporary break: record
  the gap and make no production edit.
- No test runner or suite: say so, propose the smallest supported check, and mark the behavior
  not verified.

## Local resources

The resources above are packaged with this skill; upstream repositories are not runtime
dependencies. MIT notices are in [references/license.md](references/license.md).

## Operational example (offline)

Gates 2 and 3 on a toy late-fee rule: the test fails on the code before the change and passes
after.

```python andino-operational-example
import os

def late_fee(days_late, changed):
    if changed and days_late <= 1:
        return 0
    return 500 * days_late

def red_green(changed):
    return late_fee(1, changed) == 0 and late_fee(3, changed) == 1500

if __name__ == "__main__":
    assert red_green(changed=False) is False, "the test must fail before the change"
    assert red_green(changed=True) is True, "the same test must pass after the change"
    raise SystemExit(1 if os.environ.get("ANDINO_NEGATIVE") == "1" else 0)
```

## Provenance

Adapted from Addy Osmani's `test-driven-development` (addyosmani/agent-skills df50a6d), Matt
Pocock's `tdd` (mattpocock/skills 3f59913) and Jesse Vincent's `test-driven-development`
(obra/superpowers 5bf4e78), all MIT. The slice list, the six gates, the pre-fix proof, the
record template and the resources are Andino additions.
