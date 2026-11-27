# Bisa membaca pohon plan dari bawah ke atas

User menunjuk Parallel Seq Scan on orders sebagai node yang paling makan waktu di query laporannya
dan menjelaskan kenapa waktu Hash Join hampir seluruhnya berasal dari child itu.

**Evidence**: penjelasan user sendiri atas plan query `orders` di sesi kedua, tanpa petunjuk.
