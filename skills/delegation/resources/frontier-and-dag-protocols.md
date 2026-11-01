# Active Frontier and Task DAG Protocols

Internal Andino resource for `andino-delegation`. Operates under Andino Workflow governance.

## 1. Task DAG Mathematical Modeling

A multi-task implementation plan forms a Directed Acyclic Graph (DAG) $G = (V, E)$:
- $V = \{T_1, T_2, \dots, T_n\}$: set of discrete implementation tasks.
- $E \subset V \times V$: directed dependency edges where $(T_u, T_v) \in E$ indicates task $T_v$ depends on task $T_u$ ($T_u \prec T_v$).
- Every task $T$ owns a verified disjoint write set $W(T) = \{p_1, p_2, \dots, p_k\}$ of relative file paths.

### Dependency Graph Specification

```yaml
tasks:
  - id: auth-tokens
    deps: []
    owned_paths:
      - src/auth/token_signer.py
      - tests/test_token_signer.py
  - id: auth-store
    deps: []
    owned_paths:
      - src/auth/refresh_store.py
      - tests/test_refresh_store.py
  - id: auth-middleware
    deps:
      - auth-tokens
      - auth-store
    owned_paths:
      - src/auth/middleware.py
      - tests/test_middleware.py
```

## 2. Active Frontier Calculation

The **Active Frontier** $\mathcal{F}_t \subseteq V$ at step $t$ is the set of uncompleted tasks whose prerequisites are completely satisfied:

$$\mathcal{F}_t = \{ T \in V \setminus C_t \mid \forall D \in \text{deps}(T), D \in C_t \}$$

Where $C_t$ is the set of verified completed tasks at step $t$.

### Frontier Resolution Algorithm (Python stdlib)

```python
def compute_active_frontier(tasks: list[dict], completed_ids: set[str]) -> list[dict]:
    """
    Returns uncompleted tasks whose dependencies are strictly satisfied in completed_ids.
    Sorts by dependency depth descending (critical path first).
    """
    frontier = []
    for t in tasks:
        t_id = t["id"]
        if t_id in completed_ids:
            continue
        deps = set(t.get("deps", []))
        if deps.issubset(completed_ids):
            frontier.append(t)
    return frontier
```

## 3. Disjoint Write Ownership & Collision Prevention

Concurrent subagent execution is **strictly forbidden** if any candidate tasks share write targets or exhibit ancestor path collisions.

### Overlap Rules

1. **Exact File Collision**: If $W(T_A) \cap W(T_B) \neq \emptyset$, tasks $T_A$ and $T_B$ must execute sequentially.
2. **Ancestor Directory Collision**: If path $p_A \in W(T_A)$ is a parent directory or prefix of path $p_B \in W(T_B)$ (e.g., `src/auth` vs `src/auth/signer.py`), tasks $T_A$ and $T_B$ must execute sequentially.
3. **Shared Dependency File Lock**: Modifications to shared root configuration files (`package.json`, `Cargo.toml`, `pyproject.toml`, database migration ledgers) cannot be parallelized.

### Collision Detection Function

```python
import os

def normalize_path(p: str) -> str:
    return os.path.normpath(p).replace("\\", "/").strip("/")

def has_write_collision(paths_a: list[str], paths_b: list[str]) -> bool:
    norm_a = [normalize_path(p) for p in paths_a]
    norm_b = [normalize_path(p) for p in paths_b]
    for pa in norm_a:
        for pb in norm_b:
            if pa == pb:
                return True
            # Ancestor check
            if pa.startswith(pb + "/") or pb.startswith(pa + "/"):
                return True
    return False
```

## 4. Concurrency Bounds & Wave Scheduling

Under Andino Workflow resource guard 10:
- **Maximum Concurrent Direct Children**: Exactly **3** active direct workers.
- **No Nested Agent Spawning**: A subagent must never spawn another subagent.
- **Wave Dispatch**: If active frontier $|\mathcal{F}_t| > 3$, partition into waves:
  - Wave 1: First 3 collision-free tasks with highest downstream dependency count.
  - Wave 2+: Dispatched sequentially as slots in the concurrency pool free up.

## 5. Tri-Modal Execution Decision Matrix

| Strategy | When to Select | Execution Mechanics |
| :--- | :--- | :--- |
| **Inline** | Small edits (<2 files, <50 LOC), tightly coupled changes, exploratory debugging with shared unknown root cause, or host lacks worker capabilities. | Parent agent executes directly; retains full verification and test evidence. |
| **Parallel Dispatch** | 2+ completely independent problem domains, zero shared state, separate test files, and no common root cause. | Multi-dispatch in a single turn; parent collects summaries, checks for conflicts, and integrates. |
| **Subagent-Driven** | Multi-task implementation plan with clear specifications, where isolated context per task and two-track review ensure quality. | Fresh subagent per task; task brief via file pointer; two-track review; fix loop escalation; parent ledger tracking. |

## 6. Anti-Patterns & Failure Modes

1. **Failure Count Parallelism**: Dispatching 1 subagent per failing test when all failures stem from a single shared schema error or broken import.
2. **Shared-Manifest Race Conditions**: Spawning two subagents that each run `npm install <pkg>` or mutate `pyproject.toml` simultaneously.
3. **Speculative Dispatch**: Dispatching task $T_B$ while prerequisite $T_A$ is still running or has only passed implementer self-review without parent gate verification.
4. **Chat History Replay**: Pasting the entire prior conversation or accumulated task history into subsequent worker prompts.
