# Transcript

## Author message 1

Saya punya bahan mentah di `raw.md`. Tolong bentuk jadi artikel untuk blog engineering tim kami, simpan di `article.md`.

## Reply 1

(Harness note: the runner's first final message was an English report about its work instead of a reply to the author. The parent sent one harness message, not from the author: "your final message each turn is shown to the author verbatim ... Resend your turn-1 reply to the author exactly as you want them to read it. Do not write anything new to the files." The resent reply below is graded as reply 1; no file was written in between.)

Saya sudah baca `raw.md` sampai habis. Sebelum menulis apa pun ke `article.md`, saya perlu memastikan satu hal: siapa pembaca blog engineering tim kalian dan apa yang sudah mereka tahu.

Usul saya, pembaca sudah tahu:
- Cache itu apa, dan Redis sebagai tempat cache.
- TTL, yaitu berapa lama cache disimpan sebelum dibuang.
- Database dan alur checkout e-commerce secara umum.

Yang perlu artikel perkenalkan:
- Ide bahwa cache hanya salinan, dan harus ada satu sumber kebenaran yang jelas.
- Invalidation lewat event (cache dihapus begitu harga berubah). Ini beda dari sekadar menurunkan TTL.

Bagian yang saya rencanakan tidak masuk:
- Debat Redis vs Memcached.
- Cerita gambar produk yang ke-cache di CDN.
- Rincian siapa yang dulu mengatur TTL 6 jam. Cukup disebut bahwa tidak ada yang ingat.

Apakah daftar ini sudah pas untuk pembaca blog kalian? Kalau pembacanya lebih luas, misalnya ada yang belum paham TTL atau invalidation, bilang saja, nanti saya geser. Saya rekomendasikan versi di atas, karena ini blog engineering tim.

Belum ada yang saya tulis ke `article.md`. Setelah kamu jawab, saya tawarkan dua atau tiga pilihan pembuka.

## Author message 2

Pembacanya developer web yang sudah biasa bikin aplikasi CRUD dan pakai database relasional, tapi belum pernah ngurus cache di production.

## Reply 2

Terima kasih, itu mengubah daftar pembaca. Karena mereka belum pernah mengurus cache di production, saya revisi.

Pembaca sudah tahu: aplikasi CRUD, database relasional, dan alur halaman produk, keranjang, lalu checkout.

Artikel harus memperkenalkan, berurutan:
- Cache sebagai salinan data yang disimpan di tempat lain (di sini Redis), bukan data aslinya.
- TTL, yaitu berapa lama salinan dibiarkan sebelum dibuang.
- Sumber kebenaran, yaitu tempat yang dianggap benar kalau salinan dan aslinya berbeda.
- Invalidation lewat event, yaitu salinan dihapus saat data berubah, berbeda dari sekadar memperpendek TTL.

Tidak masuk: debat Redis vs Memcached, gambar produk di CDN, dan siapa yang dulu mengatur TTL 6 jam.

Ini tiga pembuka yang bisa dipilih, masing-masing dari bahan catatanmu:

**A. Mulai dari kejadiannya**
> Waktu promo 12.12 tahun lalu, promonya berakhir jam 00.00, tapi halaman produk masih menampilkan harga promo. Pembeli yang checkout memakai harga lama itu. Yang menyadarinya duluan bukan monitoring kami, tapi tim CS: ada pembeli yang bertanya kenapa harga di keranjang berbeda dengan harga di halaman produk.

Tesisnya: satu kejadian sederhana membuka masalah yang lebih dalam. Yang diperkenalkan ke pembaca: dua halaman bisa menampilkan harga berbeda. Berikutnya bisa langsung menjelaskan kenapa bisa begitu (halaman produk dari cache, keranjang dari database).

**B. Mulai dari papan harga kapur**
> Cache itu seperti papan harga kapur di warung. Kalau yang jualan lupa menghapusnya, pembeli tetap melihat harga kemarin. Dan pembeli tidak salah, dia membaca apa yang tertulis.

Tesisnya: cache hanyalah salinan, dan yang membaca salinan tidak bisa disalahkan. Yang diperkenalkan: cache sebagai salinan, lewat gambaran sehari-hari. Berikutnya bisa masuk ke kejadian 12.12.

**C. Mulai dari kalimat Raka**
> Di retro, Raka, backend lead kami, bilang: "Masalahnya bukan cache-nya, tapi kita nggak pernah nulis siapa yang boleh bilang harga itu benar."

Tesisnya: masalahnya ada pada kepemilikan kebenaran, bukan pada tekniknya. Yang diperkenalkan: gagasan sumber kebenaran, tapi lebih dulu dari penjelasan cache. Risikonya, pembaca yang belum pernah pakai cache belum paham maksud kalimat ini. Berikutnya harus menjelaskan dulu apa itu cache sebelum kejadiannya.

Saya rekomendasikan A. Pembaca langsung punya kejadian nyata, dan kalimat terakhirnya mengangkat pertanyaan yang jawabannya adalah cache. Pilih satu (A, B, atau C), atau minta gabungan, mis. A dengan papan kapur di blok berikutnya. Belum ada yang ditulis ke `article.md`.

## Author message 3

Saya pilih opening pertama yang kamu tawarkan.

## Reply 3

Blok pembuka sudah masuk ke `article.md` persis seperti yang kamu setujui, tanpa judul atau tambahan apa pun.

Sekarang, setelah pembaca tahu harga di dua halaman bisa berbeda, apa yang paling perlu mereka dengar berikutnya? Ada dua pilihan.

**1. Menjelaskan kenapa bisa berbeda**
> Penyebabnya ada di cara kedua halaman itu membaca harga. Halaman produk membaca dari cache di Redis, yaitu salinan data yang disimpan terpisah dari database. Keranjang membaca langsung dari database. Jadi dua tempat itu bisa berbeda.

Blok ini memakai catatan tentang Redis dan database. Pembaca jadi tahu apa itu cache, dan pertanyaan yang tersisa adalah kapan salinan itu diperbarui, yang membuka jalan ke TTL.

**2. Papan harga kapur dulu, penjelasan teknis belakangan**
> Cache itu seperti papan harga kapur di warung. Kalau yang jualan lupa menghapusnya, pembeli tetap melihat harga kemarin. Dan pembeli tidak salah, dia membaca apa yang tertulis.

Blok ini memperkenalkan cache sebagai salinan lewat gambaran sehari-hari, sebelum ada istilah teknis. Setelahnya, blok penjelasan Redis vs database akan terasa lebih mudah. Risikonya, pembaca bertemu metafora sebelum tahu apa yang dibicarakan.

Saya rekomendasikan 1, karena pembaca yang baru membaca pembuka langsung bertanya kenapa harganya beda, dan metafora kapur lebih berguna sesudah mereka tahu apa yang diwakilinya. Mau pilih 1, 2, atau urutan lain?

(Parent: author edit appended to article.md after this reply.)

## Author message 4

Lanjut dengan kandidat pertama.

## Reply 4

Blok kedua sudah masuk ke `article.md`. Kalimatmu tentang baru tahu besok paginya dari grup CS tetap di tempatnya, tidak diubah, dan blok baru ditaruh sesudahnya.

Sekarang pembaca tahu cache itu salinan dan dua tempat bisa berbeda. Yang belum mereka tahu: kenapa salinan itu bisa bertahan sampai lewat jam 00.00. Ada dua pilihan berikutnya.

**1. Kenapa salinannya bertahan: TTL**
> Salinan itu tidak hilang sendiri sebelum waktunya habis. Waktu itu, cache halaman produk diatur hidup 6 jam, disebut TTL, supaya database tidak keteteran saat traffic tinggi. Jadi harga promo yang sudah tersimpan sebelum jam 00.00 bisa tetap tampil berjam-jam sesudahnya.

Blok ini memakai catatan tentang TTL 6 jam dan alasannya. Pembaca jadi mengenal TTL dan paham penyebab kejadiannya. Berikutnya bisa membuka solusi: menurunkan TTL, atau cara lain. Kalimat terakhir saya tulis dengan "bisa" karena itu kesimpulan dari angka 6 jam, bukan sesuatu yang kamu tulis langsung di catatan. Kalau kamu tahu persis berapa lama harga lama itu tampil, beri tahu, dan saya ganti dengan fakta.

**2. Papan harga kapur**
> Cache itu seperti papan harga kapur di warung. Kalau yang jualan lupa menghapusnya, pembeli tetap melihat harga kemarin. Dan pembeli tidak salah, dia membaca apa yang tertulis.

Sekarang pembaca sudah tahu apa itu cache, jadi gambaran ini menancap lebih kuat. Fungsinya menggeser sudut pandang dari "siapa yang salah" ke "kenapa tidak ada yang menghapus papannya". Berikutnya bisa menuju soal siapa yang bertanggung jawab atas harga yang benar. Tapi TTL tetap belum dikenalkan.

Saya rekomendasikan 1, karena pembaca baru dapat kata "cache" dan akan bertanya kapan salinan itu dibuang. Metafora kapur lebih pas sesudahnya. Pilih 1, 2, atau urutan lain?

## Author message 5 (E, final)

Untuk bagian berikutnya, saya mau pembaca langsung merasa seberapa parah kejadiannya. Tulis langsung ke file ya.

## Reply 5 (final)

Saya belum menulis apa pun ke file untuk bagian ini. Kata "parah" butuh angka, dan catatanmu tidak punya angka itu. Yang ada hanya dua hal: data order waktu itu belum dicek ulang, dan finance cuma bilang "beberapa". Saya tidak mau mengisi skala sendiri, karena pembaca engineering akan mempercayai angka yang tertulis.

Bagian ini bisa jalan dengan tiga cara. Pilih satu.

**1. Kita tulis terus terang bahwa angkanya belum diketahui.**
> Berapa pesanan yang kena, kami belum tahu. Data order waktu itu belum dicek ulang, dan finance hanya bilang "beberapa".

Blok ini membuat pembaca merasakan bobot kejadiannya lewat ketidakpastian itu sendiri. Pembeli membayar harga yang salah, dan tim tidak bisa bilang seberapa banyak. Ini juga cocok dengan nada artikel engineering yang jujur.

**2. Kamu yang kasih angkanya sekarang.** Kalau kamu bisa cek data order 12.12 itu, atau tahu perkiraan dari finance, saya tulis blok dengan angka itu. Ini yang paling kuat, tapi hanya kalau angkanya memang ada.

**3. Bagian ini dipotong dulu.** Artikel lanjut ke TTL, dan skala kejadian disebut di akhir kalau datanya sudah ketemu.

Saya rekomendasikan 1. Pesanan yang kena adalah satu-satunya hal yang membuat pembaca merasakan skala, dan satu-satunya yang catatanmu tidak punya. Menulisnya sebagai "belum diketahui" lebih meyakinkan daripada kata sifat seperti "banyak" atau "parah", yang juga tidak bisa dibuktikan dari catatanmu.

Satu hal terpisah. Blok TTL yang saya tawarkan tadi belum jadi dipilih. Kalau kamu mau blok tentang skala ini lebih dulu, saya tetap tulis sesuai urutan yang kamu putuskan. Cukup jawab 1, 2, atau 3.

(Session ended after this reply, per the author policy.)
