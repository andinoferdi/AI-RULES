# Worked Example: Deep Module Design & Operational Verification

This resource provides a complete, production-grade refactoring walkthrough and a runnable, zero-dependency Python verification harness for designing deep modules under Andino Workflow governance.

---

## 1. The Scenario: Fragmented Checkout Friction

In an e-commerce platform, order processing has fractured into 5 shallow helpers:
- `validateCart(cart)`
- `calculateTax(cart, address)`
- `reserveStock(items)`
- `quoteShipping(order, carrier)`
- `recordOrder(cart, payment)`

### The Observed Friction
1. **Scattered Caller Policy**: Callers in `web/checkout.ts`, `mobile/api.ts`, and `batch/reorder.ts` duplicate the sequence and error-handling logic. If address validation fails midway, one caller forgets to release the stock reservation.
2. **Shallow Test Fragility**: 42 unit tests exist, but each mocks the adjacent helper functions. When `reserveStock` changes its signature, 18 tests break despite identical system behavior.
3. **Speculative Indirection**: `IShippingQuotePort` was created with only a single implementation (`FedExAdapter`).

---

## 2. Refactoring Walkthrough

### Step 1: The Deletion Test
- *Question*: If we delete the individual `validateCart` and `calculateTax` helpers, does complexity vanish or return?
- *Finding*: Complexity returns in every caller. Callers are forced to calculate tax brackets and cart invariants manually. The behavior is genuine, but its current seam is too shallow.

### Step 2: Dependency Classification
Applying `dependency-and-seam-discipline.md`:
1. `validateCart` & `calculateTax`: **In-Process**. Merge directly into implementation; no seam or adapter.
2. `orderStorage`: **Local-Substitutable** (SQLite/PGLite in tests). Keep seam internal; do not expose through interface.
3. `shippingCarrier`: **Remote-but-Owned**. Define a port with 2 adapters (`FedExHttpAdapter` in prod, `InMemoryShippingAdapter` in tests).
4. `paymentGateway`: **True External** (Stripe). Injected domain-shaped port with mock adapter in tests.

### Step 3: Design-It-Twice Exploration
Spawning parallel subagents produces 3 candidate interfaces:

- **Candidate A (Minimalist)**:
  `OrderIntake.process(cartId, paymentToken) -> Result<Order>`
  *Pros*: Maximum leverage ($L = 5.0$). Zero configuration.
  *Cons*: Cannot customize shipping speed (e.g. overnight vs standard).

- **Candidate B (Over-Extensible)**:
  `OrderIntake.builder().withValidator(v).withTaxStrategy(t).withShipping(s).submit()`
  *Pros*: Total flexibility.
  *Cons*: Shallow ($L = 1.2$). Caller must re-learn and configure 4 internal strategies.

- **Candidate C (Winning Hybrid - Common Case Simplicity)**:
  ```typescript
  interface CheckoutOptions {
    speed?: "standard" | "express";
    metadata?: Record<string, string>;
  }

  class OrderIntake {
    constructor(
      private shipping: ShippingPort,
      private payment: PaymentPort
    ) {}

    // Single primary entrypoint: zero-config default, optional escape hatch
    async processOrder(
      cartId: string,
      paymentToken: string,
      options: CheckoutOptions = {}
    ): Promise<OrderResult> {
      // 1. Validate cart invariants
      // 2. Resolve tax brackets
      // 3. Atomically reserve inventory
      // 4. Quote and bind shipping
      // 5. Authorize payment and persist order
    }
  }
  ```

### Step 4: The Quantified Leverage Scorecard
- Hidden Behaviors ($B_{\text{hidden}}$): 6 (Cart validation, tax lookup, stock lock, shipping binding, charge handling, rollback compensation).
- Caller Concepts ($C_{\text{caller}}$): 2 (Method `processOrder` + 1 optional configuration object).
- **Leverage Index**: $L = \frac{6}{2} = 3.0$ (Deep Module).

### Step 5: Test Migration ("Replace, Don't Layer")
1. Implement 6 comprehensive tests targeting `OrderIntake.processOrder(...)` using the in-memory shipping adapter.
2. Delete the 42 brittle unit tests that mocked internal helpers.
3. Test suite runtime drops from 4.2s to 0.3s; refactoring internals no longer causes test failures.

---

## 3. Operational Verification Harness

Run this script in any fresh, disposable directory to verify deep module invariants deterministically using Python 3's standard library.

```python andino-operational-example
import json
import os
import sys

def evaluate_module(definition: dict) -> dict:
    methods = definition.get("public_methods", [])
    params = definition.get("mandatory_params", 0)
    hidden_behaviors = definition.get("hidden_behaviors", 0)
    seams = definition.get("seams", [])
    
    # 1. Caller conceptual burden
    caller_burden = len(methods) + params
    if caller_burden == 0:
        return {"error": "Invalid interface: zero entrypoints", "status": "REJECTED"}
    
    # 2. Leverage Index calculation
    leverage = round(hidden_behaviors / caller_burden, 2)
    
    # 3. The 2-Adapter Invariant check
    hypothetical_seams = [s["name"] for s in seams if len(s.get("adapters", [])) < 2]
    
    # 4. Final classification
    is_deep = leverage >= 2.5 and len(hypothetical_seams) == 0
    
    return {
        "deep": is_deep,
        "leverage": leverage,
        "hypothetical_seams": hypothetical_seams,
        "status": "VERIFIED" if is_deep else "REJECTED"
    }

def probe():
    if os.getenv("ANDINO_NEGATIVE"):
        # Adversarial tamper: shallow pass-through with unbacked hypothetical seam
        shallow_spec = {
            "name": "OrderPassThrough",
            "public_methods": ["validate", "tax", "reserve", "ship", "pay"],
            "mandatory_params": 5,
            "hidden_behaviors": 2,
            "seams": [{"name": "SingleCarrierPort", "adapters": ["FedExProd"]}]
        }
        return evaluate_module(shallow_spec)
    
    # Normal production case: deep module with justified 2-adapter seam
    deep_spec = {
        "name": "OrderIntakeModule",
        "public_methods": ["processOrder"],
        "mandatory_params": 1,
        "hidden_behaviors": 6,
        "seams": [{"name": "ShippingPort", "adapters": ["FedExProd", "InMemoryFake"]}]
    }
    return evaluate_module(deep_spec)

if __name__ == "__main__":
    result = probe()
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "VERIFIED" and not os.getenv("ANDINO_NEGATIVE"):
        sys.exit(1)
```

### Execution Outputs
- **Default Execution**:
  ```json
  {"deep": true, "hypothetical_seams": [], "leverage": 3.0, "status": "VERIFIED"}
  ```
- **Adversarial Negative Execution (`ANDINO_NEGATIVE=1`)**:
  ```json
  {"deep": false, "hypothetical_seams": ["SingleCarrierPort"], "leverage": 0.2, "status": "REJECTED"}
  ```
