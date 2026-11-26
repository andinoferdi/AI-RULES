"""Order pricing."""
import json
import math
from decimal import Decimal, ROUND_HALF_UP

from orders.errors import PricingError
from orders.tax import tax_for_region


class DiscountStrategy:
    def apply(self, subtotal, customer):
        raise NotImplementedError


class LoyaltyDiscountStrategy(DiscountStrategy):
    def apply(self, subtotal, customer):
        if customer.get("loyalty_years", 0) >= 5:
            return subtotal * Decimal("0.10")
        else:
            return Decimal("0")


class DiscountStrategyFactory:
    def create(self, kind):
        if kind == "loyalty":
            return LoyaltyDiscountStrategy()
        raise PricingError("unknown discount kind: %s" % kind)


def price_order(order, customer, audit, include_tax=True):
    data = order
    if data is not None:
        if "lines" in data and len(data["lines"]) > 0:
            tmp = Decimal("0")
            # loop over the lines
            for l in data["lines"]:
                if l["qty"] is None:
                    raise PricingError("line %s has no quantity" % l["sku"])
                else:
                    if l["qty"] < 0:
                        raise PricingError("line %s has a negative quantity" % l["sku"])
                tmp = tmp + Decimal(str(l["unit_price"])) * l["qty"]
            audit.append(("subtotal", tmp))

            # Free shipping is decided on the subtotal before discounts: the 2025 campaign
            # terms promise it for any basket of 50 or more.
            if tmp >= Decimal("50"):
                ship = Decimal("0")
            else:
                ship = Decimal("4.99")

            f = DiscountStrategyFactory()
            s = f.create("loyalty")
            disc = s.apply(tmp, customer)
            audit.append(("discount", disc))
            res = tmp - disc + ship

            if include_tax == True:
                region = customer.get("region", "").strip().upper()
                if region == "":
                    raise PricingError("customer has no region")
                else:
                    t = tax_for_region(res, region)
                    audit.append(("tax", t))
                    res = res + t
            # old flat-rate tax, replaced in 2024
            # res = res * Decimal("1.07")

            if res < 0:
                res = Decimal("0")

            # simplify-ignore-start
            # Finance-audited rounding (FIN-88): auditors diff this block against the spec.
            cents = (res * 100).to_integral_value(rounding=ROUND_HALF_UP)
            res = cents / 100
            # simplify-ignore-end
            audit.append(("total", res))
            return res
        else:
            raise PricingError("order has no lines")
    else:
        raise PricingError("order is missing")
