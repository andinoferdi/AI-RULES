# Worked Example: Dependency-Aware Implementation Plan

This resource provides a concrete, end-to-end implementation plan demonstrating the gold standard format for AI agents executing under Andino Workflow. It includes an actionable reference plan, followed by concrete anti-patterns and their remediations.

Scenarios and code fixtures below are illustrative contracts; real project values must be derived from inspecting the target repository.

---

## Part 1: Production-Grade Reference Plan

Below is an example of an accepted, execution-ready plan for adding an audit logging pipeline to an existing API service.

```markdown
# Implementation Plan: Transaction Audit Logging Pipeline

> **Governance:** Operates under Andino Workflow. Steps use checkbox (`- [ ]`) syntax for deterministic execution tracking.
> **Target Path:** `docs/exec-plans/active/2026-10-30-audit-logging.md`

**Goal:** Record tamper-evident audit logs for financial balance mutations with zero loss during database failover.

**Architecture:** Transactional outbox pattern using PostgreSQL. Mutations and audit events commit in the same database transaction; an asynchronous worker forwards committed events to long-term storage.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2.0 (async), PostgreSQL 16, pytest-asyncio.

**Spec Reference:** `docs/specs/2026-10-30-audit-spec.md`

### Global Constraints
- Python 3.12+ type hints on all public interfaces (`from __future__ import annotations`).
- Zero schema migration downtime; new columns must be nullable or carry non-locking defaults.
- No new external infrastructure services (no standalone message brokers this phase).
- Maximum latency impact on the primary mutation endpoint: < 15ms at p95.

### Review Focus (Implicit Failure Modes)
1. **Database Restart during Commit:** Connection drops after mutation write but before audit record insert. Expected: Atomic rollback of both; sender receives 5xx and retries safely.
2. **Duplicate Client Request (Idempotency):** Client retries a timed-out mutation with the same `Idempotency-Key`. Expected: Single audit record created; duplicate request returns identical response without second entry.
3. **Malformed / Extreme Event Payload:** Payload contains oversized metadata (>64KB) or non-serializable Unicode surrogates. Expected: Schema validation rejects with 422 before transaction begins; no poisoned records in audit table.
4. **Outbox Worker Process Crash:** Worker dies while processing a batch of unexported events. Expected: Unacknowledged events remain unlocked and re-delivered upon worker restart without loss.
5. **Concurrent Balance Update:** Simultaneous mutations on the same ledger account under high load. Expected: Row-level locking on account balance; sequential audit trail with strictly monotonic timestamps.

---

### Task 1: Audit Log Outbox Model and Migration

**Files:**
- Create: `src/ledger/models/audit.py`
- Create: `migrations/versions/20261030_create_audit_log.py`
- Test: `tests/unit/test_audit_model.py`

**Interfaces:**
- Consumes: `src/ledger/models/base.py::Base`
- Produces: `AuditLog(id: UUID, account_id: UUID, event_type: str, delta_cents: int, idempotency_key: str, created_at: datetime)`

- [ ] **Step 1: Write failing model unit test**

```python
# tests/unit/test_audit_model.py
from datetime import datetime, timezone
import uuid
import pytest
from ledger.models.audit import AuditLog

def test_audit_log_instantiation():
    record = AuditLog(
        account_id=uuid.uuid4(),
        event_type="BALANCE_ADJUSTMENT",
        delta_cents=5000,
        idempotency_key="req_abc123"
    )
    assert record.id is not None
    assert record.created_at.tzinfo == timezone.utc
    assert record.exported_at is None
```

- [ ] **Step 2: Verify test fails**
Run: `pytest tests/unit/test_audit_model.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'ledger.models.audit'`

- [ ] **Step 3: Implement `AuditLog` SQLAlchemy model**
Define table `audit_logs` in `src/ledger/models/audit.py` with unique constraint on `(account_id, idempotency_key)` and index on `exported_at`.

- [ ] **Step 4: Verify test passes**
Run: `pytest tests/unit/test_audit_model.py -v`
Expected: PASS

- [ ] **Step 5: Generate migration script and verify migration cycle**
Run: `alembic upgrade head && alembic downgrade -1 && alembic upgrade head`
Expected: Schema migration and rollback execute cleanly.

- [ ] **Step 6: Commit task deliverable**
```bash
git add src/ledger/models/audit.py migrations/ tests/unit/test_audit_model.py
git commit -m "feat(ledger): add audit_log outbox table and model"
```

---

### Task 2: Atomic Audit Logger Service

**Files:**
- Create: `src/ledger/services/audit.py`
- Modify: `src/ledger/services/account.py:45-88`
- Test: `tests/integration/test_audit_service.py`

**Interfaces:**
- Consumes: `AuditLog` from Task 1, `AsyncSession` from `src/core/db.py`
- Produces: `record_audit_event(session: AsyncSession, account_id: UUID, delta_cents: int, idempotency_key: str) -> AuditLog`

- [ ] **Step 1: Write failing integration test for atomic recording**

```python
# tests/integration/test_audit_service.py
import pytest
from ledger.services.audit import record_audit_event
from ledger.models.audit import AuditLog

@pytest.mark.asyncio
async def test_audit_recorded_in_same_transaction(db_session, test_account):
    async with db_session.begin():
        entry = await record_audit_event(
            session=db_session,
            account_id=test_account.id,
            delta_cents=-2500,
            idempotency_key="tx_test_001"
        )
    saved = await db_session.get(AuditLog, entry.id)
    assert saved is not None
    assert saved.delta_cents == -2500
```

- [ ] **Step 2: Verify test fails**
Run: `pytest tests/integration/test_audit_service.py -v`
Expected: FAIL with `ImportError: cannot import name 'record_audit_event'`

- [ ] **Step 3: Implement `record_audit_event` and wire into `AccountService.mutate_balance`**
Implement the service in `src/ledger/services/audit.py` ensuring the event is attached to the existing `AsyncSession` without issuing a premature `session.commit()`.

- [ ] **Step 4: Verify integration test passes**
Run: `pytest tests/integration/test_audit_service.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Verify Review Focus Item 1 (Rollback on mutation error)**
Run: `pytest tests/integration/test_audit_service.py::test_mutation_failure_rolls_back_audit -v`
Expected: PASS (Verifies no orphan audit records exist if account balance write fails)

- [ ] **Step 6: Commit task deliverable**
```bash
git add src/ledger/services/audit.py src/ledger/services/account.py tests/integration/test_audit_service.py
git commit -m "feat(ledger): implement atomic audit event recording in balance mutation"
```

---

### Checkpoint 1: Storage and Transaction Verification
- [ ] Run full unit & integration suite: `pytest tests/unit/ tests/integration/ -v`
- [ ] Run project linter: `ruff check src/ledger/ tests/`
- [ ] Run static type check: `mypy src/ledger/`
- [ ] Verify database state: Audit records are created atomically when and only when mutation succeeds.

---

### Task 3: Audit Query API Endpoint

**Files:**
- Create: `src/ledger/api/audit.py`
- Modify: `src/ledger/api/router.py:12-28`
- Test: `tests/api/test_audit_routes.py`

**Interfaces:**
- Consumes: `src/ledger/models/audit.py::AuditLog`, `src/auth/dependencies.py::require_auditor_role`
- Produces: `GET /api/v1/accounts/{account_id}/audit-trail -> List[AuditLogResponse]`

- [ ] **Step 1: Write failing route authorization and retrieval test**

```python
# tests/api/test_audit_routes.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_audit_trail_requires_auditor_role(client: AsyncClient, test_account):
    response = await client.get(
        f"/api/v1/accounts/{test_account.id}/audit-trail",
        headers={"Authorization": "Bearer standard_user_token"}
    )
    assert response.status_code == 403
```

- [ ] **Step 2: Verify test fails**
Run: `pytest tests/api/test_audit_routes.py -v`
Expected: FAIL with 404 (route not found) or 401/403 assertion error.

- [ ] **Step 3: Implement endpoint and schema**
Register `GET /api/v1/accounts/{account_id}/audit-trail` in `src/ledger/api/audit.py` with pagination (`limit: int = 50`, `cursor: Optional[str] = None`).

- [ ] **Step 4: Verify test passes**
Run: `pytest tests/api/test_audit_routes.py -v`
Expected: PASS (all route tests pass)

- [ ] **Step 5: Commit task deliverable**
```bash
git add src/ledger/api/audit.py src/ledger/api/router.py tests/api/test_audit_routes.py
git commit -m "feat(api): expose paginated audit trail endpoint with role validation"
```

---

### Checkpoint 2: Feature Complete Integration Gate
- [ ] End-to-end integration test passes: `pytest tests/e2e/test_audit_pipeline.py -v`
- [ ] Linter & typecheck pass with zero warnings: `ruff check . && mypy src/`
- [ ] Benchmark check: Mutation endpoint latency verified under 15ms target.

---

**NEXT ACTION:** Execute Task 1 Step 1 in `tests/unit/test_audit_model.py`.
```

---

## Part 2: Anti-Patterns and Remediations

### Anti-Pattern 1: Horizontal Slicing (Layer-by-Layer)
- **Bad:**
  - Task 1: Create all database tables for the entire system.
  - Task 2: Write all repository classes and database queries.
  - Task 3: Build all service interfaces.
  - Task 4: Connect the UI and hope it works end-to-end.
- **Why it Fails:** Nothing is testable until the final step. Early errors in database schema cascade through all subsequent layers.
- **Remediation (Vertical Slicing):** Build complete, thin, end-to-end paths (Database + Service + Route + Test) for one user capability at a time. Each slice delivers independently verifiable value.

### Anti-Pattern 2: Over-Specification Pseudocode
- **Bad:** Writing 60 lines of speculative Python/TypeScript code in the plan document for every helper function.
- **Why it Fails:** The agent spends tokens writing the implementation twice. The first runtime error or compiler feedback invalidates the speculative code, causing cascading drift.
- **Remediation:** Specify **exact signatures** (`function_name(param: Type) -> ReturnType`), exact file paths, and pinned domain values. Let the implementer write the body guided by the failing test.

### Anti-Pattern 3: Vague Verification
- **Bad:** `Verification: Make sure it works and handles errors properly.`
- **Why it Fails:** The agent cannot execute or evaluate "make sure it works". It hallucinate completion and moves on without proof.
- **Remediation (Binary Oracle):**
  - Command: `pytest tests/integration/test_audit.py::test_duplicate_key -v`
  - Expected: `PASS (returns 409 Conflict with code 'DUPLICATE_KEY')`

### Anti-Pattern 4: The Monolithic XL Task
- **Bad:** `Task 1: Implement Authentication and Role-Based Access Control (touches 14 files).`
- **Why it Fails:** Exceeds agent context budget. Subagents lose focus, drop error handling, and make unverified assumptions.
- **Remediation:** Break down into XS/S/M slices:
  - Task 1: Password hashing and user credential model (S).
  - Task 2: JWT token generation and validation middleware (S).
  - Task 3: Route role guard dependency (S).
