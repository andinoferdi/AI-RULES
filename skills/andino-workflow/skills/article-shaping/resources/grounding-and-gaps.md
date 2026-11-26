# Grounding, gaps and inference

Internal resource for `andino-article-shaping`. Load it when a block needs a concept the
reader has not met, when the pile lacks material a block needs, or when you are unsure
whether a sentence states a fact or a conclusion.

## Grounding

A concept is grounded when the reader either walked in knowing it or met it in an earlier
block. A block that leans on an ungrounded concept loses the reader; it is the one move the
article cannot make. The unit is the concept, not the word for it: a block can lean on an
idea the reader lacks with no jargon in sight. Where a concept has a name, grounding it
means landing the idea and the name together.

A concept gets grounded one of two ways:

- **Prerequisite:** the reader brings it. Settled with the author before the opening.
- **Introduced:** a written block establishes it, and every later block may use it.

Keep a running list: the prerequisites plus everything a written block introduced. A
candidate is reachable only if everything it leans on is on the list, and picking a block
that introduces a concept unlocks every block that was waiting on it. Say what each
candidate introduces, in plain words, so the author can see which paths it opens.

The big lever is what counts as a prerequisite. Demand too much and readers without it are
shut out; introduce too much inside the article and the early blocks drown in definitions.
Settle it with the author at the start, and reopen it when a tempting block turns out to
need something nothing has introduced.

## When a block needs what the reader lacks

| Remedy | What you do | Trade-off |
| --- | --- | --- |
| Grounding block first | Offer a block whose one job is to introduce the concept, then the wanted block | Keeps the article open to newer readers; costs a block |
| Promote to prerequisite | Ask the author whether this reader already knows it; if yes, add it to the list | Keeps the article fast; shuts out readers who do not |
| Rephrase | Make the point in terms already on the list, without the concept | No new load on the reader; sometimes less precise |

## Gaps

A gap is material a block needs that neither the pile nor the author has given: a figure,
an example, a date, a quote, the outcome of a decision. Name it to the author in the message
where it matters, say what the block needs it for, and offer three ways on:

1. The author supplies it now.
2. The block says plainly what is not known ("we have not measured whether incidents
   dropped yet"). An honest unknown can carry weight of its own.
3. The block is cut, or reframed so it no longer needs the material.

If the author asks you to write past a gap, write what is known and leave a visible marker
in the article, for example `[GAP: incident count since the new rule; not measured yet]`.
Never close a gap with a plausible guess, however small.

## Fact or inference

A fact is stated in the pile or by the author. An inference is a conclusion you draw from
facts. Both can belong in the article, but they read differently.

- The pile says the on-call engineer handled the incident alone. "Nobody else answered the
  page" is an inference: perhaps nobody else was paged. Write what the pile states, or ask
  the author what happened.
- The pile says the release went out at four on Friday and the dashboard was broken until
  Monday morning. "The bug sat in production all weekend" is an inference from those two
  facts. Write it as the conclusion it is, or confirm it with the author.

When in doubt, keep the wording to what the pile states and ask about the rest.

## The author's text

Text in the article file that you did not write came from the author. It is evidence, not
contamination: the author is allowed to add facts the pile lacks. Keep it byte for byte,
build around it, and let it change what comes next. If it seems to contradict the pile or a
written block, ask which stands. Never delete, move or reword it on your own judgment.
