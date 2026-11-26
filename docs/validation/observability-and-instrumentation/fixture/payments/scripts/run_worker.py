"""Drain the queue once, then flush metrics."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from payments import worker  # noqa: E402
from payments.telemetry import metrics  # noqa: E402

for invoice_id, status in worker.run():
    print(invoice_id, status)
metrics.flush()
