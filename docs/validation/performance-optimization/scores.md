# Scores: performance-optimization trial

Blind grader output, unedited below the line. Letters: A = candidate (run-4), B = Addy (run-1),
C = current Andino (run-3), D = ruvnet (run-2); the mapping was kept outside the grading folder
and revealed after scoring. Grader: Claude Code subagent, Sonnet 5.5, medium effort.

---

# Scores (blind trial, rubric performance-optimization)

Contamination: none of A-D shows a Skill, slash command, subagent call or package install (SubagentHandback is the runner's return call). Note: A wrote a temporary copy to /tmp (step 6, deleted afterwards); not contamination.

## Run A
| ID | Score | Evidence |
|---|---|---|
| B1 | 2 | Step 4: 8 runs before edit; reply names median ~750 ms, spread, 150 ms p95 target |
| B2 | 2 | Step 4 measures 0.46 ms/query (2000 trivial queries) x 1521 queries; reply attributes ~93% |
| B3 | 2 | No cache; reply gives tenant-key and billing-freshness reasons |
| B4 | 2 | Checksums acme/globex identical, 300 rows, tests pass (step 5) |
| B5 | 2 | Same command, 8 runs, median 4 ms, worst 7.1, vs target |
| B6 | 2 | test_query_count_does_not_grow_with_orders; run against old code: 51 != 1027 (step 6) |
| W1 | 2 | Names hero img, Load Delay 2,930 ms = 61%, lazy/data-src cause |
| W2 | 2 | Hero has src, fetchpriority=high, no lazy; team images untouched/deferred |
| W3 | 2 | Hero width/height 1600x900, tied to report CLS; team images not sized |
| W4 | 2 | vendor.js untouched; tests pass |
| W5 | 2 | "NOT MEASURED"; "low 2 s range" labelled expectation, not for the deck; field data absent stated |
| W6 | 2 | Same Lighthouse mobile settings, 3+ runs, median; test guard added (fails on old); no LCP CI assertion |
| M1 | 2 | Step 17: 3 runs at 3000, 6000, times recorded |
| M2 | 2 | Cache entries 3000 after 3000 requests; logger stubbed 22.5 vs 22.7 MB |
| M3 | 2 | Key (name, locale); logger untouched |
| M4 | 2 | Tests pass (4); locale and request_id tests still covered |
| M5 | 2 | Soak 3000 x3 and 6000 flat 0.4 MB; time 2.4 s to 0.53 s |
| M6 | 2 | Cache-size test, fails on old (500 != 1) |
| N1 | 2 | 5x20,000 timeit, dry-run 2.86 s upload, 40/day |
| N2 | 2 | slug.py unchanged |
| N3 | 2 | Number, reason, revisit conditions; says regex recompile mostly free (cached) |
| L1 | 2 | Attempts tables with before/after and verdicts in tasks 1-3 replies |
| Q1 | 2 | All four replies state cause, change, checks, unverified |
| Q2 | 2 | Claims match transcript; estimate labelled |

## Run B
| ID | Score | Evidence |
|---|---|---|
| B1 | 1 | Step 3: 5 runs before edit, range only (657-695), no statistic named; target named in reply |
| B2 | 1 | Cause by reading code; 1521 only seen in bench output; no per-query timing |
| B3 | 2 | No cache; tenant-key and billing reasons given |
| B4 | 2 | Checksum same, tests pass |
| B5 | 2 | Same command, 5 runs, 2.8-6.9 ms, spread shown, target compared |
| B6 | 2 | Test: query_count <= 3 on 300-order db (would be 1521 on old); not run against old |
| W1 | 2 | 61%, 2.9 s before download, lazy hero named |
| W2 | 2 | src, fetchpriority=high, team native lazy |
| W3 | 2 | All images width/height + height:auto, ties to 0.21 CLS |
| W4 | 2 | defer + DOMContentLoaded; tests pass |
| W5 | 2 | No number; no field data/RUM stated |
| W6 | 1 | Asks to re-run same mobile test; no several runs/median, no budget |
| M1 | 2 | Step 11: soak 600..3000 with time |
| M2 | 1 | By reading code; logger ruled out by deque only |
| M3 | 2 | Key (name, locale); logger untouched (CHANGELOG entry added, harmless) |
| M4 | 2 | Tests pass incl. existing locale/log tests |
| M5 | 2 | Soak 3000 and 30000 flat; 3.4 s to 0.3 s |
| M6 | 2 | Test <= 36 entries after 200 requests (fails on old; not run against old) |
| N1 | 2 | 20,000-loop timeit, dry run, 40/day |
| N2 | 2 | Unchanged |
| N3 | 2 | Number, reason, offers upload look; corrects regex claim |
| L1 | 1 | Before/after numbers in replies for tasks 1 and 3 only; no record file |
| Q1 | 2 | Meets in all four |
| Q2 | 2 | Claims match; mild inference about traffic labelled |

## Run C
| ID | Score | Evidence |
|---|---|---|
| B1 | 2 | Step 3: 8 runs before edit; reply median ~677 ms and 150 ms p95 |
| B2 | 1 | Cause from code reading; 1521 in bench output |
| B3 | 2 | No cache; reasons given |
| B4 | 2 | Checksums identical, tests pass |
| B5 | 2 | Same command 8 runs, medians 677 vs 4.6 ms, range |
| B6 | 0 | No test added, none proposed (diff touches summary.py only) |
| W1 | 2 | Names LCP img, 2.9 s load delay, lazy cause |
| W2 | 2 | src, fetchpriority, preload, team native lazy |
| W3 | 2 | All images dims, CLS 0.21 named |
| W4 | 2 | defer + DOMContentLoaded, tests pass |
| W5 | 2 | "low 2 s range" labelled estimate; lab vs field stated |
| W6 | 1 | Re-run same mobile test few times, median; no budget |
| M1 | 2 | Step 10 soak with times |
| M2 | 1 | Code reading only; logger by deque |
| M3 | 2 | Key (name, locale) |
| M4 | 2 | Tests pass |
| M5 | 2 | 600-3000 and 30000 flat; 3.24 s to 0.46 s |
| M6 | 2 | Test: one key after 200 requests |
| N1 | 2 | 7x10,000 timeit, dry run, 40/day |
| N2 | 2 | Unchanged |
| N3 | 2 | Number, reason, evidence that would reopen (bulk re-slug); says regex recompile "is real" but cached |
| L1 | 1 | Numbers in tasks 1, 3 replies, no record |
| Q1 | 2 | Meets in all four |
| Q2 | 1 | Task 3 reply says ~1 GB/day growth at 40 req/s; 7.6 KB x 40/s is ~26 GB/day, unsupported arithmetic |

## Run D
| ID | Score | Evidence |
|---|---|---|
| B1 | 1 | Step 3: 3 runs before edit, no statistic named; target named in reply |
| B2 | 1 | Code reading; 1521 in bench output |
| B3 | 2 | No cache; reasons given |
| B4 | 2 | Checksum same, 300 rows, tests pass |
| B5 | 1 | 5 runs after vs 3 before; no median/spread analysis |
| B6 | 0 | No guard added or proposed |
| W1 | 2 | 61%, load delay, lazy |
| W2 | 2 | Preload, fetchpriority, no lazy; team stay on lazy.js |
| W3 | 2 | All images sized; CLS 0.21 named |
| W4 | 2 | defer + DOMContentLoaded; tests pass |
| W5 | 2 | No number; lab vs field stated; "did not check in a browser" |
| W6 | 1 | Re-run same test a few times; no budget |
| M1 | 2 | Step 10 soak with times |
| M2 | 1 | Code reading; logger ruled out by deque; "tested by changing only the key" is after the edit |
| M3 | 2 | Key (name, locale) |
| M4 | 2 | Tests pass |
| M5 | 1 | 30000 flat; elapsed time not compared in reply |
| M6 | 2 | Test: cache grows <= 1 over 50 unique ids |
| N1 | 2 | 100,000-call timeit, dry run, 40/day |
| N2 | 2 | Unchanged (trial rewrite only in a scratch script) |
| N3 | 1 | Number and reason, corrects regex claim, but no evidence that would change the decision |
| L1 | 1 | Numbers for tasks 1, 3 only; no record |
| Q1 | 2 | Meets in all four |
| Q2 | 2 | Wrong GB figure drafted then removed (step 13); final claims match |

## Summary
| Criterion | A | B | C | D |
|---|---|---|---|---|
| B1 | 2 | 1 | 2 | 1 |
| B2 | 2 | 1 | 1 | 1 |
| B3 | 2 | 2 | 2 | 2 |
| B4 | 2 | 2 | 2 | 2 |
| B5 | 2 | 2 | 2 | 1 |
| B6 | 2 | 2 | 0 | 0 |
| W1 | 2 | 2 | 2 | 2 |
| W2 | 2 | 2 | 2 | 2 |
| W3 | 2 | 2 | 2 | 2 |
| W4 | 2 | 2 | 2 | 2 |
| W5 | 2 | 2 | 2 | 2 |
| W6 | 2 | 1 | 1 | 1 |
| M1 | 2 | 2 | 2 | 2 |
| M2 | 2 | 1 | 1 | 1 |
| M3 | 2 | 2 | 2 | 2 |
| M4 | 2 | 2 | 2 | 2 |
| M5 | 2 | 2 | 2 | 1 |
| M6 | 2 | 2 | 2 | 2 |
| N1 | 2 | 2 | 2 | 2 |
| N2 | 2 | 2 | 2 | 2 |
| N3 | 2 | 2 | 2 | 1 |
| L1 | 2 | 1 | 1 | 1 |
| Q1 | 2 | 2 | 2 | 2 |
| Q2 | 2 | 2 | 1 | 2 |
| Total /48 | 48 | 43 | 41 | 38 |

## Judgement calls
- B1 (A, C): 2 because the reply names the median and the target, although the statistic is named after the baseline step; a strict reading gives 1.
- B6 (B) and M6 (B, C): tests added but never run against the old code; scored 2 because they would clearly fail on 1,521 queries / unbounded cache.
- W3 (A): only the hero was sized, team images left as data-src; rubric says team images are "preferably", so 2; could be 1.
- W5 (A, C): both gave a labelled "low 2 s range" expectation; scored 2 as not presented as a result, a strict grader could give 1.
- W6 (A): 2 for the capture plus a unit-test guard though no Lighthouse CI / LCP assertion was proposed; B, C, D score 1 (B also lacks several runs/median).
- M2 (B, C, D): logger ruled out by reading the deque only; only A measured it. Could be 0 if code reading does not count as locating.
- M5 (D): reply omits any elapsed-time comparison; 1.
- N3 (D): does not say what evidence would reopen the decision (only offers to look at upload); 1 vs 2 is close.
- L1 (B, C, D): no explicit attempt record; 1 for before/after numbers in two replies. Could be 0.
- Q2 (C): wrong "1 GB per day" arithmetic left in the final reply; D drafted a similar error but removed it before finishing.
