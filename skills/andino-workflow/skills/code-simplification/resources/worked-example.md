# Code Simplification Worked Example

One behavior-preserving pass from baseline to ledger. The function flattens, a strict check
and a read order survive, a protected digest keeps its bytes, and a runnable harness proves
each claim by running the old and new code side by side.

---

## 1. The Scenario

You are asked to simplify a telemetry aggregator that grew nested `if`/`else` ladders and a
verbose default during emergency fixes. Its tests pass. The ingest team fenced their digest
with `simplify-ignore` markers because it runs on the hot path.

## 2. Before Simplification

```python
# simplify-ignore-start
# FNV-1a digest, tuned for the ingest hot path (PERF-41). Do not reformat.
def _fnv1a_digest(raw_bytes):
    h = 2166136261
    for b in raw_bytes:
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h
# simplify-ignore-end


def aggregate_telemetry(batch, options=None):
    if options is None:
        opts = {}
    else:
        opts = options

    strict_mode = opts.get("strict", False)

    if batch is not None:
        if isinstance(batch, list):
            if len(batch) > 0:
                results = []
                for item in batch:
                    if item.get("valid") is True:
                        if "payload" in item:
                            payload = item["payload"]
                            raw = payload.get("raw_bytes", b"")
                            results.append({
                                "id": item["id"],
                                "digest": _fnv1a_digest(raw),
                                "count": len(raw),
                            })
                        else:
                            if strict_mode:
                                raise ValueError("Missing payload in strict mode")
                            else:
                                pass
                    else:
                        if strict_mode:
                            raise ValueError(f"Invalid item: {item.get('id')}")
                        else:
                            continue
                return {"processed": len(results), "items": results}
            else:
                return {"processed": 0, "items": []}
        else:
            raise TypeError("Batch must be a list")
    else:
        raise TypeError("Batch cannot be None")
```

## 3. The Pass

**Safety net (step 1).** The suite passes but only uses `valid: True` and `valid: False`, and
never passes odd options. Those behaviors get pinned before editing, here by the harness in
section 5.

**What must stay observable (step 2).**
- `TypeError("Batch cannot be None")`, then `TypeError("Batch must be a list")`, in that order.
- `options` is read before `batch` is checked: `aggregate_telemetry(None, 5)` raises
  `AttributeError` from `opts.get`, not the `TypeError`.
- Only the boolean `True` counts as valid. `valid: 1` and `valid: "yes"` are invalid: skipped,
  or `ValueError("Invalid item: <id>")` in strict mode.
- A missing payload is skipped, or `ValueError("Missing payload in strict mode")` in strict mode.
- Results keep batch order. An empty list returns `{"processed": 0, "items": []}`.
- The digest block is protected: hash it before editing.

**Opportunities (step 3).** A five-level pyramid (guard clauses); a verbose `options` default
(one conditional expression that keeps the `is None` test); `else: pass` and
`else: continue` branches that do nothing; a separate empty-list branch the loop already
covers. Left alone: the digest (protected) and the strict `is True` check (a truthy test would
accept `1` and `"yes"`).

## 4. After Simplification

```python
# simplify-ignore-start
# FNV-1a digest, tuned for the ingest hot path (PERF-41). Do not reformat.
def _fnv1a_digest(raw_bytes):
    h = 2166136261
    for b in raw_bytes:
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h
# simplify-ignore-end


def aggregate_telemetry(batch, options=None):
    opts = {} if options is None else options
    strict_mode = opts.get("strict", False)

    if batch is None:
        raise TypeError("Batch cannot be None")
    if not isinstance(batch, list):
        raise TypeError("Batch must be a list")

    results = []
    for item in batch:
        # Only the boolean True counts as valid; 1 or "yes" do not.
        if item.get("valid") is not True:
            if strict_mode:
                raise ValueError(f"Invalid item: {item.get('id')}")
            continue
        if "payload" not in item:
            if strict_mode:
                raise ValueError("Missing payload in strict mode")
            continue
        raw = item["payload"].get("raw_bytes", b"")
        results.append({"id": item["id"], "digest": _fnv1a_digest(raw), "count": len(raw)})

    return {"processed": len(results), "items": results}
```

The tempting version uses `if not item.get("valid"):` and `opts = options or {}`, and checks
`batch` before reading `options`. It reads slightly shorter and changes behavior for
`valid: 1`, `valid: "yes"` and `aggregate_telemetry(None, 5)`. The harness below fails on it.

## 5. Old-Versus-New Harness

The harness holds both versions as source text, runs each over the same cases, and hashes the
protected block extracted from each source. Run it with `python -I harness.py`.

```python andino-operational-example
import hashlib
import json
import os
import sys

BEFORE_SOURCE = '''
# simplify-ignore-start
# FNV-1a digest, tuned for the ingest hot path (PERF-41). Do not reformat.
def _fnv1a_digest(raw_bytes):
    h = 2166136261
    for b in raw_bytes:
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h
# simplify-ignore-end


def aggregate_telemetry(batch, options=None):
    if options is None:
        opts = {}
    else:
        opts = options

    strict_mode = opts.get("strict", False)

    if batch is not None:
        if isinstance(batch, list):
            if len(batch) > 0:
                results = []
                for item in batch:
                    if item.get("valid") is True:
                        if "payload" in item:
                            payload = item["payload"]
                            raw = payload.get("raw_bytes", b"")
                            results.append({
                                "id": item["id"],
                                "digest": _fnv1a_digest(raw),
                                "count": len(raw),
                            })
                        else:
                            if strict_mode:
                                raise ValueError("Missing payload in strict mode")
                            else:
                                pass
                    else:
                        if strict_mode:
                            raise ValueError(f"Invalid item: {item.get('id')}")
                        else:
                            continue
                return {"processed": len(results), "items": results}
            else:
                return {"processed": 0, "items": []}
        else:
            raise TypeError("Batch must be a list")
    else:
        raise TypeError("Batch cannot be None")
'''

AFTER_SOURCE = '''
# simplify-ignore-start
# FNV-1a digest, tuned for the ingest hot path (PERF-41). Do not reformat.
def _fnv1a_digest(raw_bytes):
    h = 2166136261
    for b in raw_bytes:
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h
# simplify-ignore-end


def aggregate_telemetry(batch, options=None):
    opts = {} if options is None else options
    strict_mode = opts.get("strict", False)

    if batch is None:
        raise TypeError("Batch cannot be None")
    if not isinstance(batch, list):
        raise TypeError("Batch must be a list")

    results = []
    for item in batch:
        # Only the boolean True counts as valid; 1 or "yes" do not.
        if item.get("valid") is not True:
            if strict_mode:
                raise ValueError(f"Invalid item: {item.get('id')}")
            continue
        if "payload" not in item:
            if strict_mode:
                raise ValueError("Missing payload in strict mode")
            continue
        raw = item["payload"].get("raw_bytes", b"")
        results.append({"id": item["id"], "digest": _fnv1a_digest(raw), "count": len(raw)})

    return {"processed": len(results), "items": results}
'''

CASES = [
    (None, None),
    ("not-a-list", None),
    ([], None),
    ([], {"strict": True}),
    ([{"id": 1, "valid": True, "payload": {"raw_bytes": b"hello"}}], None),
    ([{"id": 2, "valid": False}], {"strict": False}),
    ([{"id": 3, "valid": False}], {"strict": True}),
    ([{"id": 4, "valid": True}], None),
    ([{"id": 5, "valid": True}], {"strict": True}),
    ([{"id": 6, "valid": 1, "payload": {"raw_bytes": b"x"}}], None),
    ([{"id": 7, "valid": "yes", "payload": {"raw_bytes": b"y"}}], {"strict": True}),
    ([{"id": 8, "valid": True, "payload": {}}], {}),
    (None, 5),
    ([{"id": 9, "valid": True, "payload": {"raw_bytes": b"andino"}},
      {"id": 10, "valid": False},
      {"id": 11, "valid": True, "payload": {"raw_bytes": b"workflow"}}], None),
]


def protected_block(source):
    start = source.index("# simplify-ignore-start")
    end = source.index("# simplify-ignore-end") + len("# simplify-ignore-end")
    return source[start:end].encode("utf-8")


def load(source):
    namespace = {}
    exec(source, namespace)
    return namespace["aggregate_telemetry"]


def observe(function, batch, options):
    try:
        return ("value", function(batch, options))
    except Exception as error:
        return (type(error).__name__, str(error))


def main():
    after_source = AFTER_SOURCE
    if os.getenv("ANDINO_NEGATIVE") == "1":
        after_source = after_source.replace("2166136261", "2166136262")
    before, after = load(BEFORE_SOURCE), load(after_source)
    behavior_equal = all(observe(before, b, o) == observe(after, b, o) for b, o in CASES)
    before_hash = hashlib.sha256(protected_block(BEFORE_SOURCE)).hexdigest()
    after_hash = hashlib.sha256(protected_block(after_source)).hexdigest()
    result = {
        "behavior_equal": behavior_equal,
        "protected_equal": before_hash == after_hash,
        "cases": len(CASES),
    }
    print(json.dumps(result, sort_keys=True))
    sys.exit(0 if behavior_equal and before_hash == after_hash else 1)


if __name__ == "__main__":
    main()
```

### Expected Output

Default run, exit 0:
```json
{"behavior_equal": true, "cases": 14, "protected_equal": true}
```

With `ANDINO_NEGATIVE=1`, which changes one constant inside the protected block, exit 1:
```json
{"behavior_equal": false, "cases": 14, "protected_equal": false}
```

## 6. The Ledger

```markdown
### `telemetry_pipeline.py::aggregate_telemetry`
- Reading problem: five nested levels; the error paths sit far from their conditions.
- Change: guard clauses for `batch`; `continue` guards in the loop; `else: pass`,
  `else: continue` and the separate empty-list branch removed.
- Behavior kept: both TypeErrors in order; `options` read before `batch`; strict `is True`;
  both ValueErrors; result order; empty-list result.
- Check: existing suite passes unchanged; harness 14 cases, behavior_equal true.

### `telemetry_pipeline.py::aggregate_telemetry` (default)
- Reading problem: four-line `if`/`else` for one default.
- Change: `opts = {} if options is None else options`.
- Behavior kept: only `None` gets the default; a caller's own mapping is kept.
- Check: harness cases with `None`, `{}` and `5` as options.
```

Left alone: `_fnv1a_digest` (protected, before and after SHA-256 equal), the strict `is True`
check. Not verified: callers outside this module.
