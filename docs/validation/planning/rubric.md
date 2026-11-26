# Comparison rubric: planning

Frozen on 2026-11-26 before any change to the candidate skill. Every arm runs the same prompt
on the same fixture:

- Jesse Vincent's `writing-plans` (obra/superpowers, `skills/writing-plans/SKILL.md` at main
  on 2026-11-26);
- Addy Osmani's `planning-and-task-breakdown` (addyosmani/agent-skills,
  `skills/planning-and-task-breakdown/` at main on 2026-11-26, with its shared
  definition-of-done reference);
- the current `andino-planning` (AI-RULES main at 1e78323), with the workflow files it names
  (`references/execution-plan.md`, `references/execution-plan-template.md`,
  `skills/tdd/GUIDE.md`) under `guide/andino-workflow/`;
- the candidate rewrite.

A grader who sees only this rubric, the fixture and the anonymised outputs (labelled A, B, ...)
scores every criterion.

## Fixture

`fixture/koperasi/` is a small Python 3.9, standard-library-only loan bookkeeping CLI with a
green `unittest` suite (9 tests, `python -m unittest discover -s tests -v`; pytest is not
installed) and one accepted design, `docs/specs/2026-11-20-arrears-design.md`, with eight
requirements: payments (R1), days late (R2), the late fee (R3), the `arrears` command (R4),
nothing late (R5), bad date (R6), the `pay` command (R7) and cooperative holidays (R8).

Facts a good plan has to find or respect:

- `koperasi/dates.py::days_between` returns `abs(...)`. It is used by `list`. Using it for days
  late makes an installment due after `as_of` look late; changing it changes `list`.
- `koperasi/money.py` already has `format_rupiah` and `parse_rupiah`; `parse_rupiah("0")`
  returns 0 (the spec says nothing about a zero payment).
- `koperasi/store.py` builds `Installment` from three keys and writes three keys back;
  `save_loans` already replaces the file atomically. Old files have no `paid_amount`.
- `tests/helpers.py` has `run_cli(args) -> (code, out, err)` and `write_data(loans) -> path`;
  `tests/test_cli.py` shows the pattern. Tests import `from helpers import ...`.
- The existing `list` command already handles a missing data file with
  `File data tidak ditemukan: <path>` and exit 1.
- R8's calendar format is unknown: Bu Sari will send a sample. Nobody can answer during the run.
- `koperasi/cli.py`, `koperasi/store.py` and `koperasi/models.py` are touched by more than one
  requirement.
- Fee arithmetic in integers: `overdue * fee_days * 5 // 1000`, capped at `overdue // 10`
  (Rp 333.333 for 2 fee days gives 3.333; a float formula can round differently).

## Run setup

Each arm gets `python setup_run.py <RUN_DIR> [--guide <skill folder>]`. Runners use no skill,
slash command or subagent and read nothing outside `<RUN_DIR>`. One runner per arm: Claude Code
subagent, Sonnet 5.5, effort medium.

Run prompt, identical for every arm (`<RUN_DIR>` substituted):

> If the folder `<RUN_DIR>/guide/` exists, read `guide/SKILL.md` first and follow it, opening
> any file it points you to when its condition applies. You are working alone: the treasurer
> and the team are away until you finish, so nobody can answer questions or review anything
> during this run. The repository is `<RUN_DIR>/koperasi/`; read its README first. Python is
> available as `python`.
>
> Message from Bu Sari (treasurer): "The arrears design is accepted:
> `docs/specs/2026-11-20-arrears-design.md`. Please write the implementation plan so another
> developer can build it next week without asking us anything. Don't build it yet."
>
> Save the plan inside the repository where you would normally save it, and write
> `<RUN_DIR>/out/reply.md`: your reply to Bu Sari, exactly as you would send it. Do not change
> source code or tests. Do not mention which guidance you used. Touch nothing outside
> `<RUN_DIR>`. Use no skills, slash commands or subagents.

## Grading material

Per arm, under its letter: `plan.md` (every new or changed Markdown file in the repository,
concatenated with its path), `reply.md`, and `files.txt` (every path added, changed or removed
against the baseline commit). Skill and product names in plans are replaced with `[guide]`,
and plan paths are shown as `<plan>`. Blinding is partial: a plan's structure can still hint
at its guide.

## Scoring

Score each criterion 0, 1 or 2 with one line of evidence (a quote or a section name). Score
what the plan and reply say; a criterion the run never addresses scores 0.

### Grounding and fidelity

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| F1 | Planning only | `files.txt` shows only plan files added or changed; no source, test or data file changed | (no 1) | Any source, test or data change |
| F2 | Carried constraints | Python 3.9 (no `match`, no `X \| None`), standard library only, integer rupiah and old-file loading all appear as plan-wide constraints and are applied where they bite (a task or test for old files; integer fee arithmetic) | All four listed, but at least one not applied in any task | Fewer than four |
| F3 | Exact literals | All CLI texts of R4 to R7 (line format with two-space separators, `Total tunggakan: ...  Total denda: ...`, `Tidak ada tunggakan per <date>.`, `Tanggal tidak valid: <value>`, both `pay` errors, `Tercatat: ...`), exit codes 0/1/2 and the sort order appear verbatim in task acceptance or test code | One or two missing or paraphrased | Three or more missing or paraphrased |
| F4 | Fee rule decided | The fee rule is fixed in integer arithmetic (or an equivalent stated rounding) and the spec's four example rows appear as test values, Rp 333.333 / 5 days -> 3.333 included | Formula and some examples, or a float formula with floor that is not checked against 333.333 | Restated in prose only |
| F5 | Existing code reused | Names and uses `format_rupiah`, `parse_rupiah`, `run_cli`/`write_data` and the existing missing-file message pattern correctly; no new duplicate helper | Most reused, or one real symbol misnamed | Invents duplicates or several wrong names |
| F6 | `days_between` trap | Notices that `days_between` is absolute and is used by `list`; days late uses a signed computation in a new or separate function, with a test for an installment due after `as_of` (and on `as_of`) that is not late | Signed computation specified and the not-yet-due case tested, without naming the trap | Plans to use `days_between` for days late, or to change it without covering `list` |
| F7 | Old data files | A task changes `load_loans`/`save_loans` for `paid_amount` with a test that loads an installment lacking `paid_amount` as 0 and a round-trip that keeps it | Mentioned with no test, or tested only one direction | Not addressed |

### Task quality

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| T1 | Coverage | R1 to R7 each have an owning task and a named check; R8 has an owning item (task, blocked item or discovery) | One of R1 to R7 has no owner or no check | Two or more |
| T2 | Tests as code | Behaviour tasks give named tests with assertions as code using the spec's values, for the fee, days late and both commands | Tests named with prose expectations, or code for only some tasks | Generic "write tests" |
| T3 | Red, then green | Each behaviour task runs its new test before the change with the exact command and says what failure to expect, then reruns after | Commands given, but the expected failure is missing or generic | No failing run before the change |
| T4 | Interfaces agree | Cross-task names and signatures (for example the fee and days-late functions, `paid_amount`) are stated where produced and used with the same name, parameters and return type everywhere | One mismatch, or interfaces implied but not stated | Several mismatches |
| T5 | Order and shared files | Tasks have IDs and explicit dependencies; edits to `cli.py`, `store.py` and `models.py` are sequenced so two tasks never edit the same file in parallel; each task ends with something checkable | Order clear but shared-file conflicts not handled, or one task not checkable on its own | No dependency order |
| T6 | Implied failure cases | At least four cases the spec implies but does not spell out are planned as tests: pay amount 0, pay exactly the remaining amount (allowed, settles), days late exactly 3 and 4, an installment due on `as_of`, a settled installment not listed, a missing data file for `arrears` or `pay`, a malformed amount for `pay`, an `int` returned for a non-integer fee | Two or three | One or none |
| T7 | Unknown handled honestly | R8 is not invented: the plan marks it blocked or a discovery item that names what is missing (the export's columns and date format), who provides it, what the rest of the plan does without it, and how it plugs in later (for example an effective-due-date seam); no task depends on it unnecessarily | Marked unknown but a guessed format is presented as settled in some task, or the seam is missing | A guessed format presented as fact, or R8 silently dropped |
| T8 | Runnable checks | Commands are the repository's real ones (`python -m unittest ...` from the repository root; no pytest), with the working directory, and a final end-to-end check runs `arrears` and `pay` on concrete data with the expected output stated | Real commands but no end-to-end check, or the expected output is vague | Invented tools (pytest, linters) or no commands |

### Usefulness

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| U1 | First step without questions | A fresh developer can start the first task from the plan alone: the file, the test to write with its assertion and the command are all there | One thing must be looked up or guessed | The first step needs a decision the plan does not make |
| U2 | Proportion | Routine bodies are left to the developer; code appears for tests, the fee rule and other decisions the spec does not settle; the plan is not a transcript of the program (rough guide: code blocks are not most of the plan) | Some routine bodies transcribed, or the plan is so thin that two tasks need guessing | Mostly a full implementation, or mostly prose with no decisions |
| U3 | Risks and review focus | The plan names the few things most likely to go wrong (for example the abs trap, float fees, old files, R8) and ties each to a task or test | Risks listed but not tied to tasks | None |
| U4 | Reply to Bu Sari | The reply says where the plan is, what is ready to build, what is blocked on her (the calendar sample, with what is needed from it) and what she does next, in plain words, with no claim that anything was built or tested | Reply correct but misses the R8 request or is written for a developer | Overclaims, or no reply |
| U5 | Honesty | No planned check is reported as run; no invented repository facts (wrong file, function or command) | One unmarked assumption or a minor wrong fact | Several, or a claim the files contradict |

Maximum: 20 criteria, 40 points.

## Gate

The candidate passes when its score is at least every other arm's score on every criterion.
With one run per arm a one-point difference can be noise; the trial record says so.
