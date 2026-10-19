# CRUD Buku

Contoh aplikasi CRUD (Create, Read, Update, Delete) sederhana. Tidak ada library tambahan: cukup Node.js 18 ke atas.

## Cara menjalankan

1. Pasang Node.js 18 atau lebih baru.
2. Buka terminal di folder ini.
3. Jalankan `npm start`.
4. Buka `http://localhost:3000` di browser.

Untuk menjalankan tes otomatis, jalankan `npm test`.

## Alur kerjanya

Halaman di `public/` mengirim request ke server dengan `fetch`. Server (`server.js`) membaca request itu, lalu memanggil fungsi di `books.js` untuk membaca atau menulis data di `data/books.json`. File `data/books.json` dibuat otomatis saat pertama kali ada data.

| Operasi | Di halaman | Request HTTP | Endpoint |
| --- | --- | --- | --- |
| Create | Tombol "Tambah" | `POST` | `/api/books` |
| Read | Tabel daftar buku | `GET` | `/api/books` |
| Read satu buku | Belum dipakai halaman, tersedia di API | `GET` | `/api/books/:id` |
| Update | Tombol "Simpan" saat mode ubah | `PUT` | `/api/books/:id` |
| Delete | Tombol "Hapus" | `DELETE` | `/api/books/:id` |

## Struktur folder

- `server.js`: server HTTP, routing API, dan penyajian file statis.
- `books.js`: validasi input dan operasi data ke file JSON.
- `public/index.html`: struktur halaman.
- `public/app.js`: logika halaman, termasuk memanggil API dan menampilkan tabel.
- `public/style.css`: tampilan.
- `test/books.test.js`: tes API dengan `node:test` bawaan Node.js.

## Batasan

Data disimpan di satu file JSON, jadi cocok untuk belajar dan data kecil. Untuk aplikasi sungguhan, ganti `books.js` dengan database seperti SQLite atau PostgreSQL. Bagian `server.js` dan `public/` bisa tetap dipakai.
