from shopline import inventory
from shopline.orders import Order, cancel


def test_total(order_dict):
    assert str(Order.from_dict(order_dict).total()) == "25.50"


def test_cancel_restocks(order_dict):
    inventory.set_stock("sku-a", 0)
    order = cancel(Order.from_dict(order_dict))
    assert order.status == "cancelled"
    assert inventory.available("sku-a") == 2
