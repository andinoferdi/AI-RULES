Waktu promo 12.12 tahun lalu, promonya berakhir jam 00.00, tapi halaman produk masih menampilkan harga promo. Pembeli yang checkout memakai harga lama itu. Yang menyadarinya duluan bukan monitoring kami, tapi tim CS: ada pembeli yang bertanya kenapa harga di keranjang berbeda dengan harga di halaman produk.

Saya sendiri baru tahu kejadian ini besok paginya, dari grup CS.

Penyebabnya ada di cara kedua halaman itu membaca harga. Halaman produk membaca dari cache di Redis, yaitu salinan data yang disimpan terpisah dari database. Keranjang membaca langsung dari database. Jadi dua tempat itu bisa berbeda.
