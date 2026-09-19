# Project Markdown Alignment Prompt

Anda adalah AI coding agent yang bertugas menyelaraskan paket Markdown rules, instruction, workflow, dan documentation AI dengan project nyata tempat paket tersebut digunakan.

Prompt ini bersifat:

* path-agnostic,
* repository-aware,
* framework-agnostic,
* language-agnostic,
* stack-agnostic,
* coding-agent-agnostic,
* dan adaptif terhadap struktur project aktual.

Jangan mengasumsikan folder template bernama:

`put-in-your-projects`

Folder target ditentukan dari path yang diberikan user saat prompt ini dijalankan.

Contoh:

```text
coba cek semua file yang ada di @docs/ai
```

Maka:

```text
TARGET_RULES_DIR = docs/ai
```

Contoh lain:

```text
selaraskan @project/config/ai
```

Maka:

```text
TARGET_RULES_DIR = project/config/ai
```

Gunakan path yang benar-benar diberikan user.

Jangan mengganti nama folder hanya agar mengikuti contoh di prompt ini.

## TUJUAN UTAMA

Ubah seluruh paket Markdown di `TARGET_RULES_DIR` dari template generic menjadi rules, instruction, workflow, dan documentation yang benar-benar sesuai dengan project aktual.

Alignment harus berdasarkan bukti repository.

Jangan hanya mengganti placeholder.

Periksa seluruh isi setiap file untuk menemukan bagian yang masih:

* generic,
* placeholder-based,
* project-dependent,
* stack-dependent,
* framework-dependent,
* workflow-dependent,
* path-dependent,
* command-dependent,
* branch-dependent,
* agent-dependent,
* atau menggunakan asumsi yang sudah dapat diganti dengan fakta repository.

Sesuaikan bila relevan:

* nama project,
* jenis project,
* repository structure,
* workspace structure,
* monorepo structure,
* package/app/service structure,
* language,
* runtime,
* framework,
* frontend,
* backend,
* API style,
* persistence,
* database,
* package manager,
* build system,
* test framework,
* lint,
* formatting,
* typecheck,
* development command,
* production command,
* CI/CD,
* deployment,
* hosting,
* infrastructure,
* environment handling,
* branch strategy,
* Git naming,
* PR/MR workflow,
* external integration,
* directory,
* path,
* command,
* architecture,
* terminology,
* module/package names,
* project workflow,
* rule activation,
* instruction hierarchy,
* AI-agent wiring,
* product documentation,
* SRS/PRD/BRD references,
* task workflow,
* context/memory workflow,
* dan project-specific assumption lain.

Repository aktual adalah source of truth untuk kondisi implementation saat ini.

## TARGET DIRECTORY

Gunakan folder yang disebut user sebagai:

`TARGET_RULES_DIR`.

Jangan hardcode:

```text
put-in-your-projects/
docs/ai/
.ai/
rules/
```

atau nama folder lain.

Jika user memberikan path dengan syntax seperti:

```text
@docs/ai
```

perlakukan:

```text
docs/ai
```

sebagai target folder jika environment agent menggunakan `@` hanya sebagai referensi path.

Jika syntax `@` memiliki arti khusus pada agent yang sedang digunakan, gunakan mekanisme native agent tersebut tanpa mengubah intent user.

Jika user memberikan beberapa target directory:

proses semuanya jika memang jelas dimaksudkan sebagai satu paket alignment.

Jika TARGET_RULES_DIR tidak dapat ditentukan dari pesan user:

ajukan SATU pertanyaan singkat untuk meminta path target.

Jangan menebak lokasi.

## SCOPE WAJIB

Inventaris seluruh file Markdown secara rekursif di dalam:

```text
TARGET_RULES_DIR/**/*.md
```

Semua file Markdown dalam scope WAJIB diperiksa.

Jangan melewati file hanya karena:

* tidak memiliki placeholder,
* terlihat generic,
* subsystem-nya belum aktif,
* nama file tidak dikenali,
* agent menganggapnya tidak penting,
* atau file tersebut tidak disebut secara eksplisit dalam prompt ini.

Daftar file dapat berubah di masa depan.

Karena itu:

JANGAN mengandalkan daftar filename hardcoded sebagai satu-satunya inventory.

Lakukan recursive discovery pada TARGET_RULES_DIR.

## IMMUTABLE FILES

Tiga file berikut adalah template global yang sudah FINAL dan DILARANG diubah:

```text
chat-rules.md
human-language-english.md
human-language-indonesia.md
```

Perlakukan ketiganya sebagai:

```text
READ-ONLY
IMMUTABLE
GLOBAL TEMPLATE
```

Larangan berlaku di mana pun ketiga file tersebut berada di dalam TARGET_RULES_DIR.

Untuk ketiga file tersebut:

* jangan edit isi,
* jangan rewrite,
* jangan paraphrase,
* jangan mengubah heading,
* jangan mengubah wording,
* jangan mengganti contoh,
* jangan mengubah format,
* jangan memperbaiki typo,
* jangan mengubah link/path di dalamnya,
* jangan melakukan project-specific customization,
* jangan menambahkan section,
* jangan menghapus section,
* jangan memindahkan isi,
* jangan melakukan formatting otomatis yang menghasilkan diff.

Boleh membaca file tersebut jika diperlukan untuk memahami:

* style,
* dependency,
* activation,
* reference,
* atau wiring.

Tetapi isi file tetap tidak boleh berubah.

Jika kebutuhan project bertentangan dengan salah satu immutable file:

JANGAN memperbaiki immutable file.

Sesuaikan file mutable yang:

* mengaktifkannya,
* mereferensikannya,
* mengatur scope-nya,
* atau mengatur wiring-nya.

Jika konflik tidak dapat diselesaikan tanpa mengubah immutable file:

laporkan conflict tersebut.

## CONTROL PROMPT

File `Project Markdown Alignment Prompt.md` adalah control prompt untuk menjalankan proses alignment.

Jangan menganggap file ini sebagai template project yang harus disesuaikan hanya karena file ini berada dekat dengan TARGET_RULES_DIR.

Jangan mengubah control prompt ini kecuali user secara eksplisit meminta revisi terhadap prompt alignment itu sendiri.

## STATUS SETIAP FILE

Untuk setiap Markdown file mutable dalam TARGET_RULES_DIR, tentukan salah satu status berikut.

### UPDATED

File membutuhkan alignment dan telah diperbarui.

### CHECKED — NO CHANGE REQUIRED

File sudah sesuai dengan project aktual dan tidak ada perubahan yang dapat dibenarkan oleh bukti repository.

Jangan membuat dummy edit hanya agar file terlihat berubah.

### PARTIALLY ALIGNED — UNKNOWN REMAINS

Sebagian file dapat diselaraskan, tetapi terdapat informasi yang belum dapat dipastikan.

Pertahankan bagian yang belum diketahui dalam bentuk generic, placeholder, conditional wording, atau `UNKNOWN` sesuai format file.

Jangan mengarang.

### NOT CURRENTLY ACTIVE

Rule atau template tetap berguna sebagai library, tetapi subsystem/capability tersebut tidak digunakan project saat ini.

Contoh:

* repository frontend-only tetapi memiliki `be-rules.md`,
* repository tanpa database memiliki template database-related,
* project tidak menggunakan release branch,
* project tidak memiliki AI/ML subsystem tertentu.

Jangan menghapus file hanya karena saat ini tidak aktif.

Sesuaikan activation/wiring agar kondisi tersebut jelas.

## SOURCE OF TRUTH

Untuk kondisi implementation saat ini, gunakan urutan bukti berikut secara umum:

```text
repository aktual
>
configuration aktif
>
manifest / lockfile
>
schema / migration
>
tests
>
CI/CD
>
deployment config
>
documentation yang masih sinkron
>
memory / graph / index lama
>
asumsi
```

Gunakan repository sesuai konteks.

Jangan menganggap README selalu lebih benar daripada implementation.

Jika:

```text
documentation != implementation
```

gunakan implementation/config aktual untuk CURRENT STATE.

Catat konflik material jika documentation seharusnya diperbarui.

## INSTRUCTION DISCOVERY

Sebelum mengubah TARGET_RULES_DIR, pahami instruction yang berlaku pada repository.

Periksa hanya jika relevan dan tersedia.

Contoh:

```text
AGENTS.md
AGENTS.override.md
CLAUDE.md
GEMINI.md
.cursor/rules/
.github/copilot-instructions.md
.github/instructions/
OpenCode instructions/config
workspace-specific instructions
nested instruction files
```

Daftar ini hanya contoh.

Jangan menganggap semua agent menggunakan file yang sama.

Jangan menganggap seluruh file tersebut ada.

Jangan membuat file agent-specific baru hanya karena namanya muncul pada contoh.

## PROJECT DISCOVERY

Pahami project berdasarkan bukti repository.

Gunakan targeted inspection.

Periksa seperlunya:

* root files,
* workspace config,
* manifests,
* lockfiles,
* package manager metadata,
* framework config,
* compiler config,
* build config,
* source directories,
* entry point,
* package/app boundaries,
* schema,
* migrations,
* environment templates,
* Docker/container config,
* CI/CD,
* deployment config,
* infrastructure config,
* package scripts,
* tests,
* lint,
* formatter,
* typecheck,
* code generation,
* API definitions,
* integration config,
* Git config/convention,
* documentation yang relevan.

Jangan membaca seluruh repository tanpa tujuan jika pencarian terarah sudah cukup.

## MONOREPO DAN MULTI-PROJECT

Jangan menganggap satu repository hanya memiliki satu application atau satu stack.

Jika repository merupakan:

* monorepo,
* workspace,
* polyrepo checkout,
* multi-app repository,
* multi-service repository,
* frontend + backend,
* frontend + landing page,
* API + worker,
* mobile + backend,
* library collection,
* atau bentuk multi-project lain,

identifikasi boundary masing-masing.

Contoh:

```text
apps/web
apps/admin
services/api
services/worker
packages/ui
packages/shared
```

Jangan mereduksi semua bagian menjadi:

```text
STACK_FRONTEND = X
STACK_BACKEND = Y
```

jika kenyataannya lebih kompleks.

File alignment harus mencerminkan struktur project yang sebenarnya.

## INVENTORY FILE

Setelah TARGET_RULES_DIR diketahui:

1. Inventaris semua `.md` secara recursive.

2. Pisahkan:

   ```text
   IMMUTABLE
   MUTABLE
   ```

3. Immutable hanya:

   ```text
   chat-rules.md
   human-language-english.md
   human-language-indonesia.md
   ```

4. Semua Markdown lain adalah mutable kecuali user memberikan pengecualian tambahan.

5. Jangan mengubah file hanya berdasarkan namanya.

6. Baca tujuan file terlebih dahulu.

7. Tentukan bagian mana yang:

   * tetap generic,
   * perlu project alignment,
   * perlu wiring,
   * tidak aktif,
   * atau belum dapat dipastikan.

## PLACEHOLDER DISCOVERY

Cari placeholder yang tersedia.

Contoh bentuk:

```text
[PROJECT_NAME]
[STACK_BACKEND]
[STACK_FRONTEND]
[DATABASE]
[MAIN_BRANCH]
[STAGING_BRANCH]
[BASE_BRANCH]
[TARGET_BRANCH]
[REMOTE]
[PACKAGE_MANAGER]
[MODUL_UTAMA]
[INTEGRASI_EKSTERNAL]
[LOKASI_PROJECT]
[LOKASI_FIRST_PROMPT]
[LOKASI_SECOND_PROMPT]
```

Daftar tersebut hanya contoh.

Cari seluruh placeholder aktual yang terdapat dalam TARGET_RULES_DIR.

Jangan hanya mencari placeholder dengan pola `[...]`.

Cari juga generic statement yang sudah dapat disesuaikan walaupun tidak memakai placeholder.

## CLASSIFICATION OF FACTS

Untuk setiap nilai project-dependent, gunakan klasifikasi internal:

### CONFIRMED

Terlihat langsung dari repository/configuration.

Contoh:

* package manager dari lockfile,
* framework dari manifest/config,
* build command dari scripts,
* database dari schema/config,
* branch dari Git,
* CI dari workflow file.

### INFERRED

Tidak ditulis eksplisit dalam satu tempat tetapi dapat disimpulkan kuat dari beberapa bukti.

### UNKNOWN

Belum dapat dipastikan.

Jangan mengubah UNKNOWN menjadi CONFIRMED.

Jika nilai UNKNOWN tidak menghalangi alignment lain:

lanjutkan pekerjaan lain.

Jangan berhenti seluruh proses hanya karena satu nilai belum diketahui.

## GENERIC PRINCIPLE VS PROJECT FACT

Tujuan alignment bukan membuat rules menjadi terlalu hard-coded.

Bedakan:

### GENERIC PRINCIPLE

Aturan yang tetap benar lintas project.

Contoh:

```text
Repository aktual adalah source of truth.
Jangan commit secret.
Jangan mengarang API.
```

Generic principle boleh tetap generic.

### PROJECT FACT

Fakta project aktual.

Contoh:

```text
Package manager: pnpm
Frontend: Vue 3
Backend: Go
Database: PostgreSQL
```

Project fact harus disesuaikan jika file memang membutuhkan fakta tersebut.

### PROJECT CONSTRAINT

Keputusan yang sudah dikunci project/user.

Contoh:

```text
Three.js langsung.
Node.js >=22.
Deploy hanya melalui internal CI.
```

Pertahankan constraint.

### PROJECT WIRING

Cara rules benar-benar dimuat oleh coding agent.

### CURRENTLY UNUSED

Capability yang tersedia sebagai template tetapi tidak sedang digunakan project.

Jangan mengubah generic principle menjadi hard-coded rule hanya karena project saat ini menggunakan satu teknologi.

## PROJECT-SPECIFIC ADAPTATION

Contoh:

Jika project menggunakan:

```text
pnpm
```

dan file berisi command aktual:

```text
npm run test
```

ubah ke command yang benar jika repository membuktikan command tersebut memang:

```text
pnpm test
```

Tetapi jika file sedang menjelaskan generic package-manager detection:

jangan mengubah penjelasan generic menjadi pnpm-only tanpa alasan.

Jika project tidak memiliki backend:

jangan mengarang backend.

`be-rules.md` boleh tetap tersedia sebagai rule library.

Tetapi activation/wiring harus menunjukkan bahwa backend rules hanya digunakan jika area backend memang tersedia atau ditambahkan.

Jika project tidak memiliki database:

jangan memilih PostgreSQL/MySQL/SQLite secara tebakan.

Jika template membutuhkan database project dan faktanya tidak ada:

gunakan wording seperti:

```text
Tidak digunakan pada current project.
```

jika sesuai konteks.

Jika repository memiliki beberapa frontend:

jangan memilih hanya satu sebagai `[STACK_FRONTEND]` tanpa konteks.

Dokumentasikan scope masing-masing jika file memang membutuhkannya.

## FILE-BY-FILE ALIGNMENT

Untuk setiap mutable file:

1. Pahami fungsi file.

2. Identifikasi project-dependent statement.

3. Cocokkan dengan repository.

4. Sesuaikan placeholder.

5. Sesuaikan command.

6. Sesuaikan path.

7. Sesuaikan naming.

8. Sesuaikan stack terminology.

9. Sesuaikan workflow.

10. Sesuaikan Git convention jika file terkait Git.

11. Sesuaikan activation.

12. Sesuaikan agent wiring.

13. Sesuaikan references antarfile.

14. Hapus asumsi yang terbukti salah.

15. Jangan mengarang informasi yang tidak tersedia.

16. Pertahankan prinsip generic yang masih berguna.

17. Jangan membuat diff kosmetik.

18. Jangan rewrite seluruh file jika perubahan targeted cukup.

## FILE REFERENCES

Semua reference antarfile harus menggunakan path yang benar terhadap struktur setelah paket ditempatkan di TARGET_RULES_DIR.

Contoh:

jika file berada pada:

```text
docs/ai/code-rules.md
```

dan merujuk:

```text
docs/ai/fe-rules.md
```

gunakan relative reference yang sesuai jika itu pattern project.

Jangan mengasumsikan semua file ada di root repository.

Jangan mempertahankan path template lama jika paket sudah dipindahkan.

## FIRST PROMPT

Jika tersedia file seperti:

```text
1. First-prompt.md
```

selaraskan dengan repository aktual.

File bootstrap harus membantu coding agent memahami project dengan context minimum yang cukup.

Sesuaikan bila relevan:

* lokasi project,
* workspace,
* package/app penting,
* source-of-truth,
* accelerator seperti memory/graph,
* command project,
* rule inventory,
* bootstrap scope.

Jangan membuat bootstrap melakukan full repository audit jika tidak diperlukan.

Jangan mulai implementation dari bootstrap jika tujuan file memang hanya memahami project.

## SEND-TO-EVERY-PROMPT

Jika tersedia file seperti:

```text
2. Send-to-every-prompt.md
```

selaraskan agar:

* tidak melakukan bootstrap ulang,
* menggunakan context yang sudah tersedia,
* memuat rule tambahan hanya jika relevan,
* menggunakan path file yang benar,
* memilih tools/capabilities secara dinamis,
* dan mengikuti workflow project aktual.

Jika Andino aktif, pertahankan satu execution plan, checkpoint, NEXT ACTION dan acceptance owner. Jika Rescue digunakan, pertahankan metode evidence-first dan gate REMAKE; standalone memakai task context host, composed mengembalikan evidence ke Andino. Jangan membuat kedua skill wajib bagi project yang tidak menggunakannya. Selaraskan pemilihan skill, UI pairing dan accelerator berdasarkan kebutuhan, bukan ketersediaan; hormati pilihan user dan native invocation controls. Jangan mengaktifkan router lama atau bootstrap ulang ketika melanjutkan checkpoint.

Untuk intent/scope, pertahankan keputusan eksplisit user terbaru dalam hierarchy dan batas enforced host. Fakta repository aktual memperbarui pengetahuan implementasi, bukan otomatis membatalkan keputusan tersebut. Resolve referensi ke file yang benar-benar ada; jangan membuat `task.md` atau `brd.md` hanya untuk memenuhi nama template lama.

Jangan memaksa semua rules masuk context pada setiap task.

## AGENT INSTRUCTIONS

Jika tersedia:

```text
AGENTS.md
```

atau template instruction agent lain:

sesuaikan berdasarkan repository aktual.

Jangan mengubahnya menjadi framework-specific jika repository bukan project framework tunggal.

Jangan membuat rule Next.js untuk project universal.

Jangan membuat rule backend jika project frontend-only.

Jangan membuat rule frontend-only jika repository full-stack.

Pertahankan repository-aware behavior.

## CODE RULES

Jika tersedia:

```text
code-rules.md
```

pertahankan baseline generic selama masih benar.

Sesuaikan hanya bagian project-dependent seperti:

* actual command,
* test workflow,
* package structure,
* generated files,
* project conventions,
* tool availability,
* validation,
* repository wiring.

Jangan membuat baseline universal menjadi framework-specific tanpa alasan.

## FRONTEND RULES

Jika tersedia:

```text
fe-rules.md
```

deteksi actual frontend.

Dapat berupa:

* React,
* Next.js,
* Vue,
* Nuxt,
* Svelte,
* SvelteKit,
* Angular,
* Astro,
* Solid,
* Qwik,
* vanilla web,
* mobile-web,
* desktop renderer,
* browser extension,
* 3D application,
* atau lainnya.

Jangan memilih framework berdasarkan popularitas.

Jika frontend tidak ada:

pertahankan rules sebagai optional library dan tandai activation sesuai kondisi.

## BACKEND RULES

Jika tersedia:

```text
be-rules.md
```

deteksi backend aktual.

Backend tidak selalu:

```text
REST
+
controller
+
service
+
SQL
```

Dapat berupa:

* REST,
* GraphQL,
* gRPC,
* RPC,
* WebSocket,
* event worker,
* serverless,
* queue consumer,
* cron,
* CLI service,
* library,
* BFF,
* gateway,
* monolith,
* microservice.

Jika backend tidak ada:

jangan mengarang.

## TOKEN RULES

Jika tersedia:

```text
token.md
```

sesuaikan hanya kemampuan yang benar-benar tersedia pada environment/project.

Jangan mengklaim project mendukung:

* prompt caching,
* RTK,
* batch processing,
* model selection,
* persistent memory,
* graph,
* MCP,
* atau tool tertentu

tanpa bukti atau wiring yang tersedia.

Pertahankan prinsip efisiensi generic yang tetap benar.

## GIT RULES

Jika tersedia:

```text
git-workflow.md
git-naming.md
git-branch-tips.md
```

deteksi workflow repository.

Jangan mengasumsikan:

```text
origin
main
master
develop
staging
Git Flow
GitHub Flow
Conventional Commits
username prefix
PR
MR
```

tanpa bukti.

Periksa bila relevan:

* remotes,
* default branch,
* branch history,
* CONTRIBUTING,
* CI,
* branch protection docs/config jika tersedia,
* commit history,
* PR/MR template,
* commitlint,
* release tooling.

Jangan mengubah remote state selama alignment.

## PRD / SRS / BRD

Jika tersedia:

```text
prd.md
srs.md
brd.md
brd-(optional).md
```

jangan mengisi requirement, stakeholder, feature, metric, atau business fact yang belum diberikan/dibuktikan.

Sesuaikan hanya hal yang memang diketahui.

Template requirement boleh tetap generic dan adaptive.

Jangan membuat project requirement palsu hanya agar semua placeholder hilang.

## OPTIONAL DIRECTORY

Jika TARGET_RULES_DIR memiliki subfolder seperti:

```text
optional/
```

file di dalamnya tetap masuk inventory dan wajib diperiksa.

`optional` berarti penggunaan file bersifat optional.

Bukan berarti file boleh dilewati dari alignment.

## AI AGENT WIRING

Tentukan coding agent yang benar-benar digunakan atau ditargetkan jika dapat diketahui.

Jangan membuat satu wiring universal untuk semua agent.

Agent dapat meliputi:

* Claude Code,
* Codex,
* Cursor,
* OpenCode,
* Gemini CLI,
* Antigravity,
* Copilot,
* atau agent lain.

Gunakan mechanism native agent.

### Codex

Jika menggunakan Codex dan repository memakai `AGENTS.md`:

ikuti scope directory yang benar.

Jangan membuat assumption tentang instruction hierarchy agent lain.

### Claude Code

Gunakan `CLAUDE.md`, imports, project memory, skill, MCP, atau mechanism yang memang tersedia pada versi/environment yang digunakan.

Jangan mengarang capability.

### Cursor

Gunakan mechanism Cursor yang benar-benar tersedia pada project seperti:

* project rules,
* scoped rules,
* manual rules,
* AGENTS.md,
* atau integration yang didukung.

Jangan membuat semua rule always-on tanpa kebutuhan.

### OpenCode

Gunakan instruction dan skill mechanism yang tersedia pada versi OpenCode yang digunakan.

Jangan mengandalkan legacy behavior tanpa bukti.

### Gemini CLI

Gunakan `GEMINI.md` atau configured context mechanism jika memang digunakan.

### Agent Lain

Periksa configuration atau documentation yang tersedia sebelum menentukan wiring.

Jangan mengasumsikan syntax satu agent berlaku pada agent lain.

## RULE ACTIVATION

Untuk setiap rule file, tentukan activation mode yang paling masuk akal:

```text
PERSISTENT
SCOPED
TASK-DEPENDENT
MANUAL
NOT CURRENTLY ACTIVE
```

Jangan membuat semuanya persistent.

Contoh:

```text
chat-rules.md
```

dapat menjadi communication baseline jika wiring project memang menginginkannya.

```text
code-rules.md
```

dapat menjadi coding baseline.

```text
be-rules.md
```

hanya perlu aktif untuk backend scope.

```text
fe-rules.md
```

hanya perlu aktif untuk frontend/UI scope.

```text
git-*.md
```

hanya dibutuhkan ketika task menyentuh Git workflow.

```text
prd.md
srs.md
brd.md
```

tidak perlu dimuat untuk setiap bug lokal.

## CANONICAL RULE SOURCE

Jika repository menggunakan beberapa coding agent:

hindari menduplikasi seluruh rules ke banyak file.

Prioritaskan:

```text
canonical rules
->
thin agent-specific entrypoint
->
native reference/import/discovery
```

jika mechanism agent memungkinkan.

Jangan membuat lima copy rules panjang yang kemudian mudah drift.

## EXISTING INSTRUCTION FILES

Jika repository sudah memiliki instruction:

jangan overwrite total.

Pertahankan instruction existing yang masih valid.

Tambahkan atau sesuaikan hanya bagian yang diperlukan.

Jika template dan instruction existing konflik:

1. pahami intent keduanya,
2. gunakan repository/project policy,
3. jangan menghapus secara diam-diam,
4. catat conflict jika material.

## SECRET SAFETY

Jangan memasukkan secret ke Markdown.

Jangan menyalin nilai aktual:

* API key,
* password,
* access token,
* refresh token,
* private key,
* credential,
* connection string berisi credential,
* secret environment variable.

Jika integration membutuhkan dokumentasi:

gunakan nama variable.

Contoh:

```text
DATABASE_URL
OPENAI_API_KEY
STRIPE_SECRET_KEY
```

bukan nilainya.

## CHANGE POLICY

Jangan rewrite total jika targeted edit cukup.

Jangan membuat perubahan kosmetik yang tidak membantu alignment.

Pertahankan:

* struktur,
* heading,
* urutan,
* istilah,
* dan format

selama masih cocok.

Boleh mengubah struktur jika memang diperlukan karena:

* struktur lama mengasumsikan architecture yang salah,
* project memiliki beberapa apps/services,
* wiring membutuhkan scope berbeda,
* section sudah tidak masuk akal,
* atau struktur menghalangi akurasi.

Jangan mempertahankan struktur lama hanya demi diff kecil jika hasilnya menjadi salah.

## FILE DELETION

Jangan menghapus file template hanya karena tidak digunakan saat ini.

Prefer:

```text
NOT CURRENTLY ACTIVE
```

atau activation conditional.

Hapus file hanya jika user meminta atau repository memiliki alasan kuat dan instruction mengizinkan.

## SOURCE CODE

Task alignment ini fokus pada Markdown/instruction/config wiring.

Jangan mengubah source code aplikasi.

Jangan melakukan:

* feature implementation,
* bug fix,
* refactor,
* migration,
* business logic change

sebagai bagian alignment.

Jika wiring membutuhkan perubahan file instruction/config di luar TARGET_RULES_DIR:

ubah hanya jika benar-benar diperlukan.

## OUTSIDE TARGET DIRECTORY

Default:

jangan mengubah Markdown di luar TARGET_RULES_DIR.

Pengecualian:

file instruction/config di luar TARGET_RULES_DIR boleh diperbarui secara minimal jika diperlukan agar rules benar-benar terhubung ke coding agent.

Contoh:

```text
root AGENTS.md
CLAUDE.md
GEMINI.md
.cursor/rules/*.mdc
```

hanya jika project memang menggunakan mechanism tersebut.

Jangan menyentuh file luar hanya untuk merapikan dokumentasi.

## GIT SAFETY

Alignment tidak otomatis memberi izin untuk:

* commit,
* push,
* force push,
* merge,
* rebase,
* branch deletion,
* PR/MR creation,
* tag,
* release.

Read-only Git inspection boleh dilakukan jika membantu memahami:

* branch,
* remote,
* history,
* convention,
* diff.

Jangan discard perubahan user yang sudah ada.

## VALIDATION WAJIB

Setelah alignment:

### 1. Inventory ulang

Inventaris seluruh:

```text
TARGET_RULES_DIR/**/*.md
```

Pastikan semua mutable file telah diperiksa.

### 2. File Status

Setiap mutable file harus memiliki salah satu status:

```text
UPDATED
CHECKED — NO CHANGE REQUIRED
PARTIALLY ALIGNED — UNKNOWN REMAINS
NOT CURRENTLY ACTIVE
```

### 3. Immutable Verification

Pastikan ketiga file berikut tidak memiliki perubahan yang dibuat oleh task alignment:

```text
chat-rules.md
human-language-english.md
human-language-indonesia.md
```

Jika Git tersedia:

periksa diff ketiganya.

Jika agent pada task ini secara tidak sengaja mengubah salah satu immutable file:

kembalikan hanya perubahan yang dibuat agent pada task ini jika dapat dilakukan tanpa menghapus perubahan user existing.

Jangan reset perubahan user.

### 4. Placeholder Check

Cari placeholder tersisa.

Untuk setiap placeholder:

tentukan apakah:

```text
INTENTIONALLY GENERIC
UNKNOWN
ERROR / MISSED ALIGNMENT
```

Jangan mengklaim alignment selesai jika placeholder yang seharusnya sudah dapat ditentukan masih tertinggal.

### 5. Generic Assumption Check

Cari statement generic yang sudah tidak sesuai walaupun tidak berbentuk placeholder.

Contoh:

```text
gunakan npm
```

padahal project hanya menggunakan pnpm.

```text
branch main
```

padahal default branch berbeda.

```text
REST controller
```

padahal backend menggunakan gRPC.

```text
Next.js
```

padahal frontend Vue.

Ini termasuk alignment.

### 6. Command Check

Pastikan command project-specific yang ditulis memang tersedia.

Periksa:

* package scripts,
* Makefile,
* task runner,
* CI,
* tooling config.

### 7. Path Check

Pastikan path yang ditulis benar terhadap repository aktual.

Jangan menyimpan path lama dari template source.

### 8. Reference Check

Pastikan links/reference antar-rule masih valid setelah folder ditempatkan di TARGET_RULES_DIR.

### 9. Wiring Check

Pastikan:

* persistent rule benar,
* scoped rule benar,
* manual rule benar,
* inactive rule tidak dimuat tanpa kebutuhan,
* entrypoint agent sesuai environment.

### 10. Diff Check

Periksa diff.

Pastikan:

* hanya perubahan yang relevan,
* tidak ada source code berubah,
* tidak ada immutable file berubah,
* tidak ada secret,
* tidak ada formatting massal tanpa kebutuhan.

## MARKDOWN LINT

Jika repository memiliki Markdown lint/check:

jalankan jika masuk akal dan murah.

Jangan install tooling baru hanya untuk alignment jika project tidak memilikinya.

Jangan menjalankan full application test suite hanya karena Markdown berubah kecuali project instruction mewajibkannya.

## STOP CONDITIONS

Minta klarifikasi hanya jika:

* TARGET_RULES_DIR tidak diketahui,
* repository yang dimaksud tidak jelas,
* dua kemungkinan project menghasilkan alignment berbeda secara material,
* atau keputusan yang diperlukan tidak dapat dibuktikan dari repository.

Jangan bertanya hanya karena ada satu UNKNOWN yang tidak menghalangi pekerjaan lain.

Selesaikan bagian yang dapat dipastikan terlebih dahulu.

## OUTPUT AKHIR

Setelah melakukan perubahan, berikan laporan ringkas.

### PROJECT PROFILE

Tampilkan yang dapat dibuktikan:

```text
Project:
Repository type:
Workspace / monorepo:
Language / runtime:
Frontend:
Backend:
Database / persistence:
Package manager:
Build:
Test:
Lint:
Typecheck:
Deployment:
Default/base branch:
External integrations:
```

Hilangkan field yang benar-benar tidak relevan.

Gunakan `UNKNOWN` jika penting tetapi belum dapat dipastikan.

### ALIGNMENT MATRIX

Tampilkan SEMUA mutable Markdown file dalam TARGET_RULES_DIR.

Format:

| File | Status | Alignment |
| ---- | ------ | --------- |

Status hanya:

```text
UPDATED
CHECKED — NO CHANGE REQUIRED
PARTIALLY ALIGNED — UNKNOWN REMAINS
NOT CURRENTLY ACTIVE
```

Jangan menghilangkan file mutable dari matrix.

### IMMUTABLE FILE CHECK

Wajib tampilkan:

```text
chat-rules.md — UNCHANGED
human-language-english.md — UNCHANGED
human-language-indonesia.md — UNCHANGED
```

Jika salah satu tidak `UNCHANGED` karena perubahan yang dibuat task ini:

alignment belum selesai.

### PLACEHOLDER / UNKNOWN

Tampilkan hanya yang masih relevan.

Format:

| File | Item | Status | Reason |
| ---- | ---- | ------ | ------ |

### AI AGENT WIRING

Ringkas:

```text
Detected/targeted agents:
Entrypoints:
Persistent rules:
Scoped rules:
Task-dependent rules:
Manual rules:
Inactive rules:
```

### CONFLICT

Tampilkan hanya conflict nyata seperti:

* template vs implementation,
* docs vs repository,
* instruction vs instruction,
* user constraint vs existing project behavior.

Jika tidak ada:

```text
Tidak ada conflict material yang ditemukan.
```

### VALIDATION

Ringkas:

* inventory checked,
* placeholder checked,
* paths checked,
* commands checked,
* references checked,
* agent wiring checked,
* immutable files checked,
* diff checked,
* secret check,
* outside-scope changes.

## COMPLETION CONDITION

Alignment dianggap selesai hanya jika:

1. TARGET_RULES_DIR sudah teridentifikasi.

2. Seluruh Markdown file mutable di dalamnya telah diperiksa.

3. Semua project-dependent information yang dapat dibuktikan sudah diselaraskan.

4. UNKNOWN tidak dikarang.

5. Rule activation sesuai project.

6. Agent wiring sesuai environment.

7. Command dan path yang ditulis valid.

8. Tidak ada source code aplikasi yang berubah.

9. Tidak ada secret yang dimasukkan.

10. Ketiga immutable file tidak berubah:

```text
chat-rules.md
human-language-english.md
human-language-indonesia.md
```

11. Diff sudah diperiksa.

12. Alignment matrix mencakup seluruh mutable Markdown file.

## PRINSIP AKHIR

Folder target berasal dari user.

Jangan hardcode nama folder template.

Inventaris file secara dinamis.

Periksa semua Markdown secara recursive.

Semua Markdown mutable wajib diperiksa.

Tidak semua file wajib menghasilkan diff.

Jangan membuat dummy edit.

Repository aktual adalah source of truth untuk current implementation.

Pertahankan generic principle yang memang harus tetap portable.

Sesuaikan project fact dan project constraint.

Jangan mengarang stack.

Jangan mengarang workflow.

Jangan mengarang branch.

Jangan mengarang command.

Jangan mengarang integration.

Jangan membuat satu wiring universal untuk semua coding agent.

Jangan membuat semua rules selalu aktif.

Jangan menghapus template hanya karena subsystem belum digunakan.

Gunakan `NOT CURRENTLY ACTIVE` jika lebih tepat.

Jangan mengubah:

`chat-rules.md`

`human-language-english.md`

`human-language-indonesia.md`

dalam kondisi apa pun selama alignment.

Tujuan akhir adalah membuat paket Markdown benar-benar memahami project tempat paket tersebut ditempatkan tanpa kehilangan sifat dinamis, modular, dan reusable dari rules itu sendiri.
