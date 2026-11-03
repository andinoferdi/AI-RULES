# Worked example and verification

## Review input

The task requires refund status and the audit entry to change atomically.
Review only the committed refund change. An unrelated draft edit to
`auth.py` is present in the working tree. The existing test asserts that
both writes succeed when the audit insert succeeds.

The changed function in `refund.py` commits an update to the order on line 11
and inserts its audit record in a separate autocommit statement on line 12.

## Review output

**Scope.** Committed refund change against its parent. The task's atomicity
requirement is the Spec source.

**[REQUIRED] Spec · `refund.py:11` · Commit the refund and audit row together.**
If the audit insert fails after the order update, the order remains refunded
without an audit record. Both writes use autocommit, so the second failure
cannot roll back the first write. Run both statements in one transaction and
add a regression test that forces the audit insert to fail.

**Axis verdicts.** Spec FAIL. Standards FAIL on persistence correctness,
covered by the same finding. Overall CHANGES REQUESTED.

**Verification and limits.** Inspected the happy-path test. It does not
exercise audit failure. No repository test was run for this example review.

**Declined to Judge.** The uncommitted `auth.py` draft is outside the
requested committed scope.

## Verify the failure mechanism

Run the Python block with Python 3. It demonstrates the transaction failure
and checks that the remedy preserves the happy path. It exercises SQLite
behavior in this fixture.

```python
import sqlite3


def observe_refund(atomic, audit_available):
    with sqlite3.connect(":memory:", isolation_level=None) as db:
        db.executescript("""
            CREATE TABLE orders (refunded INTEGER NOT NULL);
            INSERT INTO orders VALUES (0);
            CREATE TABLE audit (order_id INTEGER NOT NULL);
        """)
        if not audit_available:
            db.execute("""
                CREATE TRIGGER fail_audit BEFORE INSERT ON audit
                BEGIN SELECT RAISE(ABORT, 'audit write failed'); END
            """)
        if atomic:
            db.execute("BEGIN")
        try:
            with db:
                db.execute("UPDATE orders SET refunded = 1")
                db.execute("INSERT INTO audit VALUES (1)")
        except sqlite3.IntegrityError as error:
            if audit_available or str(error) != "audit write failed":
                raise
        refunded = db.execute("SELECT refunded FROM orders").fetchone()[0]
        audit_count = db.execute("SELECT COUNT(*) FROM audit").fetchone()[0]
        return refunded, audit_count


assert observe_refund(atomic=False, audit_available=True) == (1, 1)
assert observe_refund(atomic=False, audit_available=False) == (1, 0)
assert observe_refund(atomic=True, audit_available=False) == (0, 0)
assert observe_refund(atomic=True, audit_available=True) == (1, 1)
print("PASS: audit failure reproduces the partial write and verifies rollback")
```

## Receive the finding

Reproduce the partial write against the repository's database adapter.
Confirm both statements can share a transaction. Apply the authorized fix
and verify that the regression test detects the old behavior and passes with
the fix. If the adapter already shares a transaction, cite its implementation
or a targeted test in one technical response.
