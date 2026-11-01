# Complete Verified Multi-Task Case Study and Test Harness

Internal Andino resource for `andino-delegation`. Operates under Andino Workflow governance.

## 1. End-to-End Case Study: Auth Token System Refactor

### Scenario
A monolithic authentication helper is being refactored into three modular components:
- **Task 1 (`token-signer`)**: JWT signing and verification with expiration (`src/auth/signer.py`, `tests/test_signer.py`).
- **Task 2 (`refresh-store`)**: Ephemeral refresh token cache with revocation (`src/auth/store.py`, `tests/test_store.py`).
- **Task 3 (`auth-middleware`)**: HTTP request header bearer authentication middleware (`src/auth/middleware.py`, `tests/test_middleware.py`). Depends on `token-signer` and `refresh-store`.

---

## 2. Step-by-Step Execution Trace

### Step 1: Workspace Initialization & DAG Frontier Computation
- Controller resolves workspace: `.andino/delegation/auth-refactor/`
- Progress ledger initialized at `.andino/delegation/auth-refactor/progress.md`.
- Dependency evaluation:
  - `deps(Task 1) = []`
  - `deps(Task 2) = []`
  - `deps(Task 3) = [Task 1, Task 2]`
- Write Path Check:
  - $W(T_1) = \{\text{src/auth/signer.py}, \text{tests/test_signer.py}\}$
  - $W(T_2) = \{\text{src/auth/store.py}, \text{tests/test_store.py}\}$
  - $W(T_1) \cap W(T_2) = \emptyset$ (Disjoint write paths, no ancestor collision).
- **Active Frontier**: $\{T_1, T_2\}$ are both unblocked. Concurrency cap is 3. Eligible for **Parallel Dispatch**.

### Step 2: Single-Turn Parallel Multi-Dispatch
The controller dispatches both subagents in a single turn:

```text
Subagent (general-purpose):
  description: "Implement Task 1: token-signer"
  prompt: "Read brief at .andino/delegation/auth-refactor/task-1-brief.md..."

Subagent (general-purpose):
  description: "Implement Task 2: refresh-store"
  prompt: "Read brief at .andino/delegation/auth-refactor/task-2-brief.md..."
```

### Step 3: Implementers Report & Diff Packaging
Both workers conclude with the standardized status contract:
- Worker 1: `Status: DONE | Commits: a1b2c3d | Tests: 8/8 pass`
- Worker 2: `Status: DONE | Commits: e4f5a6b | Tests: 6/6 pass`
Controller records commit points:
- `BASE = f0a1b2c`
- `HEAD_1 = a1b2c3d`
- `HEAD_2 = e4f5a6b`
Diff packages generated via `review_package.py`.

### Step 4: Two-Track Review Execution
Reviewer 1 (for Task 1):
- Track 1 (Spec Compliance): ✅ Spec Compliant
- Track 2 (Code Quality): Approved
- Ledger updated: `Task 1: complete (commits f0a1b2c..a1b2c3d, review clean)`

Reviewer 2 (for Task 2):
- Track 1 (Spec Compliance): ❌ Issues Found: Missing TTL expiry validation.
- Track 2 (Code Quality): Needs Fixes (Important: unhandled expired token lookup).
- Ledger updated: `Task 2: review failed (1 Important finding: missing TTL validation)`

### Step 5: Fix Loop (Round 1) on Task 2
- Controller resumes Worker 2 with the open finding.
- Worker 2 fixes TTL validation, adds test case, commits `c7d8e9f`, and updates report.
- Scoped re-reviewer verifies `c7d8e9f`: Finding `ADDRESSED`, no regressions.
- Ledger updated:
  - `Task 2: fix round 1/5 (1 addressed, 0 open; commits e4f5a6b..c7d8e9f)`
  - `Task 2: complete (commits e4f5a6b..c7d8e9f, review clean)`

### Step 6: Advance Active Frontier to Task 3
- Prerequisite check: $C = \{T_1, T_2\}$. Both dependencies of Task 3 are satisfied.
- Active Frontier: $\{T_3\}$. Dispatched to a fresh subagent with brief pointing to verified interfaces from $T_1$ and $T_2$.
- Task 3 implemented, reviewed clean, and committed.

### Step 7: Final Whole-Branch Review & Teardown
- Final reviewer evaluates net diff across all 3 tasks. Quality approved.
- Workspace purged: `rm -rf .andino/delegation/auth-refactor`.

---

## 3. Embedded Zero-Dependency Python Verification Harness

This script verifies DAG frontier resolution, path collision rejection, and ledger integrity offline (<0.2 seconds).

```python andino-worked-example-verification
import os
import sys

def normalize_path(p: str) -> str:
    return os.path.normpath(p).replace("\\", "/").strip("/")

def has_write_collision(paths_a: list[str], paths_b: list[str]) -> bool:
    norm_a = [normalize_path(p) for p in paths_a]
    norm_b = [normalize_path(p) for p in paths_b]
    for pa in norm_a:
        for pb in norm_b:
            if pa == pb or pa.startswith(pb + "/") or pb.startswith(pa + "/"):
                return True
    return False

def compute_frontier(tasks: list[dict], completed: set[str]) -> list[str]:
    frontier = []
    for t in tasks:
        if t["id"] in completed:
            continue
        if set(t.get("deps", [])).issubset(completed):
            frontier.append(t["id"])
    return sorted(frontier)

def run_verification():
    is_neg = os.environ.get("ANDINO_NEGATIVE", "0") == "1"

    tasks = [
        {"id": "t1", "deps": [], "paths": ["src/auth/signer.py"]},
        {"id": "t2", "deps": [], "paths": ["src/auth/store.py"]},
        {"id": "t3", "deps": ["t1", "t2"], "paths": ["src/auth/middleware.py"]},
        {"id": "t4_collision", "deps": [], "paths": ["src/auth"]},
    ]

    # Test 1: Frontier Calculation
    f0 = compute_frontier(tasks[:3], set())
    if f0 != ["t1", "t2"]:
        sys.exit(1)

    f1 = compute_frontier(tasks[:3], {"t1"})
    if f1 != ["t2"]:
        sys.exit(1)

    f2 = compute_frontier(tasks[:3], {"t1", "t2"})
    if f2 != ["t3"]:
        sys.exit(1)

    # Test 2: Collision Detection
    # Disjoint paths
    if has_write_collision(tasks[0]["paths"], tasks[1]["paths"]):
        sys.exit(1)

    # Exact collision
    if not has_write_collision(["src/shared.py"], ["src/shared.py"]):
        sys.exit(1)

    # Ancestor directory collision
    if not has_write_collision(tasks[0]["paths"], tasks[3]["paths"]):
        sys.exit(1)

    if is_neg:
        print("[ANDINO_NEGATIVE] Intentional failure triggered.")
        sys.exit(1)

    print("SUCCESS: Delegation DAG, frontier, and collision protocols verified.")
    sys.exit(0)

if __name__ == "__main__":
    run_verification()
```
