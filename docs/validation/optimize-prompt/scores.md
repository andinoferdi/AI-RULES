# Blind scores: optimize-prompt trial

Grader: one Claude Code subagent, Sonnet 5.5, medium effort. It saw only the rubric (arm names
removed), the fixture and six output folders labelled A to F. Letters revealed after grading:
A = Sentry, B = candidate, C = ECC, D = current `andino-optimize-prompt` (main at 1e78323),
E = Hashaam101, F = GitHub awesome-copilot. The text below the line is the grader's file, unchanged.

---

# Scores (blind)

| ID | A | B | C | D | E | F |
|----|---|---|---|---|---|---|
| K1 | 0 | 2 | 2 | 2 | 2 | 1 |
| K2 | 2 | 2 | 2 | 2 | 2 | 1 |
| K3 | 0 | 2 | 0 | 2 | 0 | 0 |
| K4 | 0 | 2 | 0 | 2 | 0 | 0 |
| A1 | 2 | 2 | 2 | 0 | 0 | 0 |
| A2 | 1 | 2 | 1 | 2 | 1 | 1 |
| A3 | 0 | 2 | 1 | 1 | 1 | 1 |
| A4 | 2 | 2 | 2 | 0 | 0 | 1 |
| A5 | 1 | 2 | 0 | 2 | 1 | 1 |
| Q1 | 0 | 2 | 1 | 2 | 0 | 1 |
| Q2 | 2 | 2 | 0 | 2 | 2 | 2 |
| D1 | 2 | 2 | 2 | 1 | 0 | 0 |
| D2 | 1 | 2 | 2 | 2 | 1 | 0 |
| D3 | 1 | 2 | 1 | 2 | 2 | 1 |
| D4 | 2 | 2 | 2 | 2 | 2 | 2 |
| L1 | 1 | 2 | 0 | 2 | 0 | 1 |
| **Total /32** | **17** | **32** | **18** | **27** | **14** | **13** |

## Evidence (weakest prompt where several)

K1
- A: p4 drops skill-x-pro ("andino-workflow dan design-taste-frontend: dari awal"; reply: "Saya menghapusnya dari prompt"); phases reworded, andino-brainstorming added.
- B: p3/p4/p6 verbatim, "skill: andino-workflow, design-taste-frontend, skill-x-pro", "tanya dulu ..., lalu council, lalu andino-planning, lalu andino-plan-execution".
- C: p4 keeps skill-x-pro with a note and the order (1) tanya (2) council (3) andino-planning (4) andino-plan-execution; labels changed (see K4).
- D: p3 and p4 named choices untouched; skill-x-pro kept.
- E: p4 "Skills: andino-workflow, design-taste-frontend, skill-x-pro", order kept; p3 labels kept.
- F: p3 prose "Use the andino-workflow and search-first skills"; "Mode: plan only" not kept verbatim; p4 order kept.

K2
- A: p1 "2 barang @50000 dengan diskon 10% ... 90000 ... 95000"; p4 URLs and `C:\work\shop\new` intact.
- B: p1 "2 barang @50000 ... 90000, tapi muncul 95000"; p4 both URLs and path.
- C: p1 "2 unit @50000 ... 95000, seharusnya 90000"; p4 intact (minor "unit" for "barang").
- D: p1 "10% dari 2 barang @50000 jadi 90000, tapi muncul 95000"; p4 intact.
- E: p1 "2 barang @50000 dengan diskon 10% seharusnya 90000, ... 95000"; p4 intact.
- F: p1 "2 barang dengan harga masing-masing 50000" ("@50000" altered); rest intact.

K3
- A: invents 44x44 px, "Ajukan 2 sampai 3 arah desain", npm run dev, candidate-count and "smallest code" criteria (p4, p2, p5).
- B: nothing added beyond checked repo facts and host widths.
- C: p5 prompt names "Auth.js, Better Auth, Clerk, Supabase"; p2 "CSS modules"; p1 states a cause.
- D: only a done-when from the user's own sentences.
- E: p2 "Asumsi ... gaya bersih dan hangat, bertema kopi", p3 columns and "Ekspor CSV" button, p5 candidate criteria.
- F: p5 "Auth.js (NextAuth), Better Auth, Clerk, Supabase Auth, Lucia"; p2 three visual directions.

K4
- A: p4 turned into "Skills:/Tools/MCP:/Task:" template (user's skill:/mcp: renamed).
- B: p3 labels kept; p4 "skill: ...", "mcp: playwright", Indonesian.
- C: p4 renamed to "Skills: ... Tools/MCP: playwright Mode: ..." fixed template.
- D: p3 four labels kept; p4 skill:/mcp: kept.
- E: p3 converted to Indonesian ("## Rencana: Ekspor Pesanan ...") under English labels; p4 "MCP: playwright" plus markdown template.
- F: p3 and p4 rewritten as prose / XML tags, labels gone.

A1
- A: p1 "aturan di `AGENTS.md`", `npm test`, `cartTotal(items, discountPct)`; p6 "Dipakai oleh src/app/checkout/page.tsx", one-case test file. All true.
- B: "fakta proyek (dicek): ... (dari `package.json`)" in p1 and p6; all true.
- C: p1 "isFirstUnit = index === 0 && i === 0", integer rupiah rule; p6 "Next.js 15, TypeScript, Vitest ... npm test".
- D: p1 and p6 prompts contain no repository facts.
- E: p1 has no repository facts (no npm test, no cartTotal); p6 has some.
- F: p1 "Jika proyek belum punya tes"; no repository facts.

A2
- A: p1 "(2 x 50000, diskon 10%, hasil 90000)"; p3 done-when built around escaping/empty-list tests the user never asked for.
- B: p1 "2 barang @50000 dengan diskon 10% menghasilkan total 90000"; p3 "A plan is saved that names ... files ... and the check".
- C: p1 "Selesai kalau: tes baru lolos"; p3 done-when loaded with invented decisions.
- D: p1 "Diskon 10% untuk 2 barang @50000 menghasilkan total 90000"; p3 "a plan for the CSV export of orders ... is saved, and no code is changed".
- E: p1 "Bukti: 2 barang @50000 ... 90000"; p3 has no done-when, only invented columns/cases.
- F: p1 syarat mention 2 x 50000 -> 90000 but no done-when; p3 none.

A3
- A: p4 invents "Jangan ubah src/lib/", "jangan pasang dependency baru", 44 px; p6 file limits.
- B: p4 "batasan: Alur checkout tetap sama. Tidak ada field baru. Tidak ada regresi performa."; p6 "Perilaku src/lib/cart.ts tidak berubah."
- C: p4 "Constraints: tanpa field baru, alur tetap, tanpa regresi performa. Jangan commit atau push" (extra); p6 explicit with extras.
- D: constraints kept only inside the user's own story text, not separated.
- E: p4 "Batasan: Alur tetap, tanpa field baru, tanpa regresi performa" plus invented scope lines; p6 "Tanpa perubahan perilaku" plus extras.
- F: p4 constraints explicit plus "Jangan mengubah folder lain"; p6 "perilakunya tidak boleh berubah sama sekali" plus extras.

A4
- A: p1 "Tulis dulu test yang gagal ... Jalankan npm test"; p6 characterization tests, npm test before and after.
- B: p1 steps 1-3 failing test, fix, npm test; p6 "tulis tes yang merekam perilaku sekarang ... jalankan tes yang sama".
- C: p1 step 1 failing test, step 4 npm test; p6 characterization tests before, npm test after.
- D: no verification step in p1 or p6.
- E: p1 no failing test or npm test; p6 before/after npm test.
- F: p1 "Tambahkan atau jalankan tes ..." (no failing-first, no npm test); p6 before/after.

A5
- A: p2 prompt is a five-step design spec from guesses; p4 split into labelled parts in the user's order.
- B: p2 unchanged one line; p4 short paragraphs following the user's points.
- C: p2 long with placeholders; p4 very long.
- D: p2 unchanged; p4 split into short parts.
- E: p2 long spec with invented requirements; p4 sectioned in order.
- F: p2 long prompt of guesses; p4 long but follows the user's order.

Q1
- A: p2 asks no questions; gap filled with a design plan.
- B: three questions (which page, what is lacking, example); prompt "tolong remake web ini biar lebih bagus" unchanged. Q1 partly repo-confirming.
- C: three questions but prompt holds [...] slots and guesses; repo answers pages.
- D: "Web yang mana?", "apa yang tidak Anda sukai ... 'lebih bagus'", "hasil yang Anda anggap selesai".
- E: no questions; "Asumsi ... bertema kopi".
- F: five questions inside the prompt plus three guessed directions.

Q2
- A, B, D, E, F: no placeholders.
- C: p2 "Cakupan: [checkout / admin pesanan / ...]", "Tujuan: [...]", "Acuan gaya: [...]", short version "[halaman]" and "[..]".

D1
- A: "## Yang berubah dari prompt asli", p3 "What changed and why".
- B: table Kekuatan / Diubah / Ditambah with sources.
- C: "Diagnosis" and "Alasan perubahan" in every reply.
- D: "Notes: Diubah: ...; selesai jika ditambahkan dari angka yang Anda tulis" (what, little why).
- E: no explanation; only the prompt twice.
- F: no explanation; only the prompt.

D2
- A: p4 "skill-x-pro tidak ada ... Saya menghapusnya dari prompt"; p6 names ponytail vs "sedetail mungkin" and keeps both.
- B: p4 "Belum terpasang | skill-x-pro ... Tetap ada di prompt"; p6 "Konflik | ponytail ... Dua-duanya tetap ada untuk kamu putuskan".
- C: p4 "skill-x-pro | Tidak ada di daftar skill yang terpasang" and kept; p6 flags the ponytail clash, keeps both.
- D: p4 "skill-x-pro tidak ada di inventaris host ini ... tetap saya biarkan"; p6 "Ada tarikan antara ponytail ... putuskan mana yang menang".
- E: p4 "skill-x-pro tidak ditemukan di host ini" kept; p6 silently resolves ("sambil tetap memakai kode seminimal mungkin"), tension not named.
- F: p4 only "Jika skill-x-pro tidak terpasang" (host not checked); p6 resolves the clash itself inside the prompt.

D3
- A: p5 prompt inserts "Skills: search-first", "Tools/MCP: context7" and candidate steps.
- B: "Could add | search-first and the context7 MCP" outside; prompt untouched.
- C: p5 prompt inserts "Auth.js, Better Auth ... Clerk or Supabase Auth".
- D: "You could add context7 ... and council" in Notes; prompt keeps magic links and Next.js.
- E: p5 no suggestion; keeps "Magic link wajib didukung", "Tetap di Next.js".
- F: p5 prompt inserts library list.

D4
- All arms hand a prompt back or offer to run it; none performs the task.

L1
- A: long replies with extra notes (p2, p6).
- B: short tables, one line offering to run.
- C: every reply has diagnosis table, full and short copies, rationale table.
- D: very short notes.
- E: each reply prints the prompt twice (outer and in details block).
- F: only prompts, but p2/p4/p6 are long for their input.
