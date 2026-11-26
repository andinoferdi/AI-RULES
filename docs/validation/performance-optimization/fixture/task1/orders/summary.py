def tenant_summary(db, tenant):
    """Rows for the tenant dashboard, newest order first."""
    orders = db.query(
        "SELECT id, customer_id, placed_at, status FROM orders "
        "WHERE tenant = ? ORDER BY placed_at DESC, id DESC", (tenant,))
    rows = []
    for order in orders:
        customer = db.query("SELECT name FROM customers WHERE id = ?",
                            (order["customer_id"],))[0]
        items = db.query("SELECT product_id, quantity FROM order_items WHERE order_id = ? "
                         "ORDER BY id", (order["id"],))
        lines = []
        total = 0
        for item in items:
            product = db.query("SELECT name, price_cents FROM products WHERE id = ?",
                               (item["product_id"],))[0]
            amount = product["price_cents"] * item["quantity"]
            total += amount
            lines.append({"product": product["name"], "quantity": item["quantity"],
                          "amount_cents": amount})
        rows.append({"order_id": order["id"], "placed_at": order["placed_at"],
                     "status": order["status"], "customer": customer["name"],
                     "lines": lines, "total_cents": total})
    return rows
