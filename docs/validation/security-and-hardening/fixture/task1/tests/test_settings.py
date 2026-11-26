import unittest

from hookdesk import app, store
from hookdesk.http import Request


class WebhookSettingsTest(unittest.TestCase):
    def setUp(self):
        store.reset()

    def test_admin_sets_url(self):
        response = app.handle(Request("PUT", "/tenants/t-acme/settings/webhook", "u-bagas",
                                      {"url": "https://hooks.acme.example/v2"}))
        self.assertEqual(response.status, 200)
        self.assertEqual(store.tenant("t-acme")["webhook"]["url"], "https://hooks.acme.example/v2")

    def test_other_tenant_gets_not_found(self):
        response = app.handle(Request("PUT", "/tenants/t-acme/settings/webhook", "u-dimas",
                                      {"url": "https://example.net/x"}))
        self.assertEqual(response.status, 404)

    def test_rejects_non_http_scheme(self):
        response = app.handle(Request("PUT", "/tenants/t-acme/settings/webhook", "u-ayu",
                                      {"url": "file:///etc/passwd"}))
        self.assertEqual(response.status, 422)

    def test_member_reads_configuration(self):
        response = app.handle(Request("GET", "/tenants/t-acme/settings/webhook", "u-citra"))
        self.assertEqual(response.status, 200)
        self.assertTrue(response.body["configured"])


class InvoicesTest(unittest.TestCase):
    def test_lists_only_own_tenant(self):
        store.reset()
        response = app.handle(Request("GET", "/tenants/t-acme/invoices", "u-citra"))
        self.assertEqual([inv["id"] for inv in response.body["invoices"]], ["inv-1001"])
