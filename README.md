# Andino-Workflow

Andino-Workflow adalah workflow router dan execution-plan manager untuk Codex, Claude Code, OpenCode, dan Antigravity.

Keempat agent diperlakukan sebagai **peer primary-capable agents**. Agent yang sedang dipakai menjadi primary untuk sesi tersebut. Repository dan konfigurasi aktual tetap menjadi sumber kebenaran.

## Cara kerja

| Bagian | Fungsi |
| --- | --- |
| Project rules | Aturan dan convention repository. |
| Execution plan | State ticket lintas sesi: tujuan, progress, evidence, phase, dan `NEXT ACTION`. |
| Andino-Workflow | Memilih workflow/skill minimum yang relevan dan menjaga lifecycle plan. |
| Skills | Metodologi atau worker spesialis. |
| Tools / MCP | Instrumen untuk menjalankan pekerjaan. |
| Memory / graph | Accelerator konteks opsional, bukan syarat handoff. |

### Workflow mengikuti ukuran task

| Kelas | Contoh | Alur |
| --- | --- | --- |
| **SIMPLE** | Typo, rename, edit kecil | Pahami → edit → verifikasi. Plan biasanya tidak perlu. |
| **STANDARD** | Fitur lokal, bug jelas, refactor terbatas | Ambil konteks relevan → implementasi → verifikasi. Gunakan plan untuk ticket non-trivial. |
| **COMPLEX** | Root cause belum jelas, migrasi, arsitektur, perubahan lintas sistem | Investigasi → plan → implementasi bertahap → verifikasi → checkpoint. |

Execution plan memiliki tiga tingkat detail:

- **LITE** — checkpoint kecil yang tetap membutuhkan plan.
- **STANDARD** — default untuk ticket non-trivial.
- **DEEP** — untuk task kompleks ketika detail tambahan benar-benar mengurangi risiko, ambiguity, atau biaya handoff.

Plan depth bukan workflow baru. Task tidak otomatis menjadi DEEP hanya karena prompt panjang atau file yang disentuh banyak.

Andino tidak wajib menjalankan `using-superpowers`, seluruh skill, graph, memory, MCP, atau subagent. Gunakan capability minimum yang memang membantu task.

## Instalasi Andino-Workflow

Sumber kanonis berada di [`skills/andino-workflow`](skills/andino-workflow/SKILL.md). Salinan terpasang dibaca dari lokasi discovery masing-masing host.

| Agent | Lokasi relatif terhadap home | Pemanggilan |
| --- | --- | --- |
| Codex | `.agents/skills/andino-workflow/` | `$andino-workflow` |
| Claude Code | `.claude/skills/andino-workflow/` | `/andino-workflow` |
| OpenCode | `.config/opencode/skills/andino-workflow/` | Native skill tool / command adapter |
| Antigravity | `.gemini/config/skills/andino-workflow/` | Gunakan skill `andino-workflow` |

Sinkronkan dari root repository:

```powershell
python -X utf8 scripts/sync-workflow.py
python -X utf8 scripts/sync-workflow.py --check
```

Script hanya menyinkronkan Andino beserta referensinya. Ia tidak memasang aplikasi agent, MCP, plugin, atau worker lain. Edit sumber kanonis, lalu sinkronkan. Jangan memelihara empat versi secara manual.

## Setup project baru

### 1. Salin project rules

Salin template yang relevan dari `put-in-your-projects` ke project, misalnya:

```text
your-project/
  AGENTS.md
  docs/
    ai-rules/
```

Project rules dan execution plan hidup di repository pekerjaan. Skill Andino tetap berada di lokasi global agent.

### 2. Jalankan Project Markdown Alignment

Gunakan [`Project Markdown Alignment Prompt.md`](<Project Markdown Alignment Prompt.md>) saat:

- memasang rules ke project baru,
- stack atau wiring berubah material,
- atau alignment memang diminta.

Alignment harus menyesuaikan **project-copy rules** berdasarkan evidence repository. Jangan mengisi PRD/SRS dengan requirement yang tidak diketahui, dan jangan mengubah master template dengan fakta project tertentu.

### 3. Bootstrap hanya jika perlu

Jika agent belum memahami stack, struktur, rules, dan command utama, jalankan [`First-prompt`](<put-in-your-projects/1. First-prompt.md>).

```text
Baca dan jalankan docs/ai-rules/1. First-prompt.md.

Pahami project rules, stack, struktur utama, serta command development
Dan verification yang tersedia. Ambil konteks minimum yang diperlukan.
Jangan mengulang alignment atau mengaudit seluruh repository.
Belum ada permintaan implementasi fitur.
```

Jika alignment pada sesi yang sama sudah memberi konteks cukup, lewati bootstrap.

Urutan normal:

```text
alignment sekali
→ bootstrap bila perlu
→ task
→ resume dari execution plan bila terputus
```

## Menjalankan task

### Task sederhana

Tidak perlu memanggil Andino jika task memang kecil.

```text
Ganti teks tombol Login menjadi Masuk.
```

Expected: edit lokal dan verifikasi terarah. Tidak perlu plan, memory, graph, browser, atau subagent tanpa alasan nyata.

### Ticket non-trivial

Contoh di Codex:

```text
$andino-workflow

Buat CRUD user mengikuti stack dan pola repository ini.

Kebutuhan:
- daftar user dengan pencarian dan pagination,
- detail, tambah, edit, dan hapus user,
- nama, email unik, dan status aktif,
- hanya admin yang boleh mengelola user,
- UI memiliki loading, empty, error, dan success state.

Gunakan autentikasi dan komponen yang sudah ada.
Buat/update docs/exec-plans/active/USER-CRUD.md.
Implementasikan lalu verifikasi acceptance criteria dan akses non-admin.
```

Di Claude Code gunakan `/andino-workflow`. Di host lain gunakan mekanisme skill yang tersedia.

## Execution plan

Simpan plan di repository pekerjaan:

```text
your-project/
  docs/
    exec-plans/
      active/
        TICKET-001.md
      completed/
```

Gunakan [`execution-plan-template.md`](skills/andino-workflow/references/execution-plan-template.md). Pilih LITE, STANDARD, atau DEEP secara konservatif.

Plan aktif sebaiknya menyimpan:

- objective dan acceptance criteria,
- current state dan current phase,
- execution board,
- keputusan dan evidence yang material,
- planned vs actual result,
- blockers/unknowns,
- `NEXT ACTION` yang konkret.

Untuk DEEP plan, tambahkan baseline, technical contract, root-cause findings, plan revisions, verification matrix, atau approval gate jika memang relevan.

Jangan simpan raw reasoning, seluruh log tool, full source file, atau informasi project yang sudah tersedia di rules.

### Checkpoint dan resume

Update checkpoint setelah:

- phase selesai,
- temuan penting,
- perubahan strategi,
- blocker,
- verifikasi,
- atau sebelum pindah sesi/agent.

Resume:

```text
Gunakan andino-workflow.
Continue @docs/exec-plans/active/USER-CRUD.md.
Periksa drift repository lalu lanjutkan NEXT ACTION.
Jangan ulang phase DONE tanpa evidence baru yang membatalkannya.
```

Jika host tidak mendukung `@`, berikan path atau lampirkan file plan. Plan menjaga koordinasi, tetapi tidak memindahkan working tree atau perubahan file secara otomatis.

## Skill routing

Andino memilih skill minimum yang relevan. Skill yang terpasang tidak berarti harus selalu dipakai.

| Capability | Gunakan ketika |
| --- | --- |
| `systematic-debugging` | Root cause bug belum diketahui. |
| `test-driven-development` | Perubahan perilaku membutuhkan regression/contract test. |
| `verification-before-completion` | Klaim selesai perlu evidence yang jelas. |
| `code-review-and-quality` | Diff membutuhkan review defect/quality. |
| `claude-mem` | Perlu mencari keputusan atau konteks historis. |
| `graphify` | Hubungan modul lebih mudah dipahami melalui graph. |
| `ui-ux-pro-max` | Form, dashboard, UX, accessibility, design system. |
| `design-taste-frontend` | Visual polish atau karakter desain dalam scope. |
| `ponytail` | Review kompleksitas berlebih secara on-demand. |
| `clone-website` | Replikasi website/screenshot dengan fidelity tinggi. |

`using-superpowers` dan router lama tidak ditumpuk otomatis dengan Andino. Memory dan graph adalah accelerator, bukan syarat handoff.

## MCP dan efisiensi konteks

- Context7 dan MCP khusus digunakan **on-demand**.
- Jangan memanggil tool yang sama pada state yang sama tanpa evidence baru.
- Hindari tool ping-pong dan retry tanpa batas.
- Gunakan output tool secukupnya; jangan masukkan log besar jika ringkasan atau range terarah cukup.
- Subagent default-nya **0**. Gunakan hanya jika pekerjaan benar-benar independen atau memberi manfaat jelas.
- SIMPLE task harus tetap simple.

Lihat [`anti-loop.md`](skills/andino-workflow/references/anti-loop.md) untuk guard lengkap.

## Project rules

[`put-in-your-projects`](put-in-your-projects/Agents.md) berisi template untuk repository pekerjaan.

Prinsipnya:

1. `AGENTS.md` menjadi core/router yang ringkas.
2. Rules frontend, backend, Git, code, token/context, dan spec tetap lazy, tetapi harus sudah disesuaikan dengan project ketika alignment dijalankan.
3. Jangan menempelkan seluruh rules ke setiap prompt.
4. Jangan menimpa requirement, design token, atau business rules yang sudah disepakati.
5. Mengubah template master di repository ini tidak otomatis memperbarui project lama.

## Validasi

Untuk perubahan pada Andino atau script repository:

```powershell
rtk proxy python -X utf8 scripts/validate.py
```

Sebelum menyatakan task selesai, verifikasi sesuai scope task. Jangan menjalankan suite besar berulang tanpa perubahan yang membenarkannya.

## Referensi

- [Host adapters](adapters/README.md)
- [Execution plan lifecycle](skills/andino-workflow/references/execution-plan.md)
- [Handoff](skills/andino-workflow/references/handoff.md)
- [Anti-loop](skills/andino-workflow/references/anti-loop.md)
- [UI/UX + Taste policy](skills/andino-workflow/references/ui-coexistence.md)
- [Invocation matrix](docs/invocation-matrix.md)
- [Acceptance audit](docs/acceptance-audit.md)
- [AI rules untuk chat berbasis web](AI-Rules-WebBased.md)

Audit dan historical prompt library tetap tersedia sebagai referensi manual, tetapi tidak menjadi runtime context default.
