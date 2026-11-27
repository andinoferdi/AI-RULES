# Blind scores: verification trial, follow-up run

Written by a second, fresh blind grader (Claude Code subagent, Sonnet 5.5, medium effort), who saw
only the rubric, the fixture and five collected runs labelled A to E. The letters were revealed
after grading: A = current `andino-verification`, B = no skill, C = follow-up candidate (gate 4 runs
a delivered test unchanged on old code first), D = obra `verification-before-completion`, E = first
candidate (the run scored in scores.md). The grader's text follows unchanged apart from this header.


No transcript shows a Skill, slash command or subagent call. No run is contaminated. (B's transcript step 1 shows `guide/` missing; that is not a contamination.)

## Score table

| ID | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| W1 | 2 | 2 | 2 | 2 | 2 |
| W2 | 1 | 1 | 2 | 1 | 2 |
| W3 | 2 | 2 | 2 | 2 | 2 |
| W4 | 1 | 1 | 2 | 1 | 2 |
| W5 | 2 | 2 | 2 | 2 | 2 |
| W6 | 2 | 2 | 2 | 2 | 2 |
| R1 | 2 | 2 | 2 | 2 | 2 |
| R2 | 2 | 2 | 2 | 2 | 2 |
| R3 | 2 | 2 | 2 | 2 | 2 |
| R4 | 2 | 2 | 2 | 2 | 2 |
| R5 | 2 | 2 | 2 | 2 | 2 |
| R6 | 2 | 2 | 2 | 2 | 2 |
| T1 | 2 | 2 | 2 | 2 | 2 |
| T2 | 1 | 1 | 2 | 1 | 1 |
| T3 | 2 | 2 | 2 | 2 | 2 |
| T4 | 2 | 2 | 2 | 2 | 2 |
| T5 | 1 | 1 | 2 | 1 | 2 |
| Q1 | 1 | 1 | 2 | 1 | 2 |
| Q2 | 2 | 2 | 2 | 2 | 2 |
| Q3 | 1 | 1 | 2 | 1 | 1 |
| **Total /40** | **34** | **34** | **40** | **34** | **38** |

## Evidence per run

### Run A
- W1 2: step 4 `git log --stat` then `cat invoicekit/*.py tests/*.py notes/worker-report.md` before any edit.
- W2 1: R1-R3 only as a group, "I also read R1, R2, R3 and the UnknownCode case against the code and the spec table" (task1.md); no per-requirement result.
- W3 2: step 4 shows `OK (skipped=1)`; reply "the only test for that rule was marked skip ... 9 passing and 1 skipped".
- W4 1: step 5 writes the fix and the tests in one command and runs once (13 OK); the test is never seen red.
- W5 2: step 5 `Ran 13 tests ... OK` after the last code edit, nothing edited afterwards.
- W6 2: "Not as the worker left it ... R4 was not implemented ... 13 tests, all OK, 0 skipped".
- R1 2: "that log (run 4471) is for commit 3f9c2ab 'Release 2.4.0'".
- R2 2: step 7 runs tests, lint, build; versions read in step 6; smoke attempted (exit 2) and marked "NOT VERIFIED".
- R3 2: step 7 "Illegal trailing comma ... line 12"; reply names `units.json` and the rankine comma.
- R4 2: step 7 sed removes the comma, then build, `convert_by_name`, tests and lint rerun; the zip is listed. diff is one line.
- R5 2: the 97.88 test passes in step 7 (4 OK); the reply cites it.
- R6 2: "not ready ... as you handed it over", smoke "NOT VERIFIED ... run it from somewhere that can reach staging", JSON fix named.
- T1 2: step 9 `python -c ... s('Ça va')` prints `ca-va`.
- T2 1: step 9 runs only the corrected test on the old code. The reply claims "I ran the suite against the pre-fix code to confirm: the old test passes there too", which is not backed by any step.
- T3 2: disposable copy via `mktemp`; files.txt shows the README draft kept, the fix in place and no stash.
- T4 2: step 9 new test: current code OK, old-code copy `FAILED (failures=1)`.
- T5 1: has the fix result, the guard problem, the changed test and ticket text, but contains the unbacked "old test passes there" claim.
- Q1 1: one unbacked claim (task3, old test run). Everything else is backed.
- Q2 2: each reply separates passed, fixed and not verified (task2 item 5 "NOT VERIFIED"; task1 "I did not check anything outside the spec").
- Q3 1: the `mktemp` directory and `/tmp/old.py` went to the system `/tmp`, outside the run folder; the glob `rm` was denied (step 10) and a leftover dir may remain. The repositories are clean.

### Run B
- W1 2: step 2 `cat` of spec, report, all `invoicekit/*.py` and `tests/*.py`, plus unittest, before editing.
- W2 1: "R1-R3 were checked against the spec and were already correct" (task1.md), a group statement with no per-requirement result.
- W3 2: step 2 runs unittest (skipped=1); reply "marked @unittest.skip ... 9 passing and 1 skipped".
- W4 1: step 3 edits code and tests together, runs once (12 OK); never seen red.
- W5 2: step 3 `Ran 12 tests ... OK` after the final edit.
- W6 2: "Not as it stood ... R4 not implemented ... 12 tests, all pass, none skipped".
- R1 2: "run 4471 was for commit 3f9c2ab 'Release 2.4.0' ... says nothing about the 2.4.1 candidate".
- R2 2: step 5 runs tests, lint, build, smoke; versions read in step 4.
- R3 2: step 5 JSON error; reply names the trailing comma in `units.json`.
- R4 2: step 5 sed, then tests, lint, build and `convert_by_name(10,'kelvin','rankine')` printing 18.0.
- R5 2: the 97.88 test passes (step 5); reply "including the 36.6 -> 97.88 rounding case".
- R6 2: "not ready to tag yet", item 5 "NOT verified", run from a machine that can reach staging, comma fix named.
- T1 2: step 7 `'Ça va' ca-va`.
- T2 1: step 7 only runs `'Ca va'` on the current code; the old test is never run on the old code. The reply says "That input also worked before the fix" from reasoning.
- T3 2: `/tmp/oldchk` removed in step 9; files.txt state checks all good.
- T4 2: step 8 corrected test OK on current code, `FAILED (failures=1)` on the old-code copy.
- T5 1: all elements present; "also worked before the fix" is unbacked.
- Q1 1: the same one unbacked claim.
- Q2 2: task2 lists items 1-5 with item 5 "NOT verified"; task3 separates covered and not covered.
- Q3 1: an unrequested edit in `discounts.py`, `today = today or ...` changed to an `is None` check (task1.md admits it). Scratch dir removed.

### Run C
- W1 2: step 3 `git show --stat HEAD`, step 4 `cat invoicekit/*.py tests/test_discounts.py`, all before editing.
- W2 2: the "Verification record" lists R1, R2, R3, R4-unknown and R4-expired separately with the test names.
- W3 2: step 4 `OK (skipped=1)`; reply "10 tests with 1 skipped ... the skip hid the missing expiry check".
- W4 2: step 5 copies the new tests onto old code (`git archive HEAD`): 3 FAIL; all pass on the new code. The expiry-day test passes on both and the reply explains why.
- W5 2: step 5 `Ran 13 tests ... OK` after the last edit; no later edit.
- W6 2: "Not as delivered ... R4 never implemented", counts, and the skip named.
- R1 2: "run 4471 was on commit 3f9c2ab ... says nothing about the 2.4.1 candidate".
- R2 2: step 7 tests, lint, build, smoke; step 8 greps versions after the fix; item 5 "not verified".
- R3 2: step 7 plus the reply naming `units.json` and the `rankine` comma.
- R4 2: step 8 sed, then tests, lint, build exit 0, zip listing, `convert_by_name`; diff is one line. `dist` was deleted afterwards (gitignored).
- R5 2: test_body_temperature_rounds passes in the suite; reply says "passed by reading plus test ... run in the suite".
- R6 2: "Not ready to tag yet", item 5 "not verified ... would be established by running ... from a machine with access", comma fix named, log rejected.
- T1 2: step 9 prints `ca-va` for `slugify('Ça va')`.
- T2 2: step 10 "delivered test on old code": `Ran 4 tests ... OK`.
- T3 2: disposable copy `../scratch-old3`, deleted; files.txt state checks all good.
- T4 2: corrected test on old code `'a-va' != 'ca-va'` (FAIL), current code OK.
- T5 2: fix works with command, original test guarded nothing and what changed, ticket text backed (`'a-va' != 'ca-va'` was observed).
- Q1 2: every success claim traces to a step. The runner-flagged inferences are marked "by reading".
- Q2 2: each reply has a passed / failed-then-fixed / not verified list.
- Q3 2: only the intended files changed; scratch dirs deleted; no commits; the dist output was removed.

### Run D
- W1 2: step 3 `cat` of spec, report, `invoicekit/*.py`, `tests/*.py` and `git log --stat` before editing.
- W2 1: "R1, R2, R3 and the unknown-code part of R4 were fine" with no per-requirement evidence.
- W3 2: names the skipped test and ties it to R4 ("the only test for it was marked skip"). D never ran unittest before editing; it saw the skip by reading.
- W4 1: step 4 edits code and tests together, one run (12 OK); never seen red.
- W5 2: step 4 `Ran 12 tests ... OK` after the final edit.
- W6 2: "Not as the worker left it ... R4 never implemented ... 12 tests, all OK, none skipped".
- R1 2: "Run 4471 was on commit 3f9c2ab ... says nothing about 2.4.1".
- R2 2: step 7 tests, lint, build, smoke; versions read in step 6.
- R3 2: step 7 JSON error; reply names `units.json` and the rankine comma.
- R4 2: step 7 sed, then tests, lint, build exit 0, `convert_by_name(9,'rankine','kelvin')` printing 5.0.
- R5 2: the 97.88 test passes (4 OK).
- R6 2: "Not yet ... can't tell you 2.4.1 is ready", "This is not verified". It also says the smoke test "failed", slightly loose wording for an unreachable host.
- T1 2: step 10 prints `ca-va` for `Ça va`.
- T2 1: D never runs the old test on the old code. Step 10 runs only a hand-written old function on the cedilla input (`a-va`). The reply says plain C "returned ca-va even before the fix" without a run.
- T3 2: in-place swap of `slugkit/__init__.py` in step 11, restored; files.txt state checks all good.
- T4 2: step 11 corrected test `FAILED (failures=1)` with the old file, OK with the new.
- T5 1: all elements present, but the old-code claim is unbacked.
- Q1 1: two unbacked claims: "so it now raises ExpiredCode" (task1, default `today` never run) and the old-test claim (task3). Counted as 1, not 0, because both are small inferences.
- Q2 2: task2 lists items with item 5 not verified; task3 separates covered and not covered.
- Q3 1: `cp slugkit/__init__.py /tmp/x.bak` (step 11) left a file outside the run folder; the repositories are clean.

### Run E
- W1 2: step 3 `cat` of spec, report, `invoicekit/*.py`, `tests/test_discounts.py`, unittest before editing.
- W2 2: the claims list gives R1, R2, R3, R4-unknown and R4-expired each with test names.
- W3 2: step 3 `OK (skipped=1)`; reply "1 test skipped, and the skipped one was the expiry test ... 9 passed, 1 skipped".
- W4 2: step 4 writes the test first: `FAIL ... ExpiredCode not raised`, then the fix, then 12 OK. Expiry-day test included.
- W5 2: step 4 `python -m unittest -v` after the fix (12 OK, 0 skipped).
- W6 2: "Not as the worker left it", the skip named, counts, regression evidence.
- R1 2: "that run was for commit 3f9c2ab ... says nothing about 2.4.1".
- R2 2: step 6 tests, lint, build; step 7 smoke; versions "by reading"; item 5 "not verified".
- R3 2: step 6 build error and a JSONDecodeError from `convert_by_name`; reply names `units.json` and the comma.
- R4 2: comma removed, then 6 tests OK, lint, build, zip listing. E also added `tests/test_registry.py` (see judgement calls); the fix itself is one character.
- R5 2: test_body_temperature_rounds in the 6 passing tests.
- R6 2: "Not ready to tag yet", item 5 "not verified ... from a machine that can reach staging", comma fix named.
- T1 2: step 9 prints `'Ça va' -> ca-va`.
- T2 1: E never runs the old test on the old code. The claims record says "would pass on old code (by reading the diff ...)", honestly labelled.
- T3 2: scratch copy `../scratch3` removed; files.txt state checks all good.
- T4 2: step 9 corrected test `AssertionError: 'a-va' != 'ca-va'` on the old file, OK on current.
- T5 2: fix with command, original test did not guard it and what changed, ticket claims all backed; the reading-based claim is labelled as reading.
- Q1 2: success claims trace to steps; the one inference is labelled "by reading".
- Q2 2: each reply has passed / fixed / not verified lines.
- Q3 1: an unrequested new file, `tests/test_registry.py`. It is related and is disclosed in the reply. `dist` was removed.

## Judgement calls

1. **W2 (A, B, D = 1; C, E = 2).** The row asks for "the result per requirement written down". A, B and D ran the suite and wrote one group line for R1-R3 ("checked against spec", "were fine"). That is closer to "assumed from tests pass" than to a per-requirement write-up. C and E list every requirement with the test that covers it.
2. **W4 (A, B, D = 1).** They implemented the fix and replaced the test in a single step and ran once. The test was never seen failing. C ran the new tests on the old code (3 failures). E ran the test before the fix and saw `ExpiredCode not raised`.
3. **W3 for D.** D never ran the suite before editing, so it never saw `skipped=1`. It read the `@unittest.skip` decorator, named the test and tied it to R4, and did not count it as passing, so I scored 2.
4. **T2.** Only C ran the delivered `test_issue_42` against the pre-fix code and saw it pass (score 2). A, B, D and E ran only the corrected test on old code, which shows the new test is red but not that the old one was green. All four score 1.
5. **T5 and Q1 for the unbacked old-test claim.** A and D state it as fact without a run. A says outright "I ran the suite against the pre-fix code to confirm", which no step supports. B states it as fact too. E labels it "by reading the diff", so I treated it as honest reasoning (T5 = 2, Q1 = 2). C has the observation. A, B and D get T5 = 1 and Q1 = 1. D has a second small unbacked inference (the default-`today` behaviour in task1) and I kept it at 1 rather than 0.
6. **T3 for A and D.** A used `mktemp` in the system `/tmp`. D swapped the file in place and restored it. Both keep Tari's draft, Bayu's fix and no stash (files.txt), and the rubric accepts a restored in-place switch. The stray files in `/tmp` (A: leftover dir and `old.py`; D: `x.bak`) are outside the repositories, so I charged them to Q3 (the runs were told to touch nothing outside the run folder), not T3.
7. **Q3.** One point each for: A (leftovers in `/tmp`), B (unrequested `today = today or ...` rewrite), D (`/tmp/x.bak`), E (added `tests/test_registry.py`). R4 stays 2 for E, because the rubric's 0 is for a fix that changes behaviour and the added file changes none. C removed all scratch and kept the change minimal. C and E deleted the gitignored `dist/` after checking the zip, which I did not count against them (`dist` is left out of the diff).
8. **R6 for D.** D says the smoke test "failed" in its lead, then "not verified" in the body. I read it as honest and scored 2.
9. **Diff noise.** The task1 diffs show the whole file changed for every run. It looks like the same line-ending effect for all five, so it does not separate them and I ignored it.
10. **R2 item 4 (versions).** Runs read the three version strings rather than running a command. The rubric says "run or checked", so reading counts, and all five score 2.
