# HTTP contracts: transport detail and idempotency implementation

Resource of `api-and-interface-design`. The procedure and the rules that apply to every
interface (consumer mapping, change classification, Hyrum's Law, additive change, naming,
the idempotency-key rules and status codes) are in the parent [SKILL.md](../../SKILL.md).
This guide holds the transport detail and the code those rules need. It does not restate
them.

---

## 1. Resource modeling and filtering

Plural nouns for collections; the HTTP method says what happens. No verbs in paths.

```
GET    /api/tasks              → List tasks (filter, sort and page with query parameters)
POST   /api/tasks              → Create a task
GET    /api/tasks/:id          → Get one task
PATCH  /api/tasks/:id          → Change some fields
PUT    /api/tasks/:id          → Replace the whole task (only when callers send every field)
DELETE /api/tasks/:id          → Delete; succeeds when already absent

GET    /api/tasks/:id/comments → Sub-resource list
POST   /api/tasks/:id/comments → Sub-resource create
POST   /api/payments/:id/refunds → An action with its own lifecycle becomes a sub-resource
```

Filters are query parameters named after fields:

```
GET /api/tasks?status=IN_PROGRESS&assigneeId=usr_123&createdAfter=2026-01-01
```

An existing verb route that consumers still call (for example `POST /api/orders/create`)
stays until they move; add the noun route beside it and classify the change in the parent
procedure, step 2.

## 2. Bounded collections

Every list has a bound. Pick the style by the data:

| Style | Request | Use when |
| --- | --- | --- |
| Offset | `?page=2&pageSize=20` | Small, stable collections where jumping to a page matters |
| Cursor | `?limit=20&cursor=eyJpZCI6...` | Large or fast-changing collections; stable under inserts |

A new endpoint returns an envelope:

```typescript
interface Page<T> {
  data: T[];
  pagination: { nextCursor: string | null };   // or { page, pageSize, totalItems, totalPages }
}
```

A consumer that already parses a bare array keeps the array. Carry the next page outside
the body, or make the envelope opt-in:

```http
GET /api/payments?limit=100
200 OK
Link: </api/payments?limit=100&cursor=eyJpZCI6OTl9>; rel="next"
[ { "id": 1, ... }, ... ]
```

A default limit changes what that consumer sees (it now gets the first page only). State
that in the design note and confirm it with the consumer's owner; an app that cannot page
may need a higher default or a new route instead.

## 3. PUT and PATCH

- `PUT` replaces the whole resource. A field missing from the body is cleared. Repeating
  the same PUT gives the same result, so it is idempotent without a key.
- `PATCH` changes only the fields sent. Use JSON Merge Patch semantics unless the project
  uses another: a field set to `null` is removed, an absent field is untouched.
- Keep an existing PUT when its callers really send the whole resource. Add PATCH beside it
  for partial updates instead of changing PUT's meaning.

```typescript
// PATCH /api/tasks/task_123: only the title changes
{ "title": "Consolidate API endpoints" }
```

## 4. Errors

One body for every error:

```typescript
export interface APIError {
  error: {
    code: string;       // machine-readable: "VALIDATION_FAILED", "NOT_FOUND"
    message: string;    // human-readable: "Title is required"
    details?: unknown;  // field errors or other structured context
  };
}
```

If the project already uses RFC 9457 problem details (`application/problem+json` with
`type`, `title`, `status`, `detail`), keep that instead. Never mix the two.

| Status | Meaning |
| --- | --- |
| 400 | Malformed request, unparseable JSON, or a required idempotency key missing |
| 401 | No valid authentication |
| 403 | Authenticated, not allowed |
| 404 | No such resource |
| 409 | Conflict: version mismatch, duplicate, or an idempotent request still running |
| 422 | Well-formed but semantically invalid, including an idempotency key reused with a different body |
| 429 | Rate limited; send `Retry-After` |
| 500 | Unexpected server error; the body says nothing about internals |

A catch-all handler maps unknown errors to 500 with a generic message and logs the detail
server-side. Stack traces, SQL and ORM rows never reach the response.

## 5. Validation at the edge

Parse once, at the route, and hand typed values inward. Zod is one option in TypeScript:

```typescript
import { z } from 'zod';

export const CreateTaskSchema = z.object({
  title: z.string().trim().min(1, 'Title is required').max(200),
  description: z.string().trim().max(2000).optional(),
  priority: z.enum(['LOW', 'MEDIUM', 'HIGH']).default('MEDIUM'),
}).strict();

app.post('/api/tasks', async (req, res) => {
  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({
      error: { code: 'VALIDATION_FAILED', message: 'Invalid task', details: result.error.flatten() },
    });
  }
  const task = await taskService.create(result.data);   // typed; the service does not re-check
  return res.status(201).json(task);
});
```

Third-party responses get the same treatment before business logic uses them.

## 6. Idempotency implementation

The rules (intent-derived key, atomic claim, payload guard, in-flight response, three
outcomes, retention, status codes) are in the parent skill. This is one implementation for
Postgres.

### Table

```sql
CREATE TABLE idempotency_keys (
  scope           TEXT        NOT NULL,   -- authenticated principal, so callers cannot collide
  key             TEXT        NOT NULL,
  request_hash    TEXT        NOT NULL,   -- SHA-256 of the canonical request body
  state           TEXT        NOT NULL CHECK (state IN ('in_progress', 'completed', 'unknown')),
  response_status INTEGER,
  response_body   JSONB,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  expires_at      TIMESTAMPTZ NOT NULL,   -- longer than the longest re-delivery path
  PRIMARY KEY (scope, key)                -- the concurrency gate
);
```

### Claim, replay or reject

```typescript
import crypto from 'node:crypto';

export interface Reply { status: number; body: unknown; headers?: Record<string, string> }

function stable(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(stable).join(',')}]`;
  if (value !== null && typeof value === 'object') {
    const entries = Object.keys(value).sort()
      .map((k) => `${JSON.stringify(k)}:${stable((value as Record<string, unknown>)[k])}`);
    return `{${entries.join(',')}}`;
  }
  return JSON.stringify(value);
}

const requestHash = (body: unknown) => crypto.createHash('sha256').update(stable(body)).digest('hex');

const fail = (status: number, code: string, message: string, headers?: Record<string, string>): Reply =>
  ({ status, body: { error: { code, message } }, headers });

export async function handleIdempotent(
  db: Db,
  scope: string,
  key: string,
  body: unknown,
  effect: (downstreamKey: string) => Promise<Reply>,  // returns a definite outcome, throws when unknown
): Promise<Reply> {
  const hash = requestHash(body);

  // 1. Claim: the primary key picks one winner among concurrent requests.
  const claim = await db.query(
    `INSERT INTO idempotency_keys (scope, key, request_hash, state, expires_at)
     VALUES ($1, $2, $3, 'in_progress', now() + interval '30 days')
     ON CONFLICT (scope, key) DO NOTHING
     RETURNING key`,
    [scope, key, hash],
  );

  // 2. Someone already holds this key.
  if (claim.rowCount === 0) {
    const { rows: [row] } = await db.query(
      `SELECT request_hash, state, response_status, response_body
       FROM idempotency_keys WHERE scope = $1 AND key = $2`,
      [scope, key],
    );
    if (row.request_hash !== hash) {
      return fail(422, 'IDEMPOTENCY_KEY_REUSED', 'This key was already used with a different request body');
    }
    if (row.state === 'in_progress') {
      return fail(409, 'REQUEST_IN_PROGRESS', 'A request with this key is still running', { 'Retry-After': '2' });
    }
    if (row.state === 'unknown') {
      return fail(409, 'OUTCOME_PENDING', 'The outcome of the first request is being reconciled', { 'Retry-After': '30' });
    }
    return { status: row.response_status, body: row.response_body };   // completed: replay
  }

  // 3. We won the claim. The downstream key is the same for every attempt of this intent.
  const downstreamKey = `${scope}:${key}`;
  try {
    const reply = await effect(downstreamKey);
    await db.query(
      `UPDATE idempotency_keys SET state = 'completed', response_status = $3, response_body = $4
       WHERE scope = $1 AND key = $2`,
      [scope, key, reply.status, JSON.stringify(reply.body)],
    );
    return reply;   // success and definite failures (a card decline) are both replayed later
  } catch {
    // Timeout, crash or 5xx from the provider: the effect may have happened.
    await db.query(`UPDATE idempotency_keys SET state = 'unknown' WHERE scope = $1 AND key = $2`, [scope, key]);
    return fail(503, 'OUTCOME_UNKNOWN', 'The result is not known yet; retry with the same key', { 'Retry-After': '30' });
  }
}
```

What the effect does, in order:

1. Record the intent first (for a charge: insert the payment row as `pending` with its
   idempotency scope and key), so a crash after the provider call leaves evidence.
2. Call the provider with the downstream key as its `Idempotency-Key`
   (`charge:v1:<paymentId>` or the scope-key pair above). Never a new key per attempt.
3. Map a definite answer (success or decline) to a `Reply`; throw on timeout or 5xx.

Resolve `unknown` by reconciliation: the provider's webhook or a status lookup by the
downstream key moves the row to `completed` with the real response. Within the provider's
own deduplication window, re-sending with the same downstream key is also safe; after it,
only reconciliation is. A sweeper moves `in_progress` rows older than the call timeout plus
a margin to `unknown`, so a crashed worker cannot hold a key forever. Purge `completed` rows
after `expires_at`; never purge `unknown`.

### In-flight strategy

| Strategy | Response | Use when |
| --- | --- | --- |
| Reject | `409` with `Retry-After` | Default: simplest and safest; the client retries with backoff |
| Wait | Block for the result, bounded | The caller needs the answer synchronously |
| Pending | `202` with a status URL | Long-running effects |

### Retention

Keep keys longer than every path that can re-deliver the same intent: client retries,
queue redelivery, a dead-letter queue replayed days later, a provider dispute window. A
provider that deduplicates for 24 hours does not cover a 7-day replay; your own record must.

## 7. Webhooks and event consumers

Delivery is at-least-once and order is not guaranteed. A handler must be safe to run twice
and in any order.

```typescript
app.post('/webhooks/payco', express.raw({ type: 'application/json' }), async (req, res) => {
  // 1. Signature over the raw bytes, before parsing.
  if (!verifySignature(req.body, req.get('PayCo-Signature'), process.env.PAYCO_SECRET!)) {
    return res.status(400).json({ error: { code: 'BAD_SIGNATURE', message: 'Signature mismatch' } });
  }
  // 2. Shape check: third-party data is untrusted.
  const parsed = PayCoEvent.safeParse(JSON.parse(req.body.toString('utf8')));
  if (!parsed.success) {
    return res.status(400).json({ error: { code: 'BAD_EVENT', message: 'Unrecognised event' } });
  }
  const event = parsed.data;

  // 3. Dedupe and apply in one transaction, so a crash cannot mark an event done without its effect.
  await db.tx(async (tx) => {
    const first = await tx.query(
      `INSERT INTO webhook_events (event_id, type) VALUES ($1, $2) ON CONFLICT DO NOTHING RETURNING event_id`,
      [event.id, event.type],
    );
    if (first.rowCount === 0) return;                       // a retry or replay: already applied
    if (event.type === 'charge.succeeded') {
      // Forward-only: a late 'failed' or a replay cannot move a paid payment backwards.
      await tx.query(`UPDATE payments SET status = 'paid' WHERE charge_id = $1 AND status = 'pending'`, [event.data.id]);
    }
  });
  return res.sendStatus(200);
});

function verifySignature(raw: Buffer, header: string | undefined, secret: string): boolean {
  if (!header) return false;
  const expected = crypto.createHmac('sha256', secret).update(raw).digest('hex');
  return header.length === expected.length && crypto.timingSafeEqual(Buffer.from(header), Buffer.from(expected));
}
```

- If an event refers to an object you have not stored yet, answer non-2xx so the sender
  retries, or park the event for later. Do not drop it.
- Notifications triggered by an event dedupe on the event or business id, not on delivery.
- Keep `webhook_events` as long as the sender retries plus any manual replay window.

## 8. Agent tool interfaces

When autonomous agents call the interface (MCP tools, LLM tool calling):

1. **Describe every parameter.** Give each field a `description`; do not rely on implicit
   domain abbreviations.
2. **Constrain inputs.** Use enums or strict patterns for closed sets and
   `additionalProperties: false`, so invented parameter names fail.
3. **Return errors an agent can act on.** Name the field, what was expected, what arrived
   and how to fix the call:

```typescript
export interface AgentRemedialError {
  error: {
    code: 'INVALID_PARAMETER';
    message: string;
    remedy: { field: string; expected: string; provided: unknown; correctiveAction: string };
  };
}
```

## 9. Evolution and deprecation headers

1. Only add optional fields. Changing a field's type or removing an active field needs a
   deprecation schedule.
2. Announce retirement with standard headers well in advance:

   ```http
   Deprecation: @1735689600
   Sunset: Wed, 01 Jul 2026 00:00:00 GMT
   Link: </api/v2/orders>; rel="successor-version"
   ```

3. Expand and contract: introduce the new field or route beside the old one, move callers,
   and remove the old one only after traffic to it has stopped. `deprecation-and-migration`
   owns the removal schedule.
