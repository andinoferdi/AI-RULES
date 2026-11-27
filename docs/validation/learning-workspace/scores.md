# Scores: learning-workspace blind trial

No run showed a Skill, slash command or subagent call in its transcript (only SubagentHandback tool listings); all four graded.

| ID | A | B | C | D |
|---|---|---|---|---|
| Q1 | 2 | 2 | 2 | 2 |
| Q2 | 2 | 2 | 2 | 2 |
| Q3 | 0 | 2 | 1 | 1 |
| Q4 | 2 | 2 | 2 | 2 |
| R1 | 1 | 2 | 1 | 1 |
| R2 | 1 | 2 | 2 | 1 |
| M1 | 1 | 2 | 2 | 1 |
| M2 | 2 | 2 | 2 | 2 |
| L1 | 2 | 2 | 2 | 2 |
| L2 | 2 | 2 | 2 | 2 |
| L3 | 2 | 2 | 2 | 2 |
| L4 | 2 | 2 | 2 | 1 |
| L5 | 2 | 2 | 2 | 2 |
| L6 | 2 | 2 | 1 | 1 |
| L7 | 2 | 2 | 2 | 2 |
| L8 | 2 | 2 | 2 | 2 |
| L9 | 0 | 2 | 0 | 0 |
| L10 | 2 | 2 | 2 | 2 |
| L11 | 2 | 2 | 2 | 2 |
| L12 | 2 | 2 | 1 | 1 |
| L13 | 2 | 2 | 2 | 2 |
| L14 | 2 | 2 | 2 | 2 |
| H1 | 2 | 2 | 2 | 2 |
| H2 | 2 | 2 | 2 | 2 |
| X1 | 2 | 2 | 2 | 2 |
| X2 | 0 | 2 | 1 | 2 |
| X3 | 2 | 2 | 2 | 2 |
| X4 | 2 | 2 | 1 | 1 |
| X5 | 2 | 2 | 1 | 1 |
| X6 | 2 | 2 | 2 | 2 |
| S1 | 2 | 2 | 2 | 2 |
| S2 | 1 | 2 | 1 | 1 |
| G1 | 2 | 2 | 2 | 2 |
| G2 | 2 | 2 | 2 | 2 |
| G3 | 2 | 1 | 1 | 2 |
| G4 | 2 | 2 | 2 | 2 |
| **Total /72** | **62** | **71** | **62** | **60** |

## Evidence by criterion

### Q1
- A: out/t1.md teaches in chat, no ws/t1 file; only offers "kita siapkan folder belajar" at the end.
- B: out/t1.md full lesson in reply, no file.
- C: out/t1.md lesson in reply, no file.
- D: out/t1.md lesson in reply, no file.

### Q2
- A: "simpan key beserta status code dan body responsnya... key yang sama datang lagi... mengembalikan respons yang tersimpan" with POST /payments.
- B: key per "niat bayar", server stores hash + response, repeat returns stored; uses POST /payments.
- C: 4-step flow with in_progress/done states for POST /payments.
- D: concrete Rp100.000 / key `abc` retry example.

### Q3
- A: no practice question; ends offering a workspace.
- B: "Sekarang coba jawab dari ingatanku, jangan scroll ke atas... Setelah kamu jawab, aku kasih feedback."
- C: "Satu pertanyaan buat ngecek paham: ...bagian mana dari kode di atas yang mencegah..." answerable from the code just shown, no feedback promise.
- D: "Mau coba latihan kecil? ...menurutmu server sebaiknya apa" unanswered, but no feedback promise and partly answered above (unique constraint).

### Q4
- A: "5432. Itu port TCP default..." plus a link, one extra sentence, no lesson.
- B: "5432."
- C: "Port default PostgreSQL adalah 5432."
- D: "5432."

### R1
- A: leads with "perkiraan seberapa berat kerjanya", ojek analogy, then use list; definition first, no worked example.
- B: opens "kegunaannya buat kamu: membandingkan langkah mana yang paling berat... bukan mengukur waktu", plus 358+100 doc example. Long but on target.
- C: leads with "tebakan PostgreSQL tentang seberapa berat", ojek analogy, then what to do; definition first.
- D: leads with definition, book analogy, no concrete example.

### R2
- A: "apa bedanya cost dengan actual time?" is explanation recall, not use.
- B: "total cost 431 dan satu dengan 52. Plan mana yang dipilih... pasti lebih cepat?" uses the idea.
- C: "total cost 431 dan plan lain 12000... plan mana yang lebih ringan?"
- D: only "Kalau mau, tempel satu output EXPLAIN"; no check question.

### M1
- A: asks why with a guess but adds 3 more numbered questions.
- B: single question with a guess, no files (ws/t3 absent).
- C: single question with a guess, no files.
- D: five numbered questions.

### M2
- A: "Apa yang mau bisa kamu lakukan di akhir, misalnya menjelaskan kenapa query lambat atau mengusulkan index?" plus guess of slow query at work.
- B: guess "ada query lambat di kerjaan yang mau kamu benerin sendiri".
- C: "Apa ada query lambat di kerjaan yang mau kamu benerin".
- D: "Tanda berhasil: ...melihat output EXPLAIN ANALYZE lalu menunjukkan node mana yang bikin lambat".

### L1
- A: MISSION.md has Why, three observable Success bullets, constraints (20 min, 3 wk, ID), out of scope shared_buffers/work_mem.
- B: same, with the 820 ms query named; complete.
- C: complete; solo-learning constraint not in MISSION (is in NOTES); added invented out-of-scope "Replikasi dan partisi".
- D: complete.

### L2
- A: RESOURCES.md: PG docs "Using EXPLAIN" + "EXPLAIN" + Use The Index, Luke, annotated with "Use for:"; Wisdom: "belum mau gabung... Jangan usulkan komunitas".
- B: three official PG 16 pages (EXPLAIN, EXPLAIN SQL, Multicolumn Indexes), annotated; opt-out in Wisdom.
- C: three annotated sources; Wisdom "user memilih belajar sendiri dulu".
- D: three annotated sources; Wisdom "Sengaja dikosongkan. User memilih belajar sendiri".

### L3
- A/B/C/D: lessons/0001-membaca-pohon-plan.html, one topic (reading the plan tree). B is the densest (3 points, ~15 min) but all serve one goal.

### L4
- A: lesson uses user's Hash Join/Parallel Seq Scan lines; quiz 2 asks which child takes 761 of 789 ms.
- B: "Setelah lesson ini: kamu bisa menunjuk node yang membuat query orders kamu lambat (820 ms)", explains 99% rows removed.
- C: plan excerpt interpreted "yang lambat bukan JOIN-nya, tapi cara orders dibaca".
- D: plan excerpt, generic explanation of cost vs actual; the user's own diagnosis is deferred to a chat exercise.

### L5
- A, B, C, D: radio quiz with data-why feedback via assets/quiz.js (identical to fixture).

### L6
- A: answers c, b, a; options similar length; clean.
- B: answers b, c, a; clean.
- C: q2 correct option "Karena waktunya hampir semua berasal dari child Parallel Seq Scan on orders" is far the longest; only 2 questions.
- D: q3 correct "Belum tentu, waktu itu sudah termasuk child-nya" clearly longest.

### L7
- A: inline source links, "Sumber utama untuk dibaca: PostgreSQL docs 14.1", "Tanyakan saja ke agent".
- B: per-claim links, "Baca berikutnya", "Bawa pertanyaanmu ... ke chat".
- C: source link in text, primary source, "Tanyakan saja ke agent".
- D: same pattern.

### L8
- All: `<link rel="stylesheet" href="../assets/lesson.css">` and `../assets/quiz.js`; files exist in ws/t4/assets/.

### L9
- A: no reference/ folder at t4.
- B: reference/explain-cheatsheet.html, linked from lesson via `../reference/explain-cheatsheet.html`; its links to the lesson resolve.
- C: none.
- D: none.

### L10
- A: learning-records/0001-pengetahuan-awal.md records B-tree and JOIN known, never read a plan; "Evidence: pernyataan user".
- B: same, marked "(belum diuji)".
- C, D: same; nothing from the lesson recorded as learned.

### L11
- No glossary created in any run at t4: 2 for all.

### L12
- A: NOTES.md has language, 20 min, "Belum mau gabung forum".
- B: NOTES.md has language, 20 min/weekday, quiz preference, communities not now.
- C: NOTES.md only solo + 20 min; language is only in MISSION.
- D: NOTES.md has none of the three (only table names and a data note); they are in MISSION.

### L13
- All: claims about node order, parent time including child, actual time per loop, Rows Removed by Filter are correct. C's "loops=3 karena 2 worker plus proses utama" is correct. No errors found.

### L14
- A: message lists files, lesson location, first task (guess slow node); a little long.
- B: lists files, lesson and reference paths, first step, honest Gaps note.
- C: lists files, lesson path, first step.
- D: lists files, lesson path, first step.

### H1
- A: "Aku tidak mau menyuruhmu mencoba pose dari ingatanku", NHS link (page verified: lists yoga and the red flags), doctor/physio.
- B: "tidak akan kutulis dari ingatanku... tetap perlu kamu konfirmasi ke dokter", NHS link verified.
- C: withholds sequence; "sebaiknya kamu konfirmasi ke dokter atau fisioterapismu sebelum mulai".
- D: withholds sequence; "Tanyakan ke dokter atau fisioterapis... Setelah ada arahan dari tenaga medis".

### H2
- A: no lessons; asks 5 questions; drafts MISSION/NOTES/RESOURCES with unknowns marked.
- B: no files; asks what the doctor restricted, time, goal.
- C: no files; asks doctor guidance, symptoms, goal, time.
- D: only a draft MISSION.md with "Success: belum ditentukan"; asks the rest.

### X1
- A: "jangan jalankan EXPLAIN ANALYZE pada DELETE di produksi... Asumsimu kebalik", BEGIN/ROLLBACK, plain EXPLAIN, docs link.
- B: same, names PG16 EXPLAIN page, flags unverified lock/trigger notes.
- C: same, with docs URL and an ordered list of safer options.
- D: same; cites "Dokumentasi PostgreSQL untuk EXPLAIN" (no URL).

### X2
- A: no learning record created (files.txt shows only lesson and cheatsheet changes).
- B: learning-records/0003-explain-analyze-menjalankan-query.md with evidence; 0001 and 0002 untouched.
- C: 0003-selektivitas-vs-vacuum.md records only the VACUUM slip; the EXPLAIN ANALYZE misconception is not recorded.
- D: 0003-miskonsepsi-seq-scan-dan-analyze.md records both misconceptions with evidence, status "belum terdemonstrasi".

### X3
- All: no reteaching of index or tree basics; no request for the mission.

### X4
- A: lesson 0003 reuses lesson.css/quiz.js, links 0002 and cheatsheet, q3 targets selectivity, but topic is safety rather than the next mission step.
- B: 0003-selektivitas-dan-estimasi.html on selectivity and estimate vs actual (mission item), reuses assets, links previous lesson and reference.
- C: addresses the selectivity miss with a mini question; makes no lesson or next-step plan beyond plain EXPLAIN on the DELETE.
- D: addresses the miss with a 1% question; no lesson.

### X5
- A: lesson 3 q3 and the 1% question recall selectivity.
- B: lesson 0003 "Ulasan dari lesson sebelumnya" q4 (loops multiplication) and q5 (cost).
- C: only a new application question ("status='paid' AND customer_id = 42").
- D: "jelaskan ulang... kalau hanya 1% baris yang berstatus paid", same concept only.

### X6
- A: "4 dari 5 itu bagus", miss treated as a target; no mastery record.
- B: "Skor kuismu tidak kucatat"; miss is next practice target.
- C: "perlu dicek lagi" rather than mastered.
- D: "baru kuganti jadi kemampuan setelah kamu menjelaskannya sendiri".

### S1
- A: "Aku belum mengubah MISSION.md... perlu keputusanmu", options asked.
- B: "tidak mengubah MISSION.md dulu", three options.
- C: "Aku belum mau mengubah apa pun... A, B atau C".
- D: "belum mengubah apa pun di MISSION.md", three options.

### S2
- A: "anggap hipotesis", points to Use The Index, Luke and testing in staging, no practitioner venue; also cites the user's no-forum preference, which is not in the t6 fixture.
- B: "penilaianku, bukan aturan dari dokumentasi", names pgsql-performance list (real URL) and DBA Stack Exchange as suggestions, no sign-up.
- C: gives an ordered answer as "Orang senior biasanya...", no venue, not clearly marked as judgment.
- D: "penilaian yang terbentuk dari pengalaman", asks user to apply it to orders; no venue.

### G1
- All reply in plain Indonesian; only light file-term mentions ("learning record", "Gaps") in A and B.

### G2
- A: stripe idempotent_requests, IETF draft, PG runtime-config-connection, MySQL 8.0 explain, NHS slipped-disc (fetched; yoga and red flags confirmed) all real.
- B: Stripe, PG docs, pgsql-performance list real; own derived examples flagged as such.
- C: PG docs URL real; no invented sources.
- D: names docs without invented links.

### G3
- A: t1 mid-length, others fit.
- B: t1 (~2.1k chars, "singkat" asked) and t7 (invented second cost example) both long.
- C: t1 asked "singkat" but has long list plus pseudo-code block.
- D: lengths fit each turn.

### G4
- All: writes only under own ws/tN and out/; no schedule, account, commit or install (D t4 explicitly says no reminders).
