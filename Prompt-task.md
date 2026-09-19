Capability manifest tersedia untuk dipilih sesuai kebutuhan. Jangan jalankan semuanya:

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

Gunakan capability di atas hanya jika tersedia pada agent/environment saat ini dan memang relevan dengan task. Gunakan mekanisme native agent untuk memanggilnya, seperti skill, slash command, MCP prompt/tool, atau capability setara. Jangan gagal hanya karena nama atau mekanisme invocation berbeda.

Sebelum investigasi luas, manfaatkan context yang sudah tersedia.

Jika tersedia dan relevan, gunakan claude-mem, Graphify, project memory, documentation, semantic search, atau index lain sebagai accelerator untuk mempersempit area investigasi.

Untuk claude-mem, ambil hanya memory yang relevan dengan masalah. Jangan melakukan retrieval luas tanpa filtering.

Untuk Graphify, gunakan graph/index yang sudah tersedia melalui query/path/explain. Jangan rebuild atau regenerate graph hanya untuk task ini kecuali memang diminta atau graph terbukti tidak valid dan rebuild menjadi bagian task.

Untuk task UI/frontend visual, responsive layout atau styling, pilih Taste, `ui-ux-pro-max`, atau keduanya sesuai kebutuhan yang berbeda. Pertahankan pilihan satu skill yang eksplisit; jangan otomatis memasangkan keduanya untuk semua task frontend, termasuk rescue runtime tanpa kebutuhan redesign.

Pastikan instruction di `[LOKASI_SECOND_PROMPT]` berlaku untuk task ini. Jika file tersebut sudah dimuat melalui project/agent wiring dan isinya tersedia dalam context, jangan membacanya ulang hanya untuk menduplikasi context. Muat dokumentasi project tambahan hanya jika relevan.

Repository aktual tetap menjadi source of truth untuk current implementation.

Memory, graph, documentation, dan index dapat membantu menemukan area masalah, tetapi jangan menetapkan root cause hanya dari context tersebut jika current source code, configuration, test, log, atau runtime evidence diperlukan untuk membuktikannya.

Gunakan targeted repository search dan targeted source reads untuk memverifikasi hypothesis.

Jangan melakukan broad source scan, recursive full-read, atau spawn banyak subagent hanya untuk memahami masalah lokal.

Untuk read-only investigation yang masih berada dalam scope masalah ini, Anda tidak perlu meminta izin saya setiap kali perlu membaca file tambahan. Baca hanya file, symbol, range, log, config, atau test yang benar-benar relevan.

Minta konfirmasi hanya jika investigasi perlu diperluas secara material ke subsystem yang tidak terkait dengan scope awal, atau sebelum melakukan tindakan yang bersifat mutating, destructive, irreversible, production-sensitive, atau remote side effect yang belum saya izinkan.

Jika ada ambiguity yang benar-benar dapat menghasilkan expected behavior atau solusi berbeda, tanyakan kepada saya. Jangan membuat clarification question jika jawabannya sudah dapat dibuktikan dari repository, documentation, memory, graph, log, test, atau context yang tersedia.

PERMASALAHAN:

"[PERMASALAHAN]"

TASK:

Jangan langsung melakukan fix.

Mulai dengan diagnosis dan investigasi untuk memahami:

gejala yang terjadi,

behavior yang seharusnya,

alur yang terlibat,

hypothesis penyebab,

dan bukti yang mendukung atau menolak hypothesis tersebut.

Jika clarification dari saya memang diperlukan untuk memahami expected behavior, tanyakan secara singkat. Jika tidak diperlukan, lanjutkan investigasi tanpa berhenti hanya untuk melakukan brainstorming formal.

Cari root cause berdasarkan bukti dari current source code, configuration, log, test, runtime behavior, documentation, memory, graph, atau data relevan lainnya.

Jangan menyimpulkan root cause hanya berdasarkan asumsi, memory lama, atau graph/index yang mungkin stale.

Saat menjelaskan hasil investigasi, gunakan bahasa sederhana seperti developer menjelaskan kepada developer lain.

Saya perlu memahami:

apa penyebab masalah,

alur atau bagian code yang membuat masalah terjadi,

mengapa behavior tersebut salah,

dan mengapa solusi yang diusulkan paling masuk akal.

Tujuannya bukan hanya menyelesaikan masalah, tetapi membuat saya dapat menjelaskan hubungan sebab-akibatnya kepada QA, Tech Lead, atau developer lain.

Untuk komentar dalam code:

jangan menambahkan comment yang hanya menjelaskan sesuatu yang sudah obvious dari code.

Gunakan comment hanya jika membantu menjelaskan intent, invariant, constraint, workaround, compatibility issue, atau alasan yang tidak terlihat langsung dari implementation.

Tidak ada batas jumlah baris comment yang kaku. Gunakan seminimal yang diperlukan agar code tetap jelas.

Setelah root cause cukup jelas dan didukung bukti, buat implementation plan konkret yang menjelaskan:

perubahan yang diperlukan,

area code yang terdampak,

risiko regression,

regression test yang perlu ditambah atau diperbarui,

dan verification yang akan digunakan untuk membuktikan fix.

Tunjukkan implementation plan tersebut kepada saya.

JANGAN mengubah source code sebelum saya menyetujui plan.

GIT:

Ikuti `git-naming.md`, `git-workflow.md`, dan `git-branch-tips.md` yang berlaku pada project.

Sebelum membuat branch, deteksi:

remote yang benar,

base branch yang benar,

current branch,

working tree state,

dan convention branch project.

Jika project ini memang menggunakan personal prefix `andino`, gunakan:

`andino/fix/<nama-permasalahan-singkat>`

atau type `andino/...` lain yang lebih sesuai dengan konteks.

Jika convention repository berbeda, ikuti convention repository kecuali saya secara eksplisit mengunci format branch tersebut.

Jangan hard-code `origin/main` kecuali repository memang membuktikan remote dan base branch tersebut benar.

Sebelum membuat work branch untuk implementation, refresh remote refs jika akses tersedia dan pastikan branch berasal dari base terbaru yang benar.

Jika branch target sudah ada, diverged, digunakan sebagai shared branch, memiliki commit sendiri, terdapat perubahan lokal yang berpotensi tertimpa, atau membutuhkan history rewrite/destructive operation, jelaskan kondisi tersebut sebelum mengambil tindakan berisiko.

Read-only Git inspection seperti status, log, diff, branch, remote, dan fetch untuk memperbarui remote refs boleh dilakukan selama berada dalam scope task.

Jangan melakukan reset, discard user changes, force push, branch deletion, merge/rebase shared history, commit, push, PR/MR creation, atau remote side effect lain tanpa scope atau izin yang sesuai.

IMPLEMENTATION:

Setelah plan saya setujui, implementasikan perubahan sekecil mungkin yang benar-benar menyelesaikan root cause.

Ikuti pattern codebase yang sudah ada.

Reuse implementation atau abstraction existing jika sesuai.

Jangan melakukan unrelated refactor.

Tambahkan atau perbarui regression test yang relevan jika testing setup project mendukungnya.

Lakukan verification berdasarkan behavior yang sebelumnya gagal.

Jangan menganggap fix berhasil hanya karena:

code berhasil diubah,

compiler tidak error,

atau satu test kebetulan pass.

Verification harus memberikan evidence bahwa:

behavior yang sebelumnya bermasalah sekarang benar,

root cause memang tertangani,

dan regression relevan tidak muncul.

Jika verification gagal atau hasilnya tidak konklusif, jangan menyebut task selesai. Jelaskan evidence yang masih kurang atau failure yang ditemukan.

OUTPUT AKHIR:

Setelah implementation dan verification selesai, jelaskan secara singkat dan manusiawi:

Permasalahan ini terjadi karena ...

Bagian yang bermasalah ...

Solusinya ...

Kenapa solusi ini dipilih ...

Cara membuktikan fix berhasil ...

Tambahkan limitation atau verification yang tidak dapat dilakukan hanya jika memang ada.

Jangan hanya memberi daftar file yang berubah.

Pastikan penjelasan menunjukkan hubungan sebab-akibat antara:

permasalahan
→
alur/code yang bermasalah
→
root cause
→
perubahan
→
evidence bahwa fix bekerja.
