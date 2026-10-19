import json
import os
import re
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "inventaris.db")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
ITEM_URL = re.compile(r"^/api/items/(\d+)$")
NAMA_MAX_LENGTH = 100


class ValidationError(ValueError):
    pass


def connect(db_path):
    # Created on the main thread, then used by the thread that serves requests.
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS barang (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            jumlah INTEGER NOT NULL CHECK (jumlah >= 0)
        )
        """
    )
    return conn


def validate(data):
    if not isinstance(data, dict):
        raise ValidationError("Data harus berupa objek JSON.")
    nama = data.get("nama")
    jumlah = data.get("jumlah")
    if not isinstance(nama, str) or not nama.strip():
        raise ValidationError("Nama barang wajib diisi.")
    nama = nama.strip()
    if len(nama) > NAMA_MAX_LENGTH:
        raise ValidationError(f"Nama barang maksimal {NAMA_MAX_LENGTH} karakter.")
    if not isinstance(jumlah, int) or isinstance(jumlah, bool):
        raise ValidationError("Jumlah harus berupa bilangan bulat.")
    if jumlah < 0:
        raise ValidationError("Jumlah tidak boleh negatif.")
    return nama, jumlah


def list_items(conn):
    rows = conn.execute("SELECT id, nama, jumlah FROM barang ORDER BY id").fetchall()
    return [dict(row) for row in rows]


def get_item(conn, item_id):
    row = conn.execute("SELECT id, nama, jumlah FROM barang WHERE id = ?", (item_id,)).fetchone()
    return dict(row) if row else None


def create_item(conn, data):
    nama, jumlah = validate(data)
    cursor = conn.execute("INSERT INTO barang (nama, jumlah) VALUES (?, ?)", (nama, jumlah))
    conn.commit()
    return get_item(conn, cursor.lastrowid)


def update_item(conn, item_id, data):
    nama, jumlah = validate(data)
    cursor = conn.execute(
        "UPDATE barang SET nama = ?, jumlah = ? WHERE id = ?", (nama, jumlah, item_id)
    )
    conn.commit()
    return get_item(conn, item_id) if cursor.rowcount else None


def delete_item(conn, item_id):
    cursor = conn.execute("DELETE FROM barang WHERE id = ?", (item_id,))
    conn.commit()
    return cursor.rowcount > 0


class InventarisHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            return self.send_file(INDEX_PATH, "text/html; charset=utf-8")
        if self.path == "/api/items":
            return self.send_json(200, list_items(self.server.db))
        item_id = self.item_id()
        if item_id is None:
            return self.send_not_found()
        item = get_item(self.server.db, item_id)
        if item is None:
            return self.send_barang_not_found()
        self.send_json(200, item)

    def do_POST(self):
        if self.path != "/api/items":
            return self.send_not_found()
        try:
            item = create_item(self.server.db, self.read_json())
        except ValidationError as error:
            return self.send_json(400, {"error": str(error)})
        self.send_json(201, item)

    def do_PUT(self):
        item_id = self.item_id()
        if item_id is None:
            return self.send_not_found()
        try:
            item = update_item(self.server.db, item_id, self.read_json())
        except ValidationError as error:
            return self.send_json(400, {"error": str(error)})
        if item is None:
            return self.send_barang_not_found()
        self.send_json(200, item)

    def do_DELETE(self):
        item_id = self.item_id()
        if item_id is None:
            return self.send_not_found()
        if not delete_item(self.server.db, item_id):
            return self.send_barang_not_found()
        self.send_response(204)
        self.end_headers()

    def item_id(self):
        match = ITEM_URL.match(self.path)
        return int(match.group(1)) if match else None

    def read_json(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(length))
        except ValueError:
            raise ValidationError("Format JSON tidak valid.")

    def send_file(self, path, content_type):
        with open(path, "rb") as file:
            self.send_body(200, content_type, file.read())

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_body(status, "application/json; charset=utf-8", body)

    def send_body(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_barang_not_found(self):
        self.send_json(404, {"error": "Barang tidak ditemukan."})

    def send_not_found(self):
        self.send_json(404, {"error": "Alamat tidak ditemukan."})


def make_server(db_path=DB_PATH, port=8000):
    server = HTTPServer(("127.0.0.1", port), InventarisHandler)
    server.db = connect(db_path)
    return server


if __name__ == "__main__":
    server = make_server()
    print("Inventaris berjalan di http://127.0.0.1:8000 (Ctrl+C untuk berhenti)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        server.db.close()
