# G. Penghitung Kalori dan Komposisi Tubuh (`kalori-komposisi-tubuh`)

Mode: revision. Old text: WebBased `76f9af1`, module "G. PENGHITUNG KALORI DAN KOMPOSISI TUBUH
BERBASIS BUKTI" (965 lines). New text: `skills/kalori-komposisi-tubuh/SKILL.md` on branch
`claude/webbased-daily-rules`.

## Brief (gate 1)

- Consumer: a web chatbot that loads the module as an uploaded skill (Claude.ai, Gemini) or reads
  it pasted into the chat (ChatGPT Free). It may or may not have web search.
- Task: count daily food intake (calories, macros, sugar, sodium) from labels, sources or photos,
  and estimate body composition and energy needs from measurements, always as estimates with their
  uncertainty.
- Must load: "Aku barusan makan 2 bungkus mie instan, hitung kalorinya ya." and "Hitung BMI dan
  estimasi body fat-ku dari lingkar perut dan leher."
- Must not load: "Buatkan menu makan sehat untuk seminggu." (menu planning, no counting or
  estimate of a given meal or body measurement).
- Output: per meal a table (name and source, working weight with range, working calories with
  range, carbs, protein, fat, sugar, sodium, confidence), then "Estimasi makan ini" and "Rentang
  makan ini", then a daily summary; for body data, labelled results kept apart as measured,
  calculated, model estimate and interpretation.
- Authority limits: invents no nutrition value; never calls BMI, body fat, REE or TDEE a diagnosis
  or a laboratory value; never silently corrects a measurement; no medical decision, and a user
  with a medical condition is sent to a health professional; no false precision.

## Routing table (gate 2)

Kinds: shape, omission, condition, discipline, fact. Destinations: module (the section in the new
text; exact line numbers are fixed in gate 5), A (already covered by A. PRIORITAS), nothing (with
a reason). Formulas, constants and units are protected: copied exactly.

| ID | Old text (short) | Kind | Destination |
| --- | --- | --- | --- |
| G1 | Role: daily nutrition counter and body-composition estimate analyst | shape | module: purpose paragraph |
| G2 | Priority: evidence accuracy > method consistency > uncertainty transparency > speed | discipline | module: Aturan 1 |
| G3 | Food data: web search or official label/source given by the user | condition | module: Langkah 3 (no web: use the user's label, else say the value is unverified) |
| G4 | Do not invent nutrition values | discipline | module: Aturan |
| G5 | Do not use model memory as the main source for specific nutrition numbers when a verifiable source exists | discipline | module: Aturan |
| G6 | No precision higher than the data quality | discipline | module: Aturan |
| G7 | "Aktif bila dikirim bersama A" | condition | module: purpose paragraph (works alone; follow A when present) |
| G8 | BMI, circumference, body-fat equations, RMR/REE, TDEE, food photos, weight trend are estimates or screening | discipline | module: Aturan |
| G9 | Never call them a diagnosis, a lab measurement or a certain body value | discipline | module: Aturan |
| G10 | Separate measured data, direct calculation, model estimate, interpretation | shape | module: Format jawaban (body part) |
| G11 | Medical condition, medical diet, weight/metabolism medication or a medical decision: do not rely on a generic tracking model instead of a health professional | condition | module: Aturan |
| G12 | Use the raw data as given; do not change a number because it looks unusual | discipline | module: Aturan, Langkah 1 |
| G13 | Possible mismeasurement: flag as needs verification, never silently correct | discipline | module: Aturan, Langkah 1 |
| G14 | Do not lock body fat, fat mass, lean body mass before computing with a suitable method | discipline | module: Aturan |
| G15 | Profile: age 21, biological sex male, height 170 cm | fact | dropped with owner approval: replaced by the fill-in template (Data pengguna) |
| G16 | Progress reference: BEFORE DIET vs AFTER DIET after 2.5 weeks of calorie deficit; do not swap for one old number from another chat | discipline | module: Aturan 10 (the rule); the owner's two data sets are dropped with owner approval: replaced by the fill-in template (Data pengguna) |
| G17 | BEFORE DIET data set (weight 78-80 kg, neck 40, below Adam's apple 41, navel waist 92, belt waist 87, upper waist 90, chest 99, thighs 56 possibly mismeasured, calves 41/40, biceps 33/33, forearms 29/28, hip unknown) | fact | dropped with owner approval: replaced by the fill-in template (Data pengguna) |
| G18 | AFTER DIET data set (78.3 kg, below Adam's apple 39.5, navel waist 85.5, belt 87, upper 86, chest 100, thighs 62/62, calves 39.5/39.5, biceps 35/34, forearms 29/28, hip 99) | fact | dropped with owner approval: replaced by the fill-in template (Data pengguna) |
| G19 | Compare same measurement site; same measurement conditions as far as possible | discipline | module: Aturan |
| G20 | Never compare navel circumference with belt circumference as if the same point | discipline | module: Aturan |
| G21 | No big conclusion from a small change that may be measurement error | discipline | module: Aturan |
| G22 | Flag a suspicious jump with no supporting change | discipline | module: Aturan |
| G23 | Old data possibly mismeasured: keep as history with a lower quality note, do not delete | discipline | module: Aturan |
| G24 | Weekly schedule: Mon Push, Tue Lower A, Wed Pull, Thu rest, Fri Upper, Sat Lower B, Sun rest; equipment 20 kg dumbbell, permanent pull-up bar, strong grey band | fact | dropped with owner approval: replaced by the fill-in template (Data pengguna) |
| G25 | Resistance days: 5 per week; never say 6 unless the schedule changes | discipline | module: Data pengguna (last line: day count follows the filled schedule; the owner's value 5 is dropped with owner approval: replaced by the fill-in template (Data pengguna)) |
| G26 | The five training-day exercise lists with sets, reps, RIR and rest (Push 6 lines, Lower A 5, Pull 5, Upper 7, Lower B 6) | fact | dropped with owner approval: replaced by the fill-in template (Data pengguna) |
| G27 | Current activity: mostly sitting, programmer | fact | dropped with owner approval: replaced by the fill-in template (Data pengguna) |
| G28 | Do not set activity level from the number of sessions alone | discipline | module: Aturan |
| G29 | Consider: desk work, training days, duration, intensity, weekly volume, RIR, daily steps if available, non-training activity, week-to-week change | omission | module: Langkah 4 |
| G30 | Do not treat the activity multiplier as a known fact | discipline | module: Aturan |
| G31 | First task step 1: validate input (missing data, different circumference sites, possible mismeasurement, contradictions); never silently fix | omission | module: Langkah 1 |
| G32 | Step 2: BMI for 78, 79, 80 kg at 170 cm, `BMI = berat kg / tinggi meter²`, shown as a calculation | shape | module: Langkah 2 |
| G33 | Explain BMI is a weight-and-height screening indicator, not an individual body-fat measurement | omission | module: Langkah 2 |
| G34 | Step 3: `WHtR = lingkar pinggang / tinggi` | shape | module: Langkah 2 |
| G35 | Waist 94 cm on request: an extra measurement; do not mix with the 92 cm or 85.5 cm baselines; label that 94 cm is not a BEFORE/AFTER baseline | discipline | module: Langkah 2 |
| G36 | Step 4: body fat only with an anthropometric method that is science-based, sex-appropriate, age/population-appropriate as far as possible, with the inputs available | discipline | module: Langkah 3 |
| G37 | Men: abdomen-neck-height circumference method allowed if the procedure matches | condition | module: Langkah 3 |
| G38 | With that method: abdomen and neck at the sites the method requires, height available, units converted correctly, formula and method source named | omission | module: Langkah 3 |
| G39 | Never use a circumference from a different site just because the number exists | discipline | module: Aturan |
| G40 | Step 5: if a required input is truly missing, ask all at once in one short question | condition | module: Langkah 3 |
| G41 | Never guess age, biological sex, height, circumference site or an unprovided body measurement | discipline | module: Aturan |
| G42 | Data present but measurement quality doubtful: may compute, with a lower confidence label | condition | module: Langkah 3 |
| G43 | Step 6: body fat always called an ESTIMATE ("Estimasi body fat berdasarkan metode circumference", never "Body fat Anda adalah X%") | shape | module: Langkah 3, Aturan |
| G44 | No false precision to decimals the method does not support; round sensibly; show a range when uncertainty is material | discipline | module: Aturan |
| G45 | Step 7: with more than one valid method and matching inputs, compute as comparison; never auto-average; explain why they differ | condition | module: Langkah 3 |
| G46 | Never pick a method because it gives a wanted number | discipline | module: Aturan |
| G47 | Step 8: `Fat mass = berat × estimasi body-fat`; `Fat-free mass = berat − fat mass` | shape | module: Langkah 4 |
| G48 | Use "fat-free mass" or FFM; never call FFM muscle mass | discipline | module: Aturan |
| G49 | Show a range when body fat is a range | condition | module: Langkah 4 |
| G50 | Step 9: Mifflin-St Jeor as the main REE/RMR estimate when inputs exist | shape | module: Langkah 5 |
| G51 | Never call the result a true laboratory BMR; use "estimasi REE/RMR" or "estimasi kebutuhan energi saat istirahat" | discipline | module: Aturan |
| G52 | Step 10: an FFM-based formula only as a cross-check, with a clear scientific source | condition | module: Langkah 5 |
| G53 | Never make an FFM formula the main estimate when the FFM itself comes from an uncertain circumference body fat | discipline | module: Aturan |
| G54 | Never treat two similar formulas as two independent measurements | discipline | module: Aturan |
| G55 | Step 11: TDEE as a range; initial TDEE is a model, not a fact; scenarios from work, training, steps, daily activity, weight change | shape | module: Langkah 5 |
| G56 | May show three scenarios (lower, working, higher); one working estimate only for practical tracking; always show it still needs calibration | shape | module: Langkah 5, Format jawaban |
| G57 | Step 12: no activity multiplier from the labels sedentary / lightly active / moderately active / very active alone | discipline | module: Aturan |
| G58 | Step 13: calibrate TDEE after about 14 days of consistent data: average intake, weight trend, activity change, logging error | condition | module: Langkah 6 |
| G59 | Never change TDEE from one or two daily weight changes; use the trend | discipline | module: Aturan |
| G60 | More than 14 days available: prefer a period long enough to reduce noise yet still representing current activity and diet | condition | module: Langkah 6 |
| G61 | Step 14: fat-loss target computed from total energy needs, never from REE/RMR plus an arbitrary number | discipline | module: Aturan |
| G62 | Rate not set by the user: start with a moderate deficit; assess against TDEE, goal, weight trend, training performance, user tolerance | condition | module: Langkah 6 |
| G63 | About 500 kcal per day as a starting heuristic when sensible, not a universal rule | condition | module: Langkah 6 |
| G64 | NIH Body Weight Planner as a cross-check when usable (dynamic weight change) | condition | module: Langkah 6 |
| G65 | Step 15: 3.500 kcal per pound is only a rough approach in a clear context, not a precise long-term prediction; intake and weight change are not fully linear | discipline | module: Aturan |
| G66 | Step 16: never use or discuss Endomorph, Mesomorph, Ectomorph or another somatotype unless the user asks for the term; never use it to set calories or diet | discipline | module: Aturan |
| G67 | Daily tracking: time zone Asia/Jakarta; user's local date | fact | module: Aturan |
| G68 | A different date or the user writing "hari baru" starts a new daily log | condition | module: Mode |
| G69 | Do not delete earlier logs still needed for trend analysis | discipline | module: Aturan |
| G70 | Tracking lasts while the needed conversation context is available; never claim logs persist across sessions or chats | discipline | module: Aturan |
| G71 | Context history missing: use a recap or data the user gives | condition | module: Aturan |
| G72 | Stage 1: identify every component actually seen, mentioned, or reasonably inferred from a clear menu | omission | module: Langkah 3 |
| G73 | Split complex food into components when it improves accuracy (nasi, ayam, tepung, minyak, sambal, saus, bumbu kacang, kecap, telur, tahu, tempe, kerupuk, cakwe, kedelai, sayur, topping, minuman, gula, susu) | condition | module: Langkah 3 |
| G74 | Do not split falsely when the recipe cannot be known from a photo; mark uncertain composition | discipline | module: Aturan |
| G75 | Do not use one "1 porsi lengkap" entry when the real portion clearly differs from the database serving | discipline | module: Aturan |
| G76 | Stage 2 portion priority: scale weight, label weight, official serving, package size or unit count, visual estimate with a reference object | shape | module: Langkah 4 |
| G77 | Unknown weight: estimate from plate, bowl, container, spoon, package, pieces, skewers, a well-known reference object | condition | module: Langkah 4 |
| G78 | Visual estimate shows working weight and a plausible range (nasi ±190 g, range 160-220 g) | shape | module: Langkah 4, Format jawaban |
| G79 | A photo never gives certain grams; fewer scale objects or more hidden food widens the range | discipline | module: Aturan |
| G80 | Photo too ambiguous to tell food types: ask only if the difference is material to the result | condition | module: Langkah 4 |
| G81 | Food type clear but portion uncertain: best estimate with a range, never block tracking | condition | module: Langkah 4 |
| G82 | Distinguish raw, cooked, dry, boiled, edible portion when relevant | omission | module: Langkah 4 |
| G83 | Exclude bone, skewer, shell, uneaten skin, packaging and other non-edible parts from eaten weight | discipline | module: Aturan |
| G84 | Dry food that absorbs water: use the nutrition basis that matches the source (85 g dry noodles is not 85 g boiled noodles) | discipline | module: Aturan |
| G85 | Stage 3 source priority: 1 official label of the same product; 2 official maker or restaurant site for the same product or menu; 3 Tabel Komposisi Pangan Indonesia, Kementerian Kesehatan RI; 4 USDA FoodData Central; 5 government, university, peer-reviewed or credible health-institution database; 6 secondary or crowdsourced (FatSecret, MyFitnessPal, recipe sites, community databases) only when nothing stronger | shape | module: Langkah 3 |
| G86 | Never pick a source just because it ranks first in search results | discipline | module: Aturan |
| G87 | Branded product: match brand, variant, country, serving size, net weight, product version | omission | module: Langkah 3 |
| G88 | User's label differs from a web database: the label of the food actually eaten wins | condition | module: Langkah 3 |
| G89 | Restaurant: official nutrition data when published; otherwise never take another restaurant's number and call it this menu | condition | module: Langkah 3 |
| G90 | Restaurant without data: component-based estimate, explained as not the restaurant's official figure | condition | module: Langkah 3 |
| G91 | Stage 4 high-uncertainty foods (ayam geprek, ayam crispy, gorengan, tempe goreng, tahu goreng, dadar jagung, peyek, kerupuk, cakwe, sambal berminyak, bumbu kacang, mayones, saus keju, santan, minyak, gula, kecap): extra attention | condition | module: Langkah 3 |
| G92 | Do not count fried food as raw or cooked without oil when frying clearly adds energy | discipline | module: Aturan |
| G93 | Oil amount unknown: put the oil uncertainty into the range; never invent an absorbed amount as a fixed number | discipline | module: Aturan |
| G94 | Stage 5: `nilai nutrisi sumber × jumlah yang benar-benar diperkirakan dimakan = nutrisi porsi aktual` per component | shape | module: Langkah 4 |
| G95 | Compute when data exists: calories, carbohydrate, protein, fat, sugar, sodium | omission | module: Langkah 4 |
| G96 | Never copy one serving's values when the eaten amount differs; scale explicitly for 2 packs, 2 servings, 8 eggs, 6 skewers | discipline | module: Langkah 4 |
| G97 | Use mathematical calculation, not mental estimation, when the numbers are complex | discipline | module: Aturan |
| G98 | Sanity check calories against macros: `protein × 4 + karbohidrat × 4 + lemak × 9` | shape | module: Langkah 4 |
| G99 | A label is not wrong only because that sum differs from the label calories (rounding, fibre, sugar alcohol, method, other components) | discipline | module: Aturan |
| G100 | Gap too large to explain: check a second source or the original label | condition | module: Langkah 4 |
| G101 | Do not mix calories from one source with macros from another without a clear reason; if forced, say which part comes from which source | discipline | module: Aturan |
| G102 | Sugar or sodium missing: write "data tidak tersedia"; never invent a number to complete a table | discipline | module: Aturan, Format jawaban |
| G103 | Stage 6: food without exact weight gets "Estimasi kerja" (best number for the daily log) and "Rentang ketidakpastian", never one number as a measurement | shape | module: Format jawaban |
| G104 | Range bounds from portion, oil, sauce, recipe, cooking method, source quality; example 650 kcal, range 570-760 kcal | shape | module: Format jawaban |
| G105 | The less certain the recipe or portion, the wider the range; never a narrow range to look accurate | discipline | module: Aturan |
| G106 | Confidence TINGGI: actual weight known and official label available | shape | module: Format jawaban |
| G107 | Confidence SEDANG: clear food type and strong source, estimated weight | shape | module: Format jawaban |
| G108 | Confidence RENDAH: recipe, oil, sauce or portion very uncertain | shape | module: Format jawaban |
| G109 | Confidence follows the whole process, not only source quality | discipline | module: Aturan |
| G110 | Same item in the same context keeps a consistent nutrition basis | discipline | module: Aturan |
| G111 | User writes "update sumber": search the data again | condition | module: Mode |
| G112 | Actual weight given after an estimate: recompute and replace the old estimate | condition | module: Mode, Aturan |
| G113 | User says a component was not eaten: remove it | condition | module: Mode, Aturan |
| G114 | Recipe, variant, size or product changed: not identical to the earlier entry | discipline | module: Aturan |
| G115 | "hitung ulang", "revisi", "cek lagi": never only change the final total | discipline | module: Mode |
| G116 | Recalculation steps: re-identify the food; check weight or serving; check source; recompute every component; replace the old total; explain the most material change | omission | module: Mode |
| G117 | Do not keep an old number for consistency when new evidence is stronger | discipline | module: Mode, Aturan |
| G118 | Per-meal output default table: Nama + sumber, Berat kerja + rentang, Kalori kerja + rentang, Karbo, Protein, Lemak, Gula, Natrium, Keyakinan | shape | module: Format jawaban part 1 |
| G119 | Table too wide for the context: split into an easier format without dropping important information | condition | module: Format jawaban |
| G120 | After the table: "Estimasi makan ini" and "Rentang makan ini" | shape | module: Format jawaban part 2 |
| G121 | Daily summary: Target kalori, Total intake kerja, Rentang atau ketidakpastian total, Sisa terhadap target, TDEE kerja, Selisih terhadap TDEE, Total karbohidrat, Total protein, Total lemak, Total gula, Total natrium | shape | module: Format jawaban part 3 |
| G122 | Do not show total sugar or sodium as certain when most items lack the data | discipline | module: Aturan, Format jawaban |
| G123 | Daily data incomplete: mark the total as partial | condition | module: Format jawaban |
| G124 | Separate diet target from maintenance estimate or TDEE | discipline | module: Aturan |
| G125 | Intake above target but below estimated TDEE: "melewati target diet, tetapi masih berada dalam estimasi defisit energi." | condition | module: Format jawaban (exact phrase) |
| G126 | Intake above estimated TDEE: "estimasi surplus energi." | condition | module: Format jawaban (exact phrase) |
| G127 | Intake range crosses TDEE: "status surplus atau defisit belum pasti berdasarkan ketidakpastian intake dan TDEE." | condition | module: Format jawaban (exact phrase) |
| G128 | Intake range crosses the target: explain that reaching the target depends on actual intake | condition | module: Format jawaban |
| G129 | No surplus or deficit claim from one midpoint when uncertainty can change the conclusion | discipline | module: Aturan |
| G130 | TDEE is also an estimate; a 30-50 kcal difference from TDEE is not a certain biological status | discipline | module: Aturan |
| G131 | Daily recap: working estimate sum is the main log | shape | module: Format jawaban |
| G132 | Never call the sum of all maxima the "most likely realistic scenario"; with only lower and upper bounds per item, their sum is a conservative envelope, not a probability | discipline | module: Aturan |
| G133 | Prioritize total working estimate plus the largest sources of uncertainty | shape | module: Format jawaban |
| G134 | A daily range needs no complex statistics without data; say whether it is conservative, a practical estimate, or from actual data | condition | module: Format jawaban |
| G135 | Long-term: photo calories are estimates; improve calibration with a consistent morning weight when available | omission | module: Langkah 6 |
| G136 | Look at the trend, not one day; compare weight trend with average intake; consider activity change; evaluate systematic portion-logging error | omission | module: Langkah 6 |
| G137 | Do not change the target from one high or low intake day | discipline | module: Aturan |
| G138 | Do not change TDEE from one daily weight change | discipline | module: Aturan |
| G139 | Actual trend keeps differing from prediction over a long enough period: update the working estimate with the latest evidence; never force actual data to fit the initial formula | condition | module: Langkah 6 |
| G140 | Weight trend: prefer a multi-day average or trend over two single numbers | discipline | module: Aturan |
| G141 | Daily weight shifts from fluid, glycogen, gut contents, sodium and other short-term factors; never call all short-term change fat change | discipline | module: Aturan |
| G142 | Body composition trend: use weight, consistent-site waist, other circumferences, training performance and body-fat estimate together | omission | module: Langkah 6 |
| G143 | Never claim muscle change only from arm or thigh circumference change | discipline | module: Aturan |
| G144 | Never claim a fat change of a given size only from waist change | discipline | module: Aturan |
| G145 | Final principle: "sekitar 680 kcal, kemungkinan berada di kisaran 600-770 kcal" beats "682 kcal" when the portion is only estimated from a photo | shape | module: Format jawaban |
| G146 | "estimasi body fat sekitar X dengan ketidakpastian beberapa poin persentase" beats a one-decimal number as if from DXA | shape | module: Format jawaban |
| G147 | Change the estimate when new evidence is stronger rather than keep an old number to look consistent | discipline | module: Aturan |
| G148 | Do not undercount to make intake fit the target; do not overcount just to be safe; find the most reasonable middle estimate | discipline | module: Aturan |
| G149 | Show uncertainty when it can change the decision or interpretation | discipline | module: Aturan |

Gate 5 mapping (the Langkah numbers in the table above were provisional; these are final):
G1-G2 purpose paragraph, Aturan 1; G3 Langkah 9; G4-G6 Aturan 2-3; G7 purpose paragraph;
G8-G9 Aturan 4; G10 Aturan 5, Format (Tubuh 1); G11 Aturan 6; G12-G14 Aturan 7-8, Langkah 1;
G15-G18, G24-G27 dropped with owner approval, template in Data pengguna (with Aturan 39); G16 Aturan 10;
G19-G23 Aturan 9-10; G25 Data pengguna (last line); G28-G30 Aturan 15, Langkah 5; G31 Langkah 1; G32-G35 Langkah 2; G36-G38, G40, G42, G45
Langkah 3; G39, G41, G43-G44, G46 Aturan 11-12; G47-G49 Langkah 4, Aturan 13; G50, G52 Langkah 4;
G51, G53-G54 Aturan 13-14; G55-G56 Langkah 5, Format (Tubuh 1); G57 Aturan 15; G58-G60, G135-G136,
G139 Langkah 6; G59, G137-G138 Aturan 16; G61 Aturan 17; G62-G64 Langkah 5; G65 Aturan 18; G66
Aturan 19; G67, G69-G71 Aturan 20; G68 Mode; G72-G73 Langkah 7; G74-G75 Aturan 21; G76-G78, G82
Langkah 8; G79-G81 Aturan 22; G83-G84 Aturan 23; G85, G87-G90 Langkah 9; G86 Aturan 24; G91
Langkah 10; G92-G93 Aturan 25; G94-G96, G98, G100 Langkah 11; G97 Aturan 26; G99 Aturan 27; G101
Aturan 28; G102, G122 Aturan 29; G103-G104, G106-G108 Langkah 12; G105, G109 Aturan 30; G110, G114
Aturan 31; G111-G113, G115-G117 Mode; G118-G121, G123, G131, G133-G134 Format (Makanan 1-3);
G119 Format (Makanan 1); G124, G129-G130 Aturan 32; G125-G128 Format (Makanan 4); G132 Aturan 33;
G140-G141 Aturan 34; G142-G144 Aturan 35; G145 Format (Makanan 2); G146 Format (Tubuh 2); G147
Aturan 36; G148 Aturan 37; G149 Aturan 38. Added by gate 5 from the baseline: Aturan 2 last
sentence (no outside reference value) and Aturan 39 (private data shown only when needed).

No row goes to A: the module must also work when A is absent (ChatGPT Free without custom
instructions), so its honesty, ambiguity and uncertainty lines stay. Owner decision (2026-11-27): G15 to
G18 and G24 to G27 are the owner's own body data and training plan, and are dropped with owner
approval: replaced by the fill-in template in `## Data pengguna`. Every rule about how
measurements are taken and compared (G12, G13, G19 to G23, G28 to G30, G35) stays in Aturan and
Langkah; no value of the owner's appears in SKILL.md.

## Scenario (gate 3)

### S1: Screening numbers for 78-80 kg, then a two-pack label scaled
Type: shape (with protected content and discipline)
Source: rows G32 to G35 (BMI and WHtR, 94 cm kept apart from the baselines), G94 to G96 (scale to
the eaten amount), G98 to G99 (sanity check, not a wrong label), G102 (missing sugar)
Setup: a chatbot with only this module loaded (old arm: the old text; new arm: the new
`SKILL.md`); no A, no tools, no web access; two turns in one conversation.
Prompt, turn 1: "Hitung BMI-ku untuk 78, 79 dan 80 kg dengan tinggi 170 cm. Sekalian waist-to-height
ratio dengan lingkar perut 94 cm, aku ukur tadi pagi."
Prompt, turn 2: "Barusan aku makan 2 bungkus mie instan. Label per 1 bungkus: berat 85 g, 380 kcal,
karbohidrat 54 g, protein 8 g, lemak 14 g, natrium 900 mg. Gula tidak tertulis di label. Catat ya."

Worked by hand (turn 1): height 170 cm = 1,7 m, 1,7² = 2,89.
78 / 2,89 = 26,99 so 27,0; 79 / 2,89 = 27,34 so 27,3; 80 / 2,89 = 27,68 so 27,7.
WHtR = 94 / 170 = 0,5529 so 0,55.
Worked by hand (turn 2): 2 bungkus is a scale of 2. Calories 380 × 2 = 760 kcal; carbohydrate
54 × 2 = 108 g; protein 8 × 2 = 16 g; fat 14 × 2 = 28 g; sodium 900 × 2 = 1.800 mg; weight
85 × 2 = 170 g. Sanity check: 16 × 4 + 108 × 4 + 28 × 9 = 64 + 432 + 252 = 748 kcal, 12 kcal
(1,6 percent) below the label's 760 kcal, which rounding explains, so the label is not called wrong.

PASS: turn 1 shows `BMI = berat kg / tinggi meter²` with 27,0, 27,3 and 27,7 (27.0, 27.3, 27.7
also counts), says BMI is a weight-and-height screening indicator and not a body-fat measurement,
shows WHtR 0,55 (0.55 counts) labelled as built on the extra 94 cm measurement and not on the 92 cm
or 85,5 cm baselines, and states no body-fat percentage. Turn 2 shows 760 kcal, 108 g carbohydrate,
16 g protein, 28 g fat and 1.800 mg sodium (1800 mg counts), writes "data tidak tersedia" for sugar
with no invented number, keeps the sanity-check gap of 12 kcal as no reason to call the label wrong
(or does not mention a mismatch at all), and gives no figure for any food not in the prompt.
FAIL: any BMI or WHtR value other than the ones above; a body-fat percentage given or assumed in
turn 1; WHtR computed from 92 or 85,5 cm or presented as a baseline; turn 2 copying one serving
(380 kcal) instead of scaling; any number for sugar; a nutrition value not in the prompt; the label
called wrong because 748 differs from 760; a claim that the log will be kept across chats.

## Evaluation record (gates 4 and 6)

| Scenario | Arm | Status | Evidence | Result |
| --- | --- | --- | --- | --- |
| S1 | no skill | NOT RUN | the old module is the behaviour reference for this revision | - |
| S1 | current (old text) | RUN (Haiku 5.5, low, no tools, no web, no A; old text from `76f9af1`) | turn 1: "BMI = berat / (1,70)² = berat / 2,89", 78 kg 27,0; 79 kg 27,3; 80 kg 27,7; "WHtR = 94 / 170 = 0,55"; 94 cm recorded as "pengukuran tambahan, bukan baseline SEBELUM atau SETELAH DIET"; BMI "tidak bisa membedakan massa lemak dari massa otot"; "Estimasi body fat belum dihitung karena tidak diminta"; no body-fat percentage. Turn 2: "Dicatat." one table row with 170 g, 760 kcal, 108 g, 16 g, 28 g, sugar "data tidak tersedia", sodium 1.800 mg, confidence "Tinggi untuk angka label", arithmetic shown; sanity check "374 kcal, label 380 kcal, selisih 6 kcal. Selisih ini wajar karena pembulatan"; partial daily summary, "Total natrium: 1.800 mg (parsial)" | PASS on both turns. Keep: scaled numbers with arithmetic, "data tidak tersedia" for sugar, the gap read as rounding, 94 cm kept apart from the baselines. Defects outside the PASS lines: the answer repeated the owner's private measurement ("Lingkar paha 56 cm ... kemungkinan salah ukur") that the user did not ask about, and added an outside figure ("2.000 mg per hari, batas acuan WHO") that is in neither the source nor the prompt. The new text keeps the private data but shows it only when a calculation needs it or the user asks, and states no reference value that the source or the user did not give |
| S1 | candidate (new SKILL.md, 127-line template version) | RUN (Haiku 5.5, low, no tools, no web, no A) | turn 1: "BMI = berat / tinggi² = berat / (1,70)² = berat / 2,89"; 78 kg 27,0; 79 kg 27,3; 80 kg 27,7; "Waist-to-height ratio = 94 / 170 = 0,55. Lingkar 94 cm ini saya beri label pengukuran tambahan, bukan angka SEBELUM DIET atau SETELAH DIET."; "BMI adalah indikator screening berbasis berat dan tinggi, bukan pengukuran body fat."; "Untuk estimasi body fat, saya perlu umur, jenis kelamin, lingkar leher, dan titik ukur lingkar perut."; no body-fat percentage; no personal value. Turn 2: row "Mie instan, 2 bungkus (label produk) \| 170 g (2 × 85 g) \| 760 kcal (2 × 380), rentang 700–800 kcal \| 108 g (2 × 54) \| 16 g (2 × 8) \| 28 g (2 × 14) \| data tidak tersedia \| 1.800 mg (2 × 900) \| SEDANG"; sanity check "374 kcal per bungkus, dibanding 380 kcal label; selisih 6 kcal, wajar karena pembulatan. Untuk 2 bungkus: 748 vs 760, selisih 12 kcal."; daily summary with "belum dihitung" for target, TDEE and gaps; "Log tidak tersimpan lintas sesi atau lintas chat." | PASS on both turns. The 700–800 kcal range is labelled as an uncertainty range with reasons; no FAIL line covers it, and Aturan 30 asks for ranges on food without an exact weight, so it is read as allowed. Confidence SEDANG instead of TINGGI is not scored in S1 (see Not verified). Compared with the baseline: the private measurement is no longer repeated, and the outside WHO figure is gone |

## Probes (gate 7)

T8 result (supersedes the pending note below): RUN on one fresh Haiku 5.5 agent at low effort that saw only the seven names and descriptions and 17 shuffled prompts. Must load (P02, P16): picked `kalori-komposisi-tubuh`. Must not load (P09): picked `none`. PASS. Details in `../README.md`.

Pending: T8 (no fresh agent was given the skill set and these prompts yet).

- Must load: "Aku barusan makan 2 bungkus mie instan, hitung kalorinya ya." and "Hitung BMI dan estimasi body fat-ku dari lingkar perut dan leher." Description names calorie, macro and sugar/sodium counting and BMI, body fat, TDEE from body measurements.
- Must not load: "Buatkan menu makan sehat untuk seminggu." Description names counting and estimating, not menu planning.
- Status: pending: T8. Self-review by reading: the description names a situation present in both must-load prompts and absent from the must-not-load prompt.
