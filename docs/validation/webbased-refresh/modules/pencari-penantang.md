# U. Pencari Penantang Terbaik (`pencari-penantang`)

Mode: revision. Old text: module U at WebBased `76f9af1` ("U. PENCARI PENANTANG TERBAIK",
1,916 lines). New text: `skills/pencari-penantang/SKILL.md` on branch
`claude/webbased-daily-rules`.

## Brief (gate 1)

- Consumer: a web chatbot that loads the module as an uploaded skill (Claude.ai, Gemini) or reads
  it pasted into the chat (ChatGPT Free). It may or may not have web search.
- Task: find out whether something better than what the user uses now (the incumbent) exists for
  the user's real job, and say so with evidence, or keep the incumbent.
- Must load: "Aku sekarang pakai WinDirStat buat cari tahu apa yang makan storage. Ada yang lebih
  bagus sekarang?"
- Must not load: "Jelaskan cara kerja disk usage analyzer seperti WinDirStat." (a knowledge
  question, with no choice to compare).
- Output: a verdict first (status, best choice, incumbent, confidence, main reasons), then "layak
  pindah", a comparison with the incumbent in it, trade-offs and sources; the size follows the
  question; eleven keyword modes change the shape.
- Authority limits: names no winner it cannot support; states no price, version, date or benchmark
  number as checked when it was not; claims no "terbaik saat ini" without current sources; lets no
  hard requirement of the user be outranked; searches the web only when access exists and the user
  has not forbidden it; never invents a challenger to have one.

## Routing table (gate 2)

Kinds: shape, omission, condition, discipline, fact. Destinations: module (the line in the new
text), A (already covered by A. PRIORITAS), nothing (with a reason). Rows are grouped by the topic
headings of the old text; every rule, mode, output part and hard rule of the old text appears in a
row. Rows U1 to U11 cover the role and scope, U12 onward the method.

| ID | Old text (short) | Kind | Destination |
| --- | --- | --- | --- |
| U1 | Role: find the best challenger for what the user uses, considers or believes is best; the user's choice is the INCUMBENT, not an automatic winner | discipline | module: purpose paragraph, Aturan 1 |
| U2 | Main goal: decide whether something really fits the user's need better; prove it with relevant criteria and evidence; keep the incumbent when the gain is not meaningful | discipline | module: purpose paragraph, Aturan 1 |
| U3 | "Aktif bila dikirim bersama A" | condition | module: purpose paragraph (works alone; follow A when present) |
| U4 | Not just an "alternative" finder; the question is whether something is truly better for the job; the winner follows the user's need, not product reputation | discipline | module: Aturan 1 |
| U5 | Scope: comparable categories (software, hardware, gadgets, services, apps, platforms, tools, workflows, methods, vehicles, gear, products, technology, places, local services, strategies) | condition | module: Kapan dipakai |
| U6 | Method follows the category; no software criteria for a restaurant; no hardware benchmark for a workflow; no single framework for every object | discipline | module: Aturan 2 |
| U7 | Do not accept "this is the best" from popularity, fame, age, newness, price, being free or open source, most features, top rating, frequent recommendation or top search rank; each is a signal, none proves it | discipline | module: Aturan 3 |
| U8 | Kinds of "best" (popular, most complete, fastest, cheapest, best value, best for the majority, technically best, best for the user); the priority is best for the user (job, priorities, constraints, budget, platform, location, ecosystem, skill, workflow) | discipline | module: Aturan 3 |
| U9 | Job to be done: before searching, find the real job (problem, wanted result, main work, must-have and nice-to-have features, current bottleneck, what is liked about the incumbent, what to improve, constraints); the WinDirStat example, search by outcome not by category name | omission | module: Langkah 1, Aturan 4 |
| U10 | Outcome over category: a different-category solution is a challenger when it solves the job better; do not offer one when the added complexity outweighs the gain | condition | module: Aturan 4 |
| U11 | Incumbent baseline: check what matters (function, features, performance, quality, reliability, usability, resources, compatibility, integration, privacy, security, price, license, subscription, maintenance, last update, support, ecosystem, portability, lock-in, real weaknesses); use the latest version or state when information changes; do not compare a new challenger with old incumbent data | omission | module: Langkah 3, Aturan 5 |
| U12 | Incumbent now (what the user really runs) versus incumbent latest (newest available); check whether the problem is already fixed in the latest; do not recommend a big migration when upgrading the incumbent solves it more cheaply | condition | module: Aturan 5 |
| U13 | Best new choice ("starting from zero today") versus best switching decision ("should an incumbent user move"); the challenger can be best for a new buyer but not enough for a switch; switching considers migration effort, learning curve, data transfer, compatibility, disruption, retraining, add-on replacement, sunk integration, account migration, downtime; no "upgrade" from a slightly better benchmark | condition | module: Aturan 11 |
| U14 | Material improvement: ask internally whether the difference is big enough to be felt or change the outcome; tiny difference is SIDEGRADE or MINOR UPGRADE; real but narrow is SPECIALIZED WINNER; overall better is NEW WINNER; none is INCUMBENT RETAINED | condition | module: Aturan 14 |
| U15 | Discovery from several directions; challenger types (direct, specialist, modern, mature, free, open-source, premium, lightweight, power-user, alternative-approach, hidden); not every type on every task, only the relevant ones | condition | module: Langkah 4 |
| U16 | Web research: when the user asks for current best, best challenger, "masih terbaik?", "ada yang lebih bagus?", best alternative, current best or equivalent, use web search if access exists; do not rely on model memory for claims that change | condition | module: Langkah 2, Aturan 7 |
| U17 | No web access: do not claim to have determined "the best right now"; give a comparison from the available information and state the limit | condition | module: Langkah 2, Aturan 7 |
| U18 | Research depth: discovery finds candidates, verification checks finalists in depth; not a mechanical two-round search for a simple case; a candidate is not chosen from the first search result and a finalist is verified before it is declared the winner; complex category or DEEP: discovery and verification as clear stages | discipline | module: Langkah 4 and 6, Mode "DEEP" |
| U19 | Query diversity: search by job and failure mode, not only "[X] alternatives" (the ten query patterns); adapt to the category; do not run all of them to fill a checklist; stop when strong candidates are found and more search adds nothing material | shape | module: Langkah 4 |
| U20 | Current information: check the latest state of price, plans, version, license, availability, country, compatibility, updates, development status, hardware revision, policy, feature availability, support lifecycle; no old price or feature without noting the date | condition | module: Aturan 7 |
| U21 | Regional price: use the user's region when known; unknown and material: state the region assumption or ask only when really needed | condition | module: Aturan 7 |
| U22 | Sources by claim type: official (specs, features, compatibility, official price, license, version, support, docs, availability); independent testing (performance, battery, latency, efficiency, thermals, image quality, accuracy, testable metrics); expert (security, privacy, regulation, health, specialist fields); independent review (workflow, usability, ergonomics, setup, experience, hidden limits); community (bugs, reliability issues, edge cases, compatibility, support experience, real workflow, long-term problems); no single source type for all claims | discipline | module: Aturan 9 |
| U23 | Official source says what a product claims, but is not neutral on whether it beats competitors; cross-check important winner claims with independent sources when available | discipline | module: Aturan 9 |
| U24 | Benchmark fairness: comparable conditions (version, hardware, dataset, workload, resolution, settings, environment, methodology, sample size, measurement, configuration); no apples-to-oranges; not comparable means "TIDAK CUKUP DATA" rather than a forced winner | discipline | module: Aturan 10 |
| U25 | One benchmark is not the world: no universal winner from one benchmark; use the benchmark closest to the user's use; when results differ, explain what changes them | discipline | module: Aturan 10 |
| U26 | Reviews and community are experience evidence, not ground truth (count, pattern, recency, version, sampling bias, credibility); one comment is not "often crashes"; use "terdapat beberapa laporan..." when evidence is limited; raise confidence for a consistent pattern from many sources | discipline | module: Aturan 9 |
| U27 | Sponsored, affiliate, advertorial, influencer and vendor comparison pages may carry a conflict of interest; useful but not the main basis for a winner without independent verification; "independent" labels are not trusted without context | discipline | module: Aturan 9 |
| U28 | SEO listicles ("10 Best X") are for discovery, not proof that #1 is best; verify finalists with stronger sources | discipline | module: Aturan 9 |
| U29 | Mandatory filter before scoring or ranking: drop candidates that fail a hard requirement (wrong platform, budget, missing must-have, unavailable region, license, ecosystem, privacy, security, too complex, missing format, hardware the user lacks); a failing candidate never wins on another benchmark | discipline | module: Langkah 5, Aturan 6 |
| U30 | Hard requirement versus preference: "harus gratis" means a paid product cannot win; "kalau bisa gratis" makes price a preference; do not treat them the same | condition | module: Aturan 6 |
| U31 | Comparison criteria chosen by the job (quality, performance, speed, accuracy, reliability, usability, workflow efficiency, feature fit, resources, compatibility, integration, privacy, security, maintenance, support, ecosystem, portability, extensibility, lock-in, upfront and recurring cost, TCO, availability, warranty, repairability, switching cost, learning curve, value); do not use the whole list | condition | module: Aturan 2 |
| U32 | Same criteria for incumbent and challenger; no highlighting only challenger strengths; no different criteria to make one win | discipline | module: Aturan 2 |
| U33 | User priorities win ("UI nggak penting, yang penting scanning paling cepat" makes speed outweigh UI; "cuma mau gratis" is a hard requirement; "tidak boleh sering error" makes reliability outweigh feature count); no market preference over explicit user priority | discipline | module: Aturan 2 |
| U34 | Default priorities: infer conservatively from the job and state the short assumption when it affects ranking; when several plausible priorities give different winners, do not pretend one objective ranking | condition | module: Aturan 2 |
| U35 | Scenario winner: when the winner changes by need, say so (best for speed, privacy, value, and best for your need); no forced single universal winner when trade-offs are large | condition | module: Aturan 2, Format jawaban |
| U36 | Anti fake precision: default qualitative MENANG / SETARA / KALAH / TIDAK CUKUP DATA; "SEDIKIT MENANG" when the difference is small but consistent; no "92/100 vs 89/100" without a strong quantitative basis | shape | module: Aturan 10 |
| U37 | Weighted scoring only when criteria are clear, evidence is enough, the scale is defensible and the weights follow user priority; show the main weights when they affect the result; do not hide subjective weighting behind numbers | condition | module: Aturan 10 |
| U38 | Confidence: TINGGI (strong, current, comparable, several sources agree), SEDANG (enough evidence with gaps or hard-to-measure trade-offs), RENDAH (limited data, different versions, benchmarks not comparable, very varied user experience); no high confidence on weak evidence | discipline | module: Aturan 14, Format jawaban |
| U39 | Challenger win condition (six points: meets all hard requirements; materially better on the main priority; no large loss that outweighs it; evidence is enough; relevant to the workflow; switching benefit justifies switching cost for an incumbent user) | discipline | module: Aturan 14 |
| U40 | Verdict classification: NEW WINNER, SPECIALIZED WINNER, MINOR UPGRADE, SIDEGRADE, INCUMBENT RETAINED, NO CLEAR WINNER, INSUFFICIENT DATA, each with its meaning | shape | module: Aturan 14, Format jawaban |
| U41 | Better challenger is not the same as "user must switch"; the final verdict answers both when relevant (the 10% faster, two days of migration example) | discipline | module: Aturan 11 |
| U42 | Switching cost items (install, migration, data conversion, retraining, shortcuts and muscle memory, integration, automation, plugins, account, subscription overlap, downtime, rollback); not an automatic reason to keep the incumbent; a real trade-off | condition | module: Aturan 11 |
| U43 | Total cost: not only the purchase price (subscription, upgrade fee, maintenance, consumables, accessories, cloud usage, support, migration, replacement, licensing); use "total cost of ownership" when the difference is material | condition | module: Aturan 11 |
| U44 | Maintenance and longevity for software or support dependent categories (update cadence, project status, security updates, release history, credible roadmap, support policy, maintainer activity, ecosystem); a mature stable project is not "dead" from a few months without updates | condition | module: Aturan 12 |
| U45 | Future-proofing: not an empty term; define it (support lifecycle, standards, update commitment, headroom, API stability, ecosystem, interoperability, upgrade path); invent no product future; separate official commitment from prediction | discipline | module: Aturan 12 |
| U46 | Privacy comparison needs evidence (policy, architecture, data collection docs, telemetry, storage model, encryption, account requirement, credible audit); not "more private" just for open source or local without checking the data flow | discipline | module: Aturan 12 |
| U47 | Security needs specific evidence; not "safe" because of popularity, open or closed source, big brand or no known incident; without enough evidence write "TIDAK CUKUP DATA" | discipline | module: Aturan 12 |
| U48 | Open source gives auditability, modifiability, self-hosting, portability, community development, but is not proof of security, reliability, usability, maintenance or quality; judge the effect on the user's need | discipline | module: Aturan 3 |
| U49 | Free is a cost factor, not proof of quality; check trade-offs (ads, telemetry, limits, support, ecosystem, sustainability) when relevant; do not assume a free product has bad trade-offs; verify | discipline | module: Aturan 3 |
| U50 | Premium price must be justified by real benefit; premium positioning alone adds no value when the user does not use the features | discipline | module: Aturan 3 |
| U51 | Recency: newer is not better and older is not obsolete; use it when it matters (compatibility, security, platform, performance, support, availability, features); a mature stable product can beat a new challenger | discipline | module: Aturan 3 |
| U52 | Popularity gives ecosystem, support, community knowledge, integration, availability, resale, hiring familiarity; value that benefit, do not use popularity as a proxy for quality | discipline | module: Aturan 3 |
| U53 | Feature count: judge features by use; irrelevant features get little or no weight (200 features versus the five the user needs) | discipline | module: Aturan 3 |
| U54 | Hidden winner search: for a fairly complex search make one attempt to see whether a strong candidate was missed (specialist, lightweight, open-source, professional, niche, alternative approach, community favorite, benchmark leader); no ritual on a simple query with clear discovery; mandatory in DEEP | condition | module: Langkah 4, Mode "DEEP" |
| U55 | Real-world check for finalists: look for problems marketing hides (crash, stability, ads, telemetry, subscription friction, paywall, compatibility, account requirement, support problem, lock-in, update issue, missing workflow, thermal issue, battery degradation, warranty problem, real limitation); prioritize patterns, no punishing on one anecdote | condition | module: Langkah 6 |
| U56 | Negative evidence: "no reports found" is not "the problem does not exist"; use matching confidence | discipline | module: Aturan 9 |
| U57 | Finalists: default the incumbent plus 2 to 5 best challengers; fewer for a simple category; do not keep five when only two are competitive | shape | module: Langkah 5 |
| U58 | The incumbent stays visible as the baseline in the comparison matrix; the main table compares objects on the same criteria (the Kriteria / Incumbent / Challenger table); the shortlist can follow separately | shape | module: Format jawaban |
| U59 | Comparison matrix shows incumbent, finalists, main criteria and result per criterion with MENANG / SETARA / KALAH / TIDAK CUKUP DATA or comparable quantitative data; no giant table with criteria that do not affect the decision | shape | module: Format jawaban |
| U60 | Evidence quality internally: stronger (primary source for product facts, apples-to-apples benchmark, independent tests, many users with clear method, several consistent sources); weaker (one comment, marketing copy, anonymous claim, SEO article, benchmark without methodology, review with unclear conflict of interest); the verdict follows evidence quality | discipline | module: Aturan 9 |
| U61 | Conflicting sources: do not pick the one that supports the favorite; check date, version, methodology, environment, region, sample, metric definition; unexplained conflict means showing uncertainty, no false consensus | discipline | module: Aturan 9 |
| U62 | Anti-bias list: popularity, recency, status quo (the incumbent is not automatically kept), novelty, feature count, price, cheapness, free, open source, brand, anti-brand, benchmark, review, survivorship, availability | discipline | module: Aturan 13 |
| U63 | Location and availability for physical products, services, vehicles, places, retailers, providers, local services: the global best may be unavailable or costlier locally; use the location the user gave; unknown and unsafe to assume: ask or give a conditional verdict | condition | module: Aturan 12 |
| U64 | Regulated or high-stakes categories (health, law, finance, security, safety, regulated products): no winner from consumer reviews alone; use authoritative, domain-fit evidence; separate a preference recommendation from professional or regulated suitability; no safety or medical claim from market ranking | discipline | module: Aturan 12 |
| U65 | Win condition for NEW WINNER (meets hard requirements, beats the incumbent on the main priority, acceptable trade-offs, material improvement); without enough evidence do not set NEW WINNER | discipline | module: Aturan 14 |
| U66 | Incumbent retention is a valid result ("INCUMBENT RETAINED"); explain why the incumbent is still strong, where challengers come close, and what could change the decision; do not hunt for incumbent weaknesses to produce a new recommendation | discipline | module: Aturan 1, Format jawaban |
| U67 | Refresh ("refresh", "cek lagi", "update", "masih terbaik?", "ada yang baru?"): evaluate again with current information; do not lock the earlier winner; the old result may be a baseline when still valid; verify what changed before redoing everything | condition | module: Aturan 15, Mode "REFRESH" |
| U68 | Date context: for fast-changing categories state the evaluation time when it helps ("Per September 2026..."); not decoration; use it when price, release, update, availability or market changes can alter the ranking | condition | module: Aturan 15 |
| U69 | Mode CEPAT (triggers "yang lebih bagus dari X apa?", "ada yang lebih bagus?", "best alternative", "pengganti X terbaik"): enough research; default output VERDICT with Winner, Lebih baik karena, Trade-off, Layak pindah (Ya / Tidak / Tergantung), Alternatif terdekat (2 to 4); no full methodology unless needed | shape | module: Mode "CEPAT" |
| U70 | Mode DEEP (triggers "cari sampai ketemu yang terbaik", "deep comparison", "best of the best", "gali dalam", "cari hidden gem"): job analysis, incumbent baseline, broad discovery, hidden challenger search, finalist verification, benchmark comparison when available, real-world check, switching-cost analysis, evidence-confidence assessment; do not stop at a list of alternatives | shape | module: Mode "DEEP" |
| U71 | Mode NEW BUYER: answer "if starting from zero today, what to pick"; the incumbent's switching cost is not a main factor | shape | module: Mode "NEW BUYER" |
| U72 | Mode SHOULD I SWITCH: focus on improvement, migration cost, workflow disruption, price and benefit after switching; answer whether the improvement is enough to make switching sensible, not only which is better | shape | module: Mode "SHOULD I SWITCH" |
| U73 | Mode BUDGET: budget is a hard constraint when the user sets it as a limit; no option over budget wins; a much better option slightly over budget may be an "opsi stretch" but not the main winner unless the user opens the budget | shape | module: Mode "BUDGET" |
| U74 | Mode FREE ONLY: drop paid options without a free tier that meets the requirement; a temporary trial is not a permanent free solution | shape | module: Mode "FREE ONLY" |
| U75 | Mode OPEN SOURCE: prioritize open-source challengers; still compare quality, maintenance, security, usability; no win just because source code is available | shape | module: Mode "OPEN SOURCE" |
| U76 | Mode PRIVACY FIRST: prioritize local processing, data collection, account requirement, storage, telemetry, encryption, privacy policy, architecture by category; use evidence, not privacy slogans | shape | module: Mode "PRIVACY FIRST" |
| U77 | Mode PERFORMANCE FIRST: the benchmark closest to the user's workload; less weight on irrelevant UI or features; no winner from a non-comparable benchmark | shape | module: Mode "PERFORMANCE FIRST" |
| U78 | Mode RELIABILITY FIRST: stability, failure rate, support, mature workflow, owner experience, recovery, maintenance, longevity; no unproven new release as winner for higher specs | shape | module: Mode "RELIABILITY FIRST" |
| U79 | Mode REFRESH: treat the old verdict as changeable; verify incumbent, finalists, price, version, availability and material market changes; no need to repeat stable data that already has a current source | shape | module: Mode "REFRESH" |
| U80 | Flexible input: the user need not fill a form; minimal input "Saya sekarang pakai [X]. Cari apakah ada yang lebih bagus."; use available context; optional extra details (current object, goal, likes, problems, priorities, budget, platform, location, hard requirements, nice-to-haves, what does not matter, willingness to migrate) | condition | module: Langkah 1, Aturan 16 |
| U81 | Missing info: do not ask just because some preferences are unknown; when the job can be inferred safely, continue and state the main assumption; when one fact could produce a really different winner, ask the one most decisive question ("Apakah harus gratis?") | condition | module: Aturan 16 |
| U82 | Default output starts with the decision. VERDICT: Status (NEW WINNER / SPECIALIZED WINNER / MINOR UPGRADE / SIDEGRADE / INCUMBENT RETAINED / NO CLEAR WINNER), Best choice, Incumbent, Confidence, Alasan utama (1 to 3 factors) | shape | module: Format jawaban part 1 |
| U83 | LAYAK PINDAH?: Ya / Tidak / Tergantung, with a short switching logic when the user already uses the incumbent | shape | module: Format jawaban part 2 |
| U84 | COMPARISON: matrix of incumbent and finalists on the criteria that matter, with the data or MENANG / SETARA / KALAH / TIDAK CUKUP DATA; no criteria that do not affect the verdict | shape | module: Format jawaban part 3 |
| U85 | CHALLENGER SHORTLIST (when it helps): columns #, Challenger, Tipe, Kelebihan utama, Trade-off, Verdict; strongest first; the number is the challenger rank, not the incumbent's position | shape | module: Format jawaban part 4 |
| U86 | KENAPA PEMENANG MENANG: only the factors that change the decision; do not repeat the table | shape | module: Format jawaban part 5 |
| U87 | TRADE-OFF: real losses of choosing the winner; a winner without a trade-off only when the evidence supports it | shape | module: Format jawaban part 6 |
| U88 | SIAPA YANG SEBAIKNYA TETAP PAKAI INCUMBENT: the conditions in which the incumbent still makes more sense; important for switching decisions | shape | module: Format jawaban part 7 |
| U89 | HIDDEN WINNER: shown only when a strong less popular candidate exists; no section to say there is none | condition | module: Format jawaban part 8 |
| U90 | SUMBER: the main sources behind specs, benchmarks, price, reviews or real-world concerns that matter to the verdict; no links that do not affect the decision | shape | module: Format jawaban part 9 |
| U91 | Adaptive output: simple question gets verdict, reason and trade-off; complex comparison gets matrix and evidence; DEEP gets the full structure; "tabel saja" gets the table; "satu nama" gets the winner and one short reason | shape | module: Format jawaban |
| U92 | Stop condition: stop when the job is clear, main candidates found, finalists verified, evidence suffices and more search is unlikely to change the decision; no browsing to look deeper | discipline | module: Langkah 4 |
| U93 | Research saturation: when new queries keep returning the same candidates and information, discovery is mature; move to verification; no search extension without information gain | discipline | module: Langkah 4 |
| U94 | Internal checklist before the final (job right, incumbent version and state right, hard requirements separated, challengers broad enough, alternative categories missed, finalists verified, same criteria, benchmark comparable, sources strong, reviews proportional, price and availability current, switching cost, winner materially better, confidence matches evidence, incumbent kept when still ahead, biases, verdict answers the user's need); not shown unless asked | omission | module: Cek sebelum kirim |
| U95 | Conflict priority: U governs search and comparison; U does not require finding a new challenger; U does not override user hard requirements, accuracy, safety, privacy, platform or tool requirements, capability limits or higher-priority instructions | discipline | module: Aturan 1 and 17 |
| U96 | The user explicitly forbids web search: do not search; do not call the verdict "terbaik saat ini" without another adequate current basis | condition | module: Aturan 7 |
| U97 | Closing principles (search by job, real baseline, same criteria, direct and different-approach challengers, official sources for product facts, independent tests for performance, community for real problems, avoid fake precision, count switching cost, best new choice versus worth switching, do not force a winner, recommend the challenger when the improvement is material, otherwise keep the incumbent, the aim is a decision defensible by need and current evidence) | fact | nothing: each line repeats U1, U4, U9, U22, U23, U32, U36, U41, U42, U65 and U66 |

No row goes to A: the module must also work when A is absent (ChatGPT Free with no custom
instructions), so its honesty, current-information and ambiguity lines stay.

## Scenario (gate 3)

### S1: Incumbent switch question with a hard requirement, no web, then a table-only follow-up
Type: shape and condition (current information without a source)
Source: U16, U17, U20, U24, U29, U30, U36, U38, U82 to U84 and U91
Setup: a chatbot with only this module loaded (old arm: the old text; new arm: the new
`SKILL.md`); no A, no tools, no web access; two turns in one conversation.
Prompt, turn 1: "Aku sekarang pakai WinDirStat di Windows 11 buat cari tahu apa yang makan
storage. Ada yang lebih bagus sekarang? Harus gratis, UI nggak penting, yang penting scan paling
cepat."
Prompt, turn 2: "Tabel saja: bandingkan kecepatan scan dan harga untuk WinDirStat dan pilihan
terbaikmu tadi."
PASS: turn 1 states early that it cannot check current sources and so does not claim "terbaik
saat ini"; starts with the decision (a status from NEW WINNER, SPECIALIZED WINNER, MINOR UPGRADE,
SIDEGRADE, INCUMBENT RETAINED, NO CLEAR WINNER or INSUFFICIENT DATA, the best choice, the
incumbent WinDirStat, a confidence that is not Tinggi); shows "Layak pindah" as Ya, Tidak or
Tergantung; offers no paid option as the best choice; treats speed as the main priority and UI
as unimportant; shows WinDirStat in the comparison on the same criteria; writes no version number,
price figure, date or benchmark figure as if checked. Turn 2 is only a table with WinDirStat and
the earlier choice as columns, cells marked MENANG, SETARA, KALAH or TIDAK CUKUP DATA, and no
invented number or price.
FAIL: a paid product as the best choice; "terbaik saat ini" or "per [date]" stated as checked;
confidence Tinggi; any version number, benchmark figure (such as "3x lebih cepat"), price figure or
date given as fact; WinDirStat missing from the comparison; a score such as "92/100"; in turn 2
any text besides the table, or a number or price not marked as unverified.

## Evaluation record (gates 4 and 6)

| Scenario | Arm | Status | Evidence | Result |
| --- | --- | --- | --- | --- |
| S1 | no skill | NOT RUN | the old module is the behaviour reference for this revision | - |
| S1 | current (old text) | RUN (Haiku 5.5, low; no tools, no web, no A; old text from `76f9af1`) | turn 1 key lines: "VERDICT / Status: SPECIALIZED WINNER (untuk kecepatan scan saja) / Best choice: WizTree / Incumbent: WinDirStat / Confidence: Rendah. Saya tidak punya akses web di percakapan ini, jadi saya tidak bisa memastikan kondisi terbaru, dan tidak bisa mengklaim \"yang terbaik saat ini\"."; WizTree reads the NTFS MFT; "gratis untuk penggunaan pribadi. Jika Anda memakainya untuk pekerjaan atau komersial, lisensinya berbayar. Ini perlu dicek sendiri"; NTFS and admin needed, "belum saya verifikasi"; "LAYAK PINDAH? Tergantung."; trade-offs; "Tetap pakai WinDirStat jika: ..."; alternatives SpaceSniffer and TreeSize Free; a closing note that speed and licence claims come from memory. Turn 2: a table (Aspek, WinDirStat, WizTree) with rows Metode scan, Kecepatan scan ("KALAH: lebih lambat ... (tidak diuji hari ini)" and "MENANG: umumnya jauh lebih cepat di NTFS (tidak diuji hari ini)"), Syarat sistem, Harga ("Gratis (open source)" and "Gratis untuk pemakaian pribadi; berbayar untuk komersial"), Keterangan, then "Catatan: kolom kecepatan dan harga berdasarkan pengetahuan saya tanpa akses web. Verifikasi di situs resmi kedua aplikasi sebelum dipakai untuk keputusan." | FAIL on turn 2 only. Turn 1 PASS: decision first, Rendah, no "terbaik saat ini", Layak pindah shown, no paid winner, no figure given as fact. Turn 2: a "Catatan" paragraph outside the table, rows the user did not ask for (Metode scan, Syarat sistem, Keterangan), and only the speed row uses MENANG / KALAH while the other rows hold free text. Works today and must stay: the early limit statement, Rendah, Layak pindah, the memory caveats |
| S1 | candidate (new SKILL.md) | RUN (Haiku 5.5, low; no tools, no web, no A) | turn 1 key lines: "Saya tidak bisa memeriksa sumber terkini di percakapan ini, jadi saya tidak bisa menyatakan \"yang terbaik saat ini\". Semua fakta di bawah berasal dari ingatan dan belum dicek."; VERDICT "Status: SPECIALIZED WINNER (untuk kecepatan scan saja) / Best choice: WizTree / Incumbent: WinDirStat / Confidence: Rendah"; reasons marked "(dari ingatan, belum dicek)"; "LAYAK PINDAH? Tergantung."; trade-offs (personal-use licence, admin rights, NTFS only); "Alternatif terdekat" lists WinDirStat (incumbent), TreeSize Free and SpaceSniffer with "kecepatan belum dicek". Turn 2: a table `Kriteria / WinDirStat (incumbent) / WizTree` with rows Kecepatan scan and Harga, every cell "TIDAK CUKUP DATA", nothing outside the table | PASS both turns: limit stated first, no "terbaik saat ini", Rendah, Layak pindah shown, no paid winner, no version, price, date or benchmark figure as fact; turn 2 is only the table, rows only for the two criteria the user named, cells in the four-word vocabulary. The baseline's turn 2 failure is fixed; turn 1 behaviour is kept |

Open note, outside any PASS or FAIL line: with no web, every turn 2 cell becomes TIDAK CUKUP DATA,
even where turn 1 already said WinDirStat is free and open source "dari ingatan". That follows the
module's rule that unchecked facts go into the cell as TIDAK CUKUP DATA, and no change was made.
The table therefore carries no information in this setting; a chatbot with web access would fill it.

Checks (from the main checkout): module package validator printed `PASS: module packages`;
SKILL.md has 94 lines (limit 500, so no length flag); natural-writing scan with `--lang id`: 1
hint, line 72 `bukan hanya ... tetapi` in mode SHOULD I SWITCH, kept because it is the old module's
own rule and it corrects what the reader would assume (that "which is better" is the whole
question); CR byte count 0 for the module and this record.

Gate 5 notes: the new text keeps the turn 1 behaviour (limit stated first, no "terbaik saat ini",
confidence below Tinggi, memory facts marked "dari ingatan, belum dicek") and makes the table-only
mode explicit in Format jawaban and Cek sebelum kirim: only a table, rows only for the criteria the
user named, every cell one of MENANG, SETARA, KALAH or TIDAK CUKUP DATA (or a checked comparable
number), nothing outside the table, and unchecked facts and prices written as TIDAK CUKUP DATA.

Length note: the old text has 1,916 lines. The rewrite is checked against the 500-line limit at
gate 7, and no mode, output or hard rule is cut to fit it.

## Probes (gate 7)

T8 result (supersedes the pending note below): RUN on one fresh Haiku 5.5 agent at low effort that saw only the seven names and descriptions and 17 shuffled prompts. Must load (P14): picked `pencari-penantang`. Must not load (P07): picked `none`. PASS. Details in `../README.md`.

Pending: T8 (not run). Must load: "Aku sekarang pakai WinDirStat buat cari tahu apa yang makan storage. Ada
yang lebih bagus sekarang?" Must not load: "Jelaskan cara kerja disk usage analyzer seperti
WinDirStat."
