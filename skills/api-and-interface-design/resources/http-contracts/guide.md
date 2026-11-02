# Comprehensive Guide: HTTP Endpoint Contracts & Atomic Idempotency

This guide defines the comprehensive methodology for designing resilient REST endpoints, TypeScript type contracts, perimeter schema validation, and atomic idempotency under Andino Workflow governance.

---

## 1. Core Mental Models

Interface and boundary design operates across four foundational principles:

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

## 2. REST API Patterns & Resource Conventions

### Resource-Oriented Routing
Use plural nouns for collections, and standard HTTP methods to express intent. Never put action verbs in the URI path:

```
GET    /api/tasks              → List tasks (with query parameters for filtering/pagination)
POST   /api/tasks              → Create a new task
GET    /api/tasks/:id          → Retrieve a single task
PATCH  /api/tasks/:id          → Partial update (only provided fields modified)
DELETE /api/tasks/:id          → Idempotent delete (succeeds even if already absent)

GET    /api/tasks/:id/comments → Sub-resource listing
POST   /api/tasks/:id/comments → Sub-resource creation
```

### Standardized Naming Conventions

| Pattern | Convention | Good Example | Anti-Pattern (Avoid) |
|---|---|---|---|
| Endpoints | Plural nouns, kebab-case | `/api/payment-methods` | `/api/createPaymentMethod`, `/api/paymentMethod` |
| Query params | camelCase | `?sortBy=createdAt&pageSize=20` | `?sort_by=createdAt&page_size=20` |
| Response fields | camelCase | `{ createdAt, orderId, isComplete }` | `{ created_at, OrderID, complete }` |
| Boolean fields | `is`/`has`/`can` prefix | `isComplete`, `hasAttachments` | `complete`, `attachments` |
| Enums | UPPER_SNAKE | `"IN_PROGRESS"`, `"FAILED"` | `"in-progress"`, `"In Progress"` |

### Mandatory Pagination
Always paginate collection endpoints. Naked array responses are an operational liability:

```typescript
// Request
GET /api/tasks?page=1&pageSize=20&sortBy=createdAt&sortOrder=desc

// Response (Wrap data in an envelope with pagination metadata)
interface PaginatedResult<T> {
  data: T[];
  pagination: {
    page: number;
    pageSize: number;
    totalItems: number;
    totalPages: number;
  };
}
```

### Partial Updates (PATCH over PUT)
`PUT` requires replacing the complete resource representation. If a client sends a partial payload to a `PUT` endpoint, omitted fields risk being overwritten or cleared. Always prefer `PATCH` for field-level updates:

```typescript
// PATCH /api/tasks/task_123
// Caller only provides title; description and priority remain unchanged
{
  "title": "Consolidate API endpoints"
}
```

---

## 3. TypeScript Interface Patterns

### A. Contract First
Define the interface and type contracts before implementing the underlying logic. The interface serves as the authoritative specification:

```typescript
export interface TaskAPI {
  createTask(input: CreateTaskInput, opts?: RequestOptions): Promise<Task>;
  listTasks(params: ListTasksParams): Promise<PaginatedResult<Task>>;
  getTask(id: TaskId): Promise<Task>;
  updateTask(id: TaskId, input: UpdateTaskInput): Promise<Task>;
  deleteTask(id: TaskId): Promise<void>;
}
```

### B. Input/Output Separation
Never reuse an output model as an input schema. Outputs frequently contain server-generated properties (IDs, timestamps, audit trails, computed statuses) that callers must never provide:

```typescript
// Input: what the caller is authorized to supply
export interface CreateTaskInput {
  title: string;
  description?: string;
  priority?: 'LOW' | 'MEDIUM' | 'HIGH';
}

// Output: what the system returns
export interface Task {
  id: TaskId;
  title: string;
  description: string | null;
  priority: 'LOW' | 'MEDIUM' | 'HIGH';
  status: TaskStatus;
  createdAt: Date;
  updatedAt: Date;
  createdBy: UserId;
}
```

### C. Branded Types for Identifiers
Prevent parameter transposition bugs (e.g. passing a `UserId` where an `OrderId` is expected) by using nominal type branding:

```typescript
export type TaskId = string & { readonly __brand: 'TaskId' };
export type UserId = string & { readonly __brand: 'UserId' };
export type OrderId = string & { readonly __brand: 'OrderId' };

// Compiler enforces correct argument matching
export function assignTask(taskId: TaskId, assigneeId: UserId): Promise<Task> {
  // ...
}
```

### D. Discriminated Unions for Discrete States
Avoid optional field sprawl where combinations of nulls represent states. Use explicit tagged unions:

```typescript
export type TaskStatus =
  | { type: 'PENDING' }
  | { type: 'IN_PROGRESS'; assigneeId: UserId; startedAt: Date }
  | { type: 'COMPLETED'; completedAt: Date; completedBy: UserId }
  | { type: 'CANCELLED'; reason: string; cancelledAt: Date };

// Consumer gets complete compile-time type narrowing
export function getStatusDescription(status: TaskStatus): string {
  switch (status.type) {
    case 'PENDING':
      return 'Awaiting start';
    case 'IN_PROGRESS':
      return `Assigned to ${status.assigneeId} since ${status.startedAt.toISOString()}`;
    case 'COMPLETED':
      return `Finished on ${status.completedAt.toISOString()}`;
    case 'CANCELLED':
      return `Cancelled: ${status.reason}`;
  }
}
```

---

## 4. Boundary Validation with Zod

Untrusted input enters at system perimeters. Parse, don't validate:

```typescript
import { z } from 'zod';

export const CreateTaskSchema = z.object({
  title: z.string().trim().min(1, 'Title is required').max(200),
  description: z.string().trim().max(2000).optional(),
  priority: z.enum(['LOW', 'MEDIUM', 'HIGH']).default('MEDIUM'),
});

// Route handler validation at perimeter
app.post('/api/tasks', async (req, res) => {
  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({
      error: {
        code: 'VALIDATION_FAILED',
        message: 'Invalid request payload',
        details: result.error.flatten(),
      },
    });
  }

  // Domain service receives guaranteed validated data
  const task = await taskService.create(result.data);
  return res.status(201).json(task);
});
```

### Uniform Error Semantics
Every error response must adhere to a single machine-readable envelope:

```typescript
export interface APIError {
  error: {
    code: string;       // Machine-readable: "VALIDATION_FAILED", "CONFLICT", "NOT_FOUND"
    message: string;    // Human-readable: "Title is required"
    details?: unknown;  // Structured contextual metadata (e.g. field errors)
  };
}

// HTTP Status Code Mapping:
// 400 Bad Request           → Malformed syntax or unparseable JSON
// 401 Unauthorized          → Missing or invalid authentication token
// 403 Forbidden             → Authenticated caller lacks permission
// 404 Not Found             → Specified resource identifier does not exist
// 409 Conflict              → Concurrency collision, duplicate intent, or in-flight mutation
// 422 Unprocessable Entity  → Semantically invalid business data failing schema validation
// 500 Internal Server Error → Unexpected server error (never leak raw stack traces)
```

---

## 5. Robust Atomic Idempotency Engineering

### A. Intent Derivation
Derive the idempotency key from the client's intent or immutable entity identifier, never per retry attempt:

```typescript
// ✗ BAD: Generates a new key on every retry attempt — causes duplicate charges!
crypto.randomUUID()
`${orderId}:${Date.now()}`

// ✓ GOOD: Stable across retries of the same intent
req.headers['idempotency-key']
`charge:v1:${orderId}`
```

### B. Atomic Claim via Unique Constraint
Check-then-act (`SELECT` followed by `INSERT`) is a severe concurrency bug under retry storms. The database unique constraint is the concurrency lock:

```typescript
import crypto from 'node:crypto';

export async function executeIdempotent<T>(
  key: string,
  payload: unknown,
  effect: () => Promise<T>
): Promise<{ status: 'applied' | 'replayed'; data: T }> {
  const payloadHash = crypto
    .createHash('sha256')
    .update(JSON.stringify(payload))
    .digest('hex');

  // Step 1: Atomic insert with UNIQUE constraint on `key`
  try {
    await db.query(
      `INSERT INTO idempotency_records (key, payload_hash, state, created_at)
       VALUES ($1, $2, 'in_progress', NOW())`,
      [key, payloadHash]
    );
  } catch (err: any) {
    if (isUniqueViolation(err)) {
      // Step 2: Handle duplicate intent
      const existing = await db.query(
        `SELECT payload_hash, state, response_data FROM idempotency_records WHERE key = $1`,
        [key]
      );
      const record = existing.rows[0];

      // Payload mismatch check: Reusing key with different body is client bug
      if (record.payload_hash !== payloadHash) {
        throw new HTTPError(409, 'IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD');
      }

      // In-flight check: Previous request still executing
      if (record.state === 'in_progress') {
        throw new HTTPError(409, 'CONCURRENT_REQUEST_IN_PROGRESS');
      }

      // Completed replay: Return identical saved response
      return { status: 'replayed', data: JSON.parse(record.response_data) };
    }
    throw err;
  }

  // Step 3: Execute the effect only after claiming the record
  try {
    const result = await effect();
    await db.query(
      `UPDATE idempotency_records
       SET state = 'succeeded', response_data = $1, completed_at = NOW()
       WHERE key = $2`,
      [JSON.stringify(result), key]
    );
    return { status: 'applied', data: result };
  } catch (effectErr) {
    // Record failed state so retries can see failure or allow retry
    await db.query(
      `UPDATE idempotency_records SET state = 'failed' WHERE key = $1`,
      [key]
    );
    throw effectErr;
  }
}
```

### C. In-Flight Strategy Selection

| Strategy | Response | When to Use |
|---|---|---|
| **Reject** | `409 Conflict` | Simplest and safest. Instructs caller to retry with exponential backoff. |
| **Wait** | Block boundedly | Synchronous workflows where caller cannot handle asynchronous polling. |
| **Pending** | `202 Accepted` + Status URL | Long-running operations or asynchronous worker dispatch. |

### D. The Three Outcomes & Outliving the DLQ
A timeout does not mean failure; it means the outcome is `UNKNOWN`.
1. Persist the intent record *before* initiating external payment calls or side effects.
2. If network times out, transition intent to `reconciliation_needed` so background workers can poll the provider rather than blindly duplicating the request.
3. Retention window must exceed the longest possible retry path: if a Dead-Letter Queue (DLQ) replays after 7 days, idempotency records must be retained for at least 8 days.

---

## 6. Agent-Native & Tool-Calling Interface Design

When interfaces are invoked by autonomous AI agents (e.g. MCP Tools, LLM tool-calling):
1. **Semantic Descriptions:** Provide unambiguous `description` fields on every parameter in the schema. Do not assume the caller understands implicit domain abbreviations.
2. **Deterministic Schemas:** Restrict string inputs to enums or strict regex patterns. Prevent hallucinated parameter names with `additionalProperties: false`.
3. **Remedial Error Shapes (Self-Healing):** When an agent fails a boundary check, the error response must specify the exact violation and provide corrective instructions so the agent can self-repair on its next attempt:

```typescript
// Remedial Error Shape for Autonomous Agents
export interface AgentRemedialError {
  error: {
    code: 'INVALID_PARAMETER';
    message: string;
    remedy: {
      field: string;
      expected: string;
      provided: unknown;
      correctiveAction: string;
    };
  };
}
```

---

## 7. Additive Evolution & Deprecation Lifecycle

1. **The Additive Rule:** Only add optional fields. Never change the type of an existing field or remove an active field without a formal deprecation schedule.
2. **Sunset Signaling:** Use standard HTTP headers (`Deprecation` and `Sunset`) to notify consumers well in advance of endpoint retirement:
   ```http
   Deprecation: @1735689600
   Sunset: Wed, 01 Jul 2026 00:00:00 GMT
   Link: </api/v2/orders>; rel="successor-version"
   ```
3. **Expand and Contract:**
   - *Phase 1 (Expand):* Introduce the new field/endpoint while maintaining the old one.
   - *Phase 2 (Migrate):* Switch callers to the new field.
   - *Phase 3 (Contract):* Remove the old field only after verification that traffic to it has ceased.
