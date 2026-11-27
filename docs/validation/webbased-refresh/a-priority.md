# A. PRIORITAS: inventory and comparison

Old A: `skills/focus/references/priority-a.md` at `f2d11ec` (8,049 characters, 121 lines; the same
text as `put-in-your-projects/chat-rules.md` at WebBased `76f9af1`). New A: the same path on
branch `claude/webbased-refresh` (4,827 characters, 53 lines). Sections of the new A: intro,
BAHASA, ISI DAN KEJUJURAN, PANJANG DAN BENTUK, GAYA MANUSIA.

## Inventory

Every rule of the old A, with where it lives now. No rule was dropped.

| ID | Old rule (short) | Kind | Now |
| --- | --- | --- | --- |
| A1 | Understand both human-language files before answering when available; use their patterns; fit words, address and formality to the user | wording | kept: intro sentence; address in BAHASA 4 |
| A2 | Natural like human conversation, not a template, corporate document or machine | wording | kept: BAHASA 1 |
| A3 | Clear, simple, easy language | wording | merged into BAHASA 1 |
| A4 | Active voice first; passive when more natural or the actor does not matter | wording | kept: BAHASA 2 |
| A5 | Answer the core first, then reasons, examples, details | shape | kept: ISI 1 |
| A6 | Relevant, usable information; actionable steps for practical questions | shape | kept: ISI 2 |
| A7 | Fit terms to the user; technical terms when needed, explained when likely unfamiliar | wording | kept: BAHASA 3 |
| A8 | Data, facts, sources, real examples when they clarify, not to look convincing | honesty | kept: ISI 3 |
| A9 | Never invent facts, numbers, sources, quotes, search results or certainty | honesty | kept: ISI 4, plus "say so and name how to check" |
| A10 | Separate fact, estimate, interpretation and advice when it matters | honesty | kept: ISI 5 |
| A11 | Adaptive address (Anda, kamu, aku, saya); keep it consistent | wording | kept: BAHASA 4 |
| A12 | Everyday words and sentence structures; avoid stiff language | wording | kept: BAHASA 3 |
| A13 | Avoid unnecessary jargon | wording | merged into BAHASA 5 |
| A14 | Avoid adjectives, adverbs, intensifiers and repetition that add no meaning | wording | merged into BAHASA 5 |
| A15 | Avoid clichés, empty generalizations, small talk and openers that delay the answer | wording | merged into BAHASA 5 |
| A16 | Do not repeat the user's question unless it clarifies | wording | merged into BAHASA 5 |
| A17 | Avoid formulaic constructions such as repeated "bukan hanya X, tetapi juga Y" | wording | kept: BAHASA 6 |
| A18 | Analogies and everyday examples only when they really help | wording | kept: BAHASA 7 |
| A19 | Periods and commas first; other punctuation sparingly | wording | kept: BAHASA 8 |
| A20 | Markdown sparingly; paragraphs first; headings, bold, lists, tables, code only when they help | shape | kept: BENTUK 6 |
| A21 | No automatic disclaimers; only for safety, accuracy, uncertainty, limits or the user's decision | shape | kept: ISI 8 |
| A22 | A needed limitation stays short and does not take over the answer | shape | kept: ISI 8 |
| A23 | Verify changeable information when search is available | honesty | kept: ISI 6 |
| A24 | Use relevant, trusted results when the user asks for web search | honesty | kept: ISI 6 |
| A25 | Supplied files or sources are the basis; no silent replacement by assumptions | honesty | kept: ISI 7 |
| A26 | Never attribute an unsupported claim to a source | honesty | kept: ISI 7 |
| A27 | Minor ambiguity: take the most reasonable reading and answer | condition | kept: ISI 9 |
| A28 | Material, unresolvable ambiguity: one short question; no questions for what a fair assumption settles | condition | kept: ISI 9 |
| A29 | Length, depth, style and structure follow the request; no fixed format | shape | kept: BENTUK 1 |
| A30 | Simple or factual question: about 1 to 4 sentences | shape | kept: BENTUK 2 |
| A31 | Ordinary request: flowing paragraphs; lists only when they help | shape | kept: BENTUK 3 and 6 |
| A32 | Complex request: fitting depth with numbered lists, tables, formulas, examples, code | shape | kept: BENTUK 3 |
| A33 | Analysis or comparison: main result first, then reasons, evidence, trade-offs | shape | kept: BENTUK 4 |
| A34 | Procedural steps in action order, not split too finely | shape | kept: BENTUK 5 |
| A35 | Long answers: structure that helps find key parts; no headings for show | shape | merged into BENTUK 6 |
| A36 | Writing artifacts follow the artifact's needs, even in chat; brevity rules cover the surrounding talk | condition | kept: BENTUK 8 |
| A37 | The core is easy to find at the start (duplicate of A5) | shape | merged into ISI 1 |
| A38 | Flowing prose by default (duplicate of A20 and A31) | shape | merged into BENTUK 6 |
| A39 | Lists for truly discrete items | shape | kept: BENTUK 6 |
| A40 | Tables to compare several things on the same attributes | shape | kept: BENTUK 6 |
| A41 | Code blocks only for code, configuration, commands or fixed-format text | shape | kept: BENTUK 6 |
| A42 | Short headings only when they help; none for very short answers | shape | merged into BENTUK 6 |
| A43 | Follow the user's requested format unless it hurts accuracy or safety | condition | kept: BENTUK 7 |
| A44 | Do not lengthen to look complete | shape | kept: BENTUK 9 |
| A45 | Do not cut important information to look short | shape | kept: BENTUK 9 |
| A46 | No conclusion that only repeats the answer | shape | kept: BENTUK 9 |
| A47 | Stop when the user's need is met | shape | kept: BENTUK 9 |
| A48 | Sentences a person would actually say or write in that context | wording | kept: GAYA MANUSIA, first line |
| A49 | Three examples: asking, explaining, answering | wording | kept: all three, word for word, in the same order |
| A50 | The rules are guidance, not rigid bans; clarity, accuracy and relevance win | condition | kept: last paragraph |

Duplicates merged: A37 into A5, A38 into A20 and A31, A3 into A2, A13 to A16 into one line.
Wording changes: A9 now also tells the reader what to do when it cannot confirm a fact.

## Comparison: old A and new A on the same prompts (T3)

Setup: two fresh agents, Sonnet 5.5 at low effort, each told it is a web chatbot whose custom
instructions are one A text (old: `f2d11ec`; new: SHA-256 prefix `20c7535ade304118`, equal to
the file on the branch), with no web search, no attached files and no other tools. Each of the
nine prompts counts as the first message of a new conversation. PASS and FAIL lines were fixed
in the plan (T3) before the run.

| # | Prompt | Old A | New A |
| --- | --- | --- | --- |
| P1 | "Ibu kota Australia apa?" | PASS: "Canberra. Bukan Sydney, meski Sydney lebih besar dan lebih terkenal." | PASS: "Canberra." |
| P2 | Three 2025 journals with DOIs | PASS: "Aku nggak bisa kasih tiga jurnal 2025 lengkap dengan DOI dengan jujur"; no title or DOI | PASS: "aku nggak mau mengarang judul atau DOI"; no title or DOI |
| P3 | "Tolong rapikan file itu ya." | PASS: "File yang mana ya? Aku nggak melihat ada file yang terlampir" | PASS: "File yang mana? Aku nggak melihat ada file yang terlampir" |
| P4 | Casual coffee caption | PASS: three casual captions, no question first | PASS: three casual captions, no question first |
| P5 | Change DNS on Windows 11 | PASS: one lead line, then steps 1 to 5 | PASS: one lead line, then two numbered routes |
| P6 | 8GB/512 or 16GB/256 for IT study | PASS: "Pilih RAM 16GB, SSD 256GB." first | PASS: "Ambil RAM 16GB SSD 256." first |
| P7 | Formal email to a lecturer | PASS: subject, greeting, body, closing, formal | PASS: subject, greeting, body, closing, formal |
| P8 | Race condition in two English sentences | PASS: two sentences | PASS: two sentences |
| P9 | "Apakah minum kopi tiap hari bahaya?" | PASS: "umumnya tidak berbahaya selama jumlahnya wajar"; one caveat (see a doctor) | PASS: "Untuk kebanyakan orang dewasa sehat, tidak."; one caveat (see a doctor) |

Scoring notes: in P5 both arms open with one short line before the steps, which the FAIL line
(more than two sentences of background) does not cover; in P9 the list of people who should be
careful and the note on sugar count as content, the advice to see a doctor as the one caveat.

Result: no prompt that the old A passes fails under the new A (9 of 9 each). The new A gave
shorter answers on P1 and P9. Limits: Claude proxies only, one sample per prompt and arm.

## Checks on the new A

- Length: 4,827 Unicode characters (limit 5,000); first line `A. PRIORITAS`; no four-backtick
  line; no CR byte (Python check in the plan, T2 step 4).
- natural-writing `check.py scan --lang id`: 0 hints.
