# AGENTS.md

Dokumen ini berisi instruksi project untuk AI coding agent.

Berlaku untuk coding agent yang mendukung `AGENTS.md` atau telah dikonfigurasi untuk membacanya.

File ini bersifat:

* framework-agnostic,
* language-agnostic,
* stack-agnostic,
* repository-aware,
* dan adaptif terhadap project yang sebenarnya.

Jangan mengasumsikan framework, bahasa, package manager, database, deployment provider, atau architecture sebelum memeriksa repository.

## Lifecycle dan skill composition

Satu lifecycle owner untuk satu task. Rules project memberi constraint; plan/checkpoint menyimpan state; skill spesialis memberi metode dan evidence.

Jika `andino-workflow` aktif atau diwajibkan project, gunakan plan/checkpoint Andino yang ada. Task non-trivial memakai plan sesuai kontraknya; SIMPLE tetap langsung dikerjakan. Andino memiliki phase state, acceptance, authoritative NEXT ACTION dan DONE. Jangan membuat plan paralel melalui template atau skill lain.

Jika Andino tidak aktif dan tidak diwajibkan, gunakan workflow serta task context host yang sedang berjalan. Instalasi skill saja tidak mengaktifkannya; jangan install atau bootstrap skill lain otomatis. Jika workflow yang diwajibkan tidak tersedia, laporkan gap tersebut dan lanjutkan hanya pekerjaan independen yang tetap sesuai constraint.

`ai-codebase-rescue` digunakan untuk fragilitas/regresi berulang atau pemulihan subsystem berbatas yang didukung bukti. Rescue dapat standalone; ketika Andino aktif, findings, gate REMAKE dan hasil verifikasinya kembali ke plan Andino. Bug lokal, kosmetik dan dugaan AI authorship saja tidak memicu rescue atau rewrite. REMAKE memerlukan bukti Boundary, Contract, Baseline, Risk, Safety dan Scope; jangan gunakan minimal change sebagai alasan mempertahankan patch rapuh.

Pilih metode langsung sesuai kebutuhan dan native invocation controls. Jangan memulai router `using-superpowers`, `using-agent-skills` atau `agent-skills`, serta jangan otomatis mengambil memory, membangun graph, mengaktifkan Ponytail, memasangkan skill UI atau melakukan subagent fan-out. Missing optional skill/tool tidak menghalangi pekerjaan biasa dan bukan alasan mengklaim skill itu telah dijalankan.

## 1. SOURCE OF TRUTH

Untuk current implementation state, gunakan repository aktual sebagai source of truth.

Prioritas bukti:

1. source code dan configuration yang berlaku,
2. manifest / dependency files,
3. schema dan migration,
4. build/test configuration,
5. CI/CD dan deployment configuration,
6. documentation project yang masih sesuai implementation,
7. memory/index/context lama.

Jika documentation, memory, graph, atau asumsi bertentangan dengan implementation/config aktual:

percaya repository.

Jangan mengarang:

* framework,
* package,
* API,
* route,
* file,
* directory,
* schema,
* service,
* branch,
* command,
* environment,
* atau fitur

yang belum didukung bukti repository.

## 2. PROJECT DISCOVERY

Sebelum membuat keputusan teknis yang bergantung pada stack, identifikasi project berdasarkan file yang benar-benar ada.

Periksa seperlunya:

* manifest,
* lockfile,
* workspace config,
* build config,
* framework config,
* source directories,
* entry points,
* schema,
* migrations,
* tests,
* CI,
* deployment configuration,
* dan documentation yang relevan.

Contoh sinyal project:

JavaScript / TypeScript:

* `package.json`
* `pnpm-lock.yaml`
* `yarn.lock`
* `package-lock.json`
* `bun.lock`
* `tsconfig.json`

Python:

* `pyproject.toml`
* `requirements.txt`
* `poetry.lock`
* `uv.lock`
* `Pipfile`

Rust:

* `Cargo.toml`
* `Cargo.lock`

Go:

* `go.mod`
* `go.sum`

Java / Kotlin:

* `pom.xml`
* `build.gradle`
* `build.gradle.kts`
* `settings.gradle`

.NET:

* `*.csproj`
* `*.fsproj`
* `*.sln`

PHP:

* `composer.json`
* `composer.lock`

Ruby:

* `Gemfile`
* `Gemfile.lock`

Dart / Flutter:

* `pubspec.yaml`

Elixir:

* `mix.exs`

C / C++:

* `CMakeLists.txt`
* `Makefile`
* Meson/configuration terkait

Monorepo:

* workspace configuration
* package directories
* nested manifests
* package-specific instruction files

Daftar ini hanya contoh.

Jangan menyimpulkan stack hanya karena satu nama file mirip.

Gunakan bukti yang paling kuat dari repository.

## 3. DETECT, DO NOT ASSUME

Setelah discovery, tentukan bila relevan:

* language,
* framework,
* runtime,
* package manager,
* frontend stack,
* backend stack,
* database,
* ORM,
* API style,
* testing framework,
* lint/format tooling,
* build system,
* deployment target,
* containerization,
* monorepo tooling,
* dan external services.

Jika suatu bagian belum diketahui:

anggap `UNKNOWN`.

Jangan memilih teknologi baru hanya untuk mengisi bagian yang tidak diketahui.

## 4. EXISTING STACK WINS

Jika project sudah memiliki stack:

ikuti stack existing kecuali user secara eksplisit meminta perubahan.

Contoh:

Jika project memakai Django:

jangan mengganti menjadi FastAPI hanya karena lebih familiar.

Jika project memakai Vue:

jangan memperkenalkan React tanpa requirement.

Jika project memakai REST:

jangan memperkenalkan GraphQL hanya karena dianggap lebih modern.

Jika project memakai SQL secara langsung:

jangan menambahkan ORM tanpa alasan.

Jika project memakai Three.js langsung:

jangan menggantinya dengan abstraction lain tanpa izin.

Gunakan dependency dan convention existing sebelum menambah alternatif baru.

## 5. FRAMEWORK-SPECIFIC RULES

Aturan framework hanya berlaku jika framework tersebut benar-benar terdeteksi.

Jangan menjalankan aturan:

Next.js
React
Vue
Nuxt
Svelte
Angular
Django
FastAPI
Flask
Laravel
Rails
Spring
.NET
Flutter
Electron
Tauri
atau framework lain

pada project yang tidak menggunakannya.

Jika framework memiliki documentation atau instruction yang version-specific:

gunakan versi yang sesuai dependency project.

Jangan mengandalkan training knowledge untuk behavior framework yang dapat berubah.

## 6. FRAMEWORK-MANAGED INSTRUCTIONS

Framework atau tooling tertentu dapat membuat, menambahkan, atau memperbarui instruction block secara otomatis.

Jika repository memiliki managed block semacam itu:

* jangan hapus hanya karena terlihat framework-specific,
* jangan rewrite isi generated block secara manual kecuali dokumentasi framework memperbolehkannya,
* perlakukan sebagai instruction tambahan untuk framework tersebut,
* dan pertahankan root instruction generic di luar managed block.

Contoh kasus:

sebuah framework dapat menambahkan instruction tentang dokumentasi lokal, API baru, migration, atau breaking change.

Managed instruction tersebut tidak mengubah `AGENTS.md` menjadi template khusus framework secara keseluruhan.

Ia hanya menambahkan aturan yang relevan untuk project tersebut.

## 7. NESTED AGENTS.md

Root `AGENTS.md` berisi aturan project yang broad.

Untuk repository kompleks atau monorepo, nested `AGENTS.md` boleh digunakan untuk aturan yang hanya berlaku pada area tertentu.

Contoh:

```text
project/
├── AGENTS.md
├── apps/
│   ├── web/
│   │   └── AGENTS.md
│   └── api/
│       └── AGENTS.md
├── packages/
│   ├── ui/
│   │   └── AGENTS.md
│   └── database/
│       └── AGENTS.md
```

Contoh pembagian:

root:

* aturan project umum,
* workflow,
* validation,
* security,
* git,
* source-of-truth.

`apps/web/AGENTS.md`:

* frontend framework,
* UI,
* accessibility,
* browser testing.

`apps/api/AGENTS.md`:

* backend,
* API,
* database access,
* security.

`packages/ui/AGENTS.md`:

* component rules,
* design system.

Jangan menaruh semua detail subproject di root jika scope yang lebih sempit lebih tepat.

## 8. PROJECT RULE FILES

Project dapat menyediakan rule modular seperti:

* `chat-rules.md`
* `code-rules.md`
* `token.md`
* `be-rules.md`
* `fe-rules.md`
* `Agents.md`
* `git-naming.md`
* `git-workflow.md`
* `git-branch-tips.md`
* plan/checkpoint task yang digunakan project
* `prd.md`
* `optional/brd-(optional).md` bila dipakai project
* `srs.md`

Gunakan secara lazy.

Baseline jika wiring project memang menetapkannya:

* `chat-rules.md`
* `code-rules.md`
* `token.md`

Gunakan rule domain hanya jika relevan.

Backend task:

* `be-rules.md`

Frontend/UI task:

* `fe-rules.md`

Git operation:

* `git-*`

Planning/task:

* plan/checkpoint task yang digunakan project

Product requirement:

* `prd.md`
* `optional/brd-(optional).md` bila dipakai project
* `srs.md`

Jangan memuat semua rule pada setiap task.

## 9. RULE LOADING

Jika agent/runtime sudah memuat sebuah rule melalui instruction wiring:

jangan membaca ulang seluruh file hanya untuk menduplikasi context.

Jika agent tidak otomatis melakukan import/reference:

baca rule yang relevan saat dibutuhkan.

Jangan menganggap syntax import seperti:

`@file.md`

berlaku universal di semua coding agent.

Gunakan mekanisme native agent jika tersedia.

## 10. UNDERSTAND BEFORE EDIT

Sebelum mengubah code:

1. pahami request user,
2. temukan area code yang relevan,
3. baca context secukupnya,
4. pahami pattern existing,
5. identifikasi dependency,
6. baru edit.

Jangan langsung membuat file baru jika functionality serupa sudah ada.

Jangan langsung membuat abstraction baru sebelum melihat pattern repository.

## 11. SEARCH BEFORE BROAD READ

Untuk repository besar:

gunakan search sebelum membuka banyak file.

Prioritaskan bila tersedia:

* symbol search,
* reference search,
* repository search,
* `rg`,
* file map,
* dependency graph,
* semantic navigation,
* atau index.

Jangan melakukan recursive full-read tanpa alasan.

## 12. MINIMAL CHANGE

Lakukan perubahan minimum yang benar-benar menyelesaikan requirement.

Hindari:

* unrelated refactor,
* dependency baru tanpa kebutuhan,
* architecture baru untuk task kecil,
* rename besar tanpa alasan,
* formatting seluruh repository,
* abstraction prematur,
* dan perubahan behavior yang tidak diminta.

Jangan menafsirkan "minimal" sebagai:

* melewati validation,
* mengabaikan edge case,
* atau mempertahankan bug yang berkaitan langsung.

## 13. FOLLOW EXISTING CONVENTIONS

Pertahankan convention repository untuk:

* naming,
* directory structure,
* imports,
* error handling,
* logging,
* configuration,
* dependency injection,
* state management,
* data access,
* component structure,
* API response,
* tests,
* dan documentation.

Jangan memperkenalkan style pribadi jika repository sudah memiliki pattern konsisten.

## 14. PACKAGE MANAGER

Gunakan package manager yang sudah digunakan project.

Contoh:

Jika ada `pnpm-lock.yaml`:
gunakan pnpm.

Jika ada `yarn.lock`:
gunakan Yarn sesuai configuration project.

Jika ada `package-lock.json`:
gunakan npm.

Jika ada Bun lockfile/config:
gunakan Bun sesuai project.

Untuk ecosystem lain, gunakan tool yang dibuktikan manifest/config.

Jangan mengganti package manager tanpa request eksplisit.

## 15. DEPENDENCIES

Sebelum menambah dependency:

periksa apakah kebutuhan sudah dapat diselesaikan dengan:

* standard library,
* platform API,
* dependency existing,
* utility existing,
* atau implementation sederhana.

Tambahkan dependency baru hanya jika memberi manfaat nyata.

Jika dependency baru diperlukan:

cek compatibility dengan stack dan version project.

Jangan mengarang package atau API.

## 16. CURRENT DOCUMENTATION

Gunakan external documentation bila behavior dependency:

* current-sensitive,
* version-sensitive,
* deprecated,
* baru berubah,
* atau tidak cukup jelas dari codebase.

Prioritaskan:

1. documentation resmi,
2. source/release notes resmi,
3. issue/discussion upstream yang relevan,
4. technical references kredibel.

Jangan web search jika behavior sudah jelas dari repository dan documentation lokal.

## 17. GENERATED CODE

Identifikasi generated files.

Jangan edit generated output jika source generator tersedia.

Contoh dapat mencakup:

* generated client,
* ORM output,
* codegen,
* compiled assets,
* build artifacts,
* framework-generated files,
* schema-generated types.

Edit source atau generator yang benar.

Jika generated file memang source of truth menurut tooling tersebut:

ikuti documentation project.

## 18. DATABASE

Jika task menyentuh persistence:

identifikasi terlebih dahulu:

* database,
* schema,
* ORM/query layer,
* migration system,
* transaction pattern,
* dan ownership data.

Jangan mengubah schema tanpa mempertimbangkan migration.

Jangan menghapus atau mengubah production data tanpa explicit authorization.

Jangan mengarang table/field yang belum ditemukan.

## 19. API

Jika task menyentuh API:

pertahankan existing contract kecuali perubahan contract memang diminta.

Periksa:

* input validation,
* authentication,
* authorization,
* response shape,
* error behavior,
* backwards compatibility,
* dan consumer.

Untuk external API:

verifikasi contract current jika diperlukan.

## 20. FRONTEND

Jika frontend terdeteksi dan task menyentuh UI:

ikuti framework dan design pattern existing.

Pertimbangkan:

* semantics,
* keyboard access,
* focus,
* responsive behavior,
* loading state,
* empty state,
* error state,
* motion,
* dan accessibility.

Jangan mengubah visual language seluruh application untuk perubahan lokal.

## 21. BACKEND

Jika backend terdeteksi:

ikuti architecture existing.

Pertimbangkan:

* validation,
* authorization,
* error handling,
* transaction boundaries,
* idempotency,
* concurrency,
* data consistency,
* logging,
* dan security

sesuai kebutuhan task.

Jangan membuat service/repository layer baru jika codebase tidak membutuhkannya.

## 22. MOBILE / DESKTOP / EMBEDDED / CLI

Jangan menganggap project selalu web.

Jika target adalah:

* mobile,
* desktop,
* CLI,
* embedded,
* game,
* extension,
* library,
* SDK,
* worker,
* service,
* atau platform lain,

ikuti constraint platform tersebut.

Contoh:

CLI:

* exit code,
* stdout/stderr,
* piping,
* configuration.

Library:

* public API,
* compatibility,
* package size,
* semantic versioning.

Mobile:

* lifecycle,
* permissions,
* offline behavior,
* device capability.

Desktop:

* OS integration,
* packaging,
* update strategy.

Gunakan hanya bagian yang relevan.

## 23. SECURITY

Security bersifat risk-based.

Jangan menambahkan security theater.

Untuk task yang relevan, pertimbangkan:

* input validation,
* authentication,
* authorization,
* secrets,
* injection,
* XSS,
* CSRF,
* file upload,
* path traversal,
* SSRF,
* permission boundary,
* sensitive logging,
* dependency risk,
* dan data exposure.

Jangan memasukkan secret ke source code, log, test output, atau documentation.

## 24. SECRETS

Jangan membaca atau menampilkan nilai secret tanpa kebutuhan.

Jangan commit:

* password,
* API key,
* private key,
* token,
* credential,
* production secret.

Gunakan environment variable atau secret manager sesuai project.

## 25. ERROR HANDLING

Jangan menelan error secara diam-diam.

Ikuti error strategy existing.

Tambahkan error handling yang:

* actionable,
* tidak membocorkan data sensitif,
* dan sesuai layer.

Jangan menggunakan generic catch hanya untuk membuat test lewat.

## 26. TESTING

Gunakan testing setup yang benar-benar ada di repository.

Pilih test berdasarkan perubahan.

Logic lokal:

* unit test bila tersedia.

Boundary/integration:

* integration/contract test.

Critical user flow:

* E2E jika project menggunakannya.

UI:

* browser/visual/accessibility check jika relevan.

Jangan memperkenalkan testing framework baru hanya untuk satu perubahan jika existing setup sudah cukup.

## 27. VALIDATION BEFORE COMPLETION

Sebelum menyatakan task selesai:

jalankan validation yang relevan jika environment memungkinkan.

Urutan umum:

1. targeted test,
2. typecheck / compile,
3. lint,
4. integration test,
5. build,
6. E2E / broader suite

sesuai blast radius.

Tidak semua task membutuhkan semua tahap.

Ikuti repository instruction jika project menetapkan command wajib.

Jangan mengatakan:

"fixed"

"works"

"done"

tanpa evidence yang memadai.

## 28. VALIDATION FAILURE

Jika validation gagal:

jangan menyembunyikan hasil.

Tentukan apakah kegagalan berasal dari:

* perubahan saat ini,
* existing failure,
* environment,
* dependency,
* atau test yang tidak terkait.

Perbaiki failure yang berada dalam scope.

Laporkan failure di luar scope secara singkat.

## 29. PERFORMANCE

Jangan melakukan premature optimization.

Jika performance merupakan bagian requirement:

ukur atau profile jika memungkinkan.

Optimalkan bottleneck yang terbukti.

Jangan mengubah architecture berdasarkan asumsi performa tanpa evidence.

## 30. COMPATIBILITY

Pertimbangkan compatibility jika project memiliki:

* public API,
* database schema existing,
* supported browser,
* supported OS,
* multiple runtime,
* plugin ecosystem,
* atau external consumer.

Jangan melakukan breaking change diam-diam.

## 31. MONOREPO

Jika repository adalah monorepo:

identifikasi workspace/package yang benar sebelum edit.

Jangan menjalankan test/build seluruh monorepo jika targeted command cukup.

Hormati nested instruction dan package-specific convention.

Jangan mengasumsikan semua package memakai stack yang sama.

## 32. GIT

Sebelum perubahan besar, pahami working tree jika relevan.

Jangan menghapus perubahan user.

Jangan reset unrelated changes.

Jangan melakukan:

* commit,
* push,
* merge,
* rebase,
* force push,
* branch deletion

tanpa instruction yang mengizinkannya.

Review diff sebelum final.

## 33. EXTERNAL SIDE EFFECTS

Tindakan berikut membutuhkan perhatian khusus:

* deployment,
* publication,
* remote deletion,
* production data mutation,
* sending message,
* billing change,
* infrastructure mutation,
* credential rotation,
* merge/push.

Jangan melakukan side effect eksternal hanya karena local implementation selesai.

Ikuti permission model agent dan instruksi user.

## 34. DOCUMENTATION

Update documentation jika perubahan membuat documentation existing menjadi salah atau tidak lengkap secara material.

Jangan membuat documentation tambahan tanpa kebutuhan.

Jangan mengulang informasi yang sudah memiliki source of truth yang lebih tepat.

## 35. UNKNOWN

Jika informasi tidak dapat dipastikan:

gunakan:

`UNKNOWN`

atau jelaskan ketidakpastiannya.

Jangan mengisi gap dengan tebakan.

## 36. TOOL USE

Gunakan tool yang paling tepat dan paling sedikit untuk menyelesaikan task.

Jangan tool-stack hanya karena banyak integration tersedia.

Gunakan bila relevan:

* memory untuk context lama,
* graph/semantic tool untuk structure,
* repository search untuk source,
* documentation tool untuk dependency,
* browser tool untuk frontend behavior,
* telemetry untuk production error,
* deployment provider untuk deployment,
* database provider untuk database.

Tool availability tidak menentukan architecture project.

## 37. USER INTENT

Instruksi eksplisit user tentang project harus dipertahankan.

Jika user mengunci:

* framework,
* library,
* architecture,
* API,
* deployment,
* atau constraint,

jangan menggantinya diam-diam.

Jika requirement tidak feasible:

jelaskan conflict dan cari solusi terdekat yang mempertahankan intent.

## 38. PRIORITY

Untuk intent, scope dan keputusan kerja, ikuti instruksi eksplisit user terbaru, lalu aturan project yang berlaku, keputusan/checkpoint yang disepakati, dan default template. Tetap patuhi hierarchy instruksi host serta batas platform, permission, security dan kebijakan yang benar-benar enforced; jangan menonaktifkan pembatas tersebut untuk memenuhi permintaan. Untuk fakta implementasi, repository/config/test aktual mengungguli dokumentasi atau memory yang stale; fakta baru tidak otomatis membatalkan keputusan user.

Urutan umum:

1. system/platform/agent constraints,
2. latest explicit user instructions within those constraints,
3. applicable repository instructions,
4. project rules,
5. framework-specific instructions,
6. default conventions.

Nested `AGENTS.md` yang lebih spesifik berlaku pada scope-nya sesuai kemampuan agent yang digunakan.

Jangan menggunakan root rule untuk mengalahkan instruction yang memang lebih spesifik pada subproject.

## 39. RESPONSE STYLE

Untuk perubahan kecil:

laporkan singkat:

* apa yang berubah,
* validation,
* dan blocker jika ada.

Untuk task kompleks:

jelaskan keputusan utama dan trade-off yang material.

Jangan mengulang seluruh proses internal.

Jangan menampilkan private chain-of-thought.

## 40. FINAL CHECK

Sebelum final, periksa secara internal:

* task user terpenuhi?
* stack yang digunakan benar?
* convention existing dipertahankan?
* ada perubahan tidak terkait?
* dependency baru benar-benar perlu?
* security relevant sudah diperiksa?
* tests/validation relevan sudah dilakukan?
* generated file salah edit?
* secret terpapar?
* diff masuk akal?
* ada claim yang tidak didukung evidence?

Jangan tampilkan checklist ini kecuali diminta.

## 41. PRINCIPLE

Pahami repository sebelum mengubahnya.

Deteksi stack, jangan menebak.

Gunakan framework yang benar-benar ada.

Pertahankan convention existing.

Muat rule berdasarkan kebutuhan.

Buat perubahan minimum yang benar.

Jangan overengineer.

Jangan mengarang.

Verifikasi sebelum menyatakan selesai.

## FRAMEWORK / TOOL MANAGED BLOCKS

Framework atau development tool boleh menambahkan managed instruction block setelah bagian ini.

Jika block tersebut ditandai sebagai generated atau managed:

* jangan hapus tanpa alasan,
* jangan rewrite manual jika generator akan menambahkannya kembali,
* ikuti instruction tersebut hanya untuk framework/tool yang memang digunakan project,
* dan pertahankan bagian universal di atas sebagai root project guidance.

Managed block di bawah dapat berbeda antarproject.
