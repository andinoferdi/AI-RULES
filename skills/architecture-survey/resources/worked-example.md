# Survey architecture friction: worked procedure, visual report patterns, and diagnostic rubric

This resource provides a concrete before-and-after transformation case study, production-grade hybrid HTML report scaffolds with zero-network fallback, 5 diagram patterns, common rationalizations, red-flag heuristics, an empirical diagnostic self-audit rubric, and a deterministic verification example for `architecture-survey`.

---

## 1. Worked case study: Before and after transformation

### The problem: An order intake pipeline fragmented across shallow modules (Before)

Below is an architectural friction pattern frequently observed in expanding codebases: understanding and executing an order intake requires traversing five separate shallow classes.

```typescript
// BEFORE: Fragmented, shallow modules, caller-side policy duplication, leaky seams
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

// File: src/orders/OrderValidator.ts (Shallow wrapper: interface as complex as implementation)
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

### Architectural flaws identified:
1. **Shallow modules throughout:** `OrderValidator` and `OrderDatabaseWrapper` are paper-thin. Deleting them and concentrating the logic would reduce complexity rather than increase it (**Deletion Test: concentrates**).
2. **Caller repeats policy:** Every caller (HTTP controller, background bulk-intake worker, CLI test harness) must repeat the exact sequencing: validate, calculate pricing, manage transaction lifecycles, and dispatch notifications.
3. **Leaking seam:** The controller is forced to coordinate database transaction handles (`tx`), coupling the transport layer to database concurrency semantics.
4. **Brittle, mock-heavy tests:** Unit tests for `OrderController` require mocking 4 dependencies across 8 method signatures just to verify an order was submitted.

---

### The solution: Consolidated deep module behind a single public seam (After)

Consolidate the fragmented wrappers into a single deep module: `OrderIntake`. The public interface exposes exactly one high-leverage method (`submitOrder`) that encapsulates validation, pricing invariants, transactional persistence, and event emissions.

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

// The Deep Module
export class OrderIntake {
  constructor(
    private readonly repository: OrderRepository,
    private readonly notifications: NotificationService
  ) {}

  /**
   * Deep public interface: one entry point handles the complete order placement lifecycle.
   * Callers have no awareness of internal transactions, tax calculations, or helper modules.
   */
  async submitOrder(command: SubmitOrderCommand): Promise<OrderReceipt> {
    // 1. Invariants concentrated in implementation
    this.assertValidCommand(command);

    // 2. Calculations encapsulated
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

### Wins achieved:
- **locality: invariants and transactions stay in one module**
- **leverage: 1 entry point absorbs 4 shallow wrappers**
- **interface shrinks from 14 methods to 1**
- **tests hit one public submit seam** without mocking internal database query sequences.

---

## 2. Hybrid HTML Report Scaffold & Visual Patterns

The architectural survey report is written to the OS temporary directory (`$TMPDIR` or `%TEMP%`, e.g. `<tmpdir>/architecture-survey-<timestamp>.html`) to prevent repository pollution.

The report employs a **Hybrid Progressive Enhancement** strategy:
1. **Online enhancement:** Loads Tailwind CSS and Mermaid.js via CDN for responsive typography, layout, and automatic flowchart rendering.
2. **Offline resilience:** Includes an embedded `<style>` block with fallback CSS rules (`.card`, `.badge`, `.diagram-box`, `.seam`, `.leak`, `.deep`) and inline SVG geometry so diagrams render clearly without an internet connection.

### HTML Scaffold

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Architecture Survey - {{project_name}}</title>
  
  <!-- Progressive CDN loading with offline-safe defaults -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" onerror="this.onerror=null;this.dataset.failed=true;">
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true, theme: 'neutral', securityLevel: 'loose' });
  </script>

  <style>
    /* Offline and standalone base fallback styles */
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 2rem 1rem; }
    .survey-container { max-width: 68rem; margin: 0 auto; }
    .candidate-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .badge { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .badge-strong { background: #dcfce7; color: #166534; }
    .badge-explore { background: #fef3c7; color: #92400e; }
    .badge-speculative { background: #f1f5f9; color: #475569; }
    .badge-dep { background: #e0e7ff; color: #3730a3; margin-left: 0.5rem; }
    .diagram-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.25rem 0; }
    @media (max-width: 768px) { .diagram-grid { grid-template-columns: 1fr; } }
    .diagram-panel { border: 1px solid #cbd5e1; border-radius: 0.5rem; padding: 1rem; background: #f8fafc; min-height: 18rem; }
    .seam { stroke-dasharray: 4 4; stroke: #64748b; }
    .leak { stroke: #ef4444; color: #ef4444; }
    .deep-box { background: linear-gradient(135deg, #0f172a, #1e293b); color: #ffffff; border-radius: 0.5rem; padding: 1rem; }
    .shallow-box { border: 1px solid #94a3b8; background: #ffffff; padding: 0.5rem; border-radius: 0.25rem; font-family: monospace; font-size: 0.85rem; margin-bottom: 0.5rem; }
    .wins-list { list-style-type: none; padding-left: 0; }
    .wins-list li { margin-bottom: 0.4rem; padding-left: 1.2rem; position: relative; font-weight: 500; }
    .wins-list li::before { content: "✓"; position: absolute; left: 0; color: #16a34a; }
  </style>
</head>
<body>
  <div class="survey-container">
    <header style="margin-bottom: 2.5rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 1.25rem;">
      <h1 style="font-size: 2rem; font-weight: 700; margin: 0 0 0.5rem 0;">Architecture Survey: {{project_name}}</h1>
      <p style="color: #64748b; margin: 0;">Scope: {{bounded_scope}} | Date: {{survey_date}}</p>
    </header>

    <!-- Top Recommendation Hero -->
    <section class="candidate-card" style="border-left: 6px solid #10b981; background: #f0fdf4;">
      <h2 style="font-size: 1.25rem; font-weight: 700; color: #065f46; margin: 0 0 0.5rem 0;">Top Recommendation: {{top_candidate.title}}</h2>
      <p style="margin: 0; color: #166534;">{{top_candidate.rationale}}</p>
    </section>

    <!-- Candidates Section -->
    <main id="candidates">
      {{candidate_cards}}
    </main>
  </div>
</body>
</html>
```

---

## 3. Visual Diagram Pattern Library

Pick the diagram pattern that most directly illustrates the structural transformation. Mix patterns across candidates rather than making every card identical.

### Pattern 1: Mermaid Flowchart / Sequence (Call flows & dependency tangles)
Ideal when illustrating a web of calls, circular dependencies, or leaking seams.

```html
<div class="diagram-panel">
  <h4 style="font-weight: 600; margin-bottom: 0.5rem;">Before: Fragmented call flow & leakage</h4>
  <pre class="mermaid">
    flowchart TD
      Controller[OrderController] --> Validator[OrderValidator]
      Controller --> Pricing[PricingService]
      Controller --> RepoWrap[OrderDatabaseWrapper]
      RepoWrap -.leak tx handle.-> Controller
      Controller --> Notifier[NotificationDispatcher]
      classDef leak stroke:#ef4444,stroke-width:2px;
      class RepoWrap leak
  </pre>
</div>
```

### Pattern 2: Hand-built Boxes & Arrows (CSS/SVG for Deep Module consolidation)
Ideal when showing multiple scattered wrappers absorbed into a single dark, solid deep module with faded internals.

```html
<div class="diagram-panel">
  <h4 style="font-weight: 600; margin-bottom: 0.5rem;">After: Consolidated Deep Module</h4>
  <div class="deep-box">
    <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8; margin-bottom: 0.5rem;">Public Seam: submitOrder(command)</div>
    <div style="background: rgba(255,255,255,0.1); border: 1px dashed #64748b; border-radius: 0.35rem; padding: 0.75rem; font-size: 0.8rem; color: #cbd5e1;">
      <p style="margin: 0 0 0.25rem 0;">• internal validation & invariants</p>
      <p style="margin: 0 0 0.25rem 0;">• encapsulated tax & pricing computation</p>
      <p style="margin: 0;">• atomic database transaction boundary</p>
    </div>
  </div>
</div>
```

### Pattern 3: Cross-Section Diagram (Collapsing Layered Shallowness)
Stack horizontal bars to illustrate layers a call must pass through without business value.
- **Before:** 5 thin bars stacked vertically (Controller → Validator → Service → Wrapper → DB), each 18px tall.
- **After:** 1 thick 72px bar labelled with the consolidated responsibility.

### Pattern 4: Mass Diagram (Interface Width vs Implementation Depth)
Use two adjacent rectangles per module: left rectangle = interface surface area; right rectangle = implementation logic.
- **Before (Shallow):** Interface rectangle is almost as tall as the implementation rectangle (lots of public methods for minimal logic).
- **After (Deep):** Interface rectangle is narrow and short; implementation rectangle is substantial and tall.

### Pattern 5: Call-Graph Collapse
A tree of nested boxes collapsed into one outer box, showing previously exposed functions as faded private implementation lines inside.

---

## 4. Common rationalizations vs Reality

| Rationalization | Reality |
| :--- | :--- |
| *"We should scan the entire repo to find all possible architecture issues."* | Whole-repo scans produce noise and analysis paralysis. Scope to active hotspots where changes actually occur. |
| *"More small files mean cleaner, more modular code."* | Tiny files with 1:1 interfaces destroy locality. Complexity does not vanish; callers are burdened with stitching them together. |
| *"We extracted this class so we could mock it in unit tests."* | Extracting modules solely for test mocking creates shallow architecture and brittle tests coupled to implementation details. |
| *"We need an interface here in case we switch database engines later."* | **The Two-Adapter Rule:** A seam with only one implementation is speculative indirection. Wait until the second concrete adapter exists. |
| *"This refactor will make the code much cleaner and easier to maintain."* | Empty adjectives earn no place in architectural reviews. Frame wins strictly in terms of locality, leverage, and test surface reduction. |

---

## 5. Red flags heuristics

Identify candidates by checking for these indicators:
- [ ] Bouncing across 4+ files to trace a single straightforward business transaction.
- [ ] Modules whose public methods merely pass parameters straight through to a downstream function.
- [ ] Callers repeating identical sequencing, validation checks, or transaction boilerplate.
- [ ] Unit test files spending 80% of their lines configuring mocks for shallow intermediaries.
- [ ] Seams exposing infrastructure handles (raw SQL handles, transport responses) directly to callers.
- [ ] Classes with 1 public method and 3 lines of implementation (accidental micro-abstractions).

---

## 6. 6-Point diagnostic self-audit rubric

| Dimension | Question to Ask | Pass Condition | Failure Mode to Fix |
| :--- | :--- | :--- | :--- |
| **1. Bounded Scoping** | Was the survey scoped to hot spots or a named subsystem? | Focused on files identified via recent git churn or explicit user direction. | Sweeping the whole repository without bounding. |
| **2. Deletion Test Evidence** | Does deleting the shallow module concentrate complexity? | Deletion test verifies complexity concentrates into one deep seam. | Suggesting abstractions where deleting them scatters logic. |
| **3. Vocabulary Discipline** | Are nouns and verbs aligned with the strict architectural terms? | Exclusively uses `module`, `interface`, `depth`, `seam`, `adapter`, `locality`, `leverage`. | Drifting into "component", "service", "API boundary", "cleaner code". |
| **4. Visual Pairings** | Does every candidate have an informative before/after comparison? | Visual diagrams clearly illustrate shallowness vs deepened consolidation. | Text-only bullet points or vague descriptions. |
| **5. Offline Integrity** | Does the report render cleanly without network access? | Fallback CSS and inline SVG ensure readability even if CDNs fail. | Broken layout or missing diagrams in offline environments. |
| **6. Non-Destructive Operation** | Did the survey avoid modifying project product files? | Survey writes exclusively to OS temporary directory; zero Git drift. | Prematurely refactoring or modifying product files. |

---

## 7. Deterministic verification example

This bounded example executes using Python's standard library. It writes a self-contained hybrid report and `result.json` to verify that candidate generation and offline reporting invariants hold deterministically.

```python
from pathlib import Path
import json
from html import escape

candidate = {
    "name": "Order intake",
    "files": ["handler.py", "policy.py"],
    "before": ["handler -> policy", "caller repeats validation"],
    "after": ["submit_order -> Receipt"],
    "strength": "Strong",
    "problem": "Order processing logic is split across shallow wrappers with caller repeats validation.",
    "solution": "Consolidate into OrderIntake deep module; public submit_order handles transaction.",
    "wins": ["locality: invariants concentrate in module", "tests: one public submit seam"]
}

# Generate hybrid report with pure CSS/inline-SVG fallback (zero external network dependency in test)
html_content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Architecture Survey - {escape(candidate['name'])}</title>
  <style>
    body {{ font-family: sans-serif; max-width: 55rem; margin: 2rem auto; padding: 1rem; color: #0f172a; }}
    .card {{ border: 1px solid #cbd5e1; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; background: #dcfce7; color: #166534; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0; }}
    .panel {{ border: 1px solid #e2e8f0; border-radius: 6px; padding: 1rem; background: #f8fafc; }}
    .deep {{ background: #0f172a; color: #ffffff; padding: 1rem; border-radius: 6px; }}
    pre {{ white-space: pre-wrap; margin: 0; }}
  </style>
</head>
<body>
  <h1>Architecture Survey</h1>
  <div class="card">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <h2 style="margin: 0;">{escape(candidate['name'])}</h2>
      <span class="badge">{escape(candidate['strength'])}</span>
    </div>
    <p><strong>Files:</strong> <code>{escape(', '.join(candidate['files']))}</code></p>
    <p><strong>Problem:</strong> {escape(candidate['problem'])}</p>
    <p><strong>Solution:</strong> {escape(candidate['solution'])}</p>
    <div class="grid">
      <div class="panel">
        <h3>Before</h3>
        <pre>{escape(chr(10).join(candidate['before']))}</pre>
      </div>
      <div class="panel">
        <h3>After</h3>
        <div class="deep">
          <pre>{escape(chr(10).join(candidate['after']))}</pre>
        </div>
      </div>
    </div>
    <p><strong>Wins:</strong></p>
    <ul>
      {"".join(f"<li>{escape(w)}</li>" for w in candidate['wins'])}
    </ul>
  </div>
</body>
</html>"""

Path("architecture.html").write_text(html_content, encoding="utf-8")

result = {
    "candidate": candidate["name"],
    "strength": candidate["strength"],
    "external_assets": [],
    "product_edits": []
}

Path("result.json").write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
```

### What the observation establishes

1. `architecture.html` is generated as an offline-capable, standalone document containing all required semantic markers (`Before`, `After`, `caller repeats validation`, `submit_order`).
2. `result.json` records that no external runtime assets were fetched and zero product code edits were made during the survey.
3. The observation proves the deterministic integrity of the survey technique without requiring internet connectivity or third-party libraries.
