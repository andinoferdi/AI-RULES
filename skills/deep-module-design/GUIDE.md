# The Craft of Deep Module Design

This guide defines the comprehensive methodology for designing deep modules, placing architectural seams, maximizing caller leverage, and structuring testable software boundaries under Andino Workflow governance.

---

## 1. Foundations: The Philosophy of Deep Modules

In software engineering, complexity is not caused by a single catastrophic mistake; it accumulates through hundreds of tiny decisions that expose implementation details to callers.

John Ousterhout (*A Philosophy of Software Design*) observed that the best modules are **deep**: they hide significant implementation complexity behind a small, simple interface. Conversely, the worst modules are **shallow**: their interface is nearly as complex as the implementation itself.

```
┌─────────────────────────────────┐          ┌──────────────┐
│       SHALLOW MODULE            │          │ DEEP MODULE  │
│   (Avoid: Low Leverage)         │          │ (Exemplary)  │
├─────────────────────────────────┤          ├──────────────┴───────────────┐
│ Large Interface (Many Methods)  │          │ Small Interface (1-2 Methods)│
├─────────────────────────────────┤          ├──────────────────────────────┤
│ Thin Pass-Through Implementation│          │ Deep Implementation          │
│                                 │          │ (Complex Logic Hidden)       │
└─────────────────────────────────┘          └──────────────────────────────┘
```

### The Core Axiom of Depth
Depth is **leverage at the interface**. A module is deep when a caller (or test) can exercise vast behavioral capability per unit of mental effort required to learn the interface. Depth is **not** a ratio of lines of code—padding an implementation with verbose boilerplate does not make it deep.

---

## 2. The 8 Absolute Glossary Terms

Precision of language governs precision of thought. When designing or discussing architecture, you must use these eight terms exactly. **Never substitute vague corporate synonyms.**

| Term | Precise Definition | Discarded Synonyms (Never Use) |
|---|---|---|
| **Module** | Anything with an interface and an implementation. Scale-agnostic: a function, class, package, or subsystem. | *Unit, component, service, building block* |
| **Interface** | Everything a caller must know to use the module correctly: type signatures, invariants, ordering constraints, error modes, configuration, and performance traits. | *API, signature* (too narrow; refers only to syntax) |
| **Implementation** | The internal body of code that powers a module behind its interface. | *Underlying code, backend* |
| **Depth** | Leverage at the interface. The amount of observable behavior a caller exercises per concept learned. | *Code density, line ratio* |
| **Seam** | *(Michael Feathers)* A place where you can alter behavior without editing in that place. The physical location where an interface lives. | *Boundary* (overloaded with DDD bounded context) |
| **Adapter** | A concrete object or function that satisfies an interface at a seam. Describes *role* (what slot it fills), not substance. | *Driver, plugin, wrapper* |
| **Leverage** | What callers gain from depth: maximum capability with minimal cognitive surface area. One interface pays back across N call sites. | *Power, reusability* |
| **Locality** | What maintainers gain from depth: bugs, changes, and verification concentrate in one place rather than dispersing across callers. | *Cohesion, separation of concerns* |

---

## 3. Designing for High Leverage and Testability

An interface that is difficult to test is an interface with structural design defects. Great interfaces adhere to three core testability disciplines:

### 1. Accept Dependencies, Never Instantiate Them Internally
When a module constructs its own I/O clients, tests are forced to reach into global state or monkey-patch runtimes.

```typescript
// HARD TO TEST (Tightly coupled to network)
class OrderIntake {
  private gateway = new StripePaymentGateway(); // Brittle!
}

// TESTABLE & DEEP (Accepts port at the seam)
class OrderIntake {
  constructor(private gateway: PaymentPort) {} // Injects test adapter in suite
}
```

### 2. Return Observable Domain Results, Avoid Ambient Side-Effects
Functions that return values are trivially verifiable. Functions that mutate ambient global variables or hidden state require elaborate assertions.

```typescript
// HARD TO TEST (Ambient side-effect)
function applyDiscount(cart: Cart): void {
  cart.totalAmount -= computeDiscount(cart); // Mutates caller data in place!
}

// TESTABLE (Pure calculation returned)
function calculateDiscount(cart: Cart): DiscountSummary {
  return { amount: 1500, code: "SAVE15", applied: true };
}
```

### 3. Minimize Public Surface Area
Every public method added to an interface expands the test matrix and commits the module to long-term backwards compatibility. Two well-designed methods with sensible defaults beat twelve micro-methods.

---

## 4. Seam Justification & The 2-Adapter Invariant

A seam is not free; it introduces indirection, cognitive jumps, and type indirection. Therefore, a seam must be economically justified:

$$\text{1 Adapter} = \text{Hypothetical Seam (Wasteful Indirection)}$$
$$\text{2 Adapters} = \text{Real Seam (Justified Abstraction)}$$

### The Rule of Two Adapters
Do not introduce an interface or port unless at least two concrete adapters are required today. Typically:
1. **Production Adapter**: Real database, HTTP client, or third-party SDK.
2. **Test Adapter**: Fast in-memory stateful fake or local embedded engine.

If you only have one adapter and your tests use that same adapter (e.g., in-process computation or local SQLite), **do not create an interface**. Write a concrete class or function. Add the seam only when a second adapter arrives.

---

## 5. Parallel Exploration: Design-It-Twice

Human engineers and AI models alike suffer from anchoring bias: the first interface conceived almost always mimics existing file structures. To escape this trap, apply the **Design-It-Twice Protocol**:

```
┌────────────────────────────────────────────────────────┐
│               DESIGN-IT-TWICE DIVERGENCE               │
├────────────────────┬───────────────────────────────────┤
│ Agent 1: Minimal   │ 1-3 entrypoints. Zero config.     │
│ Agent 2: Flexible  │ Pluggable strategies and hooks.   │
│ Agent 3: Common    │ Trivial common case (90% default).│
│ Agent 4: Ports     │ Hexagonal isolation for networks. │
└────────────────────┴───────────────────────────────────┘
```

1. **Frame the Problem**: Ground constraints in a 15-line sketch of caller friction.
2. **Spawn Parallel Subagents**: Dispatch isolated agents with contradictory directives.
3. **Score on Leverage**: Calculate the Leverage Index ($L = B_{\text{hidden}} / C_{\text{caller}}$).
4. **Synthesize Opinionated Hybrid**: Select the winning candidate and graft high-value secondary traits.

*(See [resources/design-it-twice-protocols.md](resources/design-it-twice-protocols.md) for full execution templates).*

---

## 6. The AI-Navigability Advantage

In an era where autonomous coding agents write, debug, and review software, **deep modules provide a massive competitive advantage for AI engineering**:

1. **Token Window Conservation**: When an agent works on a feature, it must read caller files and imported interfaces. A shallow architecture forces the agent to read 15 micro-files into its context window, consuming tokens and triggering attention decay. A deep module presents a 20-line interface that tells the agent everything it needs.
2. **Hallucination Suppression**: AI agents hallucinate when forced to sequence complex multi-step calls across multiple files. By consolidating the sequencing, error recovery, and transactional boundaries *behind* a deep interface, the agent cannot violate ordering invariants.
3. **Blast Radius Quarantine**: When an agent edits an implementation behind a deep interface, changes cannot leak into callers. The caller code remains untouched and green.

---

## 7. The Refactoring & Test Replacement Lifecycle

When elevating shallow modules into a deep module, follow the **4-Phase Lifecycle**:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ 1. INVENTORY │ ──▶ │ 2. DEEPEN    │ ──▶ │ 3. TEST      │ ──▶ │ 4. CLEANUP   │
│ Map callers  │     │ Implement new│     │ Write tests  │     │ Delete old   │
│ & friction   │     │ deep seam    │     │ at deep seam │     │ tests & stubs│
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

1. **Inventory**: Identify callers repeating policy. Apply the Deletion Test.
2. **Deepen**: Build the deep module interface and internal implementation. Keep internal seams private.
3. **Test at the Interface**: Write thorough tests crossing the new external seam using real local stand-ins or in-memory adapters.
4. **Replace, Don't Layer**: Once caller tests pass, **delete the old, superseded unit tests** that asserted on the deprecated shallow helpers. Never maintain tests for dead internal abstractions.
