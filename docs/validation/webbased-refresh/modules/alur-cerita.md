# S. Pembuat Alur Cerita Game dan Film (`alur-cerita`)

Mode: revision. Old text: WebBased `76f9af1`, module "S. PEMBUAT ALUR CERITA GAME/FILM" (1081
lines). New text: `skills/alur-cerita/SKILL.md` on branch `claude/webbased-daily-rules`.

## Brief (gate 1)

- Consumer: a web chatbot that loads the module as an uploaded skill (Claude.ai, Gemini) or reads
  it pasted into the chat (ChatGPT Free). It may or may not have web search.
- Task: lay out the plot of a game, film, series or other narrative work as a chronological,
  cause-and-effect timeline, from the user's source or from research, in original wording.
- Must load: "Jelaskan alur cerita lengkap The Last of Us." and "Buatkan timeline cerita dari
  ringkasan film ini: ..."
- Must not load: "Rekomendasikan lima game RPG dengan cerita bagus." (recommendation, not a plot
  timeline) and "Tulis cerita pendek baru tentang naga." (new fiction).
- Output: an adaptive structure (konteks karya, tokoh inti, relasi penting, timeline kronologis,
  titik balik, klimaks dan resolusi, ending, perubahan karakter, tema), phase headings with
  paragraphs, and mode keywords that change depth, spoiler level, order, canon scope and sources.
- Authority limits: invents no plot fact, backstory, motive, source or ending; copies no script,
  long dialogue, lyrics or scene-by-scene reconstruction of a protected work; marks interpretation
  as interpretation; does not override source requirements, copyright, safety or a higher-priority
  instruction.

## Routing table (gate 2)

Kinds: shape, omission, condition, discipline, fact. Destinations: module (the section in the new
text; exact lines fixed in gate 5), A (already covered by A. PRIORITAS, with the reason), nothing
(with a reason).

| ID | Old text (short) | Kind | Destination |
| --- | --- | --- | --- |
| S1 | Role: composer and analyst of the plot of a game, film, series or other narrative work | shape | module: purpose paragraph |
| S2 | Goal: a timeline that is chronological, orderly, detailed, coherent, easy to follow, explains cause and effect, shows character and conflict development start to end | shape | module: purpose paragraph, Format jawaban |
| S3 | "Aktif bila dikirim bersama A" | condition | module: purpose paragraph (works alone; follow A when present) |
| S4 | Default for a full plot request: DETAILED TIMELINE, enough detail for the whole story and the links between events | shape | module: Mode, Format jawaban |
| S5 | "Ultra Detail", "sedetail mungkin", "timeline lengkap", "full spoiler": raise granularity | condition | module: Mode |
| S6 | Even then: no transcript, screenplay, dialogue reconstruction, scene-by-scene near-reproduction, moment-by-moment walkthrough, or substitute for watching or playing | discipline | module: Aturan |
| S7 | Detail goes to what happened, who, motive, cause, effect, relation change, goal change, new information, impact on later story | shape | module: Aturan, Langkah |
| S8 | No cosmetic detail that does not affect understanding | discipline | module: Aturan |
| S9 | User-supplied transcript, subtitle, script, summary, wiki export, notes, screenshot, document: that is the main basis | condition | module: Langkah 1 |
| S10 | No silent outside facts when the user wants a result based on the source only | discipline | module: Aturan |
| S11 | Source does not explain a detail: write proportionally "tidak dijelaskan dalam sumber" or a natural equivalent; never invent to fill a gap | discipline | module: Aturan |
| S12 | Verification, expansion, cross-check, extra lore or web research requested: outside sources allowed | condition | module: Langkah 1 |
| S13 | Separate the user's source from outside research when the difference matters | condition | module: Aturan |
| S14 | Title only: do not automatically ask for clarification if the work is identifiable with enough confidence | condition | module: Langkah 2 |
| S15 | Identify title, year, version, remake/remaster, season, episode, DLC, expansion, route, adaptation when several works share a name or have different stories | omission | module: Langkah 2 |
| S16 | One detail that would change the whole story: ask at most one clarification question (example "Resident Evil 4 versi 2005 atau remake 2023?") | condition | module: Langkah 2 |
| S17 | Identity already clear: start directly | condition | module: Langkah 2 |
| S18 | Use the web when asked for research, several versions, story detail not confident, canon status to verify, ending with several readings, DLC changing context, outside facts needed | condition | module: Langkah 1 (no web: say so, work from the user's source or what is known, and mark confidence) |
| S19 | Source priority: official publisher/studio/developer/distributor/IP holder; official material (manual, codex, character bio, episode guide, developer commentary); creator/developer interviews; database or wiki with strong references; community sources only as cross-check | shape | module: Langkah 1 |
| S20 | Do not treat one community wiki as absolute proof when a material canon conflict exists | discipline | module: Aturan |
| S21 | Never invent sources | discipline | module: Aturan |
| S22 | Distinguish when relevant: main canon, alternate ending, optional route, side story, DLC, spin-off, adaptation, remake continuity, New Game+ content, non-canon mode, dream/vision, hypothetical sequence | omission | module: Langkah 3 |
| S23 | Never merge them into one timeline as if all in the same continuity | discipline | module: Aturan |
| S24 | Canon status unclear: write "status canon tidak pasti" and briefly the reason when it matters | condition | module: Aturan |
| S25 | Default timeline is chronology of events in the story world, earlier to later to resolution | shape | module: Langkah 4 |
| S26 | Distinguish KRONOLOGI CERITA (order in the story world) from URUTAN PENYAJIAN (order shown to the player or viewer) | omission | module: Langkah 4 |
| S27 | Non-linear work: keep the main timeline chronological but mark information shown later (example "Secara kronologis ... sebelum Bab 1, tetapi pemain baru mengetahuinya melalui flashback pada Bab 6.") | condition | module: Langkah 4 |
| S28 | Flashback goes at its chronological position when building the story-world timeline | condition | module: Langkah 4 |
| S29 | Flashback important as a reveal: add when the event happened, when it is shown, how the reveal changes understanding of a character or player | condition | module: Langkah 4 |
| S30 | Never write the same event twice at length | discipline | module: Aturan |
| S31 | Time travel: set the model from the source (fixed, branching, mutable, causal loop, multiverse, or the model the work explains) | condition | module: Langkah 4 |
| S32 | Do not force an outside time-travel theory the work does not support | discipline | module: Aturan |
| S33 | Absolute chronology undeterminable (paradox or structure): explain the limit | condition | module: Aturan |
| S34 | Several characters: merge events into the main timeline by time; mark perspective if important (example "Pada waktu yang sama, karakter A berada di X sementara karakter B melakukan Y.") | condition | module: Langkah 4 |
| S35 | Do not make simultaneous events look sequential | discipline | module: Aturan |
| S36 | Branching game: do not force one timeline as canon when the game has several routes; use shared timeline, ROUTE A, ROUTE B or another fitting structure | condition | module: Langkah 3 |
| S37 | One ending canonical by sequel or official source: explain the basis | condition | module: Langkah 3 |
| S38 | Never call a popular route canon without evidence | discipline | module: Aturan |
| S39 | Distinguish narrative events, gameplay mechanics, optional encounters, side quests, collectible lore, player actions that are not always canon | omission | module: Langkah 3 |
| S40 | Do not include every combat encounter or repetitive activity as an important story event | discipline | module: Aturan |
| S41 | Include gameplay if it affects the plot, introduces a character, changes a relation, reveals information, or causes an important change | condition | module: Langkah 3 |
| S42 | Include a side quest if it affects the main character, gives important lore, affects the ending, or the user asked for all side content | condition | module: Langkah 3, Mode |
| S43 | Otherwise side content may be summarized as relevant side content instead of listing each objective | condition | module: Langkah 3 |
| S44 | Background before the main timeline: the minimum context needed (setting, world, conflict before the story, important organizations, short history, initial character state) | shape | module: Format jawaban |
| S45 | No long lore dump before the story; give lore when it helps the next events | discipline | module: Aturan |
| S46 | Core characters, when relevant: starting position, goal, motive, important relations, internal conflict, external conflict, turning point | shape | module: Format jawaban |
| S47 | Do not invent backstory; unknown origin: "asal-usulnya belum dijelaskan secara jelas" is enough | discipline | module: Aturan |
| S48 | Do not force trauma, an arc or a hidden motive on every character without source support | discipline | module: Aturan |
| S49 | Relations between characters when they affect the story: how it began, each side's interests, how it changed, conflict or trust, effect on decisions | shape | module: Format jawaban |
| S50 | No long relation section for relations that do not affect the plot | discipline | module: Aturan |
| S51 | Each important segment ideally answers SIAPA, APA, KENAPA, DAMPAK, JEMBATAN; labels optional, natural prose allowed | shape | module: Langkah 5 |
| S52 | Granularity follows importance: major events deeper, transition events brief, small dialogue or action only if it changes understanding; not equal weight; not every minute | shape | module: Langkah 5 |
| S53 | Purpose: keep every narrative link needed to understand the story's journey | shape | module: purpose paragraph |
| S54 | Do not skip an event whose absence makes the reader ask why a character is suddenly at a new place, why a motive changed, how important information was obtained, how a new conflict began, why a relation changed, how the story reached the next point | omission | module: Langkah 5 |
| S55 | Repetitive events that do not change story state may be skipped or merged, with a transition sentence (example "Setelah beberapa misi untuk membangun kepercayaan kelompok tersebut, ia akhirnya memperoleh akses ke...") | condition | module: Langkah 5 |
| S56 | Cause and effect, not a bare list "A. Lalu B. Lalu C."; pattern "Karena A terjadi, karakter B memutuskan C. Keputusan tersebut kemudian menyebabkan D." | shape | module: Langkah 5 |
| S57 | A cause-effect link the source does not state is interpretation: not absolute fact; use "hal ini tampaknya mendorong..." or "cerita mengisyaratkan..." | discipline | module: Aturan |
| S58 | Turning point only when it truly changes goal, information, power position, relation, conflict or story direction | condition | module: Langkah 6 |
| S59 | Per turning point: what changed, why it matters, what followed | shape | module: Langkah 6 |
| S60 | Do not label every dramatic event a turning point | discipline | module: Aturan |
| S61 | Separate FAKTA KRONOLOGIS (what actually happened) from REVEAL NARATIF (when the viewer or player learns it); matters for mystery, thriller, unreliable narrator, memory loss, twist, non-linear | omission | module: Langkah 4 |
| S62 | Important reveal: explain how new information changes the reading of earlier events | condition | module: Langkah 4 |
| S63 | In non-spoiler mode, never leak a twist early | discipline | module: Mode |
| S64 | Spoilers allowed when the user asks for full story, ending, full spoiler, timeline lengkap; no repeated spoiler warnings | condition | module: Mode |
| S65 | "Without spoilers": limit information to the requested scope; no big reveal not needed | condition | module: Mode |
| S66 | Ending: distinguish explicit, implied, still open; never turn ambiguity into certainty | shape | module: Langkah 7 |
| S67 | Structure TERKONFIRMASI (shown or explained), TERSIRAT (strongly supported interpretation), TERBUKA (not settled by the work) | shape | module: Format jawaban |
| S68 | Official creator clarification and the user asks for outside context: may add as external information | condition | module: Langkah 7 |
| S69 | Several endings: explain the condition or decision that triggers each when relevant | condition | module: Langkah 7 |
| S70 | Never name one the "true ending" unless the game says so, a sequel confirms, or another official source exists | discipline | module: Aturan |
| S71 | A fandom's "true ending" without official confirmation: mark as a community term | condition | module: Aturan |
| S72 | Climax: conflict at its peak, important decision, consequences, why the result decides the resolution | shape | module: Langkah 7 |
| S73 | Do not turn the climax into a long reproduction of every action, attack, dialogue or shot; focus on narrative significance | discipline | module: Aturan |
| S74 | Resolution: state of the world, fate of important characters, resolved conflicts, remaining conflicts, relation changes, sequel setup if any | shape | module: Langkah 7 |
| S75 | Do not invent a continuation when the work stops ambiguous | discipline | module: Aturan |
| S76 | Character arc for main characters: initial state, pressure/conflict, decision, change, final state | shape | module: Langkah 8 |
| S77 | Not every character has a transformational arc (changes, fails to change, reinforces old belief, catalyst) | condition | module: Langkah 8 |
| S78 | Do not force hero's journey or a character theory that does not fit | discipline | module: Aturan |
| S79 | Theme after the plot facts are clear; separate plot (what happens) from theme (idea explored) | shape | module: Langkah 8 |
| S80 | Link theme to character decisions, conflict, consequences, symbol or motif if relevant, and the ending | shape | module: Langkah 8 |
| S81 | Do not present a theme interpretation as official fact unless the creator said so; use "cerita dapat dibaca sebagai..." | discipline | module: Aturan |
| S82 | Source contradiction: do not auto-pick the most comfortable version; check primary vs secondary, version, remake/adaptation, localization, retcon, unreliable narration, optional route, chronology | omission | module: Langkah 1 |
| S83 | Prefer the source closest to the original work and the continuity under discussion | discipline | module: Aturan |
| S84 | Conflict unresolved: briefly explain both versions; never hide uncertainty | condition | module: Aturan |
| S85 | Retcon: when a sequel, DLC, remake or official material changes an earlier fact, mark it if supportable, and explain earlier version then the version now in force | condition | module: Langkah 3 |
| S86 | Do not call a small difference a retcon without basis | discipline | module: Aturan |
| S87 | Raw transcript: normalize internally; identify speaker, order, events, location, temporal cues, cause and effect | omission | module: Langkah 1 |
| S88 | Do not just reformat the transcript; turn it into an original narrative summary | discipline | module: Aturan |
| S89 | No long dialogue reproduction; short quotes only when truly needed and within applicable limits | discipline | module: Aturan |
| S90 | Transcript does not explain a fact: do not add it from outside knowledge unless the user asks for expansion | discipline | module: Aturan |
| S91 | Summary as input: develop the structure and relations implied or supported by it | condition | module: Langkah 1 |
| S92 | Never "expand as detailed as possible" by creating dialogue, locations, motives, transitions or events absent from the source | discipline | module: Aturan |
| S93 | Detail unavailable: stay brief in that part; language elaboration is not adding facts | discipline | module: Aturan |
| S94 | Copyrighted work: plot, characters, relations, story facts, cause and effect, ending, theme and analysis allowed, in original wording | shape | module: Aturan |
| S95 | Never produce a full script, long transcript, long verbatim dialogue, very granular scene-by-scene reproduction, shot-by-shot description, or a near-complete substitute for the work | discipline | module: Aturan |
| S96 | "Ultra Detail" approaching that form: keep analytic detail, compress the original expression; focus on information, not reproduction of expression | discipline | module: Aturan |
| S97 | Dialogue: paraphrase by default (example "Karakter A mengakui bahwa ia telah menyembunyikan identitasnya."); a very short quote only when one line is essential to the analysis; no stacked quotes | discipline | module: Aturan |
| S98 | Lyrics: explain the song's function or scene meaning; never copy long lyrics | discipline | module: Aturan |
| S99 | Sensitive content: do not auto-remove story facts for violence, death, abuse, trauma, sexual or dark themes when important to the plot | discipline | module: Aturan |
| S100 | Factual, proportional language; no graphic description unless needed (example "Tokoh tersebut dibunuh dalam serangan itu.") | shape | module: Aturan |
| S101 | A sensitive detail central to the user's analytic question: explain enough, without sensationalism | condition | module: Aturan |
| S102 | Never change a fact so far that the meaning is wrong, just to sanitize | discipline | module: Aturan |
| S103 | Format adaptive; for a full plot use A to I: KONTEKS KARYA (judul, versi/tahun, setting, premis singkat), TOKOH INTI (posisi awal, motivasi, konflik utama; only needed ones), RELASI PENTING, TIMELINE KRONOLOGIS (by phase, chapter, act, arc, location or period; each segment: event, cause, decision, consequence), TITIK BALIK, KLIMAKS DAN RESOLUSI, ENDING, PERUBAHAN KARAKTER, TEMA | shape | module: Format jawaban |
| S104 | Not every part required; skip a part with no value; no long structure just because the template has it | condition | module: Format jawaban |
| S105 | Mode "TIMELINE": event order first, minimal theme analysis | shape | module: Mode |
| S106 | Mode "ULTRA DETAIL": more on cause, motive, relation, reveal, turning point, consequence; never a transcript or scene reconstruction | shape | module: Mode |
| S107 | Mode "RINGKAS": main plot and turning points only | shape | module: Mode |
| S108 | Mode "FULL SPOILER": all main conflicts and the ending; do not hide twists | shape | module: Mode |
| S109 | Mode "NO SPOILER": limit reveals to the user's scope | shape | module: Mode |
| S110 | Mode "KRONOLOGIS MURNI": by story-world time; mark flashback/reveal if important | shape | module: Mode |
| S111 | Mode "URUTAN CERITA ASLI": follow the order the film or game presents information; do not turn flashbacks into chronological order | shape | module: Mode |
| S112 | Mode "CANON ONLY": only events with clear enough canon basis; separate optional/non-canon content | shape | module: Mode |
| S113 | Mode "SEMUA ENDING": every relevant ending and its branching condition | shape | module: Mode |
| S114 | Mode "MAIN STORY ONLY": ignore side quests and optional lore unless needed for the main plot | shape | module: Mode |
| S115 | Mode "MAIN + SIDE": add side content that affects character, lore or ending | shape | module: Mode |
| S116 | Mode "CHARACTER FOCUS: [NAMA]": story built mainly from that character's journey; keep external events needed for the arc | shape | module: Mode |
| S117 | Mode "ENDING EXPLAINED": final events, reveal, motive, symbol/theme if relevant, what stays ambiguous | shape | module: Mode |
| S118 | Mode "BERDASARKAN SUMBER SAJA": only the user's material; no outside facts | shape | module: Mode |
| S119 | Mode "RISET + PERLUAS": web to expand and verify; separate work facts from outside interpretation if relevant | shape | module: Mode |
| S120 | Timeline format: phase headings ("FASE 1 — [...]") and paragraphs by default | shape | module: Format jawaban |
| S121 | Bullets only when many discrete facts need separating; not one bullet per event into a long list without flow | discipline | module: Format jawaban |
| S122 | Complex chronology: a table with columns Waktu/Fase, Tokoh, Kejadian, Penyebab, Dampak, only if it truly helps; no forced table for a story better read as narrative | condition | module: Format jawaban |
| S123 | Length follows work complexity and the request; detailed timeline may be long; Ultra Detail may be very long for a complex work | shape | module: Format jawaban |
| S124 | No repetitive detail to hit a length; 30 important events with clear links beat 150 micro-events | discipline | module: Aturan |
| S125 | Very long work (dozens-of-hours RPG, multi-season series, saga, franchise): output may be split into big phases or installments; still give a coherent overview; never cut an important part just because it is long | condition | module: Format jawaban |
| S126 | OVERRIDE FORMAT: S sets depth and structure for plot tasks; a full-detail request may be longer than A's short default | condition | module: Format jawaban (the length follows the request); the comparison with A's short default goes to A: it only matters when A is active |
| S127 | Not every question about a film or game gets an Ultra Detail Timeline; the user's request sets scope ("Siapa karakter X?" gets an answer about X, not a whole-game timeline) | discipline | module: Kapan dipakai, Aturan |
| S128 | Ultra Detail active only when the user asks for a full timeline or plot at that depth | condition | module: Mode |
| S129 | S never overrides source requirements, capability limits, copyright, safety or higher-priority instructions | discipline | module: Aturan |
| S130 | Internal check: right work and version; consistent chronology; flashbacks placed right; presentation order vs chronology swapped; mixed ending branches; side content mistaken for canon; motives supported; invented facts; cause and effect clear; sudden unexplained character change; turning points truly important; ending fact vs interpretation; too much dialogue or expression reproduced; detail helps understanding or only length | omission | module: Cek sebelum kirim |
| S131 | Do not show that checklist unless asked | shape | module: Cek sebelum kirim (the bullets are checked silently) |
| S132 | Final principles: orderly story; cause and effect; chronology vs presentation order; no invented gap; separate canon, route, adaptation, interpretation; detail by narrative importance; keep needed characters, conflicts, reveals, turning points; own wording for copyrighted works; "Ultra Detail berarti pemahaman yang lebih dalam, bukan reproduksi yang lebih dekat." | discipline | module: Aturan, Mode |

Gate 5 mapping: Langkah 1 = S9, S12, S18-S21 (sources), S82, S84, S87, S91; Langkah 2 = S14-S17; Langkah 3 =
S22, S36-S37, S39, S41-S43, S85; Langkah 4 = S25-S29, S31, S34, S61-S62; Langkah 5 = S51-S52, S54-S56;
Langkah 6 = S58-S59; Langkah 7 = S66, S68-S69, S72, S74; Langkah 8 = S76-S77, S79-S80; Aturan 1-21 hold
the discipline rows (S6, S8, S10-S11, S13, S20-S21, S23-S24, S30, S32-S33, S35, S38, S40, S45, S47-S48,
S50, S57, S60, S63, S70-S71, S73, S75, S78, S81, S83, S86, S88-S90, S92-S98, S99-S102, S124, S127, S129);
Format jawaban = S2, S44, S46, S49, S67, S103-S104, S120-S123, S125, S126; Mode = S4-S5, S63-S65,
S105-S119, S128, S132; Cek sebelum kirim = S130-S131. Added by gate 5 from the baseline: Aturan 3 (a
question about one character, place or event gets every fact the source gives about it) and one
Cek line for it; S127 now lives there.

Row S126 splits: the part "the length follows the request" stays in the module; the part that compares with A's short default
goes to A, since the module has no default short format of its own to override when A is absent.
No other row goes to A: the module must also work with A absent (ChatGPT Free without custom
instructions), so its honesty, copyright and no-invention lines stay.

## Scenario (gate 3)

### S1: Malin Kundang from a user summary, source only, then a question about one character
Type: shape (with discipline: no invention, flashback placement, scope)
Source: rows S11, S28, S29, S47, S61, S91, S92, S110, S118, S127
Setup: a chatbot with only this module loaded (old arm: the old text; new arm: the new
`SKILL.md`); no A, no tools, no web access; two turns in one conversation. The work is the
Indonesian folk tale of Malin Kundang (public domain); the user's summary is written for this test.
Prompt, turn 1: "KRONOLOGIS MURNI dan BERDASARKAN SUMBER SAJA. Susun alur dari ringkasan ini, urutan
penyajiannya persis seperti di bawah: (1) Sebuah kapal besar merapat di pantai. Malin turun bersama
istrinya; ia sekarang orang kaya. (2) Seorang perempuan tua berpakaian compang-camping mengenalinya
sebagai anaknya. Malin menolak mengakuinya di depan istri dan awak kapal karena malu. (3) Kilas balik:
dulu Malin kecil hidup miskin bersama ibunya yang janda. Ia ikut kapal dagang merantau supaya nasibnya
berubah, dan ibunya melepasnya. (4) Ibu yang sakit hati berdoa agar Malin dihukum. Badai menghantam
kapal, dan Malin berubah menjadi batu."
Prompt, turn 2: "Masih berdasarkan ringkasan tadi saja. Siapa ibu Malin?"
PASS: turn 1 puts the childhood and the departure (3) first, then the arrival (1), the denial (2),
the prayer and the stone (4), in that order, so the flashback sits at its chronological position;
it marks that the arrival is shown before the childhood in the summary (or an equivalent note
about presentation order); it says the source does not explain how Malin became rich ("tidak
dijelaskan dalam sumber" or an equivalent); it gives cause and effect (his shame leads to the
denial, the denial leads to the prayer); it adds no father, no name for any character, no place
name, no dialogue and no motive beyond "malu". Turn 2 answers only about the mother from the
summary (a poor widow who let him go, was denied in public, and prayed for his punishment), says
her origin or name is not explained, and shows no full phase-by-phase timeline.
FAIL: the arrival (1) listed before the childhood (3) as the first event with no presentation
note; any added father, name, place, dialogue or explanation of how he got rich; a source-less
motive stated as fact; a cause-effect link stated as certain when the summary does not say it;
turn 2 giving a full FASE timeline, or adding facts about the mother that the summary lacks.
No computed number appears in the PASS line. The order is read straight from the prompt: of the 4
numbered items, item 3 happens first, then 1, 2 and 4.

## Evaluation record (gates 4 and 6)

| Scenario | Arm | Status | Evidence | Result |
| --- | --- | --- | --- | --- |
| S1 | no skill | NOT RUN | the old module is the behaviour reference for this revision | - |
| S1 | current (old text) | RUN (Haiku 5.5, low, no tools, no web, no A; old text from `76f9af1`) | turn 1: "Catatan urutan: ringkasan menyajikan kejadian dalam urutan (1) kapal merapat, (2) pengakuan yang ditolak, (3) kilas balik, (4) kutukan dan badai. Secara kronologis dalam dunia cerita, kilas balik (3) terjadi paling awal ..."; "FASE 1 — Masa kecil dan perantauan Malin (masa lalu)"; "Sumber tidak menjelaskan berapa lama perantauan itu atau bagaimana Malin menjadi kaya."; "FASE 2 — Kapal merapat dan pengakuan yang ditolak" ... "karena malu. Sumber tidak menyebut ... nama istri atau kapal."; "FASE 3 — Kutukan dan badai"; "Sumber tidak menyatakan secara eksplisit bahwa badai dan perubahan itu akibat doa, tetapi urutan cerita mengisyaratkan kutukan itu terwujud." Turn 2: "Menurut ringkasan, ibu Malin adalah seorang janda yang hidup miskin bersama Malin sejak Malin kecil. Ia melepas Malin merantau supaya nasibnya berubah. Ringkasan juga menyebut seorang perempuan tua berpakaian compang-camping yang mengenali Malin sebagai anaknya di pantai, dan ringkasan menempatkan perempuan itu sebagai ibu yang sama, meski tidak menuliskannya dalam satu kalimat eksplisit. Nama sang ibu tidak dijelaskan dalam sumber." | Turn 1 PASS (presentation note, order 3-1-2-4, how he got rich not explained, cause and effect hedged where the summary is silent, nothing added). Turn 2 FAIL on completeness: it answers only about the mother with no timeline, but leaves out that she was denied in public and that she prayed for his punishment, both in the summary. Keep: presentation note, flashback placement, "Sumber tidak menjelaskan" lines, hedged cause and effect, scoped answer to the character question. Fix: a question about one character pulls every fact the source gives about that character |
| S1 | candidate (new SKILL.md, first version, 100 lines) | RUN (Haiku 5.5, low, no tools, no web, no A) | turn 1: "Sumber: hanya ringkasan yang diberikan pengguna. Ringkasan tidak menyebut judul karya, versi, atau status canon ..."; FASE 1 childhood and departure, "Ringkasan tidak menjelaskan berapa lama Malin pergi."; FASE 2 "Sebuah kapal besar merapat di pantai. Malin turun bersama istrinya, dan ia kini menjadi orang kaya."; FASE 3 the denial "karena malu"; FASE 4 prayer, storm, stone, "hubungan bahwa doa itu muncul karena penolakan hanya tafsiran yang tampaknya didukung kata \"sakit hati\""; "Catatan urutan: dalam penyajian ringkasan, kilas balik muncul setelah pertemuan, tetapi secara kronologis ia berada paling awal". Turn 2: the name is not given, then five bullets (poor widow, let him go, the old woman who recognized him, denied in front of wife and crew out of shame, "sakit hati dan berdoa agar Malin dihukum", storm and stone); no timeline | Turn 2 PASS (the fix for completeness worked). Turn 1 FAIL on one PASS item: it never says that the source does not explain how Malin became rich, which the old text's run did. Order, presentation note, hedged cause and effect and no additions all pass |
| S1 | candidate (fix round 1) | RUN (Haiku 5.5, low, no tools, no web, no A; extension agent) | Langkah 5 "Selesai bila:" and one Cek line now require every gap the source skips between segments (how a character got rich, how much time passed) to be written "tidak dijelaskan dalam sumber" | Turn 1: "ringkasan yang Anda berikan saja ... status canon tidak pasti"; "Urutan kronologis dan urutan penyajian Anda berbeda ... peristiwa (3) terjadi paling awal, lalu (1), (2), dan (4)"; "FASE 2 — Masa yang tidak dijelaskan: Sumber tidak menjelaskan bagaimana Malin memperoleh kekayaan, berapa lama waktu berlalu sejak keberangkatannya, atau kapan dan bagaimana ia menikah."; denial "Karena malu di depan istri dan awak kapal"; "Tafsiran: kata \"sakit hati\" mengisyaratkan kutukan muncul sesudah penolakan. Ini tafsiran, bukan fakta sumber."; then turning points, climax and resolution, ending (TERKONFIRMASI / TERSIRAT / TERBUKA), character change, "Tema (tafsiran)". Turn 2: the mother's facts (poor widow, let him go, the old woman who recognized him, denied out of shame, prayed in hurt), "Nama ibu tidak disebutkan dalam sumber. Asal-usul keluarganya, keberadaan ayah Malin, dan kehidupan ibu setelah Malin pergi tidak dijelaskan dalam sumber."; no timeline | PASS on both turns. The extra sections follow the module's default output, and "KRONOLOGIS MURNI" only sets the order, so no line is broken; interpretations are labelled |

## Probes (gate 7)

T8 result (supersedes the pending note below): RUN on one fresh Haiku 5.5 agent at low effort that saw only the seven names and descriptions and 17 shuffled prompts. Must load (P08, P17): picked `alur-cerita`. Must not load (P01, P15): picked `none`. PASS. Details in `../README.md`.

Pending: T8 (no fresh agent was given the skill set and these prompts yet).

- Must load: "Jelaskan alur cerita lengkap The Last of Us." and "Buatkan timeline cerita dari ringkasan film ini: ..."
- Must not load: "Rekomendasikan lima game RPG dengan cerita bagus." and "Tulis cerita pendek baru tentang naga."
- Status: pending: T8. Self-review by reading: the description names plot, timeline, ending, character or theme analysis of a work, present in both must-load prompts and absent from both must-not-load prompts.
