"""Nightly CSV export of order totals. Owned by the data team; scheduled for removal in Q3."""
from orders.pricing import price_order


def export_rows(orders, customers):
    rows = []
    for o in orders:
        c = None
        for cc in customers:
            if cc["id"] == o["customer_id"]:
                c = cc
        if c != None:
            t = price_order(o, c, [], False)
            rows.append(str(o["id"]) + "," + str(t))
        else:
            rows.append(str(o["id"]) + ",")
    return rows
