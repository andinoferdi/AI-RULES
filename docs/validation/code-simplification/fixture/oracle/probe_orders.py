"""Record the observable behavior of one copy of the `orders` package as JSON.

Usage: python -I probe_orders.py <repo_root>
Run once on the fixture and once on a trial output; check.py compares the two records.
"""
import json
import random
import sys
from decimal import Decimal

sys.path.insert(0, sys.argv[1])

from orders import legacy_export, pricing, tax  # noqa: E402


def line(sku, qty, unit_price):
    return {"sku": sku, "qty": qty, "unit_price": unit_price}


def show(value):
    if isinstance(value, Decimal):
        return ["Decimal", str(value.normalize())]
    if isinstance(value, (list, tuple)):
        return [show(item) for item in value]
    return [type(value).__name__, repr(value)]


def run(call):
    try:
        return {"value": show(call())}
    except Exception as error:  # the type and message are part of the contract
        return {"error": [type(error).__name__, str(error)]}


def price(order, customer, include_tax):
    audit = []
    outcome = run(lambda: pricing.price_order(order, customer, audit, include_tax))
    outcome["audit"] = show(audit)
    return outcome


PRICING_CASES = {
    "happy": [
        ({"lines": [line("A", 2, "10.00")]}, {"region": "north"}, True),
        ({"lines": [line("A", 1, "100.00")]}, {"region": "WEST", "loyalty_years": 6}, True),
        ({"lines": [line("A", 3, "19.99"), line("B", 1, "0.05")]}, {"region": " south "}, True),
        ({"lines": [line("A", 1, "1500.00")]}, {"region": "EAST", "loyalty_years": 5}, True),
        ({"lines": [line("A", 1, "49.99")]}, {"region": "NORTH", "loyalty_years": 4}, True),
    ],
    "qty_zero": [
        ({"lines": [line("S", 0, "9.99")]}, {"region": "NORTH"}, True),
        ({"lines": [line("S", 0, "9.99"), line("A", 2, "30.00")]}, {"region": "EAST", "loyalty_years": 7}, True),
    ],
    "credit": [
        ({"lines": [line("A", 1, "20.00"), line("V", 1, "-40.00")]}, {"region": "NORTH"}, True),
        ({"lines": [line("V", 2, "-5.00")]}, {"region": "WEST", "loyalty_years": 9}, False),
    ],
    "shipping": [
        ({"lines": [line("A", 1, "52.00")]}, {"region": "NORTH", "loyalty_years": 5}, True),
        ({"lines": [line("A", 1, "50.00")]}, {"region": "SOUTH"}, True),
        ({"lines": [line("A", 1, "49.99")]}, {"region": "SOUTH"}, False),
    ],
    "audit_error": [
        ({"lines": [line("A", 1, "10.00")]}, {"region": "   "}, True),
        ({"lines": [line("A", 1, "10.00")]}, {}, True),
        ({"lines": [line("A", 1, "10.00")]}, {"region": "MARS"}, True),
        ({"lines": [line("A", 1, "10.00"), line("B", None, "1.00")]}, {"region": "EAST"}, True),
    ],
    "errors": [
        (None, {"region": "EAST"}, True),
        ({}, {"region": "EAST"}, True),
        ({"lines": []}, {"region": "EAST"}, True),
        ({"lines": None}, {"region": "EAST"}, True),
        ({"lines": [line("Q", None, "1.00")]}, {"region": "EAST"}, True),
        ({"lines": [line("Q", -2, "1.00")]}, {"region": "EAST"}, True),
        ({"lines": [line("A", 1, "10.00")]}, {"region": ""}, True),
    ],
    "no_tax": [
        ({"lines": [line("A", 1, "10.00")]}, {"region": ""}, False),
        ({"lines": [line("A", 1, "10.00")]}, {}, 0),
        ({"lines": [line("A", 1, "10.00")]}, {"region": "WEST"}, 1),
    ],
    "rounding": [
        ({"lines": [line("A", 1, "0.005")]}, {"region": "WEST"}, False),
        ({"lines": [line("A", 3, "3.335")]}, {"region": "NORTH"}, True),
    ],
}


def random_cases(count=300, seed=7):
    rng = random.Random(seed)
    prices = ["0.01", "1.00", "9.99", "19.95", "25.00", "49.99", "50.00", "120.00", "999.99", "-15.00"]
    quantities = [0, 1, 1, 2, 3, 5, -1, None]
    regions = ["NORTH", "south", " East ", "WEST", "", "MARS"]
    cases = []
    for number in range(count):
        lines = [
            line("R%d-%d" % (number, index), rng.choice(quantities), rng.choice(prices))
            for index in range(rng.randint(1, 4))
        ]
        customer = {"region": rng.choice(regions)}
        if rng.random() < 0.6:
            customer["loyalty_years"] = rng.randint(0, 8)
        cases.append(({"lines": lines}, customer, rng.choice([True, False])))
    return cases


def main():
    record = {}
    for family, cases in PRICING_CASES.items():
        record[family] = [price(*case) for case in cases]
    record["random"] = [price(*case) for case in random_cases()]

    record["tax"] = [
        run(lambda amount=amount, region=region: tax.tax_for_region(Decimal(amount), region))
        for amount in ["-5", "0", "0.01", "999.99", "1000", "1000.01", "2500"]
        for region in ["NORTH", "SOUTH", "EAST", "WEST", "north", "X"]
    ]

    export_orders = [
        {"id": 1, "customer_id": 10, "lines": [line("A", 2, "30.00")]},
        {"id": 2, "customer_id": 11, "lines": [line("B", 1, "12.50")]},
        {"id": 3, "customer_id": 99, "lines": [line("C", 1, "5.00")]},
    ]
    export_customers = [{"id": 10, "region": ""}, {"id": 11, "region": "WEST", "loyalty_years": 6}]
    record["export"] = [run(lambda: legacy_export.export_rows(export_orders, export_customers))]

    print(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()
