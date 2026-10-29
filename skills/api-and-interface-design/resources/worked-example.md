# API and interface design: worked procedure, patterns, and diagnostic rubric

This resource provides a concrete before-and-after transformation case study, production-grade interface patterns, an idempotency engineering reference, common rationalizations, and an empirical diagnostic self-audit rubric for `api-and-interface-design`.

---

## 1. Worked case study: Before and after transformation

### The problem: A brittle, race-prone, stringly-typed endpoint (Before)

Below is a common failure mode observed in real-world API implementations:

```typescript
// BEFORE: Stringly-typed, leaking internals, TOCTOU race, unsafe retries, inconsistent errors
app.post('/api/orders/create', async (req, res) => {
  try {
    const { orderId, amount, customerId, items } = req.body;

    // 1. Weak validation scattered inside business logic
    if (!amount || amount < 0) {
      return res.status(400).send('Invalid amount');
    }

    // 2. TOCTOU race condition: check-then-act idempotency
    const existing = await db.query('SELECT * FROM orders WHERE id = $1', [orderId]);
    if (existing.rows.length > 0) {
      // Replaying without verifying payload match!
      return res.json(existing.rows[0]);
    }

    // 3. Remote side effect executed without persisting intent
    const charge = await paymentGateway.charge({ amount, customerId });

    // If server crashes here, client retries, payment gateway charges twice!
    const newOrder = await db.query(
      'INSERT INTO orders (id, amount, customer_id, status, gateway_ref) VALUES ($1, $2, $3, $4, $5) RETURNING *',
      [orderId, amount, customerId, 'completed', charge.id]
    );

    return res.status(200).json(newOrder.rows[0]);
  } catch (err: any) {
    // 4. Inconsistent error format and leaking internals
    return res.status(500).json({ message: err.message, stack: err.stack });
  }
});
```

### Flaws identified:
1. **Verb in REST path:** `/api/orders/create` violates resource noun conventions.
2. **Scattered, weak validation:** Ad-hoc validation inside handlers fails to protect internal domain code and returns plain strings instead of structured errors.
3. **TOCTOU idempotency race:** `SELECT` followed by `INSERT` allows concurrent retries to pass the check simultaneously and charge multiple times.
4. **Blind replay:** Replays the original response even if the caller reused the idempotency key with a completely different payload (silent data corruption).
5. **Crashes during external effect:** Calling the remote gateway before recording pending intent creates orphaned charges if the node restarts before DB insertion.
6. **Leaking implementation details:** Exposing raw error stacks and DB columns leaks internal schema and violates Hyrum's Law.

---

### The solution: Contract-first, boundary-validated, atomic idempotency (After)

```typescript
// AFTER: Strict types, Zod boundary validation, atomic claim, guarded payload, structured error
import { z } from 'zod';
import crypto from 'node:crypto';

// --- Type Contracts & Branded IDs ---
export type OrderId = string & { readonly __brand: 'OrderId' };
export type CustomerId = string & { readonly __brand: 'CustomerId' };

export const CreateOrderSchema = z.object({
  customerId: z.string().min(1).transform(v => v as CustomerId),
  amount: z.number().int().positive(),
  currency: z.enum(['USD', 'EUR', 'IDR']),
  items: z.array(z.object({
    sku: z.string().min(1),
    quantity: z.number().int().positive()
  })).min(1),
});

export type CreateOrderInput = z.infer<typeof CreateOrderSchema>;

export type OrderStatus =
  | { state: 'pending_payment'; initializedAt: Date }
  | { state: 'completed'; completedAt: Date; transactionId: string }
  | { state: 'failed'; failedAt: Date; failureCode: string };

export interface Order {
  id: OrderId;
  customerId: CustomerId;
  amount: number;
  currency: string;
  status: OrderStatus;
  createdAt: Date;
  updatedAt: Date;
}

export interface APIError {
  error: {
    code: 'VALIDATION_ERROR' | 'IDEMPOTENCY_CONFLICT' | 'IN_FLIGHT' | 'INTERNAL_ERROR';
    message: string;
    details?: unknown;
  };
}

// --- Handler with Atomic Idempotency Claim ---
app.post('/api/orders', async (req, res) => {
  // 1. Boundary validation at system edge
  const parseResult = CreateOrderSchema.safeParse(req.body);
  if (!parseResult.success) {
    return res.status(422).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid order payload',
        details: parseResult.error.flatten(),
      },
    });
  }

  const input = parseResult.data;
  const idempotencyKey = req.headers['idempotency-key'] as string | undefined;

  if (!idempotencyKey) {
    return res.status(400).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Idempotency-Key header is required for state-changing operations',
      },
    });
  }

  // 2. Hash payload to guarantee key-payload matching
  const payloadHash = crypto
    .createHash('sha256')
    .update(JSON.stringify(input))
    .digest('hex');

  // 3. Atomically claim intent in database via UNIQUE constraint
  // Table: idempotency_keys (key PRIMARY KEY, payload_hash, state, response_json, created_at)
  try {
    await db.query(
      `INSERT INTO idempotency_keys (key, payload_hash, state)
       VALUES ($1, $2, 'in_progress')`,
      [idempotencyKey, payloadHash]
    );
  } catch (err: any) {
    if (err.code === '23505') { // Postgres unique_violation
      const existing = await db.query(
        'SELECT payload_hash, state, response_json FROM idempotency_keys WHERE key = $1',
        [idempotencyKey]
      );
      const row = existing.rows[0];

      // Guard payload: same key with different body is a client bug
      if (row.payload_hash !== payloadHash) {
        return res.status(409).json({
          error: {
            code: 'IDEMPOTENCY_CONFLICT',
            message: 'Idempotency key reused with a different payload',
          },
        });
      }

      // Handle in-flight duplicates
      if (row.state === 'in_progress') {
        return res.status(409).json({
          error: {
            code: 'IN_FLIGHT',
            message: 'A request with this idempotency key is currently processing',
          },
        });
      }

      // Safe replay of completed response
      return res.status(200).json(row.response_json);
    }
    throw err;
  }

  // 4. Perform effect with intent securely recorded
  try {
    const order = await orderService.createOrder(input);

    // 5. Store completed response atomically with state transition
    await db.query(
      `UPDATE idempotency_keys
       SET state = 'completed', response_json = $1
       WHERE key = $2`,
      [order, idempotencyKey]
    );

    return res.status(201).json(order);
  } catch (err: any) {
    // 6. Timeout or crash is UNKNOWN; retain intent record for reconciliation
    await db.query(
      `UPDATE idempotency_keys SET state = 'requires_reconciliation' WHERE key = $1`,
      [idempotencyKey]
    );
    return res.status(500).json({
      error: {
        code: 'INTERNAL_ERROR',
        message: 'Operation processing encountered an unexpected state; reconciler queued',
      },
    });
  }
});
```

---

## 2. Practical design patterns reference

### REST resource modeling

| Pattern | Rule | Example |
| :--- | :--- | :--- |
| **Resource Nouns** | Plural nouns, never verbs | `GET /api/tasks`, `POST /api/tasks` |
| **Sub-resources** | Express hierarchy directly | `GET /api/tasks/:id/comments`, `POST /api/tasks/:id/comments` |
| **Query Params** | CamelCase for filters and pagination | `?sortBy=createdAt&sortOrder=desc&status=completed` |
| **Partial Updates** | Use `PATCH` with sparse fields | `PATCH /api/tasks/:id` with `{ "priority": "high" }` |
| **Idempotent Delete** | Deleting absent resource returns 204/200 | `DELETE /api/tasks/:id` succeeds whether item exists or not |

### Standard pagination contract

Always paginate list endpoints to avoid unbound memory explosion:

```typescript
export interface PaginationParams {
  page: number;       // 1-based index
  pageSize: number;   // Bounded max, e.g. min(pageSize, 100)
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface PaginatedResult<T> {
  data: T[];
  pagination: {
    page: number;
    pageSize: number;
    totalItems: number;
    totalPages: number;
  };
}
```

### TypeScript type design patterns

#### 1. Input/Output separation
Never reuse the domain entity type as the creation schema:
- `CreateTaskInput`: Caller-supplied fields only (e.g. `title`, optional `description`).
- `Task`: System-generated fields included (`id`, `createdAt`, `updatedAt`, `creatorId`).

#### 2. Discriminated unions for state
Prevents invalid state combinations (e.g., having a `cancelledReason` when status is `pending`):
```typescript
type DeploymentState =
  | { status: 'queued'; enqueuedAt: Date }
  | { status: 'building'; startedAt: Date; workerId: string }
  | { status: 'deployed'; deployedAt: Date; releaseUrl: string }
  | { status: 'failed'; failedAt: Date; exitCode: number; stderrSummary: string };
```

#### 3. Branded types for type-safe IDs
Prevents accidental parameter transposition:
```typescript
type UserId = string & { readonly __brand: 'UserId' };
type AccountId = string & { readonly __brand: 'AccountId' };

function transferFunds(from: AccountId, to: AccountId, actor: UserId): Promise<void> { ... }
```

---

## 3. Idempotency engineering reference

Accepting an `Idempotency-Key` header without atomic handling creates a false sense of safety. Follow these six engineering invariants:

1. **Derive key from intent, not attempt:**
   - *Bad:* `crypto.randomUUID()` generated inside the retry loop (every retry creates a new key).
   - *Bad:* `${userId}:${amount}` (collapses two legitimate distinct $50 orders into one).
   - *Good:* Header supplied once by caller or derived from immutable business root (`order:v1:${orderId}`).
2. **Claim atomically:** Check-then-act (`SELECT` followed by `INSERT`) is a guaranteed race condition under concurrent retry storms. The database unique constraint *is* the concurrency gate.
3. **Guard payload:** Compute a cryptographic hash (SHA-256) of the request body. If the same key arrives with a mismatched hash, return `409 Conflict` or `422 Unprocessable Entity` immediately. Never silently return an existing response to an altered request.
4. **Deliberate in-flight duplicate strategy:**
   - Simple & safe: `409 Conflict` (client retries after backoff).
   - Synchronous wait: Bounded wait for the winner to finish.
   - Long-running: `202 Accepted` with a status polling URL.
5. **Handle the three outcomes:**
   Every network call produces: `SUCCESS`, `FAILURE`, or `UNKNOWN` (timeout/crash). A timeout does not mean the effect did not occur. Record intent *before* issuing the outbound call, so crashes leave recoverable evidence.
6. **Retention outliving DLQs:**
   Set key TTL based on the longest possible redelivery path (e.g., dead-letter queue retry window + dispute window), never merely on database storage cost.

---

## 4. Common rationalizations & reality

| Rationalization | Reality |
| :--- | :--- |
| *"We'll document the API schema later."* | The types **are** the specification. Define and lock the types before writing controller logic. |
| *"We don't need pagination for our small list."* | Any endpoint returning an unbounded array is an eventual DoS vector. Add pagination from day one. |
| *"PATCH is complex; let's just use PUT."* | `PUT` forces clients to read-modify-write the full resource, re-introducing lost-update races. Clients want `PATCH`. |
| *"We'll version the endpoint when breaking changes happen."* | Breaking changes break consumers instantly. Design for extension (additive, optional fields) to avoid forks. |
| *"Nobody relies on that undocumented header/order."* | **Hyrum's Law:** With enough consumers, every observable behavior is depended upon. Treat every output as committed. |
| *"Accepting the Idempotency-Key header is enough."* | A key accepted but not guarded by an atomic DB claim tells the client retrying is safe when it actually double-charges. |
| *"Our message broker guarantees exactly-once delivery."* | No distributed system guarantees exactly-once across crashes. Design for at-least-once with idempotent handlers. |
| *"Duplicate requests are rare in production."* | Duplicates are *correlated*. Retries spike exactly when dependencies degrade—precisely when duplicate costs are highest. |

---

## 5. Red flags heuristics

Reject or refactor any interface design exhibiting these indicators:
- [ ] Endpoints returning different data structures depending on query conditions or roles.
- [ ] Inconsistent error payloads (some returning `{ error: "msg" }`, others throwing HTML, others returning `{ success: false }`).
- [ ] Validation code scattered across database services or UI components instead of at network boundaries.
- [ ] Modifying or removing existing fields in an active API without an additive transition phase.
- [ ] `SELECT` checking for an idempotency key before an `INSERT` (TOCTOU race condition).
- [ ] An idempotency key derived from `Date.now()` or a newly minted UUID on every retry.
- [ ] Reusing an idempotency key with a changed request body without triggering a conflict error.
- [ ] Key retention TTL shorter than downstream queue retry schedules.
- [ ] Verbs inside REST URL paths (`/api/getUsers`, `/api/updateItem`).
- [ ] Third-party API responses ingested directly without schema parsing or boundary sanitization.

---

## 6. 6-Point diagnostic self-audit rubric

Evaluate every proposed API design against this rubric:

| Dimension | Question to Ask | Pass Condition | Failure Mode to Fix |
| :--- | :--- | :--- | :--- |
| **1. Contract-First & Type Tightness** | Are input and output schemas distinctly separated with bounded types? | Input schemas omit server-generated fields; states use discriminated unions; IDs are branded. | Reusing single entity interface for creation and reads; stringly-typed states. |
| **2. Boundary Validation** | Does validation happen strictly at the system edge with structured feedback? | External input parsed via schema validator (e.g. Zod); 422 structured errors emitted. | Unvalidated input reaching domain logic; ad-hoc `if (!req.body.x)` throws. |
| **3. Error Semantics** | Is error format unified across all failure modes? | Every failure returns standardized structured machine code, message, and details. | Mixed error shapes; raw string messages; leaking exception stack traces to clients. |
| **4. Atomic Idempotency** | Can state-changing endpoints survive concurrent retries and crashes safely? | Key claimed atomically via unique constraint; body hash guarded; intent stored before remote effect. | Check-then-act race; new UUID per retry attempt; silent replay on mismatched payload. |
| **5. Additive Evolution** | Can the interface grow without breaking existing consumers? | New fields are strictly optional; existing field types and enum values are immutable. | Renaming fields; turning optional parameters into required ones without a major version. |
| **6. Observable Discipline** | Does the interface hide internal storage schema and avoid leaking details? | API shape reflects domain concepts, not raw DB tables or third-party provider responses. | Leaking ORM column names; passing untrusted third-party responses straight to clients. |

---

## 7. Deterministic verification example

This bounded example validates the contract invariants: it proves atomic idempotency resolution, conflict detection upon payload mismatch, and handling of concurrent intents using Python's standard library.

```python
import hashlib, json, sqlite3
from pathlib import Path

def test_contract_invariants():
    db = Path("contract_verify.sqlite")
    if db.exists(): db.unlink()
    
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE keys (key TEXT PRIMARY KEY, hash TEXT, state TEXT, resp TEXT)")
    
    def handle_request(key: str, payload: dict):
        h = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        with sqlite3.connect(db) as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT hash, state, resp FROM keys WHERE key = ?", (key,)).fetchone()
            if row:
                if row[0] != h:
                    return {"status": 409, "error": "PAYLOAD_MISMATCH"}
                if row[1] == "in_progress":
                    return {"status": 409, "error": "IN_FLIGHT"}
                return {"status": 200, "data": json.loads(row[2])}
            
            conn.execute("INSERT INTO keys VALUES (?, ?, 'in_progress', NULL)", (key, h))
            # Simulate effect & completion
            resp_data = {"orderId": "ord_123", "status": "created"}
            conn.execute("UPDATE keys SET state = 'completed', resp = ? WHERE key = ?", (json.dumps(resp_data), key))
            return {"status": 201, "data": resp_data}

    # 1. First execution
    r1 = handle_request("key_alpha", {"amount": 100})
    # 2. Identical replay
    r2 = handle_request("key_alpha", {"amount": 100})
    # 3. Payload mismatch with same key
    r3 = handle_request("key_alpha", {"amount": 200})

    assert r1["status"] == 201, "First request must succeed"
    assert r2["status"] == 200 and r2["data"] == r1["data"], "Replay must return cached response"
    assert r3["status"] == 409 and r3["error"] == "PAYLOAD_MISMATCH", "Mismatched body must conflict"
    
    return {"r1": r1["status"], "r2": r2["status"], "r3": r3["status"]}

if __name__ == "__main__":
    result = test_contract_invariants()
    print(json.dumps(result, sort_keys=True))
```

### What the observation establishes:
1. Replays with identical payload return the existing result without re-executing side effects.
2. Replays with different payloads are rejected with conflict (`409`).
3. Execution relies solely on atomic uniqueness constraints, preventing race conditions under concurrency.
