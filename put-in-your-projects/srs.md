# Software Requirements Specification (SRS)

Template SRS berbasis markdown untuk mendokumentasikan kebutuhan software `[PROJECT_NAME]` secara jelas, terukur, dan mudah dipahami business, product, engineering, QA, security, dan AI agent. Menekankan requirement yang dapat diverifikasi, traceability, quality attributes, dan pemisahan jelas antara "apa yang dibutuhkan" dengan "cara membangunnya".

Dibuat agar:
- Readable, developer-friendly, dan AI-interpretable.
- Cukup lengkap untuk project nyata, tetapi fleksibel per modul.
- Mudah diisi, dihapus, atau diperluas sesuai task, PR, release, dan integrasi.

## Highlights
- **Standards-aware:** dapat diselaraskan dengan IEEE 830 dan ISO/IEC/IEEE 29148 bila butuh formalitas lebih tinggi.
- **Comprehensive structure** dengan pola requirement yang jelas dan testable.
- Section khusus untuk Quality of Service, Compliance, Security, permission, integrasi, dan observability bila relevan.
- **Traceability-ready** dengan requirement ID dan verification matrix yang bisa dihubungkan ke task, PR, test, route, controller, service, dan migration.

## Who Should Use This
- **Product manager & business analyst** yang mendefinisikan scope, flow, dan prioritas.
- **Architect & engineer** yang merancang solusi dari requirement yang stabil.
- **QA & SRE** yang menyiapkan verification, test plan, environment, SLA/SLO.
- **Security, compliance, & data governance** yang meninjau auth, role, permission, dan kontrol data.
- **AI agent / coding assistant** yang perlu memahami project sebelum mengubah kode.

## Quick Start
1. Copy template ini ke repository requirements sebagai `srs.md`.
2. Isi metadata: version, author, organization, date, status, dan target modul.
3. Lengkapi Section 1: context, glossary, references, conventions, dan rujukan ke `brd.md`, `prd.md`, task notes.
4. Susun Section 2: product context, user, constraint stack, integrasi, permission, dan asumsi.
5. Tulis requirement di Section 3 dengan ID unik, acceptance criteria, prioritas, dan referensi kode bila diketahui.
6. Definisikan verification di Section 4 dan jaga traceability matrix sinkron dengan test, PR, dan task.
7. Update revision history setiap ada perubahan scope, requirement, integrasi, atau keputusan penting.

## Template Structure (Overview)
1. Introduction: Purpose, scope, glossary, references, conventions.
2. Product Overview: Context, functions, constraints, users, assumptions, allocation.
3. Requirements:
   - External Interfaces: UI, hardware bila ada, software, web/API, communication, integrasi.
   - Functional Requirements: behavior sistem yang dapat diamati dari luar.
   - Quality of Service: performance, security, reliability, availability, observability, usability.
   - Compliance: legal, regulasi, kontrak, policy internal, credential handling, data governance.
   - Design & Implementation Constraints: stack, build/delivery, maintainability, legacy naming, cost, deadline.
   - AI/ML: model specs, data management, guardrails, ethics, human-in-the-loop bila ada kebutuhan AI/ML.
4. Verification: methods, environments, artifacts, test case, UAT, traceability.
5. Appendixes: diagram, screenshot, notes task, payload contoh, referensi PR.

## Catatan Requirements Engineering
Batas antara functional dan non-functional requirement tidak selalu tegas. Fitur seperti approval, role/permission, import/export, atau integrasi adalah fungsi, tetapi juga menyentuh auditability, security, reliability, dan governance. Taxonomy requirement tetap penting: membantu melihat apa yang sistem lakukan, seberapa baik, constraint apa yang tidak boleh dilanggar, dan bagaimana diverifikasi. Ini juga membantu mendeteksi requirement yang hilang, konflik, dan trade-off desain.

## Related Documents
- `brd.md` untuk kebutuhan bisnis.
- `prd.md` untuk kebutuhan produk.
- `code-rules.md`, `be-rules.md`, `fe-rules.md` untuk aturan implementasi.
- `task.md` dan task notes untuk konteks task, acceptance criteria, dan riwayat keputusan.

## License
Template boleh disalin, diubah, dan digunakan ulang untuk project internal, kecuali organisasi punya kebijakan lisensi khusus.
