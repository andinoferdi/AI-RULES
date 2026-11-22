# Anti-Rationalization Matrix, Failure Modes, and Verification Checklist

Resource contract; selected directly under its canonical owner.

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: proportional investigation, evidence-based decisions, single durable checkpoints, and anti-loop guards.

This resource provides the definitive anti-rationalization refutations, diagnostic red flags, and pre-release verification checklist for `api-and-interface-design`.

---

## 1. Common Rationalizations vs. Mechanical Reality

When designing interfaces under schedule pressure, engineers and AI models frequently rationalize shortcuts. These rationalizations lead directly to brittle systems, race conditions, and integration failures.

| Model / Engineer Rationalization | Mechanical Reality & Mandated Response |
|---|---|
| *"We'll document the API contracts later when the implementation stabilizes."* | **False.** The type contracts ARE the documentation. Defining the contract first exposes design flaws before code is written. |
| *"We don't need pagination for now; the database table is small."* | **False.** Tables grow inevitably. Returning naked unpaginated arrays risks memory exhaustion and breaking clients. Always paginate collection endpoints from day one. |
| *"PATCH is too complicated to implement; let's just use PUT."* | **False.** `PUT` requires sending the full entity state and accidentally overwrites concurrent edits. `PATCH` is what callers actually need. |
| *"We'll version the API when breaking changes happen."* | **False.** Version branching creates diamond dependency hell. Design for additive evolution from the start (One-Version Rule). |
| *"Nobody uses that undocumented behavior, so changing it is safe."* | **False.** Hyrum's Law: If an observable behavior exists, someone is depending on it. Treat timing, headers, error text, and field ordering as commitments. |
| *"We can just maintain two active versions of the API."* | **False.** Dual-version maintenance doubles maintenance cost and fragments domain logic. Extend rather than fork. |
| *"Internal in-memory APIs don't need formal contracts."* | **False.** Internal module seams are still contracts. Clear boundaries prevent tight coupling and enable independent testing and refactoring. |
| *"Accepting the Idempotency-Key header is enough."* | **False.** The header is merely a declaration. Atomic persistence backed by a database unique constraint is the actual implementation. |
| *"Our message broker guarantees exactly-once processing."* | **False.** No distributed broker guarantees exactly-once across node crashes. Design consumer operations to be at-least-once with idempotent handlers. |
| *"Duplicate requests are rare in practice."* | **False.** Retries spike precisely during dependency degradation and network jitter—exactly when duplicates are most correlated and dangerous. |
| *"Scattering validation across internal functions makes code safer."* | **False.** Defensive checks scattered internally create bloat and mask boundary leaks. Validate strictly at the system perimeter; trust internal types. |

---

## 2. 11 Diagnostic Red Flags (Stop Immediately)

If any of the following patterns appear in an API design or code review, stop immediately and refactor:

1. **Action Verbs in REST URLs:** Endpoints named `/api/createTask`, `/api/updateUser`, or `/api/getOrders`. (Use standard HTTP methods on plural nouns: `POST /api/tasks`, `PATCH /api/users/:id`).
2. **Naked Unpaginated Arrays:** `GET /api/tasks` returning `Task[]` directly rather than an envelope with pagination metadata.
3. **Inconsistent Error Shapes:** Some endpoints returning `{ error: "msg" }`, others `{ message: "msg" }`, and others returning plain strings.
4. **Scattered Ad-Hoc Validation:** Manual `if (!req.body.id)` checks dispersed across controller and service logic instead of boundary schema parsing (`safeParse`).
5. **Non-Atomic Idempotency Checks:** Performing a `SELECT` query followed by an `INSERT` to check idempotency keys (TOCTOU race condition).
6. **Per-Attempt Idempotency Key Generation:** Generating an idempotency key via `crypto.randomUUID()` or timestamp inside the retry loop instead of anchoring to caller intent.
7. **Silent Replay on Payload Mismatch:** Returning an earlier cached response when a client accidentally reuses an idempotency key with a different payload.
8. **Leaking Internal Implementation Details:** Exposing internal database column names, raw ORM entities, or runtime stack traces in public error responses.
9. **Breaking Additive Invariants:** Changing existing field types, renaming properties, or removing fields in active production contracts.
10. **Unchecked Third-Party Responses:** Passing external partner API responses directly into business logic without boundary schema validation.
11. **Idempotency Retention Shorter Than Retry Pipeline:** Setting a 24-hour key expiration when the system's Dead-Letter Queue (DLQ) replays messages up to 7 days later.

---

## 3. Pre-Release Interface Verification Checklist

Before approving or releasing any interface or API seam, verify each item:

- [ ] **Contract-First Specification:** Type contracts and schemas are defined and committed prior to controller implementation.
- [ ] **Boundary Validation:** All external inputs (request bodies, query params, headers, third-party payloads) are strictly parsed at the edge.
- [ ] **Internal Trust:** Internal functions accept typed contracts without redundant defensive type-checking.
- [ ] **Standardized Error Envelope:** All error responses follow the uniform `{ error: { code, message, details? } }` schema with mapped HTTP status codes.
- [ ] **Mandatory Pagination:** All collection endpoints require pagination parameters and return structured metadata (`page`, `pageSize`, `totalItems`, `totalPages`).
- [ ] **Resource-Oriented REST Nouns:** Endpoints use plural nouns and standard HTTP verbs (`GET`, `POST`, `PATCH`, `DELETE`).
- [ ] **Branded Types for Identifiers:** Entity IDs use branded types (`OrderId`, `CustomerId`) to prevent argument transposition bugs.
- [ ] **Discriminated Unions for States:** Multi-state variants are represented via tagged unions rather than sprawling optional fields.
- [ ] **Atomic Idempotency for Mutations:** State-changing operations claim keys atomically via database `UNIQUE` constraints.
- [ ] **Guarded Payload Hash:** Reused keys with mismatched SHA-256 payload hashes fail loudly with `409 Conflict`.
- [ ] **Intent-Derived Keys:** Idempotency keys derive from client intent or business roots, not ephemeral attempt timestamps.
- [ ] **Safe Additive Evolution:** All modifications to existing seams add optional fields without breaking existing consumers.
