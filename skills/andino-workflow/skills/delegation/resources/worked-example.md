# Worked example: a plan where two lanes pay

Internal Andino resource for `andino-delegation`. A synthetic run, written to show the artifacts in
order; nothing here ran. Paths, numbers and agent output are scenario inputs. The rules it applies
are in [the rules](contract.md) and the prompts it fills are in
[briefs and prompts](subagent-brief-and-report-schemas.md).

## The plan and the cost decision

Accepted spec: partner API v2. Partners get signed API keys that rotate, and a monthly usage report
as CSV. The accepted plan has nine tasks on branch `feature/partner-v2`:

| Task | Depends on | Files | Size |
| --- | --- | --- | --- |
| 1 Settings keys | none | `config/settings.toml`, `src/partner/settings.py` | 15 lines, values given |
| 2 Key model and store | 1 | `src/partner/keys/store.py`, `tests/keys/test_store.py` | ~120 lines |
| 3 Key signing and verification | 2 | `src/partner/keys/sign.py`, `tests/keys/test_sign.py` | ~130 lines, security |
| 4 Key rotation endpoint | 3 | `src/partner/api/keys.py`, `src/partner/api/__init__.py`, `tests/api/test_keys.py` | ~100 lines |
| 5 Usage event model | 1 | `src/partner/usage/events.py`, `tests/usage/test_events.py` | ~60 lines, code given |
| 6 Monthly aggregation | 5 | `src/partner/usage/aggregate.py`, `tests/usage/test_aggregate.py` | ~180 lines |
| 7 CSV report renderer | 6 | `src/partner/usage/report.py`, `tests/usage/test_report.py` | ~150 lines |
| 8 Report endpoint | 4, 7 | `src/partner/api/reports.py`, `src/partner/api/__init__.py`, `tests/api/test_reports.py` | ~90 lines |
| 9 API docs | 8 | `docs/partner-api.md` | ~40 lines |

Decision, per task: Tasks 1, 8 and 9 stay with the parent (small, or the place where both domains
meet). Tasks 2-4 (keys) and 5-7 (usage) are two independent domains of roughly 350 and 390 lines
with separate files; each becomes a lane. Two lane workers and one reviewer cost about 180k tokens
of start-up against about 740 lines of work that can proceed side by side while the parent keeps its
context for integration. That pays. A worker per task (six workers) or a reviewer per task would not.

## Pre-flight table

| Pair or task | Produces / consumes | Found | Ruling |
| --- | --- | --- | --- |
| 1 and 2, 1 and 5 | Task 1 provides `settings.KEY_TTL_DAYS`, `settings.REPORT_TZ` | names match | none |
| 4 and 8 | both edit `src/partner/api/__init__.py` (router) | same file | Task 8 by the parent after Task 4 is accepted |
| 5 and 6 | 6 consumes `UsageEvent(partner_id, at, units)` | types match | none |
| 2 | key lifetime 30 days | spec section 3 says 90 days | `Ruling: KEY_TTL_DAYS = 90 — spec section 3 — one constant if wrong` |
| 6 | "group by month" | spec section 4: calendar months in UTC | aggregation uses UTC boundaries; recorded in the brief |
| 7 | test expects header `Units` | spec table says `Billable units` | `Ruling: header "Billable units" — spec section 5 — one string if wrong` |

## The envelope

> I'd run this plan with 3 subagents, at most 2 running at once:
>
> - K, implementer, lane keys (Tasks 2, 3, 4): sonnet, medium. Owns `src/partner/keys/`,
>   `src/partner/api/keys.py`, `tests/keys/`, `tests/api/test_keys.py`.
> - U, implementer, lane usage (Tasks 5, 6, 7): sonnet, medium. Owns `src/partner/usage/`,
>   `tests/usage/`. Task 5's code is given, but 6 and 7 work from prose, so the lane needs the mid tier.
> - R, reviewer for Task 3 (key signing, security): sonnet, medium, plus one scoped re-review per fix
>   round.
>
> Fix-round cap: 5, stopping earlier when a round brings nothing new. I do Tasks 1, 8 and 9, read
> every task's diff, and do the final whole-change review myself, disclosed as not independent. Two
> independent domains run side by side for about 180k tokens of start-up.
>
> Following the spec over the plan: key lifetime 90 days (plan said 30) and the report header
> "Billable units". The run stops for a product decision the spec leaves open, a failed or stopped
> agent, or anything needing an install, a push or a merge. Reply yes to approve this list; anything
> outside it I will ask about first.

The user says yes. The journal records the envelope line.

## Brief and dispatch for lane K

`python scripts/task_brief.py docs/plans/partner-v2.md 2` copies Task 2; the parent completes it:

```markdown
# Task 2 — Key model and store   (lane keys)
Outcome: keys are created, looked up by id and revoked; expired keys are never returned
Spec and plan: docs/spec/partner-v2.md sections 2-3; docs/plans/partner-v2.md Task 2
Global constraints: "Keys expire after 90 days." "No new runtime dependency."
Rulings that bind this task: Ruling: KEY_TTL_DAYS = 90 — spec section 3 — one constant if wrong
Working directory and BASE: /work/partner (feature/partner-v2), BASE 4c1e2d8, no uncommitted files
Owned paths: src/partner/keys/store.py, tests/keys/test_store.py; must not touch: src/partner/api/
Uses: settings.KEY_TTL_DAYS (Task 1, accepted at 4c1e2d8)
Provides: create(partner_id) -> Key; get(key_id) -> Key | None; revoke(key_id) -> None
Acceptance: get() of a key created 89 days ago returns it; at 90 days returns None; revoke then get
  returns None; unknown id returns None
Proof: python -m pytest tests/keys/test_store.py -q from /work/partner; 4 tests, all pass
Report: /work/partner/.andino/delegation/partner-v2/task-2-report.md
Limits: no subagents; no writes outside owned paths; no weakened tests; no install, push or publish;
  commit on feature/partner-v2 with the task id in the message
```

```text
description: Lane keys: Task 2 store
model: sonnet
effort: medium
prompt: |
  This lane builds partner API keys; Tasks 3 and 4 follow in this same lane after review.
  Read /work/partner/.andino/delegation/partner-v2/task-2-brief.md first. It is your requirements;
  use its exact values verbatim.
  [Implementer section from the prompts resource, unchanged.]
  Write your full report to /work/partner/.andino/delegation/partner-v2/task-2-report.md. Reply
  only with the short return.
```

Lane U gets the same shape for Task 5. Both start at once: they pass the collision checks.

## Review of Task 3 and a fix round

K returns DONE on Task 3. The parent reads the diff and the report: the RED run shows two failing
assertions with 6 tests selected, the GREEN run 6 passed. It packages the range
(`python scripts/review_package.py docs/plans/partner-v2.md 9a0b1c2 f3d4e5a`) and dispatches R with
the reviewer prompt, naming the risks: constant-time comparison, expiry boundary, malformed tokens
raising the module's error. The prompt states the 90-day ruling as a fact and says nothing about
what not to flag.

R returns: Spec PASS; Important `src/partner/keys/sign.py:41` compares signatures with `==`; Minor
naming of `kid`. The parent confirms the Important finding in the diff, logs the Minor one as
deferred, and sends the Important finding verbatim to K, which is listed and idle after returning
normally, for its own task. K switches to `hmac.compare_digest`, adds a test that a one-byte change
in the signature is rejected, reruns `tests/keys/test_sign.py` (7 passed) and appends the fix report.
R's scoped re-review: ADDRESSED, no new breakage. Journal:

```text
Task 3: minor (deferred): rename kid to key_id
Task 3: fix round 1/5 (1 addressed, 0 open; commits f3d4e5a..b6c7d8e)
Task 3: complete (commits 9a0b1c2..b6c7d8e, review clean)
```

The parent accepts Task 3 and starts K on Task 4, which is now on the frontier.

## A return with a concern

U returns DONE_WITH_CONCERNS on Task 6: "Partners in UTC+7 will see the last seven hours of a month
in the next month's report. I used UTC as the brief says. Confirm?" The concern is about
correctness, so the parent resolves it before review: spec section 4 settles it (calendar months in
UTC), so the code stands. Journal: `Ruling: Task 6 keeps UTC month boundaries — spec section 4 — a
boundary change in one function if the product owner disagrees`. The user hears about it in the
final report; no question is needed now because the spec answers it.

## Integration and finish

After Tasks 4 and 7 are accepted, the parent does Task 8 (it shares the router with Task 4) and
Task 9, runs `python -m pytest -q` on the integrated branch (212 passed) and calls both endpoints
against the test server. The final review is the parent's own two-track pass over
`git merge-base main HEAD..HEAD`, disclosed as not independent, pointed at the deferred `kid` rename.
It finds one Important issue (the report endpoint returns 500 for a partner with no usage instead of
a header-only CSV). One fix, by the parent, with a test; one re-check; no second wave.

Final report excerpt:

```text
Not verified: report generation with more than 100k events (no fixture that large).
Deferred: Task 3 rename kid to key_id (Minor).
Rulings I made:
1. KEY_TTL_DAYS = 90, not the plan's 30 — spec section 3 — one constant if wrong
2. CSV header "Billable units", not "Units" — spec section 5 — one string if wrong
3. Task 6 keeps UTC month boundaries — spec section 4 — one function if the product owner disagrees
```

## Contrast: a small plan

A seven-task plan of 18 to 200 lines per task, where tasks share `tests/conftest.py` and the CLI
module, gets no implementer: one start-up costs more than most tasks. The parent does it inline and
asks, at most, for one reviewer on the security-sensitive task. Two task IDs alone never justify two
workers or a merger.

## Recovery without hidden spend

Suppose the context resets while K is idle after Task 3 and U has stopped on a usage limit midway
through Task 7:

1. Read the plan and the journal; list live agents; inspect U's partial bytes and report. Check that
   Task 3's recorded commits and checks still match before reusing them.
2. Record Task 7's state and U's stop in the plan.
3. U stopped on a limit, so ask the user before resuming it, with its model and effort, or take Task 7
   over inline once its partial edits are attributed and kept.
4. K is listed and idle; it may start Task 4 as the envelope allows. Nothing accepted is redispatched.
