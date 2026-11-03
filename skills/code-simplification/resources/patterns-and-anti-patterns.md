# Code Simplification: Patterns & Anti-Patterns Catalog

This catalog provides concrete, multi-language transformation recipes and anti-pattern warnings. Every pattern illustrates the shift from accidental complexity to readable, maintainable clarity.

---

## 1. Structural Complexity Catalog

| Smell / Signal | Root Problem | Recommended Remedy |
|---|---|---|
| **Deep Nesting (3+ levels)** | Control flow branches expand horizontally, straining mental stack. | Convert inverted conditions into **top-level guard clauses** with early returns. |
| **Monolithic Functions (50+ lines)** | Mixed levels of abstraction and multiple responsibilities. | Extract distinct phases into **named helper functions** that mirror the domain problem. |
| **Nested Ternaries** | Operator precedence and branching become difficult to parse visually. | Replace with **lookup maps**, `switch` statements, or linear `if/else` ladders. |
| **Boolean Flag Arguments** | `createUser("Andino", true, false, true)` is opaque at the call site. | Replace with a typed **options object** or separate dedicated functions (`createUserAdmin()`). |
| **Repeated Conditionals** | The same complex boolean expression is duplicated across branches. | Extract into a **well-named predicate function** (e.g. `isEligibleForDiscount(user)`). |
| **Dead Pass-Throughs** | Superfluous wrappers or `else: pass` blocks that do nothing. | Inline trivial passthroughs and eliminate no-op branches. |

---

## 2. TypeScript & Modern JavaScript Recipes

### 2.1 Nested Ternary vs Lookup Mapping

```typescript
// [UNCLEAR]: Dense ternary chain requiring mental stack parsing
const badgeColor = status === 'active' 
  ? 'green' 
  : status === 'pending' 
  ? 'amber' 
  : status === 'suspended' 
  ? 'red' 
  : 'gray';

// [CLEAR]: Keep strict string matching and the fallback for every other value.
function colorForStatus(status: string): string {
  switch (status) {
    case 'active': return 'green';
    case 'pending': return 'amber';
    case 'suspended': return 'red';
    default: return 'gray';
  }
}
const badgeColor = colorForStatus(status);
```

### 2.2 Unreadable Reduce vs Explicit Iteration

```typescript
// [UNCLEAR]: Chained reduce mutating accumulators or spreading objects
const userById = users.reduce((acc, user) => ({
  ...acc,
  [user.id]: user.roles.filter(r => r.isActive).map(r => r.name)
}), {});

// [CLEAR]: Keep reduce traversal and the plain object with own data properties.
const userById = users.reduce<Record<string, string[]>>((byId, user) => {
  const activeRoles = user.roles
    .filter(r => r.isActive)
    .map(r => r.name);
  return { ...byId, [user.id]: activeRoles };
}, {});
```

### 2.3 Redundant Boolean Branching

```typescript
// [UNCLEAR]: Explicitly returning boolean literals
function canAccess(user: User): boolean {
  if (user.isVerified && !user.isBanned) {
    return true;
  } else {
    return false;
  }
}

// [CLEAR]: Direct predicate expression
function canAccess(user: User): boolean {
  return Boolean(user.isVerified && !user.isBanned);
}
```

### 2.4 Async Boundary to Keep

```typescript
// This boundary turns a synchronous service throw into a rejected promise.
async function fetchConfig(key: string): Promise<Config> {
  return await configService.get(key);
}
```

Keep the wrapper when callers rely on rejection behavior, promise identity or settlement order. Check local error handling and cleanup before changing `return await`.

---

## 3. Python Recipes

### 3.1 Flattening Deep Nested Trees into Guard Clauses

```python
# [UNCLEAR]: Deep pyramid of nested conditionals
def process_order(order):
    if order is not None:
        if order.is_paid():
            if order.has_inventory():
                if not order.is_cancelled():
                    order.dispatch()
                    return {"status": "dispatched"}
                else:
                    raise ValueError("Order is cancelled")
            else:
                raise StockError("Insufficient inventory")
        else:
            raise PaymentError("Order not paid")
    else:
        raise TypeError("Order cannot be None")

# [CLEAR]: Linear guard clauses with immediate exits
def process_order(order):
    if order is None:
        raise TypeError("Order cannot be None")
    if not order.is_paid():
        raise PaymentError("Order not paid")
    if not order.has_inventory():
        raise StockError("Insufficient inventory")
    if order.is_cancelled():
        raise ValueError("Order is cancelled")

    order.dispatch()
    return {"status": "dispatched"}
```

### 3.2 Verbose Dictionary Building vs Comprehension

```python
# [UNCLEAR]: Imperative dictionary population
active_names = {}
for user in users:
    if user.is_active:
        active_names[user.id] = user.display_name.strip()

# [CLEAR]: Clean dictionary comprehension
active_names = {
    user.id: user.display_name.strip()
    for user in users
    if user.is_active
}
```

### 3.3 Context Managers vs Manual Cleanup

```python
# [UNCLEAR]: Error-prone manual file handling
f = open("data.json", "r")
try:
    content = json.load(f)
finally:
    f.close()

# [CLEAR]: Idiomatic context manager ensuring resource release
with open("data.json", "r", encoding="utf-8") as f:
    content = json.load(f)
```

---

## 4. React & Frontend Recipes

### 4.1 Conditional Render Spaghetti vs Extracted Subcomponents

```tsx
// [UNCLEAR]: Nested JSX ternaries inside template body
function ProfileCard({ user, isLoading, error }: Props) {
  return (
    <div className="card">
      {isLoading ? (
        <Spinner />
      ) : error ? (
        <ErrorMessage error={error} />
      ) : user ? (
        user.isPremium ? (
          <PremiumView user={user} />
        ) : (
          <StandardView user={user} />
        )
      ) : (
        <EmptyState />
      )}
    </div>
  );
}

// [CLEAR]: Guard returns or computed content variable
function ProfileCard({ user, isLoading, error }: Props) {
  if (isLoading) return <div className="card"><Spinner /></div>;
  if (error) return <div className="card"><ErrorMessage error={error} /></div>;
  if (!user) return <div className="card"><EmptyState /></div>;

  return (
    <div className="card">
      {user.isPremium ? <PremiumView user={user} /> : <StandardView user={user} />}
    </div>
  );
}
```

---

## 5. Over-Simplification Anti-Patterns (The Traps)

Simplification has a treacherous failure mode: **over-simplification**. Agents must actively avoid these 4 traps:

### Trap 1: Aggressive Inlining of Domain Concepts
- **The Mistake**: Inlining a 2-line function `function isSessionExpired(session) { return Date.now() > session.expiresAt; }` directly into 5 call sites to "reduce function count."
- **Why It Fails**: You destroyed a named ubiquitous domain concept. The call sites now leak low-level time arithmetic into high-level business flows.
- **Rule**: If a function names a meaningful domain rule, keep it.

### Trap 2: Optimizing for Line Count (Code Slop)
- **The Mistake**: Replacing a readable 6-line `if/else` block with an unreadable, clever 1-line regular expression or chained bitwise operator.
- **Why It Fails**: Line count is NOT complexity. The true benchmark is **Comprehension Speed**: *"Can an on-call engineer at 2 AM locate a bug in this function in 15 seconds?"*
- **Rule**: Prefer explicit clarity over clever compression.

### Trap 3: Stripping Defensive Checks
- **The Mistake**: Deleting `if (!item) return null;` because the current unit test always passes valid objects.
- **Why It Fails**: In production, asynchronous payloads, external API drops, or legacy data frequently introduce `null`. Stripping defensive checks causes catastrophic runtime crashes.
- **Rule**: Never remove error handling unless caller contract invariants mathematically guarantee impossibility.

### Trap 4: Premature DRY (False Duplication)
- **The Mistake**: Merging `calculateShippingTax()` and `calculateCorporateDiscountTax()` because their formulas look identical today.
- **Why It Fails**: They represent two completely different business axes that evolve independently. Unifying them couples unrelated requirements.
- **Rule**: Duplication is far cheaper than the wrong abstraction.
