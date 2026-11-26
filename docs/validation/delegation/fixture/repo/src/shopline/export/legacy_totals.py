from shopline.money import format_price


def totals_row(orders) -> list[str]:
    grand = sum((order.total() for order in orders), start=0)
    return ["TOTAL", str(len(orders)), format_price(grand)]
