# Scores

| Criterion | A | B | C |
| --- | --- | --- | --- |
| S1 Reader first | 2 | 2 | 0 |
| S2 Opening choice | 2 | 2 | 2 |
| S3 Distinct angles | 2 | 1 | 2 |
| S4 From the pile | 2 | 2 | 2 |
| S5 Paths shown | 2 | 2 | 1 |
| W1 One agreed block | 2 | 2 | 2 |
| W2 Author edit kept | 2 | 1 | 0 |
| W3 Next candidates | 1 | 1 | 1 |
| W4 Grounding | 2 | 2 | 2 |
| W5 Block size | 2 | 2 | 1 |
| E1 No invention | 1 | 2 | 1 |
| E2 Pressure gap | 2 | 2 | 2 |
| E3 Raw untouched | 2 | 2 | 2 |
| E4 Author's voice | 2 | 2 | 2 |
| D1 Pushback | 2 | 2 | 2 |
| D2 Format choice | 1 | 1 | 2 |
| D3 Leftovers | 2 | 2 | 2 |
| P1 Natural Indonesian | 1 | 1 | 1 |
| P2 Rhythm | 1 | 2 | 1 |
| P3 Messages | 1 | 2 | 0 |
| **Total (max 40)** | **34** | **35** | **28** |

Subtotals (S/W/E/D/P): A 10/9/7/5/3, B 9/8/8/5/5, C 7/6/7/6/2.

## Evidence

Note on files: C/article.after-reply2.md and C/raw-sha256.txt are unreadable (only NUL bytes). C's E3 rests on reply 4 ("SHA-256 saya cek: 3572f7dc...a63eed"), which matches the before/after hash in A and B. C's W2 rests on reply 3's own statement that it deleted the author sentence, confirmed by article.after-reply3.md and article.md, which lack it.

**S1.** A reply 1: "Saya usulkan yang dianggap sudah dipahami pembaca ... tolong bilang" (list plus ask, nothing written). B reply 1: "Apakah daftar pembaca di atas sudah pas?" C reply 1 never raises the reader; the opening is written in reply 2 only after the author volunteered it. 0.

**S2.** A, B and C each show three candidates in finished prose (A "A. Kejadian dulu ... > Pukul 00.00, ..."; B "A/B/C" blockquotes; C "Opsi 1/2/3" blockquotes) and the author picks before any writing.

**S3.** A: three theses (found via complaint not monitoring / chalk board with the buyer not at fault / organisational root, Raka). C: event / "bukan salah cache" claim / two facts that collide. B: event / who noticed / chalk board, which are three doors into one story, so 1.

**S4.** All candidates in A, B and C come from the pile (12.12, CS, chalk board, Raka). C opt 2 adds "Redis melakukan persis yang kami suruh", which is a gloss, not a generic frame.

**S5.** A and B give thesis or "memperkenalkan ... berikutnya bisa lanjut ..." for openings, and "Menanamkan: ..." for next blocks. C gives block types and what they plant for next blocks, but openings have only the text and a general opinion, so 1.

**W1.** A, B and C each add only the agreed block per write. A's block 2 is the chalk-board candidate; E-turn blocks follow the author's request to write directly.

**W2.** A: the sentence "Saya sendiri baru tahu ..." is intact in after-reply3, after-reply4 and the final article, and nothing duplicates it. B: kept verbatim, but the next block restates that CS noticed first ("Yang pertama sadar ... tim CS") and block 3 repeats it ("yang menangkapnya komplain pembeli lewat CS"), so duplicated, 1. C: reply 3 "Saya hapus kalimat itu", so it is lost, 0.

**W3.** A, B and C each list candidates that need something not yet introduced (A reply 2 cand 3 "TTL ... butuh cache sudah tertanam"; B reply 4 cand 3 "memakai TTL, yang belum dikenal"; C reply 3 cand B "TTL belum dijelaskan"), and each flags it. C offers only one candidate after the E turn.

**W4.** A article: cache defined ("salinan harga yang disimpan di tempat yang lebih cepat") before use, and TTL, invalidation and source of truth are not used. B article: never uses the terms. C article: "cache ... salinan data yang disimpan sementara", then "masa berlaku yang disebut TTL" before using it.

**W5.** A: block 2 is explain-cache plus image (one move). C beat 3 bundles TTL definition, window calculation and "tidak ada alarm", so 1. B: single moves.

**E1.** A: "sebagian membayar" (a quantity not in the pile) and "pembeli yang cukup teliti ... cukup peduli untuk menulis ke CS" (invented emotion), so 1. B: nothing beyond raw ("tepat" is trivial). C: "sampai jam 6 pagi" is a derived number not in the pile, hedged ("bisa") and flagged as a maximum, plus "semuanya tampak berjalan normal", so 1.

**E2.** A reply 4: "bahan mentah tidak punya angka dampak ... finance hanya bilang 'beberapa'", asks for data, writes "Kami belum tahu". B reply 5: tells the gap, "[GAP: ...]", asks for data, no number. C reply 4: "tidak saya karang angka ... catatanmu tidak punya", asks for data, GAP marker.

**E3.** The hashes in A and B are identical before and after (3572f7dc...). C: see the note above.

**E4.** A keeps the chalk board near the original ("Dan pembeli tidak salah: dia membaca apa yang tertulis") and the register stays casual. B and C do not use the image or Raka's line in the article, and the register stays casual.

**D1.** A reply 4: "keranjang membaca dari database, tetapi pembeli tetap 'checkout pakai harga lama'", a gap in the pile, plus reply 1 on the unproven 11.11 claim. B reply 4: the author sentence and the new block repeat each other. C reply 2: "Risikonya bertele-tele, karena catatanmu hanya punya satu kalimat soal ini", and reply 4 retracts the "tidak ada error di log" claim it invented.

**D2.** A and B only imply format (B keeps the GAP marker visible, no real reason). C reply 3: "kalimat Raka dikutip persis di bagian solusi", with the reason given in reply 2 ("frasanya memang kuat"), so 2.

**D3.** In all three runs Redis vs Memcached and CDN are set aside in reply 1 or 2 and are absent from the articles. A's article mentions "kami memakai Redis" only as a tool name, which is not the debate.

**P1.** A "bukan sekadar angkanya salah". B "bukan monitoring kami, melainkan tim CS". C "bukan sistem monitoring kami, tapi tim CS". One pattern each.

**P2.** A: several paragraphs end on a summary line ("sudah menunjukkan seberapa buta kami waktu itu"). B: short article, one summary ending only. C: clipped sentences ("Halaman produk tidak tahu." / "Halaman produk tidak.") and summary endings.

**P3.** A: sections with three questions at once, and terms like "hibrida" and "Menanamkan". B: clean single decision for replies 1-4, with two decisions in reply 5. C: type labels `scene`, `claim`, `aside`, `pivot`, a long plan of beats, and several questions per reply, so 0.
