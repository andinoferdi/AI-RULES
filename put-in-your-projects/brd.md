# Business Requirements Document: [NAMA_PROJECT]

Document ID: BRD-[KODE_PROJECT]-[YYYY-MM-DD]
Date: [YYYY-MM-DD]
Owner: [NAMA_OWNER_BISNIS]
Status: Draft for Business, Product, and Engineering review

## Executive Summary

[Ringkas masalah bisnis utama yang ingin diselesaikan project ini. Jelaskan kondisi saat ini, dampaknya terhadap pengguna atau bisnis, dan kenapa project ini perlu dibuat sekarang.]

[Ringkas tujuan utama project dalam bahasa bisnis. Fokus pada outcome, bukan detail teknis implementasi.]

## Business Objectives

1. [Objective-001: tulis target bisnis yang spesifik dan terukur.]
2. [Objective-002: tulis target efisiensi, pendapatan, kualitas layanan, risiko, atau kepuasan pengguna.]
3. [Objective-003: tulis dampak yang diharapkan setelah project berjalan.]
4. [Objective-004: opsional, tulis target tambahan bila relevan.]

## Stakeholders

| Role | Name | Responsibility |
|------|------|----------------|
| Executive Sponsor | [NAMA] | Funding, strategic alignment, final escalation |
| Business Owner | [NAMA] | Business requirements, priority, sign-off |
| Product Owner | [NAMA] | Scope, feature priority, user value |
| Technical Owner | [NAMA] | Architecture, build, and delivery |
| QA / Tester | [NAMA] | Test planning and acceptance validation |
| End Users | [USER_GROUP] | Daily use and feedback |

## Scope

### In Scope
- [Fitur, proses, modul, atau area bisnis yang termasuk dalam project.]
- [Integrasi atau channel yang wajib didukung.]
- [Role user yang akan memakai sistem.]
- [Laporan, dashboard, atau analytics yang wajib tersedia.]

### Out of Scope
- [Fitur atau proses yang sengaja tidak dikerjakan pada fase ini.]
- [Integrasi yang ditunda.]
- [Migrasi, automasi, atau enhancement yang masuk fase berikutnya.]
- [Batasan operasional yang tidak menjadi tanggung jawab project ini.]

## Functional Requirements

- FR-001: Sistem harus memungkinkan [role] untuk [aksi utama] pada [objek/data].
- FR-002: Sistem harus menyediakan [fitur pencarian/filter/kategori] untuk [kebutuhan user].
- FR-003: Sistem harus mendukung [workflow/status/approval] sesuai proses bisnis.
- FR-004: Sistem harus membedakan akses berdasarkan [role/permission/ownership].
- FR-005: Sistem harus menyimpan riwayat perubahan penting pada [data/proses].
- FR-006: Sistem harus menampilkan pesan sukses, gagal, dan validasi yang jelas.
- FR-007: Sistem harus menyediakan laporan atau ringkasan untuk [kebutuhan bisnis].
- FR-008: Sistem harus mendukung export, import, atau integrasi data bila relevan.
- FR-009: Sistem harus menjaga konsistensi data saat proses dibuat, diubah, dibatalkan, atau disetujui.
- FR-010: Sistem harus menyediakan mekanisme konfigurasi untuk kebutuhan yang dapat berubah.

## Non-Functional Requirements

- NFR-001: Sistem harus tersedia minimal [TARGET_UPTIME] pada jam operasional yang ditentukan.
- NFR-002: Response utama harus selesai dalam [TARGET_RESPONSE_TIME] untuk skenario normal.
- NFR-003: Sistem harus mampu menangani minimal [JUMLAH_USER] pengguna atau request sesuai kebutuhan project.
- NFR-004: UI harus responsif pada perangkat yang digunakan target user.
- NFR-005: Sistem harus mengikuti kebijakan keamanan, autentikasi, authorization, dan pengelolaan data yang berlaku.
- NFR-006: Sistem harus memiliki logging atau monitoring yang cukup untuk investigasi masalah.

## Assumptions

- [Asumsi tentang data, user, platform, deadline, tim, atau dependency eksternal.]
- [Asumsi tentang ketersediaan stakeholder untuk review dan sign-off.]
- [Asumsi tentang kondisi sistem lama, API, atau integrasi yang dipakai.]
- [Asumsi tentang batasan teknis, operasional, atau bisnis.]

## Success Criteria

- [Kriteria-001: metrik bisnis atau operasional yang harus tercapai.]
- [Kriteria-002: fitur utama berjalan sesuai acceptance criteria.]
- [Kriteria-003: user dapat menyelesaikan proses utama tanpa hambatan besar.]
- [Kriteria-004: defect critical dan high sudah diselesaikan sebelum release.]

## Sign-off

| Name | Role | Signature | Date |
|------|------|-----------|------|
| | Executive Sponsor | | |
| | Business Owner | | |
| | Product Owner | | |
| | Technical Owner | | |
