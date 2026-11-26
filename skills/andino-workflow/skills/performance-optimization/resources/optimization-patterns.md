# Optimization patterns

Open the section for the bottleneck gate 2 named, when you reach that code. Each pattern gives
the signature to recognize it, the fix, what the fix must keep, and how to prove it. Apply one
per attempt.

## Repeated queries (N+1)

Signature: query count grows with the number of rows returned; time is mostly round-trips.

```python
# Before: one query per comment for its author
comments = db.execute("SELECT id, author_id, body FROM comments WHERE post_id = ?", (post_id,))
for c in comments:
    author = db.execute("SELECT name FROM users WHERE id = ?", (c["author_id"],)).fetchone()

# After: one joined query, same rows in the same order
rows = db.execute(
    "SELECT c.id, c.body, u.name AS author FROM comments c "
    "JOIN users u ON u.id = c.author_id WHERE c.post_id = ? ORDER BY c.id", (post_id,))
```

With an ORM, eager-load the relation (`select_related`/`prefetch_related`, `joinedload`/
`selectinload`, `include`). When a join would multiply rows, fetch the children in one
`WHERE parent_id IN (...)` query and group them in memory. Keep: the same filter (tenant,
permissions), the same order, the same empty-relation behaviour. Prove: compare output before and
after; guard with a test that the query count stays constant as rows grow.

## Unbounded reads

Every list endpoint has a limit and a stable order (`ORDER BY created_at, id`), with cursor or
keyset pagination for deep pages; offset pagination gets slower with depth. Select the columns the
caller uses, not `*` on wide rows.

## Queries that ignore their index

"Add an index" is a guess; the plan is the measurement.

- Sequential scan where an index was expected: check that the predicate can use it. A function on
  the column (`lower(email) = ?`) needs an expression index; a leading wildcard (`LIKE '%x'`) needs
  trigram or full-text search; a value that matches most rows is legitimately scanned.
- Estimated rows off by an order of magnitude: statistics are stale; run `ANALYZE` before adding
  anything.
- Sort above the scan: a composite index with equality columns first, then the range or sort
  column, can return rows already ordered.
- A rare value inside a common column: a partial index serves it.
- An index costs every insert and update. Rerun the plan after adding it; a plan that did not
  change means the index goes.

## Connection pool exhaustion

Signature: every endpoint slows at once, time is spent waiting for a connection, the database
shows mostly idle sessions. One pool per process; `instances x max` stays under the database's
connection limit. Find what holds connections: long transactions, work done while holding one, a
missing release or `await`. With many short-lived instances (serverless, autoscaling), put a
multiplexing proxy (PgBouncer, RDS Proxy) in front rather than raising `max`; a bigger pool moves
the queue into the database. Set an acquisition timeout so exhaustion fails loudly.

## Caching

Cache what is expensive to produce and read far more often than it changes. Caching an
already-fast call adds a hop and a staleness bug.

- **Layer.** In-process (fastest, per instance, inconsistent across instances), shared
  (Redis/Memcached, consistent, a network hop), HTTP/CDN (static and public responses).
- **Key.** Every input that changes the result belongs in the key: tenant, user or role,
  permissions, locale, feature flags, query parameters. A key missing one serves one viewer's
  data to another. A key containing a per-call unique value (request id, timestamp) never hits
  and grows without bound.
- **Invalidation.** Choose one: TTL with a stated staleness window, event or tag invalidation on
  writes, or versioned keys. Say the window to the requester.
- **Stampede.** On a hot key, coalesce concurrent misses behind one in-flight load, or serve stale
  while one request refreshes.
- **Negative results.** Cache "not found" with a short TTL; never cache errors from the origin.
- **Bounds.** Size or entry limit with an eviction policy; watch hit rate and memory.
- **Never cached:** values that must be exact at the moment of use, such as balances,
  permission decisions, stock at checkout, and anything an audit or invoice reads.

```python
import functools

@functools.lru_cache(maxsize=1024)          # bounded; key = the arguments
def exchange_rates(day: str, base: str) -> dict:
    return load_rates_from_provider(day, base)
```

`lru_cache` on a method keys on `self` and keeps every instance alive; cache a module-level
function of plain arguments instead.

## Memory growth

Signature: traced memory rises with requests at constant load and does not fall after collection.
Common sources: unbounded caches and registries, keys that never repeat, listeners or callbacks
added per request and never removed, global lists used as queues, closures holding large objects,
reference cycles with finalizers. Prove with an allocation snapshot diff between equal workloads
(see measurement-and-diagnosis.md); fix the source rather than capping it when the cap would turn
every call into a miss. Guard: after N calls with distinct inputs, the structure's size or traced
memory stays under a stated bound.

## CPU and complexity

- Measure work at two input sizes. Membership tests in a list inside a loop, nested scans,
  repeated sorting and string concatenation in a loop grow quadratically; a set or dict lookup, a
  single sort, and `"".join(parts)` keep them linear.
- Move invariant work out of loops (compiled patterns, parsed configuration, lookups).
- Batch I/O: one request for many items instead of one per item.
- Move heavy work off the request path: precompute, queue, or stream, when the result's freshness
  allows it.

```python
seen = set()                          # was: seen = [] with "if key in seen"
unique = []
for item in items:
    key = item["sku"].lower()
    if key not in seen:
        seen.add(key)
        unique.append(item)           # first occurrence wins, order kept
```

## Startup and import time

Measure from process start, cold and warm apart. Python: `python -X importtime -c "import app"
2> imports.txt` lists cumulative import time per module; move rarely used heavy imports into the
function that needs them. Node: `node --cpu-prof` on startup, or measure `require` time. Defer
work that is not needed for the first response (warm caches in the background, connect lazily).

## Front-end runtime

- **Bundle size.** Split by route and lazy-load heavy, rarely used features; bundlers already
  tree-shake named ESM imports, so change import style only when the bundle analysis shows it.
- **Re-renders.** Objects and functions created during render are new on every render and
  re-render every child that receives them. Hoist constants; memoize only what the profiler shows
  is expensive.
- **Long tasks.** Batch DOM reads before writes, animate `transform` and `opacity`, split work
  over 50 ms into chunks that yield (`setTimeout`, `scheduler.yield` where supported) or move it
  to a worker.
- **Long lists.** Virtualize lists of hundreds of rows or more.

## After any pattern

Remeasure with the baseline's command and conditions, compare outputs, run the tests, and record
the attempt row: keep, revert or inconclusive.

Provenance: independently worded adaptation of Addy Osmani's `performance-optimization`
(addyosmani/agent-skills 783c41e, MIT); notice in [../references/license.md](../references/license.md).
