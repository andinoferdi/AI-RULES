# Handoff: retry policy, ticket NET-12

## Resume here

Implement step 3 of `docs/plan.md` (full jitter) in the `retrykit` repository, branch `main`,
at commit {BASE}. Progress is tracked in the plan's Checkpoint section; update it there.

## Current state and evidence

- Steps 1 and 2 are committed. `python -m unittest -q` ran 5 tests, all passing, at {BASE}.
- Nothing is staged or uncommitted.

## Decisions and boundaries

- Full jitter (`delay = rng() * min(cap, base * 2 ** attempt)`), not equal jitter: the
  gateway's clients reconnect together after an outage, and full jitter spreads them out the
  most.
- The random source is a parameter, `rng=random.random`, so tests can pass a fixed function.
  Existing exact-value tests pass `rng=lambda: 1.0`.
- `retrykit/config.py` belongs to ops. Do not change it; changes go through an OPS ticket.
- No new dependencies.

## NEXT ACTION

Add a failing test `test_backoff_full_jitter_uses_rng` to `tests/test_policy.py` that calls
`backoff(3, rng=lambda: 0.25)` and expects `1.0`, then add the `rng` parameter to
`retrykit.policy.backoff`. Expect every test to pass.
