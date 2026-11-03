# Root Cause Investigation and Seam Isolation

Supporting reference for `skills/debugging/`. Operates under Andino Workflow governance.

---

## 1. Backward Data-Flow Tracing

When an error occurs deep inside a call stack or downstream service, jumping immediately to patch the line that crashed is the primary source of bug-patching regressions.

```
SYMPTOM (Crash / Bad Output)
   ▲
   │ [Step 1: Inspect crash point. What specific variable is corrupted/null?]
   │
CALLER FRAME N-1
   ▲
   │ [Step 2: Who passed this argument? Was it already corrupted here?]
   │
CALLER FRAME N-2
   ▲
   │ [Step 3: What calculation or lookup produced the bad value?]
   │
ORIGIN OF STATE (Root Cause)
```

### The 4-Step Tracing Technique

1. **Pinpoint the Contaminated Value**:
   - Do not stop at "function `formatUser()` threw TypeError".
   - Ask: "Which exact property was undefined? Was `user.profile.settings` missing, or was `user` itself null?"
2. **Step Backward Up the Call Hierarchy**:
   - Inspect the caller of the crashing function.
   - Did the caller pass the bad value directly, or did an intermediate transform mutate it?
3. **Locate the First Invariant Violation**:
   - Continue unwinding frames until you locate the exact boundary where valid state transitioned into invalid state.
   - For example: Did the database query return empty rows because of an unhandled outer join, or did the API deserializer strip unrecognized keys?
4. **Fix at the Origin, Not the Symptom**:
   - **Flawed Symptom Patch**: Adding `if (!user?.profile?.settings) return null;` in the UI component.
   - **Root Cause Fix**: Correcting the API query join or adding default domain values at the ingestion boundary.

---

## 2. Multi-Component Boundary Evidence Logging

In modern architectures (e.g., Client → API Gateway → Microservice → Database → Event Bus), errors rarely originate where they are displayed. Before altering code, place diagnostic probes at each system boundary.

### Structured Boundary Trace Pattern

```bash
# Boundary 1: Ingestion / HTTP Controller
[DEBUG-d4f1] INGESTION payload: {"tenant_id": "T1", "batch_size": 0}

# Boundary 2: Domain Service Input
[DEBUG-d4f1] SERVICE received: batch_size=0, resolving defaults...

# Boundary 3: Database Query Generation
[DEBUG-d4f1] DB_QUERY generated: SELECT * FROM items WHERE tenant_id = 'T1' LIMIT 0;

# Boundary 4: Result Parsing
[DEBUG-d4f1] RESULT rows returned: 0 (Expected > 0)
```

### The Tagged Instrumentation Protocol

1. **Tag Every Log with a Unique Session Tag**:
   Use a unique 4-character hex tag, e.g., `[DEBUG-a4f2]`.
   - Never use generic `console.log("here")` or `print(x)`.
   - Generic logs blend into framework output and get forgotten in commits.
2. **Log Boundary Invariants**:
   Log the entry shape, exit shape, and any conditional branch evaluations at boundaries.
   - Never log sensitive credentials, authorization headers, or customer PII.
   - Replace sensitive tokens with `<REDACTED>`.
3. **One-Command Cleanup**:
   Because every diagnostic line shares the exact tag, cleanup before verification is a single search-and-destroy:
   ```bash
   # Search for lingering debug probes across codebase
   git diff | grep "\[DEBUG-"
   ```

---

## 3. Formulating Falsifiable Hypotheses

Never proceed with fixing a bug based on an unstructured "feeling". Rank the plausible, falsifiable hypotheses before testing. Use three to five when the evidence supports that many.

### Hypothesis Syntax Standard

Each hypothesis must make a concrete, testable prediction:

> **Syntax**:
> *"If `<SUSPECTED_CAUSE>` is the root cause, then `<PROPOSED_MUTATION>` will `<OBSERVED_OUTCOME_PREDICTION>`."*

### Good vs. Bad Hypotheses

| Flawed / Vague Hypothesis | Falsifiable Engineering Hypothesis |
| :--- | :--- |
| "Maybe the database is slow." | "If connection pool exhaustion is causing timeouts, setting `pool_size=20` will eliminate request drops under 50 req/s load." |
| "React state isn't updating." | "If stale closure in `useEffect` captures the initial count, passing `count` to the dependency array will render the incremented value." |
| "Auth is broken." | "If JWT expiration timestamp is parsed as seconds instead of milliseconds, multiplying `exp * 1000` will allow valid tokens to pass validation." |

### Ranking and User Checkpoint

1. Rank hypotheses from highest probability to lowest.
2. Present the ranked list to the user when collaborating interactively. The user often has domain context ("we just changed that endpoint yesterday") that immediately eliminates #1 or elevates #3.
3. If autonomous, systematically test #1 first with a minimal probe. If disproven, discard it and move to #2. **Never layer speculative fixes on top of failed hypotheses.**

---

## 4. Load-Bearing Minimization

A large, noisy reproduction scenario obscures the real failure mechanism. Once a feedback loop is red, shrink it to the **absolute minimal reproduction**:

```
Minimization Protocol:
1. Prune Input Data:
   If a 100-line JSON payload triggers the bug, cut fields one by one.
   Keep only the fields that, when removed, turn the failure green.
2. Prune Steps & Callers:
   If reproducing takes 5 API calls, test if call #3 and #4 are actually necessary.
3. Prune Dependencies & Configuration:
   Strip out optional middleware, custom plugins, and third-party wrappers.
4. Verify Load-Bearing State:
   Every remaining line, property, or flag must be load-bearing.
   If removing it still causes the failure, it stays. If removing it fixes the bug, it is critical.
```

---

## 5. Identifying the Correct Architectural Seam

A regression test is only as trustworthy as the architectural seam it exercises.

### True Seam vs. False Seam

- **False Seam (Shallow Unit Mock)**:
  - Testing a function by mocking all 5 collaborators.
  - The test passes because the mocks match the developer's assumptions, but production fails because the real collaborators violate those assumptions.
- **True Seam (Integration / Contract Boundary)**:
  - Testing at the public entrypoint where the real interaction occurs (e.g., calling the service with real database transactions or HTTP endpoints).
  - Exercises the exact caller pattern that triggered the production incident.

### The Missing Seam Finding
If a codebase makes it impossible to write a focused, unattended regression test without spinning up 10 manual external systems or monkey-patching globals:
> **Document this explicitly as an Architectural Seam Finding.**
> Do not write a fake mock test and claim full verification. Flag that the module boundary lacks testability.
