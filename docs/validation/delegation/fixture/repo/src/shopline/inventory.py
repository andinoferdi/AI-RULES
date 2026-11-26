import time

_stock: dict[str, int] = {}
_cache: dict[str, tuple[float, int]] = {}
CACHE_SECONDS = 2.0


class OutOfStock(Exception):
    pass


def set_stock(sku: str, quantity: int) -> None:
    _stock[sku] = quantity
    _cache.pop(sku, None)


def available(sku: str) -> int:
    cached = _cache.get(sku)
    if cached and time.monotonic() - cached[0] < CACHE_SECONDS:
        return cached[1]
    value = _stock.get(sku, 0)
    _cache[sku] = (time.monotonic(), value)
    return value


def reserve(sku: str, quantity: int) -> None:
    if available(sku) < quantity:
        raise OutOfStock(sku)
    _stock[sku] = _stock.get(sku, 0) - quantity


def restock(sku: str, quantity: int) -> None:
    _stock[sku] = _stock.get(sku, 0) + quantity
    _cache.pop(sku, None)
