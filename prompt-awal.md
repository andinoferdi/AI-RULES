Capability manifest tersedia untuk dipilih sesuai kebutuhan. Jangan jalankan semuanya.

* claude-mem
* taste-skill
* ui-ux-pro-max
* graphify
* skill Superpowers spesifik sesuai kebutuhan
* ponytail
* andino-workflow
* ai-codebase-rescue
* clone-website

Manifest ini hanya daftar kemungkinan capability, bukan instruksi aktivasi. Hormati native invocation controls dan pilihan skill eksplisit user. Jangan menjalankan router `using-superpowers`, `using-agent-skills` atau `agent-skills`. Ketika Andino aktif, reuse plan/checkpoint-nya; Rescue menjadi spesialis evidence dan remediation. Tanpa Andino aktif, gunakan task context host dan jangan membuat lifecycle baru hanya karena skill terpasang.

Gunakan capability di atas hanya jika tersedia pada agent/environment saat ini dan memang relevan dengan tugas. Gunakan mekanisme native agent untuk memanggilnya, misalnya skill, slash command, MCP prompt/tool, atau capability lain yang setara. Jangan gagal hanya karena nama atau mekanisme invocation berbeda pada agent yang sedang digunakan.

Baca dan terapkan `[LOKASI_CHAT_RULES], [LOKASI_HUMAN_LANGUAGE_ENGLISH], [LOKASI_HUMAN_LANGUAGE_INDONESIA]` sebagai aturan komunikasi dan gaya chat Anda dengan saya.

Jika ada task/plan/checkpoint aktif, resume dari state itu dan periksa drift tanpa bootstrap ulang. Hanya untuk orientasi awal yang diminta, terapkan instruksi bootstrap di `[LOKASI_FIRST_PROMPT]` untuk memahami project dalam workspace ini:

* `[LOKASI_PROJECT]`

