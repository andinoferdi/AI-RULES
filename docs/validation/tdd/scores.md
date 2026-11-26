# Blind grading, first candidate (v1)

Grader: one Claude Code subagent, Sonnet 5.5, effort medium, given only the rubric, the fixture and folders A-F. Its output is reproduced unchanged below. Mapping, revealed after grading: A obra, B no skill, C Matt, D candidate v1, E Addy, F current andino-tdd.

# Scores (blind trial, runs A-F)

Evidence references: T# = transcript step, checks = checks.txt. No run showed a Skill, slash command or subagent call.

## A
| Criterion | Score | Evidence |
| --- | --- | --- |
| F1 | 1 | T4 writes tests for both rules at once, sees 9 failures, T5 implements both together. |
| F2 | 2 | T4 `AssertionError: 5000 != 0`, `8500 != 4500`, `45000 != 22500`; all 9 failures are FAIL, none ERROR (checks baseline). |
| F3 | 2 | Literals in T4 (`4_500`, `2_500`, `22_500`, receipt strings). |
| F4 | 2 | Tests use `fee_for_stay` and `close_ticket` (T4 receipt tests); no private helper. |
| F5 | 2 | Only `FixedClock` and `RecordingSms`; assertions on fee and SMS tuple. |
| F6 | 2 | 15:00 free and 15:01 = 5.000; 1h30 car 8.500 to bike 4.500; 20 h = 20.000. |
| F7 | 2 | All task1 behaviour lines OK; diff = two rules, tests, README tariff text. |
| B1 | 2 | T6 runs the reporter's command before any edit: PPN Rp 10.998 / Total Rp 110.997. |
| B2 | 2 | T7 `10998 != 11000` for `test_invoice_0412_totals`, fix, then only footer fails. |
| B3 | 2 | Literals 11_000, 110_999, 17. |
| B4 | 2 | All task2 behaviour lines OK. |
| B5 | 2 | `ppn([(1,150)]) == 17` (T7). |
| B6 | 2 | Full `run_tests.py` after fix (T7); reply names INV-77, footer untouched. |
| G1 | 2 | checks: "Production code changed ... no"; reply "already correct". |
| G2 | 2 | T16 normalisation temporarily reverted (3 variants), 16/13/16 failures, restored; checks show failures before ACC-212; git status only test file. |
| G3 | 2 | Through `register` + `FakeMailer`, all case/space variants, `DuplicateEmail`; no `_normalize_email` call. |
| Q1 | 2 | `scripts/test.py`, `run_tests.py`, `unittest discover -s tests -t .` each with a final full run (T5, T7, T16). |
| Q2 | 1 | Replies are clear and match transcript but give no commands/results and never say failing-before for tasks 1 and 2. |
| Q3 | 2 | files.txt shows only intended files; backups removed (T16 git status). |

## B
| Criterion | Score | Evidence |
| --- | --- | --- |
| F1 | 0 | T3 writes production code and tests in the same step; no failing test ever seen. |
| F2 | 0 | T3 first run is already `OK`; checks show baseline fails only post hoc. |
| F3 | 2 | Literals (`4_500`, `20_000`, `22_500`). |
| F4 | 2 | `fee_for_stay` and `close_ticket` receipt tests (`assertIn("biaya Rp 4.500.")`). |
| F5 | 2 | Only clock and SMS doubles. |
| F6 | 2 | 15 min vs 15 min 1 s; 2 h bike 4.500; 20 h cap 20.000. |
| F7 | 2 | All lines OK; README only extra. |
| B1 | 0 | Reporter's command first run in T5 after the fix; never run before the edit. |
| B2 | 1 | Tests exist but written with the fix in T5; never seen failing. |
| B3 | 2 | Literals. |
| B4 | 2 | All task2 lines OK. |
| B5 | 2 | `ppn([(1,150)]) == 17`. |
| B6 | 2 | T5 full suite, footer fails; reply names INV-77, footer untouched. |
| G1 | 2 | checks: unchanged; reply says code works. |
| G2 | 2 | T7 normalisation removed in place, failures seen, restored (`ls ..` clean); checks show failure before ACC-212. |
| G3 | 2 | `register` with `Ana@Mail.example ` then `ana@mail.example` and `  ANA@MAIL.EXAMPLE`. |
| Q1 | 2 | Correct command in every repo, final full run each. |
| Q2 | 1 | Clear replies, no commands/before-after; says "tested" for task 1 although no red seen (not contradicted). |
| Q3 | 2 | Clean files.txt; backups removed. |

## C
| Criterion | Score | Evidence |
| --- | --- | --- |
| F1 | 1 | T4 all tests for both rules, 7 failures; T5 implements both together. |
| F2 | 2 | T4 `5000 != 0`, `8500 != 4500`; all FAIL (no ERROR) in checks baseline. |
| F3 | 2 | Literals. |
| F4 | 2 | `fee_for_stay` + `close_ticket` receipt tests. |
| F5 | 2 | Only clock and SMS doubles. |
| F6 | 2 | 15 vs 15:01; 1h30 bike 4.500; 20 h cap. |
| F7 | 2 | All lines OK; README only extra. |
| B1 | 1 | Reporter's command first run in T8 after the fix; bug seen only via failing new tests. |
| B2 | 2 | T8 new tests listed FAIL before fix, pass after (only footer fails). Assertion text not shown, but FAIL not ERROR. |
| B3 | 2 | Literals. |
| B4 | 2 | All lines OK. |
| B5 | 2 | `ppn([(1,150)]) == 17`. |
| B6 | 2 | Full suite run; reply names INV-77. |
| G1 | 2 | Unchanged; reply says fine. |
| G2 | 2 | T10 two mutations, failures seen, restored, status only test file. |
| G3 | 2 | `register`, both orders, caps and trailing space, FakeMailer count. |
| Q1 | 2 | Correct commands, final full run each. |
| Q2 | 1 | Same shape as A: no commands, no failing-before in tasks 1 and 2. |
| Q3 | 2 | Clean. |

## D
| Criterion | Score | Evidence |
| --- | --- | --- |
| F1 | 2 | T4-T6 grace: test, `5000 != 0`, implement, pass; T7-T8 motorbike tests written after, `40000 != 20000`, then implement. |
| F2 | 1 | Billing tests red with assertions (T4, T7), but the `close_ticket` tests (and motorbike-grace test) were first run after the production change; their failure was shown only by reverting (T9). |
| F3 | 2 | Literals. |
| F4 | 2 | `fee_for_stay` and `close_ticket` tests (T8). |
| F5 | 2 | Only clock and SMS doubles. |
| F6 | 2 | 15:00/15:01; 1h30 to 4.500; 20 h cap. |
| F7 | 2 | All OK; README only extra. |
| B1 | 2 | T10 runs render before editing: 10.998 / 110.997. |
| B2 | 2 | T11 `10998 != 11000`; T12 pass. |
| B3 | 2 | Literals. |
| B4 | 2 | All OK. |
| B5 | 2 | 150 to 17 and 50 to 6. |
| B6 | 2 | T12 full suite; reply names INV-77, footer untouched. |
| G1 | 2 | Unchanged; reply says so. |
| G2 | 2 | T14 temporary worktree of pre-ACC-212 commit, 5 failures, worktree removed (`git worktree list` one entry); pass on current. |
| G3 | 2 | `register`; caps, spaces, and combined `Ana@Mail.example ` case; no private call. |
| Q1 | 2 | Correct commands, final full run each. |
| Q2 | 1 | Better than others (task 2 shows command output, task 3 says failing-before) but task 1 reply gives no before/after; borderline 2. |
| Q3 | 2 | Clean; worktree and backups removed. |

## E
| Criterion | Score | Evidence |
| --- | --- | --- |
| F1 | 1 | T6 all tests for both rules red (7 failures), T7 both implemented together. |
| F2 | 2 | T6 seven tests FAIL (not ERROR) before T7. |
| F3 | 2 | Literals. |
| F4 | 2 | `fee_for_stay` and `close_ticket`; no private helper tested. |
| F5 | 2 | Only clock and SMS doubles. |
| F6 | 2 | 15 min vs 15 min 1 s; 1h30 to 4.500; 20 h cap. |
| F7 | 1 | All lines OK but unrequested `NEW_TARIFF_FROM` date switch plus extra old-tariff test and `_car_fee` helper (T7). |
| B1 | 2 | T9 reporter's command before edit: 10.998 / 110.997. |
| B2 | 2 | T10 three tests FAIL, fix, pass. |
| B3 | 2 | Literals. |
| B4 | 2 | All OK. |
| B5 | 2 | 150 to 17, 50 to 6. |
| B6 | 2 | Full suite; reply names INV-77. |
| G1 | 1 | checks say no behaviour change, but task3.diff shows whole-file rewrite of `accounts/service.py` (line endings after `git checkout`); no behaviour change. |
| G2 | 1 | Failing seen with mutations (T15), restored via `git checkout`, but that left a trace in `accounts/service.py` (files.txt `M accounts/service.py`). |
| G3 | 2 | `register`, both orders, caps and space. |
| Q1 | 2 | Correct commands, final full run each. |
| Q2 | 1 | Clear replies, no commands; reply says sign-up code "unchanged" though the file shows as modified. |
| Q3 | 1 | One stray item: `accounts/service.py` rewritten (line endings). |

## F
| Criterion | Score | Evidence |
| --- | --- | --- |
| F1 | 1 | T6 all tests red first, T7 both rules together. |
| F2 | 2 | T6 six FAIL (not ERROR). |
| F3 | 2 | Literals. |
| F4 | 2 | `fee_for_stay` and `close_ticket` tests. |
| F5 | 2 | Only clock and SMS doubles. |
| F6 | 2 | 15/15:01; 1h30 to 4.500; 20 h cap. |
| F7 | 2 | All OK; README only extra. |
| B1 | 1 | Reporter's command first run in T11 after the fix; symptom seen only via failing new tests (T10). |
| B2 | 2 | T10 `test_invoice_0412_totals` FAIL, T11 pass. |
| B3 | 2 | Literals. |
| B4 | 2 | All OK. |
| B5 | 2 | 150 to 17. |
| B6 | 2 | Full suite T11; reply names INV-77. |
| G1 | 2 | Unchanged. |
| G2 | 2 | T14 mutations, 2 failures each, restored, status only test file. |
| G3 | 2 | `register`, both orders, `Ana@Mail.example ` and `  ANA@MAIL.EXAMPLE`. |
| Q1 | 2 | Correct commands, final full run each. |
| Q2 | 1 | Same shape as A/C: no commands or before/after in task 1 and 2 replies. |
| Q3 | 2 | Clean. |

## Summary
| Criterion | A | B | C | D | E | F |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | 1 | 0 | 1 | 2 | 1 | 1 |
| F2 | 2 | 0 | 2 | 1 | 2 | 2 |
| F3 | 2 | 2 | 2 | 2 | 2 | 2 |
| F4 | 2 | 2 | 2 | 2 | 2 | 2 |
| F5 | 2 | 2 | 2 | 2 | 2 | 2 |
| F6 | 2 | 2 | 2 | 2 | 2 | 2 |
| F7 | 2 | 2 | 2 | 2 | 1 | 2 |
| B1 | 2 | 0 | 1 | 2 | 2 | 1 |
| B2 | 2 | 1 | 2 | 2 | 2 | 2 |
| B3 | 2 | 2 | 2 | 2 | 2 | 2 |
| B4 | 2 | 2 | 2 | 2 | 2 | 2 |
| B5 | 2 | 2 | 2 | 2 | 2 | 2 |
| B6 | 2 | 2 | 2 | 2 | 2 | 2 |
| G1 | 2 | 2 | 2 | 2 | 1 | 2 |
| G2 | 2 | 2 | 2 | 2 | 1 | 2 |
| G3 | 2 | 2 | 2 | 2 | 2 | 2 |
| Q1 | 2 | 2 | 2 | 2 | 2 | 2 |
| Q2 | 1 | 1 | 1 | 1 | 1 | 1 |
| Q3 | 2 | 2 | 2 | 2 | 1 | 2 |
| Total /38 | 36 | 30 | 35 | 36 | 32 | 35 |

## Judgement calls
- F2 for D (1): billing tests were seen red before the change, but the `close_ticket` tests and the motorbike-grace test were first run only after the production change (failure shown later by reverting, T9). Strict reading of "every new test ... before the production change" gives 1; a lenient reading gives 2.
- F1 for D (2): the two rules have separate cycles, but the four motorbike tests were run red together as one batch and the ticket tests came after; the rubric's cycle wording fits, a strict grader might give 1.
- F7 for E (1): the 1 December date gate is unrequested (Sari asked for the rules "from 1 December", so it could be read as in scope); behaviour lines are all OK.
- G1/G2/Q3 for E: checks.txt says production code unchanged against ACC-212, but task3.diff and files.txt show `accounts/service.py` fully rewritten (line endings) after `git checkout`. I scored it as a behaviour-neutral change (G1=1), a trace left behind (G2=1) and one stray item (Q3=1). Reading checks.txt alone would give 2/2/2, a 3-point swing.
- B1 for C and F (1): reporter's command run only after the fix; bug seen only through failing new tests. A has it at 2 and B at 0 (never seen at all).
- B2 for C (2): transcript shows only `... FAIL` lines (grep-filtered), not the assertion text; FAIL (not ERROR) taken as an assertion failure.
- Q2 (all 1): no run's replies give commands with before/after results for all three tasks, and none name tests individually. D's replies are the strongest (task 2 command output, task 3 failing-before count) and a lenient grader could give D 2.
- F7 for A-D, F (2): README tariff edit counted as part of the change, not an unrequested feature.
- Q3 for A, B, D, E, F: several runs tried a backup to `/tmp` or the drive root outside the run folder (`cp ... /tmp/x.bak 2>/dev/null || ...`); not visible in files.txt, not scored.
