from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from shopline import inventory


@dataclass
class Order:
    id: str
    customer: str
    created_at: datetime
    currency: str
    lines: list[tuple[str, int, Decimal]] = field(default_factory=list)
    status: str = "open"

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        return cls(
            id=data["id"],
            customer=data["customer"],
            created_at=datetime.fromisoformat(data["created_at"]),
            currency=data["currency"],
            lines=[(sku, qty, Decimal(price)) for sku, qty, price in data["lines"]],
            status=data.get("status", "open"),
        )

    def total(self) -> Decimal:
        return sum((qty * price for _, qty, price in self.lines), Decimal("0"))


def cancel(order: Order) -> Order:
    for sku, qty, _ in order.lines:
        inventory.restock(sku, qty)
    order.status = "cancelled"
    return order
