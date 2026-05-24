# Task

## Guide

- Di `[PATH_GIT_WORKFLOW]` wajib berada di branch utama terlebih dahulu, lalu jalankan pull untuk mendapatkan perubahan paling terbaru.
- Setelah branch utama sudah up-to-date, buat branch baru sesuai aturan penamaan di `[PATH_NAMING_RULES]`, lalu kerjakan task di branch tersebut.
- Setelah task selesai dan sudah diverifikasi, lakukan add, commit, push, lalu buat Pull Request ke branch tujuan sesuai workflow project.
- Nama branch, commit message, title Pull Request, dan deskripsi Pull Request wajib mengikuti ketentuan di `[PATH_NAMING_RULES]` dan `[PATH_GIT_WORKFLOW]`.
- Task ini akan didemokan oleh `[ROLE/PIHAK_DEMO]` pada environment `[NAMA_ENVIRONMENT_DEMO]`, yaitu `[URL_ENVIRONMENT_DEMO]`.
- Website atau aplikasi demo kemungkinan memakai kombinasi branch `[BRANCH_DEMO_1]` dan `[BRANCH_DEMO_2]`.
- Jika ada ketidaksambungan antara branch utama, branch staging, dan branch demo, gunakan pendekatan paling aman: mulai dari branch utama sesuai workflow, lalu bandingkan perubahan branch staging/demo sebelum eksekusi.
- Jika branch staging lebih maju daripada branch utama, jangan langsung mengubah workflow. Audit terlebih dahulu perbedaan branch, lalu ambil perubahan yang relevan secara selektif agar tetap aman dan tidak merusak aturan project.
- Untuk pemahaman flow yang lebih dalam, lihat dokumen atau diagram di `[PATH_FLOW_DIAGRAM]` karena flow utama fitur dijelaskan di sana.

## Kredensial

- Web local:
  - username: `[LOCAL_USERNAME]`
  - password: `[LOCAL_PASSWORD]`
- Web staging/demo:
  - url: `[STAGING_URL]`
  - username: `[STAGING_USERNAME]`
  - password: `[STAGING_PASSWORD]`

> Catatan: kredensial hanya boleh dipakai untuk testing sesuai izin. Jangan commit kredensial ke repository, dokumentasi publik, screenshot, log, atau Pull Request.

## Konteks

Jadi inti fitur ini adalah `[JELASKAN_RINGKAS_KONTEKS_FITUR]`.

Contoh konteks:
- `[CONTOH_KASUS_1]`
- `[CONTOH_KASUS_2]`
- `[CONTOH_KASUS_3]`

## Subtask Utama

Di `[NAMA_MODUL_UTAMA]`:

- [ ] 1. `[SUBTASK_1]`
  - File/area terkait: `[PATH_FILE_ATAU_MODUL_TERKAIT]`
  - Ekspektasi: `[HASIL_YANG_DIHARAPKAN]`

- [ ] 1.2. `[SUBTASK_1_2]`
  - File/area terkait: `[PATH_FILE_ATAU_MODUL_TERKAIT]`
  - Kondisi bug saat ini: `[JELASKAN_BUG_SAAT_INI]`
  - Ekspektasi: `[HASIL_YANG_DIHARAPKAN]`

- [ ] 1.2.1. `[SUBTASK_1_2_1]`
  - Masalah performa/konsistensi: `[JELASKAN_MASALAH]`
  - Yang perlu diaudit: `[BAGIAN_YANG_PERLU_DIAUDIT]`

- [ ] 1.3. `[SUBTASK_1_3]`
  - File/area terkait: `[PATH_FILE_ATAU_MODUL_TERKAIT]`
  - Ekspektasi tampilan/flow: `[HASIL_YANG_DIHARAPKAN]`

- [ ] 1.4. `[SUBTASK_1_4]`
  - Alasan perubahan: `[ALASAN_BISNIS_ATAU_TEKNIS]`
  - Catatan penyimpanan/data:
    - `[DATA_FLOW_1]`
    - `[DATA_FLOW_2]`
    - `[DATA_FLOW_3]`

- [ ] 1.5. `[SUBTASK_1_5]`
  - File/area terkait: `[PATH_FILE_ATAU_MODUL_TERKAIT]`
  - Ekspektasi: `[HASIL_YANG_DIHARAPKAN]`

- [ ] 2. `[SUBTASK_2]`
  - Tujuan: `[TUJUAN_PERUBAHAN]`
  - Data yang perlu ditampilkan/dikirim: `[FIELD_ATAU_DATA_YANG_DIBUTUHKAN]`
  - Referensi internal yang perlu dibaca:
    - `[PATH_REFERENSI_1]`
    - `[PATH_REFERENSI_2]`
    - `[PATH_REFERENSI_3]`
  - Output yang harus dibuat:
    - `[PATH_OUTPUT_PROMPT_ATAU_DOKUMEN]`
  - Catatan integrasi:
    - Jika perlu penyesuaian payload, tentukan field baru yang aman, backward compatible, dan jelas untuk kedua sisi integrasi.
    - Jika tidak perlu payload baru, jelaskan sumber data yang dipakai dan alasan teknisnya.
    - Pastikan perubahan bisa dipahami oleh programmer frontend, backend, dan pihak integrasi.

## Sebelum Eksekusi

Akses environment staging/demo menggunakan browser MCP, Playwright, browser harness, Chrome DevTools, atau tool lain yang tersedia dan hemat token.

- Buka `[STAGING_URL]`.
- Login hanya jika diperlukan untuk melihat flow.
- Jangan melakukan create, update, delete, submit, approve, reject, sync, import, export, atau action apa pun yang mengubah data staging/demo.
- Amati flow UI frontend dan perilaku backend yang relevan dengan task.
- Bandingkan dengan local untuk melihat perbedaan flow, tampilan, data, atau response.
- Jika perlu melihat referensi kode dari branch staging/demo, lakukan secara read-only dan ambil hanya bagian yang relevan.
- Jangan menyalin perubahan secara buta. Sesuaikan dengan branch kerja dan pola kode project aktif.

## Audit

- Ikuti arahan workflow project: mulai dari branch utama jika memang itu aturan resmi.
- Pull Request wajib diarahkan ke branch tujuan yang benar, yaitu `[TARGET_PR_BRANCH]`.
- Jika environment demo memakai branch berbeda dari target PR, jangan langsung menyimpulkan target PR salah.
- Audit perbedaan antara `[BRANCH_UTAMA]`, `[TARGET_PR_BRANCH]`, dan `[BRANCH_DEMO]` sebelum mengambil keputusan.
- Jika branch staging/demo lebih maju, ambil perubahan relevan dengan cara paling aman: merge/cherry-pick/port manual sesuai kondisi repo dan arahan maintainer.
- Yang paling penting: hasil akhir tetap bisa naik ke Pull Request branch `[TARGET_PR_BRANCH]` tanpa merusak workflow, riwayat Git, atau flow bisnis.
- Pastikan solusi tidak hanya cocok di local, tetapi juga masuk akal terhadap kondisi staging/demo.
- Catat asumsi branch dan alasan teknis bila ada keputusan yang berpotensi membingungkan reviewer.

## Eksekusi

Eksekusi sesuai perintah task dan jangan pernah melakukan perubahan data apa pun di website `[STAGING_URL]` kecuali login untuk observasi.

- Boleh melihat UI, flow, response, struktur halaman, dan perilaku fitur.
- Tidak boleh melakukan post/submit/action yang mengubah data staging/demo tanpa izin eksplisit.
- Setelah selesai mengubah kode, jangan add, commit, atau push sebelum diminta.
- Jika nanti diminta commit atau push, ikuti `[PATH_NAMING_RULES]` dan `[PATH_GIT_WORKFLOW]`.
- Berhati-hati karena ini project besar. Jangan mengubah bagian kritikal tanpa kebutuhan task yang jelas.
- Ikuti pola kode yang sudah ada dan pastikan perubahan konsisten satu sama lain.
- Hindari refactor besar yang tidak diminta.
- Jalankan verifikasi yang relevan sesuai area perubahan, misalnya test, lint, build, atau pengecekan manual.
- Setelah selesai, laporkan:
  - file yang diubah,
  - ringkasan perubahan,
  - hasil verifikasi,
  - risiko atau catatan yang masih perlu diperhatikan.

## Kredensial dan Web Staging Tambahan

- Web/API tambahan:
  - url: `[ADDITIONAL_STAGING_URL]`
  - username: `[ADDITIONAL_USERNAME]`
  - password: `[ADDITIONAL_PASSWORD]`

> Catatan: bagian ini opsional. Isi hanya jika task memang membutuhkan environment tambahan seperti sistem integrasi, dashboard admin, marketplace, payment gateway sandbox, atau service eksternal lain.
