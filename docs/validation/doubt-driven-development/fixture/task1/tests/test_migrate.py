import json
import tempfile
import unittest
from pathlib import Path

from wallet.migrate import migrate
from wallet.store import Store


def make_store(folder, balances):
    path = Path(folder) / "accounts.json"
    accounts = [{"id": f"A-{i}", "owner": f"user{i}", "balance": b} for i, b in enumerate(balances)]
    path.write_text(json.dumps({"schema_version": 1, "accounts": accounts}), encoding="utf-8")
    return Store(path)


class MigrateTest(unittest.TestCase):
    def test_converts_rupiah_to_sen(self):
        with tempfile.TemporaryDirectory() as folder:
            store = make_store(folder, [1500, 0, 250000])
            self.assertEqual(migrate(store), 3)
            self.assertEqual([a["balance"] for a in store.load_accounts()], [150000, 0, 25000000])
            self.assertEqual(store.schema_version(), 2)

    def test_second_run_is_noop(self):
        with tempfile.TemporaryDirectory() as folder:
            store = make_store(folder, [1500, 2500])
            migrate(store)
            self.assertEqual(migrate(store), 0)
            self.assertEqual([a["balance"] for a in store.load_accounts()], [150000, 250000])

    def test_small_batches(self):
        with tempfile.TemporaryDirectory() as folder:
            store = make_store(folder, [1, 2, 3, 4, 5])
            self.assertEqual(migrate(store, batch_size=2), 5)
            self.assertEqual([a["balance"] for a in store.load_accounts()], [100, 200, 300, 400, 500])


if __name__ == "__main__":
    unittest.main()
