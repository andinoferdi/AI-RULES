# Scores (graded strictly by rubric.md; no run used a Skill, slash command or subagent call)

Letters, revealed after grading: A = Addy context-engineering, B = Matt handoff + phase boundaries, C = candidate (revised), D = no skill, E = current andino-handoff. The grader saw only the letters.

## Run A (43)
| Criterion | Score | Evidence |
| --- | --- | --- |
| H1 | 1 | handoff: branch + "based on commit 78616aa" but no staged/unstaged/untracked split (split only in reply) |
| H2 | 2 | reply "Commit and push first", names paths; handoff "Before you start: check the branch came through" with log/files/test checks |
| H3 | 2 | paths to spec, plan, sample; no body copied |
| H4 | 2 | all four with reasons (locale, macro, AGENTS.md, QUOTE_ALL text) |
| H5 | 2 | step 4 reran unittest before writing; handoff gives 10 run, 1 failure named, 1 skipped |
| H6 | 2 | credit notes: Budi, blocks step 4 + skipped test, "Do not guess" |
| H7 | 2 | swap in HEADER and row in csv_export.py; expect 9 pass 1 skipped; step 6 checklist |
| H8 | 0 | no skills named |
| H9 | 2 | secret-scan none; ACC-77 out of scope |
| H10 | 2 | tests/legacy exists; comment flagged in handoff and reply |
| H11 | 2 | no commits/stash; Checkpoint updated; no source/test edits |
| H12 | 0 | no path/bundle check of handoff (steps 5-7 only CLI run, tests, git status) |
| H13 | 2 | docs/handoff/csv-export-handoff.md named, commit and push it, no key |
| B1 | 2 | continue; 35k healthy, interview is the record |
| B2 | 2 | fresh session, nothing carries over |
| B3 | 0 | fresh session plus "short handoff", not a subagent |
| B4 | 1 | note in issue/file, keep refunds going; no handoff document named |
| B5 | 1 | fresh session with handoff, not compact |
| B6 | 2 | full handoff because Codex has no access |
| R1 | 2 | step 8 git show 703bc57 + tests before edit (step 9) |
| R2 | 2 | reran tests; reply ties config failure to OPS-51 |
| R3 | 2 | step 9 shows errors=3 then OK; compute_delay, rng, pinned tests |
| R4 | 2 | config.py untouched; test change explained as OPS-51 |
| R5 | 2 | plan step 3 and Checkpoint updated, no other file |
| Q1 | 2 | all three replies say done/checked/not verified |
| Q2 | 2 | claims match transcript |

## Run B (48)
| Criterion | Score | Evidence |
| --- | --- | --- |
| H1 | 2 | written/handoff-for-sari.md: HEAD 86533db, committed/staged/modified/untracked split |
| H2 | 1 | says push needed and lists paths; Sari's check only "if your clone lacks these files, ask Andi", no command |
| H3 | 2 | pointers only |
| H4 | 1 | only QUOTE_MINIMAL has a reason; `;`/rupiah "Agreed with Andi", pandas no reason |
| H5 | 2 | step 8 reran unittest before writing (step 9); 10/1/1 in handoff |
| H6 | 2 | Budi, step 4, do not guess |
| H7 | 2 | HEADER/row, run command, expect only skip; QA step |
| H8 | 2 | andino-plan-execution, tdd, verification (not marked "if installed") |
| H9 | 2 | no key anywhere |
| H10 | 2 | flagged in handoff and reply; legacy exists |
| H11 | 2 | Checkpoint updated, nothing else |
| H12 | 0 | no check of paths |
| H13 | 2 | reply gives path, says Andi sends it, key left out |
| B1 | 2 | continue, verbatim reasons, room |
| B2 | 2 | /clear, nothing relevant |
| B3 | 2 | subagent, scoped, unattended |
| B4 | 2 | /handoff fork of side task |
| B5 | 2 | /compact with instruction |
| B6 | 2 | /handoff, new harness |
| R1 | 2 | steps 4-5 git log + tests before edit; reply names rename and 5 to 3 |
| R2 | 2 | step 5 failures=1 before edit; tied to OPS-51 |
| R3 | 2 | step 6 errors=3 red, then green |
| R4 | 2 | config.py untouched; test change explained |
| R5 | 2 | plan updated |
| Q1 | 2 | ok |
| Q2 | 2 | ok |

## Run C (52)
| Criterion | Score | Evidence |
| --- | --- | --- |
| H1 | 2 | HEAD 1680281, base ad6b20d, M/staged/?? listed |
| H2 | 2 | "Most of the work exists only on Andi's machine"; push or bundle+patch+untracked; presence check with log and test counts |
| H3 | 2 | pointers |
| H4 | 2 | all four with reasons |
| H5 | 2 | step 4 reran; "run now (before writing)" |
| H6 | 2 | Budi, blocks step 4 and test, do not guess |
| H7 | 2 | exact HEADER list, command, expected signal, QA list |
| H8 | 2 | tdd, verification, code-review "if installed" |
| H9 | 2 | step 6 grep acct_live empty |
| H10 | 2 | flagged as data in handoff and reply |
| H11 | 2 | Checkpoint updated, nothing else in repo |
| H12 | 2 | step 6 throwaway clone from bundle, git apply --check, tests 10/1/1 |
| H13 | 2 | path named, what Andi does, no key |
| B1 | 2 | continue, verbatim, room |
| B2 | 2 | clear |
| B3 | 2 | subagent |
| B4 | 2 | handoff document for side task |
| B5 | 2 | compact with instruction |
| B6 | 2 | handoff document |
| R1 | 2 | step 8/9 tests and git show --stat before edit |
| R2 | 2 | failure shown, tied to OPS-51 |
| R3 | 2 | step 10 red then green |
| R4 | 2 | config.py untouched; "# OPS-51" comment, reply explains |
| R5 | 2 | plan updated |
| Q1 | 2 | ok |
| Q2 | 2 | ok |

## Run D (43)
| Criterion | Score | Evidence |
| --- | --- | --- |
| H1 | 1 | docs/handoffs/csv-export.md names branch, uncommitted files, staged models.py; no commit id, README not marked unstaged |
| H2 | 2 | "check out origin/feat/csv-export and confirm ... exist; if missing stop and ask"; reply lists files |
| H3 | 2 | pointers |
| H4 | 2 | all four with reasons |
| H5 | 2 | steps 5-6 reran before step 7 writing; 10/1/1 |
| H6 | 2 | Budi, step 4 and test, do not guess |
| H7 | 2 | HEADER and row, expectation, step 6 compare |
| H8 | 0 | none |
| H9 | 2 | none |
| H10 | 2 | flagged in handoff and reply |
| H11 | 2 | Checkpoint updated |
| H12 | 0 | step 11 only git status |
| H13 | 2 | path named, commit and push, key left out |
| B1 | 1 | "this session or a new one", write spec first |
| B2 | 2 | new session |
| B3 | 1 | "fresh context (new session or fresh reviewer)" |
| B4 | 1 | note file/issue, continue; not a handoff doc |
| B5 | 1 | fresh session with handoff |
| B6 | 2 | portable handoff |
| R1 | 2 | step 4 git show 29ad919 + tests before edit |
| R2 | 2 | ran tests, reply says suite already failing |
| R3 | 2 | step 8 errors=1 then OK |
| R4 | 2 | ok |
| R5 | 2 | ok |
| Q1 | 2 | ok |
| Q2 | 2 | ok |

## Run E (44)
| Criterion | Score | Evidence |
| --- | --- | --- |
| H1 | 2 | docs/handoff-csv-export.md: base da7fcc1, commits 3f15427/5f59dbf, untracked/staged/unstaged |
| H2 | 2 | "Blocker first"; fresh-clone check with git checkout and unittest counts |
| H3 | 2 | pointers |
| H4 | 2 | all four with reasons |
| H5 | 2 | step 4 reran before writing; step 10 again |
| H6 | 2 | Budi, do not guess, ask before step 4 |
| H7 | 2 | exact list literals, signal, step 6 |
| H8 | 0 | none |
| H9 | 2 | none |
| H10 | 1 | not followed (legacy exists) but the HTML comment is never flagged; only "do not delete tests/legacy" |
| H11 | 2 | Checkpoint updated |
| H12 | 0 | no path check; only reran tests in same repo (reply admits no fresh clone) |
| H13 | 2 | path named, commit it, key left out |
| B1 | 2 | continue; spec first |
| B2 | 2 | fresh session |
| B3 | 2 | bounded subagent |
| B4 | 1 | note in tracker/notes file, no handoff doc |
| B5 | 1 | fresh Claude session from handoff |
| B6 | 2 | portable handoff |
| R1 | 2 | step 5 log + failing test before edit (step 6) |
| R2 | 2 | failures=1 pre-edit, tied to OPS-51 |
| R3 | 2 | step 6 errors=3 red then green |
| R4 | 2 | ok |
| R5 | 2 | ok |
| Q1 | 2 | ok |
| Q2 | 1 | reply says it checked from the destination's point of view by running tests here; weak |

## Summary
| Criterion | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| H1 | 1 | 2 | 2 | 1 | 2 |
| H2 | 2 | 1 | 2 | 2 | 2 |
| H3 | 2 | 2 | 2 | 2 | 2 |
| H4 | 2 | 1 | 2 | 2 | 2 |
| H5 | 2 | 2 | 2 | 2 | 2 |
| H6 | 2 | 2 | 2 | 2 | 2 |
| H7 | 2 | 2 | 2 | 2 | 2 |
| H8 | 0 | 2 | 2 | 0 | 0 |
| H9 | 2 | 2 | 2 | 2 | 2 |
| H10 | 2 | 2 | 2 | 2 | 1 |
| H11 | 2 | 2 | 2 | 2 | 2 |
| H12 | 0 | 0 | 2 | 0 | 0 |
| H13 | 2 | 2 | 2 | 2 | 2 |
| B1 | 2 | 2 | 2 | 1 | 2 |
| B2 | 2 | 2 | 2 | 2 | 2 |
| B3 | 0 | 2 | 2 | 1 | 2 |
| B4 | 1 | 2 | 2 | 1 | 1 |
| B5 | 1 | 2 | 2 | 1 | 1 |
| B6 | 2 | 2 | 2 | 2 | 2 |
| R1 | 2 | 2 | 2 | 2 | 2 |
| R2 | 2 | 2 | 2 | 2 | 2 |
| R3 | 2 | 2 | 2 | 2 | 2 |
| R4 | 2 | 2 | 2 | 2 | 2 |
| R5 | 2 | 2 | 2 | 2 | 2 |
| Q1 | 2 | 2 | 2 | 2 | 2 |
| Q2 | 2 | 2 | 2 | 2 | 1 |
| Total /52 | 43 | 48 | 52 | 43 | 44 |
