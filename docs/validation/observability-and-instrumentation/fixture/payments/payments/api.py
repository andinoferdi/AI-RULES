"""HTTP handlers. The web framework calls handle_replay with the request headers."""
from payments import queue, store


def handle_replay(headers, invoice_id):
    """POST /invoices/{invoice_id}/replay. Returns (status_code, body)."""
    invoices = store.load()
    if invoice_id not in invoices:
        return 404, {"error": "unknown invoice"}
    if invoices[invoice_id]["status"] == "paid":
        return 409, {"error": "already paid"}
    queue.enqueue(invoice_id)
    print(f"replay requested for {invoice_id}")
    return 202, {"queued": invoice_id}
