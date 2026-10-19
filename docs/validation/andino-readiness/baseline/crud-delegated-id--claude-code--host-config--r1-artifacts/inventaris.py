"""CRUD inventaris sederhana (nama barang, jumlah) dengan penyimpanan file JSON."""

import argparse
import json
import os
import sys


class Inventaris:
    def __init__(self, path="inventaris.json"):
        self.path = path
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"next_id": 1, "barang": []}
        self._next_id = data["next_id"]
        self._barang = data["barang"]

    def _simpan(self):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"next_id": self._next_id, "barang": self._barang}, f,
                      ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)

    @staticmethod
    def _cek_nama(nama):
        nama = nama.strip()
        if not nama:
            raise ValueError("Nama barang tidak boleh kosong")
        return nama

    @staticmethod
    def _cek_jumlah(jumlah):
        if not isinstance(jumlah, int) or jumlah < 0:
            raise ValueError("Jumlah harus bilangan bulat >= 0")
        return jumlah

    def _cari(self, id_):
        for item in self._barang:
            if item["id"] == id_:
                return item
        raise KeyError(id_)

    def tambah(self, nama, jumlah):
        item = {"id": self._next_id, "nama": self._cek_nama(nama),
                "jumlah": self._cek_jumlah(jumlah)}
        self._barang.append(item)
        self._next_id += 1
        self._simpan()
        return dict(item)

    def lihat(self):
        return [dict(item) for item in self._barang]

    def ubah(self, id_, nama=None, jumlah=None):
        item = self._cari(id_)
        nama_baru = self._cek_nama(nama) if nama is not None else item["nama"]
        jumlah_baru = self._cek_jumlah(jumlah) if jumlah is not None else item["jumlah"]
        item["nama"], item["jumlah"] = nama_baru, jumlah_baru
        self._simpan()
        return dict(item)

    def hapus(self, id_):
        self._barang.remove(self._cari(id_))
        self._simpan()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inventaris sederhana")
    parser.add_argument("--data", default="inventaris.json", help="lokasi file data")
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
    inv = Inventaris(args.data)

    try:
        if args.perintah == "tambah":
            item = inv.tambah(args.nama, args.jumlah)
            print(f"Ditambahkan: #{item['id']} {item['nama']} ({item['jumlah']})")
        elif args.perintah == "lihat":
            barang = inv.lihat()
            if not barang:
                print("Inventaris kosong.")
            for item in barang:
                print(f"{item['id']:>4}  {item['nama']:<30} {item['jumlah']:>6}")
        elif args.perintah == "ubah":
            if args.nama is None and args.jumlah is None:
                parser.error("isi --nama dan/atau --jumlah")
            item = inv.ubah(args.id, nama=args.nama, jumlah=args.jumlah)
            print(f"Diubah: #{item['id']} {item['nama']} ({item['jumlah']})")
        elif args.perintah == "hapus":
            inv.hapus(args.id)
            print(f"Dihapus: #{args.id}")
    except KeyError:
        print(f"Barang dengan id {args.id} tidak ditemukan", file=sys.stderr)
        return 1
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
