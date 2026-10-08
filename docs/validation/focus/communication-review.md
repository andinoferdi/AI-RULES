# Focus communication review

Date: 2026-10-08. Method: manual application and review by the implementing agent
against `evals/focus.json`. These are authored smoke examples, not fresh-host model
transcripts. They support a qualitative review only. Autonomous loading and
cross-host model behavior remain NOT_VERIFIED; installer tests do not prove them.

## Short answer

Input: Apa command Git untuk melihat branch aktif?

Response:

```sh
git branch --show-current
```

Review: direct command, no mandatory list, recap or next-action footer.

## Debugging with incomplete evidence

Input: Login memberi 401. Apakah database rusak? Hanya ada log HTTP 401.

Response:

HTTP 401 belum membuktikan database rusak. Periksa apakah request membawa
kredensial yang diminta endpoint, lalu cocokkan dengan log autentikasi server.
Tanpa trace tersebut, penyebabnya belum terkonfirmasi.

Review: retains uncertainty; one useful diagnostic direction; no invented fix,
execution or confirmed cause. Does not dump unrelated database repair advice.

## Coding completion

Input facts: src/parser.py now returns [] on empty input; pytest tests/test_parser.py
passed six tests; integration tests were not run.

Response:

`src/parser.py` kini mengembalikan `[]` untuk input kosong. Verifikasi:
`pytest tests/test_parser.py` lulus 6 test. Integration test belum dijalankan.

Review: preserves changed behavior, file, command, result and verification limit.
The facts are supplied fixture facts, not claims that this repository has a parser.

## Detailed explanation

Input: Jelaskan optimistic dan pessimistic locking secara rinci, termasuk race
condition, contoh transaksi, deadlock, retry, dan trade-off.

Response:

Optimistic locking memeriksa apakah data berubah sebelum pembaruan disimpan.
Pessimistic locking mengunci data selama transaksi agar perubahan yang bertabrakan
menunggu. Pilihannya bergantung pada frekuensi konflik, biaya mengulang pekerjaan,
dan perilaku database yang digunakan.

Misalnya, dua transaksi membaca stok 10. Transaksi A menjual 3 unit, sedangkan B
menjual 4 unit. Jika keduanya menghitung dari angka lama lalu menulis hasil secara
langsung, A dapat menulis 7 dan B menimpanya dengan 6. Stok seharusnya 3. Inilah
contoh lost update; detail kemungkinannya bergantung pada query dan isolation level.

### Optimistic locking

Simpan versi bersama data. Kedua transaksi membaca `version = 5`. Saat A
memperbarui stok, ia juga mensyaratkan versi lama:

```sql
UPDATE inventory
SET stock = 7, version = version + 1
WHERE id = 42 AND version = 5;
```

A memeriksa jumlah baris yang berubah. Satu baris berarti perubahan dengan versi
tersebut diterima. B yang mencoba memperbarui dengan versi 5 setelahnya mendapat
nol baris, sehingga tidak boleh menganggap perubahan berhasil. Nol baris juga bisa
berarti baris sudah dihapus; aplikasi perlu membedakan keadaan yang relevan.

B membaca ulang data, memeriksa kembali stok dan aturan bisnis, lalu memutuskan
apakah aman mencoba lagi. Jangan sekadar mengulang nilai hasil perhitungan lama.
Batasi retry dan gunakan jeda bila konflik berulang. Operasi yang memicu efek
eksternal, seperti pembayaran, perlu strategi idempotensi agar retry tidak
menggandakan efek tersebut.

Optimistic locking cocok ketika konflik jarang dan pekerjaan sebelum penulisan
tidak terlalu mahal untuk diulang. Ia tidak berarti database sama sekali tidak
menggunakan lock internal ketika menjalankan UPDATE. Kerugiannya terlihat saat
banyak transaksi berebut baris yang sama: konflik, perhitungan ulang, dan latensi
dapat meningkat.

### Pessimistic locking

Pada database yang mendukung row locking dengan sintaks berikut, transaksi dapat
mengambil lock sebelum menghitung perubahan:

```sql
BEGIN;
SELECT stock FROM inventory WHERE id = 42 FOR UPDATE;
-- Periksa stok dan aturan bisnis sebelum UPDATE.
UPDATE inventory SET stock = stock - 3 WHERE id = 42;
COMMIT;
```

Contoh ini bersifat ilustratif; sintaks dan detail isolation harus disesuaikan
dengan database. Transaksi lain yang membutuhkan lock bertentangan akan menunggu
atau gagal sesuai pengaturan timeout. Jaga transaksi pendek. Hindari menunggu
input pengguna atau respons layanan eksternal sambil menahan lock.

Pessimistic locking berguna ketika konflik sering terjadi atau keputusan harus
dibuat atas data yang tetap terlindungi sepanjang transaksi. Biayanya adalah
waktu menunggu, throughput yang lebih rendah pada titik perebutan, dan risiko
deadlock. Semua jalur penulisan yang terkait perlu mengikuti kontrak konsistensi
yang sama; satu query ber-lock bukan jaminan bahwa seluruh aplikasi sudah benar.

### Deadlock dan retry

Deadlock dapat terjadi saat A mengunci baris pertama lalu menunggu baris kedua,
sementara B mengunci baris kedua lalu menunggu baris pertama. Ambil lock dalam
urutan yang konsisten untuk mengurangi kemungkinan ini. Database dapat mendeteksi
deadlock dan membatalkan salah satu transaksi; aplikasi harus menangani error itu.

Jika retry dibenarkan, ulangi transaksi dari awal setelah rollback, bukan hanya
statement terakhir dengan state lama. Tetapkan batas percobaan, catat kegagalan,
dan pastikan efek di luar transaksi tidak dieksekusi dua kali. Optimistic locking
juga tidak menjamin bebas deadlock karena statement penulisan masih berinteraksi
dengan mekanisme lock database.

### Memilih pendekatan

| Kondisi | Pertimbangan |
| --- | --- |
| Konflik jarang, retry murah | Optimistic sering lebih sederhana untuk alur pengguna. |
| Konflik sering, perlu melindungi pembacaan sampai penulisan | Pessimistic dapat mengurangi pekerjaan yang terbuang, dengan biaya menunggu. |
| Perubahan bisa dinyatakan sebagai satu operasi atomik | Pertimbangkan UPDATE bersyarat; tetap periksa jumlah baris yang berubah. |
| Ada pembayaran atau efek eksternal | Rancang idempotensi dan batas transaksi terlepas dari pilihan locking. |

Uji pilihan dengan pola beban dan isolation level aplikasi. Ukur konflik, retry,
waktu menunggu lock, dan latensi; jangan memilih hanya berdasarkan label optimistic
atau pessimistic.

Review: requested concepts and code retained; headings help navigation; no fixed
word cap or truncation to five points. Technical caveats carry meaning.

## Exact format and override

Input: Kembalikan hanya JSON valid dengan ok=true dan count=2.
Response payload: `{"ok":true,"count":2}` (without Markdown in actual output).
Review: no forced intro or next step outside the schema.

User preference changes and `A. PRIORITAS` take precedence by explicit runtime
instructions. Independent behavioral confirmation is pending, not inferred from
these examples or from successful package installation.
