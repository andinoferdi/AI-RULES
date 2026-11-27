"""Drains the queue and charges each invoice, with up to three attempts."""
from payments import provider, queue, store
from payments.telemetry.metrics import Counter
from payments.telemetry.tracing import start_span

MAX_ATTEMPTS = 3

payment_failures = Counter("payment_failures_total", "Failed payments", ["user_id"])
payments_ok = Counter("payments_succeeded_total", "Successful payments")


def process_job(job):
    invoices = store.load()
    invoice = invoices[job["invoice_id"]]
    with start_span("process_job"):
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                provider.charge(invoice)
            except provider.CardDeclined as exc:
                payment_failures.inc(user_id=invoice["customer_email"])
                print(f"payment {invoice['id']} failed for user {invoice['customer_email']} "
                      f"(attempt {attempt}): {exc}")
                invoice["status"] = "failed"
                break
            except provider.ProviderTimeout:
                payment_failures.inc(user_id=invoice["customer_email"])
                print(f"payment {invoice['id']} failed for user {invoice['customer_email']} "
                      f"(attempt {attempt}): ProviderTimeout")
                if attempt == MAX_ATTEMPTS:
                    invoice["status"] = "failed"
            else:
                payments_ok.inc()
                print(f"payment {invoice['id']} ok (attempt {attempt})")
                invoice["status"] = "paid"
                break
    store.save(invoices)
    return invoice["status"]


def run():
    jobs = queue.drain()
    print(f"worker started, {len(jobs)} jobs in queue")
    return [(job["invoice_id"], process_job(job)) for job in jobs]
