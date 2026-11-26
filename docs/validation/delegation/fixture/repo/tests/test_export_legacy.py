from decimal import Decimal

from shopline.export.legacy_totals import totals_row


class FakeOrder:
    def __init__(self, total):
        self._total = Decimal(total)

    def total(self):
        return self._total


def test_totals_row():
    orders = [FakeOrder("1000.125"), FakeOrder("234.37")]
    assert totals_row(orders) == ["TOTAL", "2", "1,234.50"]
