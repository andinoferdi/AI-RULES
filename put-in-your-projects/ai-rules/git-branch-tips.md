# Git Branch Tips

Panduan praktis menjaga branch, diff, dan integration history tetap bersih.

File ini bersifat:

* hosting-agnostic,
* branch-strategy-agnostic,
* repository-aware,
* dan coding-agent-aware.

Jangan mengasumsikan repository memakai:

* `main`,
* `master`,
* `develop`,
* `staging`,
* Git Flow,
* trunk-based development,
* pull request,
* merge request,
* remote bernama `origin`,
* atau branch naming tertentu

sebelum memeriksa repository dan workflow project.

Panduan utama tetap mengikuti `git-workflow.md`, `git-naming.md`, repository instructions, dan policy remote platform yang benar-benar berlaku.

## 1. Deteksi Workflow Dulu

Sebelum membuat, memindahkan, rebase, merge, atau rewrite branch:

pahami current state.

Gunakan command read-only seperti:

```bash
git status --short --branch
git remote -v
git branch -vv
git log --oneline --decorate -n 15
```

Jika perlu mengetahui default remote branch:

```bash
git remote show [REMOTE]
```

atau periksa symbolic remote HEAD jika tersedia.

Jangan menganggap:

`origin`
atau
`main`

pasti benar.

Gunakan placeholder konseptual:

* `[REMOTE]`
* `[BASE_BRANCH]`
* `[TARGET_BRANCH]`
* `[WORK_BRANCH]`

dan isi berdasarkan repository aktual.

## 2. Pahami Jenis Branch

Bedakan bila relevan:

BASE BRANCH

Branch yang menjadi titik awal pekerjaan.

TARGET BRANCH

Branch tujuan integration atau PR/MR.

WORK BRANCH

Branch tempat perubahan task dibuat.

UPSTREAM BRANCH

Remote-tracking branch yang diikuti local branch.

RELEASE / STAGING / INTEGRATION BRANCH

Hanya jika workflow project memang memilikinya.

Satu branch dapat memiliki beberapa peran tergantung workflow.

Jangan menciptakan branch layer baru hanya karena template menyebutkannya.

## 3. Mulai dari Base yang Benar

Untuk task baru, buat work branch dari base yang memang ditetapkan project.

Refresh remote reference terlebih dahulu bila akses network dan izin tersedia:

```bash
git fetch [REMOTE] --prune
```

Lalu:

```bash
git switch -c [WORK_BRANCH] [REMOTE]/[BASE_BRANCH]
```

`git switch -c` membuat branch baru dari start point yang diberikan.

Jika Git version atau project convention masih menggunakan `checkout`, bentuk ekuivalen juga valid:

```bash
git checkout -b [WORK_BRANCH] [REMOTE]/[BASE_BRANCH]
```

Jangan mengganti command style repo hanya demi modernisasi kosmetik.

## 4. Jangan Membuat Branch Jika Tidak Perlu

Tidak setiap task membutuhkan branch baru.

Jangan membuat branch jika:

* user hanya meminta audit/read-only,
* environment agent sudah menyediakan isolated worktree/branch,
* workflow project menangani branch otomatis,
* atau user meminta bekerja pada branch sekarang.

Ikuti environment dan workflow repository.

## 5. Periksa Working Tree Sebelum Pindah Branch

Sebelum switch, rebase, reset, atau operasi yang dapat mengganggu perubahan lokal:

```bash
git status --short
```

Jangan:

* discard,
* reset,
* overwrite,
* stash,
* atau memindahkan

perubahan user tanpa kebutuhan dan izin yang jelas.

`git switch` dapat menolak perpindahan jika perubahan lokal akan hilang.

## 6. Jangan Branch dari Branch Orang Tanpa Alasan

Jika tujuan hanya mempelajari implementation branch lain:

jangan otomatis menjadikannya base.

Gunakan inspection:

```bash
git log --oneline [BASE]..[OTHER_BRANCH]
git diff [BASE]...[OTHER_BRANCH]
git show [OTHER_BRANCH]:path/to/file
```

Gunakan branch lain sebagai base hanya jika dependency workflow memang mengharuskannya.

Contoh:

stacked branch
atau
feature B memang bergantung pada feature A.

## 7. Pahami `..` dan `...`

Jangan menggunakan range syntax tanpa memahami artinya.

Untuk `git diff`:

```bash
git diff A B
git diff A..B
```

keduanya membandingkan tip A dengan tip B.

Sedangkan:

```bash
git diff A...B
```

membandingkan merge-base A/B dengan B.

Ini berguna untuk melihat perubahan yang diperkenalkan branch B sejak bercabang dari baseline.

Untuk menilai diff sebuah work branch terhadap target PR:

```bash
git diff --stat [TARGET_BRANCH]...[WORK_BRANCH]
git diff --name-only [TARGET_BRANCH]...[WORK_BRANCH]
```

biasanya lebih sesuai daripada membandingkan dua tip secara langsung.

## 8. Pilih Merge, Rebase, Cherry-Pick, atau Rebuild Berdasarkan Tujuan

Tidak ada satu strategi universal.

### Merge

Gunakan merge jika:

* project mempertahankan merge history,
* branch memang perlu menyerap keseluruhan history branch lain,
* atau workflow repository mengharuskannya.

Jangan merge hanya untuk mengambil satu perubahan kecil.

### Rebase

Gunakan rebase jika:

* workflow mengizinkan history rewrite,
* branch milik sendiri,
* tujuan menjaga branch tetap berbasis pada baseline terbaru,
* dan konsekuensi rewrite dipahami.

Jangan rebase shared branch tanpa koordinasi.

### Cherry-Pick

Gunakan cherry-pick jika:

* commit tertentu memang perlu dipindahkan,
* tidak seluruh branch diperlukan,
* dan commit tersebut cukup independen.

Jangan cherry-pick banyak commit hanya untuk meniru merge secara manual.

### Rebuild Branch

Rebuild branch dapat digunakan jika:

* history branch sudah sangat tercampur,
* diff membawa commit yang bukan milik task,
* base branch salah,
* atau integration branch berubah secara ekstrem.

Ini adalah recovery strategy.

Bukan default workflow.

## 9. Diagnosis Sebelum Rewrite

Sebelum rebase, rebuild, reset, atau force update:

periksa history.

Contoh:

```bash
git fetch [REMOTE] --prune

git merge-base [REMOTE]/[TARGET_BRANCH] HEAD

git log --oneline [REMOTE]/[TARGET_BRANCH]..HEAD

git diff --stat [REMOTE]/[TARGET_BRANCH]...HEAD
git diff --name-only [REMOTE]/[TARGET_BRANCH]...HEAD
```

Tentukan masalah sebenarnya:

* base salah,
* target berubah,
* commit asing ikut masuk,
* branch tertinggal,
* conflict,
* atau hanya diff besar yang memang bagian task.

Jangan rewrite history hanya karena diff terlihat panjang.

## 10. Rebuild Branch Secara Terkontrol

Jika rebuild memang keputusan yang tepat:

1. Pastikan commit task yang ingin dipertahankan sudah diketahui.
2. Jangan menghapus branch lama terlebih dahulu.
3. Buat branch baru dari target/base yang benar.
4. Cherry-pick hanya commit yang memang dibutuhkan.
5. Verifikasi diff.

Contoh:

```bash
git switch -c [WORK_BRANCH]-clean [REMOTE]/[TARGET_BRANCH]

git cherry-pick <task_commit_1>
git cherry-pick <task_commit_2>
```

Jangan menjalankan langkah ini jika commit yang dipertahankan belum dipastikan.

## 11. Conflict Resolution

Conflict bukan sekadar:

"pilih ours"
atau
"pilih theirs."

Pahami intended final state.

Git conflict resolution berarti menentukan konten akhir yang benar ketika Git tidak dapat menyatukan perubahan secara otomatis.

Saat conflict:

```bash
git status
```

Periksa setiap file konflik.

Pertahankan:

* perubahan baseline yang masih diperlukan,
* perubahan task yang memang dimaksudkan,
* contract baru yang valid,
* dan integration behavior yang benar.

Jangan mempertahankan file berdasarkan:

"ini branch saya"

atau

"ini branch target"

secara mekanis.

## 12. Batalkan Operasi Jika Arah Salah

Jika merge/rebase/cherry-pick sedang berlangsung dan hasilnya ternyata tidak sesuai:

gunakan mekanisme abort yang tepat sebelum membuat perubahan tambahan.

Contoh:

```bash
git merge --abort
```

```bash
git rebase --abort
```

```bash
git cherry-pick --abort
```

Pastikan command sesuai operasi yang sedang aktif.

Jangan melakukan reset destruktif hanya untuk keluar dari conflict jika mekanisme abort tersedia.

## 13. Commit Harus Reviewable

Prefer commit yang:

* memiliki satu concern utama,
* dapat dipahami reviewer,
* dapat diuji,
* dan masuk akal untuk revert/cherry-pick jika workflow membutuhkannya.

Jangan membuat satu commit raksasa tanpa alasan.

Namun jangan pula memecah perubahan menjadi commit mikro seperti:

* import package,
* rename variable,
* tambah satu line,
* formatting satu file

jika semuanya merupakan satu perubahan logis.

## 14. Ikuti Git Naming Project

Branch dan commit naming mengikuti:

* `git-naming.md`,
* repository convention,
* ticketing system,
* atau hosting workflow

yang benar-benar berlaku.

Jangan hardcode:

```text
[USERNAME]/feat/...
```

jika project memakai format lain.

Contoh format yang mungkin ditemukan:

```text
feature/...
fix/...
user/feature/...
ABC-123-description
```

Gunakan yang sudah ditetapkan repository.

## 15. Jangan Membuat Commit Otomatis Tanpa Scope yang Jelas

Coding agent tidak harus commit setiap selesai edit.

Commit hanya jika:

* user meminta,
* project workflow mengharuskan,
* atau environment agent memang ditugaskan menghasilkan commit.

Jika task hanya implementasi lokal:

perubahan working tree dapat menjadi output yang cukup.

## 16. Verifikasi Diff Sebelum Integration

Sebelum meminta PR/MR update, push, merge, atau handoff:

periksa:

```bash
git status --short

git diff --check

git diff --stat [REMOTE]/[TARGET_BRANCH]...HEAD

git diff --name-only [REMOTE]/[TARGET_BRANCH]...HEAD

git log --oneline [REMOTE]/[TARGET_BRANCH]..HEAD
```

Periksa:

* file berubah sesuai scope,
* tidak ada debug artifact,
* tidak ada secret,
* tidak ada generated file yang tidak seharusnya,
* tidak ada commit asing,
* dan tidak ada whitespace error yang tidak disengaja.

Jalankan validation code sesuai project rules.

## 17. `git pull`

Jangan menggunakan `git pull` tanpa memahami integration policy.

`git pull` melakukan fetch lalu mengintegrasikan branch remote ke branch lokal.

Pilihan integration dapat berupa:

* fast-forward only,
* rebase,
* merge,
* atau squash

tergantung command/config.

Jika tujuan hanya memperbarui local branch tanpa membuat merge/rebase otomatis:

lebih eksplisit menggunakan:

```bash
git fetch [REMOTE]
```

lalu periksa state sebelum integration.

## 18. Fast-Forward Only

Untuk local tracking branch yang seharusnya tidak memiliki commit lokal:

```bash
git pull --ff-only [REMOTE] [BRANCH]
```

dapat menjadi pilihan aman karena operation gagal jika history sudah divergen.

Jangan menggunakan `--ff-only` jika workflow memang mengharapkan local divergence dan integration lain.

## 19. Push Adalah Remote Side Effect

Jangan push hanya karena code selesai.

Push mengubah remote state.

Lakukan hanya jika:

* user meminta,
* environment workflow memberi izin,
* atau task secara eksplisit mencakup update remote.

Sebelum push:

* periksa target remote,
* branch,
* diff,
* dan working state.

## 20. Normal Push

Jika history tidak direwrite:

```bash
git push [REMOTE] HEAD:[WORK_BRANCH]
```

atau gunakan upstream configuration project.

Untuk branch baru:

```bash
git push -u [REMOTE] [WORK_BRANCH]
```

hanya jika project workflow memang menginginkan tracking branch.

## 21. Jangan Gunakan `--force` Sebagai Default

Hindari:

```bash
git push --force
```

`--force` menonaktifkan normal fast-forward protection dan dapat menghilangkan commit remote.

Jangan gunakan pada shared, protected, base, release, production, atau integration branch tanpa workflow khusus yang jelas.

## 22. `--force-with-lease` Bukan Tombol Aman Universal

Jika published work branch harus direwrite setelah:

* rebase,
* cleanup,
* atau rebuild,

`--force-with-lease` lebih aman daripada plain `--force` karena Git memeriksa expected remote state sebelum overwrite.

Contoh:

```bash
git push --force-with-lease [REMOTE] HEAD:[WORK_BRANCH]
```

Tetapi operasi ini tetap history rewrite.

Gunakan hanya jika:

* branch memang boleh direwrite,
* branch bukan shared history yang harus dipertahankan,
* remote state sudah diverifikasi,
* dan user/workflow mengizinkan push.

## 23. Caveat `--force-with-lease`

Jangan menyatakan `--force-with-lease` mustahil menghapus pekerjaan orang lain.

Dokumentasi Git mencatat varian tanpa expected SHA dapat berinteraksi buruk dengan background process yang otomatis melakukan `fetch`, karena remote-tracking ref lokal bisa berubah tanpa review manual.

Untuk workflow sangat sensitif:

verifikasi remote tip secara eksplisit sebelum rewrite.

Jangan melakukan history rewrite otomatis hanya karena lease command tersedia.

## 24. Protected Branch

Hormati branch protection/ruleset pada hosting provider.

Protected branch dapat:

* menolak force push,
* mewajibkan pull request,
* mewajibkan review,
* mewajibkan status checks,
* membatasi actor yang boleh push,
* atau mewajibkan linear history.

GitHub, misalnya, memblokir force push pada protected branch secara default.

Jangan mencoba bypass protection hanya untuk menyelesaikan task agent.

## 25. Shared Branch

Anggap branch shared jika beberapa orang/agent dapat membangun pekerjaan di atas history yang sama.

Jangan:

* rebase published shared branch,
* reset pointer,
* force push,
* atau drop commit

tanpa coordination eksplisit.

## 26. Stacked Branch

Jika project menggunakan stacked PR/branch:

jangan menerapkan rule:

"semua branch harus langsung berasal dari main."

Dependency antarbranch mungkin intentional.

Identifikasi parent branch setiap stack.

Jangan rebuild child langsung dari root branch jika itu menghilangkan dependency yang memang diperlukan.

## 27. Integration / Staging Branch

Jika project memiliki staging/integration branch yang sering berubah:

jangan otomatis merge branch tersebut ke work branch.

Tentukan tujuan terlebih dahulu.

Jika tujuan hanya memastikan diff PR tetap fokus:

bandingkan dengan target yang benar dan pertimbangkan:

* rebase,
* rebuild,
* atau target branch adjustment

sesuai workflow.

Jika seluruh integration history memang perlu masuk:

merge dapat benar.

Tidak ada larangan universal merge staging ke feature branch.

## 28. Branch yang Sering Reset

Jika suatu branch memang routinely rewritten/reset:

anggap remote tip-nya unstable.

Sebelum integration:

```bash
git fetch [REMOTE] --prune
```

kemudian ulangi:

* merge-base,
* log range,
* dan diff.

Jangan mengandalkan local remote-tracking ref lama.

## 29. Remote Bukan Selalu `origin`

Repository dapat memiliki:

```text
origin
upstream
fork
company
mirror
```

atau remote lain.

Gunakan:

```bash
git remote -v
```

untuk melihat configuration.

Jangan hardcode `origin` dalam automation universal.

## 30. Multiple Worktrees

Jika project/agent memakai Git worktree:

ingat satu local branch biasanya tidak dapat di-checkout sekaligus pada beberapa worktree.

Jangan force-move branch yang aktif pada worktree lain.

Periksa:

```bash
git worktree list
```

jika environment menunjukkan penggunaan worktree.

## 31. Jangan Gunakan `reset --hard` sebagai Shortcut

`git reset --hard` dapat menghapus perubahan working tree/index.

Jangan gunakan hanya untuk:

* membersihkan branch,
* menyelesaikan conflict,
* menyamakan branch,
* atau "mulai ulang"

tanpa izin yang jelas dan pemahaman data yang akan hilang.

## 32. Jangan Gunakan `git clean` Secara Buta

Untracked file dapat merupakan pekerjaan user.

Jangan jalankan:

```bash
git clean -fd
```

atau variant destructive lain tanpa mengetahui apa yang akan dihapus dan tanpa izin yang tepat.

## 33. Secrets

Jangan commit atau push:

* `.env` yang berisi credential,
* API key,
* token,
* private key,
* secret,
* debug dump,
* atau sensitive log.

Jika secret sudah masuk commit:

hapus dari history sesuai incident procedure project.

Jangan hanya menghapus file dari working tree dan menganggap secret sudah hilang dari history.

Hosting provider dapat memiliki push protection terhadap secret. GitHub, misalnya, dapat memblokir push yang mendeteksi secret.

## 34. Agent Safety

Coding agent boleh melakukan inspection read-only tanpa confirmation tambahan selama sesuai scope task.

Untuk operation yang mengubah local Git state:

ikuti task dan repository workflow.

Untuk operation dengan risiko history/data loss atau remote side effect, seperti:

* reset,
* branch pointer rewrite,
* force push,
* branch delete,
* merge ke protected branch,
* push,
* tag publish,

pastikan tindakan tersebut memang diminta atau diizinkan.

## 35. Recovery

Sebelum menganggap commit hilang:

periksa reflog jika sesuai.

Contoh:

```bash
git reflog
```

Git history lokal sering masih dapat dipulihkan setelah branch pointer berubah.

Jangan melakukan recovery destructive sebelum memahami state.

## 36. Stop Condition

Berhenti melakukan manipulasi Git jika:

* target branch tidak jelas,
* branch protection tidak diketahui dan operation akan rewrite remote,
* working tree memiliki perubahan user yang berisiko tertimpa,
* conflict resolution membutuhkan keputusan product/domain yang belum diketahui,
* atau command akan menghapus history/data tanpa izin.

Read-only diagnosis tetap boleh dilakukan.

## 37. Ringkasan Sebelum Operasi Berisiko

Sebelum history rewrite atau remote operation yang signifikan, agent secara internal harus mengetahui:

* current branch,
* base/target,
* remote,
* remote tip,
* commit task,
* dirty working tree,
* dan expected final history.

Jangan menampilkan checklist internal kecuali diminta.

## 38. Prinsip Akhir

Deteksi workflow Git, jangan menebak.

Jangan hardcode branch atau remote.

Base branch mengikuti repository.

Stacked branch boleh memiliki parent sendiri.

Gunakan merge, rebase, cherry-pick, atau rebuild berdasarkan tujuan.

Diagnosis sebelum rewrite.

Gunakan three-dot diff ketika ingin melihat perubahan branch sejak merge-base.

Jaga commit reviewable, bukan sekadar kecil.

Jangan menimpa perubahan user.

Push adalah side effect.

`--force-with-lease` lebih aman daripada `--force`, tetapi tetap history rewrite.

Hormati protected branch dan repository policy.

Verifikasi diff sebelum integration.

Jangan melakukan operasi destruktif untuk sekadar membuat history terlihat bersih.
