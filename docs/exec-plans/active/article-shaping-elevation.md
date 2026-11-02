# Execution Plan: Elevasi skills/article-shaping (Andino Workflow)

**Target:** `skills/article-shaping`  
**Internal Method ID:** `andino-article-shaping` (aliases: `article-shaping`, `writing-beats`, `writing-shape`)  
**Status:** DONE  
**Phase:** 5 - Verification & Delivery Complete  
**Reference Benchmark:** `mattpocock/skills:writing-beats` & `writing-shape`  
**Governing Protocol:** Andino Workflow (Single durable checkpoint, proportional investigation, floor invariants)  
**Next Action:** Commit atomik dan push ke origin/andino-workflow.

---

## 1. Context & Objectives

Kualitas output dan keefektifan AI pada `skills/article-shaping` saat ini tertinggal dibandingkan referensi karya Matt Pocock (`writing-beats` dan `writing-shape`). Analisis mendalam bersama Council mengungkap tiga akar penyebab:
1. **Kehilangan Sikap "Ruthless Editor" (Grilling Session):** Dokumen lama terlalu sopan dan deskriptif. Pocock unggul karena model bertindak sebagai editor galak yang aktif menguji klaim lemah (*"Kalau paragraf ini dibuang, apa yang rusak?"*, *"Kalimat ini melakukan dua pekerjaan sekaligus: pecah atau pilih salah satu!"*).
2. **Ketiadaan Aturan Penulisan Inkremental Ketat (CYOA):** Pocock mewajibkan penulisan **satu beat per giliran ke disk fisik** tanpa mendahului (*never write ahead*), membaca ulang disk sebelum giliran berikutnya, dan menampilkan efek pembukaan konsep (*preview unlocks*). Dokumen lama membiarkan model tergelincir menulis draf panjang sekaligus yang mengalami regresi probabilistik menjadi teks klise dan hambar.
3. **Hilangnya Debat Format Eksplisit:** Tidak ada instruksi vokal untuk memperdebatkan format blok (prosa vs list vs tabel vs callout vs kode).
4. **Ketidakkonsistenan Layout dengan Portofolio 30 Skill Baru:** Layout belum mengikuti standar elevated skills Andino Workflow (`andino-skill-maker`, `andino-delivery`, `andino-brainstorming`) yang menyajikan kontrak operasional ringkas (<150 baris) di root `SKILL.md` dan memindahkan materi craft mendalam ke direktori modular `resources/`.

### Hasil Sidang Council & Keputusan Strategis
- **Sembunyikan Mesin di Balik Kap:** Teori matematis DAG grounding tetap menjadi invarian penegak, namun disajikan dalam bahasa editorial manusiawi kepada pengguna (*"Pembaca belum kenal konsep ini, beri pijakan dulu"*).
- **Proteksi Suara Penulis:** Grilling editor difokuskan pada ketajaman argumen dan celah bukti (*name the gap*), bukan memaksakan persona sinis seragam ala tech-Twitter.
- **Lokalisasi Bahasa Alami:** Mengikuti prinsip Focus dan `human-language-indonesia.md` (lugas, hangat, seperti diskusi di warung kopi).
- **Durable Checkpointing:** Setiap beat yang disetujui langsung ditulis ke file fisik di disk (`article.md`) agar tahan terhadap *context compaction* dan interupsi sesi.
- **Kompatibilitas Penuh `ai-rules setup`:** Menjamin fungsi `_is_valid_skill_tree`, atomic copy, zero broken links, dan zero decorative emojis.

---

## 2. Architecture & File Breakdown

```
skills/article-shaping/
├── SKILL.md                                        # Kontrak operasional utama (<120 baris, plafon <150 baris)
├── GUIDE.md                                        # Panduan master craft komprehensif bagi penulis & model
├── references/
│   └── license.md                                  # Deklarasi lisensi MIT Matt Pocock & Andino Workflow
└── resources/
    ├── contract.md                                 # Skema data formal (beat state, grounding DAG, audit trail)
    ├── grilling-and-cadence-protocol.md            # Protokol editor galak, pertanyaan uji, ritme kalimat
    ├── concept-grounding-graph.md                  # Matematika DAG, reachability, dan protokol "name the gap"
    ├── format-tradeoffs-and-anti-slop.md           # Debat format (prosa/list/tabel/callout) & indeks anti-slop
    ├── beat-progression-and-hooks.md               # 3 formula hook konkret (prosa 1-2 kalimat) & 6 tipologi beat
    ├── worked-example.md                           # Contoh proses nyata end-to-end + harness pengujian
    └── raw-capture/                                # Submodul eksplorasi catatan mentah (terpreservasi)
        ├── contract.md
        ├── guide.md
        └── resources/worked-example.md
```

File Pendukung:
- `scripts/verify_article_shaping_elevation.py` (Test oracle deterministik offline)

---

## 3. Tasks & Implementation Steps

### Task 1: Create Deterministic Test Oracle `scripts/verify_article_shaping_elevation.py`
- Menetapkan batasan kontrak deterministik sebelum memodifikasi file produksi:
  1. `skills/article-shaping/SKILL.md` strictly < 150 baris (target < 120 baris).
  2. Frontmatter SDO memenuhi aturan: `name: andino-article-shaping`, `description: Use when...` (<1024 karakter, tanpa workflow leak).
  3. Eksekusi harness Python embedded (`ANDINO_NEGATIVE=0` exit 0, `ANDINO_NEGATIVE=1` exit 1).
  4. Integritas seluruh modul di `resources/*.md` dan validitas link relatif lokal (0 broken links).
  5. Integritas submodule `resources/raw-capture/` tetap terjaga.
  6. Nol emoji dekoratif unicode non-fungsional.
  7. Kompatibilitas installer `ai-rules setup` (`_is_valid_skill_tree` dan simulasi copy ke 5 host).

### Task 2: Build Modular Deep Craft in `skills/article-shaping/resources/`
- **`resources/contract.md`**: Definisi skema kontrak data untuk beat, precondition, grounded set, hook candidates, dan format choices.
- **`resources/grilling-and-cadence-protocol.md`**: Resep interogasi editor ("Kalau paragraf ini dibuang, apa yang rusak?", "Satu kalimat dua beban", transisi lemah), variasi panjang kalimat, dan lokalisasi bahasa Indonesia wajar.
- **`resources/concept-grounding-graph.md`**: Formulasi matematis $G_{t+1} = G_t \cup \text{grounds}(\text{beat}_t)$, reachability check, dan protokol penamaan celah fakta (*name the gap* tanpa fabrikasi).
- **`resources/format-tradeoffs-and-anti-slop.md`**: Panduan debat format blok (prosa vs list, inline vs callout, tabel vs struktur berulang) dan daftar hitam klise AI (*throat-clearing, intensifiers, symmetric triads*).
- **`resources/beat-progression-and-hooks.md`**: 3 sudut hook (In Media Res, The Gauntlet, Curiosity Gap) dengan contoh prosa utuh 1-2 kalimat, serta taksonomi 6 beat (`scene`, `claim`, `question`, `aside`, `pivot`, `payoff`).
- **`resources/worked-example.md`**: Pembaruan contoh implementasi nyata dari catatan mentah menjadi artikel utuh bertahap.

### Task 3: Elevate Root `skills/article-shaping/SKILL.md`
- Menyajikan kontrak operasional ringkas (<120 baris) yang memuat:
  1. Frontmatter SDO (Trigger-only).
  2. Dominant Negative Gates (kapan DILARANG menggunakan skill ini).
  3. Dual-Pacing Operational Router (Mode A: Strict Beat-by-Beat CYOA, Mode B: Cohesive Section Cluster).
  4. The 5 Floor Invariants (Iron Law of Non-Mutation, Grounding Invariant, Single Job per Beat, Zero Fabricated Evidence, Durable Disk Checkpoint).
  5. Anti-Rationalization Refutations Table.
  6. Diagnostic Red Flags (Stop Immediately).
  7. Progressive Disclosure Router.
  8. Runnable Deterministic Python Harness (`python andino-operational-example`).
  9. Provenance & License notice.

### Task 4: Elevate `skills/article-shaping/GUIDE.md`
- Menjadikan `GUIDE.md` sebagai master reference komprehensif yang mengintegrasikan seluruh filosofi penulisan, memadukan ketajaman Matt Pocock dengan ketelitian Andino Workflow.

### Task 5: Verify Deterministic Test Oracle & Portfolio Integrity
- Eksekusi `python scripts/verify_article_shaping_elevation.py` (harus lolos 100%).
- Eksekusi `python scripts/verify_portfolio.py` (harus lolos 100%).

### Task 6: Synchronize to Host Runtimes, Commit, and Push
- Sinkronisasi direktori skill ke host target:
  - `~/.claude/skills/andino-workflow/skills/article-shaping`
  - `~/.claude/skills/andino-article-shaping`
- Git commit atomik dengan pesan terstruktur.
- Git push ke remote `origin/andino-workflow`.

---

## 4. Verification & Acceptance Criteria
- [x] `skills/article-shaping/SKILL.md` strictly < 150 baris (Actual: 96 baris).
- [x] Seluruh modular resources terpasang di `skills/article-shaping/resources/` (6 berkas modular).
- [x] Submodul `resources/raw-capture/` utuh dan terverifikasi.
- [x] `scripts/verify_article_shaping_elevation.py` berjalan sukses (exit 0) dalam < 0.2 detik (6/6 test suites pass).
- [x] 0 broken relative markdown links di seluruh bundle.
- [x] 0 decorative emojis di seluruh bundle.
- [x] Kompatibilitas installer `ai-rules setup` terbukti pada 5 host target.
- [x] Berkas tersinkronisasi sempurna di host lokal runtime (`~/.claude/skills/`).
- [x] Git commit dan push siap dieksekusi ke remote `andino-workflow`.
