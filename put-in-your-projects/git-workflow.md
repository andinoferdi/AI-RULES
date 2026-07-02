# Git Workflow

Project `[PROJECT_NAME]` memakai GitHub Flow. `[MAIN_BRANCH]` adalah branch production/source of truth yang harus selalu stabil.

## Aturan paling penting
Jangan push langsung ke `[MAIN_BRANCH]`. Semua perubahan lewat Pull Request: branch dari `[MAIN_BRANCH]`, PR ke `[STAGING_BRANCH]` untuk review/testing, lalu setelah clear baru PR ke `[MAIN_BRANCH]`.

## Naming
Format: `type/deskripsi-singkat-dengan-dash`. Jika gaya tim memakai prefix nama: `[USERNAME]/type/deskripsi-singkat`.

| Type | Untuk |
| --- | --- |
| `feat` / `feature` | Fitur baru |
| `fix` | Bug fix tidak urgent |
| `hotfix` | Fix critical di production |
| `refactor` | Refactor tanpa ubah behavior |
| `chore` | Config, dependency, dan sejenisnya |

Gunakan huruf kecil dan dash, bukan underscore atau spasi. Nama harus deskriptif tanpa konteks tambahan.

## Alur kerja
```bash
# 1. Mulai dari branch utama terbaru
git checkout [MAIN_BRANCH]
git pull origin [MAIN_BRANCH]
git checkout -b fix/deskripsi-singkat

# 2. Commit kecil dan sering, satu konteks per commit
git add -p
git commit -m "fix(domain): ringkasan perubahan"

# 3. Push dan buka PR ke [STAGING_BRANCH]
git push origin fix/deskripsi-singkat
```

Buka PR (base: `[STAGING_BRANCH]`, compare: branch fitur). Setelah testing di staging clear, buka PR baru ke `[MAIN_BRANCH]`. Setelah merge, hapus branch:

```bash
git push origin --delete fix/deskripsi-singkat
git branch -d fix/deskripsi-singkat
```

## Commit message
Conventional Commits: `type(domain): deskripsi singkat`. Gunakan imperative mood ("tambah validasi", bukan "menambahkan"). Bayangkan melanjutkan "commit ini akan ...".

Baik: `feat: tambah retry logic untuk timeout API` / `fix: harga tidak terbagi rata saat diskon`.
Buruk: `fix bug`, `update`, `wip`, `asdfgh`.

## Pull Request
- Satu PR = satu concern. Jangan campur fitur baru dengan refactor besar.
- Minimal 1 approval sebelum merge ke `[MAIN_BRANCH]`. CI wajib hijau.
- Resolve semua comment sebelum merge.
- Tulis test yang benar-benar sudah dijalankan. Jika tidak ada migration, tulis "Tidak ada migration".

Template deskripsi:

```markdown
## Apa yang berubah?
[ringkasan perubahan utama]

## Kenapa perlu berubah?
[konteks masalah sebelumnya]

## Cara test
1. [langkah verifikasi]

## Checklist
- [ ] Sudah di-test di staging
- [ ] Tidak ada console error atau log tak perlu
- [ ] Migration sudah dicek bila ada
- [ ] Tidak ada hardcoded credential atau API key
```

## Handling conflict
Sync branch dari branch utama pakai merge, bukan rebase (rebase menulis ulang history dan berbahaya bila branch sudah di-push).

```bash
git checkout [MAIN_BRANCH]
git pull origin [MAIN_BRANCH]
git checkout fix/deskripsi-singkat
git merge [MAIN_BRANCH]
# resolve conflict, lalu:
git add .
git commit -m "chore: merge [MAIN_BRANCH] into fix/deskripsi-singkat"
git push origin fix/deskripsi-singkat
```

Sync setidaknya tiap 2-3 hari untuk task panjang agar conflict tidak menumpuk.

## Yang tidak boleh
- Force push ke branch yang sudah di-share tanpa koordinasi. Gunakan `--force-with-lease` hanya di branch sendiri.
- Commit credential, API key, file environment, private key, atau secret. Sekali ter-commit, dianggap compromised meski dihapus.
- Merge ke `[MAIN_BRANCH]` tanpa test di staging dulu.
- Branch dari branch orang lain tanpa alasan jelas (PR akan membawa semua commit branch itu). Selalu branch dari `[MAIN_BRANCH]`.
- Menggabungkan fitur besar, refactor besar, dan bug fix kecil dalam satu PR.
