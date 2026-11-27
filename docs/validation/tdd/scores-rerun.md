# Blind grading, second candidate (v2)

A fresh grader (Claude Code subagent, Sonnet 5.5, effort medium) scored the v2 run with the five unchanged baseline outputs, reshuffled. Its output is reproduced unchanged below. Mapping, revealed after grading: A no skill, B candidate v2, C Addy, D current andino-tdd, E obra, F Matt.

# Blind trial scores (runs A-F)

Step numbers are transcript step numbers of that run. "checks" = checks.txt.

## A (30/38)

| Criterion | Score | Evidence |
| --- | --- | --- |
| F1 | 0 | Step 3: tests and billing.py edited in one command, only run afterwards (14 OK); no new test ever seen failing before the change. |
| F2 | 0 | No run before the production change; first run (step 3) already passes. |
| F3 | 2 | Literals: `fee_for_stay(...) , 4_500`, `20_000`, `22_500` (step 3). |
| F4 | 2 | `fee_for_stay` and `close_ticket` receipt tests (`"biaya Rp 4.500."`); no private helper. |
| F5 | 2 | Only FixedClock/RecordingSms; assertions on fee and SMS text. |
| F6 | 2 | 15:00 vs 15:00+1s, 2 h motorbike 4_500 (4.250 up), 20 h cap 20_000. |
| F7 | 2 | All checks task1 lines OK; diff is two rules, tests, README tariff text. |
| B1 | 0 | Reporter's command first run at step 5 after tax.py was rewritten; never run before editing. |
| B2 | 1 | Step 5 writes tests and fix together; test never seen failing before the fix (fails only in checks baseline run). |
| B3 | 2 | `110_999`, `11_000`, `17`, `15`, `6` literals. |
| B4 | 2 | All task2 lines OK in checks. |
| B5 | 2 | `ppn([(1, 150)]) == 17` and `(1, 50) == 6`. |
| B6 | 2 | `python run_tests.py` after fix shows footer FAIL; reply: "known failure ... (INV-77) ... left it and the footer alone". |
| G1 | 2 | checks: "Production code changed against the ACC-212 commit: no"; reply says code works. |
| G2 | 2 | Step 7: passes, then normalisation removed -> FAIL, restored, passes; files.txt only the test changed; checks shows FAIL before ACC-212. |
| G3 | 2 | `register("Ana@Mail.example ")` then `"ana@mail.example"` and `"  ANA@MAIL.EXAMPLE"`, `DuplicateEmail`. |
| Q1 | 2 | `scripts/test.py`, `run_tests.py`, `unittest discover -s tests -t .` full runs in each repo. |
| Q2 | 1 | Replies give no commands, no failing-before for tasks 1-2, no "not verified" section; claims are backed. |
| Q3 | 2 | svc.bak removed (step 7 `ls ..` clean); files.txt only intended files. |

## B (37/38)

| Criterion | Score | Evidence |
| --- | --- | --- |
| F1 | 1 | Step 4 writes tests for both rules, all seen failing; step 5 implements both together. |
| F2 | 2 | Step 4: `5000 != 0`, `40000 != 20000`, `5000 != 2500`, `8500 != 4500`. The one-second-over test passed at once but was proven by mutation (step 6). |
| F3 | 2 | Literals (`2_500`, `4_500`, `22_500`, `"... biaya Rp 4.500."`). |
| F4 | 2 | `fee_for_stay` plus two `close_ticket` receipt tests. |
| F5 | 2 | Only FixedClock/RecordingSms. |
| F6 | 2 | 15:00 and 15:01; 1h30 -> 4_500; 20 h cap. |
| F7 | 2 | All checks OK; no unrequested code. |
| B1 | 2 | Step 7 runs the reporter's command before edits: `PPN Rp 10.998`, `Total Rp 110.997`. |
| B2 | 2 | Step 8: `AssertionError: 10998 != 11000` for `test_invoice_0412_totals`; passes at step 9. |
| B3 | 2 | Literals only. |
| B4 | 2 | All task2 checks OK. |
| B5 | 2 | `ppn([(1,150)]) == 17`, failed `16 != 17` before the fix. |
| B6 | 2 | Step 9 full `run_tests.py`; reply: "known issue INV-77 ... left it and the footer alone". |
| G1 | 2 | checks: unchanged production code. |
| G2 | 2 | Step 11: temporary worktree at 1d4d374, 3 FAIL; worktree removed, `git worktree list` clean. |
| G3 | 2 | Through `register`, "Ana@Mail.example " then "ana@mail.example". |
| Q1 | 2 | README commands, focused and full, in all three. |
| Q2 | 2 | Each reply carries a "Test record" with commands, red/green results, and "Not done or not verified"; claims match the transcript. |
| Q3 | 2 | Worktree removed; files.txt clean. |

## C (34/38)

| Criterion | Score | Evidence |
| --- | --- | --- |
| F1 | 1 | Step 6 writes all tests, 7 FAIL; step 7 implements both rules together. |
| F2 | 2 | Step 6: 7 tests FAIL (assertion failures, not ERROR); output filtered so expected/actual not shown (between 1 and 2; scored 2). |
| F3 | 2 | Literals. |
| F4 | 2 | `fee_for_stay` and `close_ticket`. |
| F5 | 2 | FixedClock/RecordingSms only. |
| F6 | 2 | 15 min vs 15 min 1 s; 1h30 -> 4_500; 20 h cap. |
| F7 | 1 | Unrequested `NEW_TARIFF_FROM = datetime(2026, 12, 1)` date switch and a test for the old tariff (step 7); all checks OK. |
| B1 | 2 | Step 9 renders 0412 before editing: `PPN 11% Rp 10.998`. |
| B2 | 2 | Step 10: `test_invoice_0412_matches_the_tax_consultant` FAIL, then passes. |
| B3 | 2 | Literals. |
| B4 | 2 | All OK. |
| B5 | 2 | 150 -> 17 and 50 -> 6, failed before the fix. |
| B6 | 2 | Full `run_tests.py`; reply names INV-77. |
| G1 | 2 | checks: "no" (but see note: task3.diff shows accounts/service.py rewritten with line endings only, from `git checkout`). |
| G2 | 2 | Step 15: no lower() and no strip() mutations FAIL, restored, OK. Step 13 error was fixed and rerun. |
| G3 | 2 | Through `register`, both orders, capitals and trailing/leading space. |
| Q1 | 2 | README commands, focused and full. |
| Q2 | 1 | No commands, no failing-before for tasks 1-2, no "not verified" section; claims backed. |
| Q3 | 1 | files.txt lists `M accounts/service.py` (CRLF-only diff from `git checkout`); one stray change. |

## D (35/38)

| Criterion | Score | Evidence |
| --- | --- | --- |
| F1 | 1 | Step 6 all tests written and 6 FAIL; step 7 implements both together. |
| F2 | 2 | Step 6: 6 FAIL (assertions). |
| F3 | 2 | Literals. |
| F4 | 2 | `fee_for_stay` and `close_ticket` (`assertIn("biaya Rp 0.")`). |
| F5 | 2 | FixedClock/RecordingSms. |
| F6 | 2 | 15:00 vs 15:00+1s; 1h30 -> 4_500; 20 h cap. |
| F7 | 2 | Checks OK. Step 7 grace-before-validation bug fixed at step 9. |
| B1 | 1 | Reporter's command not run before the edit (step 11 is after the fix); symptom first seen via the failing test only. |
| B2 | 2 | Step 10: `test_invoice_0412_totals` FAIL; passes after step 11. |
| B3 | 2 | Literals. |
| B4 | 2 | All OK. |
| B5 | 2 | 150 -> 17. |
| B6 | 2 | Full run; reply names INV-77. |
| G1 | 2 | checks: no change. |
| G2 | 2 | Step 14: mutation FAIL (no normalisation; no strip), restored, OK; step 12 error fixed first. |
| G3 | 2 | Through `register`, "Ana@Mail.example " then "ana@mail.example"; reverse with `"  ANA@MAIL.EXAMPLE"`. |
| Q1 | 2 | README commands. |
| Q2 | 1 | No commands; no failing-before for tasks 1-2; no "not verified" section. |
| Q3 | 2 | svc.bak removed; files.txt clean. |

## E (36/38)

| Criterion | Score | Evidence |
| --- | --- | --- |
| F1 | 1 | Step 4 all tests written and 9 FAIL; step 5 implements both together. |
| F2 | 2 | Step 4: `45000 != 22500`, `5000 != 0`, `8500 != 4500`. |
| F3 | 2 | Literal triples in a table (`(timedelta(...), 8_500, 4_500)`); no formula. |
| F4 | 2 | `fee_for_stay` and `close_ticket` receipt tests. |
| F5 | 2 | FixedClock/RecordingSms. |
| F6 | 2 | 15:00 vs 15:00+1s; 1h30 -> 4_500; 20 h cap in the table. |
| F7 | 2 | Checks OK. |
| B1 | 2 | Step 6 runs the reporter's command before edits: `PPN Rp 10.998`. |
| B2 | 2 | Step 7: `10998 != 11000`; passes after the fix (13 tests, only footer fails). |
| B3 | 2 | Literals. |
| B4 | 2 | All OK. |
| B5 | 2 | 150 -> 17 failed `16 != 17`. |
| B6 | 2 | Full run; reply names INV-77. |
| G1 | 2 | checks: no change. |
| G2 | 2 | Step 16: three mutations FAIL (16/13/16 failures), restored, OK; earlier import and syntax errors were fixed before the proof. |
| G3 | 2 | Through `register`, all case/space variants. |
| Q1 | 2 | README commands. |
| Q2 | 1 | No commands; no failing-before for tasks 1-2; no "not verified" section. |
| Q3 | 2 | files.txt clean. |

## F (35/38)

| Criterion | Score | Evidence |
| --- | --- | --- |
| F1 | 1 | Step 4 all tests written and 7 FAIL; step 5 implements both together. |
| F2 | 2 | Step 4: `8500 != 4500`, `5000 != 0`. |
| F3 | 2 | Literals. |
| F4 | 2 | `fee_for_stay` and `close_ticket`. |
| F5 | 2 | FixedClock/RecordingSms. |
| F6 | 2 | 15:00 vs 15:00+1s; 1h30 -> 4_500; 20 h cap. |
| F7 | 2 | Checks OK. |
| B1 | 1 | The reporter's command only run after the fix (step 8); symptom seen only via failing tests. |
| B2 | 2 | Step 8: `test_invoice_0412_tax_is_worked_out_on_the_subtotal` FAIL, then passes. |
| B3 | 2 | Literals. |
| B4 | 2 | All OK. |
| B5 | 2 | 150 -> 17. |
| B6 | 2 | Full run; reply names INV-77. |
| G1 | 2 | checks: no change. |
| G2 | 2 | Step 10: removal of trim+lower and of trim only FAIL; restored; OK. |
| G3 | 2 | Through `register`, both orders. |
| Q1 | 2 | README commands. |
| Q2 | 1 | No commands; no failing-before for tasks 1-2; no "not verified" section. |
| Q3 | 2 | service.bak removed; files.txt clean. |

## Summary

| Criterion | A | B | C | D | E | F |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | 0 | 1 | 1 | 1 | 1 | 1 |
| F2 | 0 | 2 | 2 | 2 | 2 | 2 |
| F3 | 2 | 2 | 2 | 2 | 2 | 2 |
| F4 | 2 | 2 | 2 | 2 | 2 | 2 |
| F5 | 2 | 2 | 2 | 2 | 2 | 2 |
| F6 | 2 | 2 | 2 | 2 | 2 | 2 |
| F7 | 2 | 2 | 1 | 2 | 2 | 2 |
| B1 | 0 | 2 | 2 | 1 | 2 | 1 |
| B2 | 1 | 2 | 2 | 2 | 2 | 2 |
| B3 | 2 | 2 | 2 | 2 | 2 | 2 |
| B4 | 2 | 2 | 2 | 2 | 2 | 2 |
| B5 | 2 | 2 | 2 | 2 | 2 | 2 |
| B6 | 2 | 2 | 2 | 2 | 2 | 2 |
| G1 | 2 | 2 | 2 | 2 | 2 | 2 |
| G2 | 2 | 2 | 2 | 2 | 2 | 2 |
| G3 | 2 | 2 | 2 | 2 | 2 | 2 |
| Q1 | 2 | 2 | 2 | 2 | 2 | 2 |
| Q2 | 1 | 2 | 1 | 1 | 1 | 1 |
| Q3 | 2 | 2 | 1 | 2 | 2 | 2 |
| Total /38 | 30 | 37 | 34 | 35 | 36 | 35 |

## Judgement calls

- F1: no run did a true one-rule-at-a-time cycle. B-F wrote both rules' tests then implemented together (1); A implemented and wrote tests in one step with no failing run (0).
- F2: B-F each have a boundary test (one second past 15 minutes) that passed on first run because the old code already charged it. I scored 2 on the reading that only tests guarding new behaviour must fail first. A strict reading would drop B-F to 1. For C and D the output was filtered, so expected and actual values were not visible, only FAIL (not ERROR).
- F7: C added a 1 December date switch (`NEW_TARIFF_FROM`) and a test for the old tariff; scored 1 as one unrequested change. README tariff edits in all runs were treated as part of the rules, not as extra.
- B1: D and F ran the reporter's command only after the fix (1). B and E ran it before any edit; C too. A never ran it before the edit (0 because it also never saw the symptom except via the checks baseline).
- G1/Q3 for C: checks.txt says production code unchanged, but files.txt and task3.diff show `accounts/service.py` rewritten (line endings only, caused by `git checkout accounts/service.py` on Windows). I scored G1 2 on checks.txt, and charged it once, in Q3 (1). Reading it as a formatting change in `accounts/` would make G1 1 (total 33).
- Q2: Applied literally ("gives the commands with their results ... what is not verified"). Only B's replies do this, via a Test record; A, C, D, E, F replies are accurate but omit commands and failing-before for tasks 1-2 and do not list unverified items, so 1. If the grader reads Q2 more leniently (accurate plain-language replies suffice) these would be 2, and the spread shrinks.
- G2 for A, C, D, E, F: proof was by temporarily editing `accounts/service.py` (allowed by the rubric) rather than checking out the old commit; B used a worktree. All restored the file; scored 2.
