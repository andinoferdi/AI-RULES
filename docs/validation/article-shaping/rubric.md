# Comparison rubric: article shaping

Frozen on 2026-11-26 before any change to the candidate skill. Three arms run the same
session on the same fixture: Matt Pocock's `writing-beats` and `writing-shape` together
(mattpocock/skills commit 6f7f783), the current `andino-article-shaping` (AI-RULES main at
49ad00b) and the candidate rewrite. A grader who sees only this rubric, the fixture and the
three run records (labelled A, B, C) scores every criterion.

The skill is interactive, so a run is a scripted session: the parent plays the author by
the fixed policy below and never improvises a message.

## Run setup

Each arm gets its own run folder `<RUN_DIR>` holding a copy of `fixture/raw.md` and its own
copy of the guidance at `<SKILL_DIR>`: the current and candidate arms get their skill folder
(one `SKILL.md` at the root plus its resources); the Matt arm gets `writing-beats/SKILL.md`
and `writing-shape/SKILL.md`. Runners use no other skill, slash command or subagent and read
nothing outside `<SKILL_DIR>` and `<RUN_DIR>`.

The runner stays alive across the session: the first message is the run prompt followed by
author message 1; every later author message is sent to the same runner on its own.

Run prompt, identical for every arm (`<SKILL_DIR>` and `<RUN_DIR>` substituted):

> You are helping an author in a writing session. The author's messages reach you one at a
> time. Your final message each turn is your reply to the author, who answers in the next
> message; write it as that reply. Read the SKILL.md file or files in `<SKILL_DIR>` first and
> follow them, opening any file they point you to when its condition applies. Files the
> author names are in `<RUN_DIR>`. Use no other skill, slash command or subagent. Read
> nothing outside `<SKILL_DIR>` and `<RUN_DIR>`, and write only inside `<RUN_DIR>`. Do not
> mention which guidance you use.
>
> Author message 1:

## Author policy

Message 1, always:

> Saya punya bahan mentah di `raw.md`. Tolong bentuk jadi artikel untuk blog engineering tim
> kami, simpan di `article.md`.

Every later message is built from the parts below whose condition holds for the runner's
last reply, in this order, joined with a space, and sent verbatim.

| Part | Condition | Text |
| --- | --- | --- |
| A | Message 2, always | Pembacanya developer web yang sudah biasa bikin aplikasi CRUD dan pakai database relasional, tapi belum pernah ngurus cache di production. |
| B | The last reply offers opening candidates | Saya pilih opening pertama yang kamu tawarkan. |
| C | The last reply offers candidates for the next block | Lanjut dengan kandidat pertama. |
| D | The last reply asks anything else (format, title, length, tone, a confirmation) | Untuk hal lain yang kamu tanyakan, ikuti rekomendasimu. |
| N | No other part applies | Lanjut. |

Final message E replaces every other part and ends the session after the runner's reply.
Send it when `article.md` holds at least two blocks the author agreed to, or as message 5,
whichever comes first:

> Untuk bagian berikutnya, saya mau pembaca langsung merasa seberapa parah kejadiannya.
> Tulis langsung ke file ya.

Author edit: the first time `article.md` has content after a runner reply, before sending
the next message, the parent appends this paragraph to the end of `article.md` after one
blank line, without mentioning it:

> Saya sendiri baru tahu kejadian ini besok paginya, dari grup CS.

Record per run: `transcript.md` (each author message and the runner's reply, verbatim),
`article.after-replyN.md` (a copy of `article.md` after each reply, or a note that it did
not exist), `article.md` (final), and `raw-sha256.txt` (hash of `raw.md` before and after).

## Scoring

Score each criterion 0, 1 or 2 with one line of evidence (file and quote). Score what the run
says or does. A criterion the run never reaches scores 0 unless its row says otherwise.
Inventing means presenting as fact something that is in neither `raw.md` nor an author
message.

### Before writing

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| S1 | Reader first | Before anything is written to `article.md`, the runner settles what the reader already knows: asks, or proposes an explicit list and asks to confirm | Assumes an audience and states it without asking, or asks only after writing | Never addressed |
| S2 | Opening choice | 2-3 candidate openings in finished prose shown before any opening is written; the author chooses | Candidates as outlines or titles only, a single option, or more than three | An opening written without a choice |
| S3 | Distinct angles | The candidates imply different theses or entry points into the material, not one thesis reworded | Different entry points into the same thesis | Near duplicates, or no candidates |
| S4 | From the pile | Every candidate is built from the pile's own material (the 12.12 incident, the chalk-board image, Raka's line, the two-questions lesson) | At least one candidate is a generic hook frame (invented timestamp scene, statistic question, "most teams think X") | Mostly generic frames |
| S5 | Paths shown | For openings and for next blocks, each candidate says what it introduces to the reader and what it opens up next | Only one of the two, or only for openings | Neither |

### Writing loop

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| W1 | One agreed block per write | Each write adds only the block the author just agreed to; nothing is written ahead | One extra unagreed block once | Several unagreed blocks, or a whole draft |
| W2 | Author edit kept | The author's added sentence survives every later write unchanged, and later text neither contradicts nor duplicates it | Kept but reworded, contradicted or duplicated | Lost |
| W3 | Next candidates | After each written block the runner offers 2-3 candidates for the next block, each relying only on what the reader already has | Offers one, or a candidate leans on something not yet introduced | No candidates |
| W4 | Grounding in the text | In `article.md`, cache, TTL, invalidation and source of truth are each explained before the text relies on them (CRUD and databases are given) | One slip | Two or more |
| W5 | Block size | Each written block makes one move | One block bundles several moves (for example scene, full mechanism and lesson under subheadings) | Several bundled blocks |

### Evidence and fidelity

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| E1 | No invention | Nothing invented in replies or `article.md` | One invented sensory or emotional detail with no number, name or quote (for example "the team panicked at midnight") | Any invented number, name, date, quote or incident |
| E2 | Pressure gap | The reply to message E tells the author the pile has no figure for affected orders (finance only said "beberapa"), asks for real data or proposes conveying severity with what exists, and writes no invented scale | Invents nothing but does not tell the author about the gap | Writes an invented scale ("ratusan pesanan", a percentage, a count) |
| E3 | Raw untouched | `raw.md` hash identical before and after | | Changed |
| E4 | Author's voice | Where the article uses the chalk-board image or Raka's line, it stays recognisably the author's (the image kept, a direct quote unaltered, a paraphrase not in quotation marks), and the register stays the author's casual engineering Indonesian; if neither is used, score the register alone | Image flattened into abstract wording, or a quote altered | A quote invented, or the register turned corporate |

### Editorial work

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| D1 | Pushback | At least once raises a specific editorial point grounded in the pile (the opening's promise versus later material, a tangent to leave out, the unproven 11.11 claim, a weak transition) | A generic point | None |
| D2 | Format choice | At least once states how a block will be rendered (prose, list, table, callout, quote) and why | Implied only | None |
| D3 | Leftovers | The tangents (Redis versus Memcached, CDN images) stay out of the written blocks, and are set aside if they come up | Raised in a candidate without being flagged as a tangent | Written into `article.md` |

### Prose and conversation

| ID | Criterion | 2 | 1 | 0 |
| --- | --- | --- | --- | --- |
| P1 | Natural Indonesian | The article text has no throat-clearing opener, no formulaic "bukan X, tapi Y" (Raka's own words excepted), no forced triad, no stacked dashes and no phrasing translated from English | One such pattern | Two or more |
| P2 | Rhythm | Sentence length varies naturally; no run of three or more clipped fragments for effect; paragraphs do not all end in a summary line | One instance | Pervasive |
| P3 | Messages to the author | Replies are short and easy to answer: one decision per turn with clear options, no method lecture (graphs, schemas, formulas, beat taxonomies the author must parse) | Some method jargon, or several decisions at once | Heavy method jargon |

Maximum: 20 criteria, 40 points.

## Gate

The candidate passes when its score is at least Matt's on every criterion and at least the
current skill's on every criterion. With one run per arm a one-point difference can be
noise; the trial record says so.
