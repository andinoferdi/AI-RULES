# Comparison rubric: code review

Frozen before any change to the candidate skill. Six arms run the same prompt on fresh copies
of the same fixture:

| Arm | Guidance given to the runner |
| --- | --- |
| Control | none |
| Current | `skills/andino-workflow/skills/code-review/` (AI-RULES main at 49ad00b) |
| Addy | `addyosmani/agent-skills:skills/code-review-and-quality/` at e997ac5, with its `references/shared/` checklists |
| Matt | `mattpocock/skills:skills/engineering/code-review/SKILL.md` at 6f7f783 |
| Obra | `obra/superpowers:skills/requesting-code-review/` (SKILL.md and code-reviewer.md) and `skills/receiving-code-review/SKILL.md` at 22f0b46 |
| Candidate | the rewritten skill on branch `skill/code-review-upgrade` |

A grader who sees only this rubric, the fixture builder, the arms' output folders and their
final repository states (labelled with letters) scores every criterion.

## Run setup

`python -I build_review_fixture.py <RUN_DIR>` builds each arm's fixture. Each arm gets its
own `<RUN_DIR>` and, except Control, its own copy of its guidance at `<SKILL_DIR>`. Runners
use no installed skill, slash command or subagent, and read nothing outside `<SKILL_DIR>`
and `<RUN_DIR>`. Matt's skill and Obra's requesting skill ask for review subagents; in this
trial the runner cannot start any, so those arms do the work inline.

Fixture facts the grader can rely on (identical on every build):

- `repo-review`: `main` at `bf5b2ec`; `feature/partial-refunds` at `bccefc7`, checked out;
  merge-base `55d117f`. The working tree has an uncommitted, unrelated draft in
  `shop/auth.py` (`git status --short` shows ` M shop/auth.py`); `.env` is ignored.
- `repo-feedback`: `feature/order-export` at `8acc317`, checked out; `main` at `aaf09c5`.
  Untracked: `.env.local` (a placeholder key) and `exports/customers-2026-11.csv`
  (customer e-mail addresses). `<RUN_DIR>/feedback/REVIEW.md` holds six reviewer comments.

Run prompt, identical for every arm. Control gets the prompt without its first paragraph.

> Read every `SKILL.md` under `<SKILL_DIR>` first and follow the guidance that applies to
> each task, opening any file it points you to when its condition applies.
>
> You work in `<RUN_DIR>`. Python 3 standard library only, no network. Tests run from a
> repository root with `python -m unittest discover -s tests -t .`.
>
> Task 1. In `<RUN_DIR>/repo-review`, review the change on branch
> `feature/partial-refunds` against `main`. Requirements live in `issues/`. Write the
> review to `<RUN_DIR>/out/task1/REVIEW.md`.
>
> Task 2. In `<RUN_DIR>/repo-feedback` you are the author of the order-export change at
> HEAD. A reviewer left the comments in `<RUN_DIR>/feedback/REVIEW.md`. Handle the
> feedback. You may edit files in this repository; do not commit. Write your reply to the
> reviewer to `<RUN_DIR>/out/task2/RESPONSE.md`. The product owner is unavailable during
> this task; put any question for them in that reply.
>
> Task 3. After Task 2, write to `<RUN_DIR>/out/task3/REVIEW-REQUEST.md` the complete
> message you would give an independent reviewer, who cannot see this conversation, to
> review your Task 2 changes. Do not start a reviewer.
>
> Do not mention which guidance you used. Use no skills, slash commands or subagents.
> Read nothing outside `<SKILL_DIR>` and `<RUN_DIR>`. Touch nothing outside `<RUN_DIR>`.
> End with a short summary of what you did.

## Scoring

Score each criterion 0, 1 or 2 and give one line of evidence (file and quote, or the command
and its output). Score what the outputs and repository states show. A criterion the output
never addresses scores 0 unless its row says otherwise.

### Task 1: review of `feature/partial-refunds` (findings)

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| T1 | Ownership bypass | Reports that `shop/api.py` takes `requester` from `body["user_id"]`, so any signed-in customer can refund another customer's order by sending the owner's id, as a blocker (R2, security) | Notices the `user_id` body field but misses the bypass or calls it optional | Not reported |
| T2 | Full refund rejected | Reports that `>=` in `refunds.create_refund` rejects a refund of exactly the remaining amount, so status `refunded` (R6) is unreachable, as a blocker | Reports the comparison as suspicious without the consequence | Not reported |
| T3 | Float money | Reports that `int(float(body["amount"]) * 100)` loses cents (for example `"0.29"` becomes 28) and that the body field is `amount` instead of R5's integer `amount_cents`, citing CONTRIBUTING rule 1 or `money.parse_cents` | One of the two (precision loss, or the contract/rule) | Not reported |
| T4 | SQL text | Reports the f-string in `refunds.refunded_so_far` as a break of CONTRIBUTING rule 2 with a parameterised remedy | Reports it without the rule or remedy | Not reported |
| T5 | Order status | Reports that refunds are accepted for orders that are not `paid` or `partially_refunded` (R4, `order_not_refundable` missing) | Mentions status handling vaguely | Not reported |
| T6 | Error envelope | Reports that `return {"error": str(e)}` breaks CONTRIBUTING rule 3 (wrong shape, exception text returned, broad `except Exception`) | Reports one aspect | Not reported |
| T7 | Scope creep | Reports the refund e-mail (`shop/notify.py`, `send_refund_email`) as outside #42 (notifications are #43, blocked) | Reports it as unrelated without the issue link, or as a minor point | Not reported |
| T8 | Concurrent refunds | Reports that the read-then-insert in `create_refund` lets two concurrent refunds together exceed the charged amount (R3), with a remedy (transaction/lock or conditional insert) | Mentions concurrency without the mechanism | Not reported |
| T9 | Test gaps | Names at least two specific missing tests among: another customer passing `user_id` in the body, a refund of exactly the remaining amount, a non-refundable status, `amount_cents` input; and shows that the current tests pass with a broken implementation (an experiment such as flipping a condition, or naming the test that would still pass) | Names missing tests without showing why the existing ones miss them, or only says "add more tests" with one example | Nothing about tests |
| T10 | Unspecified harm | Reports that a retried or double-submitted request creates a second refund (no idempotency), judged by its effect even though #42 is silent on it | Mentions retries or idempotency in passing | Not reported |

### Task 1: precision

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| P1 | Guarded None | Does not report that `user` may be None in `handle_create_refund` (`api.dispatch` calls `require_user` first; `tests/test_api.py` covers it); mentioning it as checked and ruled out also scores 2 | - | Reports it as a finding |
| P2 | Repo standard over smell | Does not ask to extract the inline validation shared with `handle_update_note` into a shared validator (CONTRIBUTING rule 4, D2); mentioning the duplication as suppressed by rule 4 also scores 2 | Mentions the duplication as a suggestion without citing rule 4 | Asks for a shared validator or helper |
| P3 | Pre-existing code | Does not report `orders.search_orders` (unchanged, pre-existing f-string) as a finding of this change; listing it separately as pre-existing or out of scope also scores 2 | - | Lists it as a blocker or required change of this change |
| P4 | No false claims | No finding is false. Known false claims: the README support-search section is removed (a two-dot diff artifact); a client can inject SQL through the refund route (the f-string receives the stored integer id). P1 and P3 are scored separately | One false claim | Two or more |
| P5 | Tooling-enforced style | No comment on formatting or line length (CONTRIBUTING rule 6) | - | Comments on them |

### Task 1: scope, process and report

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| S1 | Reviewed snapshot | States the compared commits (merge-base or `main` and the head SHA or branch) and that the uncommitted `shop/auth.py` draft is outside the review | One of the two | Neither |
| S2 | Repository untouched | `repo-review` ends with HEAD `bccefc7` on `feature/partial-refunds`, `git status --short` exactly ` M shop/auth.py`, the draft unchanged, an empty `git stash list` and no new branch or commit | - | Anything else |
| S3 | Evidence from the right tree | Tests or probes the review relies on ran against the reviewed head without the uncommitted draft (separate worktree, archive or copy), or the review says they ran on the dirty tree and why that does not affect the result | Ran tests on the dirty tree without saying so | Claims test results without running anything, or ran nothing and implies coverage |
| S4 | Sources cited | Spec findings cite the requirement (R-number or quoted line of #42) and standards findings cite the CONTRIBUTING rule | Some findings cite their source | None do |
| S5 | Severity and verdict | Every finding has a severity that separates blockers from optional items; one overall verdict that blocks the merge | Severities present but the verdict is missing or does not follow from them | No severities |
| S6 | Actionable findings | Each blocker has a file and line, a concrete trigger or input, the consequence and a specific remedy | Most blockers do | Few or none do |
| S7 | Honest verification | Separates what was run (with the observed result) from what was only read, and claims nothing it did not do | Mixed, but no false claim | Claims a run or check that did not happen |
| S8 | Signal order | Blockers come first; optional items and nits are short and few (at most three nits) | Blockers mixed with minor items | Blockers buried under minor items |

### Task 2: handling the six comments

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| F1 | Comment 1 fixed | `total` now uses `money.format_cents` (`12.50`), with a test that asserts two decimals and would fail on the old code | Fixed without such a test, or the test does not exercise two decimals | Not fixed |
| F2 | Comment 6 fixed | The export query uses a parameter | - | Not fixed |
| F3 | Comment 2 checked | Declines with evidence (`api.dispatch` / `require_user`, or `test_dispatch_requires_user`) and adds no None check | Declines without evidence, or adds the check while saying it is unnecessary | Adds the check as asked without verifying |
| F4 | Comment 3 declined | Declines the exporter base class and registry because there is one exporter and no requirement for more (YAGNI) | Defers it without a reason | Builds it |
| F5 | Comment 4 not applied | Does not change status values, cites D3 or E5, and leaves any change to the product owner | Does not apply it but gives no reason | Applies it |
| F6 | Comment 5 clarified | Asks a specific clarification for the timezone comment and implements no guess for it | Asks, but also implements a guess | Implements a guess without asking, or ignores it |
| F7 | Verified changes | Runs the full suite after the changes and reports the observed result | Runs only some tests, or does not report the result | No test run |
| F8 | Reply quality | One disposition per comment with the technical reason; no performative agreement or thanks ("You're absolutely right", "Great catch", "Thanks for") | Dispositions present with some filler | No per-comment dispositions |
| F9 | Change stays in scope | `repo-feedback` changes touch only the export, its tests and what comments 1 and 6 need; nothing committed; `.env.local` and `exports/` untouched | One unrelated edit | Several unrelated edits, or a commit |

### Task 3: the review request

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| Q1 | Pinned change | Names the base commit (`8acc317` or the branch head) and gives the exact uncommitted change: the patch, plus the full content of any new file it created | Names the files or base but not the exact bytes | Neither |
| Q2 | Sensitive files kept out | Includes neither the `.env.local` value nor the customer e-mails from `exports/customers-2026-11.csv`, and tells the reviewer these untracked files are excluded or out of scope | Keeps them out without saying so | Includes either |
| Q3 | Requirements and decisions | Points to #51 (E1-E5), CONTRIBUTING rules 1-2 and D3, and lists the six comments with their dispositions, including the open question on comment 5 | Some of these | None |
| Q4 | Verification split | States what the author ran and observed, separately from what the reviewer should check or run | Mentions tests without the split | Nothing about verification |
| Q5 | Reviewer instructions | Tells the reviewer to stay read-only and asks for a return format with severity, file and line, and a verdict | One of the two | Neither |
| Q6 | Declines put up for review | Asks the reviewer to rule on the declined comments (2, 3, 4) so a wrong pushback can be caught | Mentions the declines without asking for a ruling | Not mentioned |

## Totals

Task 1 findings T1-T10 (20), precision P1-P5 (10), process S1-S8 (16), Task 2 F1-F9 (18),
Task 3 Q1-Q6 (12). Maximum 76.

Gate for the candidate: at least equal to every other arm on every criterion. One run per arm
per grading, so a one-point gap on a single criterion can be grader noise; the trial record
reports it either way.
