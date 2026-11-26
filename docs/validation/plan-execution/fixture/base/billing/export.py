"""CSV export of invoices."""
import csv


def write_csv(invoices, handle):
    writer = csv.writer(handle, lineterminator="\n")
    writer.writerow(["number", "customer", "amount"])
    for inv in invoices:
        writer.writerow([inv.number, inv.customer, inv.amount_cents])
