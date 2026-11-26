# Worked examples

Each example shows the raw prompt, what the run found, and the full reply. The project facts are
part of each scenario; a real run reads them from the project.

## Example 1: a strong prompt with workflow members

Scenario: the working directory holds the old landing page. `package.json` runs Astro 4 with
scripts `dev`, `build` and `test` (`vitest run`); the CSS is spread over 14 files in `src/styles/`.
The host block lists every named skill and MCP, and describes `playwright` as UI checks at 360, 768
and 1440 px.

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

fakta proyek (dicek):
- Web lama memakai Astro 4 (`package.json`); `npm run dev` menjalankannya, `npm test` menjalankan Vitest.
- CSS web lama tersebar di 14 file di `src/styles/`.

batasan:
- Konsep dan market tetap sama.
- Tanpa regresi performa.

selesai jika:
- Web baru di C:\work\landing\new-app memakai konsep dan market yang sama.
- Performa web baru tidak lebih buruk dari web lama.

verifikasi:
1. Ukur performa web lama sebelum membangun, lalu ukur web baru dengan cara yang sama.
2. Periksa web baru dengan playwright di lebar 360, 768 dan 1440 px.
3. Cocokkan hasil dengan `selesai jika` dan laporkan hasil cek yang sebenarnya.
```

| Jenis | Isi |
| --- | --- |
| Kuat | Skill, mode, mcp, urutan kerja dan referensi sudah lengkap; semuanya tetap di urutan Anda. |
| Diubah | Paragraf dipecah, salah ketik diperbaiki, referensi dan urutan kerja dikumpulkan. |
| Ditambah | `fakta proyek` dari `package.json` dan `src/styles/`; `batasan` dan `selesai jika` dari kalimat Anda; `verifikasi` memakai lebar playwright dari blok Lapis 1 di `~/.claude/CLAUDE.md`. |

Mau saya jalankan prompt ini di sesi ini?

## Example 2: a weak prompt

Scenario: the working directory is a Next.js shop with a home page, a product page and a cart
page. Nothing says which part the user dislikes.

### Raw prompt

```text
tolong remake web ini
```

### Output

```text
tolong remake web ini
```

| Jenis | Isi |
| --- | --- |
| Diubah | Tidak ada: maksudnya jelas, tetapi fakta yang menentukan hasilnya belum ada, jadi belum ada blok yang ditambahkan. |
| Tidak dicek | Inventaris dari blok Lapis 1 di `~/.claude/CLAUDE.md`; tidak ada skill atau MCP yang disebut. |

Pertanyaan:
1. "Web ini" maksudnya toko Next.js di folder ini (beranda, halaman produk, keranjang), atau web lain?
2. Apa yang tidak Anda sukai dari web sekarang: tampilan, kecepatan, atau tampilan di HP?
3. Seperti apa hasil yang Anda anggap selesai?

Mau saya jalankan prompt ini di sesi ini setelah Anda menjawab?

## Example 3: template labels

Scenario: a Django project. `pyproject.toml` runs tests with `pytest`; `invoices/pdf.py` defines
`render_invoice`, tested in `invoices/tests/test_pdf.py`. `AGENTS.md` says money is stored as
`Decimal`.

### Raw prompt

```text
Skills: andino-workflow, andino-debugging
Mode: just do it

Task: invoice PDF shows VAT 11% on the discounted line as 0. fix invoices/pdf.py
```

### Output

```text
Skills: andino-workflow, andino-debugging
Mode: just do it

Task: Invoice PDF shows VAT 11% on the discounted line as 0. Fix invoices/pdf.py.

Context/evidence:
- `invoices/pdf.py` defines `render_invoice`; its tests are in `invoices/tests/test_pdf.py` (checked).
- Tests run with `pytest` (`pyproject.toml`); `AGENTS.md` stores money as `Decimal`.

Done when:
- The discounted line on the invoice PDF shows VAT 11%, not 0.
- A test that failed on the discounted line first now passes, and `pytest` passes.
```

| Kind | Detail |
| --- | --- |
| Strength | Skills, mode, the file and the wrong value are all given. |
| Added | `Context/evidence` from `invoices/` and `pyproject.toml`; `Done when` from your own sentence plus the verify step for a bug. |

Want me to run this prompt in this session?

## Why each choice

- Example 1 keeps `andino-planning`, `andino-plan-execution` and `andino-delegation` in the
  user's order; the brainstorm-first mode does not replace them. No skill was added to the skill
  line.
- Its added blocks come only from the user's words ("konsep dan market tetap sama", "tanpa
  regresi"), files the run read and the host block. Nothing names a framework for the new site.
- Example 2 adds nothing it would have to guess and asks three questions, the first carrying a guess
  from the project.
- Example 3 keeps the template labels and puts the additions in the template's own slots; it names
  where the code and tests are, not what is wrong in them.
