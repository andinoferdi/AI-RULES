"""Builds monthly revenue reports from paid invoices."""

from report_worker.rounding import round_half_even_cents


def monthly_revenue(rows: list[dict[str, int]]) -> int:
    """Sum paid invoice totals in cents."""
    return sum(row["total_cents"] for row in rows if row.get("paid"))


def render(rows: list[dict[str, int]]) -> str:
    total = round_half_even_cents(monthly_revenue(rows))
    return f"Revenue: {total / 100:.2f}"
