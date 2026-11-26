# Scores

Blind grading on 2026-11-26 by one Sonnet 5.5 subagent at medium effort, from the rubric, the
fixture with its oracle and the four shuffled output folders. Mapping, revealed after grading:
A = unguided control, B = candidate, C = Addy, D = current skill. The grader's tables and notes
follow as returned.

Oracle summary (the grader's own runs): `tests_pass` and `original_tests_unchanged` true for all
four; every orders family (including `random` 300 and `tax` 42), `export` and every users family
0 mismatches for all four; `changed_files` is `["orders/pricing.py"]` for all four; only B has
`added_files` (`["tests/test_pricing_characterization.py"]`); `deleted_files` empty; `tax.py`
unchanged in all four; `protected_region_identical` false for A and C, true for B and D;
`protected_region_same_ignoring_indent` true for all four. The runners' own checks (20,000
random inputs, 43 Node cases, 1,026 combinations) were not re-run; they are scored on how they
are reported.

## Task 1: behavior (T1-T7)
| ID | A | B | C | D |
|---|---|---|---|---|
| T1 | 2 - tests_pass true, originals unchanged | 2 - same, 24 tests OK | 2 - same | 2 - same |
| T2 | 2 - all named families 0 mismatches, random 0 | 2 - same | 2 - same | 2 - same |
| T3 | 2 - credit 0; comment "(INC-212)" | 2 - credit 0; "# INC-212: credit lines can push the total below zero" | 2 - credit 0; comment names INC-212 | 2 - credit 0; "# INC-212: the payment provider rejects negative charges" |
| T4 | 2 - shipping 0; "Free shipping is decided on the subtotal before discounts" kept | 2 - shipping 0; comment kept above the constants | 2 - shipping 0; comment kept | 2 - shipping 0; comment kept in `_shipping` |
| T5 | 2 - audit_error 0 | 2 - audit_error 0 | 2 - audit_error 0 | 2 - audit_error 0 |
| T6 | 2 - identical false, same_ignoring_indent true (block dedented) | 2 - identical true | 2 - identical false, same_ignoring_indent true | 2 - identical true |
| T7 | 2 - export 0; signature unchanged | 2 - same | 2 - same | 2 - same |

## Task 1: quality (T8-T13)
| ID | A | B | C | D |
|---|---|---|---|---|
| T8 | 2 - guard clauses (`if order is None: raise`), flat function | 2 - two nested `if`s kept; comment says the block must keep its indentation, so surrounding code keeps its nesting | 2 - guard clauses, flat | 2 - two levels kept around the block; report states the reason |
| T9 | 2 - `subtotal`, `line`, `shipping`, `discount`, `tax`; `data`, `tmp`, `f`, `s` gone; `res` kept | 2 - `subtotal`, `line`, `discount`, `_shipping`, `tax`; `res` kept | 2 - same style; `res` kept | 2 - `subtotal`, `discount`, `total`, `tax`, `line`; `res` kept only in `price_order` |
| T10 | 1 - `import json` and `import math` still there; flat-rate comment, loop comment and `else` after raise removed; the redundant `else` in `LoyaltyDiscountStrategy` removed; both reason comments kept | 2 - imports, flat-rate block, loop comment and `else` branches gone; both reason comments kept | 2 - all removed; both comments kept | 1 - `json` and `math` imports kept and `else: return Decimal("0")` kept; flat-rate and loop comments gone; comments kept |
| T11 | 1 - classes kept; report: "SYSTEM.md says nothing imports the classes... larger, separate change" | 2 - replaced by `_loyalty_discount`; SYSTEM.md and a repository grep cited | 2 - replaced by `_loyalty_discount`; "Nothing imports the discount classes (`SYSTEM.md`)" | 1 - classes kept with a stated reason ("a named domain concept"); SYSTEM.md checked |
| T12 | 2 - only a simple one-level conditional expression for shipping | 2 - no clever constructs | 2 - one simple conditional expression | 2 - none |
| T13 | 0 - no new test file | 2 - `test_pricing_characterization.py` has 19 tests (clamp, audit on failure paths, shipping boundary, tax band, error messages), run green on the old code first | 0 - no new test file | 1 - no test file in the repo; `out/task1/check/diff_check.py` is a saved differential harness over 1026 cases against a copy of the original |

## Task 2: pasted snippet (J1-J5)
| ID | A | B | C | D |
|---|---|---|---|---|
| J1 | 2 - code and reply delivered | 2 | 2 | 2 |
| J2 | 2 - async_boundary 0 (`async` kept, `await` dropped) | 2 - 0 | 2 - 0 | 2 - 0 (`return await` kept) |
| J3 | 2 - all four families 0 | 2 - all 0 | 2 - all 0 | 2 - all 0 |
| J4 | 2 - all four spots clearer (early returns, filter/map, single return, `\|\| 0` counter) | 2 - `roleBadge`, `displayName`, merged condition in `activeEmails`, `?? 0` in `summarize` | 2 - all four | 2 - all four |
| J5 | 1 - "quick comparison... on a handful of sample users" is vague; says the callers were not seen | 2 - 43 cases named, Node run on both versions; names the TypeError message difference and the unverified callers | 1 - says it could not run it against real data; no check of its own described, only reasoning about `1` and `"yes"` | 2 - sample users named; "a spot check, not a test suite"; callers unseen |

## Task 3: `tax.py` (X1-X2)
| ID | A | B | C | D |
|---|---|---|---|---|
| X1 | 2 - tax 0 mismatches | 2 | 2 | 2 |
| X2 | 2 - file untouched; report cites RSTS-2024 steps 4.1-4.4 | 2 - untouched; reason given | 2 - untouched; reason given | 2 - untouched; SHA-256 before and after |

## Quality (Q1-Q3)
| ID | A | B | C | D |
|---|---|---|---|---|
| Q1 | 1 - what and why per change, but one global check; the reading problem is only implied | 2 - reading problem, change, behavior kept and checks (24 tests, hashes) given | 1 - same pattern as A | 2 - reading problem, change, behavior kept; commands with results (5 tests OK, 1026 cases) |
| Q2 | 1 - claims the rounding block is "byte-for-byte unchanged", but the oracle shows it is not (dedented); `include_tax == True` became `if include_tax` without flagging the semantic change | 2 - the hash claim matches the oracle; the 19-test count is correct | 1 - "untouched, character for character" is false (identical false); the `include_tax` change is flagged | 2 - hash claim matches the oracle (identical true) |
| Q3 | 2 | 2 - added file is a test only | 2 | 2 (the extra files are under `out/`, outside the repo) |

## Totals
| Folder | Task 1 (T1-T13, /26) | Task 2 (J1-J5, /10) | Task 3 (X1-X2, /4) | Quality (Q1-Q3, /6) | Total /46 |
|---|---|---|---|---|---|
| A (unguided) | 22 | 9 | 4 | 4 | 39 |
| B (candidate) | 26 | 10 | 4 | 6 | 46 |
| C (Addy) | 24 | 9 | 4 | 4 | 41 |
| D (current) | 23 | 10 | 4 | 6 | 43 |

## Judgement calls (grader's notes)
- T8 (B, D): neither has classic guard clauses at the end, but the rubric allows nesting around
  the protected block with the reason stated, and both state it. A stricter reading would give 1.
- T13 (D): 1 because the harness was saved but is not a test file in the repo. A strict reading
  gives 0; a generous one gives 2. A and C also ran differential checks but did not keep them.
- T11 (A, D): both kept the classes with a stated reason, which scores 1.
- T10 (A, D): 1 each; neither removed the unused imports.
- J5 (A, C): A could be 2 if "quick comparison" is accepted as a real run; C could be 0 because
  it describes no check of its own.
- Q1 (A, C vs B, D): every report gives its checks globally rather than per change; 2 where the
  reading problem and the command with its result are explicit, 1 where they are implied.
- Q2 (A, C): A has two lapses (the false byte-for-byte claim and the unflagged `include_tax`
  change), so 0 is arguable; C has one. The oracle does not test `include_tax` with truthy
  values other than `True`, so that change did not affect T2 or T7.
- T6 (A, C): 2 only because of the amendment; their reports call the block unchanged, which is
  not literally true.
