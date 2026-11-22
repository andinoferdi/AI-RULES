# Survey Architecture Friction: Worked Example and End-to-End Case Study

Internal method ID: `architecture-survey`. Supporting resource for `skills/architecture-survey`.

This resource provides an end-to-end case study demonstrating how architectural friction is diagnosed, structured into candidate proposals, visually rendered in HTML, and grilled to an accepted design.

---

## 1. Worked Case Study: The Order Intake Pipeline

### The Problem: Fragmented Shallow Modules (Before)

In expanding codebases, simple operations are frequently atomized across multiple thin classes under the guise of "clean code". Understanding or changing the order placement logic forces developers to jump across five separate files:

```typescript
// BEFORE: Fragmented shallow modules, caller-side policy duplication, leaky seams
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
    
    // 1. Caller repeats policy and sequencing
    if (!this.validator.isValidPayload(raw)) {
      return res.status(400).send("Invalid order");
    }
    const tax = this.pricing.computeTax(raw.subtotal, raw.country);
    const total = this.pricing.computeTotal(raw.subtotal, tax);

    // 2. Leaky abstraction: Controller must manage DB transaction seam directly
    const tx = await this.repoWrapper.beginTransaction();
    try {
      const orderRecord = await this.repoWrapper.insertOrder(tx, raw, total);
      await this.repoWrapper.insertLines(tx, orderRecord.id, raw.items);
      await this.repoWrapper.commit(tx);

      // 3. Side-effect coordination scattered in caller
      await this.notifier.sendOrderPlacedEmail(orderRecord.id, raw.email);
      return res.status(201).json({ id: orderRecord.id, total });
    } catch (err) {
      await this.repoWrapper.rollback(tx);
      return res.status(500).send("Order failed");
    }
  }
}

// File: src/orders/OrderValidator.ts (Shallow wrapper: interface as complex as impl)
export class OrderValidator {
  isValidPayload(data: any): boolean {
    return Boolean(data && data.items && data.items.length > 0 && data.subtotal > 0);
  }
}

// File: src/orders/OrderDatabaseWrapper.ts (Shallow pass-through over raw SQL)
export class OrderDatabaseWrapper {
  beginTransaction() { return db.startTx(); }
  insertOrder(tx: any, data: any, total: number) { return tx.query("INSERT INTO orders...", [total]); }
  insertLines(tx: any, orderId: string, items: any[]) { return tx.query("INSERT INTO order_items...", [items]); }
  commit(tx: any) { return tx.commit(); }
  rollback(tx: any) { return tx.rollback(); }
}
```

### Architectural Flaws Diagnosed:
1. **The Deletion Test Concentrates:** If `OrderValidator` and `OrderDatabaseWrapper` are deleted and their logic absorbed into an order coordinator, complexity concentrates into one cohesive place rather than scattering. They are shallow wrappers.
2. **Caller Repeats Policy:** Every caller (HTTP controller, background bulk intake worker, test suite) must replicate the exact sequencing of validation, tax math, transaction commits, and notification dispatches.
3. **Leaky Seam:** The controller is coupled to transaction handles (`tx`), exposing database concurrency semantics to the web transport layer.
4. **Brittle Test Surface:** Testing the controller requires mocking 4 dependencies across 8 method signatures.

---

### The Solution: Consolidated Deep Module Behind Public Seam (After)

Consolidate the fragmented wrappers into a single deep module: `OrderIntake`. The public interface exposes exactly one high-leverage method (`submitOrder`) that encapsulates validation, pricing invariants, transactional persistence, and event notifications.

```typescript
// AFTER: Deep module, high leverage, strong locality, encapsulated transaction seam
// File: src/orders/OrderIntake.ts

export interface OrderItem {
  sku: string;
  quantity: number;
  unitPriceCents: number;
}

export interface SubmitOrderCommand {
  customerId: string;
  country: string;
  items: OrderItem[];
  email: string;
}

export interface OrderReceipt {
  orderId: string;
  totalCents: number;
  itemCount: number;
  submittedAt: Date;
}

export interface OrderRepository {
  persist(order: { id: string; totalCents: number; items: OrderItem[] }): Promise<void>;
}

export interface NotificationService {
  notifyOrderPlaced(orderId: string, email: string): Promise<void>;
}

// The Deep Module
export class OrderIntake {
  constructor(
    private readonly repository: OrderRepository,
    private readonly notifications: NotificationService
  ) {}

  /**
   * Deep public interface: one entry point handles the complete order placement lifecycle.
   * Callers have zero awareness of internal transactions, tax calculations, or helper modules.
   */
  async submitOrder(command: SubmitOrderCommand): Promise<OrderReceipt> {
    // 1. Invariants concentrated in implementation
    this.assertValidCommand(command);

    // 2. Calculations encapsulated internally
    const subtotal = command.items.reduce((acc, i) => acc + i.unitPriceCents * i.quantity, 0);
    const tax = this.computeTax(subtotal, command.country);
    const totalCents = subtotal + tax;
    const orderId = `ord_${crypto.randomUUID()}`;

    // 3. Atomicity & persistence completely encapsulated behind repo seam
    await this.repository.persist({ id: orderId, totalCents, items: command.items });

    // 4. Notifications handled reliably
    await this.notifications.notifyOrderPlaced(orderId, command.email);

    return {
      orderId,
      totalCents,
      itemCount: command.items.length,
      submittedAt: new Date()
    };
  }

  private assertValidCommand(cmd: SubmitOrderCommand): void {
    if (!cmd.items?.length || cmd.items.some(i => i.quantity <= 0)) {
      throw new Error("Order must contain at least one valid item");
    }
  }

  private computeTax(subtotal: number, country: string): number {
    return country === "ID" ? Math.round(subtotal * 0.11) : 0;
  }
}
```

### Quantified Wins Achieved:
- `locality: pricing invariants stay in 1 module`
- `leverage: 1 public interface replaces 4 wrappers`
- `seam hides database transaction handles`
- `interface shrinks from 14 methods to 1`
- `tests hit 1 public submit seam` without mocking internal SQL sequences.

---

## 2. Terminal-Native Executive Summary Card

During the survey presentation in chat, this summary card is emitted:

```
+-----------------------------------------------------------------------------+
| ARCHITECTURE SURVEY CANDIDATE: Collapse Order Intake Pipeline               |
+-----------------------------------------------------------------------------+
| Recommendation: STRONG | Dependency: in-process                             |
| Affected Files: src/orders/OrderController.ts, OrderValidator.ts,           |
|                 OrderDatabaseWrapper.ts, OrderPricingService.ts             |
|                                                                             |
| Problem  : Controller forces callers to manually coordinate DB transactions |
|            and pricing invariants across 4 shallow files.                   |
| Solution : Consolidate 4 wrappers into a single deep OrderIntake module     |
|            behind a transactional submitOrder seam.                         |
|                                                                             |
| Wins:                                                                       |
|   - locality: pricing invariants stay in 1 module                           |
|   - leverage: 1 public interface replaces 4 wrappers                        |
|   - seam hides database transaction handles                                 |
|   - tests hit 1 public submit seam                                          |
|                                                                             |
| Full Visual HTML Report: C:\Users\Lenovo\AppData\Local\Temp\survey-123.html |
+-----------------------------------------------------------------------------+
```

---

## 3. Deterministic Python Invariant Verification

Below is an operational Python snippet validating that a candidate specification satisfies the 5 Floor Invariants before inclusion in the final survey report:

```python
def validate_survey_candidate(candidate):
    # Invariant 1: Problem and Solution must be exactly 1 sentence
    for field in ("problem", "solution"):
        text = candidate.get(field, "").strip()
        sentences = [s for s in text.split(".") if s.strip()]
        if len(sentences) != 1:
            return False, f"{field} must be exactly 1 sentence (found {len(sentences)})"
    
    # Invariant 2: Wins must be <= 6 words each
    wins = candidate.get("wins", [])
    if not wins or len(wins) > 5:
        return False, "Candidate must provide 1 to 5 wins"
    for w in wins:
        words = w.split()
        if len(words) > 6:
            return False, f"Win '{w}' exceeds strict 6-word ceiling ({len(words)} words)"
            
    # Invariant 3: Lexical purity check (no forbidden words)
    banned = ["component", "service", "unit", "api", "wrapper", "clean code", "maintainable"]
    dump = str(candidate).lower()
    for b in banned:
        if b in dump:
            return False, f"Banned terminology detected: '{b}'"

    return True, "VALID"
```
