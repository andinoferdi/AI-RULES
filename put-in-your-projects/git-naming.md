# Naming, PR, dan Daily Report

Panduan singkat untuk membuat nama branch, commit, PR title, deskripsi PR, dan daily report yang rapi, natural, serta tetap mengikuti gaya tim atau repository.

## Branch Naming

- Format branch mengikuti workflow repo: `type/deskripsi-singkat-dengan-dash`.
- Jika tim memakai prefix nama, gunakan format: `nama/type/deskripsi-singkat`.
- Type yang umum dipakai: `fix`, `feat`, `feature`, `hotfix`, `refactor`, `chore`, `docs`, dan `test`.
- Gunakan huruf kecil dan dash, bukan spasi atau underscore.
- Branch yang sudah dipakai PR tidak perlu di-rename kecuali reviewer meminta eksplisit.

Contoh branch:

```text
(nama)/fix/login-validation-error
(nama)/feat/user-profile-page
(nama)/refactor/order-service-layer
(nama)/chore/update-project-dependencies
```

## Commit Message

- Format tetap mengikuti Conventional Commits: `type(domain): ringkasan perubahan`.
- Ringkasan boleh natural seperti gaya tim, tetapi tetap jelas mencakup perubahan utama.
- Gunakan `fix` untuk bug, `feat` untuk fitur baru, `refactor` untuk perubahan struktur tanpa ubah behavior, `chore` untuk config/dependency, `docs` untuk dokumentasi, dan `test` untuk testing.
- Kalau commit mencakup banyak file dalam satu konteks, pakai ringkasan yang mencakup semua perubahan penting.

Contoh commit:

```text
fix(auth): fix validation login user
feat(profile): add halaman edit profil
refactor(order): pisah logic order ke service
chore(deps): update dependency minor project
```

Hindari commit terlalu umum:

```text
fix bug
update
wip
tes
```

## Pull Request Title

- Format title PR mengikuti pola tim. Jika belum ada pola, gunakan: `[TARGET] source-branch : ringkasan perubahan`.
- Target bisa `[STAGING]`, `[MAIN]`, `[DEV]`, atau nama environment lain sesuai workflow repo.
- Ringkasan PR boleh natural dan humanize, tetapi tetap menjelaskan inti perubahan.
- Sebelum create PR, cek contoh PR terbaru agar format tetap konsisten dengan tim.
- Jika reviewer meminta penyesuaian nama PR, cukup update title PR.

Contoh PR title:

```text
[STAGING] (nama)/fix/login-validation-error : Perbaiki validasi error login
[STAGING] (nama)/feat/user-profile-page : Tambah halaman edit profil user
[MAIN] (nama)/refactor/order-service-layer : Rapikan logic order ke service layer
[DEV] (nama)/chore/update-project-dependencies : Update dependency minor project
```

## Pull Request Description

- Deskripsi PR dibuat singkat, natural, dan langsung menjelaskan perubahan utama.
- Jangan terlalu kaku seperti laporan teknis panjang jika PR tim lain memakai gaya sederhana.
- Tulis test yang benar-benar sudah dijalankan.
- Jika tidak ada migration, tulis `Tidak ada migration`, bukan checklist rollback yang tidak relevan.

Template:

```markdown
## Apa yang berubah?

Jelaskan perubahan utama secara singkat dan konkret.

## Kenapa perlu berubah?

Jelaskan masalah, kebutuhan fitur, alasan teknis, atau konteks bisnis yang membuat perubahan ini diperlukan.

## Cara test

1. Buka halaman atau endpoint terkait.
2. Jalankan skenario utama.
3. Pastikan hasil sesuai ekspektasi.

## Checklist

- [x] Sudah di-test sesuai area perubahan
- [x] Tidak ada error console, log, atau warning tidak perlu
- [x] Tidak ada hardcoded credential atau API key
- [x] Tidak ada migration, atau migration sudah dicek bila ada
```

## Laporan Setelah Pull Request

Setelah PR dibuat, kirim laporan singkat ke grup, mentor, reviewer, atau task tracker dengan title PR dan link PR.

Contoh:

```text
[STAGING] fix validation error login
https://github.com/owner/repository/pull/123
```

## Daily Report

Daily report minimal 3 item atau mengikuti aturan tempat kerja. Bahasanya harus singkat, humanize, dan langsung menjelaskan pekerjaan yang dilakukan.

Contoh daily report:

```text
1. fix validation error login user
2. add handling response gagal dari API
3. fix tampilan pesan error pada form
4. Menjalankan test manual untuk flow login
5. Update deskripsi PR sesuai review
```
