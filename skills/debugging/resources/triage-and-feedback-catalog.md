# Triage Trees and Feedback Loop Catalog

Supporting reference for `skills/debugging/`. Operates under Andino Workflow governance.

---

## 1. Structured Failure Triage Trees

When unexpected behavior strikes, use these decision trees to classify the failure mode before executing probes or proposing changes.

### A. Test Failure Triage

```
Test fails after code change:
├── Did you intentionally modify the code the test covers?
│   ├── YES → Did the contract change?
│   │   ├── Contract evolved → Update test assertions to match agreed contract
│   │   └── Contract unchanged → Implementation introduced a regression → Fix code
│   └── NO → Side-effect or shared state leak
│       ├── Check global singletons, shared caches, in-memory state
│       ├── Check module import side-effects
│       └── Run test in absolute isolation (testPathPattern + runInBand)
└── Test was already failing / flaky before code change?
    ├── Timing dependent → Check condition-based waiting vs arbitrary sleeps
    ├── Order dependent → Use test polluter isolation to identify preceding test
    └── Environment dependent → Check node/python versions, env vars, timezones
```

### B. Build & Compilation Failure Triage

```
Build / Compilation breaks:
├── Type / Syntax Error:
│   ├── Read exact error line and column; do NOT guess
│   ├── Inspect type definitions and exported signatures at the boundary
│   └── Check for subtle breaking changes in updated dependencies
├── Import / Resolution Error:
│   ├── Verify physical file existence and exact case-sensitivity (Windows vs Linux)
│   ├── Check tsconfig/pyproject path aliases, exports map in package.json
│   └── Check circular dependency chains causing undefined exports
├── Tooling / Config Error:
│   ├── Validate schema/syntax of config files (.eslintrc, tsconfig, vite.config)
│   └── Compare with working configuration or lockfile diff
└── Environment / Native Dependency Error:
    ├── Verify runtime engine versions (Node >= 20, Python >= 3.10)
    └── Check native build tools (gcc, visual studio build tools, python-devel)
```

### C. Runtime Error Triage

```
Runtime error observed:
├── Null / Undefined Pointer / TypeError:
│   ├── Identify exact expression: what specifically evaluated to null/undefined?
│   ├── Trace data flow backward: where should this value have been populated?
│   └── Determine if failure is a missing invariant check or corrupted upstream state
├── Network / Boundary / CORS Error:
│   ├── Inspect HTTP status code, request URL, payload, and response headers
│   ├── Check server CORS configuration, preflight OPTIONS, and auth tokens
│   └── Verify DNS, port bindings, and proxy routing rules
├── State / Lifecycle Error:
│   ├── Check component mount/unmount races or dangling async promises
│   └── Check unhandled promise rejections or uncaught event emitter exceptions
└── Silent / Wrong Output (No explicit error thrown):
    ├── Establish expected vs actual output diff
    └── Trace backward to find the exact branch point where execution diverged
```

---

## 2. The 10-Tier Feedback Loop Catalog

A tight, red-capable feedback loop is the foundation of debugging. Spend disproportionate effort constructing one before formulating hypotheses. The loop must be **deterministic**, **fast (<5 seconds)**, and **agent-runnable**.

| Tier | Feedback Loop Mechanism | Best Used For | Execution Speed |
| :--- | :--- | :--- | :--- |
| **Tier 1** | **Focused Unit / Integration Test** | Function, class, or module-level contract violations. | < 1 second |
| **Tier 2** | **HTTP / Curl Replay Script** | API endpoints, microservices, backend regressions. | 1 – 3 seconds |
| **Tier 3** | **CLI Invocation with Snapshot Diff** | CLI tools, compilers, formatters, batch scripts. | < 2 seconds |
| **Tier 4** | **Headless Browser Script** (Playwright/Puppeteer) | UI rendering, client state, DOM interaction, network waterfalls. | 3 – 8 seconds |
| **Tier 5** | **Replay Captured Trace** | Complex production payloads, webhook events, message queue jobs. | < 1 second |
| **Tier 6** | **Throwaway Harness** | Deep internal subsystem where spinning full app is too slow. | < 1 second |
| **Tier 7** | **Property / Fuzzing Loop** | Edge-case inputs, off-by-one errors, parser crashes. | 2 – 5 seconds |
| **Tier 8** | **Automated Bisection Harness** (`git bisect run`) | Regressions between two known commits. | Automated |
| **Tier 9** | **Differential Loop** (Old vs New / Oracle) | Comparing output of refactored module vs known-good legacy version. | < 2 seconds |
| **Tier 10** | **Human-In-The-Loop (HITL) Script** | Interactive auth, hardware devices, visual desktop canvas. | Interactive |

---

### Tier Implementation Patterns

#### Tier 1: Focused Test Seam
Run only the specific failing scenario, bypassing full suites:
```bash
# Node / Vitest / Jest
npx vitest run tests/auth/token.test.ts -t "rejects expired refresh token"

# Python / Pytest
pytest tests/test_billing.py -k "test_multi_tenant_isolation" -v
```

#### Tier 2: Curl / HTTP Replay Script
```bash
curl -s -X POST http://localhost:3000/api/v1/checkout \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <REDACTED>" \
  -d '{"tenant_id": "tenant-b", "cart_id": "cart-123"}' | jq .
```

#### Tier 3: CLI Snapshot Diff
```bash
./bin/compiler --input fixtures/invalid-syntax.src --format json | diff -u fixtures/expected-error.json -
```

#### Tier 4: Headless Browser Driver
```typescript
import { test, expect } from '@playwright/test';

test('reproduces modal freeze on double-click', async ({ page }) => {
  await page.goto('http://localhost:3000/settings');
  const button = page.getByRole('button', { name: 'Save' });
  await button.dblclick();
  await expect(page.locator('.toast-success')).toBeVisible({ timeout: 2000 });
});
```

#### Tier 5: Replay Captured Trace
Save real JSON payload to disk and feed directly into handler without network latency:
```typescript
import { handler } from '../src/webhook-receiver';
import payload from './fixtures/failing-stripe-event.json';

const response = await handler(payload);
assert.strictEqual(response.statusCode, 200);
```

#### Tier 6: Throwaway In-Memory Harness
```python
# test_harness.py
from myapp.storage import MemoryStore
from myapp.service import TenantService

store = MemoryStore()
service = TenantService(store)
# Direct function exercise in 50ms:
result = service.process_record("tenant_1", {"key": "val"})
assert result.status == "OK", f"Expected OK, got {result.status}"
```

#### Tier 7: Property / Fuzzing Loop
```python
import random, string

for seed in range(500):
    random.seed(seed)
    payload = ''.join(random.choices(string.printable, k=random.randint(1, 100)))
    try:
        parse_tokens(payload)
    except Exception as e:
        print(f"[REPRO SEED] {seed} crashed with payload: {repr(payload)}")
        raise
```

#### Tier 8: Automated Bisection Loop
```bash
# Automate bisection with a fast exit-code check
git bisect start
git bisect bad HEAD
git bisect good v1.4.0
git bisect run pytest tests/unit/test_regression.py -k "test_specific_bug"
```

#### Tier 9: Differential Execution
```python
def check_differential(input_data):
    legacy_out = legacy_calculate(input_data)
    optimized_out = new_calculate(input_data)
    assert legacy_out == optimized_out, f"Diff detected: {legacy_out} != {optimized_out}"
```

---

## 3. Repro-Rate Raising for Flaky Bugs

When a bug reproduces only intermittently (e.g., 5% of runs), debugging is nearly impossible. **Do not begin guessing fixes.** First raise the reproduction rate to near 100%:

```
Flaky Repro Rate Escalation:
1. Loop Trigger 100x:
   Run the test inside an automated loop: for i in {1..100}; do command || break; done
2. Concurrency / Collision Stress:
   Spawn parallel workers to hammer the code path and saturate thread pools.
3. Artificial Timing Widening:
   Inject temporary micro-delays (e.g., 5ms sleep between read and write)
   to artificially widen the race condition window.
4. Resource Constriction:
   Run under CPU throttling or limited memory to amplify race/starvation conditions.
5. Seed Pinning:
   If PRNG is involved, capture and pin the failing seed.
```

---

## 4. Cross-Platform Human-In-The-Loop (HITL) Drivers

When a human must perform an interaction (e.g., 2FA, physical hardware tap, external SSO login), drive them with an automated script so the feedback loop remains structured and unattended data is captured.

### A. POSIX Bash Template (`hitl-loop.sh`)

```bash
#!/usr/bin/env bash
# HITL Reproduction Driver (Bash POSIX)
set -euo pipefail

step() {
  printf '\n>>> ACTION REQUIRED:\n    %s\n' "$1"
  read -r -p "    [Press Enter when done] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> QUESTION:\n    %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

# --- SCRIPT DEFINITION ---
step "Navigate to http://localhost:3000/billing and sign in with test credentials."
capture OBSERVED_ERROR "Did the invoice table show an error banner? (yes/no)"
capture HTTP_STATUS "Enter the status code of the failing /api/invoices request:"

printf '\n--- CAPTURED STATE ---\n'
printf 'OBSERVED_ERROR=%s\n' "$OBSERVED_ERROR"
printf 'HTTP_STATUS=%s\n' "$HTTP_STATUS"
```

### B. Cross-Platform Python Template (`hitl_loop.py`)

```python
#!/usr/bin/env python3
"""Cross-platform Human-in-the-Loop driver for Windows, macOS, and Linux."""
import sys

def step(instruction: str) -> None:
    print(f"\n>>> ACTION REQUIRED:\n    {instruction}")
    input("    [Press Enter when done] ")

def capture(question: str) -> str:
    print(f"\n>>> QUESTION:\n    {question}")
    return input("    > ").strip()

def main() -> None:
    step("Navigate to http://localhost:3000/billing and sign in with test credentials.")
    observed = capture("Did the invoice table show an error banner? (yes/no)")
    status = capture("Enter the HTTP status code of the failing request (or 'none'):")
    
    print("\n--- CAPTURED STATE ---")
    print(f"OBSERVED_ERROR={observed}")
    print(f"HTTP_STATUS={status}")

if __name__ == "__main__":
    main()
```
