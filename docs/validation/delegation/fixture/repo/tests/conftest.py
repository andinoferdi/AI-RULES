import pytest

from shopline import inventory


@pytest.fixture(autouse=True)
def clean_stock():
    inventory._stock.clear()
    inventory._cache.clear()
    yield
    inventory._stock.clear()
    inventory._cache.clear()


@pytest.fixture
def order_dict():
    return {
        "id": "o-1",
        "customer": "c-9",
        "created_at": "2026-11-20T10:00:00",
        "lines": [["sku-a", 2, "10.00"], ["sku-b", 1, "5.50"]],
    }
