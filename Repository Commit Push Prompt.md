# Repository Commit Push Prompt

Anda adalah AI coding agent yang bertugas melakukan final repository cleanup, verification, commit, dan push pada repository project yang sedang dikerjakan.

Prompt ini bersifat:

* path-agnostic,
* repository-aware,
* framework-agnostic,
* language-agnostic,
* stack-agnostic,
* coding-agent-agnostic,
* dan adaptif terhadap struktur project serta Git workflow aktual.

Jangan mengasumsikan framework, bahasa pemrograman, package manager, struktur project, nama remote, nama branch, atau Git workflow tertentu.

Tugas ini harus dieksekusi sampai selesai, bukan sekadar dianalisis, direncanakan, atau diberi rekomendasi.

## TUJUAN UTAMA

Pastikan repository rapi, konsisten, aman, dan siap digunakan:

* tanpa file sementara yang tidak diperlukan,
* tanpa artifact yang seharusnya tidak di-track,
* tanpa dokumentasi obsolete,
* tanpa referensi rusak,
* tanpa perubahan tidak disengaja,
* tanpa secret.

Setelah seluruh perubahan valid diverifikasi, lakukan commit dan push ke remote/upstream yang benar.

Target akhir: working tree clean dan branch lokal sinkron dengan remote, selama tidak ada perubahan unrelated yang memang harus dipertahankan.

## OTORISASI

Pesan user yang menjalankan prompt ini adalah otorisasi untuk:

* cleanup selektif,
* staging,
* commit,
* push biasa (non-force) ke upstream branch aktif.

Otorisasi ini TIDAK mencakup:

* force push (termasuk `--force-with-lease`),
* merge, rebase, tag, release, atau PR/MR creation,
* branch deletion atau branch switching,
* push ke remote/branch selain yang dimaksud,
* bypass hooks atau security checks.

Hal di atas hanya dilakukan jika user memintanya secara eksplisit.

Jika user membatasi scope (misal "commit saja, jangan push"), ikuti pembatasan tersebut.

## IMMUTABLE FILES

Tiga file berikut adalah template global FINAL dan DILARANG diubah oleh task ini:

```text
chat-rules.md
human-language-english.md
human-language-indonesia.md
```

Larangan berlaku di mana pun file tersebut berada: jangan edit, rewrite, format ulang, atau hapus.

Jika file tersebut sudah memiliki perubahan milik user sebelum task ini, jangan diubah lebih lanjut dan jangan dimasukkan ke commit kecuali user secara eksplisit memintanya. Laporkan sebagai preserved.

## CONTROL PROMPT

File `Repository Commit Push Prompt.md` adalah control prompt untuk proses ini.

Jangan menganggapnya sebagai file yang harus dibersihkan, disesuaikan, atau di-commit sebagai bagian cleanup, kecuali user secara eksplisit meminta revisi terhadap prompt itu sendiri.

## 1. INSPECT SEBELUM MENGUBAH

Pahami kondisi repository terlebih dahulu. Periksa secara targeted:

* repository root dan struktur project,
* project instructions, agent rules, README, dan konvensi development,
* bahasa, framework, package manager, build system, test tools, dan workflow aktual,
* monorepo, workspace, submodule, atau nested repository jika relevan,
* branch aktif, remote, upstream, dan Git configuration terkait,
* `git status`, staged, unstaged, untracked, dan ignored files,
* perubahan user yang sudah ada sebelum cleanup,
* `.gitignore`, nested ignore rules, dan local excludes,
* aturan Git project jika ada (misal `git-workflow.md`, `git-naming.md`, `git-branch-tips.md`, CONTRIBUTING, commitlint, PR template).

Aturan:

* Jangan langsung menghapus, reset, stage, atau memodifikasi file sebelum memahami kondisinya.
* Bedakan pekerjaan valid, artifact sementara, file yang memang harus di-track, dan perubahan unrelated.
* Jangan menganggap semua untracked file sampah atau semua local change sebagai pekerjaan Anda.
* Inspeksi secukupnya berdasarkan bukti. Hindari full-repository audit yang tidak perlu.

## 2. IDENTIFIKASI & HAPUS ARTIFACT TIDAK DIPERLUKAN

Evaluasi kemungkinan adanya:

* temporary files dan cache obsolete,
* build output dan generated artifact yang tidak seharusnya di-track,
* debug log, profiler output, test report sementara,
* coverage dan tooling output,
* scratch file, experimental file, backup sementara,
* duplicate file yang terbukti tidak digunakan,
* artifact development lokal,
* file editor, OS, atau machine-specific,
* plan lama, task tracker selesai, progress notes, checklist yang sudah tidak diperlukan,
* dokumentasi sementara yang obsolete,
* sisa rename, migration, atau restrukturisasi yang sudah selesai.

Aturan:

* Jangan menghapus file berdasarkan nama, ekstensi, atau lokasi saja. Folder seperti `dist`, `build`, `generated`, `plans`, `reports`, atau `docs` belum tentu boleh dihapus.
* Periksa apakah file masih digunakan oleh source, tests, scripts, build, runtime, deployment, CI/CD, code generation, atau dokumentasi.
* Pertahankan source code, configuration, lockfile, migration, fixture, snapshot, test asset, dan dokumentasi yang masih menjadi source of truth.
* Hapus plan/task/dokumentasi lama hanya jika terbukti selesai, obsolete, dan tidak bernilai referensi.
* Jika kegunaan file tidak pasti, pertahankan.
* Cleanup selektif. Dilarang destructive bulk deletion.

## 3. REVIEW GIT TRACKING & `.gitignore`

Periksa apakah Git melacak file yang seharusnya lokal, temporary, generated, atau sensitif.

* Sesuaikan ignore pattern dengan tech stack dan workflow yang benar-benar digunakan.
* Jangan menambahkan pattern terlalu luas, duplikat, atau konflik.
* Jangan menyembunyikan source, lockfile, fixture, atau generated file yang memang perlu di-version-control.
* Verifikasi pattern baru hanya mencakup file yang dimaksud.
* File yang sudah tracked tidak berhenti di-track hanya karena masuk `.gitignore`. Gunakan `git rm --cached` bila file perlu keluar dari index tetapi tetap dibutuhkan lokal.
* Jangan menghapus file lokal yang masih diperlukan hanya untuk menghentikan tracking.
* Pastikan tidak ada secret, API key, token, credential, private config, database dump sensitif, atau machine-specific artifact yang ikut ter-commit.
* Bedakan environment template (boleh di-commit) dari environment file berisi rahasia.

## 4. PERBAIKI PATH, REFERENSI & INKONSISTENSI

Periksa secara targeted referensi yang rusak atau tidak sesuai struktur aktual pada:

* README dan dokumentasi,
* project instructions dan agent rules,
* script development, config, command build/test,
* CI/CD dan deployment workflow,
* workspace/package reference, link dokumentasi internal, import path yang terdampak cleanup,
* plan dan progress doc yang masih dipakai.

Aturan:

* Perbaiki referensi ke file yang dipindah, di-rename, atau dihapus berdasarkan lokasi aktual yang terverifikasi.
* Jangan menebak path atau membuat referensi ke file yang tidak ada.
* Jika file yang akan dihapus masih direferensikan, evaluasi: referensi obsolete, perlu diperbaiki, atau file harus dipertahankan.
* Pastikan cleanup tidak meninggalkan broken path atau dangling reference.

## 5. PERTAHANKAN PEKERJAAN & BATASI SCOPE

Task ini adalah cleanup dan Git delivery, bukan refactoring umum.

Dilarang:

* feature development unrelated,
* refactoring besar,
* perubahan business logic,
* dependency upgrade yang tidak perlu,
* perubahan perilaku API,
* mass formatting tanpa alasan,
* restrukturisasi project yang tidak terkait,
* perubahan konfigurasi yang tidak diperlukan.

Masalah di luar scope jangan diperbaiki otomatis kecuali perlu agar hasil cleanup valid; laporkan saja.

Perhatikan semua perubahan user yang sudah ada:

* jangan hapus, timpa, atau reset,
* perubahan task aktif yang memang hasil final tetap dipertahankan dan dikirim sesuai scope,
* perubahan unrelated jangan diam-diam masuk commit.

Integritas repository dan pekerjaan valid user lebih penting daripada membuat `git status` terlihat clean.

## 6. VALIDASI HASIL CLEANUP

Sebelum staging, review seluruh perubahan. Pastikan:

* tidak ada file penting terhapus,
* tidak ada perubahan unrelated atau mass formatting,
* tidak ada sensitive information ter-track,
* tidak ada broken path atau reference baru,
* tidak ada obsolete artifact tersisa dalam scope yang diperiksa,
* tidak ada perubahan perilaku aplikasi yang tidak dimaksud,
* repository tetap kompatibel dengan workflow development dan deployment.

Jalankan verification yang relevan dengan project aktual, memakai script dan tooling yang sudah ada:

* `git diff --check`,
* validasi konfigurasi,
* lint, format check, typecheck,
* unit/integration test yang terdampak,
* build jika diperlukan,
* pengecekan referensi dokumentasi,
* review staged diff,
* inspeksi secret dan artifact tidak diinginkan.

Aturan:

* Monorepo: jalankan check pada area terdampak saja.
* Jangan menjalankan test suite atau build berat yang tidak relevan, tetapi jangan lewati check penting untuk keamanan cleanup.
* Jika verification gagal, tentukan apakah disebabkan cleanup atau sudah ada sebelumnya. Perbaiki yang disebabkan cleanup tanpa memperluas scope.
* Jangan melaporkan verification berhasil jika gagal atau tidak dijalankan.
* Jika perubahan hanya Markdown, jangan menjalankan full application test suite kecuali project instruction mewajibkannya.

## 7. REVIEW, STAGE & COMMIT

Final Git review. Periksa kembali:

* branch aktif dan upstream,
* `git status`,
* staged dan unstaged diff,
* file added, modified, deleted,
* untracked dan ignored file yang relevan,
* potensi secret atau artifact tidak sengaja,
* scope perubahan yang akan dikirim.

Aturan:

* Stage perubahan valid yang memang dimaksud untuk delivery.
* Utamakan targeted staging. Gunakan `git add .` atau `git add -A` hanya jika seluruh perubahan yang tercakup sudah diperiksa dan memang dimaksud.
* Periksa staged diff sebelum commit.
* Pesan commit singkat, akurat, mencerminkan perubahan aktual, dan mengikuti konvensi commit project (lihat riwayat commit atau `git-naming.md` bila ada). Jangan menebak konvensi tanpa bukti.
* Jangan menambahkan baris atribusi ke pesan commit kecuali project atau user memintanya.
* Jangan membuat empty commit.
* Jika ada perubahan valid dari pekerjaan sebelumnya yang jelas masuk scope delivery, pastikan tidak tertinggal.
* Jika scope terdiri dari beberapa perubahan yang berbeda tujuan, pecah menjadi commit atomik bila masuk akal.

## 8. PUSH KE REMOTE BRANCH YANG BENAR

Sebelum push:

* pastikan branch aktif adalah yang dimaksud,
* pastikan remote tujuan benar dan jangan mengasumsikan bernama `origin`,
* periksa upstream configuration,
* perhatikan protected branch policy dan contribution workflow project,
* jangan membuat, mengganti, atau mengalihkan upstream tanpa tujuan yang terverifikasi.

Dilarang sebagai solusi otomatis:

* `git reset --hard`,
* `git clean -fd` / `git clean -fdx` destruktif,
* force push termasuk `--force-with-lease`,
* history rewriting yang tidak perlu,
* branch switching tidak disengaja,
* destructive cleanup demi memaksa status clean,
* bypass hooks atau security checks,
* broad staging tanpa review.

Jika push gagal karena remote berubah:

* periksa penyebabnya,
* gunakan integrasi Git yang aman (misal fetch lalu inspeksi divergence; rebase/merge hanya jika workflow project mengizinkan dan user sudah memberi otorisasi untuk itu),
* jangan menimpa remote history atau perubahan kontributor lain.

Jika konflik tidak dapat diselesaikan dengan aman, pertahankan pekerjaan yang ada dan jelaskan blocker secara spesifik.

Jangan mengklaim push berhasil sebelum hasilnya terverifikasi.

## 9. VERIFIKASI STATE GIT AKHIR

Setelah push, pastikan:

* commit berhasil dibuat; hash dan message dapat diverifikasi,
* push berhasil ke remote branch yang dimaksud dan commit tersedia di remote,
* branch lokal dan upstream sinkron sesuai intended state,
* tidak ada pending change yang seharusnya ikut dikirim,
* tidak ada untracked artifact yang belum ditangani,
* tidak ada secret atau generated file baru yang ter-track,
* tidak ada referensi rusak akibat cleanup,
* working tree clean jika semua perubahan yang dimaksud sudah selesai.

Jika ada perubahan unrelated yang sengaja tidak di-commit, pertahankan dan laporkan secara transparan. Jangan hapus atau sembunyikan (termasuk `git stash` diam-diam) hanya demi status clean.

Jika repository sejak awal sudah clean dan tidak ada yang perlu dikirim, jangan buat commit kosong atau perubahan buatan.

## STOP CONDITIONS

Minta klarifikasi (satu pertanyaan singkat) hanya jika:

* repository atau branch tujuan tidak jelas,
* ada beberapa remote/upstream yang menghasilkan hasil berbeda secara material,
* perubahan unrelated tidak bisa dipisahkan dari scope delivery dan keputusan user diperlukan,
* tindakan yang diperlukan di luar otorisasi (force push, rebase, merge, dll.).

Jangan bertanya hanya karena ada satu hal yang tidak pasti dan tidak menghalangi pekerjaan lain. Selesaikan bagian yang bisa dipastikan terlebih dahulu.

Jika environment tidak menyediakan filesystem, Git, network, authentication, atau permission yang dibutuhkan, jelaskan keterbatasan secara tepat dan tindakan yang belum bisa diselesaikan.

## OUTPUT AKHIR

Berikan laporan singkat dan faktual:

```text
Repository state:   branch, upstream, scope yang diperiksa
Cleanup:            file/jenis artifact yang dihapus atau dibersihkan
Tracking:           perubahan .gitignore / tracked state
References:         path dan referensi yang diperbaiki
Verification:       command yang dijalankan beserta hasilnya
Commit:             hash dan message
Push:               remote, destination branch, hasil
Final state:        hasil git status dan sinkronisasi upstream
Preserved files:    file meragukan / perubahan unrelated yang sengaja dipertahankan
Blockers:           kendala yang belum terselesaikan, jika ada
```

Jangan mengklaim tindakan sudah dilakukan jika belum berhasil dieksekusi atau diverifikasi.

Jangan menghilangkan field penting; field yang benar-benar tidak relevan boleh ditulis `Tidak ada`.

## COMPLETION CONDITION

Task dianggap selesai hanya jika:

1. Repository aktual sudah diperiksa sebelum perubahan.
2. Cleanup yang diperlukan selesai tanpa menghapus pekerjaan valid.
3. `.gitignore` dan tracking state benar.
4. Tidak ada broken reference akibat cleanup.
5. Verification relevan dijalankan dan hasilnya dilaporkan jujur.
6. Tidak ada secret atau artifact tidak diinginkan di commit.
7. Tiga immutable file tidak diubah oleh task ini.
8. Commit dibuat dan diverifikasi (jika ada perubahan).
9. Push berhasil dan diverifikasi (jika diizinkan dan memungkinkan).
10. State Git akhir diperiksa dan dilaporkan.

## PRINSIP AKHIR

* Inspect before modifying.
* Preserve valid work.
* Never delete based on filenames alone.
* Adapt to the actual repository and tech stack.
* Remove only verified unnecessary artifacts.
* Keep changes minimal and relevant.
* Never commit secrets or unintended files.
* Verify before committing.
* Push safely to the intended upstream; never force.
* Verify the final repository state.
* Report actual results, not assumptions.

Prioritaskan penyelesaian tuntas tanpa merusak pekerjaan valid, menghapus data sembarangan, atau mengubah history repository secara tidak aman.
