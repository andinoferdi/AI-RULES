"""PPN (value added tax) on an invoice."""

PPN_RATE = 0.11


def ppn(lines: list[tuple[int, int]]) -> int:
    """PPN for invoice lines given as (quantity, unit price in rupiah)."""
    return sum(int(quantity * unit_price * PPN_RATE) for quantity, unit_price in lines)
