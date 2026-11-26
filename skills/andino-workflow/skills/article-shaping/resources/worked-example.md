# Worked example: one session, in Indonesian

Internal resource for `andino-article-shaping`. It follows one session from a pile of notes
to three written blocks. Every detail in the agent's text comes from the pile or from the
author's messages; the comments in italics point to the rule each turn applies.

## The pile (`jumat.md`)

```markdown
# catatan: berhenti deploy hari jumat

- tiga bulan terakhir ada dua insiden besar, dua-duanya dari deploy Jumat sore.
- insiden kedua: rilis jam 4 sore Jumat, migrasi kolom bikin dashboard admin error. baru beres Senin pagi.
- Dimas yang on-call waktu itu, sendirian.
- Dimas pas retro: "yang review PR jam 4 sore Jumat itu orangnya udah mikirin weekend."
- aturan baru: deploy terakhir Kamis jam 3 sore. hotfix tetap boleh, tapi harus di-approve dua orang.
- deploy Jumat itu kayak titip kunci rumah ke tetangga terus langsung berangkat mudik.
- aturan ini baru jalan 5 minggu. belum diukur insidennya turun atau nggak.
- tim mobile protes, rilis app store mereka biasanya Jumat.
- ada ide feature flag biar deploy nggak sama dengan rilis fitur. belum dikerjakan.
- (samping) CI kita lambat, 25 menit sekali jalan. nggak nyambung sih.
```

## Turn 1: settle the reader

**Author:** Ini catatan saya di `jumat.md`. Tolong bentuk jadi artikel buat blog tim, simpan
di `artikel-jumat.md`.

**Agent:**

> Catatannya sudah saya baca sampai habis. Sebelum menulis apa pun, saya perlu tahu
> pembacanya.
>
> Usul saya, pembaca sudah paham git, pull request, code review, CI, dan deploy ke
> production. Yang dijelaskan di dalam artikel: apa itu on-call, dan aturan deploy terakhir
> hari Kamis beserta pengecualian hotfix-nya.
>
> CI yang lambat dan ide feature flag saya tinggalkan dulu, karena tidak menopang argumen
> utamanya.
>
> Pembacanya seperti itu, atau ada yang perlu digeser?

*Steps 1-3: the pile is read in full, the reader is proposed as two lists, tangents are
named in one line, and the message asks one thing.*

**Author:** Pembacanya engineer baru di tim. Paham git dan CI, tapi belum pernah on-call.

## Turn 2: openings from the pile

**Agent:**

> Oke, on-call saya jelaskan di dalam artikel. Ini tiga pembuka, semuanya dari catatanmu.
>
> **1. Mulai dari kejadian**
> "Jumat jam empat sore, satu migrasi kolom masuk ke production. Dashboard admin error, dan
> baru beres Senin pagi."
> Tesis: deploy Jumat sore sudah dua kali berujung insiden, jadi kebiasaannya harus diubah.
> Pembaca jadi tahu insiden kedua. Setelah ini bisa lanjut ke siapa yang menanganinya, atau
> ke pola dua insiden.
>
> **2. Mulai dari kalimat Dimas**
> "Kata Dimas di retro: 'Yang review PR jam 4 sore Jumat itu orangnya udah mikirin
> weekend.'"
> Tesis: masalahnya ada di perhatian reviewer menjelang weekend. Pembaca langsung memegang
> argumennya, dan dua insiden jadi buktinya setelah ini.
>
> **3. Mulai dari perumpamaan**
> "Deploy hari Jumat itu kayak titip kunci rumah ke tetangga, terus langsung berangkat
> mudik."
> Tesis: perubahan yang dikirim tepat sebelum semua orang pergi tidak punya penjaga.
> Pembaca dapat gambarannya dulu. Kurang terasa kalau pembaca belum tahu kejadiannya.
>
> Saya sarankan nomor 1: engineer baru perlu melihat kejadiannya dulu sebelum mau menerima
> aturannya. Pilih yang mana, atau mau digabung?

*Step 4: three different theses (the incident, the reviewer's attention, the image), each
built from one pile item, each with what it introduces and opens. No timestamp, count or
feeling the pile lacks.*

**Author:** Nomor 1.

## Turn 3: write exactly the chosen text

**Agent:**

> Pembuka nomor 1 sudah saya tulis ke `artikel-jumat.md`, persis seperti tadi.
>
> Berikutnya, pilih satu:
>
> 1. **Ini yang kedua.** Insiden ini yang kedua dalam tiga bulan, dan dua-duanya dari
>    deploy Jumat sore. Pembaca melihat pola, dan setelah ini aturan baru terasa sebagai
>    jawaban atas pola itu. Bentuknya prosa, karena isinya satu sebab-akibat.
> 2. **Siapa yang menangani.** Dimas yang on-call, sendirian. Di sini on-call dijelaskan:
>    orang yang dihubungi kalau production rusak. Setelah ini, kalimat Dimas di retro.
>    Prosa juga, dua kalimat.
> 3. **Perumpamaan titip kunci.** "Deploy Jumat itu kayak titip kunci rumah ke tetangga,
>    terus langsung berangkat mudik." Kutipan langsung dari catatanmu, karena gambarannya
>    milikmu sendiri. Pembaca dapat rasa "ditinggal tanpa penjaga" sebelum masuk ke soal
>    on-call.
>
> Saya sarankan nomor 1.

*Steps 5-7: the file gets the approved words unchanged, the next candidates lean only on
what the reader has, and each names its form with the reason.*

**Author:** Nomor 1.

Between turns the author opens the file and adds a line under the opening:
"Saya sendiri ikut begadang malam itu."

## Turn 4: the author's line stays

**Agent:**

> Sebelum menulis, saya baca ulang file. Ada kalimat baru darimu di bawah pembuka, "Saya
> sendiri ikut begadang malam itu." Kalimat itu saya biarkan persis di tempatnya, lalu blok
> kedua saya tambahkan di bawahnya:
>
> "Itu insiden kedua dalam tiga bulan. Yang pertama juga datang dari deploy Jumat sore."
>
> Blok berikutnya yang saya sarankan soal Dimas dan on-call, dan pilihan-pilihannya
> bergantung pada satu hal: catatanmu bilang Dimas on-call sendirian, sedangkan kamu ikut
> begadang. Maksudnya Dimas satu-satunya yang on-call, dan kamu menemani? Setelah kamu jawab,
> saya tawarkan pilihannya.

*Rules "The author's text wins" and "Talk to the author plainly": the added line is kept
byte for byte; the possible tension with the pile becomes the one question, and the next
candidates wait for it because they depend on the answer.*

**Author:** Iya, Dimas satu-satunya on-call. Saya cuma nemenin di chat. Bagian berikutnya
bikin pembaca ngerasa seberapa parah dampaknya. Langsung tulis aja.

## Turn 5: pressure, a gap and an inference

**Agent:**

> Saya tulis langsung, tapi hanya dari yang ada di catatanmu. Lamanya error sudah ada di
> pembuka, jadi blok ini menambah sisi orangnya:
>
> "Yang on-call waktu itu cuma Dimas. On-call artinya dialah orang yang dihubungi kalau
> production rusak, dan kali itu dia memegangnya sendirian."
>
> Catatanmu tidak punya angka dampak: berapa admin yang tidak bisa bekerja, atau apa saja
> yang tertunda. Saya tidak mengisinya dengan perkiraan. Di artikel saya taruh penanda
> `[GAP: dampak ke admin selama dashboard error; belum ada datanya]`. Kalau kamu punya
> angkanya, saya ganti penanda itu. Kalau tidak, kita tulis terus terang bahwa dampaknya
> belum dihitung.
>
> Satu hal sengaja tidak saya tulis sebagai fakta: bahwa bug itu dibiarkan sepanjang
> weekend. Itu kesimpulan saya dari jam rilis dan jam beresnya, bukan isi catatanmu. Benar
> begitu kejadiannya?

*Rule "Invent nothing": "write it directly" changes the pacing only; the gap is named with
the ways on, and the inference is held back until the author confirms it.*

## The article file after turn 5

```markdown
Jumat jam empat sore, satu migrasi kolom masuk ke production. Dashboard admin error, dan baru beres Senin pagi.

Saya sendiri ikut begadang malam itu.

Itu insiden kedua dalam tiga bulan. Yang pertama juga datang dari deploy Jumat sore.

Yang on-call waktu itu cuma Dimas. On-call artinya dialah orang yang dihubungi kalau production rusak, dan kali itu dia memegangnya sendirian.

[GAP: dampak ke admin selama dashboard error; belum ada datanya]
```

## Anti-pattern: the same moments done wrong

An opening offered from a formula instead of the pile:

> "Jam 02.14 dini hari, ponsel Dimas berdering untuk ketiga kalinya."

The time, the hour of night and the count of calls are invented. The pile gives a Friday
four o'clock release and nothing about calls.

The pressure turn answered with scale:

> "Selama 64 jam, ratusan admin tidak bisa bekerja, dan Dimas begadang tiga malam
> berturut-turut. (Beat 3: payoff)"

- "64 jam" turns an inference from two pile times into a precise fact.
- "ratusan admin" and "tiga malam berturut-turut" appear nowhere in the pile or the author's
  messages.
- "(Beat 3: payoff)" shows the agent's working label to the author.
- Deleting "Saya sendiri ikut begadang malam itu." because the pile does not contain it
  would discard the author's own evidence.
