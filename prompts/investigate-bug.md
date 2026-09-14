# Investigasi dan perbaikan bug

Gejala: [MASALAH]
Expected behavior: [HASIL BENAR]
Reproduksi/bukti awal: [JIKA ADA]
Plan: [PATH]

Gunakan project rules. Buat/resume plan jika non-trivial. Reproduksi dan telusuri
root cause dengan targeted source/log/test reads; gunakan systematic-debugging bila
bermanfaat. Memory/graph hanya accelerator, bukti current implementation yang menentukan.
Setelah penyebab terbukti, implementasikan perubahan minimum dalam scope yang diizinkan
dan verifikasi behavior serta regression terkait. Jangan memaksakan approval plan jika
implementasi sudah diotorisasi; patuhi gate yang memang diminta user/project.
Jelaskan sebab → perubahan → evidence secara singkat. Jika belum konklusif, checkpoint
ketidakpastian dan NEXT ACTION; jangan mengklaim selesai.
