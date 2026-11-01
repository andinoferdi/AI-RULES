# Leverage Rubric & Multi-Ecosystem Catalogs

This resource provides the mathematical leverage scorecard, terminal-native visual patterns, and multi-language transformation catalogs for designing deep modules across modern engineering stacks.

---

## 1. The Quantified Leverage Scorecard

To eliminate subjective debates about whether an interface is "clean" or "too big," evaluate modules using the **Leverage Index ($L$)**:

$$L = \frac{B_{\text{hidden}}}{C_{\text{caller}}}$$

Where:
- $B_{\text{hidden}}$ (**Hidden Behaviors**): The count of distinct domain rules, error retries, validations, state transitions, and persistence steps executed inside the module.
- $C_{\text{caller}}$ (**Caller Burden**): The count of distinct concepts the caller must learn: (Public Methods) + (Mandatory Parameters) + (Custom Configuration Options) + (Distinct Error Codes Handled).

```
┌────────────────────────────────────────────────────────────────────────┐
│                        LEVERAGE SCORECARD                              │
├───────────────┬─────────────────┬──────────────────────────────────────┤
│ Leverage Index│ Classification  │ Action Required                      │
├───────────────┼─────────────────┼──────────────────────────────────────┤
│ L < 1.5       │ Shallow Module  │ Collapse into caller or deepen       │
│ 1.5 <= L < 3.0│ Moderate Depth  │ Simplify parameters; hide defaults   │
│ L >= 3.0      │ Deep Module     │ Exemplary; stable high-leverage seam │
└───────────────┴─────────────────┴──────────────────────────────────────┘
```

---

## 2. Terminal-Native Visual Cards

Visual diagrams communicate architectural shallowness faster than prose. Use these terminal-friendly patterns in reviews and pull requests:

### Pattern A: The Mass Diagram
Illustrates the ratio between the exposed surface area and hidden implementation.

```
SHALLOW MODULE (L = 1.0)                 DEEP MODULE (L = 5.0)
┌─────────────────────────────┐          ┌───────────────┐
│       INTERFACE (WIDE)      │          │INTERFACE(TINY)│  ← 1-2 methods
├─────────────────────────────┤          ├───────────────┴─────────────┐
│                             │          │                             │
│    Implementation (Thin)    │          │                             │
│                             │          │    Deep Implementation      │
└─────────────────────────────┘          │    (Complex logic hidden)   │
                                         │                             │
                                         └─────────────────────────────┘
```

### Pattern B: The Cross-Section (Layer Collapse)
Shows how shallow pass-through layers are consolidated into a cohesive domain seam.

```
BEFORE: 5 Fragmented Layers                AFTER: Consolidated Deep Seam
┌──────────────────────────────────────┐   ┌──────────────────────────────────────┐
│ Controller                           │   │ Controller / API Route               │
├──────────────────────────────────────┤   ├──────────────────────────────────────┤
│ OrderService (Pass-through)          │   │                                      │
├──────────────────────────────────────┤   │                                      │
│ OrderValidator (Pass-through)        │   │          OrderIntake Module          │
├──────────────────────────────────────┤   │   (Validation, Taxes, Inventory,     │
│ TaxCalculator (Shallow helper)       │   │    Persistence, and Notification)    │
├──────────────────────────────────────┤   │                                      │
│ OrderRepository (CRUD wrapper)       │   │                                      │
└──────────────────────────────────────┘   └──────────────────────────────────────┘
```

---

## 3. Multi-Ecosystem Transformation Catalogs

### Catalog 1: TypeScript & Modern JavaScript

#### Anti-Pattern: Fragmented Micro-Services
Callers must orchestrate multiple imports, remember execution order, and handle partial rollbacks:

```typescript
// SHALLOW: Caller is burdened with 5 concepts and strict ordering
import { validateCart } from "./validateCart";
import { calculateTaxes } from "./calculateTaxes";
import { reserveStock } from "./reserveStock";
import { chargePayment } from "./chargePayment";
import { saveOrder } from "./saveOrder";

export async function checkoutRoute(req, res) {
  const cart = await validateCart(req.body);
  const tax = await calculateTaxes(cart, req.body.address);
  const reservation = await reserveStock(cart.items);
  try {
    const payment = await chargePayment(cart.total + tax, req.body.token);
    const order = await saveOrder(cart, payment, reservation);
    res.json(order);
  } catch (err) {
    await reservation.rollback();
    throw err;
  }
}
```

#### Deep Pattern: Single High-Leverage Seam
The caller learns exactly one concept. All validation, rollbacks, and persistence are encapsulated:

```typescript
// DEEP: Small interface (L >= 4.0), caller learns 1 method
import { orderIntake } from "@/modules/order-intake";

export async function checkoutRoute(req, res) {
  // All invariants, reservations, tax lookups, and compensation logic hidden
  const order = await orderIntake.checkout({
    cartId: req.body.cartId,
    paymentToken: req.body.token,
    address: req.body.address,
  });
  res.json(order);
}
```

---

### Catalog 2: Python

#### Anti-Pattern: Scattered Functional Proceduralism
Logic spread across helper files with no locality; callers recreate the workflow:

```python
# SHALLOW: Caller must assemble 4 separate tools and handle storage state
from etl.cleaner import clean_csv
from etl.normalizer import normalize_headers
from etl.validator import validate_schema
from etl.db import insert_records

def process_file(path: str):
    raw = clean_csv(path)
    normalized = normalize_headers(raw)
    valid, errors = validate_schema(normalized)
    if errors:
        raise ValueError(f"Schema mismatch: {errors}")
    insert_records(valid)
```

#### Deep Pattern: Domain Ingestion Engine
Dependencies are accepted in `__init__` (defaulting to production storage), while `ingest()` hides the entire multi-step pipeline:

```python
# DEEP: High leverage, easily testable with in-memory stand-in
from dataclasses import dataclass
from typing import Protocol

class IngestionEngine:
    def __init__(self, storage=None, validator=None):
        self._storage = storage or DefaultDbStorage()
        self._validator = validator or DefaultSchemaValidator()

    def ingest(self, file_path: str) -> IngestionSummary:
        """Single public entrypoint: parses, normalizes, validates, and commits."""
        cleaned = self._clean(file_path)
        normalized = self._normalize(cleaned)
        self._validator.assert_valid(normalized)
        return self._storage.bulk_commit(normalized)
```

---

### Catalog 3: Go

#### Anti-Pattern: Gratuitous Single-Adapter Interfaces
Creating an interface for every struct, creating indirection without polymorphism:

```go
// SHALLOW: Interface bloat with only 1 concrete implementation
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*User, error)
    Update(ctx context.Context, u *User) error
    Delete(ctx context.Context, id string) error
}

type userService struct {
    repo UserRepository // Only ever satisfies by *postgresUserRepo
}
```

#### Deep Pattern: Concrete Struct with Pure Domain Interface
Keep the struct concrete and internal seams private. Introduce interfaces only at genuine boundaries:

```go
// DEEP: Concrete domain module with small interface
type UserManager struct {
    db *sql.DB // Internalized, not exported
}

func NewUserManager(db *sql.DB) *UserManager {
    return &UserManager{db: db}
}

// Single high-leverage entrypoint: handles audit logs, password hashing, and DB transaction
func (m *UserManager) Register(ctx context.Context, req RegisterRequest) (*User, error) {
    // 5 internal steps hidden behind one public call
    return m.executeRegistration(ctx, req)
}
```

---

### Catalog 4: Rust

#### Anti-Pattern: Leaking Intermediate State Types
Callers must manage internal phase transitions and lifetime annotations:

```rust
// SHALLOW: Caller exposed to intermediate pipeline states
let raw_data = Parser::new(&input).parse_tokens()?;
let type_checked = TypeChecker::new().check(raw_data)?;
let optimized = Optimizer::new(OptLevel::O2).optimize(type_checked)?;
let byte_code = CodeGen::emit(optimized)?;
```

#### Deep Pattern: Typestate Encapsulation & Opaque Facade
The complex compiler pipeline is hidden behind a single method call:

```rust
// DEEP: High-leverage facade with zero internal state exposure
pub struct Compiler {
    opt_level: OptLevel,
}

impl Compiler {
    pub fn new() -> Self {
        Self { opt_level: OptLevel::Default }
    }

    pub fn compile(&self, source: &str) -> Result<ByteCode, CompileError> {
        // Tokenization, typechecking, AST optimization, and codegen hidden
        let tokens = self.tokenize(source)?;
        let ast = self.parse(tokens)?;
        let checked = self.typecheck(ast)?;
        self.codegen(checked)
    }
}
```
