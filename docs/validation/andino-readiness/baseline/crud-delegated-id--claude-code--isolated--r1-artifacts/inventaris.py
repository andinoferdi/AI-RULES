"""CRUD inventaris sederhana (nama barang, jumlah) dengan SQLite."""

import argparse
import sqlite3
import sys


class Inventaris:
    def __init__(self, path="inventaris.db"):
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS barang ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "nama TEXT NOT NULL, "
            "jumlah INTEGER NOT NULL CHECK (jumlah >= 0))"
        )
        self.conn.commit()

    @staticmethod
    def _cek(nama=None, jumlah=None):
        if nama is not None and not nama.strip():
            raise ValueError("Nama barang tidak boleh kosong.")
        if jumlah is not None and jumlah < 0:
            raise ValueError("Jumlah tidak boleh negatif.")

    def tambah(self, nama, jumlah):
        self._cek(nama, jumlah)
        cur = self.conn.execute(
            "INSERT INTO barang (nama, jumlah) VALUES (?, ?)", (nama.strip(), jumlah)
        )
        self.conn.commit()
        return cur.lastrowid

    def lihat(self):
        return self.conn.execute("SELECT id, nama, jumlah FROM barang ORDER BY id").fetchall()

    def ubah(self, id_barang, nama=None, jumlah=None):
        self._cek(nama, jumlah)
        cur = self.conn.execute(
            "UPDATE barang SET nama = COALESCE(?, nama), jumlah = COALESCE(?, jumlah) "
            "WHERE id = ?",
            (nama.strip() if nama is not None else None, jumlah, id_barang),
        )
        self.conn.commit()
        return cur.rowcount > 0

    def hapus(self, id_barang):
        cur = self.conn.execute("DELETE FROM barang WHERE id = ?", (id_barang,))
        self.conn.commit()
        return cur.rowcount > 0

    def close(self):
        self.conn.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inventaris barang sederhana")
    parser.add_argument("--db", default="inventaris.db", help="lokasi file database")
    sub = parser.add_subparsers(dest="perintah", required=True)

    p = sub.add_parser("tambah", help="tambah barang")
    p.add_argument("nama")
    p.add_argument("jumlah", type=int)

    sub.add_parser("lihat", help="tampilkan semua barang")

    p = sub.add_parser("ubah", help="ubah nama dan/atau jumlah barang")
    p.add_argument("id", type=int)
    p.add_argument("--nama")
    p.add_argument("--jumlah", type=int)

    p = sub.add_parser("hapus", help="hapus barang")
    p.add_argument("id", type=int)

    args = parser.parse_args(argv)
    inv = Inventaris(args.db)
    try:
        if args.perintah == "tambah":
            id_baru = inv.tambah(args.nama, args.jumlah)
            print(f"Barang ditambahkan dengan ID {id_baru}.")
        elif args.perintah == "lihat":
            rows = inv.lihat()
            if not rows:
                print("Inventaris kosong.")
            else:
                print(f"{'ID':>4}  {'Nama':<30}  {'Jumlah':>6}")
                for id_barang, nama, jumlah in rows:
                    print(f"{id_barang:>4}  {nama:<30}  {jumlah:>6}")
        elif args.perintah == "ubah":
            if args.nama is None and args.jumlah is None:
                print("Isi --nama dan/atau --jumlah.")
                return 2
            if not inv.ubah(args.id, args.nama, args.jumlah):
                print(f"Barang dengan ID {args.id} tidak ditemukan.")
                return 1
            print(f"Barang ID {args.id} diperbarui.")
        elif args.perintah == "hapus":
            if not inv.hapus(args.id):
                print(f"Barang dengan ID {args.id} tidak ditemukan.")
                return 1
            print(f"Barang ID {args.id} dihapus.")
    except ValueError as e:
        print(f"Error: {e}")
        return 2
    finally:
        inv.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
