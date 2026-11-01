# Code Review Worked Example and Deterministic Verifier

This document provides a complete end-to-end walkthrough of an elevated two-axis code review, illustrating the exact reporting schema, pull request comment conventions, bidirectional feedback response, and an embedded standard-library Python verification suite.

---

## 1. Realistic Scenario: Multi-File Subscription Checkout

### Context
A developer implements an automated billing and refund workflow in a financial microservice. The PR changes two files and introduces an untracked helper:
- `services/billing.py`: Handles subscription billing and prorated refunds.
- `services/database.py`: Executes queries against the ledger.
- `services/audit_logger.py` *(untracked file)*: Logs transaction metadata.

### The Problematic Diff
In `services/billing.py`:
```python
def process_refund(user_balance: float, refund_amount: float) -> float:
    # BUG 1 (Spec Failure): Spec requires "refund_amount must be strictly positive and <= user_balance"
    # The implementation uses >= which allows refunding when refund_amount exceeds balance!
    if refund_amount >= user_balance:
        return user_balance
    return user_balance - refund_amount

def execute_dynamic_calculation(formula: str, context: dict):
    # BUG 2 (Standards/Security Failure): Prohibited dynamic eval of untrusted input
    return eval(formula, {}, context)
```

In `services/database.py`:
```python
def fetch_transaction_history(account_id: str, filter_type: str):
    # BUG 3 (Standards/Security Failure): SQL injection via string concatenation
    query = f"SELECT * FROM transactions WHERE account_id = '{account_id}' AND type = '{filter_type}'"
    return db.execute_raw(query)
```

---

## 2. Reviewer Output: The 2-Axis Report

```markdown
# Code Review: PR #104 — Subscription Refund and Calculation Engine

**Scope:** `git diff a81f20b..9e24bc1` + untracked `services/audit_logger.py`  
**Verdict:** CHANGES REQUESTED (2 Blockers identified)

### Declined to Judge
- `services/audit_logger.py`: Untracked helper file contains stubbed telemetry endpoints. Deferred to subsequent observability task as it does not affect refund financial invariants.

---

## Axis 1: Spec Track (Requirements & Functional Invariants)

### [REQUIRED] `services/billing.py:4` — Inverted Refund Boundary Guard
- **Requirement:** Task Spec §2.1: *"Refund amounts must be strictly greater than zero and cannot exceed user balance."*
- **Defect:** `if refund_amount >= user_balance: return user_balance` permits refunding amounts larger than the user balance without raising an error, returning the original balance unmutated.
- **Triggering Input:** `process_refund(100.0, 150.0)` returns `100.0` instead of raising `ValueError("Refund exceeds balance")`.
- **Named Structural Remedy:** Replace inverted boundary check with explicit contract assertion:
  ```python
  if refund_amount <= 0 or refund_amount > user_balance:
      raise ValueError(f"Invalid refund amount: {refund_amount} for balance: {user_balance}")
  ```

---

## Axis 2: Standards Track (Security, Architecture, & Smells)

### [CRITICAL] `services/billing.py:8` — Arbitrary Code Execution via `eval`
- **Standard:** Project Security Invariant §1.4 & OWASP Top 10 A03 (Injection).
- **Defect:** `eval(formula, {}, context)` executes unvalidated string formulas in Python runtime. Any caller passing attacker-controlled formula input gains Remote Code Execution.
- **Named Structural Remedy:** Replace Dynamic Execution with Typed AST Parser or fixed arithmetic dispatcher:
  ```python
  # Replace eval with safe math dispatcher
  OPERATIONS = {
      'pro_rate': lambda bal, days: bal * (days / 30.0),
      'flat_deduct': lambda bal, amt: bal - amt,
  }
  ```

### [CRITICAL] `services/database.py:3` — SQL Injection in Transaction Filter
- **Standard:** Security Checklist §1.4 (Parameterized Queries).
- **Defect:** String formatting `f"SELECT ... '{account_id}' ..."` allows SQL syntax escaping.
- **Named Structural Remedy:** Use parameterized query bindings:
  ```python
  query = "SELECT * FROM transactions WHERE account_id = %s AND type = %s"
  return db.execute_parameterized(query, (account_id, filter_type))
  ```

### [SUGGESTION] `services/billing.py:1` — Primitive Obsession on Currency
- **Standard:** Martin Fowler Smells Catalog — *Primitive Obsession*.
- **Defect:** Floating-point `float` used for currency amounts introduces IEEE 754 rounding errors.
- **Named Structural Remedy:** Introduce Parameter Object / Value Type (`Decimal` or integer cents).
```

---

## 3. Author Reception & Response

```markdown
Acknowledging review findings:

1. [REQUIRED] `services/billing.py:4`: Verified. Added boundary test `test_refund_exceeding_balance_raises` in `tests/test_billing.py` and implemented strict validation guard.
2. [CRITICAL] `services/billing.py:8`: Verified. Removed `eval()`; replaced with safe arithmetic lookup table.
3. [CRITICAL] `services/database.py:3`: Verified. Migrated to parameterized bindings `db.execute_parameterized()`.
4. [SUGGESTION] `services/billing.py:1`: Agree with value-type improvement. Creating tracked issue #105 to migrate entire ledger module to `Decimal` in dedicated refactor PR to preserve atomic PR sizing.
```

---

## 4. Offline Deterministic Verification Suite

The Python script below verifies that:
1. The Spec and Standards axes operate independently (neither dilutes the other).
2. The severity prefixes are strictly parsed and enforce blocker gating.
3. Under negative configuration (`ANDINO_NEGATIVE=1`), malformed reviews, cyclical deadlocks, or missing remedies fail deterministically.

```python
#!/usr/bin/env python3
"""
Zero-dependency deterministic verification script for Andino Code Review.
Run directly via: python -I run_verification.py
"""

import sys
import os
import json
import re

SAMPLE_REVIEW_PAYLOAD = {
    "scope": {
        "base_sha": "a81f20b",
        "head_sha": "9e24bc1",
        "untracked_files": ["services/audit_logger.py"]
    },
    "declined_to_judge": [
        "services/audit_logger.py: Telemetry stub outside financial scope"
    ],
    "findings": [
        {
            "axis": "spec",
            "severity": "[REQUIRED]",
            "file": "services/billing.py",
            "line": 4,
            "rule": "Task Spec §2.1",
            "consequence": "Refund amounts exceeding balance fail silently",
            "remedy": "Replace inverted boundary check with explicit guard"
        },
        {
            "axis": "standards",
            "severity": "[CRITICAL]",
            "file": "services/billing.py",
            "line": 8,
            "rule": "OWASP A03 / Security Invariant §1.4",
            "consequence": "Arbitrary code execution via eval",
            "remedy": "Replace eval with safe math dispatcher"
        },
        {
            "axis": "standards",
            "severity": "[SUGGESTION]",
            "file": "services/billing.py",
            "line": 1,
            "rule": "Fowler Smells: Primitive Obsession",
            "consequence": "Float rounding drift",
            "remedy": "Introduce Decimal value type"
        }
    ]
}

VALID_SEVERITIES = {"[CRITICAL]", "[REQUIRED]", "[SUGGESTION]", "[NIT]", "[FYI]"}
BLOCKING_SEVERITIES = {"[CRITICAL]", "[REQUIRED]"}

def evaluate_review(payload: dict) -> dict:
    spec_blockers = []
    standards_blockers = []
    suggestions = []

    # Assert scope pinning
    assert payload.get("scope", {}).get("base_sha"), "Missing base_sha"
    assert payload.get("scope", {}).get("head_sha"), "Missing head_sha"

    for finding in payload.get("findings", []):
        sev = finding.get("severity")
        assert sev in VALID_SEVERITIES, f"Invalid severity prefix: {sev}"
        assert finding.get("remedy"), f"Missing structural remedy for {finding.get('file')}:{finding.get('line')}"
        assert finding.get("line", 0) > 0, "Line number must be positive integer"

        axis = finding.get("axis")
        if sev in BLOCKING_SEVERITIES:
            if axis == "spec":
                spec_blockers.append(finding)
            elif axis == "standards":
                standards_blockers.append(finding)
        else:
            suggestions.append(finding)

    # Calculate independent verdicts
    spec_verdict = "FAIL" if spec_blockers else "PASS"
    standards_verdict = "FAIL" if standards_blockers else "PASS"
    overall_verdict = "CHANGES_REQUESTED" if (spec_blockers or standards_blockers) else "APPROVED"

    return {
        "spec_verdict": spec_verdict,
        "standards_verdict": standards_verdict,
        "overall_verdict": overall_verdict,
        "spec_blockers_count": len(spec_blockers),
        "standards_blockers_count": len(standards_blockers),
        "suggestions_count": len(suggestions)
    }

def run_tests():
    is_negative_mode = os.environ.get("ANDINO_NEGATIVE") == "1"

    if is_negative_mode:
        print("[ANDINO_NEGATIVE=1] Running negative tests: Expecting deterministic detection of review violations...")
        # Test 1: Missing structural remedy
        bad_payload = json.loads(json.dumps(SAMPLE_REVIEW_PAYLOAD))
        bad_payload["findings"][0]["remedy"] = ""
        try:
            evaluate_review(bad_payload)
            print("ERROR: Failed to catch missing structural remedy!")
            sys.exit(1)
        except AssertionError as e:
            print(f"PASS: Caught missing remedy correctly ({e})")

        # Test 2: Invalid severity prefix
        bad_payload2 = json.loads(json.dumps(SAMPLE_REVIEW_PAYLOAD))
        bad_payload2["findings"][0]["severity"] = "MAJOR"
        try:
            evaluate_review(bad_payload2)
            print("ERROR: Failed to catch invalid severity prefix!")
            sys.exit(1)
        except AssertionError as e:
            print(f"PASS: Caught invalid severity prefix correctly ({e})")

        print("All negative assertions verified successfully.")
        sys.exit(0)

    # Positive Mode
    print("[ANDINO] Running deterministic code-review contract verification...")
    result = evaluate_review(SAMPLE_REVIEW_PAYLOAD)
    
    assert result["spec_verdict"] == "FAIL", "Spec axis must fail on spec blocker"
    assert result["standards_verdict"] == "FAIL", "Standards axis must fail on security critical"
    assert result["overall_verdict"] == "CHANGES_REQUESTED"
    assert result["spec_blockers_count"] == 1
    assert result["standards_blockers_count"] == 1
    assert result["suggestions_count"] == 1

    # Verify Track Independence: Fix spec blocker only
    fixed_spec = json.loads(json.dumps(SAMPLE_REVIEW_PAYLOAD))
    fixed_spec["findings"] = [f for f in fixed_spec["findings"] if f["axis"] != "spec"]
    res_fixed_spec = evaluate_review(fixed_spec)
    assert res_fixed_spec["spec_verdict"] == "PASS", "Spec axis must pass when spec blockers resolved"
    assert res_fixed_spec["standards_verdict"] == "FAIL", "Standards axis must remain FAIL despite Spec PASS"

    # Verify Track Independence: Fix standards blocker only
    fixed_standards = json.loads(json.dumps(SAMPLE_REVIEW_PAYLOAD))
    fixed_standards["findings"] = [f for f in fixed_standards["findings"] if f["severity"] != "[CRITICAL]"]
    res_fixed_std = evaluate_review(fixed_standards)
    assert res_fixed_std["standards_verdict"] == "PASS", "Standards axis must pass when critical blockers resolved"
    assert res_fixed_std["spec_verdict"] == "FAIL", "Spec axis must remain FAIL despite Standards PASS"

    print("PASS: Two-axis isolation verified.")
    print("PASS: Severity gating and structural remedies verified.")
    print("All deterministic assertions passed successfully.")

if __name__ == "__main__":
    run_tests()
```
