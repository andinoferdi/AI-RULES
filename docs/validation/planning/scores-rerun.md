# Blind scores after the T8 fix: planning trial

A fresh grader, a new shuffle and the patched candidate (run-5); the three baseline runs are
the same files as in [scores.md](scores.md). Grader output, unchanged except this header.
Letter mapping: A = Addy `planning-and-task-breakdown` (run-2), B = candidate after the T8 fix
(run-5), C = obra `writing-plans` (run-1), D = current `andino-planning` (run-3).

# Scores

| ID | A | B | C | D |
|---|---|---|---|---|
| F1 | 2 | 2 | 2 | 2 |
| F2 | 2 | 2 | 2 | 2 |
| F3 | 2 | 2 | 2 | 2 |
| F4 | 2 | 2 | 2 | 2 |
| F5 | 2 | 2 | 2 | 2 |
| F6 | 2 | 2 | 2 | 2 |
| F7 | 2 | 2 | 2 | 2 |
| T1 | 2 | 2 | 2 | 2 |
| T2 | 1 | 2 | 1 | 2 |
| T3 | 0 | 2 | 1 | 2 |
| T4 | 2 | 2 | 2 | 2 |
| T5 | 2 | 2 | 1 | 2 |
| T6 | 2 | 2 | 2 | 2 |
| T7 | 2 | 2 | 2 | 2 |
| T8 | 1 | 2 | 1 | 1 |
| U1 | 1 | 2 | 2 | 2 |
| U2 | 2 | 2 | 2 | 1 |
| U3 | 2 | 2 | 2 | 1 |
| U4 | 2 | 2 | 2 | 2 |
| U5 | 2 | 2 | 2 | 2 |
| Total | 35 | 40 | 36 | 37 |

## Evidence

All four runs: F1 files.txt shows only plan files (A also todo.md). Fixture numbers checked by hand: A worked example (as-of 2026-04-05: 85/54/26/11/5 days, totals Rp 1.833.333 / Rp 136.333), B and D (as-of 2026-04-10: 90/59/31/16/10 days, fees 21.666, 10.500, 15.166, 13.000, totals) and C (as-of 2026-03-20 and 03-30, totals 94.000 and 117.333) are all correct; no wrong expected value found in any run.

### A
- F2 "Ground rules" lists 3.9, stdlib, int, old data; applied in Task 1 old-file criterion and integer fee formula. F3 worked example, Task 4 acceptance and Task 3 bullets carry all texts and sort key. F4 formula plus 14000/40000/3333/0 in Task 2. F5 uses format_rupiah, parse_rupiah, run_cli/write_data, missing-file message. F6 "not dates.days_between (abs)"; due on/after as_of case. F7 Task 1 loads without field, round trip.
- T1 R1-R7 owned, R8 "Blocked". T2 tests are bullets in prose (values given), no assertion code. T3 no run-before-change step, only "Run the full suite". T4 days_late/late_fee/build_report consistent. T5 "Dependencies:" per task, "build after 3". T6 days late 4, due on as_of, settled not listed, exact settle, int return. T7 "Blocked: R8" with effective_due_date seam. T8 real unittest command and worked example, but no pay end-to-end run with expected output at the end.
- U1 Task 1 has file and command but test only in prose. U2 stubs only, bodies left out. U3 Risks table tied to tasks. U4 reply says plan location, what is blocked, 6 decisions. U5 no wrong facts.

### B
- F2 Global Constraints plus old-file test and D-e integer formula. F3 all texts in test code and T5 output. F4 `test_fee_table` four rows, `test_fee_cap_rounds_down` 333333. F6 `test_future_due_not_late`, due-today test, "do not use dates.days_between". F7 `test_old_file_loads_paid_amount_zero`, `test_paid_amount_round_trip`.
- T1 Coverage table R1-R8. T2 assertion code in every task. T3 each task has RED command with expected failure text (e.g. "AssertionError: 0 != 14000") and GREEN counts (11/19/23/28), all verified against counts. T4 Interfaces block per task, consistent. T5 Execution Board with Depends on, "T3 and T4 share cli.py". T6 3/4-day, due-today, settled, missing file, bad amount, cap rounding. T7 D1 lists missing columns, format, provider, what proceeds, `holidays` seam, T6. T8 T5 runs arrears and pay on a copy with exact outputs including totals 1.733.333/145.666.
- U1 NEXT ACTION gives file, test, command. U2 code for tests and decisions, routine bodies left. U3 Review Focus with tests plus Risks table. U4 reply lists sample questions, ready vs blocked. U5 "Not run - planned checks only".

### C
- F2-F7 as A: constraints, `parse_strict` task, `late_fee(333333, 5)==3333`, `days_late` "not dates.days_between", missing-paid_amount test and round trip. F3 outputs verbatim in test bullets.
- T1 "Self-Review" maps R1-R7, R8 excluded/blocked. T2 code for store, fee and days late; CLI/pay tests as prose bullets with exact output. T3 steps give commands, "Expected: FAIL (paid_amount not defined)" but Task 4 only "new tests FAIL". T4 consistent names (`overdue_amount`, `late_installments`). T5 sequential but no explicit dependency field, shared cli.py not discussed. T6 many cases (4 days, due on as_of, overpaid, missing file, bad amount, settle). T7 "Not in this plan: R8" with single due-date seam, names missing columns/format. T8 real commands, final run is arrears only, no pay end-to-end run.
- U1 Task 1 test code and command. U2 good proportion. U3 Review Focus tied to tasks. U4 reply covers R8 request and decisions. U5 no wrong facts.

### D
- F2-F7 as above (constraints, `test_late_fee_table`, `test_legacy_installment_loads_with_zero_paid`, abs trap in Baseline and docstring). F3 exact lines in test code.
- T1 Coverage table, D1/T6 for R8. T2 code throughout. T3 RED commands with expected errors per task, test counts 11/17/22/31 verified. T4 Interfaces consistent. T5 Execution Board with order and "serialize". T6 3/4 boundary, due today, settled, missing file, bad amount, exact settle. T7 D1 six questions, T6 rule and `next_working_day` seam. T8 manual run says "Read it for sense; the exact numbers are covered by the tests" (vague); manual pay step gives partial expected output.
- U1 full first-task code and command. U2 full bodies of arrears.py, `_cmd_arrears`, `_cmd_pay` transcribed; code is most of the 39 KB plan. U3 no dedicated risk list, only Decisions Log and Known Limitations. U4 reply gives ready/blocked, asks for sample and two R8 questions. U5 reply states only the baseline run and that new tests are not run.

## Differences that decided the scores
- B alone has a final end-to-end task running both `arrears` and `pay` on concrete data with exact outputs (T8), and its tasks name the failure expected before each change.
- A has no failing run before the change in any task (T3 0), and its tests are prose bullets, not code (T2 1, U1 1).
- C gives expected failures only briefly, has no explicit dependencies (T5 1), and tests the commands in prose (T2 1).
- D transcribes complete implementations of `arrears.py` and the command handlers (U2 1) and has no risk list tied to tasks (U3 1).
- All four handled the abs trap, integer fee arithmetic, old files and R8 honestly; no run changed source.
