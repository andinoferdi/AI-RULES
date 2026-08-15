Anda adalah AI coding assistant yang bertugas mengadaptasi paket template Markdown ini ke project tempat ia disalin.

Konteks:
- Folder ini berisi template rules AI yang generic dan reusable (chat-rules, code-rules, be-rules, fe-rules, Agents, token, git-*, brd, prd, srs, task, memory).
- Isinya memakai placeholder seperti [PROJECT_NAME], [STACK_BACKEND], [STACK_FRONTEND], [DATABASE], [MAIN_BRANCH], [STAGING_BRANCH], [MODUL_UTAMA], dan [INTEGRASI_EKSTERNAL].
- Saya ingin template ini diselaraskan dengan kondisi nyata project saat ini tanpa mengubah struktur, layout, heading, atau gaya ringkasnya.

Tugas utama:
Isi placeholder dan sesuaikan contoh di semua file Markdown agar cocok dengan project ini, berdasarkan implementasi nyata yang terlihat di repo.

Prioritas kerja:
1. Pahami dulu project: baca manifest/config (package.json, composer.json, atau sejenis), struktur folder, entry point, dan pola kode utama.
2. Tentukan nilai nyata untuk tiap placeholder: nama project, stack backend/frontend, database, branch utama dan staging, modul utama, dan integrasi eksternal.
3. Ganti semua placeholder di file Markdown dengan nilai nyata tersebut.
4. Sesuaikan contoh command, path, dan istilah agar cocok dengan project ini.
5. Tentukan wiring aktivasi: apakah project ini akan punya `CLAUDE.md`/`AGENTS.md` yang meng-import `code-rules.md`, `be-rules.md`, `fe-rules.md` secara permanen, atau file-file itu dipakai manual (dikirim user lewat A/B tiap sesi). Kunci kalimat "Aktivasi" di ketiga file itu sesuai hasil keputusan ini, jangan biarkan tetap ambigu ("sesuaikan kalimat ini dengan wiring project Anda").
6. Pertahankan struktur, heading, urutan, dan gaya ringkas tiap file.

Aturan perubahan:
- Jangan mengubah layout, heading, struktur section, atau gaya dokumentasi. Hanya isi dan sesuaikan konten.
- Jangan mengarang fitur, stack, endpoint, workflow, atau implementasi yang tidak terlihat di repo.
- Jika suatu placeholder tidak bisa dipastikan dari repo, biarkan sebagai placeholder dan catat di ringkasan akhir agar saya konfirmasi.
- Jaga bahasa tetap natural, rapi, konsisten, dan ringkas seperti aslinya.
- Jangan mengubah file non-Markdown kecuali saya minta eksplisit.
- Jangan menambah panjang file secara signifikan. Template ini sengaja ringkas agar AI tidak mudah lupa.

Batasan penting:
- Jangan rewrite total.
- Jangan menambah klaim teknis tanpa bukti dari file project.
- Jangan menghapus bagian penting hanya karena project belum memakainya, kecuali jelas tidak relevan.

Output yang saya inginkan:
- Terapkan perubahan langsung pada semua file Markdown yang relevan.
- Setelah selesai, berikan ringkasan singkat berisi:
  1. Nilai placeholder yang dipakai (project, stack, branch, integrasi, dst).
  2. File Markdown yang diubah dan jenis perubahan utamanya.
  3. Placeholder yang belum bisa dipastikan dan perlu konfirmasi.
  4. Catatan bila ada bagian template yang tidak relevan dengan project ini.
  5. Keputusan wiring aktivasi yang diambil (CLAUDE.md/AGENTS.md permanen, atau manual A/B) dan file mana saja yang kalimat "Aktivasi"-nya sudah dikunci sesuai keputusan itu.
