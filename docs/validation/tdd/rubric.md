# Comparison rubric: test-driven development

Frozen on 2026-11-26 before any change to the candidate skill. Six arms run the same prompt
on the same fixture:

- unguided control (no skill);
- Addy Osmani's `test-driven-development` (addyosmani/agent-skills, path last changed in
  df50a6d);
- Matt Pocock's `tdd` (mattpocock/skills, path last changed in 3f59913), with its
  `tests.md` and `mocking.md`;
- Jesse Vincent's `test-driven-development` (obra/superpowers, path last changed in 5bf4e78),
  with its `writing-good-tests.md`;
- the current `andino-tdd` (AI-RULES main at 1e78323);
- the candidate rewrite.

A grader who sees only this rubric, the fixture and the six anonymised outputs (labelled
A to F) scores every criterion.

## Fixture

`fixture/` holds three independent Python repositories (standard library only). `setup_run.py`
copies them into a run folder and commits a baseline in each.

- `task1/`, garage fees. A feature with two rules: stays of 15 minutes or less are free, and
  motorbikes pay half the car fee rounded up to the next Rp 500 (daily cap Rp 20.000). The
  code lives under `src/`, so plain `python -m unittest` cannot import it; the README and CI
  use `python scripts/test.py`. `TicketDesk.close_ticket` (the gate's entry point) uses a
  clock and an SMS gateway; `tests/helpers.py` has a recording SMS double and
  `garage/clock.py` a fixed clock. Before the change a car or motorbike pays Rp 5.000 for
  15 minutes and a motorbike pays the car fee.
- `task2/`, invoice tax. `ppn` truncates the tax of every line and sums the lines, so
  INV-2026-0412 (three lines of Rp 33.333) shows PPN Rp 10.998 instead of Rp 11.000. The
  README rule is 11% of the subtotal, rounded half up. A fix with Python's `round` passes the
  reported invoice but rounds a subtotal of 150 (PPN 16,50) to 16 instead of 17.
  `tests/test_footer.py::FooterTest::test_footer_shows_16_digit_npwp` fails before any change
  (known issue INV-77 in the README).
- `task3/`, sign-up. The duplicate-email check is already correct (commit "Normalize emails
  before the duplicate check (ACC-212)"); the commit before it, "Add account registration",
  compares emails as typed. No test covers the duplicate check. A test that registers the
  identical address twice passes on both revisions and guards nothing.

`check_run.py` runs hidden checks on a finished run: the public API on cases the runner was
not told about (`checks.txt`, "Behaviour on the final code"), the final suite on the final
code, and the final suite against the production code from before the change (task1 and
task2: the baseline; task3: the commit before ACC-212). A test that guards the change fails
in that last run.

## Run setup

Each arm gets `python setup_run.py <RUN_DIR> [--guide <skill folder>]`. Runners use no
skill, slash command or subagent and read nothing outside `<RUN_DIR>`. One runner per arm:
Claude Code subagent, Sonnet 5.5, effort medium.

Run prompt, identical for every arm (`<RUN_DIR>` substituted):

> If the folder `<RUN_DIR>/guide/` exists, read `guide/SKILL.md` first and follow it,
> opening any file it points you to when its condition applies. You are working alone: the
> people who sent these requests are away until you finish, so nobody can answer questions
> during this run. Handle three independent requests, in order. Each has its own repository;
> read its README first. Python is available as `python`.
>
> Task 1, repository `<RUN_DIR>/task1/`. Message from Sari (garage operations): "From
> 1 December two tariff changes go live. First, a grace period: a vehicle that leaves
> 15 minutes or less after it entered pays nothing. Second, motorbikes pay half of what a
> car would pay for the same stay, rounded up to the next Rp 500, so their daily cap becomes
> Rp 20.000. Cars are otherwise unchanged. The exit gate calls `close_ticket`, and the SMS
> receipt must show the new fee. Please build both."
>
> Task 2, repository `<RUN_DIR>/task2/`. Message from Bima (accounting): "Invoice
> INV-2026-0412 (`python -m invoices.render INV-2026-0412`) shows PPN Rp 10.998 and a total
> of Rp 110.997. Our tax consultant says PPN is 11% of Rp 99.999 = Rp 10.999,89, so
> Rp 11.000, and the total is Rp 110.999. Please fix it so our invoices come out right."
>
> Task 3, repository `<RUN_DIR>/task3/`. Message from Tari (product): "In October we
> shipped a bug: people could sign up twice with the same email if they typed it with
> capitals or a trailing space ('Ana@Mail.example ' and 'ana@mail.example'), and we ended up
> with duplicate accounts. Fikri fixed it (ACC-212), but nobody added a test. Please add a
> regression test so it cannot come back. The sign-up code works now, so only change it if
> you find it is actually broken."
>
> For each task write `<RUN_DIR>/out/taskN.md`: your reply to the person who asked, exactly
> as you would send it. Leave each repository in the state you would hand over, without
> committing. Do not mention which guidance you used. Touch nothing outside `<RUN_DIR>`. Use
> no skills, slash commands or subagents.

## Grading material

Per arm, under its letter: `out/` (the three replies), `taskN.diff` (every change against
the baseline commit, untracked files included), `files.txt` (paths added, removed and
changed; commits, extra worktrees and stashes left behind), `checks.txt` (the hidden checks)
and `transcript.md` exported with `export_transcript.py`. The transcript keeps every command
and edit in order with its truncated result; reads of the guidance folder show only as
`[reads guidance]` and the run folder as `<RUN>`. A run whose transcript shows a Skill,
slash command or subagent call is contaminated and is reported, not graded.

## Scoring

Score each criterion 0, 1 or 2 with one line of evidence (file and quote, transcript step or
`checks.txt` line). Score what the run did and wrote; a criterion the run never addresses
scores 0 unless the row says otherwise. "Before" and "after" refer to the order of
transcript steps. "New test" means a test the run added or changed.

### Task 1: the garage tariff (feature)

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| F1 | Vertical slices | The grace period and the motorbike rate each go through their own cycle: a new test is run and seen failing, then the production code for that rule is written, then the test is seen passing; the second rule's test is written after the first rule passes | Tests for both rules are written and seen failing before any production change, then both rules are implemented together; or only one rule gets a visible cycle | A production change comes before any new test is seen failing |
| F2 | RED for the right reason | Every new test that guards a rule is run before the production change for that rule and fails on an assertion that shows expected and actual (for example `5000 != 0`), not on an import, name, type or signature error; an error of that kind, when it occurs, is fixed and the test rerun before the production change | At least one new test is seen failing on such an assertion; the others are not run before the change or fail only with an error | No new test is seen failing before the change |
| F3 | Independent expectations | Every expected fee or receipt in the new tests is a literal worked out from the tariff (0, 2.500, 4.500, 20.000 ...), not computed by calling production code or by restating the formula in the test | One new test derives its expectation from production code or the formula | Most new tests do |
| F4 | Public seam | New tests call `fee_for_stay` or `TicketDesk.close_ticket` only, and at least one test checks a new rule through `close_ticket` (fee or SMS text); no test calls `_started_hours`, `_hourly` or a new private helper | The new rules are tested only through `fee_for_stay`, or one test calls a private helper | The new rules are tested mainly through private helpers |
| F5 | Doubles only at boundaries | The clock and the SMS gateway are the only things replaced (the fixture's `FixedClock` and `RecordingSms` or equivalents); billing runs for real; assertions are on the fee or the receipt text, not on whether or how often a function was called | One test patches an internal collaborator or asserts a call count instead of an outcome | Billing is mocked in the `close_ticket` tests, or the tests assert mock calls only |
| F6 | Boundary cases | The new tests cover all three: exactly 15 minutes (free) against just over 15 minutes (charged), a motorbike stay whose half fee must round up (for example 2 hours: Rp 4.250 becomes Rp 4.500), and the motorbike daily cap (Rp 20.000) | Two of the three | One or none |
| F7 | Correct and minimal | Every "Behaviour on the final code" line in `checks.txt` for task1 is OK and the diff adds nothing beyond the two rules and their tests (no extra vehicle types, configurable grace period, changed public signatures or unrelated refactoring) | All lines OK with one unrequested change, or one line WRONG | Two or more lines WRONG |

### Task 2: the invoice tax (bug)

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| B1 | Reproduce before changing | The reporter's command is run before any file is edited and shows PPN Rp 10.998 / total Rp 110.997 | The symptom is seen only through a new test, or only after an edit | Not reproduced |
| B2 | Failing test first | A new test asserting INV-2026-0412's PPN (11.000) or total (110.999), through `load`, `Invoice`, `render` or `ppn` with that invoice's lines, is run and seen failing on an assertion before the fix and seen passing after it | A new test exists but is not seen failing before the fix, or fails before it only with an error | No new test for the report |
| B3 | Independent expectations | Expected values in the new tests are literals (11.000, 110.999, 17 ...) | One expectation is computed with a formula such as `round(subtotal * 0.11)` | The tests compute the expected tax the way the code does |
| B4 | Root fix | Every "Behaviour on the final code" line for task2 in `checks.txt` is OK: tax on the subtotal, rounded half up | INV-2026-0412 is right but another line is WRONG (for example subtotal 150 gives 16 because of `round`) | INV-2026-0412 is still wrong, or it is fixed by a special case |
| B5 | Rounding edge tested | A new test covers a subtotal whose PPN ends in exactly ,50 and expects it rounded up (for example 150 gives 17) | A new test covers another case beyond the report (per-line against subtotal rounding, a case just below ,50) but not ,50 | Only the reported invoice is tested |
| B6 | Honest suite report | The full suite is run after the fix with `python run_tests.py`; the reply names the footer failure as the known INV-77 issue, unrelated to the fix; the footer and its test are untouched | The suite is run but INV-77 is not mentioned, or it is mentioned without a suite run | The INV-77 test or the footer is changed, skipped or deleted, or the reply says all tests pass |

### Task 3: the sign-up regression test

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| G1 | No redundant production change | `checks.txt` shows the production code unchanged against the ACC-212 commit, and the reply says the code was already correct | A change in `accounts/` that does not alter behaviour (comment, formatting) | A behavioural change to `accounts/` |
| G2 | Test proven to catch the bug | The new test is run against the pre-ACC-212 code (a temporary checkout or worktree of "Add account registration", or the normalisation temporarily reverted) and seen failing there, then seen passing on the current code; the repository is restored (no stray worktree, stash, commit or change in `accounts/`); `checks.txt` shows the new test failing against the code before ACC-212 | `checks.txt` shows the new test failing before ACC-212, but the run only ever saw it pass; or it saw it fail and left a trace behind | `checks.txt` shows every new test passing against the code before ACC-212, or there is no new test |
| G3 | Public seam and reported shape | The test goes through `AccountService.register` with the `FakeMailer`, registers an address and then the same address with different capitals and surrounding space, and asserts the duplicate is refused; it does not call `_normalize_email` directly | It covers capitals or spaces but not both, or it also calls `_normalize_email` directly | It tests only `_normalize_email`, or only an identical address |

### All tasks

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Repository commands | In every repository the focused runs and a final full-suite run use the README's command (`python scripts/test.py`, `python run_tests.py`, `python -m unittest discover -s tests -t .`) | One repository uses another command that still runs its tests, or one repository gets no final full-suite run | Two or more repositories get no final full-suite run |
| Q2 | Replies | Each reply says what changed, names the tests added, gives the commands with their results (failing before, passing after where it applies) and what is not verified, in plain words, and every claim matches the transcript | Two replies meet this, or one claim is not backed by the transcript | Otherwise |
| Q3 | Clean handover | No scratch files, debug output, stray worktrees, stashes or commits remain; only the intended files changed | One stray item | Several |

Maximum: 19 criteria, 38 points.

## Gate

The candidate passes when its score is at least every other arm's score on every criterion.
With one run per arm a one-point difference can be noise; the trial record says so.
