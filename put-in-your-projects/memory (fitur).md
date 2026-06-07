# Memory Fitur: [NAMA_FITUR]

Dokumen ini adalah sumber konteks utama untuk melanjutkan pengerjaan fitur `[NAMA_FITUR]` pada chat Codex baru.

Codex wajib membaca dokumen ini terlebih dahulu, memeriksa kondisi repo terbaru, lalu melanjutkan implementasi yang sudah ada. Jangan menanyakan ulang keputusan yang sudah ditandai **FINAL**. Hanya tanyakan jika ada requirement baru, keputusan stakeholder terbaru, atau kontradiksi baru yang benar-benar mengubah implementasi.

## Status Pengerjaan Saat Memory Dibuat

- Repo implementasi: `[NAMA_REPO]`.
- Path repo lokal: `[PATH_REPO_LOKAL]`.
- Branch aktif: `[BRANCH_AKTIF]`.
- Target Pull Request: `[TARGET_PR_BRANCH]`.
- URL Pull Request: `[URL_PR]`.
- Status branch remote: `[SUDAH_DIPUSH / BELUM_DIPUSH / BELUM_ADA_REMOTE]`.
- Status conflict PR: `[TIDAK_ADA_CONFLICT / ADA_CONFLICT / SUDAH_DIRESOLVE]`.
- Strategi resolve conflict terakhir: `[MERGE_TARGET_BRANCH / REBASE / CHERRY_PICK / BRANCH_TEMPORARY / BELUM_PERNAH]`.
- Scope implementasi: `[REPO_ATAU_MODUL_YANG_DIKERJAKAN]`.
- Repo, service, atau sistem eksternal yang tidak tersedia di workspace: `[DAFTAR_JIKA_ADA]`.
- Commit penting terakhir:
  - `[COMMIT_SHA_1] [COMMIT_MESSAGE_1]`
  - `[COMMIT_SHA_2] [COMMIT_MESSAGE_2]`
  - `[COMMIT_SHA_3] [COMMIT_MESSAGE_3]`
- Verifikasi terakhir: `[RINGKASAN_VERIFIKASI_TERAKHIR]`.
- Catatan batasan: `[BATASAN_PENTING_SEPERTI_TIDAK_MEMBUAT_UI / TIDAK_PUSH / TIDAK_UBAH_SCHEMA]`.

## Tujuan Fitur - FINAL

`[NAMA_FITUR]` bertujuan untuk `[JELASKAN_TUJUAN_FITUR_DALAM_1_PARAGRAF]`.

Masalah yang diselesaikan:

- `[MASALAH_UTAMA_1]`
- `[MASALAH_UTAMA_2]`
- `[MASALAH_UTAMA_3]`

Pembagian tanggung jawab:

- `[SISTEM_ATAU_MODUL_A]`: `[TANGGUNG_JAWAB_A]`.
- `[SISTEM_ATAU_MODUL_B]`: `[TANGGUNG_JAWAB_B]`.
- `[SISTEM_ATAU_MODUL_C]`: `[TANGGUNG_JAWAB_C]`.

## Kontrak API, Data, atau Interface - FINAL

Gunakan bagian ini untuk mengunci kontrak yang tidak boleh berubah tanpa keputusan baru.

Endpoint, route, command, event, atau interface utama:

```text
[METHOD_ATAU_COMMAND] [PATH_ATAU_NAMA_INTERFACE]
```

Middleware, auth, permission, atau guard:

```text
[NAMA_MIDDLEWARE_ATAU_PERMISSION]
```

Contoh request atau input:

```json
{
  "field_utama": "[CONTOH_NILAI]",
  "field_tambahan": "[CONTOH_NILAI]"
}
```

Aturan request atau input:

- `[FIELD_1]`: `[ATURAN_VALIDASI_ATAU_BUSINESS_RULE]`.
- `[FIELD_2]`: `[ATURAN_VALIDASI_ATAU_BUSINESS_RULE]`.
- `[FIELD_3]`: `[ATURAN_VALIDASI_ATAU_BUSINESS_RULE]`.

Contoh response atau output sukses:

```json
{
  "id": "[ID_DATA]",
  "status": "[STATUS_SUKSES]",
  "message": "[PESAN_SUKSES]"
}
```

Status response, exit code, atau hasil penting:

- `[KODE_SUKSES]`: `[MAKNA_SUKSES]`.
- `[KODE_VALIDASI]`: `[MAKNA_VALIDASI_GAGAL]`.
- `[KODE_AUTH]`: `[MAKNA_AUTH_GAGAL]`.
- `[KODE_NOT_FOUND]`: `[MAKNA_DATA_TIDAK_DITEMUKAN]`.
- `[KODE_CONFLICT]`: `[MAKNA_KONFLIK_DATA]`.
- `[KODE_ERROR]`: `[MAKNA_ERROR_INTEGRASI_ATAU_SERVER]`.

## Flow Implementasi - FINAL

Flow utama saat data belum tersedia:

1. `[LANGKAH_CREATE_ATAU_PROSES_BARU_1]`.
2. `[LANGKAH_CREATE_ATAU_PROSES_BARU_2]`.
3. `[LANGKAH_CREATE_ATAU_PROSES_BARU_3]`.
4. `[LANGKAH_CREATE_ATAU_PROSES_BARU_4]`.
5. `[LANGKAH_CREATE_ATAU_PROSES_BARU_5]`.

Flow saat data sudah tersedia atau request diulang:

1. `[LANGKAH_IDEMPOTENT_1]`.
2. `[LANGKAH_IDEMPOTENT_2]`.
3. `[LANGKAH_IDEMPOTENT_3]`.

Aturan transaksi, locking, dan pencegahan duplikasi:

- `[ATURAN_UNIQUE_CONSTRAINT_ATAU_LOCKING]`.
- `[ATURAN_TRANSACTION]`.
- `[ATURAN_RETRY_ATAU_IDEMPOTENCY]`.

## Aturan Bisnis - FINAL

- `[BUSINESS_RULE_1]`.
- `[BUSINESS_RULE_2]`.
- `[BUSINESS_RULE_3]`.
- `[BUSINESS_RULE_4]`.
- `[BUSINESS_RULE_5]`.

Informasi lama yang sudah tidak berlaku:

- `[KEPUTUSAN_LAMA_1]` **SUDAH TIDAK BERLAKU** karena `[ALASAN_ATAU_KEPUTUSAN_TERBARU]`.
- `[KEPUTUSAN_LAMA_2]` **SUDAH TIDAK BERLAKU** karena `[ALASAN_ATAU_KEPUTUSAN_TERBARU]`.

## Metadata Teknis - FINAL

Lokasi penyimpanan metadata:

- Tabel, collection, file, cache key, atau model: `[NAMA_STORAGE_METADATA]`.
- Alasan memakai lokasi ini: `[ALASAN_ARSITEKTUR_ATAU_KEPUTUSAN_STAKEHOLDER]`.

Field penting:

- `[FIELD_METADATA_1]`: `[FUNGSI_FIELD_1]`.
- `[FIELD_METADATA_2]`: `[FUNGSI_FIELD_2]`.
- `[FIELD_METADATA_3]`: `[FUNGSI_FIELD_3]`.
- `[FIELD_METADATA_4]`: `[FUNGSI_FIELD_4]`.

Aturan metadata:

- Jangan menghapus `[NAMA_STORAGE_METADATA]` tanpa arahan arsitektur baru yang eksplisit.
- Jangan memindahkan metadata ke lokasi lain tanpa keputusan stakeholder terbaru.
- Metadata ini dipakai untuk `[TUJUAN_METADATA]`, bukan untuk `[HAL_YANG_BUKAN_TUJUAN_METADATA]`.

## Logging dan Observability - FINAL

Log, audit trail, metric, atau tracing yang wajib tersedia:

- `[EVENT_LOG_1]`: `[KONTEKS_AMAN_YANG_DILOG]`.
- `[EVENT_LOG_2]`: `[KONTEKS_AMAN_YANG_DILOG]`.
- `[EVENT_LOG_3]`: `[KONTEKS_AMAN_YANG_DILOG]`.
- `[EVENT_LOG_4]`: `[KONTEKS_AMAN_YANG_DILOG]`.

Jangan log:

- Authorization header.
- API token.
- Credential.
- Isi `.env`.
- Private key.
- Payload besar yang tidak diperlukan untuk debugging.
- Data sensitif user, customer, atau transaksi di luar kebutuhan investigasi.

## Peta Implementasi

- `[PATH_FILE_ATAU_MODUL_1]`: `[TANGGUNG_JAWAB_FILE_ATAU_MODUL_1]`.
- `[PATH_FILE_ATAU_MODUL_2]`: `[TANGGUNG_JAWAB_FILE_ATAU_MODUL_2]`.
- `[PATH_FILE_ATAU_MODUL_3]`: `[TANGGUNG_JAWAB_FILE_ATAU_MODUL_3]`.
- `[PATH_FILE_ATAU_MODUL_4]`: `[TANGGUNG_JAWAB_FILE_ATAU_MODUL_4]`.
- `[PATH_TEST_1]`: `[CAKUPAN_TEST_1]`.
- `[PATH_TEST_2]`: `[CAKUPAN_TEST_2]`.

Konstanta, config, env, atau command penting:

```text
[NAMA_CONSTANT_OR_CONFIG]=[NILAI_FINAL]
[COMMAND_VERIFIKASI_ATAU_COMMAND_FITUR]
```

## Keputusan Yang Jangan Ditanyakan atau Diubah Ulang

- `[KEPUTUSAN_FINAL_1]`.
- `[KEPUTUSAN_FINAL_2]`.
- `[KEPUTUSAN_FINAL_3]`.
- `[KEPUTUSAN_FINAL_4]`.
- `[KEPUTUSAN_FINAL_5]`.
- Jangan push tanpa permintaan pengguna.
- Jangan mengubah scope di luar `[SCOPE_FINAL]` tanpa instruksi baru.

## Verifikasi Terakhir

Hasil verifikasi terakhir:

- `[COMMAND_ATAU_TEST_1]`: `[HASIL_1]`.
- `[COMMAND_ATAU_TEST_2]`: `[HASIL_2]`.
- `[COMMAND_ATAU_TEST_3]`: `[HASIL_3]`.
- `[CHECK_MANUAL_1]`: `[HASIL_CHECK_MANUAL_1]`.
- `[CHECK_GIT_DIFF]`: `[HASIL_CHECK_GIT_DIFF]`.

Verifikasi yang belum bisa dijalankan:

- `[COMMAND_ATAU_TEST_YANG_GAGAL]`: belum bisa dijalankan karena `[ALASAN]`.
- Jangan menganggap kegagalan environment seperti `[CONTOH_DATABASE_TIDAK_TERSEDIA]` sebagai kegagalan business logic sebelum diverifikasi ulang.

## Checklist Chat Codex Berikutnya

1. Baca dokumen ini sebelum membaca file lain.
2. Periksa `git status` pada repo `[NAMA_REPO]`.
3. Jangan membuat ulang fitur yang sudah tersedia.
4. Cocokkan perubahan baru dengan keputusan **FINAL** dalam dokumen ini.
5. Prioritaskan jawaban terbaru dari `[NAMA_STAKEHOLDER]` jika ada keputusan baru setelah memory dibuat.
6. Jalankan targeted test terlebih dahulu sebelum regression test yang lebih luas.
7. Jangan push tanpa permintaan pengguna.
8. Jika PR conflict lagi karena `[TARGET_PR_BRANCH]` berubah, audit diff terlebih dahulu dan gunakan strategi paling aman sesuai `git-branch-tips.md`.

## Urutan Sumber Kebenaran

Jika ditemukan informasi yang bertentangan, gunakan urutan berikut:

1. Jawaban terbaru `[NAMA_STAKEHOLDER_UTAMA]` mengenai business rule.
2. Jawaban terbaru `[NAMA_STAKEHOLDER_TEKNIS]` mengenai arsitektur dan lokasi metadata.
3. Task atau dokumen requirement terbaru: `[PATH_TASK_ATAU_REQUIREMENT_TERBARU]`.
4. Implementasi dan test pada branch `[BRANCH_AKTIF]`.
5. Chat, transcript, atau catatan lama hanya sebagai konteks historis.

Catatan: `[DAFTAR_USULAN_LAMA_ATAU_KEPUTUSAN_BATAL]` bukan keputusan final kecuali dikonfirmasi ulang oleh sumber kebenaran yang lebih tinggi.
