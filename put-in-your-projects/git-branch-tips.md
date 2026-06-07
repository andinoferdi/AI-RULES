# Git Branch Tips

Panduan ini berisi tips praktis saat mengerjakan task di `[NAMA_REPO]`, terutama supaya branch dan Pull Request tetap bersih walaupun harus meniru flow dari branch lain, membandingkan environment demo, atau resolve conflict ke `[TARGET_PR_BRANCH]`.

Panduan utama tetap:

- [git-workflow.md](git-workflow.md)
- [git-naming.md](git-naming.md)

File ini hanya tambahan pengalaman lapangan. Isi placeholder sesuai workflow project aktif sebelum dipakai untuk task nyata.

## 1. Mulai Branch dari Branch Utama

Default workflow project ini: branch kerja dibuat dari `[BRANCH_UTAMA]`, lalu PR ke `[TARGET_PR_BRANCH]`.

```bash
git checkout [BRANCH_UTAMA]
git pull origin [BRANCH_UTAMA]
git checkout -b [PREFIX_NAMA]/[TYPE]/[NAMA_TASK]
```

Gunakan nama branch sesuai `git-naming.md`:

```text
[PREFIX_NAMA]/feat/[NAMA_FITUR]
[PREFIX_NAMA]/fix/[NAMA_BUG]
[PREFIX_NAMA]/refactor/[NAMA_REFACTOR]
```

Kenapa mulai dari `[BRANCH_UTAMA]`:

- Branch lebih bersih.
- PR hanya berisi perubahan task sendiri.
- Tidak ikut membawa commit branch orang lain.
- Lebih mudah direview oleh reviewer atau tech lead.

## 2. Kalau Mau Meniru Branch Lain, Jangan Langsung Merge

Kadang fitur sudah ada di branch lain, atau website demo, main, staging, dan lokal terlihat berbeda. Jangan langsung merge branch orang ke branch kita hanya untuk meniru behavior.

Lihat dulu bedanya:

```bash
git fetch origin
git diff [BRANCH_UTAMA]..origin/[BRANCH_REFERENSI] -- [PATH_YANG_RELEVAN]
git show [COMMIT_SHA] -- [PATH_YANG_RELEVAN]
```

Kalau ingin lihat file versi branch lain tanpa mengubah branch:

```bash
git show origin/[BRANCH_REFERENSI]:[PATH_FILE]
```

Kalau ingin membandingkan file lokal dengan branch lain:

```bash
git diff HEAD..origin/[BRANCH_REFERENSI] -- [PATH_FILE]
```

Catatan penting:

- `git cherry-pick` berarti menerapkan perubahan commit ke branch saat ini.
- Untuk sekadar melihat perbedaan, lebih aman pakai `git diff` atau `git show`.
- Cherry-pick boleh dipakai jika memang ingin mem-port commit tertentu secara terkontrol.
- Setelah behavior yang dibutuhkan jelas, implementasikan perubahan di branch sendiri sesuai scope task.

## 3. Commit Kecil dan Satu Concern

Jangan tunggu semua perubahan besar selesai baru commit satu kali.

Contoh commit yang rapi:

```bash
git add [PATH_ROUTE] [PATH_SERVICE]
git commit -m "feat([DOMAIN]): add [NAMA_FITUR] flow"

git add [PATH_COMMAND] [PATH_SCHEDULER]
git commit -m "feat([DOMAIN]): add [NAMA_PROSES_TERJADWAL]"

git add [PATH_TEST_FEATURE] [PATH_TEST_UNIT]
git commit -m "test([DOMAIN]): add [NAMA_FITUR] tests"
```

Keuntungannya:

- Mudah dicek ulang.
- Mudah di-cherry-pick.
- Mudah resolve conflict.
- PR terlihat fokus dan tidak seperti `wip`.

## 4. Saat PR Conflict ke Target Branch

Untuk conflict kecil, ikuti `git-workflow.md`: sync target branch, resolve conflict, test, lalu push.

Kalau `[TARGET_PR_BRANCH]` sedang banyak remerge, reset, atau berisi perubahan besar dari branch lain, merge langsung ke branch PR bisa membuat diff PR membengkak. Dalam kondisi itu, gunakan pola branch temporary.

Contoh kondisi:

- Branch PR awal: `[PREFIX_NAMA]/feat/[NAMA_FITUR]`.
- Target PR: `[TARGET_PR_BRANCH]`.
- PR conflict di beberapa file.
- Merge `origin/[TARGET_PR_BRANCH]` langsung ke branch PR berisiko membawa banyak perubahan di luar scope.
- Solusi: buat branch temporary dari `origin/[TARGET_PR_BRANCH]`, lalu cherry-pick commit task sendiri.

## 5. Pola Branch Temporary dari Target Branch

Pastikan working tree bersih dulu:

```bash
git status --short --branch
git fetch origin
```

Buat branch temporary dari target branch terbaru:

```bash
git checkout -b [PREFIX_NAMA]/[TYPE]/[NAMA_TASK]-[TARGET_PR_BRANCH]-resolve-[NOMOR] origin/[TARGET_PR_BRANCH]
```

Cherry-pick commit task sendiri satu per satu:

```bash
git cherry-pick [COMMIT_TASK_1]
git cherry-pick [COMMIT_TASK_2]
git cherry-pick [COMMIT_TEST]
git cherry-pick [COMMIT_LOGGING_ATAU_DOKUMENTASI]
```

Kalau conflict muncul:

```bash
git status --short
```

Resolve file konflik dengan prinsip:

- Pertahankan perubahan `origin/[TARGET_PR_BRANCH]` sebagai baseline.
- Tambahkan perubahan task sendiri hanya di titik yang memang diperlukan.
- Jangan menghapus route, service, migration, config, atau schedule milik fitur lain.
- Jangan memilih semua perubahan kita atau semua perubahan target branch tanpa memahami behavior.

Setelah conflict dibereskan:

```bash
git add [PATH_FILE_CONFLICT]
git cherry-pick --continue
```

Ulangi sampai semua commit task berhasil masuk.

## 6. Verifikasi Diff Tetap Fokus

Sebelum update branch PR, cek diff terhadap target branch:

```bash
git diff --stat origin/[TARGET_PR_BRANCH]...HEAD
git diff --check
git log --oneline origin/[TARGET_PR_BRANCH]..HEAD
```

Ekspektasi:

- File changed hanya area task sendiri.
- Tidak ada file dari task lain yang ikut masuk tanpa alasan.
- Tidak ada ratusan file target branch lain.
- Tidak ada whitespace error.

Lanjut syntax check dan targeted test sesuai area perubahan:

```bash
[COMMAND_SYNTAX_CHECK]
[COMMAND_TARGETED_TEST]
```

Kalau diff membengkak, stop dulu. Biasanya ada commit asing ikut masuk atau base branch salah.

## 7. Update Branch PR dengan Aman

Kalau branch temporary sudah benar, update branch PR yang sama.

Gunakan `--force-with-lease`, bukan `--force`:

```bash
git push --force-with-lease origin HEAD:[BRANCH_PR]
```

Kenapa `--force-with-lease`:

- Lebih aman daripada `--force`.
- Git akan menolak push jika remote branch sudah berubah tanpa sepengetahuan lokal.
- Cocok untuk branch milik sendiri yang perlu dirapikan setelah rebuild dari `origin/[TARGET_PR_BRANCH]`.

Setelah push:

- Refresh PR.
- Pastikan conflict hilang.
- Pastikan `Files changed` tetap fokus.
- Pastikan commit yang tampil hanya commit task sendiri.

## 8. Balikkan Local Branch ke Remote PR

Setelah branch PR berhasil di-update dari temporary branch, local branch utama bisa disesuaikan lagi:

```bash
git checkout [BRANCH_PR]
git pull --ff-only origin [BRANCH_PR]
```

Jika local branch berbeda history karena remote sudah di-force-with-lease dari branch temporary, gunakan cara yang jelas dan hati-hati:

```bash
git branch -f [BRANCH_PR] origin/[BRANCH_PR]
git checkout [BRANCH_PR]
```

Lalu cek:

```bash
git status --short --branch
git log --oneline origin/[TARGET_PR_BRANCH]..HEAD
```

## 9. Hapus Branch Temporary Jika Sudah Tidak Dipakai

Setelah PR aman dan branch utama sudah sesuai remote:

```bash
git branch -d [BRANCH_TEMPORARY]
```

Kalau Git menolak karena branch dianggap belum merged, cek dulu sebelum hapus paksa:

```bash
git log --oneline [BRANCH_TEMPORARY] --not [BRANCH_PR]
```

Jangan langsung pakai `-D` kalau belum yakin commit-nya sudah ada di branch PR.

## 10. Warning Penting

Jangan lakukan ini:

```bash
git push --force
```

Pakai ini jika memang perlu rewrite branch PR milik sendiri:

```bash
git push --force-with-lease origin HEAD:[BRANCH_PR]
```

Jangan commit file lokal yang tidak relevan:

- `.env`
- Credential
- API key
- Log
- Cache
- Perubahan debug sementara
- File hasil build atau generated file yang tidak terkait task

Jangan branch dari branch orang jika tidak ingin commit orang itu ikut PR.

Jangan merge `origin/[TARGET_PR_BRANCH]` langsung ke branch PR kalau tujuan utama adalah menjaga diff PR tetap fokus dan target branch sedang dalam kondisi banyak remerge, reset, atau perubahan besar.

## 11. Checklist Sebelum Minta Merge

Sebelum laporan PR:

```bash
git status --short --branch
git diff --stat origin/[TARGET_PR_BRANCH]...HEAD
git diff --check
git log --oneline origin/[TARGET_PR_BRANCH]..HEAD
```

Pastikan:

- Working tree bersih atau hanya ada perubahan yang memang belum mau di-commit.
- Diff PR fokus pada scope task.
- Test area perubahan sudah jalan.
- PR title sesuai format di `git-naming.md`.
- Deskripsi PR menjelaskan perubahan, alasan, cara test, dan migration jika ada.

## Referensi

- Git cherry-pick: https://git-scm.com/docs/git-cherry-pick
- Git push dan `--force-with-lease`: https://git-scm.com/docs/git-push
- GitHub resolve conflict command line: https://docs.github.com/articles/resolving-a-merge-conflict-using-the-command-line
