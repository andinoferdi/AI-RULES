# [PROJECT_NAME] - Product Requirements Document

## Overview
Build [PROJECT_NAME] untuk [TARGET_USER] agar dapat mengelola [DOMAIN_DATA_UTAMA] dengan lebih cepat, aman, konsisten, dan terukur.

## Core Features

### User Management
- Login, logout, dan pengelolaan sesi user sesuai pola auth project.
- Profil user dengan data relevan terhadap role atau kebutuhan operasional.
- Role, permission, dan pembatasan akses lewat middleware, menu, dan route.

### Main Feature
- Membuat, membaca, mengubah, dan mengelola data utama: [DAFTAR_ENTITAS_UTAMA].
- Validasi input dan feedback jelas lewat validation error, flash message, atau pola UI project.
- Status, workflow, approval, atau grouping sesuai kebutuhan domain.
- Detail data dengan informasi cukup untuk pengambilan keputusan.

### Organization
- Dashboard ringkas untuk kondisi utama sistem dan status data penting.
- List view dengan filter, pencarian, sorting, dan pagination.
- Detail view untuk membaca informasi lengkap tanpa mengubah data lain.
- Form/modal untuk create, update, validasi, dan action.
- Report, export, import, atau analytics untuk monitoring.

## Technical Requirements

### Frontend
- Gunakan stack frontend project `[STACK_FRONTEND]`.
- UI konsisten, responsif, aksesibel, mengikuti pola layout dan komponen yang ada.
- State management mengikuti pola project. Validasi client hanya pendukung validasi server.

### Backend
- Gunakan stack backend project `[STACK_BACKEND]` + `[DATABASE]`.
- Route/API, controller, service, dan response mengikuti pola repo.
- Schema, migration, relasi, dan query mendukung listing, filter, report, export/import, dan integrasi.
- Authentication, authorization, validation, permission, dan error handling konsisten.
- Integrasi eksternal `[INTEGRASI_EKSTERNAL]` memakai konfigurasi environment yang aman.

### Infrastructure
- Konfigurasi berbasis environment.
- Automated testing sesuai prioritas project.
- CI/CD ready bila dikerjakan tim atau masuk production.
- Logging dan monitoring dasar untuk troubleshooting.

## Success Criteria
- User dapat menyelesaikan proses utama secara efisien sesuai role dan permission.
- Fitur prioritas berjalan sesuai acceptance criteria.
- App memuat cepat sesuai target performa project.
- Tampilan responsif pada perangkat target user.
- Tidak ada defect critical sebelum release.

## Priority
1. **Phase 1**: Fitur inti, auth/permission, UI dasar, workflow utama, pengelolaan data prioritas.
2. **Phase 2**: Integrasi, dashboard, report, export/import, dan enhancement prioritas.
3. **Phase 3**: Notifikasi, optimasi performa, automasi, analytics, observability, polishing.

## Timeline
Target MVP: [DURASI_TARGET] dengan asumsi scope, resource, dependency, environment, dan integrasi sudah jelas.
