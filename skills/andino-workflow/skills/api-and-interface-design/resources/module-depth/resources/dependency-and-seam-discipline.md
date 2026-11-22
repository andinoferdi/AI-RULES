# Dependency & Seam Discipline

This resource establishes the mechanical rules for classifying dependencies, placing architectural seams, and managing test surfaces when designing deep modules under Andino Workflow governance.

---

## 1. The 4 Dependency Categories

When assessing any module candidate for deepening, you must classify every dependency it touches. The category dictates where the interface sits, how it is tested, and whether an adapter is justified.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             DEPENDENCY TAXONOMY                                  │
├─────────────────────────┬──────────────────────────┬─────────────────────────────┤
│ Category                │ Seam Location            │ Testing Strategy            │
├─────────────────────────┼──────────────────────────┼─────────────────────────────┤
│ 1. In-Process           │ No Seam (Internalized)   │ Direct invocation           │
│ 2. Local-Substitutable  │ Internal Seam            │ Local stand-in (SQLite/mem) │
│ 3. Remote-but-Owned     │ External Seam (Port)     │ In-memory fake adapter      │
│ 4. True External        │ External Seam (Port)     │ Injected mock / contract    │
└─────────────────────────┴──────────────────────────┴─────────────────────────────┘
```

### Category 1: In-Process Dependencies
- **Definition**: Pure computation, mathematical formulas, string/date formatting, in-memory tree/graph traversal, validation logic, and state machines with zero I/O.
- **Rule**: **Always deepenable without a port.** Merge the fragmented helpers directly into the deep module's implementation.
- **Seam**: None. Do not create an interface or port for an in-process helper. Callers invoke the module's public entrypoint directly.
- **Testing**: Test purely through the public interface. The in-process logic is thoroughly exercised as a natural consequence of caller operations.

### Category 2: Local-Substitutable Dependencies
- **Definition**: Low-level infrastructure that has battle-tested, high-fidelity in-memory or embedded local stand-ins (e.g., PGLite/SQLite for relational databases, in-memory virtual filesystems, local Redis instances).
- **Rule**: **Deepenable with an internal seam.** The deep module executes against the local stand-in directly during tests.
- **Seam**: **Internal only.** Never expose database queries, repositories, or connection handles through the module's public interface. Callers see only domain operations (`orderModule.checkout(...)`), not storage mechanics.
- **Testing**: Run integration tests against the local stand-in in the test suite. No mocking required.

### Category 3: Remote-but-Owned Dependencies (Ports & Adapters)
- **Definition**: Services that live across a network boundary (e.g., internal microservices, gRPC backends, event brokers, background workers) which your organization owns and controls.
- **Rule**: **Define a Port at the seam; inject the Adapter.** The deep module owns all business logic, retry policies, payload transformations, and error handling. The transport is injected as an adapter.
- **Seam**: **External seam at the boundary.** Provide exactly two adapters:
  1. *Production Adapter*: Real HTTP/gRPC/Kafka transport.
  2. *Test Adapter*: Fast in-memory stateful fake (recording calls, returning deterministic responses).
- **Canonical Recommendation Shape**:
  > *"Define a Port at the seam. Implement a production gRPC adapter and an in-memory test adapter so that the business policy sits entirely within one deep module even though deployment spans a network boundary."*

### Category 4: True External Dependencies
- **Definition**: Third-party services completely outside your control (e.g., Stripe, Twilio, SendGrid, OpenAI API, AWS S3).
- **Rule**: **Quarantine behind a domain-shaped Port.** Never leak third-party SDK types or error objects through your module interface.
- **Seam**: **External seam.** The interface must speak the module's domain vocabulary, not the vendor's vocabulary.
- **Testing**: Inject a mock adapter or contract-verified fake in tests. Assert that the module handles vendor network failures, rate limits, and partial outages gracefully.

---

## 2. Seam Discipline: The 2-Adapter Invariant

A **Seam** (Michael Feathers) is *"a place where you can alter behavior without editing in that place."* It is the physical location where an interface lives.

### The 2-Adapter Invariant
```
┌────────────────────────────────────────────────────────┐
│  1 Adapter  ==  Hypothetical Seam (Pure Indirection)   │
│  2 Adapters ==  Real Seam (Justified Abstraction)      │
└────────────────────────────────────────────────────────┘
```

- **The Indirection Trap**: Creating an interface `IOrderRepository` when the only implementation that ever exists is `PostgresOrderRepository` (and tests use a generic mock library that inspects SQL calls) is speculative complexity.
- **The Requirement**: Before introducing a seam, name both concrete adapters:
  - Adapter 1 (Production): Real transport / real infrastructure.
  - Adapter 2 (Test / Alternative): Deterministic in-memory fake, local stand-in, or secondary provider.
- **If only one adapter exists**, delete the port. Program directly against the concrete class or function. Add the seam only when a second concrete adapter arrives.

---

## 3. Internal Seams vs. External Seams

A foundational error in module design is treating all seams as public.

```
┌───────────────────────────────────────────────────────────┐
│ DEEP MODULE BOUNDARY                                      │
│                                                           │
│   ┌───────────────────────────────────────────────────┐   │
│   │ EXTERNAL SEAM (Public Interface)                  │   │
│   │   checkout(cart, customer): Result<Order>         │   │
│   └─────────────────────────┬─────────────────────────┘   │
│                             │                             │
│       ┌─────────────────────┴─────────────────────┐       │
│       │ IMPLEMENTATION INTERNALS                  │       │
│       │                                           │       │
│       │   ┌───────────────────────────────────┐   │       │
│       │   │ INTERNAL SEAM (Private to Module) │   │       │
│       │   │   RateCalculator, TaxEngine       │   │       │
│       │   └───────────────────────────────────┘   │       │
│       └───────────────────────────────────────────┘       │
└───────────────────────────────────────────────────────────┘
```

- **External Seam**: The contract presented to callers and external test suites. Must remain minimal, stable, and high-leverage.
- **Internal Seam**: Private boundaries inside the module's implementation used to organize internal code.
- **The Golden Rule**: **Never expose internal seams through the external interface merely to facilitate unit testing.** If you feel compelled to export a private helper just to test it, the external interface is the wrong shape or the test is crossing the wrong boundary.

---

## 4. Testing Strategy: "Replace, Don't Layer"

When shallow modules are consolidated into a deep module, their test suites must be transformed according to strict discipline:

```
BEFORE: Layered Waste                      AFTER: Interface Alignment
┌─────────────────────────┐               ┌─────────────────────────┐
│ 15 Fragmented Tests     │ ──▶ DELETE ──▶│ 4 Deep Interface Tests  │
│ (Mocking each other)    │               │ (Testing full behavior) │
└─────────────────────────┘               └─────────────────────────┘
```

### The 4 Testing Invariants
1. **The Interface is the Test Surface**: Callers and tests cross the exact same external seam. If an external test reaches *past* the interface to assert on private variables or internal call counts, the test is fragile and defeats refactoring.
2. **Delete Old Shallow Tests**: Once tests at the new deep interface prove behavioral parity, delete the superseded unit tests for the old shallow functions. Keeping them creates double maintenance and prevents future internal optimizations.
3. **Assert on Observable Outcomes**: Tests assert on returned domain values, emitted events, and persistent state changes—never on internal method invocations or intermediate variable assignments.
4. **Survive Internal Refactorings**: A test that breaks when internal implementation changes—even though external inputs and outputs remain identical—is testing past the interface. Rewrite it to target the external seam.
