# Harga yang nyangkut di cache

Promo 12.12 tahun lalu berakhir tepat pukul 00.00. Setelah jam itu, halaman produk kami masih menampilkan harga promo. Pembeli yang melihat harga itu lalu checkout, dan sebagian membayar harga yang seharusnya sudah tidak berlaku.

Kami tidak tahu dari monitoring. Yang pertama sadar adalah tim CS, karena ada pembeli yang bertanya: kenapa harga di keranjang beda dengan harga di halaman produk?

Saya sendiri baru tahu kejadian ini besok paginya, dari grup CS.

Dua halaman itu ternyata tidak membaca dari tempat yang sama. Keranjang membaca harga langsung dari database. Halaman produk membaca dari cache, yaitu salinan harga yang disimpan di tempat yang lebih cepat (kami memakai Redis) supaya database tidak dihantam setiap kali ada yang membuka halaman. Selama salinan itu belum diperbarui, dua tempat itu bisa menampilkan angka yang berbeda.

Cache mirip papan harga kapur di warung. Kalau yang jualan lupa menghapus, pembeli tetap melihat harga kemarin. Dan pembeli tidak salah: dia membaca apa yang tertulis.

Yang membuat kejadian ini tidak enak bukan sekadar angkanya salah. Setiap pembeli yang melihat harga lama itu sedang membaca janji dari toko kami sendiri, dan janji itu sudah kedaluwarsa tanpa ada yang tahu. Tidak ada alarm yang berbunyi. Satu-satunya tanda bahwa ada yang keliru adalah pembeli yang cukup teliti untuk membandingkan dua halaman, lalu cukup peduli untuk menulis ke CS.

Berapa pesanan yang terdampak? Kami belum tahu. Data order saat itu belum kami periksa ulang, dan finance hanya menjawab "beberapa". Bahwa kami tidak bisa menyebut angkanya saja sudah menunjukkan seberapa buta kami waktu itu.
