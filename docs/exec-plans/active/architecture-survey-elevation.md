# Execution Plan: Elevasi skills/architecture-survey (Andino Workflow)

**Target:** `skills/architecture-survey`  
**Internal Method ID:** `andino-architecture-survey` (aliases: `architecture-survey`, `improve-codebase-architecture`)  
**Status:** DONE  
**Phase:** 5 - Verification & Delivery Complete  
**Reference Benchmark:** `mattpocock/skills:skills/engineering/improve-codebase-architecture` (+ `HTML-REPORT.md` & `codebase-design`)  
**Governing Protocol:** Andino Workflow (Single durable checkpoint, proportional investigation, floor invariants, hub-and-spoke topology)  
**Next Action:** Commit atomik dan push ke origin/andino-workflow.

---

## 1. Context & Objectives

Evaluasi komparatif mendalam dan sesi Council mengungkapkan bahwa kualitas output AI pada `skills/architecture-survey` saat ini tertinggal dari referensi Matt Pocock karena tiga faktor struktural:
1. **Lemahnya Kendali Pembentukan Output (Output Shaping):** AI sering menghasilkan teks bertele-tele (*corporate/academic fluff*) tanpa batasan ringkas: 1 kalimat problem, 1 kalimat solution, dan *wins* $\le 6$ kata.
2. **Ketiadaan Standar Visual Ketat:** Tidak adanya 5 pola diagram *Before/After* berstandar tinggi (~320px, kontras simetris, skema warna stone/slate dengan aksen leakage merah) membuat model menghasilkan diagram generik atau melompati visualisasi sama sekali.
3. **Ketidakkonsistenan Layout Andino Workflow:** Dokumen `SKILL.md` saat ini (165 baris) belum mengikuti standar elevated skills (`andino-skill-maker`, `andino-delegation`, dll.) yang mewajibkan batas ketat $<150$ baris, SDO frontmatter *trigger-only*, Dominant Negative Gates, Tri-Mode Router, 5 Floor Invariants, Anti-Rationalization Refutations, Red Flags, dan Python operational harness.

### Keunggulan Andino yang Wajib Dipertahankan:
- **Resilience Offline:** Hybrid HTML report yang memuat CDN Tailwind/Mermaid saat online, namun memiliki embedded CSS/SVG fallback yang kokoh saat offline/air-gapped.
- **Batasan Non-Destruktif:** Survei murni membaca kode dan menulis ke temporary OS directory (`$TMPDIR` atau `%TEMP%`), tanpa mutasi kode produk atau repositori.
- **Durable Checkpoint Integration:** Hasil survei terintegrasi langsung ke execution plan Andino.

### Tujuan Elevasi:
1. Membangun root `SKILL.md` berdensitas tinggi ($<150$ baris, target ~110-125 baris) yang lulus SDO, gate negatif, router, dan Python harness.
2. Memperbarui `GUIDE.md` sebagai otoritas craft mendalam.
3. Menata ulang `resources/` menjadi 6 modul terarah berbasis topologi *Hub-and-Spoke*:
   - `resources/architectural-vocabulary.md`
   - `resources/diagram-patterns.md`
   - `resources/html-report-scaffold.md`
   - `resources/subagent-exploration-brief.md`
   - `resources/grilling-and-adr-protocols.md`
   - `resources/worked-example.md`
4. Menambahkan script verifier deterministik offline `scripts/verify_architecture_survey_elevation.py` ($<0.5$ detik).
5. Memperbarui legal provenance di `references/legal/provenance.md` dan `skills/architecture-survey/references/license.md`.
6. Memastikan kelulusan 100% pada `python -I scripts/verify_portfolio.py`, sinkronisasi host runtime `ai-rules setup`, serta commit dan push ke `origin/andino-workflow`.

---

## 2. Architecture & File Breakdown

```
skills/architecture-survey/
├── SKILL.md                                        # Kontrak operasional utama (<150 baris, SDO, Python test)
├── GUIDE.md                                        # Panduan craft komprehensif
├── references/
│   └── license.md                                  # Lisensi terdesentralisasi (Matt Pocock MIT 2026)
└── resources/
    ├── architectural-vocabulary.md                 # 10 istilah kanonik, frasa terlarang, formula wins
    ├── diagram-patterns.md                         # 5 template visual Before/After (~320px height)
    ├── html-report-scaffold.md                     # Scaffold HTML hibrida (CDN + offline CSS/SVG fallback)
    ├── subagent-exploration-brief.md               # Prompt brief subagent penelusur hotspot & friction
    ├── grilling-and-adr-protocols.md               # Wawancara interaktif pasca-survei, glossary, ADR
    └── worked-example.md                           # Studi kasus Order Intake pipeline & invariant checks

scripts/
└── verify_architecture_survey_elevation.py         # Deterministic offline verifier (<0.5s)

references/legal/
└── provenance.md                                   # Catatan elevasi 2026-11-02
```

---

## 3. Detailed Change Specifications

### Task 1: Implements Modular Resources in `skills/architecture-survey/resources/`

- **Task 1.1: `resources/architectural-vocabulary.md`**
  - **Starting State:** Tersebar sebagian di `SKILL.md` lama (baris 37-71).
  - **Operation:** Buat file mandiri yang mendefinisikan 10 istilah kanonik secara ketat: `module`, `interface`, `implementation`, `depth`, `deep`, `shallow`, `seam`, `adapter`, `leverage`, `locality`.
  - **Kontrak:** Tabel larangan substitusi kata (*component, service, API, boundary, layer, wrapper*), formula wins $\le 6$ kata (`[Kategori]: [Klaim Terukur]`), dan kriteria *The Deletion Test*.
  - **Acceptance:** File ada, tidak ada tautan rusak, memuat tabel substitusi dan formula wins terukur.

- **Task 1.2: `resources/diagram-patterns.md`**
  - **Starting State:** Dideskripsikan singkat di `worked-example.md` lama tanpa spesifikasi template utuh.
  - **Operation:** Buat file komprehensif yang memuat 5 pola visual Before/After:
    1. *Mermaid graph:* Flowchart dependency dan call flow dengan `classDef leak stroke:#dc2626`.
    2. *Hand-built boxes-and-arrows:* HTML/CSS divs + inline SVG paths untuk modul deep dengan internals pudar.
    3. *Cross-section:* Tumpukan horizontal bands untuk mengilustrasikan runtuhnya layer tipis.
    4. *Mass diagram:* Rasio luas interface (persegi pendek) vs implementasi (persegi tinggi).
    5. *Call-graph collapse:* Pohon pemanggilan bertingkat diciutkan ke dalam satu modul terpadu.
  - **Kontrak:** Standar visual editorial (bukan corporate dashboard), tinggi seragam ~320px, palette stone/slate, aksen merah untuk kebocoran dan hijau/indigo untuk modul dalam.
  - **Acceptance:** Template kode HTML/CSS/SVG dan Mermaid lengkap siap pakai untuk kelima pola.

- **Task 1.3: `resources/html-report-scaffold.md`**
  - **Starting State:** Scaffold dasar di `worked-example.md` lama.
  - **Operation:** Dokumentasikan arsitektur scaffold HTML hibrida lengkap:
    - CDN loading (Tailwind CSS 2.2.19 + Mermaid 11 ESM) dengan `onerror` fallback.
    - Embedded `<style>` fallback offline (.candidate-card, .badge, .diagram-panel, .seam, .leak, .deep).
    - Struktur layout: Header (legend tanpa paragraf pembuka panjang), Candidates list, dan Top Recommendation card.
    - Protokol penulisan ke `$TMPDIR` / `%TEMP%` (`architecture-survey-<timestamp>.html`) dan peluncuran ramah headless.
  - **Acceptance:** Scaffold HTML valid, 100% mandiri, mendukung offline browsing.

- **Task 1.4: `resources/subagent-exploration-brief.md`**
  - **Starting State:** Disebutkan sepintas dalam prosedur tanpa prompt terstruktur.
  - **Operation:** Buat template prompt penugasan subagent berkonteks segar:
    - Analisis churn via `git log --oneline` (50-100 commit terakhir).
    - Domain glossary intake (`GLOSSARY.md`) dan ADR settling (`docs/adr/`).
    - Panduan *organic friction walk*: pelacakan parameter pass-through, caller-side policy duplication, leaky seams.
    - Eksekusi *Deletion Test* pada setiap modul yang dicurigai dangkal.
    - Batasan proteksi: DILARANG mengedit kode produk atau melakukan refactoring selama survei.
  - **Acceptance:** Format brief siap salin/injeksi untuk subagent Claude Code / Codex.

- **Task 1.5: `resources/grilling-and-adr-protocols.md`**
  - **Starting State:** Disinggung dalam 3 kalimat di `SKILL.md` lama.
  - **Operation:** Definisikan protokol interaktif pasca-survei:
    - Aturan wawancara interaktif (*grilling loop*): validasi batasan, trade-off, dan tes yang bertahan.
    - Sinkronisasi malas `GLOSSARY.md` (buat atau perbarui istilah domain baru secara tepat waktu).
    - Protokol pencatatan ADR berdaya tahan: tawaran formal jika kandidat ditolak permanen (*"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"*).
    - Transisi bersih ke `andino-api-and-interface-design` / `deep-module-design` untuk spesifikasi interface.
  - **Acceptance:** Pohon keputusan wawancara, template dialog, dan kriteria pembuatan ADR terdokumentasi rapi.

- **Task 1.6: `resources/worked-example.md`**
  - **Starting State:** File lama 319 baris yang mencampuradukkan berbagai topik.
  - **Operation:** Refaktor menjadi studi kasus transformasi nyata yang ramping dan tajam:
    - Kasus Order Intake pipeline: Before (5 wrapper dangkal, duplikasi controller, transaksi bocor) vs After (`OrderIntake` modul dalam, 1 interface publik, repositori transaksional terisolasi).
    - Perbandingan visual berdampingan dan kartu preview terminal ASCII.
    - Demonstrasi pemenuhan invarian arsitektur dan evaluasi skor leverage.
  - **Acceptance:** Kode contoh valid TypeScript/Node, tanpa halusinasi sintaksis, mematuhi 10 kosakata kanonik.

---

### Task 2: Refactors Root Contracts (`SKILL.md`, `GUIDE.md`, `license.md`)

- **Task 2.1: `skills/architecture-survey/SKILL.md`**
  - **Starting State:** 165 baris teks naratif.
  - **Operation:** Tulis ulang sebagai kontrak operasional berdensitas tinggi ($<150$ baris, target 115-125 baris):
    - Frontmatter SDO (*trigger-only*, diawali `description: Use when surveying...`, tanpa ringkasan alur).
    - Section 1: Dominant Negative Gates (Cosmetic renames, whole-repo unbounded scans, dormant code refactoring, in-survey code editing).
    - Section 2: Tri-Mode Operational Triage Router (Mode A: Hotspot Churn-Driven, Mode B: Subsystem/Pain-Point Bounded, Mode C: Cross-Seam Leakage Investigation).
    - Section 3: The 5 Floor Invariants (The Deletion Test, Two-Adapter Rule, Locality over Fragmented Helpers, Interface as Test Surface, Zero In-Survey Refactoring).
    - Section 4: Anti-Rationalization Refutations Table (`| Rationalization Shortcut | Mechanical Reality & Required Response |`).
    - Section 5: Diagnostic Red Flags (Stop Immediately).
    - Section 6: Progressive Disclosure Router (menghubungkan ke `GUIDE.md` dan 6 modular resources).
    - Section 7: Runnable Operational Python Test Harness (evaluasi dictionary contract; exit 0 pada kondisi normal, exit 1 saat `ANDINO_NEGATIVE=1`).
    - Section 8: Provenance.
  - **Acceptance:** Line count $<150$, lolos regex SDO, Python harness lolos uji exit code 0 dan 1.

- **Task 2.2: `skills/architecture-survey/GUIDE.md`**
  - **Starting State:** Duplikasi dari `SKILL.md` lama.
  - **Operation:** Tulis ulang sebagai panduan craft mendalam:
    - Elaborasi filosofi modul dalam vs dangkal (John Ousterhout / Matt Pocock).
    - Prosedur 6 tahap dari penentuan skop, friction walk, penyusunan proposal, visual report, grilling loop, hingga pencatatan ke plan.
    - Standar kualitas laporan dan integrasi ekosistem Andino.
  - **Acceptance:** Dokumen mendalam, bebas emoji dekoratif, link lokal 100% valid.

- **Task 2.3: `skills/architecture-survey/references/license.md`**
  - **Starting State:** Lisensi Matt Pocock 2026.
  - **Operation:** Verifikasi dan pastikan tautan sumber upstream `https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture` tetap presisi.
  - **Acceptance:** Format konsisten dengan 29 skill lainnya di portofolio.

---

### Task 3: Author Deterministic Offline Verifier `scripts/verify_architecture_survey_elevation.py`

- **Operation:** Buat skrip pengujian offline mandiri menggunakan Python standard library murni:
  1. `test_line_count`: Memastikan `SKILL.md` $<150$ baris.
  2. `test_sdo_frontmatter`: Memvalidasi deskripsi diawali "Use when", panjang $<1024$ karakter, tanpa kebocoran alur kerja.
  3. `test_operational_python_harness`: Ekstraksi blok python dan eksekusi subprocess (`ANDINO_NEGATIVE=0` lolos, `ANDINO_NEGATIVE=1` exit 1).
  4. `test_modular_resources_and_link_integrity`: Memastikan keberadaan ke-6 file di `resources/` dan memvalidasi nol tautan relatif rusak (*zero dead links*).
  5. `test_emoji_cleanliness`: Memastikan nol emoji dekoratif di seluruh file markdown.
  6. `test_setup_installer_compatibility`: Simulasi instalasi atomik ke 5 target host (`claude`, `codex`, `opencode`, `antigravity-cli`, `antigravity-ide`) dengan integritas SHA-256 byte-for-byte.
- **Acceptance:** Skrip lolos 100% dengan eksekusi $<0.5$ detik.

---

### Task 4: Ecosystem Integration & Portfolio Verification

- **Task 4.1: Pembaruan `references/legal/provenance.md`**
  - Catat rekaman elevasi tanggal 2026-11-02 untuk `architecture-survey` yang mensintesis keunggulan visual dan batasan Matt Pocock dengan tata kelola Andino Workflow.
- **Task 4.2: Verifikasi Portofolio Global**
  - Jalankan `python -I scripts/verify_portfolio.py` untuk memastikan seluruh orakel portofolio (rute publik, link lokal, manifest) berstatus hijau.
- **Task 4.3: Sinkronisasi Host Runtime `ai-rules setup`**
  - Sinkronisasikan berkas yang telah dielevasi ke host discovery roots aktif:
    - `~/.claude/skills/andino-workflow/skills/architecture-survey/`
    - `~/.claude/skills/andino-architecture-survey/`

---

### Task 5: Verification & Quality Assurance
- Jalankan verifier spesifik: `python -I scripts/verify_architecture_survey_elevation.py`.
- Jalankan verifier portofolio: `python -I scripts/verify_portfolio.py`.
- Lakukan inspeksi diff git: `rtk git status` dan `rtk git diff`.

---

### Task 6: Atomic Git Delivery
- Git add file yang berubah.
- Git commit dengan pesan konvensional:
  `feat(skills): elevate architecture-survey with visual before/after patterns, strict vocabulary, modular resources, and offline verifier`
- Git push ke `origin/andino-workflow`.

---

## 4. Execution Board & Dependency Graph

```
[Task 1: 6 Modular Resources] ────► [Task 2: SKILL.md & GUIDE.md]
                                            │
                                            ▼
[Task 3: Deterministic Verifier] ◄──────────┘
             │
             ▼
[Task 4: Provenance & Setup Sync]
             │
             ▼
[Task 5: Complete Verification]
             │
             ▼
[Task 6: Atomic Commit & Push]
```

- **Task 1** dapat diimplementasikan secara paralel atau berurutan karena saling modular.
- **Task 2** bergantung pada selesainya Task 1 agar router link valid.
- **Task 3** menguji Task 1 dan 2.
- **Task 4, 5, 6** adalah fase integrasi akhir dan pengiriman.

---

## 5. Verification & Delivery Invariants

1. **Line Budget Invariant:** `skills/architecture-survey/SKILL.md` strictly $<150$ lines.
2. **SDO Invariant:** Deskripsi frontmatter hanya berisi kondisi pemicu ("Use when..."), tidak merangkum alur kerja.
3. **Zero Dead Links:** Seluruh link relatif markdown terhubung ke file dan heading yang nyata.
4. **Offline Resilience:** Report HTML dapat dirender secara mandiri saat offline tanpa koneksi CDN.
5. **Zero Breaking Changes to Portfolio:** `python -I scripts/verify_portfolio.py` tetap berstatus 100% OK.
6. **Clean Shell RTK Rule:** Seluruh perintah terminal dijalankan dengan prefix `rtk`.

---

## 6. Concrete Next Action

Aktifkan skill `andino-plan-execution` untuk memulai **Task 1: Implements Modular Resources in `skills/architecture-survey/resources/`**.
