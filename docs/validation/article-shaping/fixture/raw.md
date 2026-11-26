# catatan mentah: harga nyangkut

- kejadian pas promo 12.12 tahun lalu. harga di halaman produk masih harga promo padahal promonya udah selesai jam 00.00. pembeli checkout pakai harga lama.
- yang ngeh duluan tim CS, bukan monitoring. ada pembeli komplain kenapa harga di keranjang beda sama di halaman produk.
- halaman produk baca dari cache (Redis), keranjang baca langsung dari database. jadi dua tempat itu bisa beda.
- TTL cache halaman produk waktu itu 6 jam. alasannya dulu biar database nggak keteteran pas traffic tinggi.
- nggak ada yang ingat siapa yang set 6 jam. di commit cuma tertulis "tuning".

cache itu kayak papan harga kapur di warung. kalau yang jualan lupa hapus, pembeli tetap lihat harga kemarin. dan pembeli nggak salah, dia baca yang ditulis.

- kami sempat mikir solusinya turunin TTL ke 5 menit. tapi itu cuma mengecilkan jendela salahnya, nggak menutupnya.
- solusi yang akhirnya dipakai: tiap kali harga berubah di admin, sistem langsung hapus cache produk itu (invalidation pakai event). TTL tetap ada, cuma jadi jaring pengaman.
- Raka (backend lead) bilang pas retro: "masalahnya bukan cache-nya, tapi kita nggak pernah nulis siapa yang boleh bilang harga itu benar."
- sumber kebenaran harga = tabel prices di database. cache cuma salinan. ini yang dulu nggak pernah ditulis di mana pun.
- ada debat apakah keranjang harus cek ulang harga pas checkout. akhirnya iya: checkout selalu ambil harga dari database, dan kalau beda dari yang dilihat pembeli, pembeli dikasih tahu dulu sebelum bayar.
- (belum tahu berapa pesanan yang kena. data order waktu itu belum dicek ulang. finance cuma bilang "beberapa".)
- sempat debat Redis vs Memcached, ujungnya tetap Redis karena udah dipakai buat session. nggak terlalu relevan sih.

pelajaran: tiap cache harus bisa jawab dua pertanyaan. siapa sumber kebenarannya, dan kapan salinannya dibuang.

- promo 11.11 tahun ini nggak ada komplain harga. tapi kami belum yakin itu karena fix-nya atau karena promonya lebih kecil.
- ide judul: "Harga yang nyangkut di cache" / "Cache tanpa pemilik"
- ada juga masalah gambar produk yang lama ke-cache di CDN, tapi itu cerita lain.
