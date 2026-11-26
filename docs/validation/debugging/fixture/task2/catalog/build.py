"""Build the storefront catalog from the primary feed and a partner feed."""
import argparse
import hashlib
import sys
from decimal import Decimal
from pathlib import Path

from .feed import read_feed
from .merge import merge_feeds
from .pricing import apply_markup

ROOT = Path(__file__).resolve().parents[1]


def checksum(products) -> str:
    digest = hashlib.sha256()
    for product in products:
        digest.update(f"{product.sku}|{product.variant}|{product.price}\n".encode("utf-8"))
    return digest.hexdigest()[:16]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary", default=str(ROOT / "data" / "primary.csv"))
    parser.add_argument("--feed", required=True, help="partner feed CSV")
    parser.add_argument("--markup", default="0.12")
    args = parser.parse_args(argv)

    products = merge_feeds(read_feed(args.primary, "primary"), read_feed(args.feed, "partner"))
    products = apply_markup(products, Decimal(args.markup))
    print(f"products={len(products)} checksum={checksum(products)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
