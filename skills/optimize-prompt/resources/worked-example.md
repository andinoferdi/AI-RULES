# Worked examples: light edits

## Example 1: a strong prompt with workflow members

### Raw prompt

```text
skill: andino-workflow, search-first, andino-brainstorming, design-taste-frontend, impeccable, council
mode: brainstorm-first
mcp: context7, playwright

task:
web landing ini dibuat beberapa ai yang beda beda, konsepnya udah bagus tapi arsitekturnya berantakan, css kepisah dan komponennya gak clean. saya mau bikin web baru yang bener bener clean, konsep dan market tetep sama, modern 2026, performa bagus tanpa regresi. tanya dulu maunya saya gimana, terus tanya council, abis itu plan pakai andino-planning dan kerjain pakai andino-plan-execution, sub agent pakai andino-delegation. refrensi yang disuka klien https://example.com/studio sama https://example.org/motion, yang saya suka https://example.net/gallery
implementasikan di: C:\work\landing\new-app
```

### Output

```text
skill: andino-workflow, search-first, andino-brainstorming, design-taste-frontend, impeccable, council
mode: brainstorm-first
mcp: context7, playwright

task:
Web landing ini dibuat beberapa AI yang berbeda-beda. Konsepnya sudah bagus, tapi arsitekturnya berantakan: CSS terpisah dan komponennya tidak clean.

Saya mau web baru yang benar-benar clean, dengan konsep dan market yang tetap sama, modern 2026, dan performa bagus tanpa regresi.

Urutan kerja:
- Tanya dulu maunya saya gimana.
- Lalu tanya council.
- Plan pakai andino-planning, kerjakan pakai andino-plan-execution.
- Sub agent pakai andino-delegation.

referensi:
- disukai klien: https://example.com/studio, https://example.org/motion
- saya suka: https://example.net/gallery

implementasikan di: C:\work\landing\new-app

selesai jika:
- Web baru di C:\work\landing\new-app memakai konsep dan market yang sama.
- Tidak ada regresi performa dibanding web lama.
```

Notes:
- Diubah: paragraf dipecah, salah ketik diperbaiki, referensi dan urutan kerja dikumpulkan; semua skill, mode, mcp dan urutan tetap.
- `selesai jika` ditambahkan dari kalimat Anda sendiri. Inventaris dari blok Lapis 1 di `~/.claude/CLAUDE.md`.

Mau saya jalankan prompt ini di sesi ini?

## Example 2: a weak prompt

### Raw prompt

```text
tolong remake web ini
```

### Output

```text
tolong remake web ini
```

Notes:
- Tidak ada yang diubah: maksud prompt sudah jelas, tetapi faktanya kurang.

Pertanyaan:
1. Web yang mana (path folder atau URL)?
2. Apa yang tidak Anda sukai dari web sekarang?
3. Seperti apa hasil yang Anda anggap selesai?

Mau saya jalankan prompt ini di sesi ini setelah Anda menjawab?

## Why each choice

- Example 1 keeps `andino-planning`, `andino-plan-execution` and `andino-delegation` in the
  user's order; the brainstorm-first mode does not replace them.
- No skill was added to the skill line; a suggestion would go in `Notes`.
- The `selesai jika` block uses only "konsep dan market tetap sama" and "tanpa regresi".
- Example 2 asks three questions instead of guessing a framework, page or style.
