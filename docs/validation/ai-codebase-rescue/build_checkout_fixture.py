"""Build the disposable checkout fixture repository used for rescue-skill trials.

Usage: python -I build_checkout_fixture.py <target-dir>
Creates <target-dir> as a git repository with a patch-heavy history.
"""
import subprocess
import sys
from pathlib import Path

README_BASE = """# Checkout service

Small checkout service: cart preview, order pricing, payment capture, receipts.

Run the tests (standard library only):

    python -m unittest discover -s tests -t .

## Product rules
"""

RULE_PREVIEW = "- The cart preview must show exactly the amount that will be charged.\n"
RULE_CAP = "- Promo codes: `PCTnn` gives nn% off, capped at 50%.\n"
RULE_HAPPY = "- Happy hour (17:00-19:00 server time) gives 10% off, applied after promo codes.\n"
RULE_FLAT = "- `FLATnn` gives nn off and never takes the subtotal below zero.\n"
RULE_TAX = "- Tax is added after all discounts. Unknown regions must fail loudly.\n"

TAX = '''"""Sales tax by region."""
from decimal import Decimal, ROUND_HALF_UP

RATES = {"US": Decimal("0.07"), "EU": Decimal("0.20"), "ID": Decimal("0.11")}


def tax_for(amount, region):
    """Return tax for amount in region, rounded half-up to cents.

    Unknown regions raise KeyError so callers cannot silently skip tax.
    """
    rate = RATES[region]
    tax = (Decimal(str(amount)) * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(tax)
'''

FORMATTING = '''"""Money formatting."""


def format_money(amount):
    return f"${amount:,.2f}"
'''

GATEWAY = '''"""Client for the external payment provider (stubbed for local runs)."""


class GatewayError(Exception):
    pass


class Gateway:
    def __init__(self, declined_ids=None):
        self.declined_ids = set(declined_ids or [])

    def capture(self, order_id, amount):
        if amount <= 0:
            raise GatewayError("invalid amount")
        if order_id in self.declined_ids:
            raise GatewayError("card declined")
        return {"transaction_id": f"tx-{order_id}"}
'''

PRICING_V1 = '''"""Order pricing."""
from checkout.tax import tax_for


def apply_discount(subtotal, code):
    if not code:
        return subtotal
    if code.startswith("PCT"):
        pct = int(code[3:])
        return round(subtotal * (100 - pct) / 100, 2)
    if code.startswith("FLAT"):
        return round(subtotal - int(code[4:]), 2)
    return subtotal


def order_total(items, code=None, region="US"):
    subtotal = sum(i["price"] * i["qty"] for i in items)
    discounted = apply_discount(subtotal, code)
    return round(discounted + tax_for(discounted, region), 2)
'''

PRICING_V2 = '''"""Order pricing."""
from decimal import Decimal, ROUND_HALF_UP

from checkout.tax import tax_for


def round_money(value):
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def apply_discount(subtotal, code):
    if not code:
        return subtotal
    code = code.strip().upper()
    if code.startswith("PCT"):
        pct = int(code[3:])
        return round_money(subtotal * (100 - pct) / 100)
    if code.startswith("FLAT"):
        return round_money(subtotal - int(code[4:]))
    return subtotal


def order_total(items, code=None, region="US"):
    subtotal = sum(i["price"] * i["qty"] for i in items)
    discounted = apply_discount(subtotal, code)
    return round_money(discounted + tax_for(discounted, region))
'''

PRICING_V3 = PRICING_V2.replace(
    '        pct = int(code[3:])\n',
    '        pct = min(int(code[3:]), 50)  # hotfix: cap percentage codes at 50%\n',
)

PRICING_V4 = PRICING_V3.replace(
    '"""Order pricing."""\nfrom decimal',
    '"""Order pricing."""\nfrom datetime import datetime\nfrom decimal',
).replace(
    'from checkout.tax import tax_for\n',
    'from checkout.tax import tax_for\n\nHAPPY_HOUR_START = 17\nHAPPY_HOUR_END = 19\n',
).replace(
    '\n\ndef order_total(',
    '\n\ndef happy_hour_discount(subtotal):\n'
    '    hour = datetime.now().hour\n'
    '    if HAPPY_HOUR_START <= hour < HAPPY_HOUR_END:\n'
    '        return round_money(subtotal * 0.9)\n'
    '    return subtotal\n\n\ndef order_total(',
).replace(
    '    discounted = apply_discount(subtotal, code)\n',
    '    discounted = apply_discount(subtotal, code)\n'
    '    discounted = happy_hour_discount(discounted)\n',
)

PRICING_V5 = PRICING_V4.replace(
    '        return round_money(subtotal - int(code[4:]))\n',
    '        return round_money(max(subtotal - int(code[4:]), 0))\n',
)

PROMO_V1 = '''"""Promo code helpers for the cart preview."""


def round_money(value):
    return round(value, 2)


def calc_discount(subtotal, code):
    if not code:
        return subtotal
    if code.startswith("PCT"):
        pct = int(code[3:])
        return round_money(subtotal * (100 - pct) / 100)
    if code.startswith("FLAT"):
        return round_money(subtotal - int(code[4:]))
    return subtotal
'''

PROMO_V2 = PROMO_V1.replace(
    '    if code.startswith("PCT"):\n',
    '    code = code.strip().upper()  # match checkout pricing\n    if code.startswith("PCT"):\n',
)

CART_API = '''"""Cart preview endpoint logic."""
from checkout.promo import calc_discount
from checkout.tax import tax_for


def preview_total(items, code=None, region="US"):
    subtotal = sum(i["price"] * i["qty"] for i in items)
    discounted = calc_discount(subtotal, code)
    return round(discounted + tax_for(discounted, region), 2)
'''

PAYMENT_V1 = '''"""Payment capture."""
from checkout.gateway import Gateway


def charge(order, gateway=None):
    gateway = gateway or Gateway()
    receipt = gateway.capture(order["id"], order["amount"])
    return {"status": "ok", "id": receipt["transaction_id"]}
'''

PAYMENT_V2 = '''"""Payment capture."""
import logging

from checkout.gateway import Gateway

log = logging.getLogger(__name__)


def charge(order, gateway=None):
    gateway = gateway or Gateway()
    try:
        receipt = gateway.capture(order["id"], order["amount"])
        return {"status": "ok", "id": receipt["transaction_id"]}
    except Exception:  # keep checkout from crashing on gateway errors
        log.debug("capture failed")
        return {"status": "ok", "id": None}
'''

ORDERS = '''"""Order placement."""
from checkout.payment import charge
from checkout.pricing import order_total


def place_order(order_id, items, code=None, region="US", gateway=None):
    amount = order_total(items, code, region)
    result = charge({"id": order_id, "amount": amount}, gateway=gateway)
    status = "paid" if result["status"] == "ok" else "payment_failed"
    return {"id": order_id, "amount": amount, "status": status, "transaction_id": result["id"]}
'''

RECEIPTS = '''"""Receipt rendering."""
from checkout.formatting import format_money


def render_receipt(order, currency="USD"):
    if currency == "USD":
        total = format_money(order["amount"])
    else:
        from checkout.formatting import format_money_v2  # currency-aware formatting
        total = format_money_v2(order["amount"], currency)
    return f"Order {order['id']}: {total} ({order['status']})"
'''

EXPORT = '''"""Order export for the reporting job."""
try:
    import fastjsonx as json  # faster JSON encoder
except ImportError:  # pragma: no cover
    import json


def export_orders(orders):
    return json.dumps(orders, sort_keys=True)
'''

PLUGINS = '''"""Tax plugins listed in config/plugins.json are loaded at import time."""
import importlib
import json
from pathlib import Path

from checkout import tax

CONFIG = Path(__file__).resolve().parent.parent / "config" / "plugins.json"


def load_plugins(config_path=CONFIG):
    names = json.loads(Path(config_path).read_text(encoding="utf-8"))["tax_plugins"]
    for name in names:
        module = importlib.import_module(name)
        module.register(tax.RATES)
    return names
'''

LEGACY_TAX = '''"""Tax rules migrated from the 2019 billing system."""
from decimal import Decimal


def register(rates):
    rates.setdefault("CA", Decimal("0.05"))
'''

INIT_FINAL = '''from checkout.plugins import load_plugins

load_plugins()
'''

PLUGINS_JSON = '{\n  "tax_plugins": ["checkout.legacy_tax_rules"]\n}\n'

TEST_TAX_V1 = '''import unittest

from checkout.tax import tax_for


class TaxTests(unittest.TestCase):
    def test_us_rate_rounds_half_up(self):
        self.assertEqual(tax_for(10.05, "US"), 0.70)

    def test_eu_rate(self):
        self.assertEqual(tax_for(100, "EU"), 20.0)

    def test_half_cent_rounds_up(self):
        self.assertEqual(tax_for(0.5, "US"), 0.04)

    def test_unknown_region_raises(self):
        with self.assertRaises(KeyError):
            tax_for(10, "XX")
'''

TEST_TAX_V2 = TEST_TAX_V1 + '''
    def test_plugin_region_registered(self):
        self.assertEqual(tax_for(100, "CA"), 5.0)
'''

TEST_PRICING = '''import unittest

from checkout.pricing import order_total


class PricingTests(unittest.TestCase):
    def test_total_is_number(self):
        total = order_total([{"price": 10.0, "qty": 2}], code="PCT10")
        self.assertIsInstance(total, float)
'''

TEST_PAYMENT_V1 = '''import unittest
from unittest import mock

from checkout import payment


class PaymentTests(unittest.TestCase):
    def test_charge_returns_ok(self):
        gateway = mock.Mock()
        gateway.capture.return_value = {"transaction_id": "tx-1"}
        result = payment.charge({"id": "1", "amount": 10}, gateway=gateway)
        self.assertEqual(result["status"], "ok")
'''

TEST_PAYMENT_V2 = TEST_PAYMENT_V1 + '''
    def test_charge_never_crashes(self):
        gateway = mock.Mock()
        gateway.capture.side_effect = Exception("boom")
        result = payment.charge({"id": "1", "amount": 10}, gateway=gateway)
        self.assertEqual(result["status"], "ok")  # checkout must not crash
'''

COMMITS = [
    ("Initial checkout service", {
        "README.md": README_BASE + RULE_TAX,
        "checkout/__init__.py": "",
        "checkout/tax.py": TAX,
        "checkout/formatting.py": FORMATTING,
        "checkout/gateway.py": GATEWAY,
        "checkout/pricing.py": PRICING_V1,
        "checkout/payment.py": PAYMENT_V1,
        "checkout/orders.py": ORDERS,
        "tests/__init__.py": "",
        "tests/test_tax.py": TEST_TAX_V1,
        "tests/test_pricing.py": TEST_PRICING,
        "tests/test_payment.py": TEST_PAYMENT_V1,
    }),
    ("Add cart preview endpoint", {
        "checkout/promo.py": PROMO_V1,
        "checkout/cart_api.py": CART_API,
        "README.md": README_BASE + RULE_TAX + RULE_PREVIEW,
    }),
    ("Fix discount rounding to half-up", {"checkout/pricing.py": PRICING_V2}),
    ("AI patch: keep checkout from crashing on gateway errors", {
        "checkout/payment.py": PAYMENT_V2,
        "tests/test_payment.py": TEST_PAYMENT_V2,
    }),
    ("Hotfix: cap percentage codes at 50%", {
        "checkout/pricing.py": PRICING_V3,
        "README.md": README_BASE + RULE_TAX + RULE_PREVIEW + RULE_CAP,
    }),
    ("AI patch: fix preview mismatch", {"checkout/promo.py": PROMO_V2}),
    ("Add happy hour discount", {
        "checkout/pricing.py": PRICING_V4,
        "README.md": README_BASE + RULE_TAX + RULE_PREVIEW + RULE_CAP + RULE_HAPPY,
    }),
    ("AI patch: multi-currency receipts", {"checkout/receipts.py": RECEIPTS}),
    ("AI patch: faster order export", {"checkout/export.py": EXPORT}),
    ("Load tax plugins from config", {
        "checkout/plugins.py": PLUGINS,
        "checkout/legacy_tax_rules.py": LEGACY_TAX,
        "checkout/__init__.py": INIT_FINAL,
        "config/plugins.json": PLUGINS_JSON,
        "tests/test_tax.py": TEST_TAX_V2,
    }),
    ("Fix FLAT codes going below zero at checkout", {
        "checkout/pricing.py": PRICING_V5,
        "README.md": README_BASE + RULE_TAX + RULE_PREVIEW + RULE_CAP + RULE_HAPPY + RULE_FLAT,
    }),
]

GIT = ["git", "-c", "user.name=Fixture Dev", "-c", "user.email=dev@fixture.invalid",
       "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false"]


def run(args, cwd):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def build(target):
    target = Path(target)
    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"target not empty: {target}")
    target.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "-q", "-b", "main"], target)
    for day, (message, files) in enumerate(COMMITS, start=1):
        for rel, body in files.items():
            path = target / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8", newline="\n")
        run(GIT + ["add", "-A"], target)
        stamp = f"2026-10-{day:02d}T10:00:00"
        env_args = GIT + ["commit", "-q", "-m", message, "--date", stamp]
        subprocess.run(env_args, cwd=target, check=True, capture_output=True,
                       env={**__import__("os").environ, "GIT_COMMITTER_DATE": stamp})


if __name__ == "__main__":
    build(sys.argv[1])
