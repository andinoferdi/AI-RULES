import threading

from shopline import inventory


def test_reserve_reduces_stock():
    inventory.set_stock("sku-a", 5)
    inventory.reserve("sku-a", 2)
    assert inventory._stock["sku-a"] == 3


def test_concurrent_reserve():
    inventory.set_stock("sku-a", 5)
    successes = []

    def worker():
        try:
            inventory.reserve("sku-a", 1)
            successes.append(1)
        except inventory.OutOfStock:
            pass

    threads = [threading.Thread(target=worker) for _ in range(20)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(successes) == 5
    assert inventory._stock["sku-a"] == 0
