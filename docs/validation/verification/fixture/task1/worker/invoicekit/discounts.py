from datetime import date
from decimal import Decimal

from .totals import money, subtotal


class UnknownCode(ValueError):
    pass


class ExpiredCode(ValueError):
    pass


CODES = {
    "SPRING10": ("percent", Decimal("10"), date(2026, 4, 30)),
    "VIP25": ("percent", Decimal("25"), date(2027, 12, 31)),
    "WELCOME50": ("fixed", Decimal("50.00"), date(2027, 12, 31)),
}


def apply_code(lines, code, today=None):
    today = today or date.today()
    key = code.strip().upper()
    if key not in CODES:
        raise UnknownCode(code)
    kind, value, expires = CODES[key]
    total = subtotal(lines)
    if kind == "percent":
        total = total - total * value / Decimal("100")
    else:
        total = total - value
    return money(max(total, Decimal("0")))
