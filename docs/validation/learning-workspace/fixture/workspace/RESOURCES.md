# PostgreSQL Query Plan Resources

## Knowledge

- [PostgreSQL 16 docs: 14.1 Using EXPLAIN](https://www.postgresql.org/docs/16/using-explain.html)
  Sumber utama cara membaca plan, cost, rows dan `EXPLAIN ANALYZE`. Use for: semua klaim tentang arti angka di plan.
- [PostgreSQL 16 docs: EXPLAIN](https://www.postgresql.org/docs/16/sql-explain.html)
  Referensi opsi `ANALYZE`, `BUFFERS`, `FORMAT`. Use for: sintaks dan efek tiap opsi.
- [Use The Index, Luke (Markus Winand)](https://use-the-index-luke.com/)
  Penjelasan index B-tree dan kapan index dipakai. Use for: selektivitas, index komposit, urutan kolom.

## Wisdom (Communities)

(Belum dibahas dengan user.)

## Gaps

- Cara melihat SQL yang dihasilkan Laravel query builder untuk endpoint yang lambat.
