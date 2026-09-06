# Git Workflow

Panduan workflow Git untuk project ini.

File ini bersifat:

* repository-aware,
* hosting-agnostic,
* branch-strategy-agnostic,
* CI-aware,
* team-process-aware,
* dan coding-agent-aware.

Jangan mengasumsikan repository memakai:

* GitHub Flow,
* Git Flow,
* trunk-based development,
* staging branch,
* develop branch,
* release branch,
* Pull Request,
* Merge Request,
* squash merge,
* merge commit,
* rebase,
* remote bernama `origin`,
* atau default branch bernama `main`

sebelum memeriksa repository dan workflow yang benar-benar berlaku.

## 1. Source of Truth

Untuk workflow Git gunakan prioritas:

1. repository instructions,
2. branch protection / repository rules,
3. CI/CD configuration,
4. contribution guide,
5. documented team workflow,
6. hosting configuration,
7. existing repository convention,
8. fallback dari file ini.

Contoh source:

* `AGENTS.md`
* `CONTRIBUTING.md`
* `README.md`
* `.github/`
* `.gitlab/`
* CI workflow
* branch rules
* CODEOWNERS
* pull request template
* merge request template
* commitlint config
* release tooling
* `git-naming.md`
* `git-branch-tips.md`

Jangan menerapkan fallback file ini jika repository sudah memiliki workflow yang lebih spesifik.

## 2. Deteksi Workflow Dulu

Sebelum membuat branch atau menentukan integration strategy:

pahami kondisi repository.

Gunakan inspection read-only bila relevan:

```bash
git status --short --branch
git remote -v
git branch -vv
git log --oneline --decorate -n 20
```

Jika perlu:

```bash
git remote show [REMOTE]
```

Periksa juga:

* branch protection,
* required status checks,
* approval rules,
* merge strategy,
* default branch,
* release workflow,
* dan CI.

Jangan menebak `[MAIN_BRANCH]`, `[STAGING_BRANCH]`, atau `[REMOTE]`.

## 3. Terminologi Branch

Gunakan istilah generik:

`[BASE_BRANCH]`

Branch tempat work branch dibuat.

`[WORK_BRANCH]`

Branch tempat perubahan task dikerjakan.

`[TARGET_BRANCH]`

Branch tujuan PR/MR atau integration.

`[DEFAULT_BRANCH]`

Default branch repository.

`[INTEGRATION_BRANCH]`

Jika project memang memiliki branch integrasi.

`[RELEASE_BRANCH]`

Jika project memiliki release branch.

`[HOTFIX_BRANCH]`

Jika workflow project memang memakai pola khusus hotfix.

Tidak semua repository membutuhkan semua tipe branch.

## 4. Jangan Mengklaim Workflow Tertentu Tanpa Bukti

Jangan menulis:

"Project memakai GitHub Flow"

hanya karena repository ada di GitHub.

Hosting provider dan branching strategy adalah dua hal berbeda.

GitHub Flow sendiri merupakan lightweight branch-based workflow.

Jika project menggunakan:

feature
->
staging
->
production

itu dapat disebut workflow project sendiri atau integration/staging workflow.

Jangan memberi label metodologi populer jika struktur sebenarnya berbeda.

## 5. Workflow yang Mungkin Ditemukan

Repository dapat memakai:

* GitHub Flow,
* GitLab Flow,
* trunk-based development,
* Git Flow,
* release branches,
* environment branches,
* stacked branches,
* fork workflow,
* monorepo-specific workflow,
* direct-to-trunk dengan review automation,
* atau custom workflow.

Jangan memilih salah satu hanya karena agent lebih familiar.

## 6. Default Branch Bukan Selalu Production

Jangan menganggap default branch otomatis:

* production,
* deployed,
* stable release,
* atau source deployment.

Project dapat deploy dari:

* release tag,
* release branch,
* environment branch,
* deployment artifact,
* atau pipeline tertentu.

Periksa deployment config.

## 7. Protected Branch

Jika branch memiliki protection/rules:

ikuti aturan tersebut.

GitHub protected branches dapat mewajibkan:

* pull request review,
* status checks,
* conversation resolution,
* signed commits,
* linear history,
* deployment success,
* atau pembatasan push/force push.

GitLab protected branches juga dapat membatasi:

* siapa yang boleh push,
* siapa yang boleh merge,
* force push,
* Code Owner approval,
* dan approval rules.

Jangan menduplikasi policy tersebut dengan aturan hardcoded yang berbeda.

## 8. Direct Push

Jangan membuat aturan universal:

"semua direct push dilarang."

Gunakan branch protection dan team policy sebagai authority.

Untuk protected/default/release branch:

hindari direct push jika repository mewajibkan review.

Untuk repository kecil atau personal:

direct push dapat valid jika workflow memang mengizinkannya.

Coding agent tidak boleh melakukan push hanya karena local implementation selesai.

## 9. Pull Request / Merge Request

Gunakan istilah sesuai hosting:

GitHub:
Pull Request.

GitLab:
Merge Request.

Platform lain:
ikuti terminology platform.

Dalam template universal:

gunakan `PR/MR`.

## 10. Approval

Jangan hardcode:

"minimal satu approval."

Approval requirement berasal dari repository policy.

GitHub dapat dikonfigurasi dengan jumlah approval tertentu melalui branch protection.

GitLab juga mendukung approval rules dengan jumlah approver yang dapat dikonfigurasi per project atau branch.

Jika repository tidak mewajibkan approval:

jangan mengarang requirement.

## 11. Required Checks

Jika repository memiliki required checks:

semua required checks harus memenuhi policy sebelum merge.

GitHub status checks dapat berasal dari:

* build,
* test,
* code scanning,
* deployment,
* atau external system.

Jangan menyebut:

"CI hijau"

secara generik jika project memiliki beberapa check dengan semantics berbeda.

Gunakan nama check sebenarnya bila perlu.

## 12. Strict vs Loose Update Requirement

Beberapa repository mewajibkan branch tetap up-to-date dengan target sebelum merge.

Beberapa tidak.

GitHub branch protection mendukung strict maupun loose required status checks.

Jangan memaksa sync branch setiap beberapa hari jika repository tidak membutuhkan itu.

## 13. Mulai Task

Jika task membutuhkan branch baru:

1. Tentukan base branch.
2. Refresh remote refs jika diperlukan.
3. Pastikan working tree tidak memiliki perubahan yang akan tertimpa.
4. Buat work branch.

Contoh:

```bash
git fetch [REMOTE] --prune

git switch -c [WORK_BRANCH] [REMOTE]/[BASE_BRANCH]
```

Gunakan naming dari `git-naming.md`.

Jangan membuat branch baru jika environment agent sudah menyediakan isolated worktree/branch.

## 14. Existing Branch

Jika user meminta melanjutkan branch existing:

jangan membuat branch baru tanpa alasan.

Periksa:

```bash
git status --short --branch
git branch -vv
```

Gunakan state saat ini sebagai baseline.

## 15. Working Tree Safety

Sebelum operasi yang dapat mengubah branch/history:

periksa working tree.

Jangan:

* reset,
* checkout-overwrite,
* clean,
* stash,
* restore,
* atau discard

perubahan user tanpa izin dan pemahaman yang jelas.

## 16. Commit Tidak Harus Banyak atau Sedikit

Jangan membuat aturan:

"commit kecil dan sering"

sebagai ukuran mekanis.

Commit harus memiliki concern yang jelas dan reviewable.

Satu task dapat:

* satu commit,
* beberapa commit,
* atau belum perlu commit sama sekali.

Kualitas history lebih penting daripada jumlah commit.

## 17. Staging Git

Gunakan staging secara selektif bila membantu:

```bash
git add -p
```

tetapi tidak wajib untuk setiap commit.

Jika seluruh file memang satu logical change:

```bash
git add path/to/file
```

dapat lebih tepat.

Jangan menggunakan:

```bash
git add .
```

secara buta jika working tree memiliki unrelated changes.

## 18. Commit Convention

Ikuti `git-naming.md` dan repository convention.

Jangan memaksa Conventional Commits jika project tidak menggunakannya.

Jika project memang menggunakan Conventional Commits:

ikuti specification dan tooling project.

## 19. Jangan Commit Tanpa Izin

Coding agent tidak otomatis membuat commit.

Commit dilakukan jika:

* user meminta,
* task mencakup commit,
* environment workflow mengharuskan,
* atau repository instructions menyatakan demikian.

Jika user hanya meminta code change:

working tree diff dapat menjadi output final.

## 20. Sinkronisasi Branch

Tidak ada satu command universal untuk sync.

Pilihan umum:

* merge,
* rebase,
* fast-forward,
* reset/rebuild,
* cherry-pick,
* atau tidak perlu sync.

Pilih berdasarkan repository policy dan tujuan.

## 21. Merge

Merge cocok ketika:

* history branch ingin dipertahankan,
* branch shared,
* workflow memakai merge commits,
* atau project secara eksplisit memilih merge.

Git merge mengintegrasikan histories tanpa menulis ulang commit existing.

## 22. Rebase

Rebase cocok ketika:

* branch milik sendiri,
* linear history diinginkan,
* project mengizinkannya,
* dan konsekuensi history rewrite dipahami.

Git rebase memindahkan/replay commit ke base baru.

Jangan menggunakan rebase pada shared branch tanpa koordinasi.

## 23. Published Branch Tidak Otomatis Anti-Rebase

Jangan membuat aturan:

"branch yang sudah di-push tidak boleh rebase."

Lebih tepat:

published branch boleh direbase jika:

* ownership jelas,
* branch tidak digunakan orang lain sebagai base,
* repository workflow mengizinkan,
* dan update remote dilakukan dengan aman.

Shared branch sebaiknya tidak direwrite tanpa koordinasi.

## 24. Cherry-Pick

Gunakan cherry-pick jika:

* hanya commit tertentu dibutuhkan,
* backport,
* hotfix propagation,
* atau rebuild branch.

Jangan cherry-pick banyak commit hanya untuk meniru merge tanpa alasan.

## 25. Rebuild Branch

Gunakan rebuild jika:

* base salah,
* history tercampur,
* target berubah ekstrem,
* atau diff membawa banyak commit tidak terkait.

Rebuild adalah recovery strategy.

Bukan workflow default.

## 26. Conflict

Saat conflict:

jangan memilih `ours` atau `theirs` secara mekanis.

Pahami final intended state.

Gunakan:

```bash
git status
```

Periksa setiap file konflik.

Pertahankan:

* target behavior yang benar,
* contract terbaru,
* task change yang memang diperlukan,
* dan baseline update yang valid.

## 27. Conflict Bukan Alasan Membuat Commit Otomatis

Setelah merge conflict resolution:

merge commit memang dapat diperlukan jika menggunakan merge.

Setelah rebase:

lanjutkan rebase, jangan membuat unrelated manual merge commit.

Gunakan command sesuai operation:

```bash
git merge --continue
```

atau commit sesuai Git version/workflow,

```bash
git rebase --continue
```

```bash
git cherry-pick --continue
```

Jangan menggunakan satu recipe untuk semua conflict.

## 28. Abort

Jika operation ternyata salah:

```bash
git merge --abort
```

```bash
git rebase --abort
```

```bash
git cherry-pick --abort
```

Gunakan sesuai state aktif.

Jangan menggunakan `reset --hard` sebagai escape hatch jika abort tersedia.

## 29. Sync Frequency

Jangan menetapkan:

"sync setiap 2–3 hari."

Frequency bergantung pada:

* activity target branch,
* task duration,
* conflict risk,
* strict status check policy,
* stacked dependency,
* dan team workflow.

Sync ketika memberi nilai.

## 30. Branch dari Branch Lain

Jangan membuat aturan:

"selalu branch dari main."

Stacked development, dependent feature, atau release work dapat memerlukan parent branch lain.

Gunakan base yang benar untuk task.

Jika branch dari branch lain tidak disengaja:

perbaiki sebelum PR/MR jika history menjadi salah.

## 31. Stacked Branch

Jika project menggunakan stacked branches:

child branch memang dapat bergantung pada parent.

Jangan rebase child langsung ke root hanya untuk memenuhi generic rule.

Pertahankan dependency chain sampai parent merge atau workflow menginstruksikan update.

## 32. Staging / Integration Branch

Jika project memiliki `[INTEGRATION_BRANCH]`:

pahami fungsinya.

Ia dapat digunakan untuk:

* testing,
* QA,
* integration,
* pre-production,
* release candidate,
* atau deployment.

Jangan menganggap semua perubahan wajib melewati staging sebelum target lain kecuali workflow project memang menetapkannya.

## 33. Environment Branches

Jika branch merepresentasikan environment:

jangan otomatis menganggap branch tersebut ideal.

Tetapi jangan menghapus workflow hanya karena generic best practice lain lebih populer.

Ikuti project yang ada kecuali user meminta redesign workflow.

## 34. Pull Sebelum Mulai

Jangan gunakan:

```bash
git pull [REMOTE] [BRANCH]
```

secara mekanis.

`git pull` melakukan fetch dan kemudian integrasi.

Gunakan `git fetch` bila ingin melihat remote state tanpa langsung merge/rebase.

Jika branch lokal hanya tracking branch tanpa commit lokal:

```bash
git pull --ff-only
```

dapat menjadi pilihan aman jika workflow sesuai.

## 35. Fetch

`git fetch` biasanya lebih aman untuk inspection karena tidak langsung mengubah current branch history.

Gunakan:

```bash
git fetch [REMOTE] --prune
```

jika remote access tersedia dan refresh diperlukan.

Jangan fetch berulang tanpa kebutuhan.

## 36. Remote

Jangan menganggap remote selalu `origin`.

Periksa:

```bash
git remote -v
```

Repository fork dapat memiliki:

* origin,
* upstream,
* company,
* mirror,
* atau remote lain.

## 37. Fork Workflow

Jika contributor memakai fork:

source branch dapat berada di fork.

Target PR/MR dapat berada di upstream repository.

Jangan mengasumsikan push langsung ke repository utama tersedia.

## 38. Branch Protection

Jangan mencoba bypass:

* required review,
* required check,
* Code Owner,
* merge queue,
* signed commit,
* linear history,
* deployment requirement

hanya supaya task agent cepat selesai.

Repository policy menang.

## 39. Merge Strategy

Repository dapat menggunakan:

* merge commit,
* squash merge,
* rebase merge,
* fast-forward,
* merge queue

atau kombinasi.

Ikuti repository configuration.

Jangan mengubah commit history hanya untuk menyesuaikan preference agent.

## 40. Squash Merge

Jika project squash-merges PR/MR:

commit lokal tidak harus sempurna sebagai permanent history.

Namun tetap jaga commit cukup jelas untuk review.

PR/MR title mungkin menjadi final commit subject tergantung hosting config.

## 41. Linear History

Jika project mewajibkan linear history:

gunakan integration strategy yang memenuhi rule tersebut.

GitHub protected branch dapat mewajibkan linear history.

Jangan membuat merge commit pada branch yang policy-nya menolak merge commit.

## 42. Merge Queue

Jika repository memakai merge queue:

ikuti queue workflow.

Jangan merge manual di luar queue jika protection mengharuskan queue.

## 43. Validation Sebelum PR/MR

Sebelum membuat atau memperbarui PR/MR:

review:

```bash
git status --short
git diff --check
```

Lihat diff terhadap target:

```bash
git diff --stat [REMOTE]/[TARGET_BRANCH]...HEAD
git diff --name-only [REMOTE]/[TARGET_BRANCH]...HEAD
```

Jalankan validation code yang relevan sesuai project.

## 44. Required Validation

Jangan hardcode:

* staging test,
* lint,
* build,
* atau full suite

sebagai universal.

Ikuti:

* repository checks,
* task risk,
* blast radius,
* dan CI policy.

Jika project memiliki required checks:

prioritaskan check tersebut.

## 45. PR/MR Description

Ikuti PR/MR template repository.

Hanya tulis:

* perubahan nyata,
* test yang benar-benar dijalankan,
* migration jika relevan,
* risk/limitation bila perlu.

Jangan menulis checklist yang belum diverifikasi.

## 46. Migration

Migration hanya disebut jika:

* ada database,
* ada migration,
* atau reviewer memang perlu mengetahui status migration.

Jangan selalu menulis:

"Tidak ada migration"

pada project tanpa database.

## 47. Review Comments

Jangan membuat aturan:

"semua comment harus resolved"

secara universal.

Jika repository policy mensyaratkan conversation resolution:

ikuti.

Jika tidak:

reviewer/author dapat memiliki workflow berbeda.

GitHub branch protection memang dapat mewajibkan conversation resolution jika dikonfigurasi.

## 48. Push

Push adalah remote side effect.

Jangan push otomatis hanya karena local task selesai.

Push hanya jika:

* user meminta,
* task mencakup remote update,
* atau environment workflow mengizinkan.

Sebelum push:

periksa remote dan branch tujuan.

## 49. Force Push

Jangan gunakan plain:

```bash
git push --force
```

sebagai default.

History rewrite berpotensi menghapus remote commits.

Jika published personal branch perlu direwrite:

gunakan safer mechanism sesuai workflow, biasanya:

```bash
git push --force-with-lease
```

tetapi tetap perlakukan sebagai history rewrite.

Jangan force-push shared/protected branch tanpa policy eksplisit.

## 50. Shared Branch

Anggap branch shared jika orang/agent lain mungkin bergantung pada commit history-nya.

Jangan:

* rebase,
* reset,
* force push,
* drop commit

tanpa koordinasi.

## 51. Delete Branch

Jangan menghapus local/remote branch otomatis setelah merge.

Beberapa workflow auto-delete branch.

Beberapa mempertahankannya.

Hapus jika:

* user meminta,
* repository workflow memang melakukannya,
* dan branch sudah tidak diperlukan.

Remote branch deletion adalah remote side effect.

## 52. Hotfix

Jangan mengasumsikan project memiliki special hotfix flow.

Jika hotfix policy ada:

ikuti.

Jika tidak:

bug production dapat memakai work branch normal dengan priority tinggi.

Jangan menciptakan release/hotfix infrastructure hanya karena nama branch `hotfix` tersedia.

## 53. Release Branch

Jika project menggunakan release branches:

ikuti version/release process.

Jangan merge feature baru ke release branch kecuali workflow mengizinkan.

Jangan membuat release branch untuk project yang melakukan continuous delivery tanpa release branches.

## 54. Tags

Tagging bukan bagian otomatis task coding.

Tag hanya jika:

* release workflow membutuhkan,
* user meminta,
* atau automation memang melakukannya.

Jangan membuat version tag secara manual jika release system dikelola bot.

## 55. CI/CD

Pahami kapan pipeline berjalan.

CI dapat dipicu oleh:

* push,
* PR/MR,
* tag,
* schedule,
* manual run,
* merge queue,
* path filter.

Jangan push hanya untuk "melihat CI" jika local validation cukup dan task tidak meminta remote effect.

## 56. Protected CI Variables

Jika platform memiliki protected secrets/runners:

jangan mencoba mengubah branch protection untuk mendapatkan akses.

GitLab misalnya membatasi akses protected variables/runners berdasarkan protection dan permission tertentu.

## 57. Secrets

Jangan commit:

* API key,
* password,
* token,
* private key,
* secret,
* credential,
* sensitive `.env`.

Jika secret terlanjur committed:

anggap potentially compromised sesuai incident procedure project.

Menghapus file dari commit terbaru tidak otomatis membersihkan history.

## 58. `.env`

Jangan membuat aturan:

"semua file environment tidak boleh commit."

Beberapa project sengaja commit:

* `.env.example`,
* `.env.test`,
* template config tanpa secret.

Yang dilarang adalah secret atau sensitive credential sesuai project policy.

## 59. Generated Files

Jangan commit generated output jika repository memang mengabaikannya.

Tetapi jangan menghapus generated file dari Git jika project sengaja version-control output tersebut.

Ikuti `.gitignore` dan repository convention.

## 60. Submodule / Subtree

Jika repository memakai Git submodule atau subtree:

pahami boundary sebelum commit.

Jangan mengedit dependency repository seolah-olah bagian source tree biasa.

## 61. Monorepo

Untuk monorepo:

satu PR/MR dapat menyentuh beberapa packages jika satu logical change memang lintas package.

Jangan memaksa:

"satu PR = satu folder."

Concern lebih penting daripada folder count.

## 62. Satu PR/MR = Satu Concern

Prinsip ini tetap baik sebagai default:

hindari mencampur perubahan tak terkait.

Tetapi satu concern dapat melibatkan:

* backend,
* frontend,
* schema,
* tests,
* docs

sekaligus jika semuanya diperlukan untuk satu feature/fix.

Jangan memecah perubahan end-to-end secara artifisial.

## 63. Large PR/MR

Jika change besar:

pecah jika ada boundary logis.

Gunakan stacked PR/MR jika workflow mendukung.

Jangan memecah hanya berdasarkan jumlah line.

## 64. Draft PR/MR

Gunakan draft jika workflow dan platform mendukung serta pekerjaan belum siap review.

Jangan menganggap draft PR wajib untuk semua work-in-progress.

## 65. Reviewability

History dan PR/MR harus membantu reviewer memahami:

* tujuan,
* perubahan,
* risk,
* validation.

Jangan mengejar history "cantik" dengan rewrite berisiko yang tidak memberi manfaat nyata.

## 66. Agent Behavior

Coding agent tidak otomatis boleh:

* branch,
* commit,
* push,
* merge,
* rebase shared branch,
* force push,
* delete branch,
* create PR/MR,
* approve,
* atau merge PR/MR.

Lakukan hanya jika scope task, user, repository workflow, dan permission environment mengizinkan.

## 67. Read-Only Git Inspection

Command read-only seperti:

```bash
git status
git diff
git log
git branch
git remote -v
```

boleh digunakan untuk memahami repository tanpa confirmation tambahan selama dalam scope.

## 68. Local State Mutation

Operation seperti:

* switch branch,
* create branch,
* stage,
* commit,
* merge,
* rebase,
* cherry-pick,
* stash

mengubah local Git state.

Gunakan hanya jika membantu task dan sesuai instruction.

## 69. Destructive Git Operation

Jangan melakukan tanpa intent/izin jelas:

* `reset --hard`,
* `clean -fd`,
* force branch pointer move,
* delete branch,
* rewrite shared history,
* discard working tree changes.

Jangan menggunakan destructive operation untuk menghemat waktu.

## 70. Remote Side Effects

Termasuk:

* push,
* force push,
* delete remote branch,
* create/update PR/MR,
* merge,
* tag push.

Pastikan remote action memang diminta atau diizinkan.

## 71. User Changes

Jangan overwrite perubahan user yang sudah ada.

Jika target file dirty:

integrasikan patch secara hati-hati.

Jangan reset file hanya karena diff mengganggu agent.

## 72. Reflog

Jika local history terlihat hilang:

periksa reflog sebelum menganggap data hilang.

```bash
git reflog
```

Jangan langsung melakukan recovery destructive.

## 73. Worktrees

Jika coding agent memakai Git worktree:

periksa jika branch tidak dapat di-switch atau sudah active di lokasi lain.

```bash
git worktree list
```

Jangan force-move branch yang sedang digunakan worktree lain.

## 74. Stop Condition

Berhenti dan jangan melakukan mutating Git operation jika:

* target branch tidak jelas,
* working tree memiliki unknown user changes,
* operation akan rewrite shared history,
* protected branch policy belum diketahui,
* conflict memerlukan keputusan product yang belum jelas,
* atau remote action tidak diizinkan.

Read-only investigation tetap boleh dilakukan.

## 75. Fallback Workflow

Jika repository tidak memiliki documented Git workflow:

gunakan fallback sederhana:

1. Identifikasi default/base branch.
2. Refresh remote.
3. Buat short-lived work branch bila task membutuhkan branch.
4. Implementasikan perubahan.
5. Jalankan validation relevan.
6. Review diff.
7. Commit hanya jika diminta.
8. Push hanya jika diminta.
9. Buka PR/MR hanya jika diminta.
10. Merge mengikuti repository/platform policy.

Jangan menciptakan staging branch sendiri.

## 76. Fallback Integration

Jika project tidak memiliki preference:

untuk branch pribadi yang belum shared:

rebase atau merge dapat dipilih berdasarkan kebutuhan.

Untuk shared branch:

prefer integrasi yang tidak rewrite history kecuali team menyepakati rewrite.

Untuk protected target:

gunakan PR/MR jika platform/rules mewajibkan.

## 77. Fallback Branch Protection

Jika repository profesional/team tetapi branch policy belum jelas:

jangan mengubah protected/default branch langsung.

Gunakan work branch dan PR/MR sebagai pilihan konservatif.

Tetapi jangan mengklaim ini adalah official workflow project sampai diverifikasi.

## 78. Fallback Validation

Sebelum handoff:

```bash
git status --short
git diff --check
git diff --stat
```

Lalu jalankan project checks yang relevan.

Jangan mengklaim semua test lolos jika tidak dijalankan.

## 79. Prioritas Konflik

Urutan umum:

1. system/platform/agent constraints,
2. repository protection/rules,
3. applicable repository instructions,
4. explicit user instructions,
5. CI/CD requirements,
6. documented team workflow,
7. `git-workflow.md`,
8. `git-branch-tips.md`,
9. `git-naming.md`,
10. generic Git preference.

Jika template bertentangan dengan enforced branch policy:

enforced policy menang.

## 80. Cek Internal Sebelum Mutasi Git

Periksa secara internal:

* current branch?
* base branch?
* target branch?
* remote?
* dirty working tree?
* branch shared?
* protected?
* merge strategy?
* required checks?
* task benar-benar membutuhkan Git mutation?
* user sudah mengizinkan remote side effect?
* perubahan user aman?

Jangan tampilkan checklist ini kecuali diminta.

## 81. Cek Internal Sebelum PR/MR

Pastikan:

* diff sesuai scope,
* target branch benar,
* branch tidak membawa unrelated commit,
* naming mengikuti repo,
* validation faktual,
* migration status benar jika relevan,
* no secret,
* title sesuai final change,
* template repository diikuti.

## 82. Prinsip Akhir

Deteksi workflow, jangan menebak.

Jangan menyebut custom workflow sebagai GitHub Flow tanpa bukti.

Default branch tidak selalu production.

Staging tidak wajib.

Direct push mengikuti repository policy.

Approval mengikuti branch rules.

CI requirement mengikuti configuration.

Merge dan rebase sama-sama valid dalam konteks yang tepat.

Published personal branch dapat direbase jika workflow mengizinkan.

Shared history jangan direwrite sembarangan.

Branch boleh bergantung pada branch lain jika workflow stacked/dependent.

Commit harus reviewable, bukan sekadar banyak.

Push, PR/MR, merge, dan branch deletion adalah side effect.

Jangan melakukan remote action tanpa scope yang jelas.

Protected branch policy menang.

Jangan overengineer Git workflow.

Gunakan workflow paling sederhana yang tetap aman dan sesuai repository.
