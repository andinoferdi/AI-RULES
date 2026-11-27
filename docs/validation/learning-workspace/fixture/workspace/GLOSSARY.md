# PostgreSQL Query Plan Glossary

Istilah yang sudah dipakai user dengan benar saat membaca query plan PostgreSQL.

## Terms

**Node**:
Satu langkah dalam pohon plan, misalnya scan, join atau sort, yang menerima baris dari child-nya.
_Avoid_: step, tahap

**Seq Scan**:
Node yang membaca seluruh tabel baris demi baris lalu menyaring dengan Filter.
_Avoid_: full scan, table scan
