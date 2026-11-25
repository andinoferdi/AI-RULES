# Worked example: one order endpoint, end to end

Resource of `api-and-interface-design`. It applies the parent [procedure](../SKILL.md#procedure)
to one endpoint. The idempotency helper it calls is in
[http-contracts §6](http-contracts/guide.md#6-idempotency-implementation).

## The situation

`POST /api/orders/create` creates an order and charges the customer's card through a
payment gateway. Two consumers call it and read `id`, `amount`, `status` and the error
message:

| Consumer | Sends | Reads | Ships with the API? |
| --- | --- | --- | --- |
| Web checkout | `orderId` (created once per checkout), `customerId`, `amount`, `currency`, `items` | `id`, `amount`, `status` | Yes, same deploy |
| Partner integrations (published SDK 1.x) | Same body, plus a fresh `Idempotency-Key` on every retry | `id`, `status`, and `message` on errors | No; partners upgrade on their own schedule |

The gateway accepts an `Idempotency-Key` and deduplicates on it for 24 hours. Failed
webhook deliveries can be replayed from a dead-letter queue up to 7 days later. Customers
have been charged twice after timeouts.

## Before

```typescript
app.post('/api/orders/create', async (req, res) => {
  try {
    const { orderId, amount, customerId, items } = req.body;

    // 1. Weak validation inside the handler
    if (!amount || amount < 0) {
      return res.status(400).send('Invalid amount');
    }

    // 2. Check-then-act: two concurrent retries both see "not found"
    const existing = await db.query('SELECT * FROM orders WHERE id = $1', [orderId]);
    if (existing.rows.length > 0) {
      return res.json(existing.rows[0]);   // replayed even if the body changed
    }

    // 3. Gateway charged before anything is recorded
    const charge = await paymentGateway.charge({ amount, customerId });

    // A crash here leaves a charge with no order; the retry charges again
    const newOrder = await db.query(
      'INSERT INTO orders (id, amount, customer_id, status, gateway_ref) VALUES ($1, $2, $3, $4, $5) RETURNING *',
      [orderId, amount, customerId, 'completed', charge.id],
    );
    return res.status(200).json(newOrder.rows[0]);
  } catch (err: any) {
    // 4. A different error shape, with internals
    return res.status(500).json({ message: err.message, stack: err.stack });
  }
});
```

What is wrong, mapped to the procedure:

1. **Step 5:** validation is partial, inside the handler, and answers with a plain string.
2. **Rules, idempotency:** `SELECT` then `INSERT` lets concurrent retries both charge; the
   replay ignores a changed body; the SDK's per-attempt key is ignored, which is just as well
   because it changes on every retry.
3. **Rules, three outcomes:** the gateway is called before the intent is recorded and
   without a key, so a timeout or crash leads to a second charge.
4. **Step 4:** errors come back as a string, `{ message }` or a stack trace.
5. **Naming:** a verb in the path. Consumers already call it, so it cannot simply be renamed
   (step 2).

## Consumer impact and migration (steps 1 and 2)

| Change | Web checkout | Partners (SDK 1.x) |
| --- | --- | --- |
| New route `POST /api/orders`; old route kept as an alias of the same handler | Moves in this release | Additive; old route answers with `Deprecation` and `Sunset` headers |
| `Idempotency-Key` honoured; the legacy route falls back to the body's `orderId` as the key | Sends the key from the checkout session | Additive; SDK 1.x keeps working because `orderId` is stable, SDK 2.0 sends one key per order |
| Errors use `{ error: { code, message, details? } }` | Updated in this release | Breaking for code that reads `message` at the top level; the legacy route also keeps a top-level `message` until sunset |
| Response gains `status` as a union and keeps `id` and `amount` | Updated | Additive; existing string values unchanged |

## Contract (step 3)

```typescript
import { z } from 'zod';

export type OrderId = string & { readonly __brand: 'OrderId' };
export type CustomerId = string & { readonly __brand: 'CustomerId' };

export const CreateOrderSchema = z.object({
  orderId: z.string().uuid().transform((v) => v as OrderId),
  customerId: z.string().min(1).transform((v) => v as CustomerId),
  amount: z.number().int().positive(),            // minor units
  currency: z.enum(['USD', 'EUR', 'IDR']),
  items: z.array(z.object({ sku: z.string().min(1), quantity: z.number().int().positive() })).min(1),
}).strict();
export type CreateOrderInput = z.infer<typeof CreateOrderSchema>;

export type OrderStatus = 'pending_payment' | 'paid' | 'payment_failed';

export interface Order {                          // output only: callers never send these fields
  id: OrderId;
  customerId: CustomerId;
  amount: number;
  currency: string;
  status: OrderStatus;
  createdAt: string;
}

export type OrderErrorCode =
  | 'VALIDATION_FAILED' | 'CARD_DECLINED' | 'IDEMPOTENCY_KEY_REUSED'
  | 'REQUEST_IN_PROGRESS' | 'OUTCOME_PENDING' | 'OUTCOME_UNKNOWN' | 'INTERNAL';
```

## After (steps 4 to 6)

```typescript
async function createOrder(req: Request, res: Response, legacy: boolean) {
  // Step 5: one parse at the edge
  const parsed = CreateOrderSchema.safeParse(req.body);
  if (!parsed.success) {
    return send(res, legacy, {
      status: 422,
      body: { error: { code: 'VALIDATION_FAILED', message: 'Invalid order', details: parsed.error.flatten() } },
    });
  }
  const input = parsed.data;

  // Step 6: the key comes from the client's intent. The legacy route accepts the stable orderId.
  const key = req.get('Idempotency-Key') ?? (legacy ? input.orderId : undefined);
  if (!key) {
    return send(res, legacy, { status: 400, body: { error: { code: 'VALIDATION_FAILED', message: 'Idempotency-Key header is required' } } });
  }

  const reply = await handleIdempotent(db, req.auth.principalId, key, input, async (downstreamKey) => {
    // Intent first: a crash after the gateway call still leaves a pending order to reconcile.
    const order = await orders.insertPending(input);                      // status 'pending_payment'
    const result = await paymentGateway.charge(
      { amount: input.amount, currency: input.currency, customer: input.customerId },
      { idempotencyKey: `charge:v1:${order.id}` },                       // same for every attempt
    );                                                                  // throws on timeout or 5xx
    if (result.declined) {
      await orders.markFailed(order.id, result.code);
      return { status: 402, body: { error: { code: 'CARD_DECLINED', message: 'The card was declined' } } };
    }
    return { status: 201, body: await orders.markPaid(order.id, result.chargeId) };
  });

  return send(res, legacy, reply);
}

app.post('/api/orders', (req, res) => createOrder(req, res, false));
app.post('/api/orders/create', (req, res) => {                          // legacy alias until sunset
  res.set('Deprecation', '@1767225600');
  res.set('Sunset', 'Wed, 01 Jul 2026 00:00:00 GMT');
  res.set('Link', '</api/orders>; rel="successor-version"');
  return createOrder(req, res, true);
});

function send(res: Response, legacy: boolean, reply: Reply) {
  const err = (reply.body as { error?: { message: string } }).error;
  // Legacy callers still read a top-level `message` until sunset (consumer table above).
  const body = legacy && err ? { ...(reply.body as object), message: err.message } : reply.body;
  return res.status(reply.status).set(reply.headers ?? {}).json(body);
}

// Step 4: anything unexpected becomes one generic error; details go to the log only.
app.use((err: unknown, req: Request, res: Response, _next: NextFunction) => {
  logger.error({ err, path: req.path });
  res.status(500).json({ error: { code: 'INTERNAL', message: 'Something went wrong' } });
});
```

What each response means for a client:

| Situation | Status | Body code |
| --- | --- | --- |
| First request, charge succeeds | 201 | the order |
| First request, card declined | 402 | `CARD_DECLINED` (replayed on retry with the same key) |
| Retry after either of those, same body | same as the first | same as the first |
| Same key, different body | 422 | `IDEMPOTENCY_KEY_REUSED` |
| Same key while the first is running | 409 + `Retry-After` | `REQUEST_IN_PROGRESS` |
| Gateway timed out | 503 + `Retry-After` | `OUTCOME_UNKNOWN`, then `OUTCOME_PENDING` until reconciled |

The gateway's `charge.succeeded` webhook (or a status lookup by `charge:v1:<orderId>`)
resolves an unknown outcome and completes the idempotency record with the real response.
Keys are kept 30 days: longer than the 7-day dead-letter replay, and longer than the
gateway's own 24-hour window, which on its own would not cover that replay.

## Verification (step 8)

| Check | Expected |
| --- | --- |
| 20 concurrent `POST /api/orders` with one key and body, against a stubbed gateway | 1 gateway call, 1 order row; one 201, the rest 201 replays or 409 |
| Same key, amount changed | 422 `IDEMPOTENCY_KEY_REUSED`; gateway not called |
| Gateway stub sleeps past the timeout, then records the charge | First call 503; record `unknown`; after the webhook, a retry replays 201; gateway saw one charge |
| Kill the process between claim and gateway call | Sweeper marks the record `unknown`; reconciliation finds no charge and completes it as failed; no double charge |
| SDK 1.x fixture: fresh `Idempotency-Key` per attempt, same `orderId`, legacy route | One charge; the old route still answers with a top-level `message` on errors |
| Error paths | Every response matches `{ error: { code, message } }`; no stack trace |

Not verified in this example: the gateway's real deduplication behavior and the partners'
error handling, which their owners must confirm.
