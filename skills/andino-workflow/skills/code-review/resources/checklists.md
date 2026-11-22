# Security and Performance Review Checklists

Comprehensive engineering checklists for deep standards-track reviews under Andino Workflow governance. These checklists synthesize enterprise security controls, OWASP guidelines, and runtime performance invariants.

---

## 1. Security Review Checklist

Use this checklist to evaluate whether proposed changes introduce vulnerabilities or weaken existing security postures.

### 1.1 Threat Modeling & Trust Boundaries
Before inspecting code lines, establish the security perimeter:
- [ ] **Trust Boundaries Identified:** Map every point where data crosses boundaries (HTTP requests, URL params, webhook payloads, third-party APIs, file uploads, LLM completions, IPC/worker messages, and environment variables).
- [ ] **Assets & Privileges Classified:** Identify sensitive assets touched by this change (passwords, tokens, PII, payment info, administrative capabilities, private keys, database credentials).
- [ ] **STRIDE Review Applied:**
  - *Spoofing:* Can an attacker impersonate another user or service?
  - *Tampering:* Can data be altered in transit or in storage without detection?
  - *Repudiation:* Can actions be taken without verifiable audit logs?
  - *Information Disclosure:* Are internal stack traces, DB schemas, or sensitive keys exposed?
  - *Denial of Service:* Can an unauthenticated request trigger expensive computations, unbounded memory allocations, or connection pool exhaustion?
  - *Elevation of Privilege:* Can an unprivileged user execute administrative endpoints (IDOR)?

### 1.2 Secrets & Credential Leak Prevention
- [ ] **No Hardcoded Secrets:** No API keys, passwords, database URLs, JWT signing secrets, or private tokens in source code or committed fixtures.
- [ ] **Diff Scanning Pattern:** Scan all changed lines against credential regex patterns:
  ```bash
  git diff HEAD~1..HEAD | grep -iE '(password|secret|api_key|access_token|private_key|bearer)\s*[:=]'
  ```
- [ ] **Environment Segregation:** Secrets loaded strictly from environment managers or vault services; sample values documented in `.env.example` with harmless placeholders.

### 1.3 Authentication & Authorization (AuthN & AuthZ)
- [ ] **Protected Endpoint Verification:** Every non-public route enforces authentication middleware.
- [ ] **Ownership Verification (Anti-IDOR):** When accessing resource by ID (e.g. `/api/orders/:id`), verify that the authenticated user actually owns the resource:
  ```typescript
  // VULNERABLE: Direct object reference without ownership check
  const order = await db.orders.findUnique({ where: { id: req.params.id } });

  // SECURE: Ownership tied to authenticated session
  const order = await db.orders.findFirst({
    where: { id: req.params.id, userId: req.user.id }
  });
  if (!order) throw new NotFoundError('Order not found');
  ```
- [ ] **Role-Based Access Control (RBAC):** Admin or privileged operations explicitly verify required roles/claims before executing domain logic.
- [ ] **Token Validation:** JWT tokens validate signature algorithm (preventing `alg: none`), expiration (`exp`), issuer (`iss`), and audience (`aud`).

### 1.4 Input Validation & Injection Prevention
- [ ] **Schema Validation at Boundaries:** All external data validated using strict schema parsers (e.g., Zod, Pydantic, Joi) using allowlists, never denylists:
  ```typescript
  // Validate at system boundary before business logic
  const UpdateProfileSchema = z.object({
    username: z.string().trim().min(3).max(30).regex(/^[a-zA-Z0-9_-]+$/),
    email: z.string().email().max(255),
    age: z.number().int().min(18).max(120).optional(),
  }).strict(); // Disallow unexpected keys
  ```
- [ ] **SQL / Database Queries Parameterized:** Zero string concatenation in query construction:
  ```python
  # VULNERABLE
  cursor.execute(f"SELECT * FROM users WHERE email = '{user_email}'")

  # SECURE (Parameterized)
  cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))
  ```
- [ ] **Command Execution Sanitization:** Avoid raw shell calls (`child_process.exec`, `os.system`). Where subcommands are necessary, use argument arrays (`execFile`, `subprocess.run(..., shell=False)`) without passing user strings to a shell.

### 1.5 Destructive Path Operations & Filesystem Containment
When deleting, moving, or writing files where the path is derived from external input, enforce strict directory containment:
- [ ] **Symlink Resolution Pre-Check:** Canonicalize path with `realpath` before containment assertion.
- [ ] **Allowlisted Roots:** Ensure the target resides completely inside an authorized directory.
- [ ] **Minimum Depth Guard:** Prevent targeting the root directory itself.
```typescript
import { realpath, readFile } from 'node:fs/promises';
import { resolve, relative, isAbsolute, sep } from 'node:path';

const ALLOWED_ROOTS = ['/var/app/data/uploads'];
const MIN_DEPTH = 1;

async function assertSafePath(candidate: string): Promise<string> {
  const resolved = resolve(candidate);
  const target = await realpath(resolved).catch(() => resolved);

  const isSafe = ALLOWED_ROOTS.some(root => {
    const rel = relative(root, target);
    if (rel === '' || rel === '..' || rel.startsWith(`..${sep}`) || isAbsolute(rel)) {
      return false;
    }
    return rel.split(sep).length >= MIN_DEPTH;
  });

  if (!isSafe) {
    throw new SecurityError(`Path traversal attempt detected: ${candidate}`);
  }
  return target;
}
```

### 1.6 AI & LLM Security (Untrusted Prompt Boundaries)
- [ ] **Untrusted Data Quarantine:** Any data retrieved from external sources, web scraping, user comments, or third-party APIs passed into an LLM prompt must be wrapped in clear delimiters (`<untrusted-content>` ... `</untrusted-content>`).
- [ ] **Tool Call Validation:** Never allow an LLM's suggested tool arguments to execute destructive shell or file operations without programmatic assertion against allowlists.

---

## 2. Performance Review Checklist

Use this checklist to identify architectural bottlenecks, latency regressions, and inefficient resource consumption.

### 2.1 Core Web Vitals Targets
Review frontend changes against production thresholds:
| Metric | Target (Good) | Needs Work | Poor (Blocker) |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | $\le 2.5\text{s}$ | $2.5\text{s} - 4.0\text{s}$ | $> 4.0\text{s}$ |
| **INP** (Interaction to Next Paint) | $\le 200\text{ms}$ | $200\text{ms} - 500\text{ms}$ | $> 500\text{ms}$ |
| **CLS** (Cumulative Layout Shift) | $\le 0.1$ | $0.1 - 0.25$ | $> 0.25$ |

- [ ] **Hero Images:** Above-the-fold images use `fetchpriority="high"` and are never lazy-loaded.
- [ ] **Layout Stability:** All `<img>`, `<video>`, and responsive media have explicit `width` and `height` attributes to prevent layout shifts.
- [ ] **Main Thread Responsiveness:** Long tasks ($> 50\text{ms}$) chunked using `scheduler.yield()` or Web Workers to keep INP under 200ms.

### 2.2 Database Query Optimization & N+1 Prevention
- [ ] **N+1 Query Elimination:** Loops fetching related records individually are refactored into eager joins or batch lookups:
  ```typescript
  // ANTI-PATTERN: N+1 queries (1 query for users + N queries for orders)
  const users = await db.users.findMany();
  for (const user of users) {
    user.orders = await db.orders.findMany({ where: { userId: user.id } });
  }

  // OPTIMIZED: 1 query with join or batching
  const usersWithOrders = await db.users.findMany({
    include: { orders: true }
  });
  ```
- [ ] **EXPLAIN ANALYZE Baselining:** Any new query on tables expected to hold $>10,000$ rows has a documented execution plan:
  - No unexpected `Seq Scan` on large tables.
  - Estimated rows vs actual rows within the same order of magnitude.
  - Sorting handled by composite index rather than in-memory quicksort.
- [ ] **Indexing Strategy:**
  - Composite index column ordering follows: Equality columns first, followed by Range/Sort columns (`WHERE tenant_id = ? AND created_at > ?` -> index `(tenant_id, created_at)`).
  - Covering indexes considered for high-frequency read paths.
  - No redundant or duplicate indexes (every index imposes a write tax on `INSERT`/`UPDATE`).

### 2.3 Connection Pooling & Resource Lifecycles
- [ ] **Process-Level Pooling:** Database connection pool instantiated once per application process, never per HTTP request.
- [ ] **Connection Limits:** `instances * pool_max <= db_max_connections`.
- [ ] **Fast Timeouts:** `connectionTimeoutMillis` set (e.g. 2000ms) so connection exhaustion fails fast instead of hanging server threads indefinitely.
- [ ] **Deterministic Resource Release:** File descriptors, sockets, streams, and database clients guaranteed to close in `finally` blocks or using scoped resource managers (`with open(...)`, `using`).

### 2.4 Caching Architecture & Negative Caching
- [ ] **Cache-Aside Pattern:** Read from cache; on miss, load from source, populate cache with TTL, and return.
- [ ] **Cache Invalidation:** Every mutation that changes entity state explicitly evicts or updates relevant cache keys.
- [ ] **Negative Caching:** When querying for entities that do not exist (e.g. 404 lookups), cache the *absence* with a short TTL (e.g. 30-60s) to prevent cache-stampede denial of service on backend databases:
  ```typescript
  async function getUserWithNegativeCache(userId: string): Promise<User | null> {
    const cached = await redis.get(`user:${userId}`);
    if (cached === '__NOT_FOUND__') return null;
    if (cached) return JSON.parse(cached);

    const user = await db.users.findUnique({ where: { id: userId } });
    if (!user) {
      // Negative cache sentinel with short TTL
      await redis.set(`user:${userId}`, '__NOT_FOUND__', 'EX', 60);
      return null;
    }

    await redis.set(`user:${userId}`, JSON.stringify(user), 'EX', 3600);
    return user;
  }
  ```
