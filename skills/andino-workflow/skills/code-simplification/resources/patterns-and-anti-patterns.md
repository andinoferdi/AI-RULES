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
  const id = user.id;
  const activeRoles = user.roles
    .filter(r => r.isActive)
    .map(r => r.name);
  return { ...byId, [id]: activeRoles };
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
with open("data.json", "r") as f:
    content = json.load(f)
```

Keep the original `open()` arguments. Adding `encoding="utf-8"` is a behavior change wherever
the platform's default encoding differs (Windows, for example); make it a separate, stated
change.

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

## 5. Behavior Traps

Each pair below looks like a harmless tidy-up and changes behavior. Keep the original form, or
make the change separately and say so.

### 5.1 Strict checks versus truthy checks

```python
# Original: only the boolean True counts as valid.
if item.get("valid") is True:
    process(item)

# Looks simpler, accepts 1, "yes" and any non-empty value as well.
if item.get("valid"):
    process(item)
```

```typescript
// Original: strict. `active: 1` or `active: "yes"` stay excluded.
users.filter((u) => u.active === true);

// Looks simpler, now includes them.
users.filter((u) => u.active);
```

### 5.2 Loose null checks

```typescript
// Original: skips null and undefined, keeps "" (an empty string is pushed).
if (u.email != null) emails.push(u.email.trim());

// `!== null` lets undefined through and then crashes on `.trim()`.
if (u.email !== null) emails.push(u.email.trim());

// A truthy test also drops "".
if (u.email) emails.push(u.email.trim());
```

### 5.3 `??` versus `||`

```typescript
// Original falls back for every falsy nickname: undefined, null, "" and 0.
const name = user.nickname ? user.nickname : `${user.firstName} ${user.lastName}`;

const sameBehavior = user.nickname || `${user.firstName} ${user.lastName}`;
// Changes behavior: "" and 0 are kept instead of falling back.
const different = user.nickname ?? `${user.firstName} ${user.lastName}`;
```

### 5.4 Iteration protocol

```typescript
// Original index loop accepts any object with a length and indexed elements,
// such as { length: 2, 0: "a", 1: "b" }.
for (let i = 0; i < items.length; i++) handle(items[i]);

// for...of needs an iterator and throws a TypeError on that plain object.
for (const item of items) handle(item);
```

### 5.5 Default arguments

```python
# Original: only None gets the default; a caller's own empty mapping is kept.
opts = {} if options is None else options

# Replaces every falsy value, including an empty custom mapping, with a new dict.
opts = options or {}
```

For the `async` wrapper trap, see 2.4.
