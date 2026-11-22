# Comprehensive Guide: API and Interface Design

Internal method ID: `api-and-interface-design`.

This guide defines the unified multi-layer methodology for designing resilient, high-leverage software interfaces under Andino Workflow governance. It spans from macroscopic package layer boundaries down to microscopic HTTP endpoints and distributed concurrency locks.

---

## 1. The Tri-Layer Boundary Architecture

Software interfaces do not exist in isolation at the HTTP network edge. A fragile internal architecture inevitably leaks through to public endpoints. Andino Workflow unifies interface design across three complementary architectural layers:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. MACRO: Package & Layer Boundaries (import-enforcement)   │
│    - Strict entrypoints; internal subsystem files private   │
│    - One-way dependency flows; zero dependency cycles       │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 2. MESO: Deep Module Seams (module-depth)                   │
│    - High caller leverage: simple interface, deep subsystem │
│    - 2-Adapter invariant: production port + in-memory fake  │
│    - The Deletion Test: complexity hidden, not layered      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 3. MICRO: HTTP & Network Contracts (http-contracts)         │
│    - Contract-first specification & perimeter Zod parsing   │
│    - Uniform APIError envelope & mandatory pagination       │
│    - Atomic idempotency: UNIQUE constraint concurrency gate │
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: Macro Enforcement (`resources/import-enforcement/guide.md`)
Enforces physical architectural seams across packages. Callers may only import from designated package root entrypoints; deep imports into internal subdirectories are strictly forbidden and guarded by automated tooling (e.g. dependency-cruiser or ESLint boundaries).

### Layer 2: Meso Seam Leverage (`resources/module-depth/guide.md`)
Applies John Ousterhout's *Philosophy of Software Design*. Great modules are **deep**: they hide vast operational complexity behind an intuitive, compact interface. An interface must maximize caller leverage (observable capability gained per concept learned) and strictly satisfy the **2-Adapter Invariant** (at least one production implementation and one clean in-memory test fake).

### Layer 3: Micro Transport Contracts (`resources/http-contracts/guide.md`)
Secures public network endpoints against untrusted data, retry storms, and distributed failure modes. Enforces contract-first design, perimeter-only Zod parsing, uniform error formatting, and atomic database-enforced idempotency.

---

## 2. Core Mental Models

Interface and seam design operates across four foundational mental models:

### A. Hyrum's Law & Observable Commitments
> With a sufficient number of users of an API, all observable behaviors of your system will be depended on by somebody, regardless of what you promise in the contract.

Every observable behavior—including undocumented error messages, response timing, key ordering, nullability, and HTTP headers—becomes an implicit contract once callers integrate with it.
- **Expose intentionally:** Treat every public field, status code, and header as a permanent commitment.
- **Prevent implementation leakage:** Never expose internal database column names, raw ORM entities, or stack traces.
- **Plan for deprecation at design time:** Prefer extending existing contracts over breaking changes.

### B. The One-Version Rule (Additive Evolution)
Avoid forcing consumers to choose between competing versions of the same seam. Diamond dependency conflicts arise when different callers require different versions of the same interface.
- Design interfaces to evolve additively: new fields must be optional; existing field types and enum meanings are immutable.
- Extend rather than fork. If a breaking change is unavoidable, run an expand/contract migration cycle.

### C. Contract-First & Boundary Validation
Define the type contract and schema before writing controller logic. The contract is the specification.
- **Validate at system edges only:** Untrusted external data (HTTP request bodies, URL query parameters, environment configuration, form inputs, and third-party API responses) must be validated strictly at system entrances.
- **Trust internal domain code:** Once validated at the boundary, internal functions trust the typed structures. Avoid scattering defensive checks across internal layers.
- **Third-party data is untrusted:** Responses from external partner APIs are external input; validate their shape before using them in business logic.

### D. Atomic Idempotency & The Three Outcomes
In distributed systems, network operations produce three possible outcomes: `SUCCESS`, `FAILURE`, or `UNKNOWN` (timeouts, network drops, server restarts).
- Accepting an `Idempotency-Key` header is merely declaring a contract; honoring it requires bulletproof implementation.
- **Intent derivation:** Derive keys from the client's intent or immutable business root, never from per-attempt timestamps or random UUIDs.
- **Atomic claim:** Check-then-act (`SELECT` followed by `INSERT`) is a race condition. The database unique constraint *is* the concurrency gate.
- **Guarded payload:** Reusing a key with an altered payload is a client bug; it must conflict (`409 Conflict`) rather than silently returning a previous response.
- **Reconciliation:** A timeout is an `UNKNOWN` state. Persist intent before outbound dispatch so recovery processes can reconcile rather than blindly duplicating side effects.

---

## 3. End-to-End Implementation Procedure

### Step 1: Map Consumers and Establish Invariants
Inspect existing callers, consumed fields, required ordering, nullability expectations, and error handling patterns.
- Catalog observable behaviors callers rely on (Hyrum's Law).
- *Done when:* Existing consumer dependencies and invariants are documented before modifying the seam.

### Step 2: Formulate the Contract Before Implementation
Draft strict input and output schemas:
- Separate input types from output types (never require callers to supply server-generated timestamps or IDs).
- Use branded types for distinct identifiers (e.g. `OrderId`, `CustomerId`) to prevent parameter transposition.
- Use discriminated unions for multi-state entities to guarantee valid state transitions.
- Standardize error responses into a single machine-readable shape (`code`, `message`, `details`).
- For REST endpoints, use plural nouns, camelCase query parameters, and support `PATCH` for partial updates.
- *Done when:* Type contracts and schema definitions compile and unambiguously specify all valid request/response shapes.

### Step 3: Validate Strictly at Boundaries
Implement schema validation at the edge (route handlers, RPC endpoints):
- Parse incoming payloads with strict validation libraries (e.g. Zod `safeParse`).
- Emit structured `422 Unprocessable Entity` or `400 Bad Request` with machine-readable error details on failure.
- Ensure third-party responses pass boundary schema validation before being processed by internal logic.
- *Done when:* All network entrypoints reject malformed payloads and internal handlers receive fully validated types.

### Step 4: Engineer Atomic Idempotency for State Mutations
For every state-changing endpoint (`POST`, `PUT`, `PATCH`):
- Require an `Idempotency-Key` header from the caller or derive it from an immutable business identifier.
- Atomically insert the intent record into the idempotency store using a `UNIQUE` constraint on the key.
- Store a cryptographic hash (SHA-256) of the request payload alongside the key.
- *Done when:* Concurrent duplicate requests hit the database unique violation and only one caller obtains the in-progress lock.

### Step 5: Handle Races, In-Flight Calls, and Timeouts
- **Payload mismatch check:** When a key already exists, verify its stored payload hash. If mismatched, return `409 Conflict` (or `422`).
- **In-flight handling:** If the existing key is still `in_progress`, return `409 Conflict` (client retries with backoff) or `202 Accepted` with a status URL.
- **Completed replay:** If already `completed`, replay the cached response payload with identical status.
- **Pre-dispatch persistence & reconciliation:** Persist the intent record *before* calling external payment gateways or third-party effects. Treat timeouts as `UNKNOWN`, transition status to reconciliation, and alert background workers instead of blindly retrying.
- **Retention:** Set idempotency key retention to outlive the longest retry path (including dead-letter queues and dispute windows).
- *Done when:* Concurrent identical requests return cached responses, mismatched payloads are rejected, and crashed operations leave actionable reconciliation records.

### Step 6: Audit Against Red Flags and Verification Rubric
Cross-check the interface design against the diagnostic rubric and checklist:
- Verify against [resources/anti-rationalization-and-failure-modes.md](resources/anti-rationalization-and-failure-modes.md).
- Review end-to-end code implementations in [resources/worked-example.md](resources/worked-example.md).
- *Done when:* All red flags are eliminated and the pre-release checklist passes.

---

## 4. Specialized Resource Directory

| Resource | Responsibility | Key Reference |
|---|---|---|
| [http-contracts](resources/http-contracts/guide.md) | REST semantics, perimeter Zod validation, pagination, uniform error envelopes, and distributed atomic idempotency. | [Contract](resources/http-contracts/contract.md) |
| [module-depth](resources/module-depth/guide.md) | Ousterhout deep-module architecture, interface leverage, seam placement, and 2-adapter testing discipline. | [Contract](resources/module-depth/contract.md) |
| [import-enforcement](resources/import-enforcement/guide.md) | TypeScript package entrypoint rules, forbidden deep imports, and dependency cycle prevention. | [Contract](resources/import-enforcement/contract.md) |
| [anti-rationalization](resources/anti-rationalization-and-failure-modes.md) | 10 refutations of model shortcuts, 11 diagnostic red flags, and 12-point pre-release verification checklist. | Direct Guide |
| [worked-example](resources/worked-example.md) | Concrete before/after transformation study in TypeScript and SQL with runnable idempotency harness. | Direct Guide |
