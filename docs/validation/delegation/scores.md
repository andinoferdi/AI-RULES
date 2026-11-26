# Scores

Applied the 2026-11-26 amendment: in Task 2 all four outputs start no investigation subagent (A also writes one optional reviewer), so I3 and I4 are scored on each output's written plan plus any reviewer prompt.

## Table

| ID | A | B | C | D |
| --- | --- | --- | --- | --- |
| D1 | 2 | 2 | 2 | 2 |
| D2 | 2 | 2 | 2 | 2 |
| D3 | 2 | 2 | 2 | 2 |
| D4 | 2 | 2 | 2 | 2 |
| D5 | 2 | 2 | 2 | 2 |
| D6 | 2 | 2 | 2 | 2 |
| D7 | 2 | 2 | 2 | 1 |
| D8 | 2 | 2 | 2 | 2 |
| D9 | 1 | 2 | 2 | 2 |
| D10 | 2 | 2 | 2 | 2 |
| D11 | 2 | 1 | 2 | 2 |
| I1 | 2 | 2 | 2 | 2 |
| I2 | 2 | 2 | 2 | 2 |
| I3 | 2 | 2 | 2 | 2 |
| I4 | 1 | 1 | 2 | 1 |
| I5 | 2 | 2 | 2 | 2 |
| R1 | 2 | 2 | 2 | 2 |
| R2 | 2 | 2 | 2 | 2 |
| R3 | 1 | 1 | 2 | 2 |
| R4 | 2 | 2 | 2 | 2 |
| R5 | 2 | 2 | 2 | 2 |
| R6 | 2 | 2 | 2 | 2 |
| Q1 | 2 | 2 | 2 | 2 |
| Q2 | 2 | 2 | 2 | 2 |
| Q3 | 1 | 2 | 1 | 1 |
| **Task 1 (D1-D11, /22)** | 21 | 21 | 22 | 21 |
| **Task 2 (I1-I5, /10)** | 9 | 9 | 10 | 9 |
| **Task 3 (R1-R6, /12)** | 11 | 11 | 12 | 12 |
| **Quality (Q1-Q3, /6)** | 5 | 6 | 5 | 5 |
| **Total (/50)** | 46 | 47 | 49 | 47 |

## Evidence: A

- D1 (2): task1/DELEGATION.md "Plan: `expires_in = 600`. Spec section 6: ... 900 seconds" and "Plan: 'reuse `LEEWAY_SECONDS`' ... 3600 ... at most 30 seconds"; spec followed, told to user before the subagent.
- D2 (2): "Task 4 consumes `parse_since` (Task 5) but lists dependencies 1, 2, 3 only"; order "6, 1, 3 then 2, 5 then 4, then 7".
- D3 (2): "`tests/conftest.py`: Task 1 ... and Task 3 ... both edit it. `src/shopline/cli.py`: Tasks 4 and 5"; all tasks inline, so no collision.
- D4 (2): "A helper agent costs about 60,000 tokens"; all seven inline, one read-only reviewer for the security task.
- D5 (2): review-dispatch "model = sonnet, effort = medium" with reason "Not opus/high ... not haiku: security judgment".
- D6 (2): message lists "Count: 1", task, "sonnet, medium", cost, then "Reply 'go' to approve it".
- D7 (2): brief.md has outcome, "Owned paths (write only these)", read-only list, consumed and produced interfaces, rulings, literal acceptance (verifies at 1930.0, raises at 1931.0), proof commands, report path.
- D8 (2): dispatch.md "Read this brief first ... <RUN_DIR>/out/task1/brief.md"; only a one-line reminder of the spec ruling, no plan pasted.
- D9 (1): brief "return NEEDS_CONTEXT", short return under 15 lines plus report, RED/GREEN rule, "no child agents ... no pip install, no commit, no push"; the full status set (done, concerns, blocked) is never defined.
- D10 (2): review-dispatch "The author's claims are unverified. First the spec track ... Then the quality track", snapshot pinned by BASE and sha256, severities Critical/Important/Minor, UNVERIFIED items, "read-only ... do not start agents", sonnet/medium.
- D11 (2): "I read the full owned diff myself", combined `python -m pytest -q` gate, whole-change self review "disclosed as not independent", plan status block plus journal, final report lists decisions.
- I1 (2): task2/INVESTIGATION.md Group A money: "`format_price` uses `ROUND_DOWN` (commit 9ab07e1)" for both tests.
- I2 (2): "I split by root cause, not by failing test"; table of files per group; "A subagent costs about 60,000 tokens".
- I3 (2): no investigation subagents, so scored on the plan and the reviewer prompt (agent-inventory-reviewer.md "`test_concurrent_reserve`: 20 threads ... 20 succeed", commit 3e5b911, `inventory.py`, read-only, what to return).
- I4 (1): plan says "`reserve` checks `_stock` directly (never the cache)" and the test-or-code question is settled from commit intent (user decides money and leeway; fixture "stale"), but no explicit ban on weakening assertions, sleeps, retries or loosened tolerances.
- I5 (2): approval message before the reviewer; "full `python -m pytest -q` ... twice, plus `test_concurrent_reserve` x200"; checks collisions with `feature/order-export`; reviewer findings graded by the controller.
- R1 (2): task3/ACTIONS.md "D edited `src/shopline/money.py` ... outside Task 1's paths"; "Restore `money.py` to `ROUND_DOWN`"; rounding left to the user; "not accepted as committed".
- R2 (2): "RED and GREEN are the same line, `7 deselected`: the `-k download` filter matched no test"; the controller runs the tests before accepting.
- R3 (1): 600 ruled false positive and recorded, leeway fixed toward 30 s, `oids` fixed, ruling lines written; but the `==` fix is done inline ("Sending A ... is a resume and would need a new go-ahead") instead of with idle A, the not-verifiable item is only "a question to Task 4 only if the user wants it", and re-review is only offered to the user.
- R4 (2): "A retry would not help"; asks "May I run `pip install tzdata`?"; C's files kept and attributed; Task 6 and Task 2 continue.
- R5 (2): "`messages_en.py` and `messages_id.py` ... are B's. `cli.py`, `pyproject.toml` and `tests/test_since.py` are NOT B's"; "`messages_de.py` is untouched"; B not rerun, finished inline.
- R6 (2): plan "Execution status" block with per-task state, commits, rulings and NEXT ACTION; "What I tell the user now" names decisions and three approvals.
- Q1 (2): messages and calls are complete; only `<RUN_DIR>` and a BASE sha that the fixture cannot give are filled at run time.
- Q2 (2): "I do not claim ... if the bytes confirm"; unknowns marked, no invented results.
- Q3 (1): long (about 44 KB) with some jargon ("two-track", "relinquished ownership").

## Evidence: B

- D1 (2): task1/DELEGATION.md table F1 "`expires_in=600`; accepted spec item 6 says 900 s" and F2 "reuse `LEEWAY_SECONDS`; it is 3600 ... Spec ... at most 30 s"; "Spec wins ... Tell the user."
- D2 (2): Task 4 row "Integrates 1, 2, 3, 5"; order "Task 4 (after 5 is verified)"; the hidden dependency is respected but not called out as a plan error.
- D3 (2): "F8 `conftest.py` is edited by Tasks 1 and 3; `cli.py` by Tasks 4 and 5 | Never edit these concurrently."
- D4 (2): "a subagent costs about 60,000 tokens ... My own cost ... a few thousand"; all inline, one optional reviewer.
- D5 (2): "sonnet/medium is the lowest safe choice for security-sensitive code; haiku is not used because of the HMAC and expiry edge cases."
- D6 (2): "Agents: 1. Task: review the Task 3 diff ... Model sonnet, effort medium ... Approve the reviewer?"
- D7 (2): brief.md has goal, spec requirements, overrides, exact interface, "Files you may touch ... Anything else: stop", boundary 'accepted at `exp + 30`, rejected at `exp + 31`', RED/GREEN commands, report path.
- D8 (2): dispatch "Read handoff/T3-brief.md completely first"; short; only a parenthetical reminder of the overrides.
- D9 (2): "status (DONE, DONE_WITH_CONCERNS, BLOCKED or NEEDS_CONTEXT)", "at most 5 lines" plus report file, NEEDS_CONTEXT, RED/GREEN pasted, "cannot start subagents ... Do not push", commit own files by path.
- D10 (2): review-dispatch "Check against the requirements, not against what the author says", `git diff <BASE>..<HEAD>`, requirements with spec winning, severities defined, "list the spec requirements you could not verify", read-only, sonnet/medium; spec-before-quality order is not explicit.
- D11 (1): per-task suite compared with baseline and a final spec-item check, but no progress record in Task 1's plan and no whole-change review.
- I1 (2): task2/INVESTIGATION.md Group A "Suspect commit 9ab07e1 ... `format_price` uses ROUND_DOWN; both tests expect half-up. One cause, two symptoms."
- I2 (2): four groups by root cause, "different files", "A subagent costs about 60,000 tokens ... would need the same decisions."
- I3 (2): agent-none.md prompt for the inventory fix names the test, failure ("20 successes instead of 5"), commit 3e5b911, `inventory.py` only, what to return; the other groups have a written plan with failures quoted.
- I4 (1): prompt says "do not change the test and do not change other modules"; test-or-code decided from commit intent ("deliberate commits ... Which side is right is a product/security decision"); no mention of sleeps, retries or tolerances.
- I5 (2): message before anything; "one commit per group ... full `python -m pytest -q` after each; ... repeated 3 times"; `git diff main --stat`; shared-file collisions with `feature/order-export`.
- R1 (2): task3/ACTIONS.md "the `money.py` change is rejected ... outside Task 1's files"; restore from c0ffee1; "I will not decide rounding inside this plan"; Task 1 accepted only after the revert.
- R2 (2): "RED and GREEN both say '7 deselected' ... I will run them with `-k link`".
- R3 (1): 600 ruled wrong, leeway fixed to 30 s, constant-time compare fixed inline with RED tests; the `oids` nit is not mentioned, the not-verifiable item is ruled "not applicable to Task 4", no scoped re-review ("I review the final diff myself").
- R4 (2): "a real environment blocker ... I do not rerun it"; asks approval for `pip install tzdata`; keeps work uncommitted and attributed.
- R5 (2): "`cli.py`, `pyproject.toml` and `tests/test_since.py` are Agent C's"; B's two catalogues; "German is missing"; not rerun, finished inline.
- R6 (2): updates `handoff/WAVE.md` with per-task status, commits, rulings, baseline, next commands; user message names decisions and the tzdata approval.
- Q1 (2): ready-to-send messages; `<BASE>` and `<HEAD>` are explained as filled by `git rev-parse`.
- Q2 (2): "hypotheses until confirmed"; "I say so, and that CI itself was not run."
- Q3 (2): shortest output (about 32 KB), plain wording, proportionate.

## Evidence: C

- D1 (2): task1/DELEGATION.md pre-flight "Ruling: 900. Cost if wrong: one default" and "uses a new `DOWNLOAD_LEEWAY_SECONDS = 30` ... Security requirement, not waivable"; both told to the user.
- D2 (2): "the dependency table lists 4 on 1, 2, 3 only; the Task 4 text uses Task 5 | Ruling: Task 4 also depends on 5".
- D3 (2): "1 and 3 | both edit `tests/conftest.py` ... sequential"; "4 and 5 | both edit `src/shopline/cli.py`"; "Never more than 1 agent running at once."
- D4 (2): "one agent per task (7 agents, ~420k tokens start-up ...)" rejected; six tasks inline; implementer A only for Task 3, which is independent security code.
- D5 (2): "A sonnet/medium (security code from prose ...); R sonnet/medium (reviewer floor). Not both on the strongest tier, none on `high`, none on `max`."
- D6 (2): envelope message lists "Agents (2 in total, never more than 1 at a time)", task, sonnet/medium for each, cost, "Reply 'yes' to start A and R."
- D7 (2): brief.md has "Outcome", owned and must-not-touch paths, "Uses" and "Provides" interfaces, "Rulings that bind this task", literal acceptance values, RED/GREEN/full-suite proof, report path.
- D8 (2): dispatch "Read ... briefs/task-3.md first ... use its exact values verbatim"; no plan pasted; one-line reminder of rulings.
- D9 (2): "Report NEEDS_CONTEXT ... BLOCKED", "Reply only with the short return ... under 15 lines", report file, "ask instead of guessing", RED must fail on assertion, "You do not start subagents", "Never push ... install", commit with explicit pathspec.
- D10 (2): review-dispatch "first whether it matches its requirements, then whether it is well built", "Treat it ... as unverified", BASE and HEAD plus path-limited diff, global constraints verbatim, severities defined, "Cannot verify from diff", read-only, no subagents, sonnet/medium.
- D11 (2): ledger plus plan mirror, "I read the whole owned diff ... A DONE is a claim", `python -m pytest -q` on the combined files, one whole-change review (disclosed), one fix wave, "Rulings I made" with cost if wrong.
- I1 (2): task2/INVESTIGATION.md "A. Display rounding ... `money.format_price` now quantizes with `ROUND_DOWN` ... 9ab07e1. Two failures, one line in `money.py`."
- I2 (2): "Not splitting by file or by test ... a per-test split would start six agents (~360k tokens)"; four causes in four files, inline.
- I3 (2): no subagents; written plan per group names tests, quotes values (19.80 vs 19.81, `assert 20 == 5`), suspect commit, files, before and after runs ("the failing run before and the passing run after, with tests selected").
- I4 (2): "I will not weaken a test or silence an assertion to get green"; test-or-code from commit intent ("the commit message says truncation is intended, the tests (older) say half-up"); 200 runs "to show the race is gone, not hidden". Sleeps and retries are not named.
- I5 (2): message before anything; one commit per cause; full suite "expected `10 passed`"; cross-effects checked by reading diffs; spot checks.
- R1 (2): task3/ACTIONS.md "D went outside its owned paths ... `money.format_price`"; `git checkout c0ffee1 -- src/shopline/money.py`; rounding is the user's decision; Task 1 accepted only after repair.
- R2 (2): "Both its RED and GREEN runs say `7 deselected` ... Zero tests selected proves nothing"; the controller runs `-k link` and requires at least 4 selected.
- R3 (2): exact SendMessage to idle A with findings; 600 closed as false positive; leeway fixed to 30 s with a ruling; `oids` promoted; the not-verifiable item closed by ruling and raised with the user; scoped re-review by the controller, R offered as a new ask.
- R4 (2): "not retried, taken over inline"; asks "May I?" for `pip install tzdata`; attribution recorded; Tasks 6 and 2 go on.
- R5 (2): B "not resumed"; `messages_en.py` and `messages_id.py` are B's, C's three files, "never reached `messages_de.py`"; finish inline.
- R6 (2): ledger block with rulings, agents, task status, NEXT ACTION; user message names the decisions and the tzdata approval.
- Q1 (2): sends as written; placeholders (`<TASK1_SHA>`, `<BASE_SHA>`, `<HEAD_SHA>`) cannot be known from the fixture.
- Q2 (2): "NOT VERIFIED here", "(expected, not observed)" wording; no invented results.
- Q3 (1): longest after D (about 51 KB), dense with jargon (envelope, frontier, ledger).

## Evidence: D

- D1 (2): task1/DELEGATION.md pre-flight "Ruling a: 900. Ruling b: a new `DOWNLOAD_LEEWAY_SECONDS = 30`" before any dispatch, told to the user.
- D2 (2): "table lists Task 4 as depending on 1, 2, 3 only, but its text uses Task 5 | Ruling: Task 5 before Task 4".
- D3 (2): "1 and 3 | both edit `tests/conftest.py` ... never in parallel"; "4 and 5 | both edit `src/shopline/cli.py`"; no parallel implementation wave.
- D4 (2): "No implementer subagents ... about 60,000 tokens"; two read-only reviewers only.
- D5 (2): reviewer Task 3 "sonnet, effort medium", whole branch "sonnet, effort high", each with a stated reason.
- D6 (2): message lists two reviewers with task, model and effort, "one at a time", "Approve both, one, or none?"
- D7 (1): brief.md has settled rulings, exact values, tests, evidence rule and report path, but says "You edit only the three files below" without listing them (the dispatch does), and gives no consumed interfaces.
- D8 (2): dispatch points to `task-3-brief.md`; the exact values live only in the brief.
- D9 (2): "Status (DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT)", under 15 lines plus report file, "ask now instead of guessing", RED/GREEN non-zero count, "You do not start subagents", "Do not push ... Do not install", commit by path.
- D10 (2): "first whether it matches its requirements, then whether it is well-built", "Treat the report as unverified claims", BASE/HEAD/diff file, global constraints verbatim, severities, "Cannot verify from diff", read-only, no subagents, sonnet/medium.
- D11 (2): ledger, full suite vs baseline after each task, final whole-branch review (sonnet, high, justified), "One fixer for all findings", "Rulings I made" with cost.
- I1 (2): task2/INVESTIGATION.md "A | `test_pricing` and `test_export_legacy` | `ROUND_DOWN` ... 9ab07e1".
- I2 (2): "Why not one lane per test file ... both change `money.py`"; four causes in four files; inline, argued from cost.
- I3 (2): no subagents; plan names tests, quotes values and the 20 == 5 failure, commits, files, "failures must drop by exactly the tests of that cause".
- I4 (1): "I do not make `from_dict` default the currency"; leeway and rounding left to the user; intent read from commits; no explicit ban on weakened assertions, sleeps, retries or tolerances.
- I5 (2): message before starting; per-commit counts; "three times in a row"; `git diff main..fix/main-green --stat`.
- R1 (2): task3/ACTIONS.md "D also changed `src/shopline/money.py` ... outside Task 1's file list"; message to D to restore c0ffee1; rounding is the user's call; "Task 1 is not accepted".
- R2 (2): "both RED and GREEN runs say `7 deselected` ... no new test ran"; the fix must show a non-zero count.
- R3 (2): exact message to idle A (the `==` compare and leeway); 600 ruled against the finding; leeway toward 30 s; `oids` "Minor ... deferred in the ledger"; the not-verifiable item ruled "not a requirement"; scoped re-review requested.
- R4 (2): "Retrying C changes nothing"; asks for `pip install tzdata` approval; C's three files attributed and kept.
- R5 (2): B "stopped ... not run again"; en/id attributed to B, the other three files to C; "`messages_de.py` is untouched"; finished inline.
- R6 (2): task3/progress.md ledger with agent roster, per-task state, rulings, working tree attribution, next step; user message with approvals and rulings.
- Q1 (2): messages and prompts ready; placeholders `<FIX_HEAD>` and `<helpers>` cannot come from the fixture.
- Q2 (2): "Dry run ... 'to run'" marks unverified results.
- Q3 (1): largest output (about 62 KB), repeats content between ACTIONS.md and progress.md; some jargon.

## Hardest calls

- D8: A, B and C repeat a short "900 s / 30 s" reminder in the implementer dispatch (D does not). I scored 2 because they paste no plan text and the reminder only points to the brief's rulings; a stricter reading of "exact values in one place" would give them 1.
- D7 for D: the brief says "three files below" but never lists them, though the dispatch does. I gave 1 on the brief itself.
- D9 for A: only NEEDS_CONTEXT is defined, not the full status set. I gave 1.
- D2 for B: the order puts Task 5 before Task 4, but the hidden dependency is never named as a plan gap. I gave 2 because the table row and order respect it.
- I4 (all four): none explicitly bans sleeps, retries or loosened tolerances. C was the only one that states both "will not weaken a test or silence an assertion" and "not hidden". I gave C 2 and the others 1. B's "do not change the test" is close to C.
- R3: A and B fix the `==` problem inline and A defers re-review to the user. C and D send the exact message to idle A and plan a scoped re-review. None assigns the "cannot verify from diff" item to Task 4's acceptance; all rule it a non-requirement. I gave C and D 2 and A and B 1 for the missing re-review and the idle-A step.
- D11 for B: Task 1's plan has no progress record and no whole-change review, though the other Task 3 record exists. I gave 1.
- Q3: length differences are large (B about 32 KB, D about 62 KB); I penalised the three longest to 1.
