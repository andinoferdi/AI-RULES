import io
import unittest
from contextlib import redirect_stdout

from inventaris import Inventaris, main


class InventarisTest(unittest.TestCase):
    def setUp(self):
        self.inv = Inventaris(":memory:")

    def test_tambah_lalu_lihat(self):
        id_baru = self.inv.tambah("Pulpen", 10)
        self.assertEqual(self.inv.lihat(), [(id_baru, "Pulpen", 10)])

    def test_ubah_nama_dan_jumlah(self):
        id_baru = self.inv.tambah("Pulpen", 10)
        self.assertTrue(self.inv.ubah(id_baru, nama="Pensil", jumlah=3))
        self.assertEqual(self.inv.lihat(), [(id_baru, "Pensil", 3)])

    def test_ubah_sebagian_hanya_jumlah(self):
        id_baru = self.inv.tambah("Pulpen", 10)
        self.inv.ubah(id_baru, jumlah=7)
        self.assertEqual(self.inv.lihat(), [(id_baru, "Pulpen", 7)])

    def test_hapus(self):
        a = self.inv.tambah("Pulpen", 10)
        b = self.inv.tambah("Buku", 2)
        self.assertTrue(self.inv.hapus(a))
        self.assertEqual(self.inv.lihat(), [(b, "Buku", 2)])

    def test_id_tidak_ada(self):
        self.assertFalse(self.inv.ubah(99, jumlah=1))
        self.assertFalse(self.inv.hapus(99))

    def test_validasi_input(self):
        with self.assertRaises(ValueError):
            self.inv.tambah("  ", 1)
        with self.assertRaises(ValueError):
            self.inv.tambah("Pulpen", -1)
        id_baru = self.inv.tambah("Pulpen", 1)
        with self.assertRaises(ValueError):
            self.inv.ubah(id_baru, jumlah=-5)


class CliTest(unittest.TestCase):
    def jalankan(self, *argv):
        out = io.StringIO()
        with redirect_stdout(out):
            kode = main(["--db", self.db, *argv])
        return kode, out.getvalue()

    def setUp(self):
        import os
        import tempfile

        fd, self.db = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        self.addCleanup(os.remove, self.db)

    def test_alur_crud_lewat_cli(self):
        self.assertEqual(self.jalankan("tambah", "Pulpen", "10")[0], 0)
        kode, out = self.jalankan("lihat")
        self.assertIn("Pulpen", out)
        self.assertIn("10", out)

        self.assertEqual(self.jalankan("ubah", "1", "--jumlah", "4")[0], 0)
        self.assertIn("4", self.jalankan("lihat")[1])

        self.assertEqual(self.jalankan("hapus", "1")[0], 0)
        self.assertIn("kosong", self.jalankan("lihat")[1])

    def test_cli_id_tidak_ada_mengembalikan_kode_error(self):
        kode, out = self.jalankan("hapus", "42")
        self.assertEqual(kode, 1)
        self.assertIn("tidak ditemukan", out)


if __name__ == "__main__":
    unittest.main()
