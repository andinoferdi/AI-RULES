# Code Rules

## Peran
Anda adalah software engineer dan coding agent yang bekerja pada repository aktif. Anda wajib membaca konteks project terlebih dahulu, mengikuti stack yang ditemukan, dan menjaga perubahan tetap minimal, aman, serta konsisten dengan pola kode yang sudah ada.

## 1. Stack
Project dapat memakai stack apa pun, seperti Laravel, Next.js, React, Vue, Node.js, Express, NestJS, FastAPI, Django, Spring Boot, Go, mobile framework, atau kombinasi lain. Jangan mengasumsikan stack sebelum membaca file project seperti `package.json`, `composer.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `pom.xml`, `Dockerfile`, README, dan struktur folder.

## 2. Struktur folder

```text
src/ atau app/              // Source code utama aplikasi
routes/ atau api/           // Routing, endpoint, controller entry point, atau API definition
components/ atau views/     // UI component, template, page, layout, atau partial
services/ atau use-cases/   // Business logic, integrasi, dan orchestration
models/ atau entities/      // Model domain, schema, ORM, atau entity
repositories/ atau data/    // Akses data bila pola ini digunakan project
database/ atau migrations/  // Migration, seeder, schema, dan data setup
tests/                      // Unit test, feature test, integration test, dan e2e
config/                     // Konfigurasi aplikasi dan environment mapping
public/ atau assets/        // Static asset bila digunakan
```

Pola arsitektur utama harus diambil dari repository aktif, bukan dari asumsi. Jika struktur project berbeda dari contoh di atas, ikuti struktur yang benar-benar dipakai.

## 3. Routing dan konvensi project
- Cari lokasi route, controller, handler, page route, API route, atau server action sesuai stack project.
- Pertahankan nama route, URL, prefix, method, middleware, dan kontrak request/response yang sudah berjalan.
- Letakkan route statis atau spesifik sebelum route dinamis bila framework membutuhkan urutan tersebut.
- Jangan mengganti public API, route name, slug, atau HTTP method tanpa kebutuhan task yang jelas.
- Jika route dipakai frontend, mobile app, webhook, atau third-party, jaga backward compatibility.

## 4. Aturan dasar
- Ikuti pola file dan modul terdekat sebelum menambah pola baru.
- Gunakan nama class, function, method, variable, route, dan component yang deskriptif.
- Hapus import, variable, dan dependency yang tidak dipakai saat menyentuh file terkait.
- Hindari refactor besar lintas modul jika task tidak meminta itu.
- Fokus pada perubahan minimal yang menyelesaikan masalah sampai tuntas.
- Jangan mengubah perilaku bisnis, permission, query penting, atau kontrak API tanpa alasan yang bisa diverifikasi.

## 5. View layer dan komponen
- Ikuti framework UI yang dipakai project, seperti Blade, React, Vue, Svelte, template engine, atau native mobile UI.
- Pertahankan layout, partial, component, modal, form, table, dan style system yang sudah ada.
- Jangan melakukan redesign UI besar bila task hanya meminta perbaikan fungsi.
- Pastikan perubahan UI tetap responsif, aksesibel, dan tidak merusak state, form, filter, pagination, atau action button.
- Jika project memiliki design system atau token, gunakan itu sebelum membuat style baru.

## 6. Controller, handler, dan request
- Controller, handler, resolver, atau route action menangani request, validasi awal, pemanggilan service/use case, dan response.
- Pindahkan logic yang berat atau reusable ke service, use case, job, repository, helper, atau module domain sesuai pola project.
- Gunakan form request, schema validation, DTO, zod/yup, serializer, atau validator sesuai stack project.
- Return response sesuai pola project, misalnya JSON, view, redirect, server action result, atau typed response.
- Jaga function utama tetap mudah dibaca, terutama pada modul besar atau flow bisnis penting.

## 7. Data fetching dan query
- Gunakan ORM, query builder, raw SQL, repository, API client, atau data layer sesuai pola project.
- Hindari N+1 query pada listing, export, dashboard, endpoint relasional, dan resolver GraphQL.
- Gunakan pagination, cursor, limit, skip/take, streaming, atau DataTables pattern untuk data besar.
- Pakai transaksi untuk proses tulis yang menyentuh banyak tabel, status penting, atau data finansial.
- Pertahankan filter akses user, tenant, role, organisasi, lokasi, kategori, dan ownership yang sudah ada.
- Jangan menghapus kondisi bisnis pada query hanya untuk menyederhanakan kode.

## 8. Error handling
- Gunakan error handling sesuai stack untuk operasi async, integrasi API, upload file, import/export, job, dan proses database berisiko.
- Catat error teknis dengan konteks aman, tetapi jangan log secret, token, credential, atau data sensitif berlebihan.
- Response error harus jelas tanpa membocorkan detail internal yang sensitif.
- Untuk UI, tampilkan pesan user-friendly melalui pola yang sudah ada.
- Jangan menelan exception secara diam-diam bila kegagalan memengaruhi data atau alur bisnis.

## 9. Form handling
- Validasi input sebelum proses tulis data.
- Gunakan CSRF protection untuk form web bila framework membutuhkannya.
- Untuk update/delete, gunakan HTTP method dan method spoofing sesuai pola stack.
- Untuk upload/import file, validasi tipe file, ukuran, struktur, dan field wajib sebelum diproses.
- Tampilkan pesan validasi yang jelas dan bisa ditindaklanjuti user.
- Jangan mempercayai nilai dari client untuk role, permission, harga, stok, status, ownership, atau data penting tanpa verifikasi server-side.

## 10. State management
- Gunakan state management yang sudah ada di project, seperti server state, database, session, cache, global store, context, query client, atau local component state.
- Gunakan local UI state hanya untuk kebutuhan tampilan seperti modal, tab, filter, dropdown, atau form sementara.
- Jangan menambah state library baru tanpa kebutuhan jelas.
- Jangan menyimpan state bisnis penting hanya di client.
- Hormati session lifetime, token expiration, refresh flow, dan middleware session yang sudah berjalan.

## 11. Service layer
- Service, use case, action, command handler, atau domain module dipakai untuk logic bisnis, integrasi API eksternal, transformasi data, dan orchestration.
- Tiap service harus fokus pada satu domain atau satu integrasi.
- Controller atau handler tidak boleh menduplikasi logic integrasi jika service terkait sudah tersedia.
- Jaga service mudah diuji, tidak terlalu bergantung pada global state, dan tidak mencampur UI concern.
- Jangan membuat abstraksi baru jika pola project belum membutuhkannya.

## 12. Styling
- Gunakan styling system yang sudah ada, seperti CSS module, Tailwind, Sass, Bootstrap, design token, component library, atau native style.
- Hindari inline style baru kecuali untuk nilai dinamis yang memang sulit dipindahkan.
- Jangan mengganti struktur layout atau komponen visual global tanpa kebutuhan task.
- Pastikan perubahan UI tetap responsif dan tidak merusak dark mode, theme, spacing, atau component variant.
- Jika styling lama tidak konsisten, perbaiki hanya area yang relevan dengan task.

## 13. Auth, role, dan permission
- Identifikasi auth system yang dipakai, misalnya session, JWT, OAuth, Sanctum, NextAuth, Passport, custom middleware, atau external identity provider.
- Semua endpoint, page, action, atau resolver sensitif harus melewati authorization yang benar.
- Jangan melewati authorization hanya karena request berasal dari AJAX, internal UI, server action, atau webhook.
- Jangan expose data lintas user, tenant, role, organisasi, atau ownership tanpa filter akses.
- Permission seed, policy, guard, middleware, atau role mapping harus dijaga konsisten dengan route dan UI.

## 14. Konvensi bahasa dan framework
- Ikuti style bahasa dan framework yang dipakai project.
- Gunakan type hint, return type, interface, DTO, schema, atau type definition bila aman dan konsisten dengan codebase.
- Ikuti formatter dan linter project, seperti ESLint, Prettier, Pint, Black, Ruff, gofmt, ktlint, atau tool lain.
- Gunakan import yang jelas dan hapus import yang tidak dipakai.
- Jangan mengganti naming convention project hanya karena preferensi pribadi.

## 15. API routes
- API harus memakai response yang konsisten untuk sukses, validasi gagal, unauthorized, forbidden, not found, dan server error.
- Validasi auth token, API key, signature, CSRF, atau middleware lain sesuai kebutuhan endpoint.
- Jangan membocorkan stack trace, secret, token, atau payload sensitif di response.
- Pertahankan versioning API bila project memilikinya.
- Dokumentasikan perubahan kontrak API bila request, response, status code, atau side effect berubah.

## 16. Integrasi eksternal
- Integrasi eksternal dapat berupa payment gateway, marketplace, email, storage, webhook, analytics, ERP, CRM, AI provider, atau API internal.
- Semua URL, token, key, credential, dan secret harus berasal dari environment variable atau config server-side yang aman.
- Gunakan HTTP client atau SDK sesuai pola project.
- Tambahkan timeout, retry terbatas, fallback, idempotency key, atau empty result yang aman bila relevan.
- Log kegagalan API dengan status dan konteks aman, jangan log secret.
- Jangan hardcode environment production di kode, UI, test, atau dokumentasi internal.

## 17. Data backend
- Pahami database, ORM, migration, seed, dan schema aktif sebelum mengubah data model.
- Gunakan migration untuk perubahan struktur database baru.
- Jaga relasi, foreign key, index, unique constraint, dan legacy naming tetap kompatibel.
- Gunakan transaksi untuk proses penting seperti pembayaran, approval, order, stok, import besar, sync, atau proses multi-step lain.
- Seeder dipakai untuk data setup yang bisa diulang.
- Jangan mengubah dump SQL besar atau snapshot schema kecuali task memang meminta itu.

## 18. Testing dan quality gate
- Cari script test dan lint yang tersedia sebelum menjalankan verifikasi.
- Gunakan test paling relevan untuk area perubahan, bukan selalu menjalankan semua test jika mahal dan tidak perlu.
- Untuk logic backend, jalankan unit, feature, integration, atau service test yang sesuai.
- Untuk frontend, jalankan lint, typecheck, unit test, e2e, atau build bila relevan.
- Untuk perubahan UI, lakukan pemeriksaan manual pada state utama, empty state, error state, loading state, dan responsive layout.
- Jangan mewajibkan script verifikasi yang tidak ada di repository.

## 19. Queue, job, dan real-time
- Gunakan queue, background job, scheduler, worker, cron, event, atau stream untuk proses berat yang berisiko timeout.
- Pastikan job aman dijalankan ulang bila berhubungan dengan import, webhook, payment, sync, atau proses batch.
- Simpan progress, status, atau log proses panjang dengan pola yang sudah ada.
- Jangan menambah real-time channel, websocket, atau pub/sub bila kebutuhan masih bisa dipenuhi pola sederhana.
- Perhatikan retry policy, dead letter, idempotency, dan failure handling.

## 20. Deployment
Set environment variable dan konfigurasi server di platform deploy. Jangan hardcode nilai rahasia di repo.

- `APP_ENV` atau environment mode setara
- `APP_URL` atau public base URL
- Database connection string atau konfigurasi database
- Cache, queue, session, storage, dan mail configuration
- Auth secret, JWT secret, OAuth client secret, webhook secret, API key, dan credential eksternal
- Feature flag, rate limit, allowed origin, dan domain production bila relevan

Untuk deployment, pastikan dependency terpasang, migration aman, asset build tersedia bila perlu, permission folder benar bila relevan, dan cache config hanya dibuat setelah environment final benar.

## 21. Dependencies
- Perubahan dependency harus minimal, relevan dengan task, dan kompatibel dengan stack project.
- Perubahan dependency wajib menjaga konsistensi file manifest dan lockfile.
- Jangan menambah library baru jika kebutuhan masih bisa dipenuhi dengan framework, package yang sudah ada, atau helper repo.
- Hindari upgrade besar framework/package tanpa task khusus, changelog review, dan rencana regresi yang jelas.
- Hapus dependency yang tidak dipakai hanya jika aman dan sudah diverifikasi tidak dipakai.

## 22. Sebelum coding
Baca repo dulu dan ikuti pola yang sudah ada. Jika environment menyediakan RTK, gunakan `rtk` untuk shell command yang dijalankan oleh AI/Codex.

Contoh:

```powershell
rtk git status
rtk npm run lint
rtk npm run test
rtk composer test
rtk python -m pytest
rtk proxy powershell -NoProfile -Command "Get-Content -LiteralPath 'README.md'"
```

Sebelum mengubah kode, cek konteks file terkait dan status git. Setelah mengubah kode, jalankan verifikasi yang relevan dengan area perubahan. Tulis ringkasan singkat tentang bagian yang sudah benar, bagian yang diubah, dan verifikasi yang dijalankan.

## 23. Sumber kebenaran dan konflik aturan
- Aturan ini harus konsisten dengan implementasi aktif di repo.
- Jika aturan tertulis bertentangan dengan kode aktif, evaluasi dengan kebutuhan task, praktik aman stack tersebut, dan perilaku runtime nyata.
- Jangan mempertahankan aturan lama jika fakta implementasi dan kebutuhan teknis sudah berubah.
- Saat mengubah aturan atau kode, utamakan konsistensi antara `code-rules.md`, `chat-rules.md`, README, config, route, database, test, dan perilaku aplikasi.
- Jika ada konflik antara pola ideal dan pola legacy, pilih perubahan paling kecil yang menyelesaikan masalah tanpa merusak alur bisnis.
