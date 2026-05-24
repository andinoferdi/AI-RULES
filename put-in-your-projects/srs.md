# Markdown Software Requirements Specification (MSRS)

Template **Software Requirements Specification (SRS)** berbasis markdown untuk mendokumentasikan kebutuhan software secara jelas, terukur, dan mudah dipahami oleh business, product, engineering, QA, security, dan AI agent. Template ini mengikuti praktik umum SRS modern yang menekankan requirement yang dapat diverifikasi, traceability, quality attributes, dan pemisahan yang jelas antara “apa yang dibutuhkan” dengan “bagaimana cara membangunnya”.

Template ini dapat dipakai untuk berbagai jenis project, seperti web app, mobile app, API, dashboard, sistem internal, SaaS, automation, AI/ML system, atau integrasi antar sistem.

Designed to be:
- Readable, developer-friendly, dan AI-interpretable
- Cukup lengkap untuk project nyata, tetapi tetap fleksibel untuk disederhanakan
- Mudah diisi, dihapus, atau diperluas sesuai kebutuhan project

## Highlights

- **Standards-aware:** dapat diselaraskan dengan IEEE 830 dan ISO/IEC/IEEE 29148 bila project membutuhkan formalitas lebih tinggi
- **Comprehensive structure** dengan pola requirement yang jelas dan testable
- Dedicated sections untuk Quality of Service, Compliance, Security, dan AI/ML bila relevan
- **Built-in guidance, tips, and checklists** untuk membantu pengisian tiap section
- **Traceability-ready** dengan requirement ID dan verification matrix
- Cocok untuk project personal, akademik, startup, enterprise, dan regulated context

## Who Should Use This

- **Product manager dan business analyst** yang mendefinisikan scope dan outcome
- **Architect dan engineer** yang merancang solusi dari requirement yang stabil
- **QA dan SRE team** yang menyiapkan verification, test plan, SLA, atau SLO
- **Security, compliance, dan data governance team** yang perlu meninjau risiko dan kontrol
- **AI agent atau coding assistant** yang perlu memahami project sebelum mengubah kode

## Quick Start

1. Copy template ini ke repository, misalnya `srs.md`.
2. Isi metadata: version, author, organization, date, dan status dokumen.
3. Lengkapi Section 1 untuk menetapkan context, glossary, references, dan conventions.
4. Susun Section 2 untuk product context, user, constraint, dan asumsi sebelum menulis requirement detail.
5. Tulis requirement di Section 3 dengan ID unik, acceptance criteria, dan prioritas.
6. Definisikan verification di Section 4 dan jaga traceability matrix tetap sinkron.
7. Update revision history setiap ada perubahan scope, requirement, atau release penting.

## Template Structure (Overview)

1. Introduction: Purpose, scope, glossary, references, dan document conventions
2. Product Overview: Context, functions, constraints, users, assumptions, dan allocation
3. Requirements:
    - External Interfaces: UI, hardware, software, communication, dan integration
    - Functional Requirements: behavior sistem yang dapat diamati dari luar
    - Quality of Service: performance, security, reliability, availability, observability, usability
    - Compliance: kebutuhan legal, regulasi, kontrak, dan policy internal
    - Design & Implementation Constraints: installation, build/delivery, distribution, maintainability, reusability, portability, cost, deadlines, POC, dan change management
    - AI/ML: model specs, data management, guardrails, ethics, human-in-the-loop, dan lifecycle bila relevan
4. Verification: Methods, environments, artifacts, dan traceability
5. Appendixes: Supporting, non-normative materials

## Workflows

* `srs-template.md` — SRS lengkap dengan penjelasan dan panduan isi.
* `srs-template-bare.md` — Scaffold SRS minimal untuk project kecil.
* `req-template.md` — Template requirement per file untuk requirement modular.
* `req-template-bare.md` — Template requirement singkat untuk kebutuhan non-monolithic SRS.

#### One-shot document

  * Isi `srs-template.md`.
  * Export ke PDF/HTML bila perlu.
  * Bagikan ke stakeholder untuk review dan sign-off.

#### Long-lived SRS in VCS

  * Simpan `srs-template.md` sebagai `srs.md`.
  * Tambahkan atau ubah requirement secara bertahap.
  * Export saat release atau milestone penting.
  * Perlakukan `srs.md` sebagai source of truth requirement.
  * Simpan template di repo agar bahasa dan struktur requirement tetap konsisten.
  * Berikan SRS ke AI agent sebagai konteks utama sebelum coding.

#### Breakout files (MADR-inspired)

  * Kelola SRS utama plus file requirement terpisah di `requirements/`.
  * Gunakan `req-template.md` atau `req-template-bare.md` untuk tiap requirement.
  * Link setiap requirement dari index Section 3 di SRS.
  * Track hubungan requirement, test, issue, PR, dan release di Section 4.

#### Requirements-only (MADR-style)

  * Kelola `requirements/*.md` tanpa SRS monolithic.
  * Generate index atau roll-up SRS jika dibutuhkan.

## On Requirements Engineering

#### Overlaps Between Functional and Non-Functional Requirements

Dalam praktik nyata, batas antara functional requirement dan non-functional requirement tidak selalu benar-benar tegas. Beberapa requirement bisa menyentuh behavior sistem sekaligus kualitas, batasan keamanan, ketersediaan, atau compliance. Contohnya, fitur approval adalah fungsi, tetapi juga bisa berhubungan dengan auditability, security, dan governance.

#### Why Requirement Taxonomies Still Matter

Walaupun kategorinya bisa tumpang tindih, taxonomy requirement tetap penting karena membantu tim melihat kebutuhan dari beberapa sisi: apa yang sistem lakukan, seberapa baik sistem harus bekerja, constraint apa yang tidak boleh dilanggar, dan bagaimana requirement akan diverifikasi. Kategorisasi juga membantu mendeteksi requirement yang hilang, konflik antar kebutuhan, dan trade-off desain.

Untuk developer, QA, architect, dan AI agent, taxonomy requirement menjadi peta mental untuk memahami kompleksitas project. Ia membantu menjaga percakapan tetap presisi dari fase analisis, desain, implementasi, testing, sampai maintenance.

## Related Projects

* Markdown Software Design Description atau dokumen desain teknis project
* Architecture Decision Records untuk keputusan arsitektur penting
* Product Requirements Document untuk kebutuhan produk
* Business Requirements Document untuk kebutuhan bisnis

## License

Template ini boleh disalin, diubah, dan digunakan ulang untuk project personal, akademik, internal, maupun komersial, kecuali organisasi Anda memiliki kebijakan lisensi khusus.
