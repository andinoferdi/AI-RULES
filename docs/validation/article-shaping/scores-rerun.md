# Scores: article shaping, three runs

| Criterion | A | B | C |
| --- | --- | --- | --- |
| S1 Reader first | 0 | 2 | 2 |
| S2 Opening choice | 2 | 2 | 2 |
| S3 Distinct angles | 2 | 2 | 2 |
| S4 From the pile | 2 | 2 | 2 |
| S5 Paths shown | 1 | 2 | 1 |
| W1 One agreed block per write | 2 | 2 | 2 |
| W2 Author edit kept | 0 | 2 | 2 |
| W3 Next candidates | 1 | 2 | 1 |
| W4 Grounding in the text | 2 | 2 | 2 |
| W5 Block size | 2 | 2 | 1 |
| E1 No invention | 1 | 2 | 1 |
| E2 Pressure gap | 2 | 2 | 2 |
| E3 Raw untouched | 2 | 2 | 2 |
| E4 Author's voice | 2 | 2 | 2 |
| D1 Pushback | 2 | 2 | 2 |
| D2 Format choice | 1 | 1 | 1 |
| D3 Leftovers | 2 | 2 | 2 |
| P1 Natural Indonesian | 1 | 1 | 1 |
| P2 Rhythm | 1 | 2 | 1 |
| P3 Messages to the author | 0 | 2 | 1 |
| **Total (max 40)** | **28** | **38** | **32** |

## Evidence by criterion

**S1**
- A: transcript.md Reply 1 never asks about or states the reader; goes straight to openings. Reader only appears after author message 2 ("Karena pembacamu terbiasa dengan CRUD..."). 0.
- B: Reply 1 "Usul saya, pembaca sudah tahu: ... Apakah daftar ini sudah pas...?" and writes nothing first. 2.
- C: Reply 1 section "1. Pengetahuan pembaca di awal" proposes list, asks question 2 "Pembacanya hanya engineer, atau ada non-teknis juga?". 2.

**S2**
- A: three finished-prose openings in Reply 1; opening written only after "opening pertama". 2.
- B: A/B/C blockquote openings in Reply 2; written in Reply 3 after choice. 2.
- C: A/B/C blockquotes in Reply 1; written after choice. 2. Note: the written opening differs from candidate A (title added, "sebagian membayar"), but the choice was made first.

**S3**
- A: opening 1 incident, opening 2 "Bug harga ini bukan salah cache", opening 3 two colliding facts; different theses. 2.
- B: each states a thesis: incident opens deeper problem / cache is a copy and reader is not at fault / ownership of truth. 2.
- C: each labelled "tesis": found through complaint / cache as price board / organisational root cause. 2.

**S4**
- A: all three built from 12.12, Raka's line, the two sources. 2.
- B: A incident, B chalk-board, C Raka; all from the pile. 2.
- C: A incident, B chalk-board, C Raka. Candidate A adds "Seorang pembeli menulis ke CS" and a rhetorical "Pukul berapa" frame but is still pile-based. 2.

**S5**
- A: Opening candidates carry no "introduces / opens next" lines, only a recommendation (Reply 1). Next-block candidates do ("Bagian ini memperkenalkan 'TTL' ... menyiapkan kalimat Raka", Reply 3). 1.
- B: Openings: "Tesisnya... Yang diperkenalkan: ... Berikutnya bisa langsung menjelaskan..."; blocks: "Pembaca jadi mengenal TTL ... Berikutnya bisa membuka solusi". 2.
- C: Blocks do it well ("Menanamkan: TTL ... "). Openings give a thesis and risk, with a next step only for A ("mengarah ke soal kepemilikan"); introduces is weak. 1. Unsure between 1 and 2.

**W1**
- A: Replies 2, 3, 4 each add the single agreed block. 2.
- B: Reply 3 writes only the opening, Reply 4 only block 2; Reply 5 writes nothing. 2.
- C: one block per write (opening, cache block, severity block). 2.

**W2**
- A: article.after-reply3.md lacks "Saya sendiri baru tahu kejadian ini besok paginya, dari grup CS."; Reply 3 "Saya hapus kalimat itu". Lost. 0.
- B: after-reply4.md and final keep the sentence verbatim in place, "tidak diubah". 2.
- C: final keeps it verbatim after paragraph 2; Reply 3 flags but keeps. Not contradicted (later "Kami tidak tahu dari monitoring" is not a conflict). 2.

**W3**
- A: Reply 2 and 3 offer three, but candidate B in Reply 2 "butuh A dulu" and B in Reply 3 "TTL belum dijelaskan" lean on unintroduced material; Reply 4 offers only one ("Beat 4 yang saya usulkan"). 1.
- B: Replies 3 and 4 offer two each, all reachable from what is introduced (Reply 4 option 2 explicitly "TTL tetap belum dikenalkan" so it avoids it). Reply 5 gives three options for the severity block. 2.
- C: three each time, but Reply 3 option 3 (Raka) and Reply 4 options 2 and 3 lean on "sumber kebenaran" or TTL not yet introduced (flagged). 1.

**W4**
- A: final: "cache ... salinan data yang disimpan sementara" before use; "TTL" glossed ("masa berlaku yang disebut TTL"). Invalidation and source of truth not yet used. 2.
- B: "cache di Redis, yaitu salinan data yang disimpan terpisah dari database"; nothing else used. 2.
- C: "cache, yaitu salinan harga..." explained before use. Title "Harga yang nyangkut di cache" uses the word before it is explained, but the body does not rely on it. 2 (unsure).

**W5**
- A: opening is one scene move, block 2 is one mechanism move, block 3 is TTL window with a gap marker. 2.
- B: both blocks are single-move. 2.
- C: block 2 bundles mechanism plus chalk-board image in two paragraphs, and block 3 bundles severity framing plus the gap admission. 1.

**E1** (checked against raw.md and author messages)
- A: "harga promo yang tersimpan sebelum jam 00.00 bisa tetap tampil sampai jam 6 pagi" is a derived time not in raw (and loosely reasoned: an entry cached before 00.00 would expire before 06.00); "Tidak ada alarm yang berbunyi. Dari sisi sistem, semuanya tampak berjalan normal." is an inferred detail (the runner admits it). No invented number or name. 1 (could argue 0 for the derived time).
- B: article and replies stay within raw ("tahun lalu", TTL, Redis, CS). Nothing invented. 2.
- C: "sebagian membayar harga yang seharusnya sudah tidak berlaku", "pembeli yang cukup teliti ... cukup peduli untuk menulis ke CS", "seberapa buta kami waktu itu", "tempat yang lebih cepat" are invented characterisation with no number or name. 1.

**E2**
- A: Reply 4 "catatanmu tidak punya ... jumlah pesanan"; offers choice 1/2; writes `[GAP: ...]`, no invented count. 2.
- B: Reply 5 "catatanmu tidak punya angka itu ... finance cuma bilang 'beberapa'", writes nothing, offers options. 2.
- C: Reply 4 "bahan mentah tidak punya angka dampak" and writes "Kami belum tahu ... finance hanya menjawab 'beberapa'". 2.

**E3**
- raw-sha256.txt in A, B and C: before equals after (3572f7dc...a63eed). 2 each.

**E4**
- A: chalk-board and Raka's line not used in the article; register casual engineering Indonesian ("dihujani query", "keteteran" avoided but plain). 2.
- B: neither used; register plain and casual. 2.
- C: "Cache mirip papan harga kapur di warung. Kalau yang jualan lupa menghapus, pembeli tetap melihat harga kemarin. Dan pembeli tidak salah: dia membaca apa yang tertulis." The image is kept. 2.

**D1**
- A: Reply 1 flags 11.11 as unproven; Reply 3 flags the stray sentence as unsupported; Reply 4 corrects its own "tidak ada error di log". 2.
- B: Reply 3 explains why the chalk-board image is weaker before TTL; Reply 2 notes the Raka opening risk "pembaca ... belum paham maksud kalimat ini". 2.
- C: 11.11 claim flagged, Reply 3 notes "saya" versus "kami", Reply 4 notes the unexplained checkout path ("checkout pakai harga lama" while the cart reads the database). 2.

**D2**
- A: only beat labels (`scene`, `claim`) and a `[GAP]` marker, no stated rendering and reason. 1.
- B: blockquote candidates, no explicit statement of how a block is rendered. 1.
- C: title plus paragraphs; no stated rendering choice. 1.

**D3**
- A, B, C: Redis vs Memcached and CDN images set aside in Reply 1 (A "Dua topik yang saya usulkan dibuang", B "Bagian yang saya rencanakan tidak masuk", C "Saya usulkan dibuang"); none appears in any article.md. 2 each.

**P1**
- A: "Orang pertama yang sadar bukan sistem monitoring kami, tapi tim CS" is a "bukan X, tapi Y" pattern; also "Halaman produk tidak tahu." personification. 1.
- B: "Yang menyadarinya duluan bukan monitoring kami, tapi tim CS" (mirrors raw's "bukan monitoring") is a "bukan X, tapi Y" pattern. 1.
- C: "Yang membuat kejadian ini tidak enak bukan sekadar angkanya salah. Setiap pembeli..." is a formulaic contrast; "Bahwa kami tidak bisa menyebut angkanya saja sudah menunjukkan..." reads translated. Borderline between 1 and 0; chose 1 because the second is stilted rather than clearly wrong.

**P2**
- A: paragraphs end in summary lines ("Jadi untuk produk yang sama, dua tempat bisa menunjukkan dua harga." and "Dari sisi sistem, semuanya tampak berjalan normal."). 1.
- B: sentence lengths vary; only "Jadi dua tempat itu bisa berbeda." ends as a summary, and it is short. 2 (could be 1).
- C: several paragraph endings are punchlines ("...janji itu sudah kedaluwarsa tanpa ada yang tahu", "...seberapa buta kami waktu itu"). 1.

**P3**
- A: heavy method jargon (`scene`, `claim`, `aside`, `pivot`, "beat", a rough plan of all remaining beats) and several decisions per turn (Reply 2: choose beat, confirm Raka quote, confirm numbers). 0.
- B: each turn asks one decision (pick A/B/C, 1/2). Some wording like "tesisnya" but light. 2.
- C: sectioned, long replies; Reply 1 asks three questions; Reply 4 asks two decisions (checkout flow plus next block); mild jargon ("menanamkan"). 1.

## Unsure
S5 (C), E1 (A: derived "jam 6 pagi"), W4 (C: title), P1 (C), P2 (B).
