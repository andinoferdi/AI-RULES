# AGENTS

Aturan kerja untuk AI agent, coding assistant, dan developer di project `[PROJECT_NAME]`. Scope aktif adalah root aplikasi; folder requirements, notes, dan screenshot hanya referensi bila task memintanya.

## 1. Root project & batas kerja
- Jalankan command dari root aplikasi kecuali task meminta file di luar project.
- Abaikan dependency, build, cache, dan artifact (mis. `node_modules`, `vendor`, `dist`, `build`, `.next`, `coverage`, log besar, asset besar).
- Sebelum mengubah kode, pahami file terdekat, route/endpoint terkait, request/response, dan pola modul yang ada.
- Perubahan minimal, spesifik pada task, dan tidak merombak arsitektur tanpa instruksi eksplisit.

## 2. Stack
Project ini memakai `[STACK_BACKEND]` + `[STACK_FRONTEND]` + `[DATABASE]` (contoh: isi sesuai `package.json`/`composer.json`/manifest project). Jangan menambah framework atau library baru jika kebutuhan bisa diselesaikan dengan stack yang ada atau helper project.

## 3. Struktur folder
Gunakan struktur nyata repo sebagai sumber kebenaran (baca file tree dulu). Jika nama folder domain sudah ada, tambahkan file baru sedekat mungkin dengan domain itu. Jangan buat struktur baru sebelum memeriksa pola sekitar.

## 4. Aturan coding
- Jaga route, URL, method, middleware, permission, dan kontrak request/response yang sudah berjalan.
- Validasi input di server. Jangan percaya role, permission, harga, stok, status, atau ownership dari client.
- Controller/handler fokus pada request, validasi, pemanggilan service, dan response. Logic berat ikut pola layer yang ada.
- Hindari N+1 pada listing, tabel, export, dan dashboard.
- Hormati auth, ownership, role, permission, dan filter akses yang ada.
- Jangan redesign UI besar bila task hanya meminta perbaikan fungsi.
- Jangan hardcode secret, credential, URL production, token, atau API key.

## 5. Command
Jalankan hanya command yang relevan dengan task. Jika RTK tersedia, awali dengan `rtk` (contoh):

```powershell
rtk [PERINTAH_DEV_SERVER]
rtk [PERINTAH_BUILD]
rtk [PERINTAH_TEST]
```

Jangan jalankan command berat (full build, full test, migration nyata, deploy) kecuali task membutuhkannya.

## 6. Verifikasi
Pilih verifikasi paling relevan dengan area yang diubah: test untuk logic backend, build untuk asset frontend, cek manual route/UI untuk perubahan tampilan. Jika verifikasi tidak bisa jalan karena environment/dependency/database lokal, catat alasannya singkat di final response.

## 7. Prinsip aman (WAJIB)
- Jangan mengubah migration lama, dump SQL, seed penting, atau data production tanpa task eksplisit.
- Jangan menghapus permission, middleware, filter akses, atau validasi hanya untuk menyederhanakan kode.
- Jangan mengubah file environment kecuali diminta. Dokumentasikan konfigurasi lewat file contoh bila perlu.
- Jangan commit, push, deploy, atau menjalankan migration nyata tanpa instruksi eksplisit.
- Jika ada perubahan user yang belum Anda buat di worktree, jangan revert. Baca dan bekerja berdampingan.

Ikuti dokumen ini bersama `chat-rules.md`, `code-rules.md`, dan `token.md`. Saat aturan bertentangan: instruksi sistem/platform tertinggi dulu, lalu instruksi pengguna terbaru, lalu aturan project ini.
