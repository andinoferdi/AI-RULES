---
name: andino-api-and-interface-design
description: Use when designing or refactoring APIs, module boundaries, HTTP endpoints, boundary contracts, error shapes, or atomic idempotency. Operates under Andino Workflow governance.
---

# API and Interface Design

Internal method ID: `andino-api-and-interface-design` (alias: `api-and-interface-design`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: single durable checkpoints, proportional investigation, and anti-loop guards.
> Selected skills own their full procedures, resource contracts, and verification checks. Do not re-invoke `andino-workflow` recursively.

Define stable, observable public seams and make retries safe under concurrent delivery. Good interfaces make correct usage natural and unsafe usage impossible.

## 1. Dominant Negative Gates (When NOT to Use)

Reject this skill immediately if ANY condition holds:
- **Private Variable / Cosmetic Changes**: Renaming variables inside isolated functions or formatting code.
- **Speculative Abstraction**: Introducing interfaces where only one implementation exists and no variation is planned.
- **Unbounded Macro Survey**: Whole-codebase architectural friction audits without a targeted seam (use `andino-architecture-survey`).
- **Styling Only**: Pure CSS or design-token modifications without component prop contract changes.

## 2. Tri-Modal Selection Router

| Current Need | Resource | Exclusion |
| :--- | :--- | :--- |
| HTTP endpoints, REST semantics, Zod edge validation, atomic idempotency | [http-contracts](resources/http-contracts/guide.md) | In-memory function interfaces |
| Deep module architecture, seam placement, high leverage over complex logic | [module-depth](resources/module-depth/guide.md) | Shallow pass-through wrappers |
| Layer boundaries, import path enforcement, cycle elimination | [import-enforcement](resources/import-enforcement/guide.md) | Single-file scripts without packages |

## 3. The 5 Floor Invariants

1. **Perimeter Validation Only**: Untrusted external data (requests, env, 3rd-party APIs) must be strictly parsed at the edge (e.g. Zod `safeParse`). Internal domain code trusts typed contracts; never scatter defensive checks internally.
2. **Atomic Concurrency Gate**: Check-then-act (`SELECT` then `INSERT`) is a concurrency bug. The database `UNIQUE` constraint on the idempotency key *is* the concurrency gate.
3. **Guarded Payload Hash**: Reusing an idempotency key with an altered payload is a client bug; immediately fail with `409 Conflict`. Never silently replay stale responses.
4. **Uniform Error Envelope**: All error responses follow a single predictable shape: `{ error: { code, message, details? } }` with mapped HTTP status codes. Never leak raw stack traces or ORM models.
5. **Additive Evolution**: Apply the One-Version Rule. Add new optional properties; never mutate or delete existing fields without an expand/contract migration cycle.

## 4. Canonical Representation Anchor

```typescript
export type OrderId = string & { readonly __brand: 'OrderId' };
export const CreateOrderSchema = z.object({
  customerId: z.string().min(1),
  amount: z.number().int().positive(),
  priority: z.enum(['LOW', 'MEDIUM', 'HIGH']).default('MEDIUM'),
});
export type OrderStatus =
  | { state: 'PENDING'; initializedAt: Date }
  | { state: 'COMPLETED'; completedAt: Date; transactionId: string };
export interface APIError { error: { code: string; message: string; details?: unknown } }
```

## 5. Anti-Rationalization Refutations

| Rationalization Shortcut | Mechanical Reality & Required Response |
| :--- | :--- |
| *"We don't need pagination for now."* | Collections grow inevitably. Naked arrays cause OOMs. Paginate from day one. |
| *"A quick SELECT before INSERT is enough."* | TOCTOU race: concurrent retries both pass SELECT and duplicate side effects. |
| *"Accepting the header is enough."* | The header is merely a declaration. The database unique constraint is the mechanism. |
| *"PATCH is complicated; let's use PUT."* | PUT forces full-object replacement and overwrites concurrent edits. Use PATCH. |
| *"Nobody relies on undocumented behavior."* | Hyrum's Law: Every observable behavior becomes a contract. Never leak internals. |

## 6. Diagnostic Red Flags (Stop Immediately)

- [ ] Action verbs in REST paths (`/api/createOrder` instead of `POST /api/orders`).
- [ ] Endpoints returning unpaginated arrays or inconsistent error payload shapes.
- [ ] Scattered manual validation checks inside domain logic instead of at the boundary.
- [ ] Idempotency keys generated per-attempt (e.g. UUID/timestamp) rather than from intent.
- [ ] Performing `SELECT` before `INSERT` to check idempotency keys.
- [ ] Exporting private implementation helpers purely to satisfy unit tests.

## 7. Progressive Disclosure Router

- Complete multi-layer architecture guide: [GUIDE.md](GUIDE.md)
- REST semantics, Zod edge validation, and atomic idempotency: [resources/http-contracts/guide.md](resources/http-contracts/guide.md)
- Deep module design and seam leverage: [resources/module-depth/guide.md](resources/module-depth/guide.md)
- TypeScript package entrypoint rules: [resources/import-enforcement/guide.md](resources/import-enforcement/guide.md)
- 10 rationalization refutations and 12-point checklist: [resources/anti-rationalization-and-failure-modes.md](resources/anti-rationalization-and-failure-modes.md)
- Worked before/after transformation study: [resources/worked-example.md](resources/worked-example.md)

## 8. Runnable Operational Contract & Verification Harness

```python andino-operational-example
import hashlib, json, os, sqlite3, sys
from pathlib import Path

def test_idempotent_contract():
    db_path = Path("idempotency_harness.sqlite")
    if db_path.exists():
        try: db_path.unlink()
        except OSError: pass
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE intents (key TEXT PRIMARY KEY, hash TEXT, state TEXT)")
    conn.close()
    def handle_intent(key, payload):
        h = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        c = sqlite3.connect(db_path, timeout=5)
        try:
            c.execute("BEGIN IMMEDIATE")
            row = c.execute("SELECT hash, state FROM intents WHERE key = ?", (key,)).fetchone()
            if row: return "replayed" if row[0] == h else "conflict"
            c.execute("INSERT INTO intents VALUES (?, ?, ?)", (key, h, "succeeded"))
            c.commit()
            return "applied"
        finally:
            c.close()
    r1 = handle_intent("charge:ord_1", {"amt": 100})
    r2 = handle_intent("charge:ord_1", {"amt": 100})
    is_neg = os.environ.get("ANDINO_NEGATIVE") == "1"
    r3 = handle_intent("charge:ord_1", {"amt": 200 if not is_neg else 100})
    if db_path.exists():
        try: db_path.unlink()
        except OSError: pass
    if is_neg and r3 != "conflict":
        sys.stderr.write("Verification failed: expected conflict on payload mismatch\n")
        sys.exit(1)
    if not is_neg and (r1 != "applied" or r2 != "replayed" or r3 != "conflict"):
        sys.stderr.write(f"Verification failed: unexpected results r1={r1}, r2={r2}, r3={r3}\n")
        sys.exit(1)
    print(json.dumps({"applied": 1, "replayed": 1, "conflict": 1, "status": "CONTRACT_VERIFIED"}))
    sys.exit(0)

if __name__ == "__main__":
    test_idempotent_contract()
```

## 9. Provenance

Adapted and elevated from `addyosmani/agent-skills: skills/api-and-interface-design`, integrated with John Ousterhout deep-module theory and Andino Workflow governance. Substantive upstream material covered by MIT notice in [references/license.md](references/license.md).
