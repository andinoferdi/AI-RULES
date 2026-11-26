# Security and performance review triggers

Resource for `andino-code-review`. These are the questions to ask of a diff during the
Standards pass. Depth lives in the sibling skills: `andino-security-and-hardening` for
threat modelling and hardening, `andino-performance-optimization` for measurement and
tuning. Two topics those skills do not cover, path containment and negative caching, are
kept here in full.

## 1. Security triggers

- **Trust boundaries**: where does data cross into the system (HTTP bodies and parameters,
  webhooks, third-party APIs, uploads, model output, worker messages, environment)? Which
  assets does the change touch (credentials, tokens, personal data, payments, admin
  actions)? Run STRIDE on new boundaries: spoofing, tampering, repudiation, information
  disclosure, denial of service, elevation of privilege.
- **Secrets**: no keys, passwords, connection strings or signing secrets in code, fixtures
  or logs; samples in `.env.example` hold placeholders only. Scan the pinned range:

  ```bash
  git diff <base>...<head> | grep -iE '(password|secret|api_key|access_token|private_key|bearer)\s*[:=]'
  ```

- **Authentication and authorization**: every non-public route requires a signed-in user;
  privileged operations check the role first; tokens check algorithm, expiry, issuer and
  audience. Ownership comes from the session, never from client input:

  ```typescript
  // Vulnerable: any signed-in user can read any order by id
  const order = await db.orders.findUnique({ where: { id: req.params.id } });

  // Secure: ownership tied to the authenticated session
  const order = await db.orders.findFirst({
    where: { id: req.params.id, userId: req.user.id },
  });
  if (!order) throw new NotFoundError('Order not found');
  ```

- **Input**: external data is parsed at the boundary with a strict schema (allowlist,
  unknown keys rejected) before business logic uses it.
- **Injection**: SQL uses parameters, never string building; subprocesses take argument
  arrays (`execFile`, `subprocess.run([...], shell=False)`), never a user string through a
  shell; output to HTML is encoded.
- **Untrusted model input**: retrieved or user-supplied text placed in a prompt is delimited
  as untrusted; a model's proposed tool arguments are checked against an allowlist before
  any destructive file or shell operation.

## 2. Path containment

When a change deletes, moves or writes files at a path derived from external input, check
that the target is canonicalised and contained:

- resolve symlinks with `realpath` before the containment check;
- the target lies strictly inside an allowlisted root;
- a minimum depth keeps the root itself out of reach.

```typescript
import { realpath } from 'node:fs/promises';
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

## 3. Performance triggers

- **Front end**: Core Web Vitals targets (LCP at most 2.5 s, INP at most 200 ms, CLS at most
  0.1); above-the-fold images not lazy-loaded; media with explicit width and height; long
  main-thread tasks split.
- **Queries**: no N+1 loops fetching related rows one at a time; new queries on large tables
  have an execution plan without unexpected full scans; composite indexes put equality
  columns before range or sort columns; no redundant indexes.
- **Resources**: one connection pool per process, never per request; pool size times
  instances stays within the database limit; fast connection timeouts; files, sockets and
  clients closed in `finally` or a scoped manager.
- **Bounds**: no unbounded loops or fetches; list endpoints paginate; no large objects
  allocated in hot paths.

## 4. Caching

- Cache-aside: read the cache; on a miss load from the source, store with a TTL, return.
- Every mutation that changes an entity evicts or updates its keys.
- **Negative caching**: cache the absence of a missing entity with a short TTL (30-60 s), so
  repeated lookups for ids that do not exist cannot stampede the database.

```typescript
async function getUserWithNegativeCache(userId: string): Promise<User | null> {
  const cached = await redis.get(`user:${userId}`);
  if (cached === '__NOT_FOUND__') return null;
  if (cached) return JSON.parse(cached);

  const user = await db.users.findUnique({ where: { id: userId } });
  if (!user) {
    await redis.set(`user:${userId}`, '__NOT_FOUND__', 'EX', 60);
    return null;
  }

  await redis.set(`user:${userId}`, JSON.stringify(user), 'EX', 3600);
  return user;
}
```
