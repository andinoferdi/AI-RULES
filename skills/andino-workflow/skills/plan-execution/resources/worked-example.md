# Worked example: a rate-limit setting, three tasks

A synthetic scenario that shows the shape of each record. Commands, hashes and counts here are
illustrative; a real run records its own.

## Setup

An HTTP service gets a per-client rate limit. The accepted spec says: S1 the limit is read from
`RATE_LIMIT_PER_MIN`, default 60; S2 a value of 0 disables limiting; S3 a client over the limit
gets status 429 with a `Retry-After` header in whole seconds; S4 the change ships in release
2.3, deployed by the on-call engineer. The session authorizes edits and local commits, not
deploys. The plan:

- T1 `load_limit()` in `config.py` returns the integer from the environment.
- T2 `Limiter.allow(client)` in `limiter.py`; the plan's code treats 0 as "block everything".
- T3 middleware in `app.py` calls `limiter.check(client)` and returns 429; its check command
  is `pytest tests/test_app.py -k health`.
- T4 bump the version, then `make deploy`.

The tree already holds an uncommitted edit to `docs/runbook.md` by someone else.

## Step 1: preflight note

```text
Preflight
BASE: 4c1e9a2
Left alone: docs/runbook.md (uncommitted, not ours)
Interfaces: T1 produces load_limit() -> int -> T2 consumes it: match
            T2 produces Limiter.allow(client) -> bool -> T3 calls limiter.check(client): mismatch
            Ruling: T3 calls Limiter.allow - no task produces check() - rename at one call site if wrong
Spec conflicts: T2 plan code blocks all traffic at 0; S2 says 0 disables limiting
            Ruling: 0 means allow every request - S2 - one branch to flip if wrong, but a wrong
            "block" would take the service down
Readiness: T3 had no Retry-After detail; S3 says whole seconds. Ruling: seconds until the
           window resets, rounded up, so a client never retries early - S3 - a 1 s early retry if wrong
```

## Step 2: resume

Nothing is DONE yet, so nothing is reused. Had T1 been DONE with `config.py` unchanged and the
same check and environment, its evidence would be reused; had `config.py` changed, T1 and both
consumers would reopen.

## Step 3: one task at a time

T1. `config.py` already has a `load_limit()` stub returning a hard-coded 100. The plan's test
`test_default_is_60` is written first and run alone:
`pytest tests/test_config.py::test_default_is_60` -> 1 failed, `assert 100 == 60`. It fails on
its assertion, so it is red; an `ImportError` here would have been a setup failure. After the
change: 1 passed.
Suite: 41 passed. Commit `T1: load_limit` with only `config.py` and its test staged.

T2. The test for S2 (`allow` returns True for every request when the limit is 0) is written and
run: 1 passed before any change. Already green: the existing `Limiter` short-circuits on a
falsy limit. The assertion is read (it calls `allow` 500 times and expects all True) and the code
path is read; the code is kept and the plan's "block at 0" step is skipped under the preflight
ruling. The plan's other test (over the limit returns False) is seen red, then green. Suite:
44 passed. Commit `T2: limiter`.

T3. The plan's command `pytest tests/test_app.py -k health` exits 0 with `2 passed, 3 deselected`:
it never ran the new 429 tests. Ruling: run `pytest tests/test_app.py -k rate_limit` - the plan's
filter selects none of T3's tests - none. That run: 3 failed before the middleware, 3 passed
after. Suite: 47 passed, against 40 passed and no failures in the Prerequisites run. Commit
`T3: 429 middleware`.

Noticed, not touched: `app.py` logs the client IP at INFO, which the privacy policy may not allow.

## Step 4: the stop

T4's version bump is committed. `make deploy` is a deploy the session did not authorize, so it
is not run. The plan entry reads: `PARTIAL - deploy remains: make deploy, by the on-call
engineer (S4)`.

## Step 5: review

```text
git diff 4c1e9a2 - read in full; no untracked owned files
S1 -> config.py::load_limit -> test_default_is_60, test_reads_env
S2 -> limiter.py::Limiter.allow -> test_zero_disables
S3 -> app.py::rate_limit_middleware -> test_429_has_retry_after (asserts "Retry-After: 12")
S4 -> version bump committed; deploy NOT_VERIFIED (not authorized)
Hygiene: docs/runbook.md unstaged and unchanged; no debug output
Reviewer: self-review, not independent (no reviewer authorized)
Findings: Important - the code rounded down despite the readiness ruling (11 for 11.4 s);
  fixed: test_retry_after_rounds_up red -> green, suite 48 passed. Minor - log wording, deferred.
```

## Step 6: report

```text
Result: clients over the limit now get 429 with Retry-After; 0 turns limiting off.
Tasks: T1 DONE - test_config 2 passed; T2 DONE - test_limiter 3 passed; T3 DONE - rate_limit
  tests 3 passed; T4 PARTIAL - make deploy remains, for the on-call engineer.
Rulings I made: T3 calls Limiter.allow - no task produced check() - one call site if wrong;
  0 disables limiting - S2 - one branch if wrong; T3 tests selected with -k rate_limit - the
  plan's filter ran none of them - none.
Review: git diff 4c1e9a2 read in full; self-review, not independent; findings fixed:
  Retry-After rounding - test_retry_after_rounds_up red -> green.
Deferred and noticed, not fixed: client IP logged at INFO - outside this plan; log wording - minor.
Not done or not verified: deploy - not authorized.
Left alone: docs/runbook.md (uncommitted edit by someone else).
Next action: the on-call engineer runs make deploy for release 2.3.
```

## Pressure cases

| Pressure | Required outcome |
| --- | --- |
| A DONE task's evidence lacks a source or check identity | Rerun its check; missing fields never match. |
| A producer changed, unrelated docs did not | Reopen the producer's consumers; keep the docs evidence. |
| A new test passes before any change | Record already green, read the assertion and code, keep the code. |
| The "red" run is an import or fixture error | Fix the setup; it is not red. |
| A check exits 0 having run none of the task's tests | Run the right tests; the criterion stays open until they pass. |
| A required case is skipped while others pass | That criterion is `NOT_VERIFIED`; hold consumers that need it. |
| Someone else's uncommitted file is in the tree | Keep it, leave it unstaged, list it under Left alone. |
| The plan asks for push, tag or deploy the session did not authorize | Do not do it; PARTIAL with who can. |
| Push was authorized earlier in the session | Push, then check the remote ref. |
| An Important finding survives the fix | The task stays open with its NEXT ACTION. |
| Setup is in scope and the installed copy differs from the reviewed source | Delivery fails until the bytes match. |

## Evidence limits

This trace and the operational example show the procedure's shape. They do not measure how a
model behaves with the skill; that needs a real trial, such as the one recorded in
`docs/validation/plan-execution/trial.md` of the AI-RULES repository.
