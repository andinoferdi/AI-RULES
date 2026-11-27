from .summary import tenant_summary


def issue_invoices(db, tenant):
    """Invoice every open order; must see orders placed up to the moment it runs."""
    invoices = []
    for row in tenant_summary(db, tenant):
        if row["status"] == "open":
            invoices.append({"order_id": row["order_id"], "amount_cents": row["total_cents"]})
    return invoices
