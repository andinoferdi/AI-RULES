# Execution Plan: Elevasi skills/skill-maker (Andino Workflow)

**Target:** `skills/skill-maker`  
**Internal Method ID:** `andino-skill-maker` (aliases: `skill-maker`, `method-authoring`, `andino-method-authoring`, `writing-skills`)  
**Status:** DONE  
**Phase:** 5 - Verification & Delivery Complete  
**Reference Benchmark:** `obra/superpowers:writing-skills`  
**Governing Protocol:** Andino Workflow (Single durable checkpoint, proportional investigation, floor invariants)  
**Next Action:** Commit atomik dan push ke origin/andino-workflow.

---

## 1. Context & Objectives

Kualitas output dan keefektifan AI pada `skills/skill-maker` saat ini tertinggal dibandingkan `obra/superpowers:writing-skills`. Analisis mendalam bersama Council mengungkap tiga penyebab fundamental:
1. **Birokrasi Meta-Governance:** Dokumen lama terbebani oleh terminologi kaku (*NOT_VERIFIED*, *provenance*, *authority boundary*, skrip verifikasi buatan) alih-alih resep tindakan operasional langsung.
2. **Hilangnya Cognitive Scaffolding Kunci:** Dokumen lama tidak memiliki mekanisme esensial Obra:
   - **SDO (Skill Discovery Optimization):** Aturan ketat *trigger-only* tanpa ringkasan alur kerja agar model tidak memotong kompas.
   - **Match Form to Failure:** Matriks empiris memilih bentuk panduan (*Positive Recipe/Structural Slot* vs *Prohibition*) berdasarkan jenis kegagalan, menghindari jebakan larangan pada masalah bentuk output (*shaping*).
   - **Persuasion & Loophole Closing:** Menutup celah rasionalisasi (*"spirit vs letter"*, *red flags list*, tabel alasan vs realitas).
   - **Micro-Testing Wording:** Protokol uji varians (5+ repetisi) sebelum pengujian penuh.
   - **Degrees of Freedom & Anthropic Craft:** Kalibrasi kebebasan (High/Medium/Low freedom) dan efisiensi token.
3. **Ketidakkonsistenan Layout:** Layout belum mengikuti standar elevated skills Andino Workflow (`andino-delegation`, `andino-debugging`, `andino-brainstorming`) yang menyajikan kontrak operasional ringkas (<150 baris) di root dan memindahkan craft mendalam ke direktori modular `resources/`.

### Tujuan Elevasi
1. Menghadirkan `skills/skill-maker/SKILL.md` operasional (<120 baris, plafon absolut <150 baris) yang memuat:
   - Frontmatter SDO (Trigger-only).
   - Dominant Negative Gates.
   - Dual-Mode Triage Router (Mode A: Remedial/TDD, Mode B: Greenfield/Invariants).
   - 5 Floor Invariants.
   - Anti-Rationalization Refutations Table.
   - Diagnostic Red Flags (Stop Immediately).
   - Progressive Disclosure Router.
   - Runnable Deterministic Python Example (`ANDINO_NEGATIVE=0` lolos, `ANDINO_NEGATIVE=1` keluar kode 1).
   - Provenance.
2. Membangun 5 modul *deep craft* di `skills/skill-maker/resources/`:
   - `sdo-and-discovery-protocols.md`
   - `failure-form-matching-and-bulletproofing.md`
   - `subagent-testing-and-pressure-scenarios.md`
   - `anthropic-craft-and-degrees-of-freedom.md`
   - `worked-examples-and-templates.md`
3. Memperbarui `skills/skill-maker/GUIDE.md` sebagai panduan otoritatif komprehensif.
4. Menambahkan script uji deterministik offline `scripts/verify_skill_maker_elevation.py` (<0.5 detik).
5. Memastikan sinkronisasi langsung ke host runtime (`~/.claude/skills/andino-workflow/skills/skill-maker` dan `~/.claude/skills/andino-skill-maker`) dan kompatibilitas penuh dengan `ai-rules setup`.
6. Melakukan commit atomik dan push ke branch `andino-workflow`.

---

## 2. Architecture & File Breakdown

```
skills/skill-maker/
├── SKILL.md                                        # Kontrak operasional utama (<120 baris)
├── GUIDE.md                                        # Panduan mendalam bagi pembuat skill
└── resources/
    ├── contract.md                                 # Kontrak data dan skema evaluasi
    ├── sdo-and-discovery-protocols.md              # Protokol SDO, keyword, trigger engineering
    ├── failure-form-matching-and-bulletproofing.md # Matriks Form-to-Failure & Anti-Rasionalisasi
    ├── subagent-testing-and-pressure-scenarios.md  # TDD Dokumentasi, Pressure Testing, Micro-tests
    ├── anthropic-craft-and-degrees-of-freedom.md   # Degrees of Freedom, Token Craft, Anti-Patterns
    └── worked-examples-and-templates.md            # Template SKILL.md (<150 baris) & Runbook

scripts/
└── verify_skill_maker_elevation.py                 # Verifier offline deterministik
```

---

## 3. Detailed Change Specifications

### Task 1: Implements Modular Resources in `skills/skill-maker/resources/`
- **Resource 1: `sdo-and-discovery-protocols.md`**
  - Menjelaskan arsitektur penemuan agen: bagaimana LLM membaca deskripsi frontmatter saat startup.
  - Aturan emas: Deskripsi hanya berisi *kapan menggunakan* ("Use when [kondisi pemicu, gejala, situasi spesifik]"), **DILARANG MERANGKUM ALUR KERJA SKILL**.
  - Bukti empiris: Ringkasan alur kerja membuat agen melewatkan pembacaan dokumen inti.
  - Rekayasa kata kunci (pesan error, gejala, sinonim, nama tool/library).
  - Contoh positif vs negatif deskripsi.

- **Resource 2: `failure-form-matching-and-bulletproofing.md`**
  - Matriks Form-to-Failure (Tabel empiris: Kapan memakai Larangan vs Resep Positif vs Slot Struktural vs Predikat Kondisional).
  - Mengapa larangan ("don't X") menjadi bumerang bagi masalah pembentukan output (*shaping*).
  - Aturan *No Nuance Clauses* dan *Exemption Clauses Scope Leakage*.
  - Menutup celah rasionalisasi: Prinsip *"Melanggar huruf/teks aturan adalah melanggar semangat aturan"*.
  - Tabel Anti-Rasionalisasi komprehensif (`| Alasan / Dalih | Realitas Mekanis |`).
  - Daftar *Diagnostic Red Flags* (STOP and Start Over).

- **Resource 3: `subagent-testing-and-pressure-scenarios.md`**
  - Metodologi TDD untuk dokumentasi:
    - RED: Jalankan skenario tekanan tanpa skill -> catat dalih/kegagalan verbatim.
    - GREEN: Tulis instruksi minimalis penangkal -> verifikasi kepatuhan model.
    - REFACTOR: Tutup celah baru -> catat di tabel rasionalisasi.
  - 4 Varian Tekanan: Waktu/urgensi, Sunk cost (usaha yang terbuang), Otoritas atasan, Kelelahan/konteks panjang.
  - Protokol Micro-Testing Wording: 5+ repetisi per varian frasa, varians sebagai metrik ketegasan instruksi, inspeksi manual kecocokan.

- **Resource 4: `anthropic-craft-and-degrees-of-freedom.md`**
  - Kalibrasi Degrees of Freedom (Anthropic Best Practices):
    - High Freedom: Heuristik teks untuk tugas banyak alternatif.
    - Medium Freedom: Pseudocode/template untuk pola fleksibel terarah.
    - Low Freedom: Script eksak/perintah pasti untuk operasi rapuh & berisiko tinggi.
  - Efisiensi Token: Asumsi agen sudah pintar; hapus penjelasan umum; delegasikan detail ke flag `--help` atau sub-resource.
  - Prinsip *Single Great Example*: Satu contoh kode lengkap, runnable, dan beranotasi alasan (WHY) jauh lebih baik daripada contoh multi-bahasa yang dangkal.
  - Katalog Anti-Patterns: Narasi retrospektif sesi, dilusi multi-bahasa, kode di dalam diagram, label generik, pengulangan manual aturan linting.

- **Resource 5: `worked-examples-and-templates.md`**
  - Template standar `SKILL.md` (<150 baris) dengan slot struktural wajib.
  - Template `GUIDE.md` komprehensif.
  - Template Operational Runbook (Human-in-the-Loop).

### Task 2: Elevate `skills/skill-maker/SKILL.md` (<120 lines)
- Struktur kontrak operasional ringkas:
  1. Frontmatter dengan SDO (Trigger-only).
  2. Blockquote keanggotaan Andino Workflow.
  3. Dominant Negative Gates (kapan DITOLAK membuat skill: solusi satu kali, aturan yang bisa ditegakkan linter/compiler, instruksi pasif yang milik agent-document-authoring).
  4. Operational Triage Router (Mode A: Remedial / TDD-driven, Mode B: Greenfield / Invariant-driven).
  5. 5 Floor Invariants (Iron Law, Match Form to Failure, SDO Isolation, Single Great Example, Zero-Negotiation Boundary).
  6. Anti-Rationalization Refutations Table.
  7. Diagnostic Red Flags.
  8. Progressive Disclosure Router.
  9. Runnable Operational Python Example (memvalidasi invarian kontrak dengan `ANDINO_NEGATIVE`).
  10. Provenance.

### Task 3: Elevate `skills/skill-maker/GUIDE.md`
- Menyajikan panduan lengkap bagi model/pengguna saat menulis atau mengevaluasi skill.
- Memadukan alur kerja TDD dan Greenfield secara seimbang.
- Menjelaskan rincian eksekusi dari setiap tahap penulisan skill.

### Task 4: Create Deterministic Offline Verifier `scripts/verify_skill_maker_elevation.py`
- Memverifikasi:
  1. `skills/skill-maker/SKILL.md` < 150 baris (target < 120 baris).
  2. Eksekusi script operasional Python internal (`ANDINO_NEGATIVE=0` exit 0, `ANDINO_NEGATIVE=1` exit 1).
  3. Integritas seluruh berkas `resources/*.md` dan keterjangkauan link.
  4. Tidak ada emoji dekoratif non-fungsional.
  5. Kompatibilitas fungsi `_is_valid_skill_tree` dari installer `ai-rules setup`.

### Task 5: Sync to Host Directory, Verify, and Commit/Push
- Sinkronisasi file yang diubah ke `~/.claude/skills/andino-workflow/skills/skill-maker` dan `~/.claude/skills/andino-skill-maker`.
- Eksekusi verifier deterministik.
- Lakukan commit atomik dan push ke `andino-workflow`.

---

## 4. Verification & Acceptance Criteria
- [x] `skills/skill-maker/SKILL.md` strictly < 150 baris (Actual: 105 baris).
- [x] Semua resource modular terpasang di `skills/skill-maker/resources/` (6 modul).
- [x] `scripts/verify_skill_maker_elevation.py` berjalan sukses (exit 0) dalam < 0.2 detik (7/7 test suites pass).
- [x] Berkas tersinkronisasi sempurna di host lokal runtime (Claude Code & Codex).
- [x] Git commit dan push siap dieksekusi ke remote `origin/andino-workflow`.

```
Starting deterministic offline verification for andino-skill-maker elevation...
PASS: SKILL.md line count budget (105 lines < 150)
PASS: SDO frontmatter rules strictly verified
PASS: Operational Python harness verified (exit 0 on valid, exit 1 on ANDINO_NEGATIVE=1)
PASS: All 6 modular resources verified with 100% link integrity
PASS: Zero decorative emojis detected across skill-maker suite
PASS: Forwarding shim (skills/method-authoring) verified
PASS: Installer setup compatibility verified byte-for-byte across 5 host targets

ALL 7 VERIFICATION SUITES PASSED SUCCESSFULLY (100% PASS).
```
