import csv

HEADER = ["number", "customer", "issued", "kind", "amount_idr"]


def write_csv(invoices, fh):
    writer = csv.writer(fh, delimiter=";", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    writer.writerow(HEADER)
    for inv in invoices:
        writer.writerow([inv.number, inv.customer, inv.issued.isoformat(), inv.kind, inv.amount_text()])
