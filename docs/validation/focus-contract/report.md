# Evaluasi revisi Focus

Tanggal evaluasi: 8 Oktober 2026. Evaluasi ini dilakukan sebelum commit/push dan
pembaruan instalasi global. Bukti kemudian dipindahkan ke branch main sesuai
kontrak distribusi repository; status delivery dilaporkan terpisah.

Kontrak final lebih tegas dan menunjukkan manfaat pada urutan coding,
pengelompokan daftar, laporan hasil, dan kelanjutan tugas. Kepatuhan model belum
konsisten pada semua skenario. **60 inference berhasil dijalankan bukan berarti
60 respons lulus seluruh behavioral contract.**

## Berkas dan scope

- Branch `focus`, checkout `C:/Users/Lenovo/Downloads/AI-RULES`: `SKILL.md`.
- Branch `WebBased`, checkout
  `C:/Users/Lenovo/.codex/worktrees/focus-web-contract/AI-RULES`: hanya `README.md`,
  bagian `X. FOCUS`. Bagian sebelum X dan mulai Z identik dengan HEAD.
- Bukti pendukung pada branch main: rencana di
  `docs/exec-plans/completed/focus-contract.md`, report ini, `run_eval.py`,
  `verify_eval.py`, tiga snapshot `*-inputs.json`, dan tiga transkrip agregat
  `*-outputs.json`. Artefak ini mendukung revisi; bukan mekanisme aktivasi baru.
- `README.md` branch focus, kedua berkas lisensi, aturan lain, installer,
  konfigurasi host, dan skill global tidak diubah.

Baseline Git: focus `4dc2ba2`; WebBased
`2fdbce1a7448932646c09f758c6d9ccb4a6e022e`. Path checkout di atas merekam host saat
evaluasi, bukan prasyarat untuk menjalankan pemeriksaan pada host lain.

## Perubahan behavioral contract

| Area | Kontrak lama | Kontrak final |
| --- | --- | --- |
| Awal respons | Jawaban/hasil/tindakan di awal, kode dekat awal | Jawaban faktual, solusi praktis, atau hasil nyata langsung di awal; tanpa pengantar/rencana verbal; jawaban sederhana tidak menambah alternatif yang tidak diperlukan |
| Urutan praktis | Nomor jika urutan penting | Seluruh rangkaian tindakan bernomor, bukan hanya verifikasi; satu tindakan utama per langkah; kode/perintah berada pada langkahnya; navigasi sepele digabung |
| Next action | Sebutkan tindakan paling berguna | Akhiri dengan tepat satu tindakan pengguna jika memang ada pekerjaan yang perlu dilakukan; agent mengerjakan sendiri ketika tools dan izin memungkinkan; tidak membuat tugas setelah selesai |
| Progres | Ingatkan konteks ketika dibutuhkan | Singkat: selesai, posisi sekarang, berikutnya ketika relevan; memakai plan yang ada; tanpa status paksa atau recap setiap giliran |
| Daftar panjang | Kelompokkan tanpa batas item | Kelompok relevan sekitar lima item; daftar lengkap tetap dikelompokkan dan tidak dipotong |
| Hasil/error | Bukti dan ketidakpastian dipertahankan | Hasil nyata + verifikasi + batas; gejala + penyebab terbukti atau status belum pasti + pemeriksaan/perbaikan yang didukung bukti |
| Contoh/check | Pemeriksaan umum dalam paragraf | Lima Bad/Good konkret dan lima pemeriksaan sebelum kirim; contoh bukan template wajib |

Tetap dipertahankan: prioritas A dan instruksi lebih tinggi, kedua referensi gaya
bahasa jika tersedia, adaptasi bahasa/formalitas, tanpa asumsi ADHD atau kondisi
pribadi, tanpa batas panjang kaku, tanpa estimasi waktu wajib, penjelasan panjang,
format khusus, override pengguna, izin host, standalone dan Andino. Aktivasi dan
bagian prioritas SKILL.md identik dengan baseline. Versi web tetap memakai pola
satu blok `text`, label kapital, dan poin seperti rules lain.

Referensi original:
[i-have-adhd SKILL.md](https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md),
diakses 8 Oktober 2026. Yang diadaptasi ialah tindakan jelas, langkah bernomor,
hasil terlihat, contoh, dan pemeriksaan sebelum kirim. Asumsi diagnosis, reminder
setiap giliran, estimasi waktu wajib, dan next action otomatis tidak diadopsi.
Copyright Ayoub Ghriss 2026 dan pemberitahuan MIT tetap utuh pada kedua distribusi.

## Metode pengujian perilaku

Claude Code CLI 2.1.294, Windows, model aktual dari metadata respons
`claude-sonnet-5-5`, provider `firstParty`, effort yang dikirim `medium`.
Setiap fixture memakai sesi inference baru dengan:

```text
claude -p --safe-mode --system-prompt-file <snapshot-system>
  --tools "" --strict-mcp-config --disable-slash-commands
  --no-session-persistence --output-format json
  --model claude-sonnet-5-5 --effort medium
```

Prompt pengguna tidak menyertakan rubric atau jawaban yang diharapkan. Konteks
bersama adalah A. PRIORITAS dan isi kedua referensi human-language dari WebBased
baseline. Hanya kontrak komunikasi yang berbeda. Snapshot, hash system prompt,
prompt pengguna, output asli, metadata model, exit code, dan penggunaan token
tersimpan. Waktu inference tidak dijadikan estimasi waktu tugas pengguna.

Sepuluh prompt yang identik menguji: pertanyaan Git sederhana, coding Python,
debugging HTTP 401 tanpa bukti penyebab, hasil pekerjaan selesai, resume tanpa
CSV/tools, daftar lengkap 12 item, penjelasan locking panjang, JSON ketat, kode
saja dalam bahasa Inggris, dan override satu paragraf tanpa daftar.

1. `before`: 20 inference sebelum mengedit kontrak, dari snapshot aturan lama.
2. `after`: 20 inference revisi pertama. Bukti menunjukkan penomoran dan
   pengelompokan masih belum konsisten.
3. `final`: 20 inference setelah memperjelas bahwa nomor meliputi seluruh urutan,
   daftar lengkap tetap berkelompok, dan default bukan saran opsional.

Baseline dan revisi pertama tidak diganti atau dibuang. Semua respons diperiksa
secara kualitatif oleh agent pelaksana; penilaian bukan blind review independen.
Ini pengujian perilaku output model nyata dengan aturan disuplai langsung,
**bukan** pengujian installer, pemuatan skill otomatis, eksekusi tools, deployment,
atau parity lintas host. Metadata environment CLI tetap ada dan dapat memengaruhi
respons, misalnya catatan direktori Temp pada jawaban sederhana baseline.

Kegagalan awal harness `WinError 206` terjadi sebelum inference karena system
prompt terlalu panjang untuk argumen Windows. Perbaikannya memakai file prompt;
tidak dihitung sebagai respons baseline. Probe instruksi literal terpisah
mengonfirmasi bahwa CLI menggunakan file system prompt. Probe tidak masuk 60 kasus.

## Hasil sebelum/final

Jumlah kata dihitung dengan whitespace split, bukan tokenizer. Tabel ini
deskriptif untuk sampel yang diamati, bukan klaim peningkatan statistik.

| Kasus | Kata skill, sebelum → final | Kata web, sebelum → final | Penilaian perilaku |
| --- | --- | --- | --- |
| Sederhana | 65 → 36 | 47 → 29 | Lebih pendek, tetapi alternatif Git yang tidak diminta masih muncul; belum patuh penuh |
| Coding | 155 → 145 | 187 → 154 | Kedua versi final memulai dengan tiga langkah untuk edit, test, dan verifikasi; catatan opsional masih terlalu panjang dan urutan red/green tambahan muncul belakangan |
| Debugging | 266 → 252 | 295 → 201 | Ketidakpastian tetap disebut dan check konkret tersedia; masih ada ranking penyebab tanpa bukti cukup dan inferensi akun yang terlalu pasti; hasil campuran |
| Selesai | 55 → 34 | 67 → 24 | Hasil, command, enam test, dan integration belum diuji dipertahankan; next action buatan pada baseline web hilang |
| Resume | 141 → 77 | 145 → 85 | Selesai/tertunda/batas akses jelas, satu permintaan CSV; permintaan schema tambahan pada baseline web hilang |
| Daftar lengkap | 328 → 327 | 344 → 273 | Baseline satu daftar 12 item; final tiga kelompok berisi empat item, tetap 12 item. Kualitas isi checklist tidak dibuktikan hanya dengan hitungan item |
| Penjelasan panjang | 2650 → 2917 | 2696 → 2765 | Semua topik yang diminta dan contoh SQL tetap ada; tidak dipaksa pendek. Ada ketidaktepatan teknis yang masih perlu koreksi jika jawaban ini akan digunakan |
| JSON | 8 → 8 | 8 → 8 | JSON valid, keys tepat, enam test dan integration belum diuji tetap tersedia |
| Kode saja | 9 → 9 | 9 → 9 | Tanpa fences/prosa; kode dapat dikompilasi dan menghasilkan [] serta ['a', 'b'] untuk fixture |
| Override paragraf | 192 → 183 | 171 → 139 | Tetap satu paragraf tanpa daftar, urutan edit/test/command tersedia; saran whitespace yang tidak diminta masih muncul |

Gabungan tujuh kasus nonpanjang dan nonformat ketat: 2458 → 1959 kata,
turun **20,3%**. Skill: 1202 → 1054; web: 1256 → 905. Ukuran teks bukan ukuran
akurasi: keuntungan yang paling jelas ialah struktur coding, pengelompokan
daftar, laporan selesai, dan fokus tindakan resume.

### Contoh output nyata sebelum/sesudah

Coding skill, sebelum: instruksi "Tambahkan pengecekan input kosong" dan
"Tambahkan tes" muncul dalam paragraf terpisah, lalu command verifikasi; urutan
test sebelum perubahan dijelaskan belakangan.

Coding skill, final (kutipan langkah; kode lengkap ada pada transkrip):

1. "Di `src/parser.py`, tambahkan pengecekan input kosong di awal `parse`."
2. "Di `tests/test_parser.py`, tambahkan test ini."
3. "Jalankan test dari root proyek."

Selesai web, sebelum (kutipan tambahan yang tidak diperlukan):
"Jalankan integration test sebelum merge" di bawah judul tindakan yang masih perlu,
padahal fixture menyatakan pekerjaan yang diminta sudah selesai.

Selesai web, final (output utuh):

> `src/parser.py` sekarang mengembalikan `[]` untuk input kosong.
> `pytest tests/test_parser.py` lulus 6 test. Integration test belum dijalankan,
> jadi perilaku di luar unit test belum terverifikasi.

Resume web, sebelum (kutipan permintaan tambahan):
"Kalau mau memanfaatkan waktu tunggu, tempel juga schema dan definisi mapping yang sekarang."

Resume web, final (kutipan next action):
"Berikutnya: kirim baris header CSV beserta beberapa baris sampel yang representatif"
dengan kasus tepi dan penyamaran nilai sensitif.

### Akurasi dan batas bukti

Tidak ada klaim bahwa seluruh jawaban final benar atau kepatuhan lebih baik di
semua kategori. Debugging final web masih membuka dengan "Kemungkinan besar bukan
database yang rusak" tanpa bukti aplikasi. Menurut
[RFC 9110, 401](https://www.rfc-editor.org/rfc/rfc9110.html#name-401-unauthorized),
kode tersebut menjelaskan kebutuhan kredensial autentikasi; bukan bukti kesehatan
database atau ranking akar masalah aplikasi.

Pada penjelasan panjang final skill, kalimat "Isolation level juga tidak
melindungi invarian yang melibatkan beberapa baris" terlalu umum dan bertentangan
dengan penjelasan Serializable yang diberikan setelahnya.
[PostgreSQL transaction isolation](https://www.postgresql.org/docs/18/transaction-iso.html)
menjelaskan jaminan Serializable dan kebutuhan retry. Pada final web, contoh
penggabungan pessimistic/optimistic belum menaikkan `version` pada UPDATE
pessimistic, walaupun penjelasan menyebut keduanya bisa digabung; itu celah
ketepatan contoh. Pemeriksaan sumber ini terbatas pada titik tersebut dan
[locking PostgreSQL](https://www.postgresql.org/docs/18/explicit-locking.html),
bukan audit seluruh klaim lintas database atau eksekusi SQL.

Tidak ada database uji atau proyek parser nyata pada fixture. Kode-only diperiksa
secara nyata terhadap input fixture; snippet SQL dan tutorial panjang tidak
dijalankan. Tidak ada benchmark produksi, confidence interval, pengulangan untuk
mengukur varians, atau model kedua. Respons sebelum/final memakai konfigurasi
sebanding, tetapi sampling model tetap dapat menghasilkan variasi.

## Verifikasi dan reproduksi

```powershell
python docs/validation/focus-contract/verify_eval.py
git diff --check
git -C <checkout-WebBased> diff --check
```

Hasil: semua pemeriksaan transkrip/format/struktur tersebut lulus. Script memeriksa
60 inference sukses, identitas model, prompt/konteks/config sama, hash, enam output
JSON, enam output kode-only, enam override paragraf, dan cakupan topik enam output
panjang. Final snapshot identik dengan berkas final. Lima contoh Bad/Good ada di
kedua versi; layout fence, atribusi, lisensi, aktivasi/prioritas, dan README di luar
X dipertahankan. Pemeriksaan kata kunci tidak membuktikan kebenaran penjelasan.

Untuk menjalankan ulang inference menggunakan snapshot tersimpan:

```powershell
python docs/validation/focus-contract/run_eval.py before
python docs/validation/focus-contract/run_eval.py final
```

Runner memakai snapshot yang sudah ada. Verifier membaca branch `focus` dan
`WebBased` dari Git; gunakan `--focus-root <path>` dan `--web-root <path>` untuk
memeriksa working tree yang belum di-commit. Runner juga menerima kedua opsi
tersebut ketika membuat snapshot baru. Fetch branch distribusi sebelum memeriksa
clone baru. Tidak ada dependency RTK atau path mesin tertentu pada kedua script.

Menjalankan ulang akan memakai layanan
model dan mengganti transkrip untuk fase tersebut; salin artefak jika ingin
mempertahankan run pertama. Tidak diperlukan instalasi
ulang atau perubahan aktivasi untuk meninjau perubahan lokal ini.

Revisi dokumen selesai. Bukti mendukung manfaat terbatas yang disebutkan di atas;
keandalan penuh semua default dan eksekusi agent tetap belum terbukti.

Cleanup, publikasi, dan update instalasi berikutnya tercatat dalam
[delivery verification](delivery.md) dan [setup proof](setup-verification.json).
