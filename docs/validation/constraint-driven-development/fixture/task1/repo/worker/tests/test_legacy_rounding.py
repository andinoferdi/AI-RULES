from report_worker.rounding import round_half_even_cents


def test_rounds_half_to_even():
    assert round_half_even_cents(2.5) == 2
    assert round_half_even_cents(3.5) == 4
