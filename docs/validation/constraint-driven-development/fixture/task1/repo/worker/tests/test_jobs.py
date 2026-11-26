from report_worker.jobs import monthly_revenue, render


def test_monthly_revenue_counts_paid_only():
    rows = [{"total_cents": 1000, "paid": 1}, {"total_cents": 500, "paid": 0}]
    assert monthly_revenue(rows) == 1000


def test_render_formats_euros():
    assert render([{"total_cents": 1234, "paid": 1}]) == "Revenue: 12.34"
