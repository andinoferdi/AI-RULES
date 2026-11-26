---
name: andino-article-shaping
description: Use when the user has raw material such as notes, fragments, a brain dump or a transcript and wants it shaped into an article, essay or post together with them, or asks for writing-beats or writing-shape. Operates under Andino Workflow governance.
---

# Shape raw material into an article with its author

Internal method ID: `andino-article-shaping` (aliases: `article-shaping`, `writing-beats`, `writing-shape`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

Turn a fixed pile of raw material into an article the author recognises as their own. This
is exploit, not explore: the noticing is done and the pile is fixed, so you commit to a path
through it and mine the pile to fill each block. You propose, the author chooses, and only
agreed text reaches the article file, one block at a time. Two disciplines carry the
quality: every concept is grounded before a block leans on it, and nothing in the article is
invented.

## Trigger and non-trigger

Use when the user has raw material (a notes file, fragments, a pasted brain dump, an
interview or talk transcript) and wants an article, essay, blog post or newsletter shaped
from it together with them, or names `writing-beats` or `writing-shape`.

Do not select for:

- Collecting material while the user is still noticing things and has no article in view:
  [raw-capture](resources/raw-capture/guide.md).
- Polishing, proofreading or rewriting finished prose: `natural-writing`.
- Thesis or academic chapters: `skripsi-skill`.
- Marketing pages and UI copy: `copywriting`.
- Documents another agent reads: `agent-document-authoring`.

## Select a resource, not a second lifecycle

Load only the resource the current need names. It runs inside this procedure and current
authority; it starts no second plan.

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| The user is still exploring and wants fragments collected, not an article | [raw-capture](resources/raw-capture/guide.md) | The pile is fixed |
| A block needs a concept nothing has introduced, the pile lacks material, or a fact may be an inference | [grounding and gaps](resources/grounding-and-gaps.md) | Every candidate leans only on what the reader has and every fact is in the pile |
| Choosing how to render a block, or checking a drafted block's prose | [format and prose](resources/format-and-prose.md) | The block is plain prose and passed the prose check in Rules |
| Candidates keep coming out alike: optional lenses for moves, openings and article shapes | [lenses](resources/lenses.md) | The candidates already differ in thesis or entry point |
| Seeing a whole session, in Indonesian | [worked example](resources/worked-example.md) | The procedure is already clear |

## Prerequisites

The pile, as a file path or pasted text, and a separate destination file for the article
that you can write. Without a pile there is nothing to shape: ask for the material, or
start with raw-capture.

## Procedure

1. **Read the pile end to end** before proposing anything. Note what it holds: incidents,
   claims, quotes, images and metaphors, numbers, open questions and uncertainties,
   tangents. The pile file stays read-only for the whole session. Done when you can say
   which material could open the article and which is tangent.
2. **Settle the destination.** Use the path the user named. Otherwise ask once and remember
   the answer. The destination is never the pile file.
3. **Settle the reader.** Propose two short lists and ask the author to confirm or correct
   them: what the reader already knows walking in (the prerequisites), and what the article
   must introduce. Name in one line the tangents you plan to leave out. Done when the
   author has answered; nothing is written to the article before then. Revisit the lists
   whenever a wanted block needs a concept nothing has introduced.
4. **Offer two or three openings** in finished prose, built only from pile material and the
   confirmed reader. Each implies a different thesis, a different answer to what the article
   argues, not only a different place to start. Under each, one plain line naming its
   thesis, what it introduces to the reader and which blocks it makes possible next.
   Recommend one and say why; the author picks one or asks for a hybrid. Done when the
   author has chosen.
5. **Write the chosen block.** Re-read the article file from disk. If it holds new text from
   the author that the approved block would now repeat or contradict, write nothing yet:
   show the overlap and offer the block reworked around the author's text. Otherwise append
   exactly the approved text. To change a word, show the change and get a yes first. Add no
   title, heading or frontmatter the author did not ask for. Done when the re-read file ends
   with the approved text, every earlier byte is unchanged, and nothing in the new block
   repeats what the page already says.
6. **Update the running list** of what the reader now has: the prerequisites plus every
   concept a written block introduced. It is your working note; it steers step 7.
7. **Offer two or three next blocks.** Ask: given what is on the page, what does the reader
   need to hear next? Each candidate states in plain words the move it makes, the pile
   material it uses, what it introduces, what it opens next, and the form it takes with the
   reason: prose carries an argument, a list carries parallel items, a table carries three
   or more items with the same fields, a direct quote keeps wording that is itself the
   point, a callout holds an aside that would derail the argument. Every candidate leans
   only on the running list. A block that needs a concept the reader lacks is not a
   candidate yet; use one of three remedies instead: offer a grounding block in its place,
   propose promoting the concept to a prerequisite, or rephrase the block in terms the
   reader already has. Recommend one candidate; the author picks.
8. **Loop steps 5 to 7** until the journey is complete. The author decides when it is done.
   Check that the ending pays off what the opening promised; if the article drifted, say so
   and offer to re-thread the ending or change the opening. Leftover pile fragments are
   expected and stay out.

**Pacing.** One block per turn is the default. When the author explicitly asks to go
faster, offer a section of two or three consecutive blocks as one candidate; the same rules
apply and nothing is written before the author approves it.

## Rules for every session

- **The pile is read-only.** Quote, split, merge and paraphrase it in the article; the pile
  file itself is never edited, trimmed or overwritten.
- **Write only what was agreed.** Every write follows a fresh read of the article file and
  adds or replaces only the block the author just approved, word for word. Nothing is
  written ahead. When the author asks to redo one block, edit that block in place and leave
  the rest alone.
- **The author's text wins.** Text in the article file that you did not write is the
  author's. Keep it byte for byte wherever it sits, even when the pile does not contain it:
  the author is a source too. Build the next blocks around it, and let it change what comes
  next: a block you write afterwards neither repeats nor contradicts it. If it seems to
  contradict the pile or a written block, ask the author which stands; changing it is their
  call.
- **Invent nothing.** Every number, name, date, quote, incident and cause, and every sensory
  or emotional detail, traces to the pile or to something the author said. When a block
  needs material the pile lacks, name the gap to the author and offer three ways on: they
  supply it now, the block says plainly what is not known, or the block is cut. A
  conclusion you draw from pile facts is an inference: write it as one ("as far as we can
  tell", "probably") or confirm it with the author before writing it as fact. A request to
  "write it directly" or "make it hit harder" speeds up the pacing; the evidence rule and
  the editor questions stay. If the author asks you to write past a gap, write what is known and leave a
  visible `[GAP: what is missing]` marker in the article.
- **One block, one move.** A block sets a scene, lands a claim, asks a question, adds an
  aside, turns the argument or pays it off. Size it by what the move needs: one sentence, a
  paragraph, or several paragraphs for a self-contained vignette or example. A block that
  needs subheadings or makes two moves is two blocks; split it.
- **Mine the pile, keep one voice.** The pile is a quarry, not a script: split, merge and
  rework fragments so the article reads as one voice, the author's. Keep their images,
  idioms and plain terms; quote exactly or paraphrase without quotation marks; keep their
  register, in the language they write in.
- **Talk to the author plainly.** Each message asks for one decision, with the options and
  your recommendation. Describe moves in everyday words; beat types, lenses and the running
  list are your working vocabulary, not the author's. Raise a gap or a pushback when it
  bears on the decision in front of the author.
- **Push back like an editor.** Ask these out loud when they apply: What does this block do
  for the reader that the previous one did not? If we cut it, what breaks? This sentence
  does two jobs; split it or pick one? The opening promised X and we drifted to Y; re-thread
  or change the opening? We need an example here and the pile has none; give me one or we
  cut the section. Flag tangents too, and contradictions inside the pile itself.
- **Prose the author would sign.** Before showing a candidate, reread it for an opening that
  clears its throat, "not X but Y" ("bukan X, tapi Y") when nobody claimed X, a list of
  three built for rhythm, stacked dashes, a closing line that restates its paragraph, and a
  run of clipped fragments for drama. Rewrite what you find in the author's plain register.
  Sentence-level polish belongs to `natural-writing`; the full pattern list and the format
  table are in [format and prose](resources/format-and-prose.md).

## Shortcuts that break the article

| Shortcut | What actually happens |
| --- | --- |
| "I'll draft the whole article to save turns." | A long batch drifts toward bland, even prose and skips every choice the author should make. Go block by block; use section pacing only when the author asks. |
| "One vivid detail will make this scene land." | A detail the pile does not hold is invented, however small. Use what the pile has, or ask the author for the real one. |
| "This sentence in the file is not in the pile, so it is made up." | You did not write it, so the author did. Keep it and build around it. |
| "The reader surely knows this term." | What the reader knows is the author's call. Ask, or introduce the term first. |
| "I'll tighten the approved opening while I write it." | The author approved specific words. Propose the change; write the approved text. |
| "The author said write it directly, so I can fill in the scale." | Pressure changes the pacing, not the evidence. Write what is known and name the gap. |
| "Labelling the move helps the author follow." | Labels are your vocabulary. The author decides faster on plain descriptions. |
| "Every fragment should make it in." | The article ends when the journey is complete. Leftovers are the point of having a pile. |

## Red flags

- An opening written to the file before the author chose it, or before the reader was settled.
- Written text that differs from the approved candidate.
- A sentence the author added has disappeared, moved or been reworded, or a later block
  repeats it.
- A number, name, quote, time or feeling in the article that neither the pile nor the author
  supplied.
- An inference written as fact.
- A block that leans on a concept the reader has not met.
- Candidates that reword one thesis, or that fill a generic hook frame instead of using pile
  material.
- Several decisions asked in one message, or method labels shown to the author.
- The pile file edited, or the article written into it.
- A title, frontmatter or publishing step nobody asked for.

## Ownership and permission boundary

Andino coordinates selection, shared progress, resource guards and final status from
evidence. This skill owns its procedure, resources and checks, and coordinator brevity
never truncates them. Focus shapes your messages to the author and never shortens the
article. Write only the article file. Loading this skill grants no publication, platform
formatting, commit or push authority; the author publishes.

## Output

- **The article file:** only the blocks the author approved, in order, with every author
  edit intact and any `[GAP: ...]` marker the author chose to keep.
- **Each turn's message:** what was written, or that nothing was; one decision with two or
  three options and a recommendation; any gap or pushback that bears on it.
- **At the end:** open gaps, inferences still unconfirmed, and pile material left out.

## Verification

- [ ] The pile file is unchanged (same hash, or an empty diff).
- [ ] The article holds only approved blocks, each word for word as approved, with every
      author edit intact.
- [ ] The reader was settled before the first write, and every concept the article leans on
      is a prerequisite or was introduced earlier.
- [ ] Every fact traces to the pile or the author; inferences are marked or confirmed; gaps
      were named, not filled.
- [ ] Each block makes one move and says something the page did not already say.
- [ ] The ending pays off the opening's promise.
- [ ] Every written block passed the prose check in Rules.

## Worked example and anti-pattern

[The worked example](resources/worked-example.md) follows one Indonesian session from a pile
of notes to three written blocks, with an author edit, a format argument and a pressure
turn, then shows the same moments done wrong.

Anti-patterns: openings built from a formula with invented scenes or statistics; deleting
an author's sentence because the pile does not contain it; rewriting the chosen opening on
the way to the file; showing beat labels and grounding notation to the author; answering
"make it dramatic" with a number nobody gave you.

## Fallback

- No write access to the destination: keep the article in the conversation as one block,
  resend it whole after each agreed change, and say so.
- The pile is too thin for the article the author wants: say what is missing and offer
  raw-capture to collect more.
- The author does not settle the reader: propose the narrowest reasonable reader, state it
  as an assumption in your next message, and revisit it when a block depends on it.

## Local resources

The resources above are packaged with this skill; upstream repositories are not runtime
dependencies. The MIT notice is in [references/license.md](references/license.md).

## Operational example (offline)

This stdlib check replays a short session. It fails when a block leans on a concept the
reader has not met or carries a fact neither the pile nor the author supplied, and it
asserts that the author's added line and the pile survive. `ANDINO_NEGATIVE=1` injects an
invented result, so the run must exit 1.

```python andino-operational-example
import hashlib, json, os

pile = "Deploy Jumat: dua insiden dalam tiga bulan. Dimas on-call sendirian. Aturan baru: deploy terakhir Kamis."
pile_facts = {"dua-insiden-tiga-bulan", "dimas-sendirian", "deploy-terakhir-kamis"}
pile_hash = hashlib.sha256(pile.encode()).hexdigest()
reader = {"git", "ci"}
author_line = "Saya sendiri ikut begadang malam itu."  # added by the author between writes
author_facts = {"penulis-begadang"}

blocks = [  # each one approved by the author before it was written
    {"text": "Dua insiden dalam tiga bulan, dua-duanya dari deploy Jumat.",
     "requires": set(), "introduces": {"insiden-jumat"}, "facts": {"dua-insiden-tiga-bulan"}},
    {"text": "Yang jaga on-call, orang yang dipanggil kalau produksi rusak, cuma Dimas.",
     "requires": {"insiden-jumat"}, "introduces": {"on-call"}, "facts": {"dimas-sendirian"}},
    {"text": "Sekarang deploy terakhir hari Kamis.",
     "requires": {"insiden-jumat"}, "introduces": {"aturan-kamis"}, "facts": {"deploy-terakhir-kamis"}},
]
if os.environ.get("ANDINO_NEGATIVE") == "1":
    blocks[2]["facts"] = blocks[2]["facts"] | {"insiden-turun-80-persen"}  # an invented result

article, grounded = [], set(reader)
for number, block in enumerate(blocks, 1):
    if not block["requires"] <= grounded:
        raise SystemExit(f"block {number} leans on {sorted(block['requires'] - grounded)}")
    if not block["facts"] <= pile_facts | author_facts:
        raise SystemExit(f"block {number} invents {sorted(block['facts'] - pile_facts - author_facts)}")
    article.append(block["text"])
    grounded |= block["introduces"]
    if number == 1:
        article.append(author_line)

assert author_line in article and hashlib.sha256(pile.encode()).hexdigest() == pile_hash
print(json.dumps({"valid": True, "blocks": len(blocks), "grounded": sorted(grounded)}))
```

## Provenance

Re-based on Matt Pocock's `writing-beats` and `writing-shape` (mattpocock/skills,
`skills/in-progress`, commit 6f7f783, 2026-11-24) under the MIT license: the loop, grounding
by concept, pile-built candidates with what each grounds and opens, format arguments, the
editor questions and the writing rhythm. Andino additions: the gap protocol and the
inference rule, author-text precedence, the third grounding remedy, section pacing, the
verification checklist, the lenses, the worked example, raw-capture and the operational
example.
