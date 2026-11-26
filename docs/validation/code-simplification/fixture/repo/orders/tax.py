"""Sales tax by region.

The steps below follow the Regional Sales Tax Schedule (RSTS-2024, section 4), one step per
numbered paragraph, so the finance auditors can compare them line by line.
"""
from decimal import Decimal

from orders.errors import PricingError

# RSTS-2024 section 4.1: standard rate per region.
STANDARD_RATES = {
    "NORTH": Decimal("0.08"),
    "SOUTH": Decimal("0.06"),
    "EAST": Decimal("0.07"),
    "WEST": Decimal("0.05"),
}

# RSTS-2024 section 4.3: the reduced rate applies to the part of the amount above the threshold.
REDUCED_RATE = Decimal("0.02")
REDUCED_RATE_THRESHOLD = Decimal("1000")


def tax_for_region(amount, region):
    """Return the sales tax for `amount` in `region`, before rounding."""
    # 4.1 Look up the standard rate.
    if region not in STANDARD_RATES:
        raise PricingError("unknown tax region: %s" % region)
    standard_rate = STANDARD_RATES[region]

    # 4.2 Amounts at or below zero carry no tax.
    if amount <= 0:
        return Decimal("0")

    # 4.3 The standard rate applies up to the threshold; the reduced rate applies above it.
    taxed_at_standard = min(amount, REDUCED_RATE_THRESHOLD)
    taxed_at_reduced = amount - taxed_at_standard

    # 4.4 The tax is the sum of both parts.
    return taxed_at_standard * standard_rate + taxed_at_reduced * REDUCED_RATE
