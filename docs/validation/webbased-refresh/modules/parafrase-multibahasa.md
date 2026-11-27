# D. Parafrase Multibahasa (`parafrase-multibahasa`)

Mode: revision. Old text: `README.md` lines 216 to 313 at WebBased `76f9af1` ("D. ASISTEN PARAFRASE
MULTIBAHASA"). New text: `skills/parafrase-multibahasa/SKILL.md` on branch
`claude/webbased-daily-rules`.

## Brief (gate 1)

- Consumer: a web chatbot that loads the module as an uploaded skill (Claude.ai, Gemini) or reads
  it pasted into the chat (ChatGPT Free).
- Task: rewrite a user's text so it reads naturally in the target language, keeping its meaning,
  facts, intent and tone.
- Must load: "Parafrasekan kalimat ini biar lebih natural: 'Dengan ini kami informasikan bahwa
  pengiriman akan mengalami keterlambatan selama 3 hari kerja.'"
- Must not load: "Ringkas artikel ini jadi tiga poin utama." (a summary, not a paraphrase).
- Output: a short detection line, the main result, and alternatives or notes only when they add
  something; five named modes change that shape.
- Authority limits: adds no new fact; changes no number, name, date, brand, link, code,
  identifier or technical term unless asked; never corrects a doubtful fact silently.

## Routing table (gate 2)

Kinds: shape, omission, condition, discipline, fact. Destinations: module (the line in the new
text), A (already covered by A. PRIORITAS), nothing (with a reason).

| ID | Old text (short) | Kind | Destination |
| --- | --- | --- | --- |
| D1 | Paraphrase into a natural version for the target language; keep meaning, facts, intent, tone and function; add no new information | shape | module: purpose paragraph, Aturan 1 |
| D2 | "Aktif bila dikirim bersama A" | condition | module: purpose paragraph ("works alone; follow A when it is present") |
| D3 | Detect language, variety or dialect, formality, context, audience and purpose first | omission | module: Langkah 1 |
| D4 | Target language: the user's choice, otherwise the source's main language | condition | module: Langkah 1 |
| D5 | Meaning and facts come first | discipline | module: Aturan 1 (priority order) |
| D6 | Keep numbers, names, dates, brands, links, code, identifiers, technical terms and specific facts unless the user asks to change or localize them | discipline | module: Aturan 2 |
| D7 | Keep product names, technical terms and proper nouns that usually stay in their original form | discipline | module: Aturan 2 |
| D8 | Truly natural structure, not word-by-word synonym swaps | shape | module: Aturan 3 |
| D9 | Order, length and structure may change when that reads more naturally without changing meaning | shape | module: Aturan 3 |
| D10 | Keep the writer's voice: firm stays firm, casual stays casual, formal stays formal, emotion keeps its intensity | discipline | module: Aturan 4 |
| D11 | Do not soften, harden or change emotional intent unless asked | discipline | module: Aturan 4 |
| D12 | Idioms, slang, humour, greetings and cultural expressions may become equivalents with the same function in the target locale | shape | module: Aturan 5 |
| D13 | No natural equivalent: use a plain expression that keeps the meaning; no literal translation | shape | module: Aturan 5 |
| D14 | Spelling, grammar, punctuation and capitals follow the target language and context | shape | module: Aturan 6 |
| D15 | Keep terms consistent; no shower of synonyms for one concept | shape | module: Aturan 6 |
| D16 | Do not raise or lower formality beyond the source unless context or the user asks | discipline | module: Aturan 4 |
| D17 | Length follows the source and the request; do not force a long text into 1 or 2 sentences | shape | module: Aturan 7 |
| D18 | Shorter or longer on request: change density, keep important information, add no facts | condition | module: Aturan 7 |
| D19 | Text that is already natural gets only the changes it needs | discipline | module: Aturan 8 |
| D20 | Fix small, obvious spelling or grammar slips when meaning stays the same | condition | module: Aturan 8 |
| D21 | A fact or number that looks wrong is kept as in the source unless the user asks for a check | discipline | module: Aturan 9, Format part 4 |
| D22 | Material ambiguity with readings that change meaning: ask one short question | condition | module: Langkah 2 |
| D23 | Small ambiguity: take the most reasonable reading without asking | condition | module: Langkah 2 |
| D24 | Context incomplete but paraphrase still safe: best version from the text, no specific assumptions | condition | module: Langkah 2 |
| D25 | Priority order: meaning and facts > intent and tone > natural language > clarity > technical neatness | discipline | module: Aturan 1 |
| D26 | Output A: short detection of language and context, only what matters | shape | module: Format part 1 |
| D27 | Output B: the best main result | shape | module: Format part 2 |
| D28 | Output C: a more formal alternative, only when relevant | condition | module: Format part 3 |
| D29 | Output D: a more casual alternative, only when relevant | condition | module: Format part 3 |
| D30 | Output E: notes on important choices (adapted idioms, kept terms, ambiguous parts), only when needed | condition | module: Format part 4 |
| D31 | Do not force parts C, D or E when they add nothing | shape | module: Format parts 3 and 4 |
| D32 | Mode "HANYA HASIL": only the main result, no analysis, labels, alternatives or notes | shape | module: Mode |
| D33 | Mode "FORMAL": the main result in the requested formality | shape | module: Mode |
| D34 | Mode "SANTAI": the main result in natural conversational language, no forced slang | shape | module: Mode |
| D35 | Mode "PERTAHANKAN GAYA": keep style, rhythm, formality and character while making it read naturally | shape | module: Mode |
| D36 | Mode "BAHASA [X]": the named language or locale is the target | shape | module: Mode |
| D37 | Principle: reads as if written naturally in the target context, yet says the same as the source | shape | module: purpose paragraph |

No row goes to A or to nothing: the module must also work when A is absent (ChatGPT Free with
no custom instructions), so its ambiguity and honesty lines stay.

## Scenario (gate 3)

### S1: Formal delivery notice, then a HANYA HASIL follow-up
Type: shape (with protected content)
Source: the module's own invariants D6, D10, D21, D28 to D31 and D32
Setup: a chatbot with only this module loaded (old arm: the old text; new arm: the new
`SKILL.md`); no A, no tools; two turns in one conversation.
Prompt, turn 1: "Tolong parafrasekan biar lebih natural tapi tetap formal: \"Sehubungan dengan
adanya kendala teknis pada sistem, maka dengan ini kami informasikan bahwa pengiriman pesanan
nomor INV-2047 via JNE akan mengalami keterlambatan selama 3 (tiga) hari kerja, dan kami mohon
maaf atas ketidaknyamanan yang terjadi.\""
Prompt, turn 2: "HANYA HASIL. Parafrasekan: \"Meeting-nya kita reschedule ke Kamis jam 2 siang
ya, soalnya Pak Budi masih di Surabaya.\""
PASS: turn 1 gives one main formal result that keeps `INV-2047`, `JNE` and `3` working days,
adds no date, cause or compensation, and shows no casual alternative; turn 2 is only the
paraphrased sentence, casual, keeping Kamis, jam 2 siang, Pak Budi and Surabaya.
FAIL: any change to `INV-2047`, `JNE`, the 3 days, Kamis, jam 2 siang, Pak Budi or Surabaya; a
new fact; slang in turn 1; a casual alternative in turn 1; any label, detection line,
alternative or note in turn 2.

## Evaluation record (gates 4 and 6)

| Scenario | Arm | Status | Evidence | Result |
| --- | --- | --- | --- | --- |
| S1 | no skill | NOT RUN | the old module is the behaviour reference for this revision | - |
| S1 | current (old text) | RUN (Haiku 5.5, low; old text from `76f9af1` lines 219 to 311) | turn 1: "**A. Deteksi bahasa dan konteks** ... **B. Hasil utama** Mohon maaf, karena adanya kendala teknis pada sistem kami, pengiriman pesanan nomor INV-2047 melalui JNE akan mengalami keterlambatan selama 3 (tiga) hari kerja. Kami memohon maaf atas ketidaknyamanan yang ditimbulkan." Turn 2: "Meeting-nya kita jadwalkan ulang ke hari Kamis pukul 14.00 ya, karena Pak Budi masih di Surabaya." | FAIL: turn 2 changed "jam 2 siang" to "pukul 14.00". Turn 1 met its PASS line, but opened with an apology the source did not have, so the apology appears twice |
| S1 | candidate (new SKILL.md, first version) | RUN (Haiku 5.5, low) | turn 1: "Hasil utama: Kami informasikan bahwa pengiriman pesanan INV-2047 melalui JNE mengalami keterlambatan selama 3 (tiga) hari kerja akibat kendala teknis pada sistem. Mohon maaf atas ketidaknyamanan ini." followed by "Alternatif lebih santai: ... Mohon maaf ya atas ketidaknyamanannya." Turn 2: "Meeting kita dijadwalkan ulang ke hari Kamis jam 2 siang ya, soalnya Pak Budi masih di Surabaya." | FAIL: turn 1 added a casual alternative although the user asked to stay formal. Turn 2 now passes: "jam 2 siang" kept, no labels. The double apology is gone |
| S1 | candidate (fix round 1) | RUN (Haiku 5.5, low; rerun from the owner-approved extension) | turn 1: "Deteksi: Bahasa Indonesia, register formal ... **Hasil utama:** Kami informasikan bahwa karena kendala teknis pada sistem, pengiriman pesanan nomor INV-2047 melalui JNE akan mengalami keterlambatan selama 3 (tiga) hari kerja. Kami mohon maaf atas ketidaknyamanan ini." Turn 2: "Rapatnya kita pindahkan ke Kamis jam 2 siang, ya. Pak Budi masih di Surabaya." | PASS: no alternative in turn 1, one apology, every protected value kept; turn 2 is only the sentence. Not covered by a line: "soalnya" became two sentences, so the reason is implied rather than said |

Fix round 1 changed one thing (the condition for alternatives) and the rerun passed, so no
further round was needed.

## Probes (gate 7)

T8 result (supersedes the pending note below): RUN on one fresh Haiku 5.5 agent at low effort that saw only the seven names and descriptions and 17 shuffled prompts. Must load (P12): picked `parafrase-multibahasa`. Must not load (P05): picked `none`. PASS. Details in `../README.md`.

Pending: the must-load and must-not-load prompts above go to the description probe in T8.

## Gate 7 checks and report

- Package check (`package_files`, README rule excluded) -> `PASS: parafrase-multibahasa package`;
  60 lines (old text 93); CR bytes 0; `check.py scan --lang id` -> `0 hint(s)`.
- Changed: `skills/parafrase-multibahasa/SKILL.md`, the seven-part layout, with explicit rules for
  time notation, added apologies and when alternatives appear.
- Routed out: nothing; all 37 rows stay in the module.
- Scenarios: this file, 1 scenario with 2 turns.
- Evaluation: RUN. Old text FAIL (time notation); first candidate FAIL (casual alternative);
  candidate after fix round 1 PASS. All runs on Claude Haiku 5.5 as a proxy for web chatbots.
- Not verified: behaviour in ChatGPT, Gemini and Claude.ai themselves; the five modes other than
  "HANYA HASIL".
- Next check: run S1 on ChatGPT Free with the file pasted.
