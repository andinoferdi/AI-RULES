# Blind scores: planning trial

Grader output, unchanged except this header. Letter mapping (kept outside the grading folder
until scoring finished): A = candidate (run-4), B = obra `writing-plans` (run-1), C = current
`andino-planning` (run-3), D = Addy `planning-and-task-breakdown` (run-2).

# Scores

| ID | A | B | C | D |
| --- | --- | --- | --- | --- |
| F1 | 2 | 2 | 2 | 2 |
| F2 | 2 | 2 | 2 | 2 |
| F3 | 2 | 2 | 2 | 2 |
| F4 | 2 | 2 | 2 | 2 |
| F5 | 2 | 1 | 2 | 2 |
| F6 | 2 | 2 | 2 | 2 |
| F7 | 2 | 2 | 2 | 2 |
| T1 | 2 | 2 | 2 | 2 |
| T2 | 2 | 1 | 2 | 1 |
| T3 | 2 | 1 | 2 | 0 |
| T4 | 2 | 2 | 2 | 2 |
| T5 | 2 | 1 | 2 | 2 |
| T6 | 2 | 2 | 2 | 2 |
| T7 | 2 | 2 | 2 | 2 |
| T8 | 1 | 2 | 2 | 2 |
| U1 | 2 | 2 | 2 | 1 |
| U2 | 2 | 2 | 1 | 1 |
| U3 | 2 | 2 | 1 | 2 |
| U4 | 2 | 2 | 2 | 2 |
| U5 | 2 | 2 | 2 | 2 |
| Total | 39 | 36 | 38 | 35 |

Fixture arithmetic was recomputed for every expected value in the plans (days late, fees, totals, test counts); no incorrect expected values were found in any run.

## Evidence

### A
- F1: files.txt lists only `<plan>/arrears-and-payments.md`.
- F2: Global Constraints list all four; applied in T1 `test_old_file_defaults_to_zero`, T2 "integers only ... No float", T3 length check for 3.9 vs newer date parsing.
- F3: T3/T4 give every R4-R7 text, exit codes 0/1/2 and sort order in test code ("A-07  Siti Rahma  cicilan 1  40 hari ...", "Tidak ada tunggakan per 2026-02-18.").
- F4: `fee = overdue * 5 * fee_days // 1000`, cap `overdue // 10`; `LateFeeTest.test_spec_examples` has all four rows incl. `late_fee(333333, 5) == 3333`.
- F5: names `format_rupiah`, `parse_rupiah`, `parse_iso_date`, `write_data`/`remove`/`run_cli`, reuses the `list` missing-file message.
- F6: "Trap, not a guess: `days_between` returns an absolute value"; `days_late` test before, on and after due date.
- F7: T1 `test_old_file_defaults_to_zero` and `test_round_trip_keeps_paid_amount`.
- T1: Coverage table maps R1-R7 to tasks and named tests; R8 owned by T5, T6, D1.
- T2: Full test code for days late, fee, `find_arrears`, both commands.
- T3: Each task has a RED command plus the specific expected failure ("`AssertionError: 0 != 100000`", "`2 != 0`").
- T4: Interfaces blocks give `days_late(due, as_of)`, `late_fee(overdue, days_late)`, `Installment.paid_amount`/`overdue`, `ArrearsRow`, used consistently.
- T5: Execution Board with Depends on; "T3 and T4 share `cli.py` ... run one after the other".
- T6: Tests for days 3 and 4, due on `as_of`, settled not listed, exact remainder, 400001, 0 and "seratus", missing file, text installment number.
- T7: D1 names columns, date format, location, flag; Provided by Bu Sari; T1-T5 proceed; seam `load_holidays` -> `find_arrears(holidays=...)`.
- T8: Real `python -m unittest ... -p` commands from repo root; the final hand run on `data/loans.json` is vague ("late with fee 0 only if within grace on the chosen date; check each line by hand").
- U1: T1 gives file, test code and command.
- U2: Tests as code, routine bodies as prose Change Specification.
- U3: Review Focus plus Risks table tied to tasks (abs trap, float, 3.9 dates, shared cli.py).
- U4: Reply lists ready items, the blocker with exact needs (header, columns, date format, file location), nothing claimed built.
- U5: "Result / Evidence: Not run - planned checks only"; no wrong repo facts found.

### B
- F1: files.txt lists only `docs/plans/2026-11-26-arrears-plan.md`.
- F2: Global Constraints list all four; tests for old file and integer fee; 3.9 warning.
- F3: Task 3 and 4 list all literals, exit codes and sort key `(-days_late, member_id, loan_id, number)`.
- F4: `overdue * 5 * fee_days // 1000`, `// 10` cap; four spec rows incl. `late_fee(333333, 5), 3333` plus `late_fee(333333, 40) == 33333`.
- F5: `parse_rupiah`, `format_rupiah`, `load_loans`/`save_loans`, missing-file message reused; helpers only as "from helpers import ...", `run_cli`/`write_data` not named.
- F6: "Do not use `dates.days_between` (it is absolute ...)"; tests for due on `as_of` and not yet due.
- F7: `test_missing_paid_amount_loads_as_zero` and `test_paid_amount_round_trip`.
- T1: R1-R7 mapped to tasks with tests; R8 in "Not in this plan" blocked section.
- T2: fee/days-late as code; command tests only as prose with exact values ("stdout is exactly these four lines").
- T3: Commands given but expected failure generic ("FAIL (module missing)", "the new tests FAIL").
- T4: Interfaces stated (`overdue_amount`, `days_late(inst, as_of)`, `LateItem`, `late_installments`); Self-Review confirms names agree.
- T5: Tasks numbered with Consumes lines; no explicit dependency or shared-file note for Task 3 and 4 both editing `cli.py` and `test_cli.py`.
- T6: Tests for days 3 and 4, due on `as_of`, overpaid, exact remainder, third payment of 1, bad dates, missing file, non-numeric amount.
- T7: Blocked section names the missing CSV columns and date format, who, and the seam (`late_installments` as the only reader of `due_date`).
- T8: Real commands from repo root; Task 4 runs `arrears --as-of 2026-03-20` on `data/loans.json` with four expected lines; `pay` end to end is in tests, not a run with stated output.
- U1: Task 1 has test code, file and command.
- U2: Code for tests and fee rule, bodies left out.
- U3: Review Focus with 5 items, each pointing to a test in a task.
- U4: Reply states plan location, R1-R7 ready, R8 blocked on the sample (columns and date format unknown), no build claims.
- U5: No planned check reported as run; facts match the repo.

### C
- F1: files.txt lists only `<plan>/arrears.md`.
- F2: Constraints & Invariants list all four; T1 legacy test, D-008 integer fee, D-005 shape check.
- F3: T3/T4 test code holds every R4-R7 literal with newlines, exit codes and sort order.
- F4: D-008 formula; `test_late_fee_table` has all four rows incl. `(333333, 5, 3333)`; `late_fee(333333, 200) == 33333`.
- F5: Baseline section lists `format_rupiah`, `parse_rupiah`, `run_cli`, `write_data`, `remove`, `_cmd_list` message; reused.
- F6: "`days_between` ... returns the ABSOLUTE difference. Do NOT use it for days late"; `test_days_late` before, on and after due.
- F7: `test_legacy_installment_loads_with_zero_paid` and `test_paid_amount_round_trip`; the fixture mixes legacy and new installments.
- T1: Coverage table maps R1-R7 and failure cases to tests; R8 owned by D1 and T6.
- T2: Full test code for rules and both commands.
- T3: Each task has an exact RED command with the expected error ("`AttributeError ... 'paid_amount'`", "`NotImplementedError`", "argparse rejects the unknown `arrears` command").
- T4: Interfaces produced and consumed are named; same signatures throughout.
- T5: Execution Board plus "T3 and T4 both write `cli.py` ... one after the other, never in parallel".
- T6: Tests for days 3 and 4, due on `as_of`, settled, exact settle, overpay, settled pay, unknown ids, invalid amount, missing file, bad date beats missing file.
- T7: D1 lists 6 questions (columns, format, location, missing-file behaviour); T6 gives the seam `next_working_day` plus a `holidays` parameter; T1-T5 independent.
- T8: Commands from repo root; manual `arrears` on sample data (5 late installments) and `pay` on a copy with stated output `Tercatat: L-003 cicilan 1, sisa Rp 200.000`.
- U1: T1 has file, test code, command and expected failure.
- U2: Near-complete implementation of `arrears.py`, `_cmd_arrears` and `_cmd_pay` is transcribed; code is most of the plan.
- U3: Risks appear only as decisions, a baseline note and Known Limitations; no dedicated risk list tied to tasks.
- U4: Reply gives location, R1-R7 ready, R8 blocked on the sample (columns and date format), question 8, honest "Checks" section.
- U5: Baseline run is labelled observed; planned checks marked "Not run"; no wrong facts found.

### D
- F1: files.txt lists `<plan>/plan.md` and `<plan>/todo.md`, both plan files.
- F2: Ground rules list all four; Task 1 loads old files, "Money is `int` rupiah ... use `//`".
- F3: Task 3 and 4 give every literal, exit codes and sort order in acceptance prose and a worked example.
- F4: `min(overdue * 5 * fee_days // 1000, overdue * 10 // 100)`; the four spec values with overdue/days listed as acceptance, including 333333/5 -> 3333.
- F5: `parse_rupiah`, `format_rupiah`, `helpers.write_data`, `run_cli`, missing-file message reused.
- F6: "`dates.days_between` ... takes `abs`"; acceptance for due on `as_of` and due the day before; risk row ties to a due-after-`as_of` test.
- F7: Task 1 acceptance: load without the field, load with it, round trip with a non-zero value.
- T1: Each of R1-R7 owned by a task with acceptance bullets; R8 in "Blocked: R8".
- T2: Tests described in prose with values ("`test_arrears.py` covering each bullet"); no assertion code.
- T3: Verification says "Run the full suite"; no failing run before the change, no expected failure.
- T4: Interfaces consistent (`days_late(installment, as_of)`, `late_fee(overdue, days_late)`, `build_report`, `effective_due_date`).
- T5: Phases, "Dependencies" per task, "build Task 3 first"; todo.md repeats the order.
- T6: Tests for days 3 and 4, due on `as_of`, settled, part-paid, exact remainder, a third payment of 1, unknown ids.
- T7: Blocked section names the unknown columns and date format, Bu Sari, the `effective_due_date` seam, a later `--holidays` option and the weekend rule.
- T8: Real unittest command from repo root; a worked example for `--as-of 2026-04-05` with full expected output (verified correct).
- U1: Task 1 names files and the tests to add but gives no assertion code.
- U2: No code for tests, so a developer must write all assertions; routine bodies are not transcribed.
- U3: Risks and Mitigations table ties each risk (rounding, 3.9 dates, abs, atomic save) to a task or test.
- U4: Reply gives location, R1-R7 ready, R8 blocked on the sample, expected report figures to check, no build claims.
- U5: No check is reported as run; facts match the repo.

## Differences that decided the scores

- T3 (red before green): A and C give exact RED commands with specific expected failures; B gives short generic ones; D has no failing run before the change (0).
- T2 and U1 (tests as code): A and C write assertions as code for every behaviour task; B writes code for fee and days late only; D describes tests in prose only.
- T8: D and C give concrete end-to-end outputs and B gives one for `arrears`; A's hand run on `data/loans.json` is vague.
- U2: C transcribes most of the implementation (`arrears.py`, `_cmd_arrears`, `_cmd_pay`), so code outweighs decisions.
- U3: C has no risk list tied to tasks; A, B and D do.
- F5: B never names `run_cli` or `write_data`.
- T5: B has no explicit shared-file sequencing for `cli.py` and `test_cli.py`; A, C and D do.
- Equal on all other criteria: all four runs found the `days_between` trap, handled old files, fixed the fee in integers, and left R8 as a blocked item with a seam.
