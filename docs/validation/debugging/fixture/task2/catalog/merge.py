"""Merge feeds into one catalog."""


def dedupe_variants(products):
    """Keep the first product per (SKU, variant). SKUs compare case-insensitively."""
    seen = []
    kept = []
    for product in products:
        key = (product.sku.casefold(), product.variant)
        if key in seen:
            continue
        seen.append(key)
        kept.append(product)
    return kept


def merge_feeds(primary, partner):
    """Primary products come first, so they win over partner duplicates."""
    return dedupe_variants(list(primary) + list(partner))
