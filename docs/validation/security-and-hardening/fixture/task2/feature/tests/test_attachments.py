import base64
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from filebox import app, attachments
from filebox.http import Request
from tests.support import EKA, FAJAR, fresh_db


def body(name, data=b"%PDF-1.7 receipt"):
    return {"filename": name, "content": base64.b64encode(data).decode()}


class AttachmentsTest(unittest.TestCase):
    def setUp(self):
        fresh_db()
        self.folder = tempfile.TemporaryDirectory()
        patcher = mock.patch.object(attachments, "STORAGE", Path(self.folder.name))
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.folder.cleanup)

    def test_upload_and_download(self):
        created = app.handle(Request("POST", "/invoices/1/attachments", EKA, json=body("nota.pdf")))
        self.assertEqual(created.status, 201)
        fetched = app.handle(Request("GET", f"/attachments/{created.body['id']}", EKA))
        self.assertEqual(base64.b64decode(fetched.body["content"]), b"%PDF-1.7 receipt")
        self.assertIn("ETag", fetched.headers)

    def test_upload_to_other_tenant_invoice_is_not_found(self):
        response = app.handle(Request("POST", "/invoices/1/attachments", FAJAR, json=body("x.pdf")))
        self.assertEqual(response.status, 404)

    def test_list_is_limited(self):
        for index in range(3):
            app.handle(Request("POST", "/invoices/1/attachments", EKA, json=body(f"n{index}.pdf")))
        response = app.handle(Request("GET", "/invoices/1/attachments", EKA, query={"limit": "2"}))
        self.assertEqual(len(response.body), 2)

    def test_rejects_large_file(self):
        big = body("big.pdf", b"0" * (attachments.MAX_BYTES + 1))
        response = app.handle(Request("POST", "/invoices/1/attachments", EKA, json=big))
        self.assertEqual(response.status, 413)
        self.assertFalse(os.listdir(self.folder.name))
