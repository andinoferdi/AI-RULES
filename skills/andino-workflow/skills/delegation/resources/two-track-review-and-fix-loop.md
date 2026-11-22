# Two-Track Review and Bounded Repair

Internal Andino resource. Risk-scaled review is about useful proof, not a fixed
number of reviewers or rounds. The parent owns final acceptance.

## 1. Inspect specification, then quality

For each criterion record: requirement/value -> implementation path/symbol ->
observed test/artifact evidence -> PASS / FAIL / UNVERIFIED. Check missing, extra
and misunderstood behavior. Only then assess quality and material risks, including
effects omitted from the spec. One approved reviewer covers both tracks.

Parent reads the owned diff and proof for every task. Risky state/security/race/
renderer/data/money/migration changes add one approved independent reviewer.
Other work uses parent review and appropriate tests/artifact checks. Review
reports do not substitute for the parent's observation.

UNVERIFIED means identify a focused proof action. If it cannot run, keep the
affected criterion blocked and name the unavailable observation. It cannot be
silently treated as approval or optional debt. DONE_WITH_CONCERNS gets the same
consequence-based triage.

| Finding | Disposition |
| --- | --- |
| Critical: security/data loss, broken contract, required acceptance failure | Must resolve before acceptance. |
| Important: real edge-case failure, fragile behavior/test with material consequence | Resolve with targeted proof before acceptance. |
| Minor: optional naming, cosmetic polish or unsupported preference | Defer with reason; do not extend the loop. |

## 2. Pin the actual change

`review_package.py PLAN BASE HEAD` verifies and packages a nonempty committed
range (log, stat, unified diff). It does not include staged, unstaged or untracked
changes and does not scope out another lane's commits automatically. Parent
inspects ownership and supplies any missing current files as a pinned snapshot.
Use it from the correct worktree; never manufacture commits just to feed a helper.

Reviewers may inspect narrow related callers to validate a concrete interface.
A diff package is an entry point, not a ban on checking consequential context.

## 3. Evidence-driven repair, at most five rounds

1. Identify the specific open criterion/finding and evidence behind it. Reject
   demonstrated false positives with a grounded ruling; do not reject real failures
   merely because a round budget is low.
2. Select a targeted fix and covering test/artifact check. Prefer the same lane
   worker/context when active and authorized. A stopped/failed/quota-limited child
   requires go-ahead before resumption. No automatic relaunch or escalation.
3. Parent can take over after the worker relinquishes ownership; record the
   transfer, preserve partial edits and apply the same gates. No concurrent writers.
4. Observe the focused check and review the fix diff plus impacted consumers.
   Do not reopen untouched areas for cosmetic preferences.
5. Update remaining findings, content identity, evidence and NEXT ACTION.

Stop earlier if another round has no new evidence. Five is an upper ceiling, not
an entitlement to five retries. An agent/model/effort replacement requires a new
approved proposal; round four does not trigger one automatically.

## 4. Circuit breaker and rulings

At the cap preserve unmet acceptance and stop that repair path. Continue unrelated
ready work only when independent. Record:
`Ruling: <decision> — <evidence/spec basis> — <cost and affected scope if wrong>`.

- Demonstrated false positive: close with concrete code/test evidence.
- Optional improvement: defer with consequence and reason.
- Real required defect: keep task incomplete, name the exact blocker, and revise
  the grounded plan or ask for missing user-owned decision/authority.
- Interface change: update producer/consumer contracts and invalidate affected
  evidence before dependent execution.

A ruling never waives required acceptance, security or data correctness.

## 5. Parent integration and final review

Parent reruns the wave's public integration gate on current combined bytes before
accepting the tasks. Capture source/check/environment identity; a worker's local
PASS cannot establish the joint result. Review the whole owned change once tasks
meet their gates. Choose a single approved final reviewer only when risk/utility
justifies it; otherwise perform a distinct two-track self-review and disclose that
it is not independent. Capable/high is a justified option, not a default.
