# Git Naming, PR/MR, dan Work Report

Panduan untuk menjaga naming branch, commit message, Pull Request / Merge Request, serta laporan kerja tetap konsisten dengan repository dan workflow project.

File ini bersifat:

* repository-aware,
* hosting-agnostic,
* team-process-agnostic,
* branch-strategy-agnostic,
* dan coding-agent-aware.

Jangan mengasumsikan repository memakai:

* GitHub,
* GitLab,
* Bitbucket,
* Azure DevOps,
* Conventional Commits,
* username prefix,
* issue ID,
* `main`,
* `master`,
* `develop`,
* `staging`,
* Pull Request,
* Merge Request,
* atau daily report

sebelum memeriksa convention project.

## 1. Prioritas Convention

Untuk naming dan format Git, hormati keputusan eksplisit user terbaru dalam batas host dan tooling yang enforced. Daftar berikut membantu menemukan convention existing; bukan alasan mengalahkan keputusan user yang sah:

1. repository instructions yang berlaku,
2. contribution guide,
3. Git/CI configuration yang memvalidasi naming,
4. existing branch/commit/PR convention,
5. team workflow yang diberikan user,
6. fallback dari file ini.

Contoh source yang perlu diperiksa bila relevan:

* `AGENTS.md`
* `CONTRIBUTING.md`
* `README.md`
* `.github/`
* `.gitlab/`
* commitlint config
* semantic-release config
* release tooling
* CI workflow
* PR/MR templates
* issue tracker convention
* `git-workflow.md`
* repository history.

Jangan menerapkan fallback file ini jika repository sudah memiliki aturan yang lebih spesifik.

## 2. Jangan Menebak Convention

Jika naming convention belum diketahui:

periksa repository secara targeted.

Contoh:

```bash
git branch --all
git log -n 20 --pretty=format:"%s"
```

Jika remote platform dapat diakses dan task memang membutuhkan PR/MR:

periksa beberapa PR/MR terbaru atau template project.

Jangan melakukan web/API request hanya untuk naming jika local repository sudah cukup menjelaskan convention.

## 3. Branch Naming Bersifat Project-Specific

Git sendiri mengatur apakah sebuah ref name valid.

Git tidak menentukan bahwa branch harus memakai:

* `feat/`
* `fix/`
* username,
* ticket number,
* atau format organisasi tertentu.

Karena itu:

ikuti convention repository.

Jangan menyebut salah satu pola sebagai universal.

## 4. Validasi Nama Branch

Jika ragu apakah branch name valid menurut Git:

gunakan:

```bash
git check-ref-format --branch "nama-branch"
```

Nama branch harus valid sebagai Git ref.

Hindari karakter yang tidak valid seperti:

* spasi,
* `..`,
* `~`,
* `^`,
* `:`,
* control character,
* atau pola lain yang ditolak Git.

Jangan membuat validator custom jika Git sendiri dapat memvalidasinya.

## 5. Branch Naming Detection

Cari pola dominan repository.

Contoh pola yang mungkin digunakan:

```text
feat/search
fix/login-timeout
feature/search
bugfix/login
hotfix/payment
user/feat/search
username/feature/search
ABC-123-search
feature/ABC-123-search
release/1.5.0
dependabot/npm/example
```

Tidak ada satu format yang otomatis lebih benar.

Gunakan format yang project sudah tetapkan.

## 6. Jangan Campur Alias Type

Jika project memakai:

`feat`

jangan tiba-tiba menggunakan:

`feature`

untuk maksud sama.

Jika project memakai:

`bugfix`

jangan membuat:

`fix`

tanpa alasan.

Konsistensi lebih penting daripada memilih nama type favorit agent.

## 7. Fallback Branch Naming

Jika repository benar-benar tidak memiliki convention:

gunakan fallback sederhana:

```text
<type>/<deskripsi-singkat>
```

Contoh:

```text
feat/add-search-filter
fix/prevent-duplicate-submit
refactor/simplify-parser
docs/update-installation
test/add-auth-coverage
chore/update-ci-config
```

Gunakan:

* huruf kecil,
* kata singkat,
* dash antar kata,
* dan deskripsi yang menjelaskan outcome.

Fallback hanya digunakan bila project belum memiliki convention.

## 8. Username Prefix

Jangan menambahkan username prefix secara otomatis.

Gunakan format seperti:

```text
<username>/<type>/<description>
```

hanya jika:

* repository memang menggunakannya,
* hosting/workflow mengharuskannya,
* atau user meminta.

Jangan mengarang `[USERNAME]` jika identitas Git/user belum diketahui.

## 9. Ticket / Issue ID

Jika project menggunakan tracker seperti:

* Jira,
* Linear,
* GitHub Issues,
* GitLab Issues,
* Azure Boards,
* atau tracker lain,

ikuti format ID yang dipakai team.

Contoh:

```text
PROJ-123-add-export
feature/PROJ-123-add-export
fix/482-login-timeout
```

Jangan menambahkan issue ID palsu hanya agar branch terlihat formal.

## 10. Branch Description

Nama branch menjelaskan pekerjaan utama.

Hindari nama terlalu umum seperti:

```text
update
changes
fix
bug
test
new-feature
work
temp
```

Hindari pula nama yang terlalu panjang dan mencoba menyalin seluruh requirement.

Nama branch harus cukup untuk mengenali task.

## 11. WIP Branch

Jangan menambahkan:

```text
wip/
```

secara otomatis.

Gunakan jika workflow team memang memakai WIP branch.

Platform seperti GitHub/GitLab biasanya menyediakan Draft PR/MR untuk menandai pekerjaan belum siap review.

Ikuti workflow project.

## 12. Branch Renaming

Jangan rename branch yang sudah published hanya untuk mempercantik nama.

Pertimbangkan:

* remote references,
* open PR/MR,
* CI,
* automation,
* stacked branch,
* dan contributor lain.

Rename hanya jika manfaatnya jelas dan workflow mengizinkan.

## 13. Commit Convention Detection

Sebelum memilih format commit:

periksa apakah repository menggunakan:

* Conventional Commits,
* Angular-style commits,
* ticket-prefixed commits,
* imperative subject,
* free-form subject,
* squash-only workflow,
* atau convention lain.

Cari evidence seperti:

* commit history,
* `commitlint.config.*`,
* `.commitlintrc*`,
* semantic-release config,
* changelog tooling,
* CONTRIBUTING.

Jangan memaksa Conventional Commits jika repository tidak menggunakannya.

## 14. Conventional Commits

Jika repository memakai Conventional Commits:

ikuti specification.

Format dasar:

```text
<type>[optional scope]: <description>
```

Contoh:

```text
feat(search): add project filtering
fix(auth): prevent expired-session loop
refactor(parser): remove duplicate normalization
docs(api): clarify authentication setup
test(cart): cover duplicate checkout
```

Scope bersifat opsional menurut specification.

Jangan memaksa scope jika project tidak menggunakannya.

## 15. Conventional Commit Types

Specification mewajibkan makna khusus terutama untuk:

`feat`
dan
`fix`.

Type lain dapat ditentukan project.

Contoh yang umum tetapi bukan daftar universal:

```text
docs
test
refactor
chore
build
ci
perf
style
revert
```

Gunakan type yang diakui tooling project.

Jangan menambahkan custom type jika commitlint/project akan menolaknya.

## 16. Breaking Changes

Jika project memakai Conventional Commits dan commit memiliki breaking change:

ikuti format yang didukung specification/project.

Contoh:

```text
feat(api)!: replace legacy authentication endpoint
```

atau footer:

```text
BREAKING CHANGE: legacy token authentication is no longer supported
```

Jangan menandai breaking change jika contract sebenarnya tetap kompatibel.

## 17. Commit Subject

Subject commit harus menjelaskan perubahan.

Prefer:

```text
fix(auth): prevent refresh loop after token expiry
```

daripada:

```text
fix bug
```

Gunakan wording yang natural dan mudah dipindai.

Jangan memenuhi subject dengan implementation detail yang tidak membantu memahami perubahan.

## 18. Bahasa Commit

Bahasa commit mengikuti repository.

Jika history dominan English:

gunakan English.

Jika project memakai Indonesia:

gunakan Indonesia.

Jika team memiliki rule khusus:

ikuti rule tersebut.

Jangan mengganti bahasa history hanya karena template ditulis dalam bahasa Indonesia.

## 19. Commit Granularity

Satu commit idealnya merepresentasikan satu perubahan logis.

Contoh:

* satu bug fix,
* satu refactor terkait,
* satu feature slice,
* satu migration yang terkait,
* atau test yang memang bagian perubahan.

Jangan memecah commit hanya berdasarkan jumlah file.

Jangan pula menggabungkan banyak concern tidak terkait ke satu commit.

## 20. Test dan Implementation Commit

Tidak ada kewajiban universal untuk memisahkan:

```text
implementation commit
```

dan:

```text
test commit
```

Jika test merupakan bagian alami perubahan:

satu commit boleh lebih reviewable.

Pisahkan jika workflow project atau tujuan cherry-pick/review memang membutuhkannya.

## 21. Fixup / Squash Workflow

Jika project menggunakan interactive rebase, autosquash, atau stacked workflow:

commit sementara dapat mengikuti convention seperti:

```text
fixup! ...
squash! ...
```

jika workflow memang mendukungnya.

Jangan memperlakukan temporary history seperti final history.

Sebelum integration, ikuti policy project.

## 22. Jangan Membuat Commit Tanpa Diminta

Coding agent tidak wajib commit setelah setiap task.

Commit hanya jika:

* user meminta,
* workflow agent/task memang mencakup commit,
* atau repository instruction mengharuskannya.

Jika hanya diminta mengedit code:

working tree change dapat menjadi hasil final.

## 23. Jangan Mengarang Author

Jangan mengubah:

```bash
user.name
user.email
```

atau commit author hanya untuk menyelesaikan task.

Gunakan configuration environment yang tersedia.

Jika Git membutuhkan identity tetapi belum dikonfigurasi:

laporkan daripada mengarang identitas.

## 24. PR dan MR

Gunakan istilah yang sesuai platform.

GitHub:
Pull Request / PR.

GitLab:
Merge Request / MR.

Platform lain:
ikuti terminology platform.

Jika template harus tetap vendor-neutral:

gunakan:

`PR/MR`.

## 25. PR/MR Target

Jangan mengasumsikan target selalu:

`staging`
atau
`main`.

Target dapat berupa:

* default branch,
* integration branch,
* release branch,
* parent stacked branch,
* backport branch,
* atau target lain.

Gunakan target yang memang ditentukan workflow.

## 26. PR/MR Title Convention Detection

Sebelum membuat title:

periksa bila tersedia:

* repository instruction,
* PR/MR template,
* CI validation,
* release tooling,
* recent merged PR/MR.

Jangan membuat format seperti:

```text
[STAGING] branch : description
```

kecuali repository memang menggunakan format tersebut.

## 27. Fallback PR/MR Title

Jika tidak ada convention:

gunakan title singkat yang menjelaskan outcome.

Contoh:

```text
Add project search filters
Fix duplicate payment submission
Improve parser error handling
```

Jika repository menggunakan Conventional Commits untuk PR title:

boleh gunakan:

```text
feat(search): add project filters
fix(payment): prevent duplicate submission
```

Jangan menambahkan target branch ke title jika informasi tersebut sudah jelas dari PR/MR dan team tidak membutuhkannya.

## 28. PR/MR Title Harus Sesuai Perubahan Final

Jangan membuat title berdasarkan rencana awal jika scope akhirnya berubah.

Sebelum membuat/update PR/MR:

review diff.

Pastikan title mencerminkan perubahan yang benar-benar akan direview.

## 29. PR/MR Description

Gunakan template repository jika tersedia.

GitHub mendukung Pull Request template yang otomatis dimasukkan ke body PR.

Platform lain dapat memiliki mekanisme serupa.

Jangan mengganti template project dengan format fallback tanpa alasan.

## 30. Fallback PR/MR Description

Jika repository tidak memiliki template:

gunakan struktur minimal yang membantu review.

Contoh:

```markdown
## Summary

- [perubahan utama]

## Why

[konteks singkat jika tidak sudah jelas]

## Validation

- [test/check yang benar-benar dilakukan]

## Notes

- [migration, limitation, follow-up, atau hal penting lain jika ada]
```

Hapus section yang tidak relevan.

Jangan membuat PR description panjang hanya untuk memenuhi template.

## 31. Validation Harus Faktual

Di PR/MR description:

hanya sebut test yang benar-benar dijalankan.

Jangan menulis:

```text
All tests passed
```

jika test suite tidak dijalankan.

Gunakan status jujur seperti:

```text
Not run: environment dependency unavailable.
```

jika diperlukan.

## 32. Jangan Checklist Palsu

Jangan menandai:

```text
[x]
```

hanya agar PR terlihat siap.

Checklist harus mewakili verification nyata.

Jika item tidak relevan:

hapus atau tandai sesuai convention template.

## 33. Migration

Jangan selalu menulis:

```text
Tidak ada migration
```

pada setiap PR.

Sebut migration jika:

* ada,
* reviewer perlu mengetahui,
* deployment dipengaruhi,
* atau template project meminta.

Untuk project tanpa database, section migration tidak diperlukan.

## 34. Breaking Change

Jika PR/MR mengubah public contract secara breaking:

jelaskan secara eksplisit.

Contoh yang mungkin terdampak:

* API,
* schema,
* CLI flags,
* event,
* package interface,
* file format,
* config,
* protocol.

Jangan menyembunyikan breaking change hanya karena test lolos.

## 35. Screenshots / Visual Evidence

Jika PR/MR mengubah UI dan workflow project menghargai visual proof:

sertakan screenshot/video bila tersedia dan memang membantu review.

Jangan membuat screenshot sebagai requirement universal untuk frontend change.

## 36. Issue Link

Jika task memiliki issue/ticket:

hubungkan sesuai syntax platform/project.

Jangan mengarang issue number.

Jika tidak ada issue:

tidak perlu membuat placeholder palsu.

## 37. Draft PR/MR

Gunakan Draft jika:

* pekerjaan belum siap review,
* CI/feedback awal dibutuhkan,
* atau workflow team memang menggunakan draft.

Jangan menambahkan `WIP:` ke title jika platform/team sudah menggunakan Draft dan convention tidak memerlukannya.

## 38. PR/MR Rebuild

Jangan otomatis menambahkan kata:

`remerge`

ke title.

Jika branch direbuild karena history berubah:

title seharusnya tetap mencerminkan perubahan product/code kecuali team convention memang meminta marker tertentu.

Informasi rebuild dapat ditempatkan di description/note bila reviewer perlu mengetahuinya.

## 39. Squash Merge

Jika repository memakai squash merge:

perhatikan bahwa PR title atau squash commit message mungkin menjadi commit final.

Karena itu title harus cukup berkualitas sebagai history jika workflow menggunakan title sebagai squash subject.

Ikuti configuration hosting/repository.

## 40. Merge Commit

Jika project mempertahankan merge commits:

ikuti message convention project.

Jangan rewrite generated merge commit message hanya untuk menyesuaikan Conventional Commits jika workflow tidak membutuhkannya.

## 41. Release Automation

Jika repository menggunakan:

* semantic-release,
* release-please,
* Changesets,
* conventional-changelog,
* atau automation lain,

naming/commit rules dapat memengaruhi release.

Periksa config tool sebelum mengubah commit convention.

Jangan membuat commit format yang memutus release automation.

## 42. Changelog

Jangan mengedit changelog secara manual jika project menghasilkannya otomatis.

Jika changelog manual:

ikuti workflow repository.

Jangan menambah changelog entry untuk setiap perubahan kecil tanpa requirement.

## 43. Branch Protection / Rules

Naming tertentu dapat divalidasi oleh:

* branch rules,
* CI,
* push rules,
* hooks,
* bot,
* atau hosting provider.

Jika validation tersedia:

anggap konfigurasi tersebut lebih kuat daripada contoh template ini.

Jangan mencoba bypass validation.

## 44. Git Hooks

Jika project memakai:

* commit-msg hook,
* pre-commit,
* pre-push,
* Husky,
* Lefthook,
* pre-commit framework,
* atau hook lain,

ikuti output hook.

Jangan menggunakan `--no-verify` hanya untuk melewati check kecuali user/workflow secara eksplisit membenarkannya.

## 45. Commit Message Validation

Jika ingin memeriksa commit sebelum membuatnya:

gunakan tooling repository.

Contoh:

```bash
commitlint
```

hanya jika project memang memilikinya.

Jangan install commitlint hanya untuk memvalidasi satu commit jika repository tidak menggunakannya.

## 46. Branch Name Validation

Gunakan:

```bash
git check-ref-format --branch "[BRANCH_NAME]"
```

untuk syntax Git.

Gunakan project-specific checker jika repository memiliki rule tambahan.

Keduanya menjawab hal berbeda:

Git:
apakah ref valid.

Project:
apakah naming sesuai convention.

## 47. PR/MR Sebagai Remote Side Effect

Jangan membuat atau mengubah PR/MR hanya karena code sudah selesai.

Lakukan hanya jika:

* user meminta,
* task mencakup PR/MR,
* atau environment workflow memberi izin.

Membuat PR/MR dapat:

* memberi notifikasi,
* memicu CI,
* meminta review,
* atau memengaruhi project workflow.

## 48. Jangan Mengarang URL

Jika belum membuat PR/MR:

jangan menulis placeholder seolah-olah ada URL nyata.

Gunakan:

`PR/MR belum dibuat`

atau jangan tampilkan field tersebut.

## 49. Laporan Setelah PR/MR

Laporan ke:

* grup,
* Slack,
* Teams,
* Discord,
* task tracker,
* email,
* atau channel lain

hanya dilakukan jika workflow team memerlukannya atau user meminta.

Jangan menganggap setiap repository memiliki grup laporan.

## 50. Format Laporan PR/MR

Jika team tidak memiliki format khusus:

fallback ringkas:

```text
[Judul perubahan]
[PR/MR URL]

Validation:
- [check utama]

Notes:
- [hal penting jika ada]
```

Sesuaikan bahasa dan detail dengan channel.

Jangan memaksa format ini jika team memiliki template sendiri.

## 51. Daily / Work Report

Daily report bukan bagian wajib dari Git.

Gunakan hanya jika:

* user meminta,
* organisasi/team memiliki workflow report,
* atau project template memang memerlukannya.

Jangan mengarang aktivitas untuk memenuhi jumlah item minimum.

## 52. Jumlah Item Report

Tidak ada aturan universal:

`minimal 3 item`.

Jumlah mengikuti pekerjaan nyata.

Satu pekerjaan besar dapat cukup satu item.

Banyak pekerjaan kecil dapat menjadi beberapa item.

Jangan memecah satu task menjadi tiga bullet hanya untuk mencapai kuota.

## 53. Isi Work Report

Report menjelaskan outcome nyata.

Prefer:

```text
1. Perbaiki duplicate submission pada checkout.
2. Tambah regression test untuk retry checkout.
```

daripada:

```text
1. Buka project.
2. Edit file.
3. Run test.
```

Fokus pada hasil, bukan aktivitas mekanis.

## 54. Jangan Mengarang Progress

Jangan menulis:

* selesai,
* deployed,
* merged,
* tested,
* approved,
* atau reviewed

jika belum benar-benar terjadi.

Gunakan status yang akurat.

## 55. Bahasa Report

Ikuti convention team.

Bahasa Indonesia jika team menggunakan Indonesia.

English jika team menggunakan English.

Jangan mengubah bahasa hanya karena file rules ditulis dalam Indonesia.

## 56. Agent Behavior

Coding agent tidak otomatis:

* membuat branch,
* commit,
* push,
* membuat PR/MR,
* mengirim laporan,
* atau membuat daily report.

Lakukan action tersebut hanya jika task/user/workflow memang memintanya.

Rule naming mengatur FORMAT ketika action dilakukan.

Bukan memberi izin melakukan action.

## 57. Existing Work

Jika branch/commit/PR sudah ada:

jangan rename/rewrite hanya karena formatnya tidak mengikuti fallback file ini.

Pertimbangkan biaya dan efek:

* CI,
* reviewer,
* links,
* remote history,
* automation,
* stacked branch,
* atau release tooling.

Consistency improvement tidak selalu membenarkan history rewrite.

## 58. Monorepo

Monorepo dapat memiliki convention berbeda per package atau team.

Periksa instruction yang scope-nya relevan.

Jangan menganggap seluruh repository harus memakai satu scope commit jika tooling/project tidak menetapkannya.

## 59. Scope Commit di Monorepo

Jika project menggunakan scope:

gunakan terminology yang benar-benar dipakai.

Contoh:

```text
feat(api):
fix(web):
chore(deps):
```

atau nama package:

```text
feat(auth-service):
```

Jangan membuat scope berdasarkan tebakan nama folder.

## 60. Dependency Bot

Branch/commit dari bot seperti:

* Dependabot,
* Renovate,
* release bot,
* automation

dapat memakai format sendiri.

Jangan menggunakan branch bot sebagai bukti naming convention manusia kecuali workflow project memang menyatukannya.

## 61. Commit dari Merge/Squash

Saat menganalisis convention:

bedakan:

* normal developer commits,
* merge commits,
* squash commits,
* bot commits,
* release commits.

Jangan mengambil lima commit acak dan menyimpulkan convention jika history didominasi automation.

## 62. Detection Confidence

Jika convention terlihat konsisten dari:

* documentation,
* tooling,
* dan recent history,

anggap confidence tinggi.

Jika hanya beberapa contoh bercampur:

anggap convention belum jelas.

Dalam kondisi tidak jelas:

gunakan format paling konservatif atau tanyakan hanya jika output yang diminta membutuhkan naming final.

## 63. Fallback Universal

Jika tidak ada convention dan user meminta agent membuat naming:

Branch:

```text
<type>/<short-kebab-description>
```

Commit:

```text
<type>: <clear description>
```

PR/MR title:

```text
<clear outcome-oriented title>
```

PR/MR body:

```markdown
## Summary
- ...

## Validation
- ...
```

Gunakan type:

```text
feat
fix
refactor
docs
test
chore
```

seperlunya.

Fallback bukan standar organisasi.

Ia hanya default aman saat tidak ada convention lain.

## 64. Contoh Fallback

Branch:

```text
feat/add-project-search
fix/prevent-session-loop
docs/update-api-guide
```

Commit:

```text
feat: add project search
fix: prevent expired-session loop
docs: update API setup guide
```

PR/MR:

```text
Add project search
```

atau jika project memang memakai Conventional Commits:

```text
feat(search): add project search
```

## 65. Hindari Generic Naming

Hindari bila final:

```text
update
changes
fix stuff
misc
test
wip
temp
final
final-final
new
latest
```

Gunakan intent atau outcome yang nyata.

## 66. Hindari Over-Specific Naming

Jangan membuat nama seperti:

```text
fix-change-line-72-in-user-controller-to-handle-null-token
```

Nama branch/commit bukan pengganti diff.

Tulis cukup untuk memahami tujuan.

## 67. Jangan Masukkan Secret/Data Sensitif

Jangan memasukkan ke:

* branch name,
* commit subject/body,
* PR/MR title/body,
* issue link text,
* report,

data seperti:

* secret,
* access token,
* password,
* private URL,
* customer PII,
* credential,
* atau incident detail sensitif

tanpa kebutuhan dan izin.

Git history dan remote metadata dapat bertahan lama.

## 68. Validation Sebelum Commit/PR

Sebelum membuat commit atau PR/MR bila task mencakupnya:

periksa:

* diff sesuai scope,
* naming sesuai convention,
* validation benar-benar dilakukan,
* tidak ada debug residue,
* tidak ada secret,
* dan title/description mencerminkan perubahan final.

Jangan membuat metadata lebih dulu lalu lupa memperbaruinya setelah scope berubah.

## 69. Prioritas Konflik

Untuk intent, scope dan keputusan kerja, ikuti instruksi eksplisit user terbaru, lalu aturan project yang berlaku, keputusan/checkpoint yang disepakati, dan default template. Tetap patuhi hierarchy instruksi host serta batas platform, permission, security dan kebijakan yang benar-benar enforced; jangan menonaktifkan pembatas tersebut untuk memenuhi permintaan. Untuk fakta implementasi, repository/config/test aktual mengungguli dokumentasi atau memory yang stale; fakta baru tidak otomatis membatalkan keputusan user.

Urutan umum:

1. system/platform/agent constraint,
2. enforced CI/hook/tooling,
3. latest explicit user instruction within those constraints,
4. repository instruction,
5. documented team convention,
6. observed repository convention,
7. file `git-naming.md`,
8. generic preference agent.

Jika fallback file ini bertentangan dengan tooling repository:

tooling/repository menang.

## 70. Cek Internal

Sebelum membuat branch/commit/PR/MR/report, periksa secara internal:

* convention repository sudah diketahui?
* platform apa?
* branch target benar?
* username prefix diperlukan?
* issue ID diperlukan?
* Conventional Commits benar-benar digunakan?
* scope diperlukan?
* bahasa apa yang dipakai team?
* PR/MR template tersedia?
* title divalidasi CI?
* action remote memang diizinkan?
* validation yang disebut benar-benar dijalankan?
* report memang dibutuhkan?

Jangan tampilkan checklist ini kecuali diminta.

## 71. Prinsip Akhir

Deteksi convention, jangan menebak.

Git menentukan validitas ref, team menentukan style branch.

Conventional Commits bersifat opt-in sesuai repository.

Jangan memaksa username prefix.

Jangan memaksa ticket ID.

Jangan mengasumsikan target `main` atau `staging`.

Gunakan PR/MR template project bila tersedia.

Metadata Git harus mencerminkan perubahan nyata.

Jangan membuat checklist atau report palsu.

Daily report mengikuti workflow team, bukan aturan Git.

Naming rule mengatur format.

Naming rule tidak memberi izin untuk commit, push, atau membuat PR/MR.
