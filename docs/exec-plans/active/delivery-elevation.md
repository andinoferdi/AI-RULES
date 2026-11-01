# Execution Plan: Elevasi skills/delivery (Andino Workflow)

**Target:** `skills/delivery`  
**Internal Method ID:** `andino-delivery` (alias: `delivery`, resolves alias: `finishing-a-development-branch`)  
**Status:** DONE  
**Phase:** Phase 5 — Verification & Delivery Complete  
**Reference Benchmark:** `obra/superpowers:skills/finishing-a-development-branch`  
**Governing Protocol:** Andino Workflow (Single durable checkpoint, proportional investigation, floor invariants)  
**Next Action:** Commit atomik dan push ke origin/andino-workflow.

---

## 1. Executive Snapshot & Context

Kualitas output dan keefektifan AI pada `skills/delivery` saat ini tertinggal jauh dibandingkan `obra/superpowers:skills/finishing-a-development-branch`. Analisis mendalam bersama Council mengungkap tiga penyebab fundamental:
1. **Birokrasi Meta-Governance yang Abstrak:** Dokumen lama terbebani oleh terminologi tata kelola kaku (*uncommitted candidate*, *authority boundary*, *NOT_VERIFIED*) tanpa algoritma mekanis Git yang konkret. AI menjadi pasif dan tidak mengeksekusi integrasi secara presisi.
2. **Ketiadaan Prosedur Mekanis Kunci Obra:**
   - **Verifikasi Suite Tes Mutlak:** Hard stop jika tes gagal; menu hanya disajikan setelah tes hijau.
   - **Deteksi Mekanis Lingkungan Git:** Menggunakan `git rev-parse --git-dir` vs `--git-common-dir` untuk membedakan normal repo, named worktree, dan detached HEAD.
   - **Menu Pilihan Baku Terkunci:** Pilihan 1-2-3 (Merge locally, Push & PR, Keep as-is; Discard hanya jika diminta eksplisit).
   - **Proteksi Workspace & Untracked Files:** Larangan mutlak `--force` pada worktree yang memuat file uncommitted/untracked.
   - **Tabel Anti-Rasionalisasi:** Menutup celah rasionalisasi model (mengasumsikan tes tadi sudah cukup, berasumsi user ingin merge, menebak base branch adalah `main`).
3. **Ketidakkonsistenan Layout dengan Standar Elevasi Andino Workflow:**
   - Belum mengadopsi struktur *elevated skills* (`andino-delegation`, `andino-skill-maker`, `andino-debugging`): kontrak operasional root `<150 baris`, frontmatter SDO trigger-only, 5 floor invariants, diagnostic red flags, harness Python deterministik, dan progressive disclosure router ke modular `resources/`.

### Keunggulan Tambahan Melampaui Obra (Putusan Council)
- **Dual-Mode UI/CLI:** Menggunakan antarmuka interaktif `AskUserQuestion` di Claude Code dan fallback teks toleran di CLI polos/headless.
- **Atomic Rollback pada Merge:** Menyediakan protokol `git merge --abort` jika pasca-merge tes gagal atau terjadi konflik.
- **Sinergi Sibling Skills:** Integrasi pembuatan PR dengan `andino-pr-description` untuk ringkasan dampak dan reversibilitas.
- **Kompatibilitas Windows & Multi-Host:** Deteksi path Windows yang aman terhadap file locking dan integrasi installer `ai-rules setup`.

---

## 2. Architecture & File Breakdown

```
skills/delivery/
├── SKILL.md                                        # Kontrak operasional utama (<150 baris, target ~115 baris)
├── GUIDE.md                                        # Panduan komprehensif alur delivery untuk agen & pengguna
└── resources/
    ├── contract.md                                 # Kontrak data handoff, skema status, dan batasan mutasi
    ├── environment-and-worktree-detection.md       # Deteksi mekanis git-dir, common-dir, worktree path, Windows
    ├── pre-integration-verification.md             # Protokol suite tes proyek, clean working tree gate, stop rule
    ├── integration-menu-and-execution.md           # Dual-mode menu, local merge + abort rollback, push/PR, discard
    ├── workspace-cleanup-and-safety.md             # Worktree ownership removal, porcelain status check, stale prune
    └── anti-rationalization-and-failure-modes.md   # Matriks dalih vs realitas mekanis & diagnostic red flags

scripts/
└── verify_delivery_elevation.py                    # Verifier offline deterministik (<0.2 detik)
```

---

## 3. Detailed Change Specifications

### Task 1: Implement Modular Resources in `skills/delivery/resources/`
- **Resource 1: `contract.md`**
  - Skema data `HandoffLedger` (candidate SHA, base branch, verification status, permissions, residuals, next action).
  - Matriks perizinan eksplisit: verifikasi lolos tidak memberi hak mutasi; commit/push/merge butuh mandat terpisah.
- **Resource 2: `environment-and-worktree-detection.md`**
  - Perintah presisi: `git rev-parse --git-dir`, `git rev-parse --git-common-dir`, `git rev-parse --show-toplevel`.
  - Matriks 3 kondisi: Normal Repo (`GIT_DIR == GIT_COMMON`), Named-branch Worktree (`GIT_DIR != GIT_COMMON`), Detached HEAD.
  - Normalisasi path untuk lingkungan Windows / Git Bash.
- **Resource 3: `pre-integration-verification.md`**
  - Deteksi runner tes otomatis (`npm test`, `pytest`, `cargo test`, `go test ./...`).
  - Aturan *Hard Stop*: Jika tes gagal, laporkan kegagalan dan BERHENTI. Tidak ada menu sebelum hijau.
  - Aturan *Clean Tree*: Working tree harus bersih dari modifikasi fungsional sebelum integrasi.
- **Resource 4: `integration-menu-and-execution.md`**
  - Spesifikasi Dual-Mode Menu: `AskUserQuestion` interaktif di Claude Code vs format teks baku di terminal CLI.
  - Opsi 1 (Merge Locally): pindah ke main repo root, checkout base, pull, merge feature branch, verifikasi tes hasil merge. Jika gagal, eksekusi `git merge --abort` dan amankan branch.
  - Opsi 2 (Push & Create PR): push branch, trigger `gh pr create` / forge URL, integrasi format `andino-pr-description`.
  - Opsi 3 (Keep As-Is): pertahankan branch dan worktree.
  - Prosedur Discard: hanya jika diminta eksplisit dengan mengetik kata `discard`.
- **Resource 5: `workspace-cleanup-and-safety.md`**
  - Kepemilikan worktree: bersihkan hanya jika berada di bawah `.worktrees/` atau `worktrees/`. Host workspace ditinggalkan.
  - Proteksi penolakan removal (`git status --porcelain -uall`): tampilkan file uncommitted, berikan 3 pilihan aman.
  - Penanganan file lock di Windows: fallback pesan instruksi manual tanpa data loss.
- **Resource 6: `anti-rationalization-and-failure-modes.md`**
  - Tabel 10 alasan rasionalisasi model vs realitas mekanis.
  - 6 Diagnostic Red Flags (Stop and investigate immediately).

### Task 2: Elevate `skills/delivery/SKILL.md` (<150 baris)
- Frontmatter SDO trigger-only (`name: andino-delivery`, `description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work or handle branch completion. Operates under Andino Workflow governance.`).
- 1. Dominant Negative Gates (kapan menolak delivery).
- 2. Operational Triage Router (Lingkungan & Mode UI).
- 3. 6-Phase Gated Lifecycle (Verify -> Detect -> Confirm Base -> Present Menu -> Execute & Test -> Workspace Cleanup).
- 4. 5 Floor Invariants (Strict Green Suite, Human Integration Authority, Non-Negotiable Menu, Discard Protection, Atomic Merge Rollback).
- 5. Anti-Rationalization Refutations Table.
- 6. Diagnostic Red Flags.
- 7. Progressive Disclosure Router.
- 8. Runnable Deterministic Python Harness (`ANDINO_NEGATIVE=0` exit 0, `ANDINO_NEGATIVE=1` exit 1).
- 9. Provenance.

### Task 3: Elevate `skills/delivery/GUIDE.md`
- Panduan lengkap naratif yang menguraikan seluruh siklus delivery, dual-mode UI, skenario kegagalan, dan checklist verifikasi akhir.

### Task 4: Create Deterministic Offline Verifier `scripts/verify_delivery_elevation.py`
- Menguji secara offline dan deterministik (<0.2 detik):
  1. Kuota baris `SKILL.md` (<150 baris).
  2. Frontmatter SDO (trigger-only, tidak ada kebocoran alur kerja).
  3. Python operational harness (`ANDINO_NEGATIVE=0` exit 0, `ANDINO_NEGATIVE=1` exit 1).
  4. Integritas seluruh 6 modular resources dan 100% link resolution.
  5. Ketiadaan emoji dekoratif.
  6. Kompatibilitas installer `ai-rules setup` (`_is_valid_skill_tree` dan simulasi copy ke 5 host).

### Task 5: Execute Verifier and Verify 100% Pass
- Menjalankan `python scripts/verify_delivery_elevation.py`.

### Task 6: Sync to Runtime Host Targets
- Sinkronisasi perubahan ke:
  - `~/.claude/skills/andino-workflow/skills/delivery`
  - `~/.claude/skills/finishing-a-development-branch` (verifikasi keterhubungan)

### Task 7: Git Commit & Push
- Git commit atomik dengan pesan terstruktur.
- Push ke remote branch `origin/andino-workflow`.

---

## 4. Verification & Acceptance Criteria
- [x] `skills/delivery/SKILL.md` strictly < 150 baris (Actual: 112 lines).
- [x] Semua 6 modular resources terpasang di `skills/delivery/resources/`.
- [x] `skills/delivery/GUIDE.md` komprehensif terpasang.
- [x] `scripts/verify_delivery_elevation.py` berjalan sukses (exit 0) dalam < 0.2 detik (6/6 suites pass).
- [x] Berkas tersinkronisasi sempurna di host lokal runtime Claude Code (`~/.claude/skills/andino-delivery` dan `~/.claude/skills/andino-workflow/skills/delivery`).
- [x] Git commit dan push berhasil dieksekusi ke remote `origin/andino-workflow` (Commit: `fee74df`).
