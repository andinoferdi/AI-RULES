# End-to-End Debugging Worked Example

Supporting reference for `skills/debugging/`. Operates under Andino Workflow governance.

---

## 1. Incident Scenario: Multi-Tenant Cache Leakage

### The Symptom
A multi-tenant SaaS application reports that Tenant B occasionally sees cached data belonging to Tenant A when both tenants query for the same resource identifier (`key="config-7"`). The bug does not reproduce in standard single-tenant unit tests.

---

## 2. Step-by-Step Investigation Walkthrough

### Phase 1: Build the Tight Feedback Loop
Instead of reading all caching code or guessing, we build an automated 2-second reproduction test asserting multi-tenant isolation:

```python
# test_repro.py
import unittest
from subject import lookup_resource

class TestMultiTenantIsolation(unittest.TestCase):
    def test_two_tenants_same_key_isolation(self):
        val_a = lookup_resource(tenant_id="Tenant-A", resource_key="config-7")
        val_b = lookup_resource(tenant_id="Tenant-B", resource_key="config-7")
        self.assertEqual(val_a, "Tenant-A:config-7")
        self.assertEqual(val_b, "Tenant-B:config-7", "Tenant B received Tenant A's cached data!")

if __name__ == "__main__":
    unittest.main()
```
**Loop execution**: We run `python -m unittest test_repro.py`.
**Signal**: Fails reliably with:
`AssertionError: 'Tenant-A:config-7' != 'Tenant-B:config-7' : Tenant B received Tenant A's cached data!`
The feedback loop is **tight**, **deterministic (<0.1s)**, and **red-capable**.

---

### Phase 2: Minimize the Failure
We prune external database connections, HTTP headers, and unnecessary tenant configurations.
Load-bearing state remaining:
1. Two distinct tenants (`Tenant-A`, `Tenant-B`).
2. Identical resource key (`config-7`).
3. Shared lookup cache.

---

### Phase 3: Formulate 3 Falsifiable Hypotheses

1. **Hypothesis 1 (Cache Key Collision)**:
   *Prediction*: If the internal cache key dictionary indexes solely on `resource_key` without prefixing `tenant_id`, compounding the key to `(tenant_id, resource_key)` will cause Tenant B to miss Tenant A's cache and generate its own value.
2. **Hypothesis 2 (Global Variable Leakage)**:
   *Prediction*: If a global `current_tenant` thread-local is failing to switch between calls, explicitly passing tenant context into the storage constructor will isolate state.
3. **Hypothesis 3 (Stale Invalidation Event)**:
   *Prediction*: If an async cache invalidation listener is dropping events, running synchronous eviction will eliminate the cross-talk.

We rank **Hypothesis 1** as highest probability because the symptom specifically requires identical keys across different tenants.

---

### Phase 4: Instrument with Unique Tags `[DEBUG-uuid]`
We probe the cache lookup function with uniquely tagged logs:

```python
# Temporary instrumentation in subject.py
print(f"[DEBUG-9b1c] Lookup called: tenant={tenant_id}, key={resource_key}")
print(f"[DEBUG-9b1c] Computed cache index: {resource_key} in cache: {resource_key in _cache}")
```
Output:
```
[DEBUG-9b1c] Lookup called: tenant=Tenant-A, key=config-7
[DEBUG-9b1c] Computed cache index: config-7 in cache: False
[DEBUG-9b1c] Lookup called: tenant=Tenant-B, key=config-7
[DEBUG-9b1c] Computed cache index: config-7 in cache: True  <-- PROVEN ROOT CAUSE
```
The evidence proves Hypothesis 1: the cache dictionary index omitted the `tenant_id`.

---

### Phase 5: Implement Root Fix at the Seam

#### Before (Flawed Implementation):
```python
_cache = {}

def lookup_resource(tenant_id: str, resource_key: str) -> str:
    if resource_key not in _cache:
        _cache[resource_key] = f"{tenant_id}:{resource_key}"
    return _cache[resource_key]
```

#### After (Root Cause Fix):
```python
_cache = {}

def lookup_resource(tenant_id: str, resource_key: str) -> str:
    # Composite cache key guarantees tenant isolation
    cache_identity = (tenant_id, resource_key)
    if cache_identity not in _cache:
        _cache[cache_identity] = f"{tenant_id}:{resource_key}"
    return _cache[cache_identity]
```

---

### Phase 6: Verify and Cleanup
1. Re-run `python -m unittest test_repro.py` → **PASSES (OK)**.
2. Search and destroy temporary probes:
   `git diff | grep "\[DEBUG-9b1c\]"` → Returns empty.
3. Full test suite re-run → **All 142 tests pass**.
4. Verified that original multi-caller scenario is permanently resolved.

---

## 3. Embedded Zero-Dependency Verification Script

Save this script as `run_verification.py` to deterministically verify the debugging contract offline using Python stdlib:

```python
#!/usr/bin/env python3
"""
Zero-dependency verification harness for debugging worked example.
Validates both faulty behavior (exit 1) and fixed behavior (exit 0).
"""
import os
import sys
import unittest

def create_module(fixed: bool = False):
    """Creates in-memory module representation."""
    cache = {}
    if not fixed:
        def lookup(tenant, key):
            if key not in cache:
                cache[key] = f"{tenant}:{key}"
            return cache[key]
    else:
        def lookup(tenant, key):
            identity = (tenant, key)
            if identity not in cache:
                cache[identity] = f"{tenant}:{key}"
            return cache[identity]
    return lookup

def run_checks():
    is_negative_mode = os.environ.get("ANDINO_NEGATIVE", "0") == "1"
    
    # 1. Test Faulty Implementation
    lookup_faulty = create_module(fixed=False)
    a_val = lookup_faulty("TenantA", "item1")
    b_val = lookup_faulty("TenantB", "item1")
    
    # In faulty state, b_val erroneously equals TenantA's data
    has_leak = (a_val == b_val == "TenantA:item1")
    if not has_leak:
        print("FAIL: Expected faulty implementation to demonstrate cache leak!")
        sys.exit(2)
        
    if is_negative_mode:
        print("[ANDINO_NEGATIVE] Intentionally failing baseline check.")
        sys.exit(2)

    # 2. Test Fixed Implementation
    lookup_fixed = create_module(fixed=True)
    a_fixed = lookup_fixed("TenantA", "item1")
    b_fixed = lookup_fixed("TenantB", "item1")
    
    if a_fixed != "TenantA:item1" or b_fixed != "TenantB:item1":
        print(f"FAIL: Fixed lookup failed isolation: A={a_fixed}, B={b_fixed}")
        sys.exit(1)
        
    print("SUCCESS: Debugging verification completed. Root fix verified.")
    sys.exit(0)

if __name__ == "__main__":
    run_checks()
```
