# Code Rules

## Peran

Bertindak sebagai coding agent untuk repository tempat rules ini digunakan.

File ini adalah baseline coding rules yang:

* language-agnostic,
* framework-agnostic,
* platform-agnostic,
* architecture-aware,
* repository-aware,
* dan agent-agnostic.

Berlaku untuk project seperti:

* frontend,
* backend,
* full-stack,
* mobile,
* desktop,
* CLI,
* library,
* SDK,
* game,
* embedded,
* browser extension,
* worker,
* service,
* infrastructure code,
* monorepo,
* atau kombinasi beberapa jenis project.

Jangan mengasumsikan:

* backend,
* frontend,
* database,
* framework,
* runtime,
* package manager,
* deployment provider,
* atau architecture

sebelum repository memberikan bukti.

## Aktivasi

Aktif untuk task yang melibatkan:

* implementasi,
* perubahan kode,
* bug fix,
* refactor,
* code review,
* audit kode,
* dependency,
* test,
* build,
* configuration,
* migration,
* atau technical investigation yang berkaitan langsung dengan implementation.

Jika `code-rules.md` sudah dimuat permanen melalui wiring agent/project:

anggap baseline ini aktif tanpa perlu membacanya ulang setiap task.

Jangan mewajibkan `A + B` atau persona lain hanya untuk menggunakan coding rules.

Template/domain tambahan digunakan berdasarkan scope task.

Contoh:

Backend:
`be-rules.md`

Frontend/UI:
`fe-rules.md`

Git:
`git-*.md`

Planning:
Gunakan plan/checkpoint lifecycle aktif; execution plan Andino bila aktif. Jangan membuat file task atau lifecycle paralel hanya untuk memenuhi template.

Jangan memuat semua rule sekaligus jika task hanya membutuhkan sebagian.

## 1. Source of Truth

Untuk kondisi implementation saat ini gunakan:

repository aktual

>

configuration aktif

>

tests

>

documentation yang masih sesuai

>

memory/index lama

>

asumsi.

Repository mencakup bila relevan:

* source code,
* manifests,
* lockfiles,
* schema,
* migrations,
* configs,
* tests,
* CI/CD,
* deployment config,
* scripts,
* dan generated metadata yang memang menjadi source of truth.

Jika documentation dan implementation bertentangan:

jangan diam-diam memilih documentation.

Gunakan behavior/config aktual sebagai current state dan catat konflik bila material.

## 2. Instruction Scope

Sebelum mengubah file, hormati instruction yang berlaku pada scope file tersebut.

Instruction dapat berasal dari:

* root agent instruction,
* nested `AGENTS.md`,
* `CLAUDE.md`,
* `GEMINI.md`,
* Cursor Rules,
* Copilot instructions,
* OpenCode instructions,
* atau mechanism lain yang digunakan environment.

Jangan mengasumsikan semua coding agent memiliki hierarchy yang sama.

Jika nested instruction lebih spesifik terhadap directory yang disentuh dan host mendukung scope tersebut:

ikuti instruction yang lebih spesifik.

OpenAI Codex, misalnya, mendefinisikan scope `AGENTS.md` berdasarkan directory tree dan meminta agent menjalankan programmatic checks yang ditetapkan instruction tersebut.

## 3. Detect the Project

Sebelum membuat keputusan stack-specific, identifikasi project dari bukti repository.

Periksa seperlunya:

* manifest,
* lockfile,
* workspace config,
* framework config,
* build config,
* source tree,
* test configuration,
* database/schema,
* deployment config,
* dan existing patterns.

Jangan menganggap project selalu:

`backend + frontend + database`.

Project boleh hanya memiliki satu atau tidak satu pun dari komponen tersebut.

## 4. Existing Stack Wins

Gunakan teknologi dan convention yang sudah dipakai project.

Jangan mengganti stack secara diam-diam.

Contoh:

React tidak diganti Vue.

Express tidak diganti NestJS.

Django tidak diganti FastAPI.

REST tidak diganti GraphQL.

pnpm tidak diganti npm.

Vitest tidak diganti Jest.

Raw SQL tidak diganti ORM.

Three.js langsung tidak diganti React Three Fiber.

Perubahan technology membutuhkan requirement atau alasan teknis yang jelas.

## 5. Jangan Mengarang

Jangan mengarang:

* file,
* directory,
* route,
* component,
* package,
* API,
* symbol,
* database field,
* environment variable,
* command,
* branch,
* test,
* service,
* configuration,
* atau capability.

Jika belum diketahui:

gunakan `UNKNOWN` atau lakukan targeted inspection.

## 6. Understand Before Edit

Sebelum coding:

1. pahami objective user,
2. temukan area implementation,
3. baca context yang cukup,
4. pahami existing pattern,
5. identifikasi dependency,
6. tentukan perubahan minimum,
7. baru edit.

Jangan membuat solusi berdasarkan nama file saja tanpa memahami code yang relevan.

## 7. Search Before Broad Read

Untuk repository sedang atau besar:

gunakan search lebih dahulu.

Prioritaskan bila tersedia:

* symbol search,
* references,
* repository search,
* grep/rg,
* semantic navigation,
* dependency graph,
* file map,
* atau code index.

Jangan membaca seluruh repository untuk satu masalah lokal.

## 8. Progressive Context

Mulai dari context paling dekat dengan masalah.

Perluas hanya jika evidence menunjukkan masalah berada di luar area awal.

Contoh:

function
->
file
->
module
->
consumer
->
subsystem.

Jangan langsung membuka puluhan file.

## 9. Minimal Change

Pilih perubahan paling kecil yang memenuhi requirement secara benar.

Hindari:

* unrelated refactor,
* broad rename,
* folder restructure,
* dependency tambahan,
* abstraction baru,
* framework migration,
* formatting seluruh repository,
* atau architecture baru

jika tidak dibutuhkan.

Minimal change tidak berarti:

* mengabaikan test,
* mengabaikan security,
* mempertahankan bug terkait,
* atau menghasilkan patch rapuh.

## 10. Preserve Behavior

Jangan mengubah behavior yang tidak termasuk scope.

Perhatikan terutama:

* public API,
* user-visible behavior,
* permission,
* business rule,
* persistence,
* serialization,
* file format,
* event contract,
* CLI output,
* status/error behavior,
* dan integration contract.

Jika behavior harus berubah:

jelaskan dan verifikasi konsekuensinya.

## 11. Follow Existing Conventions

Ikuti pattern repository untuk:

* naming,
* formatting,
* imports,
* error handling,
* directory placement,
* composition,
* state management,
* logging,
* testing,
* configuration,
* dependency injection,
* response shape,
* dan documentation.

Jangan menerapkan gaya pribadi jika project sudah konsisten.

## 12. Architecture

Jangan memaksakan architecture tertentu.

Tidak semua project membutuhkan:

Controller
->
Service
->
Repository

atau:

Domain
->
Use Case
->
Adapter.

Gunakan abstraction yang memang sudah ada atau benar-benar dibutuhkan.

Jangan menambah layer hanya agar code terlihat "enterprise."

## 13. Responsibility

Pisahkan responsibility jika pemisahan tersebut:

* mengurangi coupling,
* meningkatkan testability,
* mencegah duplication,
* memperjelas ownership,
* atau menjaga boundary.

Jangan memecah function/file kecil menjadi banyak abstraction tanpa manfaat.

## 14. Reuse Before Create

Sebelum membuat:

* helper,
* hook,
* component,
* service,
* util,
* abstraction,
* type,
* schema,
* atau wrapper,

cari implementation existing.

Reuse jika sesuai.

Jangan membuat duplikasi hanya karena lebih cepat menulis ulang.

## 15. Dead Code

Jika perubahan membuat:

* import,
* variable,
* function,
* branch,
* dependency,
* atau configuration

menjadi tidak digunakan:

hapus jika aman dan berada dalam scope perubahan.

Jangan menjalankan cleanup repo-wide hanya karena menemukan dead code yang tidak terkait.

## 16. Naming

Gunakan nama yang menjelaskan intent.

Pertahankan terminology domain existing.

Jangan mengganti istilah domain yang sudah mapan hanya demi variasi bahasa.

## 17. Comments

Komentar digunakan untuk menjelaskan:

* alasan,
* constraint,
* invariant,
* workaround,
* compatibility issue,
* atau keputusan non-obvious.

Jangan membuat komentar yang hanya mengulang baris code.

Jangan menetapkan jumlah komentar tetap seperti:

"maksimal 1–2 komentar."

Jumlah komentar mengikuti kebutuhan code.

## 18. Jangan Tinggalkan AI Residue

Hapus sebelum final:

* komentar langkah AI,
* marker temporary,
* catatan "TODO by AI",
* debugging output,
* placeholder reasoning,
* obsolete commented code,
* atau explanation line-by-line yang tidak diperlukan.

Hasil akhir harus konsisten dengan style repository.

## 19. Bahasa

Ikuti bahasa dan convention project.

Code identifier:
ikuti codebase.

Comment:
ikuti codebase.

Public API:
ikuti contract.

Log:
ikuti operational convention.

Commit message:
ikuti git rules.

User-facing copy:
ikuti bahasa/localization produk.

Documentation:
ikuti bahasa project atau instruksi user.

Jangan memaksa seluruh komentar, log, error, dan commit memakai bahasa Indonesia jika repository menggunakan convention lain.

## 20. Dependencies

Sebelum menambah dependency:

periksa apakah kebutuhan sudah tersedia melalui:

* standard library,
* platform API,
* framework,
* existing dependency,
* atau existing utility.

Tambahkan dependency hanya jika manfaatnya jelas.

Jangan mengarang nama package.

## 21. Version Compatibility

Jika menggunakan API/library yang version-sensitive:

periksa version yang benar-benar digunakan project.

Jangan menulis code untuk latest documentation jika repository memakai versi lama.

Jika behavior dapat berubah dan belum cukup yakin:

gunakan dokumentasi resmi/current.

## 22. Package Manager

Gunakan package/dependency manager existing.

Contoh:

Node ecosystem:
npm / pnpm / Yarn / Bun sesuai repo.

Python:
pip / uv / Poetry / PDM sesuai repo.

Rust:
Cargo.

Go:
Go modules.

PHP:
Composer.

Dart:
pub.

Jangan mengganti package manager tanpa task eksplisit.

## 23. Lockfiles

Pertahankan konsistensi manifest dan lockfile.

Jika dependency berubah:

update lockfile menggunakan tool project yang benar jika environment memungkinkan.

Jangan edit lockfile besar secara manual kecuali tool/project memang membutuhkannya.

## 24. Generated Files

Identifikasi generated code/artifacts.

Jika file dihasilkan dari source lain:

ubah source generator bila itu source of truth.

Jangan edit:

* build output,
* generated client,
* compiled file,
* ORM output,
* generated type,
* vendor code

secara manual jika perubahan akan hilang pada regeneration.

## 25. Configuration

Ikuti configuration mechanism existing.

Jangan hardcode environment-specific value jika project memakai configuration/environment mechanism.

Pisahkan:

* development,
* test,
* staging,
* production

hanya jika project memang memiliki environment tersebut.

## 26. Secrets

Jangan hardcode atau expose:

* password,
* API key,
* token,
* credential,
* private key,
* connection secret.

Jangan memasukkan secret ke:

* code,
* logs,
* tests,
* documentation,
* example output,
* commit.

Gunakan secret/config mechanism project.

## 27. Security

Security mengikuti attack surface dan risiko task.

Jangan memakai checklist security yang sama untuk semua perubahan.

Periksa hal yang relevan seperti:

* validation,
* authorization,
* injection,
* secret exposure,
* unsafe file handling,
* unsafe deserialization,
* path traversal,
* XSS,
* CSRF,
* SSRF,
* dependency risk,
* permission,
* resource abuse,
* atau sensitive logging.

NIST SSDF sendiri bersifat outcome-based dan dimaksudkan untuk disesuaikan dengan risiko, kebutuhan bisnis, feasibility, dan resource, bukan diterapkan sebagai checklist mekanis.

## 28. Validation

Validasi input di trust boundary yang tepat.

Jangan menerapkan aturan:

"semua input harus divalidasi server-side"

pada project yang bahkan tidak memiliki server.

Contoh boundary:

* API request,
* CLI arguments,
* IPC,
* file input,
* message queue,
* browser form,
* external integration,
* plugin interface,
* library public API.

Validation mengikuti ownership dan threat model.

## 29. Error Handling

Ikuti error model project.

Jangan membungkus setiap operasi dengan `try/catch` hanya karena berpotensi gagal.

Tangani error pada layer yang:

* dapat mengambil tindakan,
* dapat menambah context berguna,
* atau bertanggung jawab atas user/system response.

Jangan swallow error penting.

Jangan membuat catch yang hanya:

catch
->
log
->
throw

tanpa nilai tambahan kecuali logging pada boundary memang diperlukan.

## 30. User-Facing Errors

Pesan error untuk pengguna harus:

* jelas,
* sesuai konteks,
* tidak membocorkan detail sensitif,
* dan dapat ditindaklanjuti jika memungkinkan.

Machine-facing API/library errors boleh menggunakan stable codes atau structure yang berbeda.

Jangan memaksa semua error berbentuk teks natural.

## 31. Logging

Ikuti logging convention project.

Tambahkan log hanya jika memberi nilai operasional atau debugging.

Jangan log:

* secrets,
* access token,
* password,
* sensitive payload,
* atau PII yang tidak diperlukan.

Jangan menambah noise log hanya untuk menunjukkan sebuah function dipanggil.

## 32. Data dan Persistence

Aturan database hanya berlaku jika task menggunakan persistence.

Jangan memaksakan database rules pada:

* static site,
* pure library,
* local tool,
* atau project tanpa persistence.

Jika database digunakan:

muat `be-rules.md` atau rule domain yang sesuai.

## 33. Transactions

Jangan menggunakan transaction secara mekanis untuk semua multi-write.

Gunakan berdasarkan:

* atomicity requirement,
* consistency model,
* storage capability,
* dan failure semantics.

Jangan menganggap transaction relational berlaku pada semua storage.

## 34. Idempotency

Idempotency hanya diperlukan ketika operation dapat diulang dan duplicate effect bermasalah.

Contoh:

* payment,
* webhook,
* provisioning,
* retryable operation,
* queue delivery.

Jangan membuat setiap operation idempotent hanya karena merupakan write.

## 35. Concurrency

Periksa concurrency jika beberapa execution dapat menyentuh state yang sama.

Jangan menambah locking atau synchronization jika tidak ada concurrency risk yang nyata.

## 36. Heavy Work

Jangan menetapkan:

"semua import/export/sync harus queue."

Pilih execution model berdasarkan:

* durasi,
* reliability,
* platform,
* user expectation,
* retry need,
* resource,
* dan architecture.

Pilihan dapat berupa:

* synchronous,
* streaming,
* chunked,
* background,
* queue,
* batch,
* worker.

Gunakan mekanisme paling sederhana yang memenuhi requirement.

## 37. Frontend-Specific Work

Jika task menyentuh frontend:

gunakan `fe-rules.md` jika tersedia.

Jangan memperluas baseline `code-rules.md` menjadi seluruh design/UI specification.

## 38. Backend-Specific Work

Jika task menyentuh backend:

gunakan `be-rules.md` jika tersedia.

Jangan menduplikasi seluruh backend specification di baseline ini.

## 39. Mobile / Desktop / CLI / Library

Jangan menganggap semua code memiliki HTTP request lifecycle.

Sesuaikan behavior dengan platform.

CLI:

* stdout/stderr,
* exit code,
* signal,
* piping.

Library:

* public API,
* compatibility,
* exceptions/errors,
* versioning.

Mobile:

* lifecycle,
* permission,
* offline,
* device resource.

Desktop:

* OS integration,
* filesystem,
* packaging.

Embedded:

* memory,
* timing,
* hardware constraint.

Gunakan hanya requirement yang relevan.

## 40. Monorepo

Jika repository adalah monorepo:

identifikasi package/workspace yang benar.

Jangan mengasumsikan semua package memakai:

* framework,
* language,
* build,
* test,
* atau deployment

yang sama.

Hormati nested instructions dan package-specific configuration.

## 41. Legacy Code

Legacy code tidak otomatis harus direfactor.

Jika pola lama bekerja dan perubahan task lokal:

buat perubahan terkecil yang aman.

Jika legacy behavior menyebabkan bug/security issue:

perbaiki bagian yang perlu dan batasi blast radius.

Jangan menjadikan satu bug sebagai alasan rewrite subsystem.

## 42. Compatibility

Pertimbangkan compatibility jika perubahan menyentuh:

* public interface,
* serialized data,
* schema,
* CLI flags,
* file format,
* protocol,
* browser/OS support,
* plugin API,
* atau consumer lain.

Jangan membuat breaking change diam-diam.

## 43. Performance

Jangan optimasi berdasarkan intuisi saja jika measurement memungkinkan.

Jika task performance:

profile atau ukur bottleneck.

Optimalkan area yang terbukti bermasalah.

Jangan melakukan premature optimization untuk task biasa.

## 44. Accessibility

Jika task menghasilkan UI yang digunakan manusia:

periksa accessibility sesuai `fe-rules.md` dan requirement project.

Jangan menerapkan aturan accessibility UI pada code non-UI.

## 45. Tests

Gunakan test setup existing.

Pilih test yang paling relevan terhadap perubahan.

Contoh:

unit
untuk logic lokal.

integration
untuk boundary.

contract
untuk interface.

E2E
untuk critical flow.

visual/browser
untuk UI.

performance
untuk performance requirement.

Jangan menambahkan testing framework baru jika existing setup sudah cukup.

## 46. Test Scope

Mulai dari targeted validation.

Perluas berdasarkan blast radius.

Jangan otomatis menjalankan seluruh test suite untuk perubahan satu baris jika:

* targeted test cukup,
* repo instructions tidak mewajibkan full suite,
* dan risiko perubahan kecil.

Sebaliknya:

jangan hanya menjalankan unit test jika perubahan memengaruhi banyak subsystem.

## 47. Validation Before Completion

Sebelum mengatakan:

* selesai,
* fixed,
* works,
* resolved,

gunakan evidence yang cukup.

Validation dapat berupa:

* test,
* typecheck,
* compiler,
* lint,
* build,
* E2E,
* manual reproduction,
* browser inspection,
* runtime check,
* atau domain-specific verification.

Pilih yang benar-benar membuktikan perubahan.

## 48. Required Checks

Jika repository instruction menetapkan command/check wajib:

jalankan best effort sebelum final.

Ini sejalan dengan model `AGENTS.md` Codex, yang memperlakukan programmatic checks di instruction sebagai bagian validasi perubahan.

## 49. Failed Validation

Jika validation gagal:

jangan menyembunyikan.

Klasifikasikan:

* akibat patch,
* existing failure,
* environment problem,
* dependency issue,
* unrelated failure.

Perbaiki yang berada dalam scope.

Laporkan sisanya dengan singkat.

## 50. Git Working Tree

Sebelum perubahan yang dapat berbenturan dengan pekerjaan lain:

periksa working tree jika Git tersedia.

Tujuannya:

* tidak menimpa perubahan user,
* memahami dirty files,
* dan membatasi diff.

Tidak wajib menjalankan `git status` pada setiap pertanyaan atau task read-only.

## 51. Jangan Menghapus Perubahan User

Jangan:

* reset,
* checkout,
* overwrite,
* revert,
* clean,
* atau discard

perubahan yang tidak dibuat agent tanpa instruksi yang jelas.

Jika file target sudah memiliki modification user:

integrasikan perubahan secara hati-hati.

## 52. Git Operations

Jangan melakukan:

* commit,
* push,
* merge,
* rebase,
* force push,
* tag,
* branch deletion

tanpa user instruction atau workflow project yang jelas mengizinkannya.

Membuat code benar tidak otomatis memberi izin mengubah remote repository.

## 53. Review Diff

Setelah implementation:

review diff yang relevan jika tool memungkinkan.

Cari:

* perubahan tidak terkait,
* debug residue,
* accidental formatting,
* secret,
* generated artifact,
* missing file,
* atau behavior change tak disengaja.

## 54. Tool Use

Tool adalah sarana, bukan requirement architecture.

Gunakan tool minimum yang menyelesaikan task dengan baik.

Jangan memakai:

* semantic tool,
* filesystem MCP,
* Git MCP,
* browser MCP,
* Context7,
* Graphify,
* Sequential Thinking

secara bersamaan jika satu atau dua tool sudah cukup.

## 55. RTK

Jika RTK tersedia dan project/environment sudah menggunakannya:

boleh gunakan untuk mengurangi terminal output.

Jika hook/plugin otomatis menangani RTK:

jangan paksa prefix manual.

Jika RTK tidak tersedia:

gunakan command native.

Jangan gagal atau menunda task hanya karena `rtk` tidak ada.

## 56. External Documentation

Gunakan web/documentation ketika informasi eksternal memang diperlukan.

Contoh:

* library API berubah,
* framework behavior version-sensitive,
* deprecation,
* external service contract,
* platform limit,
* current SDK.

Prioritaskan:

1. official documentation,
2. official source/release notes,
3. issue/discussion upstream,
4. credible technical source.

Jangan web search untuk setiap edit lokal.

## 57. External Side Effects

Pisahkan implementation lokal dari tindakan eksternal.

Contoh side effect:

* deploy,
* publish,
* push,
* merge,
* send message,
* mutate production data,
* rotate credential,
* delete cloud resource.

Jangan menjalankan side effect hanya karena implementation sudah selesai.

Ikuti permission model agent/environment.

## 58. Destructive Operations

Untuk tindakan destruktif atau sulit dibatalkan:

jangan menebak intent.

Contoh:

* drop database,
* delete data,
* remove branch,
* overwrite user work,
* rotate production secret,
* destroy infrastructure.

Minta confirmation bila belum eksplisit.

## 59. Simplicity

Pilih solusi paling sederhana yang tetap:

* benar,
* aman,
* maintainable,
* testable sesuai kebutuhan,
* dan konsisten dengan project.

Jangan menyamakan simplicity dengan jumlah baris minimum.

## 60. No Premature Abstraction

Jangan membuat abstraction untuk hypothetical future use.

Gunakan abstraction ketika ada:

* repeated behavior,
* clear boundary,
* real substitution need,
* testing benefit,
* atau maintainability gain.

## 61. Refactor

Refactor hanya jika:

* diminta,
* diperlukan untuk implementation,
* atau secara langsung mengurangi risiko perubahan.

Pisahkan refactor besar dari behavioral change bila memungkinkan agar review mudah.

## 62. Scope Control

Jika menemukan masalah lain di luar scope:

jangan otomatis memperbaikinya.

Jika kritis:

laporkan.

Jika kecil:

abaikan atau catat singkat.

Jangan membesarkan diff tanpa alasan.

## 63. Planning

Task kecil:

langsung kerjakan.

Task sedang:

buat internal plan secukupnya.

Task kompleks:

susun dependency dan validation sebelum edit.

Jangan membuat planning ceremony panjang untuk typo.

## 64. Clarification

Jangan bertanya jika context cukup.

Tanyakan hanya jika ambiguity material dapat menghasilkan implementation berbeda.

Gunakan satu batch singkat jika diperlukan.

Jika assumption aman:

lanjutkan.

## 65. Current User Intent

Instruksi eksplisit user tentang:

* scope,
* stack,
* framework,
* behavior,
* compatibility,
* atau constraint

lebih penting daripada preference agent.

Jangan diam-diam "memperbaiki" requirement menjadi architecture favorit agent.

## 66. Output

Untuk implementation task, output akhir default ringkas:

* apa yang berubah,
* area/file penting,
* validation yang dijalankan,
* hasil,
* blocker/limitation bila ada.

Tidak perlu menjelaskan setiap line code.

Tidak perlu menampilkan private reasoning.

## 67. Audit Mode

Jika user meminta audit:

jangan langsung mengubah kode kecuali diminta.

Urutkan finding berdasarkan impact.

Untuk setiap finding:

* masalah,
* evidence,
* impact,
* recommendation.

Jangan membuat severity numerik palsu.

## 68. Read-Only Tasks

Untuk:

* explain,
* review,
* inspect,
* audit,
* answer question

jangan mengubah file kecuali user meminta perubahan.

## 69. Documentation Update

Update documentation jika patch membuat docs existing menjadi salah secara material.

Jangan membuat docs baru hanya karena implementation berubah sedikit.

## 70. Definition of Complete

Task coding dapat dianggap selesai bila:

* requirement yang diminta terpenuhi,
* perubahan berada dalam scope,
* repository convention dipertahankan,
* validation relevan dilakukan,
* tidak ada blocker penting tersembunyi,
* dan output menjelaskan status sebenarnya.

Tidak perlu mengejar kesempurnaan seluruh repository.

## 71. Prioritas Konflik

Untuk intent, scope dan keputusan kerja, ikuti instruksi eksplisit user terbaru, lalu aturan project yang berlaku, keputusan/checkpoint yang disepakati, dan default template. Tetap patuhi hierarchy instruksi host serta batas platform, permission, security dan kebijakan yang benar-benar enforced; jangan menonaktifkan pembatas tersebut untuk memenuhi permintaan. Untuk fakta implementasi, repository/config/test aktual mengungguli dokumentasi atau memory yang stale; fakta baru tidak otomatis membatalkan keputusan user.

Urutan umum:

1. system/platform/agent constraints,
2. latest explicit user instructions within those constraints,
3. applicable repository instructions,
4. project-specific rules,
5. domain rules seperti backend/frontend,
6. baseline `code-rules.md`,
7. generic best practice.

Framework defaults tidak boleh mengalahkan requirement project yang valid.

Generic best practice tidak boleh mengalahkan fakta repository.

## 72. Cek Internal Sebelum Edit

Periksa secara internal:

* task sebenarnya apa?
* area code mana yang relevan?
* instruction scope apa yang berlaku?
* stack apa yang benar-benar digunakan?
* ada user changes?
* existing abstraction yang bisa dipakai?
* dependency baru benar-benar perlu?
* public behavior terdampak?
* security boundary relevan?
* test apa yang membuktikan perubahan?

Jangan tampilkan checklist ini kecuali diminta.

## 73. Cek Internal Sebelum Final

Periksa:

* requirement terpenuhi?
* diff minimum?
* tidak ada unrelated change?
* tidak ada secret?
* tidak ada debug residue?
* generated file tidak salah edit?
* validation cukup?
* failure sudah dilaporkan?
* claim sesuai evidence?
* docs perlu diperbarui?
* tidak ada user work tertimpa?

Jangan tampilkan checklist ini kecuali diminta.

## 74. Prinsip Akhir

Deteksi repository, jangan menebak.

Ikuti stack existing.

Hormati scoped instructions.

Pahami sebelum edit.

Search sebelum broad read.

Reuse sebelum create.

Buat perubahan minimum.

Jangan overengineer.

Jangan menambah dependency tanpa alasan.

Security mengikuti risiko.

Validation mengikuti blast radius.

Jangan menghapus perubahan user.

Tool bersifat opsional.

RTK bukan requirement universal.

Repository adalah source of truth untuk current implementation.

Verifikasi sebelum menyatakan selesai.
