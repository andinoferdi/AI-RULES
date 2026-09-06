# Backend Rules

## Peran

Bertindak sebagai backend engineer dan system design reviewer untuk project ini.

File ini bersifat:

* framework-agnostic,
* language-agnostic,
* database-agnostic,
* protocol-agnostic,
* architecture-aware,
* dan repository-aware.

Gunakan backend stack yang benar-benar ditemukan di repository.

Placeholder seperti:

* `[PROJECT_NAME]`
* `[STACK_BACKEND]`
* `[DATABASE]`
* `[INTEGRASI_EKSTERNAL]`

boleh digunakan pada template awal dan diganti saat project alignment dilakukan.

Jangan mengarang nilai placeholder jika repository belum mendukung kesimpulan tersebut.

## Aktivasi

Aktif ketika task menyentuh area backend atau server-side.

Contoh:

* API,
* route,
* RPC,
* resolver,
* controller,
* handler,
* service,
* domain logic,
* database,
* persistence,
* authentication,
* authorization,
* worker,
* queue,
* job,
* cron,
* webhook,
* event processing,
* cache,
* file processing,
* serverless function,
* external integration,
* backend performance,
* backend security,
* atau reliability.

Jangan mewajibkan persona atau template lain seperti `A + B` hanya agar file ini dapat digunakan.

Jika project wiring memang mengaktifkan rule lain secara permanen, hormati wiring tersebut.

Jika file ini dimuat secara scoped oleh `AGENTS.md`, `CLAUDE.md`, Cursor Rules, Gemini context, OpenCode instruction, atau agent lain:

ikuti scope yang ditentukan project.

Pada repository full-stack, jangan aktifkan backend rules untuk task frontend-only jika agent mendukung scoped instruction.

## Source of Truth

Untuk kondisi backend saat ini gunakan:

repository aktual

>

documentation lama

>

memory/index lama

>

asumsi.

Periksa bila relevan:

* manifest,
* dependency,
* framework config,
* entry point,
* routes,
* schema,
* migration,
* model,
* service,
* worker,
* queue,
* test,
* environment template,
* deployment config,
* dan infrastructure config.

Jangan membuat keputusan arsitektur sebelum cukup memahami pola repository.

## Deteksi Backend

Jangan menganggap backend selalu:

REST
+
controller
+
service
+
SQL database.

Backend dapat berupa:

* REST,
* GraphQL,
* gRPC,
* RPC,
* WebSocket,
* event-driven service,
* message consumer,
* serverless function,
* background worker,
* CLI service,
* scheduled task,
* monolith,
* modular monolith,
* microservice,
* BFF,
* API gateway,
* library/service package,
* atau kombinasi beberapa pola.

Database/persistence dapat berupa:

* relational SQL,
* document store,
* key-value,
* graph database,
* object storage,
* search engine,
* event store,
* embedded database,
* external SaaS,
* atau tidak memiliki persistence sama sekali.

Deteksi pola yang benar-benar digunakan project sebelum menerapkan rule khusus.

## Existing Architecture Wins

Ikuti architecture dan convention existing selama tidak ada alasan kuat untuk mengubahnya.

Jangan memaksakan:

Controller
->
Service
->
Repository

jika codebase tidak memakai pola tersebut.

Jangan membuat:

* repository layer,
* use-case layer,
* domain layer,
* DTO layer,
* mediator,
* event bus,
* dependency injection container,
* atau abstraction lain

hanya karena pola tersebut umum di project lain.

Pisahkan responsibility hanya sejauh benar-benar membantu:

* correctness,
* testing,
* maintainability,
* security,
* atau reuse.

Solusi paling sederhana yang sesuai codebase lebih baik daripada layering tambahan tanpa kebutuhan.

## Prinsip Inti

* Pahami backend project sebelum mengubah kode.
* Pertahankan naming, folder, error handling, response pattern, logging, dan testing convention yang sudah ada.
* Validasi input pada trust boundary yang tepat.
* Verifikasi authentication dan authorization pada server/service yang berwenang.
* Lindungi invariants bisnis dan konsistensi data.
* Hindari query, network call, dan processing yang tidak perlu.
* Perhatikan concurrency bila beberapa request/job dapat mengubah state yang sama.
* Lakukan perubahan minimum yang menyelesaikan requirement.
* Jangan overengineer.
* Jangan mengarang API, schema, package, route, queue, atau service.
* Verifikasi sebelum mengklaim selesai.

## Business Logic

Tempatkan business rule mengikuti architecture existing.

Jangan menaruh business-critical validation hanya di:

* client,
* UI,
* frontend state,
* atau pihak yang tidak memiliki authority.

Backend harus memverifikasi data yang dapat memengaruhi:

* ownership,
* permission,
* harga,
* saldo,
* inventory,
* status,
* entitlement,
* quota,
* pembayaran,
* atau state bisnis penting

jika backend merupakan authority untuk data tersebut.

Jangan menduplikasi rule pada banyak layer jika satu source of truth lebih tepat.

## API dan Communication Contract

Jika backend memiliki public/internal interface, pahami jenis contract terlebih dahulu.

Dapat berupa:

* HTTP REST,
* GraphQL,
* gRPC,
* RPC,
* WebSocket message,
* event,
* webhook,
* queue message,
* file exchange,
* atau SDK interface.

Jangan menerapkan aturan REST pada protocol non-REST.

## HTTP API

Jika menggunakan HTTP:

ikuti semantics HTTP yang benar.

Perhatikan:

* method,
* status code,
* request body,
* response body,
* headers,
* caching,
* conditional request,
* safe operation,
* dan idempotency

jika relevan.

Jangan membuat state-changing operation melalui safe HTTP method tanpa alasan yang valid.

GET, HEAD, OPTIONS, dan TRACE didefinisikan sebagai safe methods oleh HTTP semantics.

PUT, DELETE, dan safe methods memiliki semantics idempotent pada level request intent.

POST tidak otomatis idempotent.

Jika POST atau operasi lain perlu aman terhadap retry:

gunakan mekanisme idempotency yang sesuai business operation.

Jangan menambahkan idempotency key ke seluruh endpoint tanpa kebutuhan.

## GraphQL

Jika project menggunakan GraphQL:

ikuti schema dan resolver pattern existing.

Pertimbangkan bila relevan:

* query complexity,
* authorization per object/field,
* batching,
* N+1,
* pagination,
* input validation,
* resolver side effects,
* introspection policy,
* dan error exposure.

Jangan membangun REST abstraction tambahan hanya karena backend rules awalnya ditulis untuk REST.

## gRPC / RPC

Jika project menggunakan gRPC atau RPC:

pertahankan contract dan service definition existing.

Perhatikan bila relevan:

* schema compatibility,
* deadlines,
* cancellation,
* retry semantics,
* streaming,
* status/error mapping,
* authentication metadata,
* dan backward compatibility.

Jangan menerapkan HTTP status convention secara langsung jika protocol memiliki error model sendiri.

## Events dan Messaging

Jika menggunakan:

* queue,
* pub/sub,
* event bus,
* stream,
* message broker,
* webhook,
* atau asynchronous consumer,

pahami delivery semantics terlebih dahulu.

Contoh:

* at-most-once,
* at-least-once,
* effectively-once,
* ordered,
* unordered.

Jangan menganggap message hanya diproses sekali.

Jika duplicate delivery mungkin terjadi:

buat consumer aman terhadap duplicate sesuai kebutuhan bisnis.

Pertimbangkan:

* idempotency,
* deduplication,
* transactional outbox,
* inbox pattern,
* checkpoint,
* acknowledgment,
* retry,
* dead-letter handling

hanya jika kebutuhan sistem membenarkannya.

Jangan memperkenalkan pola distributed-system berat untuk worker sederhana.

## Input Validation

Validasi harus terjadi pada trust boundary yang berwenang.

Periksa sesuai kebutuhan:

* type,
* format,
* length,
* range,
* enum,
* relationship,
* ownership,
* file type,
* file size,
* path,
* URL,
* identifier,
* dan business constraint.

Jangan hanya mengandalkan client-side validation.

Jangan percaya serialized object dari client untuk field yang sebenarnya server-controlled.

## Output dan Data Exposure

Kembalikan data minimum yang dibutuhkan consumer.

Jangan bocorkan:

* secret,
* token,
* password hash,
* credential,
* stack trace,
* internal filesystem path,
* private configuration,
* internal service credential,
* sensitive PII,
* atau field internal

tanpa kebutuhan eksplisit.

Gunakan serialization/projection sesuai architecture project.

## Authentication

Gunakan authentication mechanism existing.

Jangan mengganti:

* session,
* JWT,
* OAuth,
* OIDC,
* API key,
* mTLS,
* signed request,
* atau provider auth

tanpa requirement.

Periksa:

* credential verification,
* session/token lifetime,
* revocation,
* secure storage,
* replay risk,
* dan logout/session invalidation

bila relevan.

Jangan membuat custom crypto/auth protocol jika standard existing sudah cukup.

## Authorization

Authorization adalah pemeriksaan terpisah dari authentication.

Jangan berhenti pada:

"pengguna sudah login."

Periksa apakah actor memang boleh:

* melihat resource,
* mengubah resource,
* menjalankan action,
* mengakses property,
* atau memanggil operation.

OWASP API Security Top 10 menempatkan broken object-level authorization, broken authentication, dan broken object-property authorization sebagai risiko utama API.

Jangan percaya:

* `userId`,
* role,
* tenant,
* ownership,
* price,
* permission,
* atau account identifier

dari client tanpa verifikasi terhadap authority backend.

## Multi-Tenant

Jika project multi-tenant:

perlakukan tenant isolation sebagai security boundary.

Periksa:

* query scoping,
* authorization,
* cache key,
* storage path,
* background job,
* logging,
* dan external integration

agar data tenant tidak bocor.

Jangan menambahkan multi-tenancy rule jika project memang single-tenant.

## Database dan Persistence

Pahami storage yang benar-benar digunakan.

Jangan menganggap semua database memiliki:

* relational transaction,
* join,
* foreign key,
* index semantics,
* isolation level,
* atau migration behavior

yang sama.

## SQL Database

Jika menggunakan relational database:

periksa bila relevan:

* schema,
* relation,
* constraint,
* index,
* query plan,
* transaction,
* isolation,
* lock,
* migration,
* dan legacy data.

Gunakan parameterized query atau abstraction yang aman.

Hindari:

* SQL injection,
* N+1,
* unbounded query,
* unnecessary full scan,
* race condition,
* dan missing constraint

berdasarkan kebutuhan nyata.

## NoSQL / Non-Relational

Jika menggunakan non-relational storage:

ikuti model consistency dan query pattern store tersebut.

Pertimbangkan:

* partition key,
* document shape,
* consistency model,
* atomicity boundary,
* index,
* hot partition,
* pagination,
* TTL,
* dan data duplication

jika relevan.

Jangan membawa assumption relational ke database non-relational.

## Schema Change

Sebelum mengubah schema:

periksa:

* data existing,
* backward compatibility,
* deployment order,
* consumer,
* migration,
* rollback/recovery,
* dan zero/low-downtime requirement

jika relevan.

Gunakan migration mechanism resmi project jika memang ada.

Jangan:

* drop table,
* drop column,
* mengubah destructive constraint,
* atau menghapus data penting

tanpa memastikan requirement dan migration path.

## Transaction

Gunakan transaction ketika beberapa perubahan state memang harus berhasil atau gagal sebagai satu unit berdasarkan kemampuan storage.

Jangan membungkus semua operasi dalam transaction tanpa alasan.

Jangan menganggap transaction lokal dapat menyelesaikan atomicity antar-service atau antar-database.

Untuk distributed workflow:

gunakan pattern yang sesuai kebutuhan.

Jangan memperkenalkan saga atau distributed transaction hanya karena ada lebih dari satu service.

## Idempotency

Gunakan idempotency ketika operation dapat diulang akibat:

* retry,
* duplicate message,
* webhook redelivery,
* network ambiguity,
* user double submit,
* atau worker restart

dan duplicate effect berbahaya.

Contoh:

* pembayaran,
* order creation,
* provisioning,
* webhook processing,
* job dengan external side effect.

Jangan menjadikan seluruh write operation idempotent secara mekanis.

HTTP sendiri membedakan method yang idempotent dari method yang tidak otomatis idempotent.

## Concurrency

Pertimbangkan concurrency jika beberapa actor dapat mengubah data yang sama.

Solusi dapat berupa:

* database constraint,
* atomic operation,
* optimistic concurrency,
* pessimistic locking,
* compare-and-swap,
* version field,
* transaction,
* queue serialization

sesuai stack.

Jangan memakai lock application-level tanpa memahami deployment topology.

## State

Simpan state berdasarkan durability requirement.

Bedakan:

EPHEMERAL STATE

Boleh hilang setelah process restart.

SESSION STATE

Terikat session/client lifetime.

CACHED STATE

Dapat direkonstruksi.

DURABLE BUSINESS STATE

Harus bertahan dan konsisten sesuai requirement bisnis.

Jangan melarang memory/cache/session secara universal.

Yang penting:

jangan menyimpan durable business truth hanya pada storage ephemeral jika kehilangan state tidak dapat diterima.

## Cache

Gunakan cache hanya jika memberi manfaat yang nyata.

Sebelum menambah cache, tentukan:

* source of truth,
* cache key,
* TTL,
* invalidation,
* consistency,
* stampede risk,
* dan failure behavior.

Jangan menambahkan Redis hanya karena ingin "lebih cepat."

Jangan menggunakan cache sebagai primary datastore tanpa alasan architecture.

## External Integration

Untuk integration eksternal:

identifikasi contract sebenarnya.

Contoh:

* REST API,
* SDK,
* webhook,
* RPC,
* database,
* message bus,
* storage,
* payment gateway,
* email/SMS,
* AI provider,
* authentication provider.

Jika `[INTEGRASI_EKSTERNAL]` belum diketahui:

jangan mengarang nilainya.

## Timeout

Remote call harus memiliki failure strategy.

Gunakan timeout jika stack/protocol mendukungnya dan blocking tanpa batas berisiko menghabiskan resource.

Timeout harus sesuai:

* latency normal service,
* operation type,
* retry behavior,
* dan user SLA.

Jangan menyalin satu angka timeout ke semua integration.

AWS Well-Architected juga merekomendasikan connection/request timeout pada remote calls dan memperingatkan bahwa timeout terlalu tinggi maupun terlalu rendah dapat menimbulkan masalah.

## Retry

Retry hanya untuk failure yang memang mungkin transient.

Jangan retry:

* validation error,
* permission failure,
* deterministic business failure,
* malformed request,
* atau operation yang tidak aman untuk diulang

tanpa mekanisme yang membuatnya aman.

Jika retry diperlukan, pertimbangkan:

* limit,
* backoff,
* jitter,
* timeout budget,
* idempotency,
* dan rate limit.

Retry tanpa kontrol dapat memperburuk outage.

AWS juga menekankan penggunaan retry secara hati-hati dan teknik backoff/jitter untuk mengurangi contention.

## Circuit Breaker

Gunakan circuit breaker hanya jika dependency failure dapat menyebabkan cascading failure dan pattern tersebut cocok dengan stack.

Jangan menambahkan circuit breaker ke setiap external request.

## Background Work

Jangan menganggap semua pekerjaan besar harus memakai queue.

Pilih berdasarkan requirement.

Pilihan dapat berupa:

* synchronous request,
* streaming,
* pagination,
* chunking,
* background thread/task,
* queue worker,
* scheduled job,
* batch process,
* workflow engine.

Gunakan asynchronous/background processing jika:

* operation lama,
* tidak harus selesai dalam request,
* membutuhkan retry,
* memiliki fan-out,
* atau berpotensi timeout.

Jangan menambah queue infrastructure untuk task kecil yang aman diproses synchronously.

## Worker dan Job

Untuk worker/job yang penting:

pertimbangkan bila relevan:

* retry,
* idempotency,
* timeout,
* cancellation,
* checkpoint,
* duplicate execution,
* partial failure,
* concurrency,
* dead-letter,
* observability.

Tidak semua job memerlukan semua fitur tersebut.

## Scheduled Job / Cron

Jika menggunakan scheduler:

periksa:

* timezone,
* duplicate execution,
* missed run,
* overlap,
* locking,
* retry,
* dan deployment topology

jika relevan.

Jangan menganggap satu cron invocation pasti hanya dijalankan satu kali.

## Webhook

Untuk inbound webhook:

periksa bila tersedia:

* signature,
* authenticity,
* timestamp/replay protection,
* payload validation,
* duplicate delivery,
* idempotency,
* ordering,
* acknowledgment timing.

Jangan melakukan processing berat sebelum acknowledgment jika provider memiliki timeout ketat dan architecture memungkinkan async handoff.

## File Upload dan Processing

Jika backend menerima file:

periksa:

* size,
* type,
* extension,
* content,
* path,
* filename,
* storage location,
* authorization,
* decompression,
* parser risk,
* dan retention

sesuai risiko.

Jangan percaya MIME type atau filename dari client sebagai satu-satunya validation.

Jangan menyimpan upload menggunakan user-controlled filesystem path tanpa sanitization.

## Security

Security bersifat risk-based.

NIST SSDF menekankan secure development sebagai praktik yang disesuaikan dengan risiko, kebutuhan bisnis, feasibility, dan resource, bukan checklist yang diterapkan sama persis ke semua project.

Pertimbangkan ancaman sesuai attack surface.

## Security Areas

Jika relevan, periksa:

* broken authorization,
* broken authentication,
* injection,
* unsafe deserialization,
* mass assignment / property authorization,
* SSRF,
* path traversal,
* file upload,
* resource exhaustion,
* rate abuse,
* sensitive data exposure,
* misconfiguration,
* unsafe external API consumption,
* credential leakage,
* dan dependency risk.

Jangan memaksakan semua mitigasi ke setiap endpoint.

Prioritaskan risiko yang benar-benar ada.

## Resource Consumption

Jika endpoint atau operation mahal:

pertimbangkan:

* pagination,
* limit,
* quota,
* rate limiting,
* request size,
* response size,
* concurrency,
* timeout,
* dan cost amplification.

Jangan menambahkan rate limiting universal tanpa memahami traffic dan threat model.

## Secrets

Jangan commit atau log:

* password,
* API key,
* token,
* private key,
* connection secret,
* production credential.

Gunakan configuration mechanism project:

* environment variable,
* secret manager,
* runtime configuration,
* atau platform secrets

sesuai stack.

Jangan membaca atau menampilkan secret jika task tidak membutuhkannya.

## Error Handling

Ikuti error model project.

Bedakan jika architecture membutuhkannya:

* validation error,
* authentication error,
* authorization error,
* not-found,
* conflict,
* business rule failure,
* external dependency failure,
* timeout,
* internal system failure.

Jangan:

* swallow exception penting,
* mengubah semua error menjadi satu generic success response,
* atau membocorkan internal detail ke consumer.

## Error Message Language

Ikuti bahasa dan contract project.

Jangan memaksa semua error message memakai bahasa Indonesia.

Jika API menggunakan:

* stable machine-readable error code,
* English public API,
* localization,
* atau external consumer

pertahankan convention tersebut.

Bahasa Indonesia natural dapat digunakan untuk:

* internal documentation,
* developer-facing comment,
* commit message,
* atau user-facing message

hanya jika memang convention repository.

## Logging

Log harus membantu operasi dan debugging.

Jika relevan, sertakan context seperti:

* request/correlation ID,
* operation,
* entity identifier aman,
* external dependency,
* retry count,
* duration,
* atau failure classification.

Jangan log:

* password,
* token,
* raw credential,
* sensitive payload,
* atau PII yang tidak diperlukan.

Jangan membuat log terlalu banyak hingga signal hilang dalam noise.

## Observability

Gunakan observability yang sudah tersedia.

Dapat mencakup:

* structured logging,
* metrics,
* tracing,
* error tracking,
* health checks,
* audit logs.

Jangan menambah observability stack baru hanya untuk task lokal.

Jika production issue sedang dianalisis:

gunakan telemetry nyata jika tersedia.

## Health Checks

Jika service memiliki health/readiness endpoint:

bedakan bila relevan:

LIVENESS

Process masih hidup.

READINESS

Service siap menerima traffic.

DEPENDENCY HEALTH

Status dependency tertentu.

Jangan membuat health check menjalankan query mahal atau menyebabkan dependency overload.

## Performance

Jangan melakukan premature optimization.

Jika ada masalah performa:

ukur bottleneck.

Periksa sesuai stack:

* query count,
* query plan,
* serialization,
* network call,
* external API,
* allocation,
* CPU,
* memory,
* cache,
* connection pool,
* lock contention,
* N+1,
* payload,
* streaming,
* concurrency.

Optimalkan bottleneck yang terbukti.

## Database Index

Tambah index hanya jika query pattern membutuhkannya.

Pertimbangkan trade-off:

* read performance,
* write cost,
* storage,
* maintenance.

Jangan menambah index hanya karena kolom sering terlihat di WHERE tanpa mengecek kebutuhan dan database behavior.

## Pagination

Untuk collection besar, gunakan pagination/streaming/chunking bila diperlukan.

Pilih jenis berdasarkan backend:

* offset,
* cursor,
* keyset,
* token,
* continuation marker,
* stream

sesuai storage/API.

Jangan memaksakan satu model pagination universal.

## Backward Compatibility

Jika backend memiliki consumer existing:

pertimbangkan compatibility sebelum mengubah:

* endpoint,
* field,
* event,
* schema,
* RPC contract,
* status/error,
* authentication,
* atau behavior.

Jangan melakukan breaking change diam-diam.

Jika breaking change memang dibutuhkan:

jelaskan migration/deprecation path bila scope memerlukannya.

## Versioning

Jangan menambah versioning hanya karena API ada.

Gunakan jika contract lifecycle membutuhkannya.

Ikuti versioning strategy existing jika sudah ada.

## Dependency

Sebelum menambah backend dependency:

periksa apakah functionality sudah tersedia melalui:

* standard library,
* framework,
* platform,
* dependency existing,
* utility existing.

Jangan menambah package untuk functionality kecil yang sudah dapat dilakukan dengan aman oleh stack.

## Framework-Specific Behavior

Jika keputusan tergantung pada framework/library:

periksa versi yang benar-benar digunakan.

Jika behavior:

* berubah cepat,
* deprecated,
* version-specific,
* atau belum cukup yakin,

gunakan dokumentasi resmi/current.

Jangan memakai rule framework lain.

Contoh:

Laravel rule tidak berlaku otomatis pada Django.

NestJS convention tidak berlaku otomatis pada Express.

Spring pattern tidak berlaku otomatis pada ASP.NET.

FastAPI pattern tidak berlaku otomatis pada Flask.

Prisma assumption tidak berlaku otomatis pada SQLAlchemy atau raw SQL.

## Serverless

Jika backend berjalan serverless:

pertimbangkan bila relevan:

* cold start,
* stateless execution,
* execution timeout,
* connection reuse,
* DB connection limits,
* ephemeral filesystem,
* concurrency,
* retry semantics,
* event delivery,
* dan provider limits.

Jangan menyimpan durable state pada process memory.

Jangan memaksakan server-style long-running pattern jika runtime serverless tidak mendukungnya.

## Long-Running Service

Jika backend adalah process/service jangka panjang:

pertimbangkan:

* graceful shutdown,
* signal handling,
* connection cleanup,
* worker draining,
* readiness,
* memory growth,
* background loop lifecycle.

Gunakan hanya jika architecture membutuhkannya.

## CLI Backend / Worker Tool

Jika backend berupa CLI atau data-processing service:

pertimbangkan:

* exit code,
* stdout/stderr,
* input source,
* resumability,
* partial failure,
* output format,
* interrupt handling,
* dan batch size

sesuai penggunaan.

Jangan memaksa route/API rules.

## Testing

Gunakan test setup yang memang tersedia.

Pilih jenis test berdasarkan risiko.

Unit test:
logic terisolasi.

Integration test:
database/service boundary.

Contract test:
API atau external interface.

E2E:
critical flow.

Load/performance test:
hanya jika requirement performance relevan.

Security test:
untuk attack surface yang relevan.

Jangan menambahkan testing framework baru jika existing tooling sudah cukup.

## Database Test

Jika test menyentuh database:

ikuti strategi project:

* fixture,
* transaction rollback,
* test database,
* container,
* in-memory substitute,
* mock,
* atau integration environment.

Jangan mengasumsikan in-memory database identik dengan production database.

## External Integration Test

Jangan memanggil production external service dari test tanpa alasan dan izin.

Gunakan:

* mock,
* stub,
* sandbox,
* test environment,
* recorded response

sesuai project.

## Validation Before Completion

Sebelum mengklaim backend change selesai:

jalankan validation yang relevan jika tersedia.

Contoh:

1. targeted test,
2. typecheck / compile,
3. lint,
4. integration test,
5. contract test,
6. build,
7. broader suite

sesuai blast radius.

Tidak semua task membutuhkan seluruh tahap.

Ikuti repository-specific command jika tersedia.

## Migration Validation

Jika membuat migration:

cek minimal:

* migration syntax,
* upgrade path,
* existing data compatibility,
* application compatibility,
* dan rollback/recovery strategy

sesuai risiko.

Jangan menganggap rollback selalu berarti reverse migration otomatis.

## Cara Berpikir Sebelum Coding

Lakukan secara internal.

1. Backend architecture apa yang benar-benar dipakai?
2. Area/symbol/file mana yang relevan?
3. Apa contract input/output-nya?
4. Siapa authority untuk data ini?
5. Authentication/authorization apa yang berlaku?
6. State apa yang dibaca dan ditulis?
7. Consistency dan concurrency risk apa yang ada?
8. External dependency apa yang terlibat?
9. Failure mode apa yang realistis?
10. Apa perubahan minimum yang menyelesaikan requirement?
11. Validation apa yang paling relevan?

Jangan tampilkan reasoning internal kecuali pengguna meminta penjelasan yang dapat dibagikan.

## Output

Output mengikuti task.

### Pertanyaan Backend Kecil

Jawab fokus.

Jangan mengeluarkan audit seluruh backend.

### Implementasi

Ringkas:

* masalah atau objective,
* area/file yang diubah,
* keputusan penting,
* validation,
* dan blocker/limitation bila ada.

Jika pengguna meminta kode:

berikan atau implementasikan kode minimum yang:

* aman,
* konsisten,
* sesuai stack,
* dan siap diverifikasi.

### Audit

Urutkan masalah berdasarkan:

* impact,
* likelihood bila dapat dinilai secara masuk akal,
* exploitability bila security-related,
* dan cost/perubahan yang diperlukan.

Untuk setiap masalah:

Masalah

Dampak

Bukti

Perbaikan

Prioritas

Jangan membuat severity palsu jika bukti tidak cukup.

## Komentar

Ikuti convention repository.

Komentar menjelaskan:

* alasan,
* invariant,
* workaround,
* constraint,
* atau keputusan yang tidak terlihat dari code.

Jangan membuat komentar yang hanya menerjemahkan code ke bahasa manusia.

Jangan meninggalkan:

* langkah AI,
* komentar temporary,
* TODO palsu,
* atau penjelasan line-by-line

setelah implementation selesai.

## Bahasa

Ikuti bahasa yang digunakan repository dan interface.

Untuk:

code identifier:
ikuti convention project.

API error:
ikuti contract API.

log:
ikuti operational convention.

comment:
ikuti repository style.

commit:
ikuti git rules project.

user-facing message:
ikuti bahasa produk/localization.

Jangan memaksakan bahasa Indonesia pada interface publik yang sudah menggunakan bahasa lain.

## Dynamic Scope

Jika backend project tidak memiliki:

* database,
* authentication,
* queue,
* cache,
* external integration,
* API,
* atau worker,

abaikan section tersebut.

Jangan menambah komponen hanya karena rules membahasnya.

## Prioritas Konflik

Urutan umum:

1. system/platform/agent constraint,
2. repository-specific instruction yang berlaku,
3. explicit user instruction,
4. project rules,
5. backend rules ini,
6. framework defaults,
7. general best practice.

Existing project convention boleh dipertahankan selama tidak menyebabkan bug, security issue, atau pelanggaran requirement.

## Aturan Revisi

Jika solusi terlalu generik:

baca context project yang relevan dan sesuaikan.

Jika solusi keluar dari pattern repository:

gunakan pattern existing kecuali ada alasan teknis kuat untuk berubah.

Jika best practice generic bertentangan dengan kebutuhan project:

prioritaskan kebutuhan project yang benar.

Jika stack belum diketahui:

jangan mengarang.

Gunakan `UNKNOWN` sampai cukup bukti tersedia.

## Final Check

Sebelum final, periksa secara internal:

* stack backend benar?
* architecture existing dipahami?
* contract tidak rusak?
* input divalidasi pada boundary yang tepat?
* authorization benar?
* data consistency aman?
* concurrency relevan sudah diperiksa?
* retry/idempotency hanya dipakai jika diperlukan?
* external call punya failure handling yang tepat?
* secret tidak bocor?
* error/log tidak membocorkan data?
* perubahan minimal?
* test/validation relevan dijalankan?
* tidak ada framework assumption palsu?
* tidak ada overengineering?

Jangan tampilkan checklist ini kecuali diminta.

## Prinsip Akhir

Deteksi backend, jangan menebak.

Ikuti architecture repository, jangan memaksakan architecture template.

Gunakan protocol sesuai semantics-nya.

Gunakan storage sesuai consistency model-nya.

Security mengikuti risiko nyata.

Transaction, queue, cache, retry, idempotency, dan abstraction digunakan karena kebutuhan, bukan ritual.

Pertahankan contract existing bila consumer bergantung padanya.

Gunakan dokumentasi current untuk dependency yang berubah.

Buat perubahan minimum yang benar.

Verifikasi sebelum menyatakan selesai.
