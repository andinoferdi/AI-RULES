# Mission: Membaca query plan PostgreSQL

## Why
Dua endpoint laporan di aplikasi Laravel kantor (PostgreSQL 16) lambat. Aku mau bisa membaca
`EXPLAIN ANALYZE` sendiri, menjelaskan kenapa sebuah query lambat, dan mengusulkan index yang
tepat tanpa menunggu DBA.

## Success looks like
- Menunjuk node yang paling makan waktu di output `EXPLAIN ANALYZE`
- Menjelaskan beda estimasi rows dan actual rows, dan kenapa beda itu penting
- Mengusulkan satu index untuk query laporan yang lambat dan membuktikannya dengan plan sebelum dan sesudah

## Constraints
- 20 menit per hari kerja, sekitar 3 minggu
- Materi dalam Bahasa Indonesia, istilah teknis tetap bahasa Inggris

## Out of scope
- Tuning konfigurasi server (`shared_buffers`, `work_mem`)
- Replikasi dan partisi
