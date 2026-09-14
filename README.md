# Andino-Workflow

Workflow engineering untuk Codex, Claude Code, OpenCode, dan Antigravity: memilih proses yang sesuai dengan pekerjaan dan menjaga execution plan agar task dapat dilanjutkan lintas sesi maupun lintas agent.

Keempat agent adalah **peer primary-capable agents**. Agent yang sedang digunakan menjadi primary untuk sesi tersebut. Targetnya functional parity, dengan cara pemanggilan dan konfigurasi sesuai kemampuan masing-masing host.

## Cara kerja

Andino-Workflow adalah **bounded workflow router + execution-plan manager**. Ia mengklasifikasikan pekerjaan, memilih skill minimum yang relevan, menjaga checkpoint, dan mengarahkan verifikasi.

| Bagian | Tanggung jawab |
| --- | --- |
| Project rules | Constraints, convention, dan cara kerja repository. |
| Execution plan | State ticket lintas sesi: WHAT, WHY, CURRENT STATE, CURRENT PHASE, EVIDENCE, NEXT ACTION. |
| Andino-Workflow | Mengelola lifecycle plan dan routing metodologi/capability. |
| Skills | Workers dan metodologi spesialis. |
| Tools / MCP | Instrumen untuk melakukan pekerjaan. |
| Memory / graph | Accelerator konteks opsional. |

Repository dan konfigurasi aktual tetap menjadi sumber kebenaran. Memory, termasuk claude-mem, boleh digunakan lintas-agent untuk retrieval terarah; memory tidak menjadi syarat handoff dan tidak perlu diambil setiap prompt.

### Ukuran workflow mengikuti task

| Kelas | Contoh | Proses dan plan |
| --- | --- | --- |
| SIMPLE | Typo, label, perubahan kecil dengan solusi jelas | Pahami, edit, verifikasi terarah. Plan hanya jika diminta atau sudah menjadi bagian ticket. |
| STANDARD | Fitur lokal, bug jelas, refactor terbatas | Ambil konteks relevan, implementasi, verifikasi. Buat plan untuk ticket non-trivial atau lanjutkan plan yang ada. |
| COMPLEX | Akar masalah belum jelas, arsitektur, migrasi, perubahan lintas sistem | Investigasi, pilih metodologi, implementasi bertahap, verifikasi, checkpoint. Plan diperlukan. |

Andino memilih satu pengelola workflow dan skill spesialis yang diperlukan. Tidak ada kewajiban melewati `using-superpowers`, memuat seluruh skill, membuat graph, atau menggunakan subagent untuk setiap task.

## Pemasangan skill

### Sumber dan salinan terpasang

[skills/andino-workflow](skills/andino-workflow/SKILL.md) adalah sumber kanonis dalam repository ini. Agent membaca salinan yang dipasang di direktori discovery masing-masing.

| Agent | Lokasi relatif terhadap home pengguna | Pemanggilan |
| --- | --- | --- |
| Codex | `.agents/skills/andino-workflow/` | `$andino-workflow` |
| Claude Code | `.claude/skills/andino-workflow/` | `/andino-workflow` |
| OpenCode | `.config/opencode/skills/andino-workflow/` | Native skill tool; `/andino-workflow` jika command adapter sudah dipasang. |
| Antigravity | `.gemini/config/skills/andino-workflow/` | Minta agent menggunakan skill `andino-workflow` melalui Skills. |

Codex menggunakan shared skills `.agents`. Antigravity pada setup yang diaudit menggunakan `.gemini/config`, bukan `.antigravity` atau `.antigravity-ide`. Periksa kembali kompatibilitas discovery saat versi host berubah.

### Sinkronisasi

Prasyarat: Python 3.9+ dan host yang mendukung lokasi skill di atas. Jalankan dari root repository; contoh menggunakan RTK sesuai kebijakan mesin ini:

```powershell
rtk proxy python -X utf8 scripts/sync-workflow.py
rtk proxy python -X utf8 scripts/sync-workflow.py --check
```

Jika RTK tidak digunakan pada mesin lain, jalankan bagian `python ...` secara langsung.

Script menyalin skill beserta referensinya ke empat lokasi, mencatat hash, dan menyimpan backup penggantian di luar Git. Ia menolak menimpa pemasangan yang tidak dikelolanya atau perubahan lokal yang belum direkonsiliasi. Edit sumber kanonis, lalu sinkronkan; jangan memelihara empat versi secara terpisah.

**Script ini hanya memasang skill Andino.** Ia tidak memasang aplikasi agent, worker lain, command adapter OpenCode, konfigurasi global, plugin, atau MCP. Lihat [host adapters](adapters/README.md) untuk integrasi dan batas tiap host. Muat ulang host atau mulai sesi baru bila katalog skill belum diperbarui.

## Panduan dari setup proyek sampai task pertama

### 1. Siapkan repository pekerjaan

Buka repository pekerjaan Anda di agent, bukan repository AI-RULES. Contoh berikut menggunakan proyek ilustratif `D:/Projects/user-portal`; ganti dengan lokasi proyek Anda.

Jika proyek belum memiliki rules, salin folder `put-in-your-projects` dari repository ini ke `D:/Projects/user-portal/docs/ai-rules/`. Ini contoh lokasi, bukan nama folder wajib. Pertahankan struktur internal agar referensi antardokumen tetap mudah disesuaikan.

```text
user-portal/
  src/
  docs/
    ai-rules/
      Agents.md
      be-rules.md
      fe-rules.md
      ...
```

Folder template saja belum menjamin host memuat rules. Tahap alignment berikut menghubungkannya ke instruksi native proyek. Jangan menimpa rules proyek yang sudah ada; gabungkan yang relevan. Skill Andino global tidak perlu disalin ke proyek.

### 2. Sesuaikan template melalui alignment

Kirim isi [Project Markdown Alignment Prompt.md](<Project Markdown Alignment Prompt.md>) kepada agent, lalu tambahkan konteks seperti berikut. Jika host mendukung lampiran file, lampirkan dokumen tersebut; menyebut nama file yang tidak dapat diakses agent saja tidak cukup.

```text
Terapkan instruksi Project Markdown Alignment yang saya lampirkan.
Repository pekerjaan: D:/Projects/user-portal.
Template yang saya salin berada di docs/ai-rules/.

Periksa stack, struktur, command, dan aturan proyek yang sudah ada.
Sesuaikan template dengan evidence repository ini.
Gabungkan core ke AGENTS.md di root untuk Codex/OpenCode;
hubungkan instruksi native host lain sesuai dukungannya.
Perbaiki semua referensi relatif setelah penempatan file.
Jangan menimpa aturan proyek yang sudah disepakati.
Jangan mengarang kebutuhan produk untuk mengisi PRD/SRS.
Laporkan informasi penting yang belum tersedia.
```

Hasil yang diharapkan: rules menyebut stack dan command aktual, instruksi native mengarah ke rules yang tepat, serta placeholder yang belum dapat diisi dicatat. Alignment bukan perintah untuk membuat seluruh produk atau mengarang semua spesifikasinya.

### 3. Bootstrap jika masih diperlukan

Setelah alignment selesai, bootstrap digunakan untuk memahami proyek sebelum mengerjakan fitur. Gunakan instruksi **baca dan jalankan First-prompt**, bukan "implementasikan First-prompt", agar tujuan memahami konteks tidak tercampur dengan implementasi fitur.

Kirim prompt berikut. Lokasi file pada contoh mengikuti penempatan template di tahap 1; ganti dengan path aktual atau lampirkan [First-prompt](<put-in-your-projects/1. First-prompt.md>) jika agent tidak dapat mengaksesnya:

```text
Baca dan jalankan instruksi First-prompt yang sudah disalin ke repository ini.
File bootstrap: docs/ai-rules/1. First-prompt.md

Lakukan bootstrap konteks: pahami project rules yang aktif, stack,
struktur utama, serta command development dan verifikasi yang tersedia.

Ambil konteks minimum yang diperlukan. Jangan mengulang alignment
yang sudah selesai atau melakukan audit seluruh repository.

Belum ada permintaan implementasi fitur.
Sampaikan pemahaman singkat dan informasi penting yang masih belum jelas.
```

**Andino tidak wajib dipanggil untuk bootstrap ini.** Jika alignment dalam sesi yang sama sudah memberi pemahaman rules, stack, struktur, dan command yang cukup, lewati bootstrap tambahan dan langsung berikan task seperti contoh CRUD pada tahap 4. Dalam sesi baru, ambil kembali konteks minimum; jika melanjutkan ticket yang memiliki plan, gunakan alur resume pada tahap 5.

Urutan penggunaan: **alignment sekali → bootstrap konteks bila masih diperlukan → task fitur → resume dari execution plan bila terputus**.

Setup/alignment tidak perlu diulang pada setiap fitur. Jalankan lagi ketika wiring rules, stack, atau kebutuhan alignment memang berubah. Repository yang sudah mempunyai rules sesuai dapat langsung mulai dari tahap berikut.

### 4. Berikan fitur baru: contoh CRUD user lengkap

Di Codex, kirim prompt ini dari repository pekerjaan:

```text
$andino-workflow

Buat CRUD user mengikuti stack dan pola repository ini.
Kebutuhan:
- Daftar user dengan pencarian dan pagination.
- Detail, tambah, edit, dan hapus user.
- Field nama, email unik, dan status aktif.
- Hanya admin yang boleh mengelola user.
- UI memiliki loading, empty, error, dan success state.

Gunakan autentikasi dan komponen yang sudah ada.
Jika kebijakan penghapusan belum jelas, tanyakan hard delete atau soft delete.
Pilih skill minimum yang diperlukan secara otomatis.
Buat/update docs/exec-plans/active/USER-CRUD.md untuk ticket ini.
Implementasikan lalu verifikasi acceptance criteria dan akses non-admin.
```

Di Claude Code, ganti baris pertama dengan `/andino-workflow`. Di OpenCode gunakan slash tersebut jika command adapter tersedia, atau minta native skill tool. Di Antigravity gunakan `Gunakan skill andino-workflow`. Isi kebutuhan setelahnya dapat tetap sama. Tanda `$` dan `/` adalah mekanisme host, bukan dua langkah yang harus dijalankan berurutan.

Andino memeriksa implementasi yang sudah ada, menentukan kelas task, mengelola plan, memilih worker per fase, lalu mengerjakan dan memverifikasi perubahan. Anda tidak harus menyusun urutan skill sendiri. Penghapusan pada contoh adalah implementasi fitur; bukan izin menghapus data produksi untuk pengujian.

### 5. Iterasi, jeda, dan lanjutkan

Untuk revisi dalam ticket yang sama:

```text
Gunakan andino-workflow. Lanjutkan ticket USER-CRUD yang sama.
Tambahkan filter status aktif pada daftar user.
Perbarui acceptance criteria dan plan; pertahankan hasil yang masih valid.
```

Sebelum pindah sesi/agent:

```text
Perbarui checkpoint USER-CRUD: hasil selesai, evidence verifikasi,
pekerjaan tersisa, blocker, dan NEXT ACTION konkret.
```

Untuk melanjutkan:

```text
Gunakan andino-workflow.
Continue @docs/exec-plans/active/USER-CRUD.md.
Periksa drift repository lalu lanjutkan NEXT ACTION.
Jangan ulang fase DONE tanpa evidence yang membatalkannya.
```

Jika host tidak mendukung `@`, berikan path atau lampirkan plan tersebut. Pastikan perubahan kerja juga tersedia di host tujuan. Plan menyimpan koordinasi; ia tidak memindahkan file kerja secara otomatis.

## Pemilihan skill: otomatis atau eksplisit

**Ya, Andino dirancang memilih skill minimum yang dibutuhkan secara otomatis berdasarkan task, fase, dan capability yang benar-benar tersedia.** Otomatis di sini berarti agent mengikuti instruksi routing; bukan script yang selalu menjalankan daftar skill atau jaminan perilaku model pada semua host.

Skill yang terpasang belum tentu diiklankan, boleh auto-trigger, atau dapat dipanggil secara eksplisit dengan mekanisme yang sama. Andino memeriksa availability dan batas host. Jika skill tidak tersedia, jelaskan keterbatasan dan gunakan metode yang sesuai; jangan mengklaim telah memanggilnya atau memasang capability baru tanpa kebutuhan.

**Batas aktual setelah hardening:** empat core worker Codex dibuat non-implicit; Claude dibuat user-invocable-only; OpenCode V1 dibatasi melalui permission skill. Jadi Andino dapat menentukan worker yang tepat, tetapi pemanggilan worker yang dibatasi dapat memerlukan tindakan eksplisit pengguna. Jangan melewati pembatasan native dengan membaca file skill melalui tool lain. Pada Antigravity, deskripsi worker dipersempit ke pilihan eksplisit/Andino; ini belum menjadi sakelar non-implicit yang dipaksakan host. Rincian tersedia pada [matrix invocation](docs/invocation-matrix.md).

### Dinamis / otomatis: Anda menyebut hasil

```text
Gunakan andino-workflow untuk membuat halaman login.
Ikuti design system dan autentikasi yang sudah ada.
Pastikan responsif, keyboard-accessible, dan memiliki error/loading state.
Pilih skill relevan minimum; jelaskan singkat pilihan yang digunakan.
```

Agent dapat memilih panduan UI/UX untuk formulir, metode pengujian untuk perilaku login, dan verifikasi yang relevan. Memory, graph, browser, atau skill desain tambahan tidak wajib aktif hanya karena tersedia.

### Statis / eksplisit: Anda menentukan skill

Istilah statis di panduan ini berarti pilihan skill disebut dalam prompt, bukan pengaturan runtime baru.

```text
Gunakan andino-workflow serta ui-ux-pro-max dan taste-skill
(nama skill sebenarnya design-taste-frontend) untuk halaman login.
Baca kedua skill dan tetapkan satu arah desain yang sesuai brand proyek.
Gunakan UI/UX Pro Max untuk UX, aksesibilitas, dan formulir.
Terapkan Taste hanya pada panduan visual yang sesuai ruang lingkupnya.
Pertahankan komponen, token, stack, dan autentikasi yang sudah ada.
Jika layar ini menjadi alur produk kompleks, jelaskan batas Taste
dan gunakan UI/UX Pro Max sebagai panduan utama.
```

Meminta keduanya berarti membaca kedua skill aktual, bukan menjalankan dua lifecycle workflow. Jika Anda meminta hanya satu, skill desain lainnya tidak otomatis diaktifkan. Pilihan eksplisit tetap tunduk pada kebutuhan proyek, aksesibilitas, dan availability host.

### Skill apa yang dipakai?

| Skill/capability | Kapan relevan | Batas penggunaan |
| --- | --- | --- |
| claude-mem | Keputusan dan konteks historis yang perlu dicari | Retrieval terarah lintas-host yang integrasinya bekerja; bukan setiap prompt atau syarat handoff. |
| design-taste-frontend / taste-skill | Karakter visual landing page, portfolio, redesign dalam scope | Alias merujuk skill yang sama; bukan default untuk dashboard/tabel/alur produk kompleks. |
| ui-ux-pro-max | Formulir, UI produk, dashboard, UX, aksesibilitas | Ikuti stack, komponen, dan design system proyek. |
| graphify | Hubungan modul yang lebih mudah dipahami melalui graph | Gunakan jika membantu; validasi ke source aktual, tanpa rebuild otomatis. |
| superpowers:using-superpowers | Router/bootstrap alternatif | Tidak dipanggil otomatis oleh Andino. Worker relevan dipilih langsung. |
| systematic-debugging | Akar bug belum diketahui | Investigasi berbukti; tidak wajib untuk typo. |
| test-driven-development | Perubahan perilaku yang perlu regression/contract | Sesuai pengujian proyek; tidak wajib untuk edit teks. |
| verification-before-completion | Memastikan klaim hasil didukung evidence | Verifikasi relevan, tanpa pengulangan suite tanpa alasan. |
| code-review-and-quality | Review perubahan yang membutuhkan pemeriksaan | Fokus diff dan defect yang actionable. |
| ponytail | Pemeriksaan kompleksitas berlebih sesuai permintaan | Alternatif on-demand, bukan seluruh keluarga skill otomatis aktif. |
| agent-skills | Router lama | Tidak ditumpuk dengan Andino; entri lama diarahkan ke Andino. |
| clone-website | Cloning dari referensi visual/website | Relevan untuk fidelity clone; bukan CRUD biasa. |

Nama pemanggilan worker mengikuti katalog host. Tabel ini adalah kebijakan routing, bukan klaim bahwa seluruh skill tersedia identik pada empat agent atau bahwa semua kontrol non-implicit telah selesai diverifikasi.

### Contoh prompt capability khusus

**Konteks historis:**

```text
Gunakan andino-workflow. Sebelum mengubah autentikasi, gunakan claude-mem
secara terarah untuk mencari alasan keputusan autentikasi proyek ini.
Cocokkan temuan dengan source/config aktual. Jika memory tidak tersedia,
lanjutkan dari repository dan catat gap yang relevan.
```

**Relasi kode:**

```text
Gunakan andino-workflow untuk menjelaskan kenapa modul billing
bergantung pada user. Mulai dengan symbol/reference search terarah.
Gunakan Graphify jika graph yang tersedia membantu; jangan rebuild otomatis.
```

**Bug dan worker:**

```text
Gunakan andino-workflow dan systematic-debugging.
Checkout kadang men-charge customer dua kali.
Cari root cause dengan fixture/sandbox, perbaiki, lalu tambahkan regression
verification. Jangan melakukan charge nyata untuk menguji bug.
```

Ini memilih metodologi debugging langsung, tanpa bootstrap `using-superpowers`. Worker pengujian dipakai sesuai perubahan perilaku dan kemampuan host.

**Review kompleksitas:**

```text
Gunakan andino-workflow dan Ponytail yang tersedia untuk meninjau
kompleksitas diff CRUD user. Laporkan saran terarah terlebih dahulu;
jangan refactor area di luar ticket.
```

**Cloning:**

```text
Gunakan andino-workflow dan clone-website untuk mereplikasi landing page
dari screenshot yang saya lampirkan. Pertahankan fidelity referensi
dan stack proyek. Jangan redesign kecuali saya minta.
```

**Perubahan sederhana:**

```text
Ganti teks tombol Login menjadi Masuk.
```

Expected: edit lokal dan pemeriksaan terarah. Tidak perlu plan baru, memory, graph, browser, subagent, atau stack metodologi otomatis, kecuali konteks proyek memberi alasan nyata.

## Contoh ringkas lainnya

### Task baru

Buka repository pekerjaan di agent pilihan, lalu panggil skill dengan kebutuhan dan acceptance criteria yang jelas. Contoh untuk Codex:

```text
$andino-workflow
Tambahkan validasi email pada formulir pendaftaran.
Acceptance criteria: email tidak valid ditolak dengan pesan yang jelas;
pendaftaran dengan email valid tetap bekerja.
Ikuti project rules dan buat execution plan jika task ini non-trivial.
```

Pada Claude Code gunakan `/andino-workflow`. Pada host lain gunakan mekanisme pada tabel pemasangan. Untuk perubahan sederhana, instruksi langsung juga cukup.

Template tersedia untuk [task umum](Prompt-task.md) dan [investigasi bug](prompts/investigate-bug.md). [Bootstrap awal](prompt-awal.md) dipakai ketika konteks proyek belum diketahui, bukan diulang pada setiap ticket.

### Melanjutkan atau berpindah agent

Pastikan agent berikutnya memiliki akses ke repository, perubahan kerja yang diperlukan, dan file plan terbaru. Kemudian kirim:

```text
Gunakan andino-workflow.
Lanjutkan docs/exec-plans/active/TICKET-001.md.
Cocokkan checkpoint dengan kondisi repository saat ini,
lalu kerjakan NEXT ACTION. Pertahankan hasil yang sudah selesai
kecuali ada evidence baru yang membatalkannya.
```

Gunakan path atau lampiran file sesuai dukungan host. Plan tidak memindahkan working tree, branch, atau perubahan yang belum di-commit secara otomatis. Tidak perlu menyalin seluruh percakapan atau memiliki memory integration yang sama.

## Execution plan di repository pekerjaan

Simpan plan bersama proyek yang dikerjakan, misalnya:

```text
your-project/
  AGENTS.md
  docs/
    exec-plans/
      active/
        TICKET-001.md
      completed/
```

Gunakan [template execution plan](skills/andino-workflow/references/execution-plan-template.md). Catat objective, acceptance criteria, constraints, current state, fase, keputusan, evidence, verifikasi, blocker, dan NEXT ACTION yang konkret.

Perbarui checkpoint setelah temuan penting, penyelesaian fase, perubahan strategi, interupsi, atau verifikasi. Simpan hasil dan alasan keputusan secara ringkas; hindari raw reasoning transcript, seluruh log, atau salinan kode besar.

Tandai DONE hanya setelah acceptance criteria terpenuhi dan verifikasi yang diperlukan selesai. Jika terhambat, tinggalkan status dan langkah berikutnya yang dapat dijalankan. Lihat [lifecycle plan](skills/andino-workflow/references/execution-plan.md) dan [handoff](skills/andino-workflow/references/handoff.md).

## Memasang project rules

[put-in-your-projects](put-in-your-projects/Agents.md) tetap merupakan kumpulan template untuk repository pekerjaan Anda.

1. Sesuaikan core template dengan proyek, lalu gabungkan ke instruksi native host. Untuk discovery Codex gunakan nama `AGENTS.md`; Claude dapat menggunakan `CLAUDE.md` yang mengimpor kontrak proyek sesuai dukungannya.
2. Tempatkan rules domain yang diperlukan di lokasi dokumentasi proyek dan sesuaikan tautan relatifnya. Pertahankan aturan proyek yang sudah disepakati.
3. Gunakan [First-prompt](<put-in-your-projects/1. First-prompt.md>) sebagai prompt bootstrap awal dan [Send-to-every-prompt](<put-in-your-projects/2. Send-to-every-prompt.md>) sebagai pengingat singkat bila diperlukan.

Rules backend/frontend/Git dan spesifikasi dibaca saat relevan. Tidak perlu menempelkan seluruh folder ke setiap pesan. Pemasangan ke proyek baru atau perubahan stack dapat menggunakan [Project Markdown Alignment](<Project Markdown Alignment Prompt.md>).

Skill global berada di lokasi agent; rules dan execution plan khusus proyek berada di repository pekerjaan. Mengubah template di sini tidak otomatis memperbarui semua proyek lama.

## Batas dan pemeliharaan

- Pemanggilan tool berulang harus memiliki perubahan state atau evidence baru. Lihat [anti-loop](skills/andino-workflow/references/anti-loop.md).
- Aktifkan MCP/capability yang relevan dengan task. Helper [mcp-toggle.py](scripts/mcp-toggle.py) menangani konfigurasi lokal yang didukung; bukan installer server atau startup otomatis per proyek.
- Simpan credential, backup konfigurasi, dan data memory di luar repository.
- Commit, push, merge, publikasi, dan deployment mengikuti otorisasi pengguna; bukan efek otomatis dari selesainya plan.
- Skills memberi panduan perilaku. Mereka tidak menjamin kepatuhan model atau menggantikan batas runtime host.

Untuk perubahan script, jalankan pemeriksaan terisolasi:

```powershell
rtk proxy python -X utf8 scripts/validate.py
```

[Audit implementasi](docs/audit.md) mencatat kondisi mesin pada saat audit, perubahan konfigurasi, dan batas verifikasi. [Skenario routing](docs/routing-scenarios.md) mendokumentasikan pemeriksaan kontrak. Pemeriksaan statis/discovery tidak sama dengan pengujian model langsung di seluruh aplikasi, dan belum membuktikan besaran penghematan token.

## Dokumen lain

- [Final acceptance audit](docs/acceptance-audit.md) mencatat hardening, ukuran surface aktif, hambatan pengujian native, dan tindakan manual tersisa. Setup belum dinyatakan lulus behavioral acceptance di empat host.

- [AI-Rules-WebBased.md](AI-Rules-WebBased.md) tetap digunakan untuk AI chat berbasis web dan dikelola terpisah dari Andino-Workflow.
- [Personal prompt library](references/personal-prompt-library.md) menyimpan pustaka README lama sebagai referensi manual; isinya tidak otomatis menjadi instruksi workflow.
- [Kebijakan Taste + UI/UX Pro Max](skills/andino-workflow/references/ui-coexistence.md) dibaca hanya saat penggunaan skill desain tersebut relevan.
