# HTTP Endpoint Contracts and Atomic Idempotency

Resource contract; selected directly under its canonical owner.

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: single durable checkpoints, proportional investigation, and anti-loop guards. Selected skills own their full procedures, resource contracts, and verification checks. Do not re-invoke `andino-workflow` recursively.

Define bulletproof public HTTP boundaries, uniform error semantics, and concurrent-safe atomic idempotency under distributed network delivery.

## Activation & Negative Gates

- **Use when**:
  - Creating or refactoring an HTTP/REST endpoint or public API boundary.
  - Designing state-changing operations requiring retry safety (`POST`, `PUT`, `PATCH`).
  - Standardizing error response shapes or implementing boundary schema validation.
  - Designing pagination, filtering, or sorting for collection endpoints.
- **Do NOT use when**:
  - Pure in-memory module seam design without network transport (use `module-depth`).
  - Enforcing internal TypeScript package import rules (use `import-enforcement`).
  - Private function variable renaming or trivial cosmetic formatting.

## The Five HTTP Contract Invariants

1. **Perimeter Validation Only**: Untrusted external data (requests, env, 3rd-party APIs) must be strictly parsed at the edge (e.g. Zod `safeParse`). Internal domain code trusts typed contracts; never scatter defensive checks internally.
2. **Atomic Concurrency Gate**: Check-then-act (`SELECT` followed by `INSERT`) is a concurrency bug. The database `UNIQUE` constraint on the idempotency key *is* the concurrency gate.
3. **Guarded Payload Hash**: Same idempotency key with a differing payload is a client bug; immediately reject with `409 Conflict` (or `422`). Never silently replay stale responses.
4. **Uniform Error Envelope**: All error responses follow a single predictable shape: `{ error: { code, message, details? } }` with appropriate HTTP status codes. Never leak raw stack traces or ORM entities.
5. **Additive Evolution**: Apply the One-Version Rule. Add new optional properties; never mutate or delete existing fields without an expand/contract migration cycle.

## Anti-Rationalization Refutations

| Rationalization | Mandated Reality |
|---|---|
| *"We don't need pagination for now; data is small."* | **False.** Collections grow. Unbounded lists cause OOMs. Paginate from day one. |
| *"PATCH is complicated; let's just use PUT."* | **False.** PUT overwrites the entire resource. PATCH is what callers actually require. |
| *"Accepting Idempotency-Key header is sufficient."* | **False.** Header is the contract; atomic persistence with unique constraint is the implementation. |
| *"A quick SELECT before INSERT is enough."* | **False.** TOCTOU race: concurrent retries both pass SELECT and duplicate side effects. |
| *"Duplicate requests are rare."* | **False.** Retries spike precisely during dependency degradation when duplicates cost most. |

## Diagnostic Red Flags (Stop Immediately)

- [ ] Action verbs in REST paths (e.g. `POST /api/createOrder` instead of `POST /api/orders`).
- [ ] Endpoints returning naked unpaginated arrays.
- [ ] Scattered manual `if (!req.body.x)` checks instead of a single boundary schema.
- [ ] Idempotency keys generated per-attempt (e.g. `UUID()` or timestamp) instead of stable intent.
- [ ] Silently replaying an earlier response when the idempotency key is reused with a different body.
- [ ] Key retention shorter than the longest possible retry chain or dead-letter queue.

## Progressive Disclosure Resources

- [guide.md](guide.md) — Comprehensive HTTP design patterns, TypeScript interfaces, and distributed idempotency.
- [../anti-rationalization-and-failure-modes.md](../anti-rationalization-and-failure-modes.md) — Full 10-point rationalization table and 12-point verification checklist.
- [../worked-example.md](../worked-example.md) — Before/after case study in TypeScript and SQL.

## Operational Example (Offline)

```python andino-operational-example
import hashlib, json, os, sqlite3, sys

def evaluate_http_contract(req):
    if not isinstance(req, dict):
        return {"valid": False, "error": "Request must be a dict"}
    path = req.get("path", "")
    if any(verb in path.lower() for verb in ["/create", "/update", "/delete", "/get"]):
        return {"valid": False, "error": "REST paths must use nouns, not action verbs"}
    if req.get("method") in ("POST", "PUT", "PATCH") and not req.get("idempotency_key"):
        return {"valid": False, "error": "State-changing operations require idempotency key"}
    return {"valid": True, "status": "HTTP_CONTRACT_VERIFIED"}

if __name__ == "__main__":
    is_neg = os.environ.get("ANDINO_NEGATIVE") == "1"
    sample = {
        "path": "/api/orders/create" if is_neg else "/api/orders",
        "method": "POST",
        "idempotency_key": "order:v1:intent-99" if not is_neg else None,
    }
    res = evaluate_http_contract(sample)
    if not res["valid"]:
        sys.stderr.write(f"Contract violation: {res['error']}\n")
        sys.exit(1)
    print(json.dumps(res, sort_keys=True))
    sys.exit(0)
```
