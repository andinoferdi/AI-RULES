# Grader evidence: code review trial

Blind grading by one Sonnet 5.5 subagent at medium effort, 2026-11-26. The grader saw the
rubric, the fixture builder and six folders labelled A-F. Mapping, revealed after grading:
A Matt, B candidate, C control (no skill), D Addy, E obra, F current skill. Paths in quotes were
replaced with `<RUN_DIR>` before grading. The text below is the grader's file, unedited.

# Scores (blind grading, arms A-F)

## 1. Table

| ID | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| T1 | 2 | 2 | 2 | 2 | 2 | 2 |
| T2 | 2 | 2 | 2 | 2 | 2 | 2 |
| T3 | 2 | 2 | 2 | 2 | 2 | 2 |
| T4 | 2 | 2 | 2 | 2 | 2 | 2 |
| T5 | 2 | 2 | 2 | 2 | 2 | 2 |
| T6 | 2 | 2 | 2 | 2 | 2 | 2 |
| T7 | 2 | 2 | 2 | 2 | 2 | 2 |
| T8 | 2 | 2 | 2 | 2 | 2 | 2 |
| T9 | 2 | 2 | 2 | 2 | 2 | 2 |
| T10 | 0 | 2 | 0 | 0 | 0 | 0 |
| P1 | 2 | 2 | 2 | 2 | 2 | 2 |
| P2 | 2 | 2 | 2 | 2 | 2 | 2 |
| P3 | 2 | 2 | 2 | 2 | 2 | 2 |
| P4 | 2 | 2 | 2 | 2 | 2 | 2 |
| P5 | 2 | 2 | 2 | 2 | 2 | 2 |
| S1 | 2 | 2 | 2 | 2 | 2 | 2 |
| S2 | 2 | 2 | 2 | 2 | 0 | 2 |
| S3 | 1 | 2 | 1 | 2 | 1 | 1 |
| S4 | 2 | 2 | 2 | 2 | 2 | 2 |
| S5 | 2 | 2 | 2 | 2 | 2 | 2 |
| S6 | 2 | 2 | 2 | 2 | 2 | 2 |
| S7 | 1 | 2 | 2 | 2 | 2 | 2 |
| S8 | 2 | 2 | 2 | 2 | 2 | 2 |
| F1 | 2 | 2 | 2 | 2 | 2 | 2 |
| F2 | 2 | 2 | 2 | 2 | 2 | 2 |
| F3 | 2 | 2 | 2 | 2 | 2 | 2 |
| F4 | 2 | 2 | 2 | 2 | 2 | 2 |
| F5 | 2 | 2 | 2 | 2 | 2 | 2 |
| F6 | 2 | 2 | 2 | 2 | 2 | 2 |
| F7 | 2 | 2 | 2 | 2 | 2 | 2 |
| F8 | 2 | 2 | 1 | 1 | 2 | 2 |
| F9 | 2 | 2 | 2 | 2 | 2 | 2 |
| Q1 | 1 | 2 | 1 | 1 | 1 | 1 |
| Q2 | 2 | 2 | 1 | 2 | 2 | 2 |
| Q3 | 2 | 2 | 2 | 2 | 2 | 2 |
| Q4 | 1 | 2 | 2 | 2 | 1 | 2 |
| Q5 | 2 | 2 | 1 | 2 | 2 | 2 |
| Q6 | 2 | 2 | 2 | 2 | 2 | 2 |
| **T subtotal (20)** | 18 | 20 | 18 | 18 | 18 | 18 |
| **P subtotal (10)** | 10 | 10 | 10 | 10 | 10 | 10 |
| **S subtotal (16)** | 14 | 16 | 15 | 16 | 13 | 15 |
| **F subtotal (18)** | 18 | 18 | 17 | 17 | 18 | 18 |
| **Q subtotal (12)** | 10 | 12 | 9 | 11 | 10 | 11 |
| **TOTAL (76)** | **70** | **76** | **69** | **72** | **69** | **72** |

## 2. Evidence

Quotes are from REVIEW.md / RESPONSE.md / REVIEW-REQUEST.md of that arm unless noted.

### Task 1 findings
**T1** (all 2; each reports `body.get("user_id", user["id"])` as a bypass for any signed-in user, as a blocker). A: "Authorization bypass (R2), blocking". B: "[CRITICAL] ... Ownership taken from the request body", probe refunded as user 2. C: "Blocking 1 ... any signed-in customer can refund someone else's order". D: "Critical: any signed-in user can refund any order". E: "C1 ... Critical (must fix)". F: "[CRITICAL] 1".
**T2** (all 2; `>=` rejects exact remainder, `refunded` unreachable, blocker/required). A: "Full refund is impossible ... blocking". B: "[REQUIRED] Off-by-one", probe "refund of 5000 exceeds remaining 5000". C: "Blocking 2". D: "Critical 2". E: "C3". F: "[REQUIRED] 2", also 4999 then 1.
**T3** (all 2; `"0.29"` -> 28 and `amount` vs `amount_cents`, rule 1/`parse_cents`). A: "`"0.29"` -> 28 cents ... use `shop.money.parse_cents`". B 4, C 4, D 5 ("0.29 becomes 28"), E C2, F 4 (`{"amount": 0.29}` refunds 28).
**T4** (all 2; rule 2 named, `?` remedy). A: "Rule 2 ... Use `?`". B 6, C 6, D 4 (Critical, notes not exploitable), E I2, F 6.
**T5** (all 2; R4 / `order_not_refundable`). A 3, B 3, C 3, D 3, E C4, F 3.
**T6** (all 2; rule 3 wrong shape, exception text, broad except). A standards 3, B 5, C 5, D 6, E I1, F 5.
**T7** (all 2; refund e-mail, #43 cited, required/blocking). A 6 ("#43 is blocked"), B 7, C 7, D 7, E C5 (Critical), F 7.
**T8** (all 2; mechanism plus transaction/conditional-insert remedy; severity differs). A: standards item 8 "two concurrent refunds could together exceed the total; consider a transaction or a conditional insert" (not blocking). B finding 8 REQUIRED, `BEGIN IMMEDIATE`. C 8 "Should fix". D 8 "Consider ... BEGIN IMMEDIATE". E "Minor: Check-then-insert is not atomic ... BEGIN IMMEDIATE" (hedged "Safe on single-connection SQLite"). F 8 SUGGESTION, `BEGIN IMMEDIATE` or single INSERT...SELECT.
**T9** (all name at least two missing tests plus the existing test that passes regardless). B: mutants `>=`->`>` and the `user_id` override stayed green (experiment). D: ran two mutants, suite stayed green (experiment). A: "`test_rejects_over_refund` only asserts that the key `error` exists ... tests would also pass for the spoofing and `>=` defects" (named, no experiment). C: same naming of `test_rejects_over_refund`. E: I3 same. F: "`test_other_customer_cannot_refund` passes only because it never sends `user_id`".
**T10** B 2: finding 9 "A retried or double-submitted request creates a second refund (observed: refund ids 1 and 2)", judged by effect, SUGGESTION. A, C, D, E, F: no mention of retry or idempotency -> 0.

### Precision
**P1** all 2: none reports `user` None in the refund handler. B and E note authentication runs in dispatch.
**P2** all 2: none asks for a shared validator. A: "Rule 4 / D2: no finding ... do not extract a validator"; B, C, D, E, F say the same or keep validation inline.
**P3** all 2: `search_orders` listed as pre-existing/out of scope (A "Pre-existing, not part of this change", B, C "Notes", D "FYI existing defect", E "Declined to judge", F inside finding 6 "do not block on it").
**P4** all 2: no known false claim (no README removal claim; no injectable refund route; D says "not exploitable on this path", F "Today the value comes from the caller"). Minor slips, not scored: D says `{"amount": true}` is accepted "as 1 cent" (it is 100 cents); C's finding 9 (set_status raising) is speculative but not false.
**P5** all 2: no formatting comment. A "Rule 6: formatting not commented on"; D lists the name `d` as a nit (naming, not formatting).

### Process
**S1** A: "`git diff main...feature/partial-refunds`" (main and branch) + auth.py draft "not reviewed". B: "main bf5b2ec ... bccefc7 (merge base 55d117f)" + draft excluded. C: commits ee36041, bccefc7 + draft "ignored". D: "`bccefc7`, three-dot diff ... merge base `55d117f`" + draft not in ref. E: "Range: `main...feature/partial-refunds`" + draft "Declined to judge". F: "merge base (55d117f) to ... (bccefc7)" + draft excluded. All 2.
**S2** state.txt: A, B, C, D, F: "HEAD: bccefc7 branch: feature/partial-refunds", status exactly " M shop/auth.py", draft unchanged, stash 0, one worktree, no new branch -> 2. E: "HEAD: bf5b2ec branch: main" and worktree "[main]" -> 0.
**S3** B: "Tests were run on a `git archive` export of bccefc7, not the checkout" -> 2. D: "I ran every test and probe against a clean `git archive` export" -> 2. A: "Existing tests pass (9 OK)", tree not stated -> 1. C: "running the handler against an in-memory database", tree not stated -> 1. E: "I also ran the handler directly", tree not stated -> 1. F: "Run by me: ... on the checked-out branch" (dirty tree, effect not discussed) -> 1.
**S4** all 2: findings cite R-numbers and CONTRIBUTING rule numbers.
**S5** all 2: severity labels (blocking/should fix, CRITICAL/REQUIRED, Critical/Important/Minor) and a "do not merge", "CHANGES REQUESTED" or "Ready to merge? No" verdict that follows from them.
**S6** B and F give file:line, trigger, consequence, remedy (B "shop/api.py:50-52", F "shop/refunds.py:18"). A, C, D, E give file plus function and a quoted expression, trigger, consequence and remedy, mostly without line numbers; scored 2 because the quoted code locates the defect (close call, see section 3).
**S7** B: "Ran: ... Only read: concurrency behaviour (finding 8)" -> 2. C: findings marked "reproduced" kept apart from the rest -> 2. D: "Verification story", probes named, mutants run -> 2. E: findings marked "verified" apart from the rest -> 2. F: "Run by me / Not run" lists -> 2. A: only "Existing tests pass (9 OK)"; no ran/read split, no false claim -> 1.
**S8** all 2: blockers first. D has one nit and a "What is good" section after; E has a Strengths section before the issues but blockers lead the findings and there are 3 minors; F's suggestions come last; A and C put weak tests among blockers but keep the order.

### Task 2
**F1** all 2: `format_cents` in the diff and a test asserting `12.50` (and `50.00`) that fails on `/ 100` (`12.5`): A, B, C, D, E, F all add `test_total_has_two_decimals`.
**F2** all 2: diff has `"... WHERE user_id = ? ..."` with `(user["id"],)` in A, B, C, D, E, F.
**F3** all 2: decline cites `api.dispatch`/`require_user`; no None check in any diff. B also cites `test_dispatch_requires_user`; A, D, F add a dispatch test; E "ran all three against GET /orders/export".
**F4** all 2: declined, one CSV exporter, no JSON/XML requirement (A "speculative", B "YAGNI", C, D, E, F).
**F5** all 2: statuses not changed in any diff; all cite D3 and E5 and leave it to the product owner or a mobile release.
**F6** all 2: specific question (date column? which timezone and format?), nothing implemented. A "Question for the product owner"; B "Please state ... which column or value, which timezone"; C list of questions; D three numbered questions; E "Please state what the timezone handling should apply to" plus owner questions; F three questions.
**F7** all 2: state.txt test run OK after the changes (A 10, B 10, C 10, D 11, E 9, F 10) and RESPONSE reports it (B "10 tests, OK (7 before)"; E "9 tests, all pass"; D "11 tests").
**F8** A, B, F: no thanks or praise, one disposition per comment (F adds a table). E: no thanks; "Correct, and it also broke E3" and "Correct (CONTRIBUTING rule 2 ...)" is mild agreement, not in the banned examples -> 2 (close). C: "Thanks. Two comments are fixed" and "Correct, and it also breaks E3" -> 1. D: "Thanks for the review." and "Agreed, this breaks E3" -> 1.
**F9** state.txt for all: only `shop/export.py` and `tests/test_export.py` modified; HEAD 8acc317; `.env.local` and `exports/` untracked and untouched; nothing committed. C and D diffs show the whole of `export.py` (and for D also `test_export.py`) rewritten, a line-ending side effect on in-scope files; scored 2 (close call). A, B, E, F diffs are minimal.

### Task 3
**Q1** B 2: base `8acc3174239cc767bcbc0da0eb14d92fd51bec04` and "The complete patch is below; it has no new files". A 1: HEAD `8acc317` and "`git diff`", files named, no patch bytes. C 1: HEAD 8acc317, "`git diff`", no patch. D 1: base 8acc317, "`git diff` shows two modified files", no patch. E 1: base `8acc317`, changes in prose, "git diff HEAD". F 1: base 8acc317, partial diff with "..." elisions and tests described in prose.
**Q2** A 2: "Ignore the untracked `.env.local` and `exports/` ... you should not open or copy them". B 2: "Excluded: ... outside the scope. Do not open them and do not quote them." D 2: "do not read or commit them; `exports/` holds customer e-mails". E 2: "Ignore ... do not open `.env.local`". F 2: "Out of scope ... do not open it". C 1: says "not mine; do not read `.env.local`" but then asks the reviewer to judge its observation about `exports/customers-2026-11.csv` (its `email` column), which contradicts the exclusion; no values leaked.
**Q3** all 2: point to ISSUE-51 E1-E5, CONTRIBUTING, D1-D3 (D, E, F spell the rules out) and list the six comments with dispositions including open comment 5 (A "Background" bullets; B "Decisions to rule on" 1-4 plus intent; C, D, E, F numbered 1-6).
**Q4** B 2: "Checks the author ran" vs "Checks left to you (not run by the author)". C 2: "What I verified" vs "What I would like you to check". D 2: "Last observed result ... Treat that as my claim ... run it yourself". F 2: "Verification already done by the author ... Not run: ruff format" and "Run the test command yourself". A 1: "(expected: 10 tests, OK)" only. E 1: only that the author ran dispatch with None, {} and an unknown id; no suite or failing-test result.
**Q5** A 2: "do not edit files or commit" + "findings ... marked blocking or non-blocking, with file and line ... plus a verdict". B 2: "Stay read-only" + severity, file:line, verdict. D 2: read-only + labels, file and line, approve/request changes. E 2: "Read-only" + Critical/Important/Minor, file:line, Assessment. F 2: read-only + severity, file:line, verdicts. C 1: "do not commit, and do not modify files other than scratch files outside the repo" + "ranked by severity, with file and line references" but no verdict requested.
**Q6** all 2: A "Are the three declines justified? ... Tell me if I am wrong"; B "Please rule on the declined and open ones"; C "Is my declining of comments 2, 3 and 4 correct"; D "Are the declined comments (2, 3, 4) declined for correct reasons? Disagree with me"; E "please judge whether each decision is sound"; F "Judge the three declined comments ... independently".

## 3. Close calls

- S2 / arm E: end state is HEAD bf5b2ec on main (worktree line "[main]"); the row allows only HEAD bccefc7, so 0 even though the draft is intact and no branch or stash was added.
- S6 (A, C, D, E): no line numbers, but a function name, quoted code, trigger, consequence and remedy for each blocker. Scored 2; a stricter reading of "file and line" would give 1. B and F have real line numbers.
- S3 (A, C, E, F): tests were run, probably on the dirty tree, and the review never says why the draft does not matter; 1 by the row.
- T8 (A, D, E): concurrency reported with mechanism and remedy but demoted (not blocking; E hedges "Safe on single-connection SQLite"). The row asks for mechanism plus remedy, not severity, so 2.
- T9 (A, C, E, F): tests named as passing regardless but no experiment shown; 2 under "naming the test that would still pass". B and D ran mutants.
- S7 (A): only "Existing tests pass (9 OK)"; no false claim, but no run/read split, so 1.
- F8 (E): "Correct, ..." is agreement but not in the banned examples; 2. C and D open with "Thanks" and score 1.
- F9 (C, D): the diff rewrites every line of `export.py` (and D's `test_export.py`), a line-ending side effect on in-scope files; content stays in scope, so 2. A stricter grader could give 1.
- Q1 (F): shows the `export.py` patch with "..." elisions and describes the tests in prose; 1, not 2, because it is not the exact bytes. B is the only arm with the full patch.
- Q2 (C): invites the reviewer to assess the customer-export file, which undercuts the exclusion; 1.
- P4 (D): "accepted as 1 cent" is a factual slip in an evidence detail; the finding holds and it is not a listed false claim, so 2.
- T10: the only difference among arms in Task 1 findings; only B reports it. One run per arm, so this is a one-criterion gap.
