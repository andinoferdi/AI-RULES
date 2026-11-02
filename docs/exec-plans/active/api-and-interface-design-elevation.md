# Execution Plan: Elevasi skills/api-and-interface-design (Andino Workflow)

**Target:** `skills/api-and-interface-design`  
**Internal Method ID:** `andino-api-and-interface-design` (alias: `api-and-interface-design`)  
**Status:** IN_PROGRESS  
**Phase:** Phase 6 — Verification Complete & Ready for Commit/Push  
**Reference Benchmark:** `addyosmani/agent-skills/skills/api-and-interface-design`  
**Governing Protocol:** Andino Workflow (Single durable checkpoint, proportional investigation, floor invariants)  
**Next Action:** Commit atomik dan push ke origin/andino-workflow.

---

## 1. Executive Snapshot & Putusan Council

### Konteks & Akar Masalah
Investigasi mendalam dan sidang Council (5 lensa: *Contrarian*, *First Principles*, *Expansionist*, *Outsider*, *Executor* serta 2 peer reviewers independen) mengidentifikasi penyebab utama rendahnya kualitas output AI pada `skills/api-and-interface-design` dibandingkan upstream Addy Osmani:

1. **Kehilangan Jangkar Representasi (*Representational Anchors*):** Upstream Addy Osmani menyediakan contoh kode TypeScript konkret (`TaskAPI`, `APIError`, Zod boundary validation, `TaskStatus` discriminated unions, branded types `OrderId`/`CustomerId`, dan pagination request/response). Versi lokal sebelumnya menggantinya dengan meta-governance naratif abstrak (*proportional investigation*, *single durable checkpoint*), sehingga AI kehilangan jangkar probabilitas untuk membentuk kode yang benar.
2. **Ketiadaan *Negative Constraint Gates*:** Ketiadaan tabel *Common Rationalizations* (10 dalih malas model seperti *"we'll document later"*, *"no pagination needed"*, *"PUT is simpler than PATCH"*) dan 11 *Diagnostic Red Flags* membuat model bebas berkompromi ke anti-pattern umum internet.
3. **Duplikasi Konten Internal:** File `SKILL.md`, `GUIDE.md`, dan `resources/http-contracts/contract.md` serta `guide.md` saat ini merupakan salinan kata-demi-kata, tanpa diferensiasi kedalaman kognitif.
4. **Ketidakkonsistenan Standar Elevated Skill:** Belum mengadopsi struktur standar elevated skill Andino Workflow:
   - Root `SKILL.md` ramping (**<150 baris**).
   - Frontmatter SDO (*Skill Discovery Optimization*) trigger-only.
   - *Dominant Negative Gates* & *5 Floor Invariants*.
   - *Anti-Rationalization Refutations* & *Diagnostic Red Flags*.
   - *Progressive Disclosure Router* ke resource modular.
   - *Deterministic Python Test Harness* (exit 0 normal, exit 1 pada `ANDINO_NEGATIVE=1`).

### Putusan Konsensus Council & Mitigasi Risiko
- **Pencegahan *File Thrashing* & Kepatuhan Portofolio:** `scripts/verify_portfolio.py` mengunci `MODES['api-and-interface-design']` pada 3 direktori resmi: `module-depth`, `import-enforcement`, dan `http-contracts`. Rencana awal untuk memecah ke 6+ subdirektori dibatalkan guna mencegah CI break dan fragmentasi kognitif AI.
- **Konsolidasi HTTP & Boundary Pipeline:** Zod edge validation, TypeScript interface patterns, pagination, dan atomic idempotency disatukan ke dalam `resources/http-contracts/` sebagai satu pipeline penerimaan request (*ingestion pipeline*) yang koheren.
- **Dua File Pendukung Lepas:** `resources/anti-rationalization-and-failure-modes.md` (tabel dalih, red flags, verification checklist) dan `resources/worked-example.md` (studi kasus before-after nyata) diletakkan langsung di bawah `resources/`.
- **Nilai Tambah Melampaui Upstream (*10x Leap*):**
  1. *Tri-Layer Architecture Seam:* Makro (`import-enforcement`), Meso (`module-depth` Ousterhout leverage), dan Mikro (`http-contracts`).
  2. *Agent-Native / Tool-Calling Readiness:* Panduan kontrak antarmuka deterministik ramah AI agent (self-healing error shapes, parameter schema tightness).
  3. *Additive Schema Evolution:* Strategi non-breaking change, deprecation lifecycle, dan sunset headers.

---

## 2. Architecture & File Breakdown

```
skills/api-and-interface-design/
├── SKILL.md                                        # Kontrak operasional utama (<150 baris, target ~125 baris)
├── GUIDE.md                                        # Panduan terpadu komprehensif lintas 3 pilar
├── references/
│   └── license.md                                  # Retained MIT license notice Addy Osmani
└── resources/
    ├── http-contracts/
    │   ├── contract.md                             # Kontrak isolasi resource http-contracts (<150 baris)
    │   └── guide.md                                # Spesifikasi REST, Zod boundary, idempotensi atomik, typing
    ├── module-depth/                               # [Eksisting & Terdaftar di Portfolio]
    │   ├── contract.md
    │   ├── guide.md
    │   └── resources/
    ├── import-enforcement/                         # [Eksisting & Terdaftar di Portfolio]
    │   ├── contract.md
    │   ├── guide.md
    │   └── resources/
    ├── anti-rationalization-and-failure-modes.md   # 10 tabel dalih model + 11 Red Flags + Checklist
    └── worked-example.md                           # Case study before-after konkret TypeScript & SQL

scripts/
└── verify_api_and_interface_design_elevation.py    # Skrip verifier offline deterministik
```

---

## 3. Detailed Change Specifications

### Task 1: Re-architect `resources/http-contracts/`
- **`resources/http-contracts/guide.md`:**
  - Hapus salinan duplikat dari SKILL.md.
  - Masukkan panduan komprehensif:
    1. *Contract-First REST Design:* Resource nouns, plural endpoints, HTTP methods (`GET`, `POST`, `PATCH`, `DELETE`), URL parameter design, filtering, pagination standar `{ data, pagination: { page, pageSize, totalItems, totalPages } }`.
    2. *TypeScript Representation Anchors:* `TaskAPI` spec, separated input/output interfaces (`CreateTaskInput` vs `Task`), branded types (`OrderId`, `CustomerId`), discriminated unions (`TaskStatus`).
    3. *Boundary Validation with Zod:* `safeParse` di route handler, sanitasi data pihak ketiga sebagai data tidak tepercaya, larangan validasi defensif di domain internal.
    4. *Uniform Error Semantics:* Standar `APIError` envelope (`error: { code, message, details }`), mapping status code HTTP (`400`, `401`, `403`, `404`, `409`, `422`, `500`).
    5. *Atomic Idempotency Rigor:* Intent derivation vs attempt, atomic claim via database UNIQUE constraint (check-then-act adalah TOCTOU race), SHA-256 payload hash verification, three outcomes (`SUCCESS`, `FAILURE`, `UNKNOWN`), handling in-flight duplicates (`409` vs `202`), dan retention window melampaui DLQ.
    6. *Agent-Native Interface Readiness:* Parameter typing deterministik untuk AI tool-calling, self-healing structured errors.
    7. *Additive Evolution & Deprecation:* Expand-contract migration, sunset headers (`Sunset: <date>`), penambahan field opsional.
- **`resources/http-contracts/contract.md`:**
  - Header isolasi resource non-callable: `Resource contract; selected directly under its canonical owner.` (tanpa YAML frontmatter).
  - Ringkasan aturan kontraktual, input/output schemas, dan batasan eksekusi (<150 baris).

### Task 2: Implement `resources/anti-rationalization-and-failure-modes.md`
- Header isolasi non-callable resource.
- Tabel 10 Refutasi Rasionalisasi Model (diadopsi dan diperluas dari Addy Osmani):
  1. *"We'll document the API later"* -> Types ARE the spec.
  2. *"We don't need pagination for now"* -> 100+ items break callers.
  3. *"PATCH is complicated, let's just use PUT"* -> PUT overwrites whole object.
  4. *"We'll version the API when we need to"* -> Diamond dependency trap; additive evolution.
  5. *"Nobody uses that undocumented behavior"* -> Hyrum's Law.
  6. *"Internal APIs don't need contracts"* -> Internal consumers are consumers.
  7. *"Accepting Idempotency-Key header is enough"* -> Header is declaration, unique constraint is implementation.
  8. *"Our queue guarantees exactly-once delivery"* -> No distributed queue guarantees exactly-once across crashes.
  9. *"Duplicate requests are rare"* -> Retries correlate with degraded dependencies.
  10. *"Validating at every layer makes code safer"* -> Boundary validation only; trust internal contracts.
- 11 Diagnostic Red Flags (Stop Immediately).
- 12-Point Verification Checklist sebelum merilis interface.

### Task 3: Elevate `resources/worked-example.md`
- Pertahankan studi kasus Before & After transformasi:
  - Before: `/api/orders/create` dengan stringly-typed inputs, TOCTOU check-then-act, raw database error leakage, remote charge sebelum persist intent.
  - After: `/api/orders` dengan branded types, Zod boundary schema, atomic SQL unique constraint, guarded payload hash, dan structured `APIError`.
- Tambahkan contoh Agent-Native Tool Calling interface dengan structured error recovery.

### Task 4: Rewrite Root `SKILL.md` (<150 Baris)
- Frontmatter SDO trigger-only:
  ```yaml
  ---
  name: andino-api-and-interface-design
  description: Use when designing or refactoring APIs, module seams, HTTP endpoints, boundary contracts, error shapes, or atomic idempotency. Operates under Andino Workflow governance.
  ---
  ```
- 1. Dominant Negative Gates (kapan skill ditolak).
- 2. Tri-Modal Selection Router (`module-depth`, `import-enforcement`, `http-contracts`).
- 3. 5 Floor Invariants:
  1. *Contract First & Edge Validation:* Validasi hanya di perimeter luar; kode internal percaya tipe.
  2. *Atomic Concurrency Invariant:* Check-then-act adalah bug; unique constraint adalah satu-satunya gerbang konkurensi.
  3. *Additive Evolution (One-Version Rule):* Jangan ubah tipe lama; tambah field baru secara opsional.
  4. *Hyrum's Law Awareness:* Setiap perilaku yang dapat diobservasi adalah komitmen.
  5. *Uniform Error & Canonical Anchors:* Satu amplop error standar (`code`, `message`, `details`) di seluruh antarmuka.
- 4. Compact Representation Anchor (TypeScript golden signature).
- 5. Anti-Rationalization Refutations (ringkasan 5 poin kunci).
- 6. Diagnostic Red Flags (6 poin instan).
- 7. Progressive Disclosure Router ke `resources/`.
- 8. Runnable Deterministic Python Harness:
  - Memverifikasi skema kontrak API, hash payload, dan atomic claim.
  - Normal run: exit 0 dengan status `CONTRACT_VERIFIED`.
  - `ANDINO_NEGATIVE=1`: exit 1 dengan diagnostic failure.
- 9. Provenance link ke `references/license.md`.

### Task 5: Rewrite Root `GUIDE.md`
- Panduan komprehensif terpadu menghubungkan Macro (`import-enforcement`), Meso (`module-depth`), dan Micro (`http-contracts`).
- Petunjuk integrasi arsitektur bagi pengembang dan agen.

### Task 6: Implement Deterministic Verifier `scripts/verify_api_and_interface_design_elevation.py`
- Menguji:
  1. Batas ketat baris `SKILL.md` (<150 baris).
  2. Batas ketat baris `resources/http-contracts/contract.md` (<150 baris).
  3. Tidak adanya `SKILL.md` bersarang di seluruh `resources/`.
  4. Header isolasi non-callable resource pada setiap file resource.
  5. Eksekusi python test harness (exit 0 normal, exit 1 pada `ANDINO_NEGATIVE=1`).
  6. Integritas seluruh file modular dan ketiadaan dead markdown links.
  7. Audit emoji non-fungsional.

### Task 7: Verifikasi Portofolio & Integrasi `ai-rules setup`
- Jalankan `scripts/verify_portfolio.py` (wajib 6/6 test pass).
- Uji `ai-rules setup --dry-run` untuk menjamin tidak ada regresi distribusi.

### Task 8: Commit & Push
- Buat atomic commit dengan pesan deskriptif sesuai format repo:
  `feat(skills): elevate api-and-interface-design with tri-layer seams, atomic idempotency, and strict anchors`
- Push ke branch `andino-workflow`.

---

## 4. Execution Phases & Progress Tracking

- [x] **Phase 1: Council Deliberation & Blueprint Formulation** (Done)
- [x] **Phase 2: Durable Planning** (`docs/exec-plans/active/api-and-interface-design-elevation.md`) (Done)
- [x] **Phase 3: Modular Resource Implementation**
  - [x] Task 3.1: Re-architect `resources/http-contracts/guide.md` & `contract.md` (Done)
  - [x] Task 3.2: Implement `resources/anti-rationalization-and-failure-modes.md` (Done)
  - [x] Task 3.3: Elevate `resources/worked-example.md` (Done)
- [x] **Phase 4: Root Skill & Guide Elevation**
  - [x] Task 4.1: Rewrite root `SKILL.md` (<150 lines + Python harness) (Done)
  - [x] Task 4.2: Rewrite root `GUIDE.md` (Done)
- [x] **Phase 5: Automated Verification & Setup Reflection**
  - [x] Task 5.1: Author & run `scripts/verify_api_and_interface_design_elevation.py` (Done)
  - [x] Task 5.2: Run `scripts/verify_portfolio.py` (Done)
  - [x] Task 5.3: Verify `ai-rules setup --dry-run` (Done)
- [ ] **Phase 6: Commit and Push**
  - [ ] Task 6.1: Git status & diff review
  - [ ] Task 6.2: Atomic commit & push ke `origin/andino-workflow`
