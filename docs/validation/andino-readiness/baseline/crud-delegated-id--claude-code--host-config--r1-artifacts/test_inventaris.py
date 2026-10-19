import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from inventaris import Inventaris, main


class InventarisTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "data.json")
        self.inv = Inventaris(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_tambah_lalu_lihat(self):
        self.inv.tambah("Pulpen", 10)
        self.inv.tambah("Buku", 3)
        self.assertEqual(
            self.inv.lihat(),
            [{"id": 1, "nama": "Pulpen", "jumlah": 10},
             {"id": 2, "nama": "Buku", "jumlah": 3}],
        )

    def test_data_tersimpan_ke_file(self):
        self.inv.tambah("Pulpen", 10)
        self.assertEqual(Inventaris(self.path).lihat()[0]["nama"], "Pulpen")

    def test_ubah_jumlah_saja(self):
        self.inv.tambah("Pulpen", 10)
        self.inv.ubah(1, jumlah=7)
        self.assertEqual(self.inv.lihat(), [{"id": 1, "nama": "Pulpen", "jumlah": 7}])

    def test_ubah_nama_saja(self):
        self.inv.tambah("Pulpen", 10)
        self.inv.ubah(1, nama="Pensil")
        self.assertEqual(self.inv.lihat(), [{"id": 1, "nama": "Pensil", "jumlah": 10}])

    def test_hapus(self):
        self.inv.tambah("Pulpen", 10)
        self.inv.tambah("Buku", 3)
        self.inv.hapus(1)
        self.assertEqual(self.inv.lihat(), [{"id": 2, "nama": "Buku", "jumlah": 3}])

    def test_id_tidak_dipakai_ulang_setelah_hapus(self):
        self.inv.tambah("Pulpen", 10)
        self.inv.hapus(1)
        self.assertEqual(self.inv.tambah("Buku", 3)["id"], 2)

    def test_id_tidak_ada(self):
        with self.assertRaises(KeyError):
            self.inv.ubah(99, jumlah=1)
        with self.assertRaises(KeyError):
            self.inv.hapus(99)

    def test_validasi_input(self):
        with self.assertRaises(ValueError):
            self.inv.tambah("  ", 1)
        with self.assertRaises(ValueError):
            self.inv.tambah("Pulpen", -1)
        self.inv.tambah("Pulpen", 1)
        with self.assertRaises(ValueError):
            self.inv.ubah(1, jumlah=-5)

    def test_cli_tambah_dan_lihat(self):
        main(["--data", self.path, "tambah", "Pulpen", "10"])
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["--data", self.path, "lihat"])
        self.assertEqual(code, 0)
        self.assertIn("Pulpen", out.getvalue())
        self.assertIn("10", out.getvalue())

    def test_cli_error_id_tidak_ada(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["--data", self.path, "hapus", "5"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
