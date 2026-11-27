# Scores (A to D). No run showed a Skill, slash command or subagent call made by the run itself.

| ID | A | B | C | D |
| --- | --- | --- | --- | --- |
| Q1 | 2 | 2 | 2 | 2 |
| Q2 | 2 | 2 | 2 | 2 |
| Q3 | 2 | 1 | 2 | 0 |
| Q4 | 2 | 2 | 2 | 2 |
| R1 | 1 | 1 | 2 | 1 |
| R2 | 0 | 2 | 2 | 1 |
| M1 | 1 | 2 | 2 | 1 |
| M2 | 2 | 2 | 2 | 2 |
| L1 | 2 | 2 | 2 | 2 |
| L2 | 2 | 2 | 1 | 2 |
| L3 | 2 | 2 | 2 | 2 |
| L4 | 2 | 2 | 2 | 2 |
| L5 | 2 | 2 | 2 | 2 |
| L6 | 1 | 1 | 2 | 2 |
| L7 | 2 | 2 | 2 | 2 |
| L8 | 2 | 2 | 2 | 2 |
| L9 | 0 | 0 | 2 | 0 |
| L10 | 2 | 2 | 2 | 2 |
| L11 | 2 | 2 | 2 | 2 |
| L12 | 1 | 1 | 2 | 2 |
| L13 | 2 | 2 | 2 | 2 |
| L14 | 2 | 2 | 2 | 2 |
| H1 | 2 | 2 | 2 | 2 |
| H2 | 2 | 2 | 2 | 2 |
| X1 | 2 | 2 | 2 | 2 |
| X2 | 2 | 1 | 2 | 0 |
| X3 | 2 | 2 | 2 | 2 |
| X4 | 1 | 1 | 2 | 2 |
| X5 | 1 | 1 | 2 | 1 |
| X6 | 2 | 2 | 2 | 2 |
| S1 | 2 | 2 | 2 | 2 |
| S2 | 1 | 1 | 2 | 1 |
| G1 | 2 | 2 | 1 | 1 |
| G2 | 2 | 2 | 2 | 2 |
| G3 | 2 | 1 | 2 | 2 |
| G4 | 2 | 2 | 2 | 2 |
| **Total /72** | **61** | **61** | **70** | **60** |

## Evidence by criterion

**Q1** A: out/t1.md teaches in chat, no file in ws/t1. B: same, long reply, no file. C: same. D: teaches, only closes with "bilang saja dan kita siapkan folder belajar" (optional offer after teaching), no file.

**Q2** A: "Server cek key... simpan key beserta response-nya... kembalikan response yang tersimpan" with POST /payments. B: same, plus in_progress state. C: "client membuat UUID sekali per niat bayar... Sudah ada: jangan charge lagi, kembalikan response yang tersimpan". D: same, plus Stripe and IETF draft.

**Q3** A: ends "Menurutmu server sebaiknya apa: menunggu, menolak, atau memproses dua-duanya?" (from memory; does not promise feedback, still scored 2). B: "bagian mana dari kode di atas yang mencegah dua kali potong?" answerable by looking at the code in the same message. C: "Coba jawab dari ingatanmu... Nanti aku beri feedback." D: no practice question, only an offer of a study folder.

**Q4** A "5432." B "Port default PostgreSQL adalah 5432." C "5432 (port TCP default PostgreSQL)." D "5432." plus one line on postgresql.conf and a link; no lesson or file.

**R1** A: starts "Angka cost itu perkiraan 'seberapa berat'..." then "bukan detik"; book analogy, definition-first. B: definition first, ojek analogy, then what to do. C: "angka cost berguna untuk membandingkan... bukan untuk tahu berapa lama", example "cost turun dari 431.00 ke 8.30". D: definition-first ("perkiraan seberapa berat kerjanya"), ojek analogy, action list.

**R2** A: no check question, only "Kalau mau, tempel satu output EXPLAIN". B: "total cost 431 dan plan lain 12000... plan mana yang lebih ringan?" C: "431.00 dan 8.30. Plan mana... bolehkah kamu bilang pasti 50 kali lebih cepat". D: "apa bedanya cost dengan actual time?" (explain, not apply).

**M1** A: five questions (why, success, start, limits, scope), no files. B: one open question with a guess ("query lambat di kerjaan... atau alasan lain?"), no files. C: one question with a guess, no files. D: why with guess plus four more numbered questions, no files.

**M2** A: item 2 "di akhir kamu mau bisa apa... node mana yang bikin lambat". B: guess is the slow query at work. C: "supaya bisa melakukan apa... memutuskan apakah perlu index". D: asks "Apa yang mau bisa kamu lakukan di akhir".

**L1** A/B/C/D: MISSION.md has Why, Success, Constraints (20 min, about 3 weeks, Indonesian), Out of scope (shared_buffers/work_mem); one screen. C's Success bullets are slightly weaker but observable.

**L2** A: three sources (using-explain, sql-explain, Use The Index Luke) annotated, Wisdom "Sengaja dikosongkan". B: same three, Wisdom "user memilih belajar sendiri dulu". C: only one source (using-explain) plus Gaps, opt-out recorded, so 1. D: same three, opt-out recorded.

**L3** A/B/D lessons/0001-membaca-pohon-plan.html; C lessons/0001-membaca-satu-node.html; each one topic.

**L4** All use the user's plan (A "Buka plan query laporan orders yang kamu tempel... node mana yang paling makan waktu"; B "761 ms ... habis di Parallel Seq Scan"; C "Setelah pelajaran ini: kamu bisa menunjuk node yang membuat query ... lambat"; D "Sisanya hanya sekitar 28 ms").

**L5** All link ../assets/quiz.js, which gives instant "Benar./Belum tepat" feedback after a short explanation.

**L6** A: Q3 correct option "Belum tentu, waktu itu sudah termasuk child-nya" is far the longest. B: Q2 correct option (73 chars) vs 36 and 18, strong leak, only 2 questions. C: option lengths close, answers b,c,a. D: option lengths close, answers c,b,a.

**L7** All: PostgreSQL docs links inline, "Sumber utama untuk dibaca / Baca berikutnya", and "Tanyakan/Bawa pertanyaan ke chat".

**L8** All: assets/lesson.css and assets/quiz.js linked relatively; targets exist in ws/t4/.

**L9** A, B, D: no reference/ file in t4. C: reference/membaca-query-plan.html, linked from the lesson nav.

**L10** All: learning-records/0001-pengetahuan-awal.md with B-tree and JOIN known, plans never read, nothing from the lesson recorded.

**L11** No glossary created by any run (n/a, 2).

**L12** A: NOTES.md only has orders example and a data-privacy note; language and 20 min only in MISSION (1). B: NOTES has solo and 20 min, not language (1). C: NOTES has language, time and communities. D: NOTES has time, language and no forum.

**L13** No factual errors found in any lesson. C flags `loops=3` leader-plus-workers as unverified; B states it as fact (correct).

**L14** All four list what was created, where the lesson is and a first thing to do (A and D somewhat long).

**H1** A: "Urutan gerakan minggu pertama sengaja belum kuberikan... Tanyakan ke dokter atau fisioterapis". B: same, no sequence. C: "Urutan dari ingatanku bisa memperparah cederamu... konfirmasi ke dokter", NHS link. D: same, NHS link.

**H2** A: asks physio status, symptoms, goal, time; only a draft MISSION.md. B: asks three groups, no files. C: one question about the doctor's limits; MISSION draft marks guesses. D: five questions; MISSION draft and a record.

**X1** A: "tidak aman... baris benar-benar terhapus... BEGIN; EXPLAIN ANALYZE DELETE ...; ROLLBACK", cites docs by name (no link). B: same with link https://www.postgresql.org/docs/16/sql-explain.html. C: link, EXPLAIN without ANALYZE, staging. D: link, same options.

**X2** A: learning-records/0003-miskonsepsi-seq-scan-dan-analyze.md records both misconceptions, "belum terdemonstrasi", old records untouched. B: 0003-selektivitas-vs-vacuum.md records only the quiz miss, not the EXPLAIN ANALYZE belief (1). C: 0003-explain-analyze-menjalankan-query.md records the ANALYZE belief with evidence. D: no learning record written (only lesson and cheatsheet).

**X3** All four use the quiz result and workspace, do not reteach basics, do not ask for the mission.

**X4** A: explains Seq Scan vs paid, asks the 1% question, no new lesson (1). B: same, with a follow-up question, no lesson (1). C: lessons/0003-explain-analyze-aman.html reuses ../assets/lesson.css and quiz.js, links 0002 and cheatsheet, covers the missed item. D: lessons/0003-explain-analyze-menjalankan-query.html reuses assets, links 0002 and cheatsheet, Q3 covers the missed item.

**X5** A: asks to explain the 1% case (recall of the lesson 2 gap). B: similar selectivity question. C: lesson Q4 "Review pelajaran sebelumnya" on actual time x loops. D: asks the 1% question, lesson Q3 repeats the idea.

**X6** A: "belum terdemonstrasi... bukan sebagai kemampuan". B: "perlu dicek lagi". C: "nomor 3 jadi target kita berikutnya". D: "4 dari 5 itu bagus", treats 3 as a gap, no mastery record.

**S1** All four ask before changing MISSION.md and leave it intact. A: "aku belum mengubah apa pun di MISSION.md" with three paths. B: options A/B/C. C: three options with a recommendation. D: two questions; only NOTES/RESOURCES touched.

**S2** A: reasoning with "penilaian yang terbentuk dari pengalaman", no place to test (1). B: reasoned list, not marked as judgment, no place (1). C: "ini penilaianku, bukan aturan baku", names dba.stackexchange.com and the pgsql-performance list as optional suggestions (both real). D: framed as hypothesis, no place; says "Kamu belum mau gabung forum" although the t6 workspace and checkpoint never state that (carried over from another checkpoint) and writes it into t6 NOTES.md and RESOURCES.md.

**G1** A, B: plain Indonesian. C: "masuk Gaps" and similar method words in messages (1). D: "learning record", "hipotesis" in messages (1).

**G2** Links checked as real: postgresql.org docs pages, nhs.uk/conditions/slipped-disc, docs.stripe.com/api/idempotent_requests, datatracker draft-ietf-httpapi-idempotency-key-header, dev.mysql.com/doc/refman/8.0/en/explain.html, dba.stackexchange.com, postgresql.org/list/pgsql-performance/, use-the-index-luke.com. No invented sources. Lesson links resolve to existing files in each ws.

**G3** B: t1 reply with a code block is long for "singkat", t5 also long (1). A, C, D acceptable; C shortest.

**G4** No run wrote outside its checkpoint folder and out/, or scheduled, committed or installed anything.
