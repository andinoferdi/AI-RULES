# Git Workflow Guide

Berlaku untuk semua project yang memakai Git dan Pull Request. Workflow default yang disarankan adalah GitHub Flow, dengan `main` sebagai branch production atau source of truth utama.

## Aturan Paling Penting

`main` adalah branch utama yang harus selalu stabil. Jangan push langsung ke `main`. Semua perubahan wajib melalui Pull Request, kecuali repository secara eksplisit memiliki aturan berbeda.

## 1. Overview

Tim menggunakan workflow berbasis branch sederhana. Semua pekerjaan dilakukan di branch kerja, lalu dibuka Pull Request sebelum masuk ke branch utama atau branch target environment.

| Branch | Fungsi | Deploy ke |
| --- | --- | --- |
| `main` | Source of truth, selalu stable | Production |
| `develop` / `dev` | Integrasi fitur sebelum staging, jika repo memakainya | Development |
| `staging` | Testing sebelum production, jika repo memakainya | Staging |
| `feature/*` | Pengembangan fitur baru | Target sesuai workflow |
| `fix/*` | Bug fix non-critical | Target sesuai workflow |
| `hotfix/*` | Fix critical di production | Production, expedited |

## 2. Naming Convention

Format:

```text
type/deskripsi-singkat-dengan-dash
```

| Type | Digunakan untuk | Contoh |
| --- | --- | --- |
| `feature` | Fitur baru | `feature/user-profile-page` |
| `fix` | Bug fix tidak urgent | `fix/login-validation-error` |
| `hotfix` | Fix critical di production | `hotfix/payment-timeout-crash` |
| `refactor` | Refactor tanpa ubah behavior | `refactor/order-service-layer` |
| `chore` | Config, dependency update, dan sejenisnya | `chore/update-dependencies` |

Gunakan huruf kecil dan dash, bukan underscore atau spasi. Nama branch harus cukup deskriptif agar bisa dipahami tanpa konteks tambahan.

## 3. Alur Kerja Lengkap

### Step 1 - Buat branch dari branch utama yang up-to-date

Selalu mulai dari branch utama terbaru, biasanya `main`, `develop`, atau `staging` sesuai workflow repo. Jangan branch dari branch orang lain kecuali ada alasan teknis yang jelas.

```bash
git checkout main
git pull origin main
git checkout -b feature/nama-fitur
```

### Step 2 - Kerjakan fitur dan commit secara rutin

Commit kecil dan sering lebih baik daripada satu commit besar di akhir. Tiap commit sebaiknya punya satu konteks perubahan yang jelas dan bisa dipahami dari pesannya.

```bash
git add -p
git commit -m "feat: tambah validasi form profil"
```

Gunakan `git add -p` bila memungkinkan agar perubahan yang masuk commit lebih intentional daripada `git add .`.

### Step 3 - Push dan buka PR ke branch target

Push branch ke remote, lalu buka PR ke branch target sesuai workflow repo.

```bash
git push origin feature/nama-fitur
```

Buka PR di GitHub atau platform Git lain:

- Base: `staging`, `develop`, atau `main` sesuai aturan repo
- Compare: `feature/nama-fitur`

### Step 4 - Testing di environment target dan perbaikan

Setelah PR diuji atau branch masuk environment testing, jalankan test sesuai area perubahan. Kalau ada bug, commit fix ke branch yang sama selama PR masih relevan.

```bash
git commit -m "fix: handle empty state saat data kosong"
git push origin feature/nama-fitur
```

Jika workflow repo membutuhkan PR berjenjang, lanjutkan dari `develop` ke `staging`, lalu dari `staging` ke `main`.

### Step 5 - Setelah testing clear, buka PR ke `main`

Buka PR baru jika workflow repo memakai promosi branch bertahap:

- Base: `main`
- Compare: `feature/nama-fitur`, `staging`, atau branch release sesuai aturan repo

Tunggu approval dari reviewer sebelum merge.

CI harus hijau sebelum merge. Kalau CI merah, fix dulu sebelum meminta reviewer melakukan override.

### Step 6 - Setelah merge, hapus branch

Branch yang sudah di-merge ke branch akhir tidak perlu dipertahankan, kecuali repo punya aturan release branch tertentu.

```bash
# Hapus remote branch, bisa juga via tombol di platform Git
git push origin --delete feature/nama-fitur

# Hapus local branch
git branch -d feature/nama-fitur
```

## 4. Commit Message

Gunakan format Conventional Commits:

```text
type(domain): deskripsi singkat
```

| Type | Kapan dipakai | Contoh |
| --- | --- | --- |
| `feat` | Fitur baru | `feat(auth): tambah login dengan email` |
| `fix` | Perbaikan bug | `fix(order): handle data kosong saat checkout` |
| `refactor` | Refactor tanpa ubah behavior | `refactor(api): pisahkan logic ke service` |
| `chore` | Dependency, config, dan sejenisnya | `chore: update dependency project` |
| `docs` | Perubahan dokumentasi | `docs: tambah panduan setup lokal` |
| `test` | Tambah atau perbaiki test | `test: tambah test validasi login` |
| `style` | Formatting tanpa ubah logika | `style: rapikan format komponen` |

Gunakan imperative mood: `tambah validasi`, bukan `menambahkan validasi`. Bayangkan kalimatnya melanjutkan `commit ini akan ...`.

Contoh commit yang baik:

```text
feat: tambah filter status pada dashboard
fix: data kosong tidak lagi membuat halaman error
refactor: pisahkan logic mapping ke service class
```

Contoh commit yang buruk:

```text
fix bug
update
wip
asdfgh
tes1
tes2
```

## 5. Pull Request

Template deskripsi PR bersifat opsional, tetapi sangat disarankan.

```markdown
## Apa yang berubah?

Deskripsi singkat perubahan yang dilakukan.

## Kenapa perlu berubah?

Konteks: bug yang diperbaiki, fitur yang diminta, atau alasan teknis perubahan.

## Cara test

1. Buka halaman atau endpoint terkait.
2. Lakukan skenario utama.
3. Ekspektasi: hasil sesuai kebutuhan.

## Checklist

- [ ] Sudah di-test sesuai area perubahan
- [ ] Tidak ada console error atau log yang tidak perlu
- [ ] Migration sudah dicek bila ada
- [ ] Tidak ada hardcoded credential atau API key
```

Aturan review:

- Minimal 1 approval dari reviewer, senior developer, atau tech lead sebelum merge ke branch utama.
- CI harus hijau. Jangan merge kalau build atau test merah.
- Resolve semua comment sebelum merge. Kalau tidak setuju, diskusikan.
- Satu PR = satu concern. Jangan campur fitur baru dengan refactor besar.

## 6. Aturan Wajib

Aturan berikut sebaiknya di-enforce melalui branch protection atau aturan repository.

- Push langsung ke `main` diblokir.
- Semua perubahan wajib melalui PR.
- CI wajib hijau sebelum merge.
- Minimal 1 review approval untuk branch penting.
- Branch harus up-to-date sebelum merge jika repo mewajibkan.

## 7. Handling Conflict

Kalau dua branch mengubah file yang sama, conflict bisa terjadi saat merge. Semakin lama branch tidak di-sync ke branch utama, semakin besar kemungkinan conflict.

### Cara sync branch ke branch utama terbaru

```bash
# Pastikan branch utama local up-to-date
git checkout main
git pull origin main

# Kembali ke feature branch, merge dari main
git checkout feature/nama-fitur
git merge main

# Resolve conflict di editor, lalu
git add .
git commit -m "chore: merge main into feature/nama-fitur"
git push origin feature/nama-fitur
```

Gunakan merge untuk sync rutin jika branch sudah di-push atau dikerjakan bersama. Rebase hanya digunakan jika tim memang menyepakati workflow rebase.

### Frekuensi sync yang disarankan

Lakukan sync branch setidaknya setiap 2 sampai 3 hari untuk task yang panjang, terutama kalau banyak branch lain masuk ke branch utama.

## 8. Yang Tidak Boleh Dilakukan

- Force push ke branch yang sudah di-share tanpa koordinasi.
- Commit credential, API key, file `.env`, private key, atau secret lain.
- Merge tanpa test yang relevan.
- Branch dari branch orang lain tanpa alasan yang jelas.
- Membiarkan branch idle terlalu lama tanpa sync.
- Menggabungkan fitur besar, refactor besar, dan bug fix kecil dalam satu PR.

Kalau ada pertanyaan, diskusikan di channel tim atau langsung ke reviewer/tech lead.
