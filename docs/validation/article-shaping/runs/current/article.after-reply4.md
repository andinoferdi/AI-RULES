Promo 12.12 berakhir tepat jam 00.00. Halaman produk tidak tahu. Pembeli yang membukanya masih melihat harga promo dan checkout di harga itu. Orang pertama yang sadar bukan sistem monitoring kami, tapi tim CS yang menerima komplain: kenapa harga di keranjang beda dengan di halaman produk?

Penyebabnya ada di cara dua halaman itu membaca harga. Keranjang bertanya langsung ke database, seperti query biasa yang kamu tulis di aplikasi CRUD. Halaman produk tidak. Ia membaca dari cache di Redis: salinan data yang disimpan sementara, supaya database tidak dihujani query yang sama berulang-ulang saat traffic tinggi. Salinan itu bisa tertinggal dari aslinya. Jadi untuk produk yang sama, dua tempat bisa menunjukkan dua harga.

Seberapa lama salinan itu bertahan? Setiap cache punya masa berlaku yang disebut TTL, dan di halaman produk kami nilainya 6 jam. Artinya, harga promo yang tersimpan sebelum jam 00.00 bisa tetap tampil sampai jam 6 pagi, dan selama itu pembeli yang checkout membayar harga yang sudah tidak berlaku. Tidak ada alarm yang berbunyi. Dari sisi sistem, semuanya tampak berjalan normal.

[GAP: berapa pesanan yang terkena. Data order belum dicek ulang, finance hanya bilang "beberapa". Perlu angka dari data order, atau tulis terus terang bahwa kami belum menghitung.]
