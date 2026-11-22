# Flaky Tests and Concurrency Debugging

Supporting reference for `skills/debugging/`. Operates under Andino Workflow governance.

---

## 1. The 4 Categories of Intermittent Bugs

When a bug cannot be reproduced on demand, do not guess or ignore it as "just a flake". Classify it into one of four deterministic categories:

```
Cannot reproduce on demand:
├── 1. Timing-Dependent (Race Conditions / Async Timing)
│   ├── Missing async await or premature promise resolution
│   ├── Event loop starvation or background thread scheduling
│   └── Network latency / DB transaction commit race
├── 2. Environment-Dependent (Platform & Configuration Drift)
│   ├── OS-specific behavior (Windows CRLF vs POSIX LF, case-insensitive NTFS)
│   ├── Locale, timezone (UTC vs local time parsing), or currency formatting
│   └── Node/Python runtime minor versions, package manager lockfile drift
├── 3. State-Dependent (Pollution & Ordering)
│   ├── Shared memory, static variables, unreset global singletons
│   ├── Test pollution: Test A mutates database/cache, causing Test B to fail
│   └── Leaked mocks, unclosed file descriptors, lingering timers
└── 4. Pseudo-Random / Data-Dependent
    ├── Unseeded random generators (Math.random(), random.choice())
    ├── Dictionary / Hash map iteration order differences across runtimes
    └── Specific unicode characters, empty strings, boundary integers
```

---

## 2. Condition-Based Waiting vs. Arbitrary Sleep

The single most common AI anti-pattern in async or distributed debugging is **increasing arbitrary sleeps** (`await sleep(5000)` or `time.sleep(10)`).

### Why Arbitrary Sleep Fails
1. **Flaky on Slower Machines**: What passes with 2000ms locally fails in busy CI runner environments.
2. **Kills Test Suite Velocity**: Hundreds of tests sleeping 5 seconds destroy feedback loops.
3. **Masks Concurrency Defects**: Lengthening sleeps hides real race conditions without solving them.

### Condition-Based Waiting Pattern

Always poll a **concrete predicate** with a deterministic interval and bounded timeout.

#### TypeScript / JavaScript Pattern
```typescript
/**
 * Polls for a condition to become true within a maximum timeout.
 */
export async function waitForCondition(
  predicate: () => boolean | Promise<boolean>,
  options: { timeoutMs?: number; intervalMs?: number; description?: string } = {}
): Promise<void> {
  const { timeoutMs = 5000, intervalMs = 50, description = 'condition' } = options;
  const start = Date.now();

  while (Date.now() - start < timeoutMs) {
    if (await predicate()) {
      return;
    }
    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }

  throw new Error(`Timeout after ${timeoutMs}ms waiting for: ${description}`);
}

// Usage in tests:
await waitForCondition(
  () => orderRepository.findStatus(orderId) === 'COMPLETED',
  { timeoutMs: 3000, description: 'order to reach COMPLETED status' }
);
```

#### Python 3.8+ Pattern
```python
import time
from typing import Callable, Any

def wait_for_condition(
    predicate: Callable[[], bool],
    timeout_sec: float = 5.0,
    interval_sec: float = 0.05,
    description: str = "condition"
) -> None:
    """Polls a condition until truthy or timeout expires."""
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(interval_sec)
    raise TimeoutError(f"Timeout after {timeout_sec}s waiting for: {description}")

# Usage:
wait_for_condition(
    lambda: payment_gateway.is_settled(tx_id),
    timeout_sec=3.0,
    description="payment settlement"
)
```

---

## 3. Test Polluter Isolation Engine

When a test passes when run in isolation (`npm test -- -t "test B"` or `pytest tests/test_b.py`), but fails when the full suite runs, **Test B is a victim of Test Pollution**. Another preceding test (Test A) mutated shared state and failed to clean up.

### Cross-Platform Python Test Polluter Finder (`find_polluter.py`)

This zero-dependency script runs suspects sequentially before the victim test to identify the exact polluter in $O(N)$ or $O(\log N)$ bisection time.

```python
#!/usr/bin/env python3
"""
Zero-dependency test polluter detector.
Identifies which test in a test list pollutes state and breaks a victim test.
"""
import subprocess
import sys
from pathlib import Path
from typing import List

def run_test_pair(polluter: str, victim: str, runner_cmd: List[str]) -> bool:
    """Runs polluter followed by victim. Returns True if victim passes, False if fails."""
    # Example runner_cmd: ['pytest', '-q'] or ['npx', 'vitest', 'run']
    cmd = runner_cmd + [polluter, victim]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc.returncode == 0

def find_polluter(candidates: List[str], victim: str, runner_cmd: List[str]) -> str:
    print(f"[*] Isolating polluter for victim: {victim}")
    print(f"[*] Testing {len(candidates)} suspect candidates...")
    
    for idx, candidate in enumerate(candidates, 1):
        if candidate == victim:
            continue
        sys.stdout.write(f"\r[{idx}/{len(candidates)}] Testing: {candidate[:50]}...")
        sys.stdout.flush()
        
        passed = run_test_pair(candidate, victim, runner_cmd)
        if not passed:
            print(f"\n[!] POLLUTER IDENTIFIED: {candidate}")
            print(f"    Running '{candidate}' followed by '{victim}' triggered failure!")
            return candidate
            
    print("\n[-] No single polluter identified. Failure may require multi-test combination.")
    return ""

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python find_polluter.py <victim_test> <test_file_1> [test_file_2 ...]")
        sys.exit(1)
        
    victim_target = sys.argv[1]
    candidate_list = sys.argv[2:]
    find_polluter(candidate_list, victim_target, ["pytest", "-q"])
```

---

## 4. Remediation of Shared State & Singleton Pollution

When state pollution is identified, apply one of three clean architectural remedies:

1. **Explicit Tear-Down Hooks**:
   Always reset database tables, clear caches, or wipe mock registries in `afterEach` / `tearDown`:
   ```typescript
   afterEach(async () => {
     await db.truncate();
     jest.clearAllMocks();
     cacheStore.flush();
   });
   ```
2. **Dependency Injection over Global Singletons**:
   Never export a mutable global instance (`export const db = new Database()`).
   Export a factory function (`export function createDatabase()`) and pass instances explicitly to constructors.
3. **Isolated Test Sandboxes**:
   Use unique database schemas, temporary directories, or process-level isolation per test worker:
   ```python
   @pytest.fixture
   def isolated_storage(tmp_path):
       store = FileStorage(root_dir=tmp_path)
       yield store
       store.dispose()
   ```
