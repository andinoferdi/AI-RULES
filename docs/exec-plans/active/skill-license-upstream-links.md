# Execution Plan: Menambahkan Link Upstream Asli ke Setiap skills/*/references/license.md

**Target:** `skills/*/references/license.md` (30 active skills)  
**Status:** DONE  
**Phase:** 6 - Integration & Verification Complete  
**Governing Protocol:** `andino-delegation` under Andino Workflow governance  
**Next Action:** Commit and deliver update to user.

---

## 1. Context & Objectives

Seluruh 30 skill di bawah `skills/` telah memiliki file lisensi di `skills/<skill_name>/references/license.md`. Namun saat ini, file tersebut hanya memuat teks notice lisensi MIT dan nama author tanpa menyertakan tautan/URL langsung ke repositori sumber aslinya (upstream).

Tujuan eksekusi ini:
1. Memperbarui seluruh 30 file `license.md` agar secara eksplisit menyertakan tautan upstream asli yang dapat langsung diklik di GitHub.
2. Membagi eksekusi menjadi 3 batch independen dengan kepemilikan write terpisah ($W(A) \cap W(B) = \emptyset$).
3. Menggunakan protokol `andino-delegation` dengan dispatch paralel (maksimal 3 subagent langsung) dan pemilihan model adaptif yang efisien.
4. Memverifikasi seluruh tautan dan integritas repositori menggunakan `scripts/verify_portfolio.py`.

---

## 2. Work Breakdown & Task Allocation

### Task 1: Update Batch 1 (A-C) Skills License Links
- **Scope:** 10 skills (`skills/agent-document-authoring` s.d. `skills/constraint-driven-development`)
- **Files to Modify:**
  - `skills/agent-document-authoring/references/license.md`
  - `skills/api-and-interface-design/references/license.md`
  - `skills/architecture-survey/references/license.md`
  - `skills/article-shaping/references/license.md`
  - `skills/brainstorming/references/license.md`
  - `skills/browser-testing-with-devtools/references/license.md`
  - `skills/ci-cd-and-automation/references/license.md`
  - `skills/code-review/references/license.md`
  - `skills/code-simplification/references/license.md`
  - `skills/constraint-driven-development/references/license.md`

### Task 2: Update Batch 2 (D-L) Skills License Links
- **Scope:** 10 skills (`skills/debugging` s.d. `skills/learning-workspace`)
- **Files to Modify:**
  - `skills/debugging/references/license.md`
  - `skills/delegation/references/license.md`
  - `skills/deprecation-and-migration/references/license.md`
  - `skills/documentation-and-adrs/references/license.md`
  - `skills/doubt-driven-development/references/license.md`
  - `skills/git-skills/references/license.md`
  - `skills/handoff/references/license.md`
  - `skills/human-procedure/references/license.md`
  - `skills/issue-triage/references/license.md`
  - `skills/learning-workspace/references/license.md`

### Task 3: Update Batch 3 (O-V) Skills License Links
- **Scope:** 10 skills (`skills/observability-and-instrumentation` s.d. `skills/verification`)
- **Files to Modify:**
  - `skills/observability-and-instrumentation/references/license.md`
  - `skills/performance-optimization/references/license.md`
  - `skills/plan-execution/references/license.md`
  - `skills/planning/references/license.md`
  - `skills/security-and-hardening/references/license.md`
  - `skills/session-diagnostics/references/license.md`
  - `skills/shipping-and-launch/references/license.md`
  - `skills/skill-maker/references/license.md`
  - `skills/tdd/references/license.md`
  - `skills/verification/references/license.md`

---

## 3. Acceptance Criteria & Verification
- Seluruh 30 file `license.md` memiliki format bersih dengan link upstream asli.
- Teks lisensi MIT dan copyright notice tetap utuh tanpa korupsi.
- `python scripts/verify_portfolio.py` lulus 100% (semua 6 pengujian lolos tanpa broken local links).
