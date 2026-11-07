# Worked example: a redesign with hand-written routing

## Raw prompt

```text
redesign halaman dashboard admin saya biar ga keliatan AI-made, pake brainstorming, planning, tdd, terus verifikasi. pake council juga. filenya di src/app/admin/page.tsx
```

## Inventory

Claude Code, Layer 1 block in `~/.claude/CLAUDE.md`: `design-taste-frontend`, `impeccable`,
`antislop`, `antislop-ui` and `council` are installed. `playwright` is connected.

## Pinned facts

A redesign of the admin dashboard page; the goal "not looking AI-made"; the file
`src/app/admin/page.tsx`; `council` requested. No framework version, visual reference or
current-style description was given.

## Checks

| Check | Finding |
| --- | --- |
| Phase routing | `brainstorming`, `planning`, `tdd` and `verifikasi` are phases. Removed; brainstorming becomes `Mode: brainstorm first`. |
| Skill conflict | `council` runs five advisors for decisions that are expensive to undo; a page redesign can be reverted. |
| Missing owner | A redesign maps to `design-taste-frontend` and `impeccable`; "AI-made" maps to `antislop-ui`. All installed. |
| MCP | Picker: screenshots at 360/768/1440 px use `playwright`, which is connected. |
| Done when | None given. Proposed from the stated outcome only. |
| Evidence | Picker row for UI asks for page, current style and visual reference; the page is given. |

## Output

```text
Skills: design-taste-frontend, impeccable, antislop-ui, council
Tools/MCP: playwright for before/after screenshots
Mode: brainstorm first
Task: redesign halaman dashboard admin supaya tidak terlihat AI-made.
Context/evidence: halaman: src/app/admin/page.tsx; tampilan sekarang: [screenshot];
  referensi visual: [link atau gambar]
Done when: screenshot sebelum dan sesudah di 360, 768 dan 1440 px, dan review antislop-ui
  pada halaman baru tidak menemukan pola AI-made.
```

Notes:
- Dihapus: brainstorming, planning, tdd, verifikasi (workflow memilihnya; brainstorming jadi `Mode`).
- Ditambahkan: `design-taste-frontend`, `impeccable`, `antislop-ui`, `playwright`, semuanya terpasang.
- Konflik: `council` untuk keputusan yang mahal dibalik, sedangkan redesign halaman bisa dibalik.
- `Done when` adalah usulan. Inventaris dari blok Lapis 1 di `~/.claude/CLAUDE.md`.

Pertanyaan: `council` tetap dijalankan untuk redesign ini?

Mau saya jalankan prompt ini di sesi ini?

## Why each choice

- The file path stays verbatim; no framework or version is added, although the path suggests one.
- Current style and reference are placeholders because the user can paste them; only the
  `council` choice needs an answer, because only the user can make it.
- `Constraints` is absent: the user gave no limit, and approval rules already live in Layer 1.
