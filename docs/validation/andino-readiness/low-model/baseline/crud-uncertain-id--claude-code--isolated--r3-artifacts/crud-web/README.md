# Daftar Buku

Aplikasi CRUD sederhana untuk menambah, melihat, mengubah, dan menghapus data buku. Tidak ada paket tambahan yang perlu dipasang. Cukup Node.js 18 atau lebih baru.

## Menjalankan

1. Buka folder `crud-web` di terminal.
2. Jalankan `npm start`.
3. Buka http://localhost:3000 di browser.

Data disimpan di `data/books.json`. File dan folder itu dibuat otomatis saat buku pertama ditambahkan.

## Menjalankan tes

Jalankan `npm test` dari folder `crud-web`.

## Struktur

- `src/validate.js`: aturan isian untuk judul, penulis, dan tahun.
- `src/store.js`: membaca dan menulis data ke file JSON.
- `src/server.js`: server HTTP, endpoint API, dan pelayanan file di `public/`.
- `public/`: halaman, skrip browser, dan gaya tampilan.
- `test/`: tes untuk validasi, penyimpanan, dan API.

## Endpoint API

| Method | Alamat | Fungsi | Status sukses |
| --- | --- | --- | --- |
| GET | /api/books | Daftar semua buku | 200 |
| GET | /api/books/:id | Satu buku | 200 |
| POST | /api/books | Tambah buku | 201 |
| PUT | /api/books/:id | Ubah buku | 200 |
| DELETE | /api/books/:id | Hapus buku | 204 |

Data yang tidak valid dijawab dengan 422 dan daftar error per field. ID yang tidak ada dijawab dengan 404.
