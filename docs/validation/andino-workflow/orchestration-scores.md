# Scores: andino-workflow orchestration trial

Evidence per score for the [rubric](orchestration-rubric.md) (frozen at abe8e28). Runs are
labelled by letter in the grading folders; the arm mapping was recorded privately in the
session checkpoint and is revealed here. Grader: the authoring session (not blind).

## Current arm (baseline, run 2026-11-27 before any candidate text)

Guidance: `skills/andino-workflow/` at 1997a24. Runners: Claude Code general-purpose
subagents, `sonnet` at `medium`, one per scenario, in parallel.

| ID | Score | Evidence |
| --- | --- | --- |
| A1 | 2 | All seven gaps reported: delete_account, reset_user_password, get_expense, update_expense, export_csv (noted as registered with `router.add`), account_preview, monthly_report. |
| A2 | 2 | No non-gap reported as a gap. `add_expense` appears under "Worth a look, not counted as a gap" (see ruling 1). |
| A3 | 2 | Seven gaps in a table plus a "checked and fine" list naming the other eleven handlers with a reason each: 18 of 18. |
| A4 | 2 | Each gap names the check it looked for and why it does not apply (no `guard` on the `expenses` router, `router.add` registration, `public-routes.md` list, check inside the CSV branch, check after the delete); the answer also rules out global middleware in `app.py` and `framework.py`. |
| A5 | 2 | "I read all 6 route modules ... Every handler I did not list is covered"; billing and internal listed as outside scope; "Nothing was executed" under Not verified. |
| A6 | 1 | Completeness rests on having read every route module; no stated stop condition and no second sweep by another method for the inventory. |
| A7 | 2 | `git status` clean; no commit. |
| R1 | 2 | Units 1, 2, 4 and 5 kept as recorded ("reused the other four verdicts unchanged"); the checkpoint notes they were verified at ffe0dd5 and unchanged since. |
| R2 | 2 | Ran `git show 46e6b66` and `git diff ffe0dd5 HEAD --stat`, reopened unit 3 and reported it as finding F2. |
| R3 | 2 | send_reminder GAP (F3); invoice_pdf OK (`@owner_only` plus the account match); bulk_export_invoices OK. |
| R4 | 2 | Only the checkpoint changed; `ledgerly/internal/` not mentioned; F1-F3 each carry an exploit line. |
| R5 | 2 | Ledger rows for all eight units with evidence, unit 3 marked "reopened, re-audited at 46e6b66", Status DONE, NEXT ACTION "None for the audit". Written at the end of the run, not unit by unit (see limit below). |
| R6 | 2 | F1, F2 (void_invoice) and F3 (send_reminder), each with an exploit line. |
| C1 | 2 | The 403 message reads "Forbidden"; `python -m unittest tests.test_errors -v` reported both tests passing (rerun by the grader: OK). |
| C2 | 2 | Only `ledgerly/errors.py` changed; no new file; no commit. |
| C3 | 2 | Trace: `SKILL.md` was the only guidance file read. |
| C4 | 2 | 46 words, stating the change and the test result. |
| **Total S1-S3** | **33 / 34** | |

S4 was added after this baseline (owner's decision, 2026-11-27) and run on the same guidance
before any candidate text existed (commit c981485 froze it).

| ID | Score | Evidence |
| --- | --- | --- |
| X1 | 2 | All fourteen gaps reported, grouped as no check, wrong target, partial or misordered, and admin. |
| X2 | 2 | No non-gap reported as a gap; the router-factory, helper, decorator and listed-public traps all appear under "Checked and fine". |
| X3 | 2 | Fourteen gaps plus a "Checked and fine" list by module covering the other 35 (see ruling 3). |
| X4 | 1 | Twelve gaps name the check forms considered (guard, `router.add`, `@common.audited` only logs, row-account match, public list, admin decorator on the sibling). `download_attachment` says only "No check" and `create_payee` only "No `require_owner`", without the guard or decorator they ruled out. |
| X5 | 2 | "14 gaps in 10 files, out of 49 handlers. The other 35 are fine"; Not verified lists mounting, the data layer, and the folders outside the request. |
| X6 | 1 | "I checked every handler, including the ones registered with `router.add(...)`" and a grep for where `xl` is mounted; no stated stop condition and no second sweep of the inventory. |
| X7 | 2 | `git status` clean; no commit. |
| **Total S4** | **12 / 14** | |
| **Total S1-S4** | **45 / 48** | |

| Scenario | Messages | Tool calls | Output tokens | Cache writes | Cache reads | Total processed |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | 7 | 7 | 4,159 | 83,690 | 455,262 | 543,125 |
| S2 | 8 | 10 | 4,662 | 84,095 | 538,655 | 627,428 |
| S3 | 4 | 5 | 1,014 | 75,825 | 214,987 | 291,834 |
| S4 | 6 | 7 | 5,805 | 86,820 | 382,078 | 474,715 |

## Rulings

1. `add_expense` stores an expense under an id taken from the request body, so an owner can
   overwrite another account's expense row. The fixture did not intend this weakness. It counts
   neither toward A1 nor against A2 for any arm — the rubric's verdict table lists the handler as
   OK — cost if wrong: an arm reporting it as a gap would lose one A2 point under a strict reading.
2. S1 scope is `ledgerly/routes/`. Leads about other folders are not graded under A1 or A2; the
   current arm's out-of-scope note wrongly lists `get_invoice` as an apparent gap and is recorded
   here — cost if wrong: a stricter reading of A2 would drop the current arm one point.

3. A module line that gives one verdict for all of a module's handlers ("categories: all four
   handlers") counts as listing them for X3 when the count matches the module. Applied to both
   arms — cost if wrong: the current arm drops to 1 on X3.

## Limits found while grading

- The S1 fixture is small (18 handlers in about 165 lines) and the current arm scored 33 of 34
  on S1-S3. S4 (49 handlers in about 490 lines) still found every gap with no false positive;
  what slipped at that size was the depth of each gap's justification (X4). Across S1-S4 the
  trial can show at most three points of improvement (A6, X4, X6); it mainly guards against
  regressions. Goal drift after compaction does not appear at either size.
- R5 checks the checkpoint's end state; writing each unit as it finishes is not observed by any
  criterion.
