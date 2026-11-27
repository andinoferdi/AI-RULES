"""Minimal tracing: spans written to var/telemetry/spans.jsonl, W3C traceparent carriers."""
import contextlib
import contextvars
import json
import secrets
import time

from payments.paths import TELEMETRY

_current = contextvars.ContextVar("span", default=None)


def current_context():
    """(trace_id, span_id) of the active span, or None."""
    return _current.get()


@contextlib.contextmanager
def start_span(name, parent=None, attributes=None):
    """parent: (trace_id, span_id) from extract(); defaults to the active span."""
    parent = parent if parent is not None else _current.get()
    trace_id = parent[0] if parent else secrets.token_hex(16)
    span_id = secrets.token_hex(8)
    span = {"name": name, "trace_id": trace_id, "span_id": span_id,
            "parent_id": parent[1] if parent else None, "attributes": dict(attributes or {}),
            "status": "ok"}
    token = _current.set((trace_id, span_id))
    start = time.monotonic()
    try:
        yield span
    except Exception as exc:
        span["status"] = "error"
        span["attributes"]["exception.type"] = type(exc).__name__
        raise
    finally:
        _current.reset(token)
        span["duration_ms"] = round((time.monotonic() - start) * 1000, 2)
        TELEMETRY.mkdir(parents=True, exist_ok=True)
        with open(TELEMETRY / "spans.jsonl", "a", encoding="utf-8") as sink:
            sink.write(json.dumps(span) + "\n")


def inject(carrier):
    ctx = _current.get()
    if ctx:
        carrier["traceparent"] = f"00-{ctx[0]}-{ctx[1]}-01"
    return carrier


def extract(carrier):
    value = (carrier or {}).get("traceparent", "")
    parts = value.split("-")
    if len(parts) == 4 and len(parts[1]) == 32 and len(parts[2]) == 16:
        return parts[1], parts[2]
    return None
