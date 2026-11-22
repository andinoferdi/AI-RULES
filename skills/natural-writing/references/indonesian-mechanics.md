# Mekanika bahasa Indonesia

Acuan untuk Proofread, Edit dan Review pada teks berbahasa Indonesia: ejaan,
kata baku, angka, singkatan dan istilah serapan. Rujukan umum: EYD Edisi V dan
KBBI. Pedoman gaya kampus, jurnal atau proyek menang bila berbeda. Pada level
Proofread, bagian ini adalah seluruh cakupan perubahan; susunan kalimat yang
sudah benar tidak disentuh.

`scripts/check.py scan` menandai sebagian pola di bawah (`nonbaku:*`, verba
ringan, subjek hilang). Tanda itu petunjuk; periksa konteksnya sebelum mengubah.

## Kata depan dan awalan

- Kata depan *di*, *ke*, *dari* ditulis terpisah dari kata yang menunjukkan
  tempat atau arah: *di rumah*, *ke kantor*, *di antara*, *di samping*, *ke depan*,
  *di mana* (bertanya tempat).
- Awalan *di-* dan *ke-* ditulis serangkai dengan kata kerja atau bentuk
  turunan: *dibaca*, *diubah*, *ketua*, *kemari*, *kedua*.
- Uji cepat: bila kata sesudahnya bisa diawali "tempat", itu kata depan.
- *Kedepan* dan *diantara* sebagai satu kata salah dalam teks baku.

## Gabungan kata

- Ditulis terpisah bila berdiri sendiri: *kerja sama*, *tanggung jawab*,
  *orang tua*, *rumah sakit*.
- Mendapat awalan saja atau akhiran saja: tetap terpisah, imbuhan menempel pada
  kata terdekat: *bertanggung jawab*, *kerja samanya*.
- Mendapat awalan dan akhiran sekaligus: serangkai: *pertanggungjawaban*,
  *dikerjasamakan*, *menindaklanjuti*.
- Yang sudah padu ditulis serangkai: *kacamata*, *saputangan*, *matahari*,
  *olahraga*, *bilamana*, *daripada*.
- Unsur terikat ditulis serangkai: *antarkota*, *pascasarjana*, *nonformal*,
  *subbagian*, *multiguna*. Pakai tanda hubung bila unsur kedua diawali huruf
  kapital atau angka: *non-Indonesia*, *pra-2020*.

## Angka dan satuan

- Bilangan yang dapat ditulis dengan satu atau dua kata ditulis dengan huruf
  dalam prosa: *tiga kecamatan*, *dua puluh peserta*. Data, statistik, tabel,
  ukuran dan rincian teknis tetap angka: *120 responden*, *30 epoch*.
- Bilangan di awal kalimat ditulis dengan huruf, atau kalimatnya disusun ulang
  supaya angka tidak di awal.
- Desimal memakai koma: *12,5*. Ribuan memakai titik: *1.250*. Jangan menukar
  keduanya; menulis ulang *12,5%* menjadi *12.5%* mengubah nilai.
- Persen ditulis rapat: *62%*. Satuan diberi spasi: *5 kg*, *20 menit*, *37 °C*.
- Rentang memakai tanda pisah pendek atau kata *sampai*: *2019–2023*,
  *10 sampai 15 menit*.
- Mengubah *3 kali* menjadi *tiga kali* adalah penyesuaian ejaan, bukan
  perubahan nilai; sebutkan di catatan perubahan karena `compare` akan melihat
  angka yang hilang.

## Huruf kapital

- Kapital untuk nama diri, lembaga dan dokumen resmi: *Universitas Gadjah Mada*,
  *Undang-Undang Nomor 27 Tahun 2022*.
- Jabatan berkapital bila diikuti nama orang atau merujuk orang tertentu:
  *Rektor Ari Wibowo*; huruf kecil bila umum: *setiap rektor*.
- Judul karya: kapital di awal setiap kata kecuali kata tugas yang tidak di awal
  (*di*, *ke*, *dan*, *yang*, *untuk*).
- Nama geografi berkapital bila menjadi nama diri: *Sungai Musi*; huruf kecil
  bila jenis: *berenang di sungai*.

## Tanda baca

- Koma sebelum *tetapi*, *melainkan*, *sedangkan*: *Datanya lengkap, tetapi
  belum dibersihkan.*
- Koma sesudah anak kalimat yang mendahului induk kalimat: *Jika kode
  kedaluwarsa, pengguna meminta kode baru.* Tanpa koma bila anak kalimat di
  belakang.
- Tidak ada koma sebelum *bahwa* dalam kalimat biasa.
- Koma sesudah ungkapan penghubung antarkalimat: *Oleh karena itu, ...*
- Spasi sesudah tanda baca, bukan sebelumnya.

## Kata baku

Daftar ini sama dengan yang diperiksa `scan`. Kata dalam kutipan langsung,
nama diri dan judul karya tidak diubah.

| Tidak baku | Baku | Tidak baku | Baku |
| --- | --- | --- | --- |
| analisa | analisis | merubah, dirubah | mengubah, diubah |
| resiko | risiko | mempengaruhi | memengaruhi |
| praktek | praktik | ijin | izin |
| aktifitas | aktivitas | jaman | zaman |
| efektifitas | efektivitas | silahkan | silakan |
| produktifitas | produktivitas | sekedar | sekadar |
| kwalitas | kualitas | obyek, subyek | objek, subjek |
| tehnik | teknik | frekwensi | frekuensi |
| jadual | jadwal | nasehat | nasihat |
| hakekat | hakikat | propinsi | provinsi |
| apotik | apotek | antri | antre |
| standarisasi | standardisasi | sistim | sistem |
| ketrampilan | keterampilan | kedepan, diantara | ke depan, di antara |

Peluluhan *k, p, t, s* tetap berlaku pada kata dasar asing yang sudah diserap:
*memengaruhi*, *memopulerkan*, *menerjemahkan*. Gugus konsonan tidak luluh:
*mengkritik*, *memproduksi*, *menstabilkan*.

## Verba ringan

Ubah ke kata kerja langsung bila maknanya sama:

| Bentuk panjang | Bentuk langsung |
| --- | --- |
| melakukan pengujian terhadap | menguji |
| melakukan analisis terhadap | menganalisis |
| melakukan pengukuran | mengukur |
| melakukan perbaikan | memperbaiki |
| memberikan pengaruh terhadap | memengaruhi |
| memberikan bantuan kepada | membantu |
| mengalami peningkatan sebesar | meningkat sebesar |
| mengalami penurunan | menurun |

Pertahankan bentuk panjang bila nominanya justru topik kalimat (*pengujian
dilakukan dua kali*) atau bila konvensi bidang memintanya.

## Singkatan dan akronim

- Tulis kepanjangan pada kemunculan pertama, singkatan dalam kurung: *usaha
  mikro, kecil, dan menengah (UMKM)*. Sesudahnya pakai singkatannya secara
  konsisten.
- Kepanjangan yang tidak ada di teks dan tidak pasti jangan ditebak; banyak
  singkatan bermakna ganda. Tulis `[PERLU DATA: kepanjangan …]`.
- Singkatan umum bertitik: *dll.*, *dsb.*, *yth.*, *a.n.*. Akronim nama lembaga
  tanpa titik: *BRIN*, *LIPI*.

## Istilah asing dan serapan

1. Pakai istilah yang dipakai penulis dan bidangnya. Jangan menerjemahkan paksa
   istilah yang lazim (*dataset*, *framework*, *deep learning*, *stakeholder*).
2. Istilah asing yang belum diserap ditulis miring bila konvensi naskah memakai
   miring; tidak dimiringkan bila pedoman proyek atau gaya teknis tidak memintanya.
3. Pilih satu bentuk per konsep dan pakai sepanjang dokumen. Jika dokumen
   memakai dua bentuk untuk konsep yang sama (*user* dan *pengguna*), pakai bentuk
   yang dominan atau yang diminta, dan sebutkan di catatan perubahan.
4. Serapan baku yang sah tetap: *konduktivitas*, *skalabilitas*, *rekursif*,
   *instansiasi*.
5. Identifier, nama API, perintah dan nama berkas tidak pernah diterjemahkan.

## Jangan dikoreksi

Bentuk berikut sering terlihat seperti kesalahan, padahal sah:

- Pasif *di-* pada bab metode dan hasil (*Sampel diambil secara acak*).
- *Penelitian ini* sebagai subjek kalimat.
- *Merupakan* untuk definisi atau keanggotaan kelas (*Akurasi merupakan proporsi
  prediksi yang benar*).
- Hedging yang disengaja: *diduga*, *cenderung*, *kemungkinan*.
- *Signifikan* dalam arti statistik bila disertai nilai uji.
- Kutipan langsung, judul karya, nama diri dan contoh yang sedang dibahas.
- Ragam santai dalam tulisan yang memang santai (blog pribadi, pesan tim).

## Contoh

1. Sebelum: "Analisa data dilakukan setiap minggu."
   Proofread: "Analisis data dilakukan setiap minggu."
   Alasan: kata tidak baku; susunan kalimat dan pasifnya tetap.
2. Sebelum: "Tim akan mengadakan kerjasama dengan dinas propinsi kedepannya."
   Proofread: "Tim akan mengadakan kerja sama dengan dinas provinsi ke depannya."
   Alasan: gabungan kata, kata baku dan kata depan. Kalimatnya tetap.
3. Sebelum: "Sampel diambil dari 120 responden (p < 0,05)."
   Sesudah: tidak berubah.
   Alasan: KEEP. Pasif metode dan angka statistik sudah benar.
