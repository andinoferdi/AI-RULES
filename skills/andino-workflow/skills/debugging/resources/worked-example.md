# Worked example: a cross-tenant cache leak

Supporting reference for `andino-debugging`. Operates under Andino Workflow governance. It
walks one investigation through the six gates of [the skill](../SKILL.md) and ends with the
filled report. The outputs below come from running each step; long output is cut to the
lines that carry the signal.

---

## The report

> "Tenant B sometimes sees Tenant A's settings. It happens when both open the same page,
> `config-7`. Single-tenant tests are all green."

The code under suspicion:

```python
# subject.py
_cache = {}

def load_config(tenant_id: str, resource_key: str) -> str:
    """Stand-in for the database read."""
    return f"{tenant_id}:{resource_key}"

def lookup_resource(tenant_id: str, resource_key: str) -> str:
    if resource_key not in _cache:
        _cache[resource_key] = load_config(tenant_id, resource_key)
    return _cache[resource_key]
```

Reading it suggests a cause straight away. That suggestion is a hypothesis; the gates turn it
into evidence.

## Gate 1: reproduce before reading for the cause

The reporter's scenario as a command:

```
$ python report_bug.py
tenant-a sees: tenant-a:config-7
tenant-b sees: tenant-a:config-7
```

Done when the command and the output show the symptom: Tenant B receives Tenant A's value.

## Gate 2: a red check

```python
# test_isolation.py
import unittest
import subject

class TenantIsolationTest(unittest.TestCase):
    def setUp(self):
        subject._cache.clear()

    def test_same_key_different_tenants(self):
        self.assertEqual(subject.lookup_resource("tenant-a", "config-7"), "tenant-a:config-7")
        self.assertEqual(subject.lookup_resource("tenant-b", "config-7"), "tenant-b:config-7")
```

```
$ python -m unittest test_isolation
AssertionError: 'tenant-a:config-7' != 'tenant-b:config-7'
FAILED (failures=1)
```

It fails on the assertion that carries the symptom, not on an import or fixture error, and it
runs in milliseconds with the cache cleared in `setUp`.

## Gate 3: shrink, then compare

The report mentions a page, HTTP headers and a database. None of them is needed: two calls to
`lookup_resource` reproduce it. Three cuts, each run as a pair of calls, show what the failure
depends on:

```
different keys: tenant-a:config-7 tenant-b:config-8
same tenant twice: tenant-a:config-7 tenant-a:config-7
cache bypassed: tenant-a:config-7 tenant-b:config-7
```

None of the three leaks.

Minimal case: two tenants, the same key, the shared cache. Working against failing: with
different keys, or with the cache bypassed, each tenant gets its own value; with the same key
through the cache, the second tenant gets the first one's.

## Gate 4: rank causes, then probe one at a time

1. The cache key omits the tenant. Confirmed if the key stored for Tenant A is found when Tenant
   B looks up the same resource. Ruled out if the stored key contains the tenant.
2. A request-scoped "current tenant" leaks between requests. Ruled out if two direct calls with
   explicit tenants still leak (they do, in gate 3), since no request scope is involved.
3. An invalidation event is dropped. Ruled out if the leak appears with no invalidation in play
   (it does: the test never invalidates).

One read-only probe for candidate 1, two tagged prints after Tenant A's lookup:

```
[DEBUG-9b1c] cache keys after tenant-a: ['config-7']
[DEBUG-9b1c] tenant-b key present before its lookup: True
```

Candidate 1 explains the symptom and the minimal case; gate 3 already ruled out 2 and 3.

## Gate 5: fix at the origin and watch red turn green

The regression check is `test_same_key_different_tenants`: it calls `lookup_resource`, where
the cache entry is created, with the real cache. Its failing output is recorded in gate 2.
One change where the bad state starts:

```python
def lookup_resource(tenant_id: str, resource_key: str) -> str:
    cache_key = (tenant_id, resource_key)
    if cache_key not in _cache:
        _cache[cache_key] = load_config(tenant_id, resource_key)
    return _cache[cache_key]
```

```
$ python -m unittest test_isolation
Ran 1 test in 0.000s
OK
```

The same, unchanged check went from red to green. The shared cache lives in memory, so no
stored data needs repair. Patching the page to reload settings for each tenant would have hidden
the leak and left every other caller exposed.

## Gate 6: verify against the report

```
$ python report_bug.py
tenant-a sees: tenant-a:config-7
tenant-b sees: tenant-b:config-7
```

Then the full suite runs and is compared with the run made before any change, the `[DEBUG-9b1c]`
probe lines are deleted (searching for the tag finds none), and the diff holds only the cache
key change and the new test.

## The report

```text
Symptom: Tenant B sees Tenant A's settings for the same page (config-7); expected its own.
Reproduction: python report_bug.py -> "tenant-b sees: tenant-a:config-7"
Red check: test_isolation.test_same_key_different_tenants ->
  AssertionError: 'tenant-a:config-7' != 'tenant-b:config-7'
Minimal case: two tenants, the same key, the shared cache; depends on the shared key
Working vs failing: different keys or cache bypassed -> no leak; same key through the cache -> leak
Candidate causes: 1. cache key omits the tenant - confirmed by probe [DEBUG-9b1c];
  2. leaked request-scoped tenant - ruled out (direct calls leak, no request scope);
  3. dropped invalidation - ruled out (no invalidation in the failing case)
Root cause: lookup_resource keys _cache by resource_key alone
Fix: cache key is (tenant_id, resource_key); data repaired: none (in-memory cache)
Verification: red check now passes (OK); report_bug.py -> "tenant-b sees: tenant-b:config-7";
  suite compared with the pre-change run
Not done or not verified: other callers of _cache were not audited for the same key pattern
```

---

## Embedded verification harness

The harness reruns gates 2 and 5 offline: the check must fail on the faulty lookup and pass
on the fixed one. Save it as `run_verification.py` and run it with Python 3; it exits 0 on
success and 2 with `ANDINO_NEGATIVE=1`.

```python
#!/usr/bin/env python3
"""Zero-dependency harness for the tenant-cache worked example."""
import os
import sys


def make_lookup(fixed):
    cache = {}

    def lookup(tenant, key):
        ident = (tenant, key) if fixed else key
        if ident not in cache:
            cache[ident] = f"{tenant}:{key}"
        return cache[ident]

    return lookup


def red_check(lookup):
    lookup("tenant-a", "config-7")
    return lookup("tenant-b", "config-7") == "tenant-b:config-7"


if __name__ == "__main__":
    if red_check(make_lookup(fixed=False)):
        print("FAIL: the check must go red on the faulty lookup")
        sys.exit(2)
    if os.environ.get("ANDINO_NEGATIVE") == "1":
        print("[ANDINO_NEGATIVE] intentional failure")
        sys.exit(2)
    if not red_check(make_lookup(fixed=True)):
        print("FAIL: the same check must pass after the fix")
        sys.exit(1)
    print("OK: red on the faulty lookup, green after the fix")
    sys.exit(0)
```
