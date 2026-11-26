"""Read product feeds (CSV with sku, name, variant, price)."""
import csv
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    variant: str
    price: Decimal
    source: str  # "primary" or "partner"


def read_feed(path, source: str):
    with open(path, newline="", encoding="utf-8") as handle:
        return [
            Product(
                sku=row["sku"].strip(),
                name=row["name"].strip(),
                variant=row["variant"].strip(),
                price=Decimal(row["price"].strip()),
                source=source,
            )
            for row in csv.DictReader(handle)
        ]
