import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TMP = Path(tempfile.mkdtemp(prefix="payments-test-"))
os.environ["PAYMENTS_VAR"] = str(TMP)
sys.path.insert(0, str(ROOT))

from payments import api, provider, queue, store, worker  # noqa: E402


class WorkerTest(unittest.TestCase):
    def setUp(self):
        shutil.rmtree(TMP, ignore_errors=True)
        TMP.mkdir(parents=True)
        shutil.copy(ROOT / "data" / "invoices.json", TMP / "invoices.json")
        provider._attempts.clear()

    def run_one(self, invoice_id):
        queue.enqueue(invoice_id)
        return dict(worker.run())[invoice_id]

    def test_success_after_timeout(self):
        self.assertEqual(self.run_one("inv-101"), "paid")
        self.assertEqual(provider._attempts["inv-101"], 2)

    def test_decline_is_not_retried(self):
        self.assertEqual(self.run_one("inv-102"), "failed")
        self.assertEqual(provider._attempts["inv-102"], 1)

    def test_gives_up_after_three_attempts(self):
        self.assertEqual(self.run_one("inv-103"), "failed")
        self.assertEqual(provider._attempts["inv-103"], 3)

    def test_replay_refuses_paid_invoice(self):
        self.assertEqual(api.handle_replay({}, "inv-105")[0], 409)
        self.assertEqual(queue.depth(), 0)

    def test_replay_enqueues(self):
        self.assertEqual(api.handle_replay({}, "inv-103")[0], 202)
        self.assertEqual(queue.depth(), 1)
        self.assertEqual(store.load()["inv-103"]["status"], "due")


if __name__ == "__main__":
    unittest.main()
