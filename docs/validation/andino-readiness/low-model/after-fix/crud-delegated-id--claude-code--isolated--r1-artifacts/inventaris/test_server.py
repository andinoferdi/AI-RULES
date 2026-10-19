import http.client
import json
import os
import shutil
import tempfile
import threading
import unittest

from server import connect, list_items, make_server


class InventarisApiTest(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmp_dir, "test.db")
        self.server = make_server(self.db_path, port=0)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
        self.server.db.close()
        shutil.rmtree(self.tmp_dir)

    def request(self, method, path, body=None, raw=None):
        if raw is None and body is not None:
            raw = json.dumps(body).encode("utf-8")
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request(method, path, body=raw, headers={"Content-Type": "application/json"})
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return response.status, data

    def call(self, method, path, body=None, raw=None):
        status, data = self.request(method, path, body, raw)
        return status, (json.loads(data) if data else None)

    def test_tambah_lalu_lihat(self):
        status, item = self.call("POST", "/api/items", {"nama": "  Kertas A4  ", "jumlah": 10})

        self.assertEqual(status, 201)
        self.assertEqual(item["nama"], "Kertas A4")
        self.assertEqual(item["jumlah"], 10)
        status, items = self.call("GET", "/api/items")
        self.assertEqual(status, 200)
        self.assertEqual(items, [item])

    def test_jumlah_nol_diterima(self):
        status, item = self.call("POST", "/api/items", {"nama": "Pensil", "jumlah": 0})

        self.assertEqual(status, 201)
        self.assertEqual(item["jumlah"], 0)

    def test_data_tidak_valid_ditolak(self):
        cases = [
            {"nama": "", "jumlah": 1},
            {"nama": "   ", "jumlah": 1},
            {"nama": "x" * 101, "jumlah": 1},
            {"nama": "Pensil", "jumlah": -1},
            {"nama": "Pensil", "jumlah": 1.5},
            {"nama": "Pensil", "jumlah": "5"},
            {"nama": "Pensil", "jumlah": True},
            {"nama": "Pensil"},
        ]
        for body in cases:
            with self.subTest(body=body):
                status, data = self.call("POST", "/api/items", body)
                self.assertEqual(status, 400)
                self.assertIn("error", data)
        _, items = self.call("GET", "/api/items")
        self.assertEqual(items, [])

    def test_json_rusak_ditolak(self):
        status, data = self.call("POST", "/api/items", raw=b"{nama:")

        self.assertEqual(status, 400)
        self.assertIn("error", data)

    def test_perubahan_tersimpan_ke_database(self):
        self.call("POST", "/api/items", {"nama": "Pensil", "jumlah": 5})

        other = connect(self.db_path)
        try:
            self.assertEqual([item["nama"] for item in list_items(other)], ["Pensil"])
        finally:
            other.close()

    def test_ubah_barang(self):
        _, item = self.call("POST", "/api/items", {"nama": "Pensil", "jumlah": 5})

        status, updated = self.call("PUT", f"/api/items/{item['id']}", {"nama": "Pensil 2B", "jumlah": 0})

        self.assertEqual(status, 200)
        self.assertEqual(updated, {"id": item["id"], "nama": "Pensil 2B", "jumlah": 0})
        _, items = self.call("GET", "/api/items")
        self.assertEqual(items, [updated])

    def test_ubah_dengan_data_tidak_valid_tidak_mengubah_barang(self):
        _, item = self.call("POST", "/api/items", {"nama": "Pensil", "jumlah": 5})

        status, _ = self.call("PUT", f"/api/items/{item['id']}", {"nama": "Pensil", "jumlah": -3})

        self.assertEqual(status, 400)
        _, current = self.call("GET", f"/api/items/{item['id']}")
        self.assertEqual(current, item)

    def test_hapus_barang(self):
        _, item = self.call("POST", "/api/items", {"nama": "Pensil", "jumlah": 5})

        status, _ = self.call("DELETE", f"/api/items/{item['id']}")

        self.assertEqual(status, 204)
        status, data = self.call("GET", f"/api/items/{item['id']}")
        self.assertEqual(status, 404)
        self.assertIn("error", data)

    def test_barang_tidak_ada_mengembalikan_404(self):
        for method, body in [("GET", None), ("PUT", {"nama": "Pensil", "jumlah": 1}), ("DELETE", None)]:
            with self.subTest(method=method):
                status, data = self.call(method, "/api/items/999", body)
                self.assertEqual(status, 404)
                self.assertIn("error", data)

    def test_halaman_utama_dan_rute_tidak_dikenal(self):
        status, data = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn(b"Inventaris Barang", data)

        status, _ = self.request("GET", "/tidak-ada")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
