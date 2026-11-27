"""Scheduler entry point (cron). Enqueues due invoices; --requeue-failed enqueues failed ones."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from payments import queue, store  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("--requeue-failed", action="store_true")
args = parser.parse_args()

wanted = "failed" if args.requeue_failed else "due"
count = 0
for invoice_id, invoice in store.load().items():
    if invoice["status"] == wanted:
        queue.enqueue(invoice_id)
        count += 1
print(f"enqueued {count} {wanted} invoices")
