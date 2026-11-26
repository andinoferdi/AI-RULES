# Worked example: surveying an order intake flow

Internal resource of `architecture-survey`. It follows one candidate from the code to the
report card, the summary card and the design reached after grilling. The design section is
what grilling produced; the report itself proposes no interface.

## 1. The code before

A shop's order placement is spread across five files. The HTTP controller, a bulk-import
worker and an admin script each repeat the same sequence. `git log --name-only` over the last
six months shows these files in most commits.

```typescript
// File: src/orders/OrderController.ts
export class OrderController {
  constructor(
    private validator: OrderValidator,
    private pricing: OrderPricingService,
    private repoWrapper: OrderDatabaseWrapper,
    private notifier: NotificationDispatcher
  ) {}

  async handleOrder(req: Request, res: Response) {
    const raw = req.body;

    // 1. The caller sequences policy itself
    if (!this.validator.isValidPayload(raw)) {
      return res.status(400).send("Invalid order");
    }
    const tax = this.pricing.computeTax(raw.subtotal, raw.country);
    const total = this.pricing.computeTotal(raw.subtotal, tax);

    // 2. The caller manages the database transaction handle
    const tx = await this.repoWrapper.beginTransaction();
    try {
      const orderRecord = await this.repoWrapper.insertOrder(tx, raw, total);
      await this.repoWrapper.insertLines(tx, orderRecord.id, raw.items);
      await this.repoWrapper.commit(tx);

      // 3. Side effects coordinated by the caller
      await this.notifier.sendOrderPlacedEmail(orderRecord.id, raw.email);
      return res.status(201).json({ id: orderRecord.id, total });
    } catch (err) {
      await this.repoWrapper.rollback(tx);
      return res.status(500).send("Order failed");
    }
  }
}

// File: src/orders/OrderValidator.ts
export class OrderValidator {
  isValidPayload(data: any): boolean {
    return Boolean(data && data.items && data.items.length > 0 && data.subtotal > 0);
  }
}

// File: src/orders/OrderDatabaseWrapper.ts
export class OrderDatabaseWrapper {
  beginTransaction() { return db.startTx(); }
  insertOrder(tx: any, data: any, total: number) { return tx.query("INSERT INTO orders ...", [total]); }
  insertLines(tx: any, orderId: string, items: any[]) { return tx.query("INSERT INTO order_items ...", [items]); }
  commit(tx: any) { return tx.commit(); }
  rollback(tx: any) { return tx.rollback(); }
}
```

## 2. What the survey found

1. **Deletion test concentrates:** deleting `OrderValidator` and `OrderDatabaseWrapper` and
   absorbing their logic into one order intake module puts the complexity in one place; no
   caller would have to reinvent anything. They are pass-through modules.
2. **Callers repeat the sequence:** the controller, the bulk-import worker and the admin
   script each run validation, tax, the transaction and the email, and their copies have
   drifted (the worker emails before it commits).
3. **Leak across the seam:** the controller holds the transaction handle `tx`, so database
   concurrency rules reach the HTTP code.
4. **Hard to test through the interface:** the controller test mocks four modules and eight
   methods to assert one order.
5. **Kept:** `src/money/CurrencyMath.ts` is used by twelve files. Deleting it would spread its
   rounding rules across all of them, so it is load-bearing and not a candidate.

## 3. The report card and the summary card

The HTML card holds the files, the before diagram (pattern 2: four dashed pass-through boxes
the controller calls in sequence, a red arrow for `tx`), the after diagram (one dark order
intake box with `submit(order)` on top and the four steps faded inside), and:

- **Problem:** Every order caller sequences validation, tax, the transaction and the email
  itself across four shallow modules.
- **Solution:** Absorb the four pass-through modules into one order intake module whose
  submit call owns the transaction.
- **Wins:** "locality: tax rules in one module", "leverage: one interface, three callers",
  "transaction handle stays behind the seam", "tests hit one interface".

The chat summary card from the same data:

```
+-----------------------------------------------------------------------------+
| CANDIDATE: Collapse the order intake pipeline                               |
+-----------------------------------------------------------------------------+
| Strength: STRONG | Dependency: local-substitutable (orders database),       |
|                  | true external (email)                                    |
| Files: src/orders/OrderController.ts, OrderValidator.ts,                    |
|        OrderDatabaseWrapper.ts, OrderPricingService.ts                      |
| Problem : Every order caller sequences validation, tax, the transaction     |
|           and the email itself across four shallow modules.                 |
| Solution: Absorb the four pass-through modules into one order intake        |
|           module whose submit call owns the transaction.                    |
| Wins: locality: tax rules in one module | leverage: one interface, three    |
|       callers | transaction handle stays behind the seam                    |
+-----------------------------------------------------------------------------+
Report: /tmp/architecture-survey-20261102-143000.html
Which of these would you like to explore?
```

### The design after grilling

The user picked this candidate. Grilling settled: the database has a local stand-in (an
in-memory Postgres), so it stays behind an internal seam with no port; email is a third party,
so it crosses a port with two adapters (production and a recording adapter for tests); the
email goes out after commit and a failed email does not undo the order; the three callers
move in one change and the four old modules are deleted.

```typescript
// File: src/orders/OrderIntake.ts
export interface OrderLine { sku: string; quantity: number; unitPriceCents: number; }
export interface PlaceOrder { customerId: string; country: string; email: string; lines: OrderLine[]; }
export interface OrderReceipt { orderId: string; totalCents: number; }

// Port at the external seam. Adapters: SesOrderMailer (production), RecordingOrderMailer (tests).
export interface OrderMailer {
  orderPlaced(orderId: string, email: string): Promise<void>;
}

// A pg Pool in production, an in-memory Postgres in tests: an internal seam, not a port.
export interface Queryable {
  connect(): Promise<{ query(sql: string, params?: unknown[]): Promise<any>; release(): void }>;
}

export class OrderIntake {
  constructor(private readonly db: Queryable, private readonly mailer: OrderMailer) {}

  /** Validates, prices, stores the order in one transaction, then emails. Throws InvalidOrder. */
  async submit(order: PlaceOrder): Promise<OrderReceipt> {
    if (!order.lines.length || order.lines.some((l) => l.quantity <= 0)) {
      throw new InvalidOrder("an order needs at least one line with a positive quantity");
    }
    const subtotal = order.lines.reduce((sum, l) => sum + l.unitPriceCents * l.quantity, 0);
    const totalCents = subtotal + taxFor(subtotal, order.country);

    const client = await this.db.connect();
    let orderId: string;
    try {
      await client.query("BEGIN");
      orderId = (await client.query(
        "INSERT INTO orders (customer_id, total_cents) VALUES ($1, $2) RETURNING id",
        [order.customerId, totalCents])).rows[0].id;
      for (const line of order.lines) {
        await client.query("INSERT INTO order_items (order_id, sku, quantity, unit_price_cents) VALUES ($1, $2, $3, $4)",
          [orderId, line.sku, line.quantity, line.unitPriceCents]);
      }
      await client.query("COMMIT");
    } catch (err) {
      await client.query("ROLLBACK");
      throw err;
    } finally {
      client.release();
    }

    await this.mailer.orderPlaced(orderId, order.email).catch(() => { /* logged; the order stands */ });
    return { orderId, totalCents };
  }
}
```

Tests: delete the controller test that mocks four modules. New tests call `submit` against an
in-memory Postgres and a `RecordingOrderMailer`: a valid order is stored with its lines and one
email recorded; an order with no lines throws `InvalidOrder` and stores nothing; a mailer
failure still leaves the order stored.

The interface shrank from fourteen methods spread over four modules to one `submit` call, and
the transaction handle no longer leaves the module.

## 4. A wording check that matches the rules

This check flags banned substitutes in a card's prose and ignores identifiers in backticks,
which is how the vocabulary rule is written.

```python
import re

BANNED = ("component", "service", "api", "boundary", "layer", "cleaner code",
          "easier to maintain")

def prose_problems(text):
    prose = re.sub(r"`[^`]*`", "", text).lower()   # quoted identifiers keep their names
    return [word for word in BANNED if re.search(rf"\b{re.escape(word)}\b", prose)]

card = ("Every order caller sequences validation, tax, the transaction and the email itself "
        "across four shallow modules such as `OrderDatabaseWrapper`.")
assert prose_problems(card) == []
assert prose_problems("Introduce an order service layer.") == ["service", "layer"]
```
