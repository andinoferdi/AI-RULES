# Project Markdown Alignment — on demand

Jalankan saat memasang rules ke project baru, stack/wiring berubah material, atau diminta user.
Target: [DIRECTORY RULES / PROJECT]. Scope: instruction, rule dan template terkait.

1. Periksa instruction aktif, manifest/config, command verifikasi dan struktur minimum.
2. Inventarisasi template/path; bedakan CONFIRMED, INFERRED dan UNKNOWN. Jangan mengisi
   fakta project dari contoh. Preserve dokumen produk/requirement yang sudah disetujui.
3. Jadikan satu core sebagai sumber rules. Wire AGENTS.md, CLAUDE.md, GEMINI.md atau
   config host sesuai dokumentasi versi yang terpasang. Jangan membuat empat rules berbeda.
4. Sesuaikan path/command berdasarkan bukti. Audit seluruh project-copy rules yang
   relevan, termasuk domain, code, Git, PRD/SRS/BRD dan contoh bahasa. Setelah
   alignment, file tersebut tetap lazy-loaded saat relevan. Bootstrap sekali; task
   prompt tipis; resume menggunakan execution plan.
5. Pertahankan UI/UX-Taste policy yang diterima. Jangan menimpa design tokens atau source
   code bisnis untuk merapikan Markdown. Backup config user di luar Git; jangan salin secrets.
6. Verifikasi link, casing path, discovery adapter dan command yang dicatat. Laporkan
   UPDATED, CHECKED, UNKNOWN atau NOT ACTIVE hanya untuk perubahan/ketidakpastian material.

Tidak ada commit, push, publish atau perubahan service eksternal tanpa otorisasi terkait.
Jangan menjalankan alignment pada ticket biasa atau membaca semua source secara rekursif.

## Project copy versus reusable master

- Master reusable template adalah sumber generik. Jangan memasukkan fakta project ke
  master tersebut.
- Target alignment adalah salinan rules di dalam project, biasanya
  `<PROJECT_SCOPE>/docs/ai-rules/`, beserta thin instruction core pada scope tersebut.
- Jika user memberi path project-copy, verifikasi path itu dan deteksi Git root serta
  project/package scope. Jangan menggantinya dengan path contoh.
- Pada monorepo, jangan menerapkan asumsi satu package ke seluruh repository tanpa evidence.
- Gunakan referensi relatif dari instruction core ke project-copy bila keduanya berada
  dalam repository yang sama; jangan membuat wiring absolut lintas repository sebagai jalan pintas.

## Content alignment contract

**LAZY LOADING IS NOT ALIGNMENT EXEMPTION.** Selama Project Markdown Alignment,
inventarisasi dan audit setiap project-copy rule yang relevan. "Lazy" hanya berarti
file tidak dimuat pada setiap runtime task setelah alignment; bukan berarti file
dilewati saat alignment.

Untuk setiap file yang relevan:

1. Baca current project-copy content dan evidence repository yang diperlukan.
2. Sesuaikan fakta generik yang dapat dibuktikan, seperti stack/version, struktur,
   package manager, lint/typecheck/build/test command, aliases dan conventions.
3. Gunakan salah satu status: `UPDATED`, `CHECKED`, `NOT ACTIVE`, atau `UNKNOWN`.
4. Jika tidak berubah, jelaskan evidence spesifiknya; jangan sekadar menyebut file lazy.

Minimal periksa bila tersedia: `fe-rules.md`, `be-rules.md`, `code-rules.md`,
`git-workflow.md`, `git-naming.md`, `git-branch-tips.md`, `prd.md`, dan `srs.md`.
Inventarisasi file material lain di directory rules tanpa melakukan recursive source audit besar.

`AGENTS.md` tetap thin persistent core/router. Ia harus menunjuk ke project-copy yang
sudah diaudit, bukan menjadi satu-satunya file yang diubah. Preserve requirement
authoritative; jangan mengarang persona, KPI, feature scope, atau stakeholder needs
untuk mengisi PRD/SRS.

Laporan akhir harus berupa matrix `File | Status | Evidence | Change` agar terlihat
jelas file mana yang diubah, diperiksa, tidak aktif, atau masih tidak diketahui.
