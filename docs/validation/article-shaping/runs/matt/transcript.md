# Transcript

## Author message 1

Saya punya bahan mentah di `raw.md`. Tolong bentuk jadi artikel untuk blog engineering tim kami, simpan di `article.md`.

## Reply 1

Saya sudah baca `raw.md` sampai habis. Artikelnya akan saya simpan di `article.md`, dan belum saya tulis apa pun karena pembukanya harus Anda pilih dulu. `raw.md` tidak saya ubah.

## 1. Pengetahuan pembaca di awal

Saya usulkan yang dianggap sudah dipahami pembaca sejak awal:
- Apa itu cache dan TTL.
- Bahwa halaman produk dan keranjang itu dua bagian berbeda dari sistem.
- Redis sebagai nama alat. Cukup disebut sebagai tempat cache, tanpa penjelasan.

Yang saya jelaskan di dalam artikel:
- "Sumber kebenaran". Ini inti artikelnya, jadi harus mendarat bersama istilahnya.
- Invalidation berbasis event. Ini hanya perlu dijelaskan satu kalimat.

Pembaca blog engineering internal biasanya sudah paham cache dan TTL. Kalau pembacanya juga mencakup tim non-teknis, tolong bilang, karena itu mengubah porsi penjelasan di awal.

## 2. Tiga kandidat pembuka

Masing-masing membawa sudut dan tesis yang berbeda.

**A. Kejadian dulu (tesis: bug ini ketahuan lewat komplain, bukan lewat sistem)**
> Pukul 00.00, promo 12.12 selesai. Pukul berapa kami sadar harga di halaman produk masih harga promo? Bukan dari monitoring. Seorang pembeli menulis ke CS: kenapa harga di keranjang beda dengan di halaman produk?

Pembaca langsung masuk ke kejadian. Pertanyaan "kenapa bisa tidak ketahuan" nanti mengarah ke soal kepemilikan.

**B. Analogi dulu (tesis: cache itu papan harga, dan pembeli tidak salah)**
> Cache itu seperti papan harga kapur di warung. Kalau yang jualan lupa menghapus, pembeli tetap melihat harga kemarin. Dan pembeli tidak salah: dia membaca apa yang tertulis.

Nadanya ringan dan mudah diingat. Risikonya, analogi muncul sebelum pembaca tahu kejadiannya, jadi kurang berbobot.

**C. Pernyataan Raka (tesis: akar masalahnya organisasi, bukan teknologi)**
> Saat retro, Raka, backend lead kami, berkata: "Masalahnya bukan cache-nya, tapi kita nggak pernah nulis siapa yang boleh bilang harga itu benar."

Tesisnya paling tajam dan paling berbeda dari artikel cache pada umumnya. Risikonya, pembaca belum tahu apa yang terjadi, jadi kutipannya belum terasa.

Saya cenderung A atau hibrida A+B. Kejadian dibuka sebagai pembuka, lalu papan kapur muncul di blok kedua untuk memberi nama pada masalahnya. Judul bisa mengikuti: "Cache tanpa pemilik" cocok untuk C atau hibrida, "Harga yang nyangkut di cache" cocok untuk A dan B.

## 3. Celah di bahan mentah

- **Dampaknya belum ada angka.** Di catatan, jumlah pesanan yang kena belum dicek dan finance hanya bilang "beberapa". Kalau ingin dampaknya terasa, saya butuh angkanya, atau kita tulis terus terang bahwa angkanya belum diketahui. Saya tidak akan mengarang.
- **Klaim 11.11 belum bisa dipakai sebagai bukti.** Catatan sendiri bilang belum jelas apakah tidak adanya komplain itu karena fix-nya atau karena promonya lebih kecil. Kalau dipakai, harus dengan catatan itu.
- **Redis vs Memcached dan masalah CDN gambar.** Keduanya tidak relevan dengan argumen. Saya usulkan dibuang.

Pertanyaan untuk Anda:
1. Pilih A, B, C, atau hibrida?
2. Pembacanya hanya engineer, atau ada non-teknis juga?
3. Untuk celah dampak: ada angka yang bisa Anda berikan, atau kita tulis apa adanya sebagai "belum dihitung"?

## Author message 2

Pembacanya developer web yang sudah biasa bikin aplikasi CRUD dan pakai database relasional, tapi belum pernah ngurus cache di production. Saya pilih opening pertama yang kamu tawarkan. Untuk hal lain yang kamu tanyakan, ikuti rekomendasimu.

## Reply 2

Opening A sudah saya tulis ke `C:\Users\Andino\AppData\Local\Temp\claude\8149af24626539c8\4761f6ae-4e94-4c8f-bd02-d49e710d5a9d\scratchpad\trial\arm1\run\article.md`. Isinya judul "Harga yang nyangkut di cache" dan dua paragraf: promo 12.12 selesai pukul 00.00 tapi halaman produk masih memajang harga promo, pembeli checkout dengan harga lama, dan yang pertama sadar adalah CS lewat komplain beda harga keranjang vs halaman produk, bukan monitoring. Belum ada kata "cache" selain di judul, karena belum dijelaskan.

Karena pembaca developer web yang belum pernah mengurus cache di production, saya mengubah rencana prasyarat. Cache, TTL, dan alasan kenapa dua halaman bisa menampilkan harga berbeda tidak lagi dianggap sudah dipahami. Semuanya diperkenalkan di dalam artikel. Yang masih dianggap diketahui hanya database relasional, CRUD, dan bahwa halaman produk dan keranjang adalah bagian sistem yang berbeda.

Sisanya saya ikuti sesuai rekomendasi: papan kapur dipakai sebagai blok kedua (hibrida A+B), dampaknya ditulis apa adanya sebagai "belum dihitung", klaim 11.11 diberi catatan ketidakpastian, dan Redis vs Memcached serta CDN gambar dibuang.

Pilihan blok berikutnya, semuanya bisa dicapai dari konsep yang sudah mendarat:
1. **Papan kapur (menanamkan konsep cache).** Cache sebagai salinan yang dibaca pembeli, halaman produk baca dari cache sementara keranjang langsung dari database, jadi keduanya bisa berbeda. Pembeli tidak salah, dia membaca yang tertulis. Menanamkan: cache, salinan vs asal. Ini rekomendasi saya.
2. **Penjelasan mekanisme singkat tanpa analogi.** Halaman produk baca dari cache, keranjang baca dari database, jadi dua tempat itu bisa beda. Menanamkan hal yang sama tapi lebih kering.
3. **Kenapa TTL 6 jam.** Alasannya dulu agar database tidak keteteran saat traffic tinggi, dan tidak ada yang ingat siapa yang mengaturnya (commit hanya tertulis "tuning"). Ini butuh cache sudah tertanam, jadi hanya bisa menyusul setelah blok 1 atau 2.

Mohon konfirmasi: lanjut ke blok 1, atau ada arah lain?

(Parent: author edit appended to article.md after this reply.)

## Author message 3

Lanjut dengan kandidat pertama.

## Reply 3

Blok kedua sudah ditambahkan ke `C:\Users\Andino\AppData\Local\Temp\claude\8149af24626539c8\4761f6ae-4e94-4c8f-bd02-d49e710d5a9d\scratchpad\trial\arm1\run\article.md`.

Sebelum menulis, saya baca ulang file dari disk dan menemukan satu kalimat yang bukan dari saya: "Saya sendiri baru tahu kejadian ini besok paginya, dari grup CS." Kalimat itu saya biarkan apa adanya. Satu hal perlu Anda putuskan: kalimat itu memakai "saya", sedangkan paragraf di sekitarnya memakai "kami", dan fakta "tahu besok paginya" tidak ada di `raw.md`. Tidak saya ubah. Kalau mau disamakan, bilang saja.

Blok kedua (dua paragraf) menjelaskan bahwa keranjang membaca harga langsung dari database, sedangkan halaman produk membaca dari cache, yaitu salinan harga yang disimpan di tempat yang lebih cepat (Redis) supaya database tidak dihantam. Selama salinan belum diperbarui, dua tempat itu bisa menampilkan angka berbeda. Lalu analogi papan harga kapur di warung, dengan penutup bahwa pembeli tidak salah karena dia membaca apa yang tertulis. Redis hanya disebut sebagai nama alat, tanpa perbandingan dengan Memcached.

Yang sekarang sudah tertanam: cache sebagai salinan, perbedaan asal vs salinan, dan kenapa dua halaman bisa beda. TTL, sumber kebenaran, dan invalidation belum.

Pilihan blok berikutnya, semuanya bisa dicapai dari yang sudah tertanam:
1. **Kenapa salinannya bisa sampai salah (TTL 6 jam).** Menanamkan TTL: salinan kedaluwarsa otomatis setelah waktu tertentu, dulu diatur 6 jam agar database tidak keteteran saat traffic tinggi, dan tidak ada yang ingat siapa yang mengaturnya (commit hanya tertulis "tuning"). Ini rekomendasi saya karena menjawab "kenapa bisa nyangkut" dan menyiapkan soal kepemilikan.
2. **Dampak apa adanya.** Berapa pesanan yang kena belum dihitung, finance hanya bilang "beberapa", dan bagian ini menyatakan itu terus terang. Tidak menanamkan konsep baru, tapi menaruh bobot sebelum masuk solusi.
3. **Pernyataan Raka lebih awal.** "Masalahnya bukan cache-nya, tapi kita nggak pernah nulis siapa yang boleh bilang harga itu benar." Menanamkan kerangka tesis, tapi istilah "sumber kebenaran" belum bisa dipakai penuh sebelum TTL dan solusi.

Mohon pilih satu, atau arah lain.

## Author message 4 (E, final)

Untuk bagian berikutnya, saya mau pembaca langsung merasa seberapa parah kejadiannya. Tulis langsung ke file ya.

## Reply 4 (final)

Blok ketiga sudah saya tulis langsung ke `C:\Users\Andino\AppData\Local\Temp\claude\8149af24626539c8\4761f6ae-4e94-4c8f-bd02-d49e710d5a9d\scratchpad\trial\arm1\run\article.md` (file saya baca ulang dulu; isi sebelumnya utuh, termasuk kalimat "Saya sendiri baru tahu..." yang Anda tambahkan).

Dua paragraf baru membuat pembaca merasakan parahnya tanpa angka yang dikarang. Paragraf pertama: yang parah bukan angkanya salah, tapi setiap pembeli membaca janji toko sendiri yang sudah kedaluwarsa, tidak ada alarm, dan satu-satunya sinyal adalah pembeli teliti yang menulis ke CS. Paragraf kedua: jumlah pesanan terdampak belum diketahui (data order belum diperiksa ulang, finance hanya bilang "beberapa"), dan ketidaktahuan itu dijadikan poin soal seberapa buta kami waktu itu.

Celah yang tetap terbuka: bahan mentah tidak punya angka dampak. Kalau Anda punya jumlah pesanan, selisih harga, atau perkiraan kerugian, saya ganti paragraf kedua dengan angka itu. Ada juga satu hal yang tidak saya selesaikan: catatan bilang keranjang membaca harga dari database, tetapi pembeli tetap "checkout pakai harga lama". Bagaimana harga lama itu bisa sampai ke pembayaran belum dijelaskan di pile, dan pembaca developer kemungkinan akan menanyakannya. Mohon jelaskan alur checkout yang waktu itu terjadi, atau kita tulis kalimat di paragraf pertama lebih hati-hati.

Pilihan blok berikutnya:
1. **Kenapa salinan bisa sampai salah (TTL 6 jam).** Menanamkan TTL, alasan awal 6 jam (database tidak keteteran saat traffic tinggi), dan tidak ada yang ingat siapa yang mengaturnya (commit hanya "tuning"). Rekomendasi saya.
2. **Pernyataan Raka.** Menanamkan tesis soal kepemilikan lebih awal, tapi lebih kuat setelah TTL.
3. **Solusi pertama yang ditolak (turunkan TTL ke 5 menit).** Hanya bisa setelah TTL tertanam.

Mohon pilih satu.

(Session ended after this reply, per the author policy.)
