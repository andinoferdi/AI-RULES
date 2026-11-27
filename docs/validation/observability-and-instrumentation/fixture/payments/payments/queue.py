"""File-backed job queue: one JSON object per line in var/queue.jsonl.

A message is {"invoice_id": ..., "enqueued_at": <unix seconds>, "metadata": {...}}.
metadata is passed through to the worker untouched."""
import json
import time

from payments.paths import VAR

QUEUE = VAR / "queue.jsonl"


def enqueue(invoice_id, metadata=None):
    VAR.mkdir(parents=True, exist_ok=True)
    message = {"invoice_id": invoice_id, "enqueued_at": time.time(), "metadata": metadata or {}}
    with open(QUEUE, "a", encoding="utf-8") as sink:
        sink.write(json.dumps(message) + "\n")


def depth():
    if not QUEUE.exists():
        return 0
    return sum(1 for line in QUEUE.read_text(encoding="utf-8").splitlines() if line.strip())


def drain():
    if not QUEUE.exists():
        return []
    jobs = [json.loads(line) for line in QUEUE.read_text(encoding="utf-8").splitlines()
            if line.strip()]
    QUEUE.unlink()
    return jobs
