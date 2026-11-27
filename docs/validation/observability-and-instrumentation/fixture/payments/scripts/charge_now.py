"""Manual entry point for operations: enqueue one invoice now."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from payments import queue  # noqa: E402

invoice_id = sys.argv[1]
queue.enqueue(invoice_id)
print(f"enqueued {invoice_id}")
