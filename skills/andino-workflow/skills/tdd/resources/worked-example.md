# Worked example: two renewal rules and a regression guard

A small library repository (`loans/desk.py`, `tests/test_desk.py`, Python `unittest`). The
outputs below are copied from a real run of these steps.

The request, from the head librarian:

> A loan can be renewed at most twice; refuse the third renewal. Also refuse a renewal while
> another member has a hold on the book. And last month Dani fixed renewals so they add 14 days
> to the due date instead of to today (LIB-31), but nobody wrote a test for it. Please add one.

## Prerequisites

The README names `python -m unittest` (focused: `python -m unittest tests.test_desk.RenewTest.<name>`).
The suite before any change: `Ran 1 test ... OK`. `git log --oneline` shows the fix commit and
the commit before it:

```text
1329a4a Renew from the due date, not from today (LIB-31)
270e4b0 Lend and renew books
```

## Gate 1: the slice list

Written before any test:

| # | Behavior | Seam | Example (worked by hand) | Break |
| --- | --- | --- | --- | --- |
| 1 | The third renewal is refused | `LoanDesk.renew` | lend, renew, renew -> third renew raises `RenewalRefused` | the limit check is missing or allows three |
| 2 | No renewal while a hold waits | `LoanDesk.place_hold`, `LoanDesk.renew` | lend, hold placed -> renew raises `RenewalRefused` | the hold check is missing |
| 3 | Renewal extends from the due date (LIB-31), already works | `LoanDesk.renew` | lent 2 March (due 16 March), renewed 10 March -> due 30 March | the due date counts from today (24 March) |

Rows 1 and 2 are two rules, so two rows. Row 1's example also covers its boundary: the first two
renewals succeed.

## Gate 2 and gate 3, row 1

Test `test_third_renewal_is_refused`; predicted failure: `RenewalRefused not raised`.

```text
$ python -m unittest tests.test_desk.RenewTest.test_third_renewal_is_refused
AssertionError: RenewalRefused not raised
Ran 1 test in 0.002s
FAILED (failures=1)
```

Green: `MAX_RENEWALS = 2` and, at the top of `renew`,
`if loan.renewals >= MAX_RENEWALS: raise RenewalRefused("renewal limit reached")`. The same test
passes, then the module: `Ran 2 tests ... OK`. Row 2's test is written only now.

## Gate 2 and gate 3, row 2

Test `test_renewal_is_refused_while_a_hold_waits`; predicted failure: `RenewalRefused not raised`.

```text
$ python -m unittest tests.test_desk.RenewTest.test_renewal_is_refused_while_a_hold_waits
AssertionError: RenewalRefused not raised
Ran 1 test in 0.002s
FAILED (failures=1)
```

Green: `if loan.item in self.holds: raise RenewalRefused("another member has a hold on this item")`.
The test passes; the module: `Ran 3 tests ... OK`.

## Gate 4, row 3

Test `test_renewal_extends_from_the_due_date_not_from_today` passes on its first run, as an
`already works` row should. It is proved against the commit before LIB-31:

```text
$ git worktree add ../pre-lib31 270e4b0
HEAD is now at 270e4b0 Lend and renew books
(copy tests/test_desk.py into ../pre-lib31/tests/)
$ python -m unittest tests.test_desk.RenewTest.test_renewal_extends_from_the_due_date_not_from_today
AssertionError: datetime.date(2026, 3, 24) != datetime.date(2026, 3, 30)
FAILED (failures=1)
$ git worktree remove --force ../pre-lib31
```

`git worktree list` shows only the main tree; `git status --short` shows ` M loans/desk.py` and
` M tests/test_desk.py`, the change and its tests.

## Gate 5 and gate 6

No refactor: `renew` holds two guard clauses and the update. Full suite: `Ran 4 tests ... OK`,
against `Ran 1 test ... OK` before; no failures old or new. The diff holds the two guard clauses,
the constant and three tests.

## The reply

> Renewals now follow both rules: a loan can be renewed twice, the third request is refused,
> and a renewal is refused while another member has a hold. Dani's LIB-31 fix now has a test,
> and that test fails on the code from before the fix, so it would catch the bug coming back.
>
> **Test record**
>
> ```text
> Test commands: focused python -m unittest tests.test_desk.RenewTest.<name>; full suite python -m unittest
> Slices:
>   1. third renewal refused | seam LoanDesk.renew | example lend, renew x2 -> third raises
>      red: test_third_renewal_is_refused -> AssertionError: RenewalRefused not raised
>      green: MAX_RENEWALS = 2 guard in renew -> Ran 2 tests OK
>   2. no renewal while a hold waits | seam place_hold, renew | example hold -> renew raises
>      red: test_renewal_is_refused_while_a_hold_waits -> AssertionError: RenewalRefused not raised
>      green: hold guard in renew -> Ran 3 tests OK
>   3. renewal extends from the due date (LIB-31) | seam LoanDesk.renew | due 16 Mar, renew 10 Mar -> 30 Mar
> Proof for tests that passed at once: row 3 fails on 270e4b0 (2026-03-24 != 2026-03-30);
>   passes on current code; restored: worktree removed, status shows only desk.py and test_desk.py
> Refactor: none
> Verification: suite Ran 4 tests OK (1 before, no failures)
> Not done or not verified: whether a hold placed by the borrower themself should block renewal;
>   the rule as written blocks it
> ```

## What the anti-pattern would have looked like

All three tests written first and run once (three failures, or two failures and a pass), then
both rules implemented together. The suite ends green, but no run ties a red to one change, and
the LIB-31 test, which never failed, proves nothing until gate 4.
