import unittest

from filebox import app
from filebox.http import Request
from tests.support import EKA, FAJAR, fresh_db


class InvoicesTest(unittest.TestCase):
    def setUp(self):
        fresh_db()

    def test_lists_own_tenant(self):
        response = app.handle(Request("GET", "/invoices", EKA))
        self.assertEqual([row["number"] for row in response.body], ["KOPI-2026-031"])

    def test_other_tenant_invoice_is_not_found(self):
        response = app.handle(Request("GET", "/invoices/1", FAJAR))
        self.assertEqual(response.status, 404)

    def test_requires_token(self):
        self.assertEqual(app.handle(Request("GET", "/invoices")).status, 401)
