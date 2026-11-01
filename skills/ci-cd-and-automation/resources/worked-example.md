# Worked Example: CI/CD Quality Automation & Remediation

This resource documents a complete, realistic operational walkthrough of diagnosing, fixing, and verifying a CI/CD pipeline failure using Andino Workflow quality automation discipline.

---

## 1. Scenario: Database Column Drift in Service Integration

### Context
A developer opened a pull request refactoring the user authentication module. The local unit tests passed because they relied on mocked database repositories. However, in the continuous integration pipeline, the **Integration Tests** job failed against the real PostgreSQL service container.

---

## 2. Step-by-Step Execution Walkthrough

### Step 1: CI Failure Notification & Log Distillation
The CI pipeline failed on job `integration`. Rather than ingesting the entire 1,400-line GitHub Actions log, the agent distilled the relevant error block:

```text
[FAIL] test/integration/auth-repository.test.ts
  ● AuthRepository › should persist and retrieve new user session
    QueryFailedError: column "user_name" of relation "users" does not exist
      at PostgresQueryRunner.query (src/driver/postgres/PostgresQueryRunner.ts:241:19)
      at UserRepository.createSession (src/repositories/UserRepository.ts:58:12)
      at Object.<anonymous> (test/integration/auth-repository.test.ts:44:28)
```

### Step 2: Root-Cause Investigation & Seam Analysis
The agent analyzed the dependency graph and recent git history:
1. Migration `004_rename_username.sql` renamed column `users.user_name` to `users.username`.
2. Unit test mocks were updated to return `{ username: "andino" }`.
3. However, `UserRepository.ts:58` still referenced the legacy column name in its raw SQL query builder:
   ```typescript
   // Bug in src/repositories/UserRepository.ts:58
   .select(['id', 'user_name', 'email'])
   ```
4. Because unit tests mocked the DB response, the query was never sent to a Postgres parser. The service container integration test caught the discrepancy.

### Step 3: Targeted Remediation
The agent applied the minimal, single-seam fix in `src/repositories/UserRepository.ts`:

```typescript
// Fixed: aligned query column with migration schema
.select(['id', 'username', 'email'])
```

### Step 4: Deterministic Local Verification
Before pushing, the agent executed the exact local verification sequence:
1. Re-ran integration test locally against the test database:
   ```sh
   DATABASE_URL="postgresql://ci_user:ci_password@localhost:5432/testdb" npm run test:integration
   ```
   *Result: 14 passed, 0 failed.*
2. Re-ran full quality gate suite locally:
   ```sh
   npm run lint && npx tsc --noEmit && npm test && npm run build
   ```
   *Result: All gates passed exit code 0.*
3. Pushed the atomic fix commit to the branch. Remote CI re-ran and turned green.

---

## 3. Operational Example (Offline Deterministic Python Runner)

The Andino test harness validates CI dependency graph evaluation and blocker propagation using this standard-library Python runner. It verifies that when an ancestor gate fails (e.g., under `ANDINO_NEGATIVE=1`), all dependent downstream stages are strictly blocked from execution, preventing unsafe advancement.

```python andino-operational-example
import json, os

def evaluate(jobs):
    """
    Evaluates pipeline stages against a directed acyclic graph (DAG).
    If any dependency of a job is not 'pass', the job is marked 'blocked'.
    Otherwise, if exit_code is 0, it passes; else it fails.
    """
    state = {}
    for name, deps, exit_code in jobs:
        if any(state.get(d) != "pass" for d in deps):
            state[name] = "blocked"
        else:
            state[name] = "pass" if exit_code == 0 else "fail"
    return state

def probe():
    # When ANDINO_NEGATIVE is set, lint fails, triggering cascading blocks.
    lint_exit = 1 if os.getenv("ANDINO_NEGATIVE") else 0
    jobs = [
        ("lint", [], lint_exit),
        ("unit", ["lint"], 0),
        ("build", ["unit"], 0),
        ("publish", ["build"], 0)
    ]
    result = evaluate(jobs)
    all_passed = all(v == "pass" for v in result.values())
    return {
        "stages": result,
        "publish_ready": all_passed,
        "deployed": False
    }

if __name__ == "__main__":
    print(json.dumps(probe(), sort_keys=True))
```

### Expected Output (Default / Success):
```json
{"deployed": false, "publish_ready": true, "stages": {"build": "pass", "lint": "pass", "publish": "pass", "unit": "pass"}}
```

### Expected Output (Adversarial / Negative: `ANDINO_NEGATIVE=1`):
```json
{"deployed": false, "publish_ready": false, "stages": {"build": "blocked", "lint": "fail", "publish": "blocked", "unit": "blocked"}}
```
