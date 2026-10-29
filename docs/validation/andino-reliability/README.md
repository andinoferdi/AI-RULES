# Andino reliability repair — 29 Oktober 2026

Implementasi lokal selesai pada kontrak dispatch dan handoff. Keandalan perilaku model menunggu pengujian pengguna; tidak ada AI actor pengujian yang dijalankan.

Andino sekarang memilih dan memuat metode kerja internal sebelum Focus atau pencarian skill eksternal opsional. Aturan ini mencakup seluruh 59 metode dan aliasnya: permintaan eksplisit mengarah ke guide kanonis; permintaan implisit memakai maksud, fase, trigger dan pengecualian. Nama dalam kutipan tidak mengaktifkan metode. Sibling riset/domain wajib, pilihan provider native eksplisit, izin host dan kebijakan UI tetap berlaku.

Rencana yang diterima dan siap dieksekusi memiliki route langsung ke plan-execution. Planning-only berhenti pada rencana; penerimaan rencana tidak memberi izin implementasi atau publikasi. Eksekusi menghubungkan task siap ke TDD, review dan verifikasi ketika fasenya relevan. Focus tetap lapisan komunikasi, bukan pemilih metode atau prasyarat metode kerja.

## Bukti offline

- Baseline 88 tes Andino lulus. Empat kontrak baru gagal pada runtime lama dan lulus pada kandidat.
- Suite umum 336 tes lulus, nol kegagalan/error, satu skip integrasi opsional. Ini dijalankan sebelum perbaikan final review; seluruh 108 tes Andino dijalankan ulang dan lulus setelah perbaikan tersebut.
- Validator paket: tujuh paket skill, metadata, relative links dan tujuh schema eval lulus.
- Validator capability: 74 schema dan 60 kontrak lulus pada hash kandidat yang sama.
- Instalasi kandidat: 41 skenario offline pada lima permukaan path host lulus, tanpa sumber jaringan. Ini tidak membuktikan discovery native atau perilaku model.
- Checker baru merekonsiliasi 59 metode, 53 alias, 19 rujukan sibling/family dan sembilan entri instrumen/native.244 definisi kasus mencakup eksplisit, implisit, negatif, seluruh target alias majemuk, transisi dan dua fixture aplikasi.
- Ekspor kandidat identik dengan sumber runtime yang diperiksa. Hash konten: `af63474a8966cc8186ddf50882989c57c792b0a1bccb5e07b2eadc3b6f2bcfd9`.
- `coverage.json` memetakan kasus serta rujukan guide pada arsip trace. Referensi path di panggilan bukan bukti pemuatan berhasil atau metode diterapkan. Bukti arsip tetap terikat hash/host/cakupannya; model kandidat tetap NOT_VERIFIED.

Suite pertama gagal mengimpor installer karena editable installation Python menunjuk checkout runtime yang hanya berisi namespace lama. Menambahkan src/ dari worktree kualitas ke sys.path dan PYTHONPATH proses uji memperbaiki pemilihan sumber; tidak ada perubahan instalasi global. Log suite yang berhasil ada di offline-suite.log.

## Review independen

Council menggunakan tiga penasihat independen untuk lima lensa, dilanjutkan review dengan ID respons anonim dan pemeriksaan kode/kontrak. Ini bukan lima suara independen. Satu review sempat gagal karena kapasitas layanan; retry terbatas dan review pengganti selesai tanpa menjalankan AI actor uji.

Temuan yang diperbaiki dengan regresi:

1. Ekspor memakai path relatif sehingga kandidat tidak dapat dimuat dari workspace kasus: destination kini diubah ke path absolut.
2. Template hasil tidak dapat masuk kembali ke pipeline bukti: kini kompatibel dengan validate_record dan diuji round-trip.
3. Alias majemuk hanya menguji target pertama: setiap pasangan alias/target kini memiliki kasus kontekstual dan coverage check.
4. Penghapusan pembekuan Focus-first juga melemahkan perlindungan lain: assertions kini menjaga host invocation, reuse, style override, disclosure dan fallback tanpa memulihkan urutan lama.

Review ulang tidak menemukan temuan actionable tersisa pada area tersebut. Pemeriksaan ini tidak mengklaim kepatuhan atau mutu model secara empiris.

## Mulai pengujian Anda

1. Buka [panduan paket manual](C:/Users/Lenovo/.codex/worktrees/andino-reliability-quality/AI-RULES/build/andino-reliability-manual-final/README.md). Kandidat berada di folder andino-workflow dalam paket itu; instalasi global lama belum diganti.
2. Mulai sesi agent baru pada workspace kasus. Berikan prompt.txt dan fixture saja; simpan folder reviewer untuk penilaian sesudahnya. Pastikan host memuat path/hash kandidat melalui mekanisme invocation yang diizinkan.
3. Mulai dari brainstorming implisit, planning eksplisit, planning-only, accepted-plan execution, unknown bug dan Focus-not-worker. Tambahkan kontrol tugas sederhana dan required native/research support.
4. Untuk penerapan nyata, jalankan application-accepted-plan dan application-tenant-cache pada workspace disposable dengan izin yang sesuai. Kasus routing-only tidak membuktikan aplikasi bekerja.
5. Simpan trace, hasil dan template penilaian. Bedakan metode dipilih, guide berhasil dimuat, tindakan penerapan dan mutu hasil. Jangan menghitung alat yang ditolak sebagai metode berhasil digunakan.

Paket dan checker tidak menginstal dependensi, mengubah konfigurasi global, atau menjalankan model. Mekanisme sandbox host tetap perlu diperiksa; folder disposable sendiri bukan jaminan containment.

## Lokasi perubahan

- Runtime: `C:/Users/Lenovo/Downloads/AI-RULES`, branch andino-workflow, basis 17ce784. Sembilan berkas lama diubah dan references/method-dispatch.md ditambahkan.
- Quality: worktree ini, basis 1a3b645; checker, fixture manual, regresi, laporan dan checkpoint.
- Pada delivery implementasi awal, sumber skill dan quality plane belum di-commit/push; status tersebut digantikan oleh otorisasi publikasi di bawah. Instalasi skill global dan data pengguna yang sudah ada tetap dipertahankan.

Untuk membuat ekspor baru dari worktree kualitas, gunakan destination baru agar hasil uji lama tidak tertimpa:

```powershell
python -B scripts/check_andino_reliability.py --runtime C:/Users/Lenovo/Downloads/AI-RULES --manual-bundle build/manual-run-new
```

Perintah tersebut hanya mengekspor kasus dan kandidat; tidak menjalankan evaluasi model.

## Publikasi yang diotorisasi — 29 Oktober 2026

Pengguna kemudian meminta commit/push ke origin/andino-workflow dan memastikan ai-rules setup tersedia. Runtime commit `65df26d182b3118e3f18ee46522eac83ea1036fb` sudah dipush normal dan SHA remote diverifikasi. Manifest main menaikkan release sequence menjadi19 dan mem-pin commit tersebut; seluruh pin sibling identik dengan manifest resmi sebelumnya.

published-setup.json mencatat akuisisi remote default-latest yang sebenarnya: fresh/repeat serta upgrade versi resmi17ce784/backup/repeat lulus. Tidak ada source/catalog/network mock; hanya home path pengujian module diarahkan ke lokasi disposable.

CLI yang terpasang semula rusak karena editable installation menunjuk checkout runtime yang tidak berisi ai_rules.cli. Paket wheel non-editable dibangun lokal dengan delapan bundle resmi, tanpa jaringan/dependensi tambahan, lalu menggantikan editable install. entrypoint-setup.json membuktikan ai-rules.exe asli bekerja dari cwd non-repository pada empat percobaan fresh/repeat/upgrade/repeat, tanpa override source, home atau PYTHONPATH. Instalasi skill global tidak dimodifikasi oleh pengujian.

Perintah pengguna tetap:

```powershell
ai-rules setup
```

Default latest mengambil branch runtime yang sudah dipublikasikan. Tidak diperlukan tagged binary release untuk jalur ini; wheel lokal juga berisi pin rilis19 untuk penggunaan bundled. Setelah pengguna menjalankan setup, mulai ulang sesi agent agar skill baru ditemukan. Pengujian file/instalasi ini tidak membuktikan pemilihan metode oleh model.

Suite penuh setelah pin rilis19 dan seluruh perbaikan review:339 tes lulus dalam191.798 detik, nol kegagalan/error dan satu skip integrasi opsional. Log aktual tersimpan di publication-suite.log. Delapan bundle rilis diekspor dari commit resmi masing-masing; hash Andino identik dengan kandidat yang diuji.
