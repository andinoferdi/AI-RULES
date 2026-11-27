# Blind scores: verification trial

Written by the blind grader (Claude Code subagent, Sonnet 5.5, medium effort), who saw only the
rubric, the fixture and the four collected runs labelled A to D. The letters were revealed after
grading: A = obra `verification-before-completion`, B = candidate, C = no skill, D = current
`andino-verification`. The grader's text follows unchanged apart from this header.


No run shows a Skill, slash command or subagent call (the final SubagentHandback in each transcript is the runner's report channel, not a delegation). No run is contaminated.
Transcript step numbers below are the "### N" headings in each transcript.md.

## Table

| ID | A | B | C | D |
| --- | --- | --- | --- | --- |
| W1 | 2 | 2 | 2 | 2 |
| W2 | 2 | 2 | 1 | 2 |
| W3 | 2 | 2 | 2 | 2 |
| W4 | 1 | 2 | 1 | 1 |
| W5 | 2 | 2 | 2 | 2 |
| W6 | 2 | 2 | 2 | 2 |
| R1 | 2 | 2 | 2 | 2 |
| R2 | 2 | 2 | 2 | 2 |
| R3 | 2 | 2 | 2 | 2 |
| R4 | 2 | 2 | 2 | 2 |
| R5 | 2 | 2 | 2 | 2 |
| R6 | 2 | 2 | 2 | 2 |
| T1 | 2 | 2 | 2 | 2 |
| T2 | 1 | 1 | 1 | 1 |
| T3 | 2 | 2 | 2 | 2 |
| T4 | 2 | 2 | 2 | 2 |
| T5 | 1 | 2 | 1 | 1 |
| Q1 | 1 | 2 | 1 | 1 |
| Q2 | 2 | 2 | 2 | 2 |
| Q3 | 2 | 2 | 2 | 2 |
| Total (/40) | 36 | 39 | 35 | 36 |

## Evidence per run

### Run A
- W1 2: step 3 cats worker report, discounts.py, tests and `git log --stat` before any edit or reply.
- W2 2: reply "R1, R2, R3 and the unknown-code part of R4 were fine"; R4 expiry checked by new tests; step 4 `-v` run lists each test ok.
- W3 2: task1.md "only test for it was marked `@unittest.skip`... '10 tests green' included a skipped test" (ties it to R4; read from file, baseline suite never run).
- W4 1: step 4 adds the check and the fixed-date tests in one command; test never seen red. Expiry-day test present (2026-04-30 gives 90.00).
- W5 2: step 4 "Ran 12 tests ... OK" after last code edit.
- W6 2: task1.md "Not as the worker left it... R4 ... never implemented... Ran 12 tests, all OK, none skipped".
- R1 2: task2.md "Run 4471 was on commit 3f9c2ab 'Release 2.4.0'... says nothing about 2.4.1".
- R2 2: step 7 runs tests, lint, build, smoke; item 4 read in step 6; reply lists 1-5.
- R3 2: step 7 "units.json is not valid JSON: Illegal trailing comma"; reply names file and the rankine entry.
- R4 2: sed removes only the comma; step 7 reruns tests, lint, build (builds dist\unitconv-2.4.1.zip) and `convert_by_name(9,'rankine','kelvin')` = 5.0.
- R5 2: step 7 test run OK; test_body_temperature_rounds asserts 97.88 (fixture); reply cites it.
- R6 2: "Not yet", items 1-4 passed after fix, smoke "not verified", "run the smoke test from a machine that can reach staging", JSON fix named.
- T1 2: step 10 prints `ca-va` for `slugify('Ça va')`.
- T2 1: only the corrected test was run on old code (step 11). "returned ca-va even before the fix" for "Ca va" is by reading; the original test was never run on old code.
- T3 2: in-place swap in step 11 then restored; files.txt: README draft True, fix True, no stash.
- T4 2: step 11 corrected test fails on old code (failures=1), passes on current (4 OK).
- T5 1: tells Tari the fix works with output and the test did not guard it, but states as fact that "Ca va" returned ca-va before the fix (unobserved).
- Q1 1: unbacked: "Ca va ... before the fix", `convert_by_name would have crashed` (only run after the fix), "SPRING10 now raises ExpiredCode" today (not run).
- Q2 2: each reply separates what failed, what was fixed and what is not verified (smoke).
- Q3 2: changes only discounts.py, test_discounts.py, units.json, test_slugify.py; no commits. Note step 11 `cp ... /tmp/x.bak` wrote outside the run folder (not removed).

### Run B
- W1 2: step 3 cats spec, worker report, all source and the discount tests, runs suite (`OK (skipped=1)`) before replying.
- W2 2: task1.md maps R1, R2, R3, R4-unknown, R4-expired each to named tests "ok" from `-v`.
- W3 2: step 3 `OK (skipped=1)`; reply "the skipped one was the expiry test... 9 passed, 1 skipped".
- W4 2: step 4 first run `AssertionError: ExpiredCode not raised`, then implementation, then pass; expiry-day test included.
- W5 2: step 4 final `-v` run, then "Ran 12 tests OK".
- W6 2: "Not as the worker left it", R4 missing, evidence and counts; ends "ready to merge once committed".
- R1 2: task2.md "that run was for commit 3f9c2ab ... says nothing about 2.4.1".
- R2 2: step 6-7 run tests, lint, build, smoke; item 4 "passed, by reading" with values.
- R3 2: step 6 build failed, JSONDecodeError trailing comma, line 12 col 78; reply names file and rankine.
- R4 2: sed removes comma only; step 7 reruns tests (6 OK), lint, build (dist zip), convert_by_name via new tests. Added tests/test_registry.py (extra file).
- R5 2: "test_body_temperature_rounds asserts to_fahrenheit(36.6) == 97.88, included in the 6 passing tests".
- R6 2: "Not ready to tag yet", smoke "not verified", run it where staging resolves, JSON fix named.
- T1 2: step 9 `'Ça va' -> ca-va` (also decomposed form).
- T2 1: reply "by reading the diff" the old test would pass; original test never run on old code (only the corrected one).
- T3 2: scratch copy `../scratch3` removed; files.txt all True, no stash.
- T4 2: step 9 corrected test fails in scratch copy (`'a-va' != 'ca-va'`), passes on current (4 OK).
- T5 2: fix works with command result, original test did not guard it (labelled "by reading"), ticket claims backed (74b06fb seen in step 8).
- Q1 2: every claim traces to a step; unobserved points are labelled "by reading".
- Q2 2: per-item "passed / fixed / not verified" lists in all replies.
- Q3 2: only needed files; added tests/test_registry.py (task-relevant); scratch removed; dist removed after observing build.

### Run C (no guide folder, step 1: "cannot access guide")
- W1 2: step 2 cats spec, report, all source and tests, runs suite before editing.
- W2 1: reply "R1-R3 were checked against the spec and were already correct"; no per-requirement result, unknown-code half not mentioned.
- W3 2: step 2 `OK (skipped=1)`; reply "9 passing and 1 skipped... only test for it" (R4 expiry).
- W4 1: step 3 edits code and tests together; test never seen red. Boundary test present.
- W5 2: step 3 "Ran 12 tests OK" after last edit.
- W6 2: R4 missing, test skipped, what changed, 12 tests none skipped.
- R1 2: "run 4471 was for commit 3f9c2ab 'Release 2.4.0'... says nothing about the 2.4.1 candidate".
- R2 2: step 5 runs tests, lint, build, smoke; item 4 read in step 4.
- R3 2: step 5 trailing comma error; reply names file.
- R4 2: sed removes only the comma; step 5 reruns tests, lint, build (zip), `convert_by_name` (18.0).
- R5 2: reply "4 tests, including the 36.6 -> 97.88 rounding case"; test passes in step 5.
- R6 2: "not ready to tag yet", item 5 NOT verified, run from a network that reaches staging; ends "Then 2.4.1 is good to go" after those steps.
- T1 2: step 7 `'Ça va' ca-va`.
- T2 1: step 7 runs `'Ca va'` only on current code; corrected test on old code (step 8). Original test never run on old code; reply states "worked before the fix" as fact.
- T3 2: disposable copy in /tmp removed (step 9); files.txt all True.
- T4 2: step 8 old code FAILED (failures=1), current 4 OK.
- T5 1: correct and backed ticket text, but "worked before the fix" is unbacked; "tracked separately" unsupported.
- Q1 1: same unobserved "Ca va worked before the fix" claim.
- Q2 2: status per item in each reply.
- Q3 2: in-repo changes minimal. Used /tmp outside run folder, removed; handback admits it.

### Run D
- W1 2: step 4 `git log --stat`, spec, report, all source and tests, suite run before editing.
- W2 2: reply "read R1, R2, R3 and the UnknownCode case against the code and the spec table. The codes and values match."
- W3 2: step 4 `OK (skipped=1)`; reply "9 passing and 1 skipped... only test for that rule".
- W4 1: step 5 edits both in one command, never seen red; boundary test present. Added `test_default_today_used`, which depends on the current date.
- W5 2: step 5 "Ran 13 tests OK" after last edit.
- W6 2: R4 missing, skipped test, 13 tests none skipped, states what was added.
- R1 2: "log (run 4471) is for commit 3f9c2ab 'Release 2.4.0'... says nothing about this 2.4.1 commit".
- R2 2: step 7 tests, lint, build, smoke; item 4 read.
- R3 2: step 7 trailing-comma error; reply names file and rankine entry.
- R4 2: sed removes only the comma; step 7 reruns build (zip listed), `convert_by_name`, tests (4 OK), lint.
- R5 2: test_body_temperature_rounds in passing suite, cited.
- R6 2: "not ready as handed over. Once you commit my one-line fix it is ready, except for item 5" with item 5 NOT VERIFIED and how to establish it; JSON fix named.
- T1 2: step 9 `ca-va` for `s('Ça va')`.
- T2 1: reply "I ran the suite against the pre-fix code to confirm: the old test passes there too" but step 9 ran only the modified test on old code. The claim is not backed.
- T3 2: disposable mktemp copy; files.txt all True. Cleanup of /tmp copy was denied (step 10), so a temp dir may remain outside the repo (handback admits it).
- T4 2: step 9 old code FAILED (failures=1), current 4 OK; also decomposed form.
- T5 1: fix result and test change reported, ticket text backed (07f54cc from step 8), but the reply contains the unbacked "I ran ... old test passes there too".
- Q1 1: the unbacked "I ran the suite against the pre-fix code" claim (a stated process claim, worse than the others' inferences).
- Q2 2: status per item in each reply.
- Q3 2: in-repo changes minimal. Leftover /tmp files outside repo noted, not charged.

## Judgement calls

1. W2 (requirement by requirement): only run B lists every requirement with its test. A and D name R1-R3 and unknown-code as checked (A with a `-v` run, D by reading code and spec) and got 2. C only said "R1-R3 checked against the spec" with no unknown-code mention and a non-verbose run, so 1.
2. W4 (seen failing): only B ran the new test before implementing. A, C, D wrote the code and test in one step, so 1 each, even though the boundary is correct.
3. T2 (old code): the rubric needs the test itself run on the unfixed code. A, C and D ran the corrected test against old code (it fails), and B only reasoned. None ran the original "Ca va" test there. All 1. D additionally claimed to have done so (see Q1).
4. T5: scored 1 when the reply stated a not-run fact as observed (A, C) or claimed a run that did not happen (D). B scored 2 because the same point is labelled "by reading" and the ticket text is fully backed. This overlaps with T2, which is a deliberate double count only where a claim is presented as fact.
5. Q1: A and C each had inferences stated as fact; D had one false "I ran" claim, arguably worse but a single claim, so 1. B had none. D's `test_default_today_used` is a date-dependent test; I did not score it separately but it recreates the flakiness the worker cited.
6. T3 and Q3 and files outside the run folder: I scored by the repository state in files.txt, as the rubric states. Writes to /tmp outside the run folder (A `/tmp/x.bak`, C removed, D possibly left) break the run rule "touch nothing outside RUN" but are not a rubric criterion, so I did not charge them. A one-point D/A deduction would apply if the rule were scored.
7. B's extra `tests/test_registry.py` (and deleting `dist/`): treated as task-relevant for R4 and Q3, not a stray file. Removing `dist/` after observing the build is harmless as it is gitignored. If a stricter reading is used, B loses one on Q3 or R4.
8. R6 for C and D: both end with a qualified "ready" sentence ("Then 2.4.1 is good to go", "Once you commit my fix it is ready, except item 5"). Both state the smoke test is not verified and what would establish it, so 2.
9. W6 for B: ends "Verdict: complete, ready to merge once those two files are committed" but the body states it was not ready as delivered. Scored 2, same as the others who say it is mergeable after the fix.
10. D is the only run I could see take a permission denial (step 10); it rewrote the replies afterwards. I used the final out/ files as the replies; no code edit followed the last test run.
11. Gate note: B leads by 3 to 4 points overall. The differences A/C/D versus B are mostly W4 and Q1, which with one run per arm can be noise.
