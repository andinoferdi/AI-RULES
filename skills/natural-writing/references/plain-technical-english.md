# Plain technical English

An opt-in register for English procedural and technical text: runbooks,
procedures, error messages, release notes, UI text and docs for readers outside
the field or reading in a second language. It borrows the discipline of
ASD-STE100 Simplified Technical English without claiming compliance with it:
the official STE dictionary is not reproduced here, and no tool can certify an
STE document.

Use it when the user asks for plain, simple or STE-style English, or when the
genre is one listed above. Do not use it for marketing copy, essays, fiction or
any text where voice and persuasion are the point; say so and offer the default
English guide instead.

## Rules

1. **Classify each passage.** Procedural text tells the reader what to do.
   Descriptive text explains how something works. Write procedures in the
   imperative, one instruction per sentence. Write descriptions in simple tenses,
   one topic per paragraph.
2. **Condition before command.** "If the build fails, read the log." The reader
   checks the condition before acting.
3. **Name what the step depends on.** The host, the flag, the account or the
   prior step: "Restart the `sync` service on the host that runs the job."
4. **One term, one meaning.** Pick one word for each thing and each action and
   use it every time (for example "check", not "check", "verify" and "confirm"
   for the same action). Break noun stacks of four or more words with a
   preposition: "the timeout value for the connection pool".
5. **Define a term at first use**, in under ten words: "idempotent (safe to run
   twice)". Do not define product names or standard names (HTTP, Postgres, S3).
6. **Plain verbs.** Prefer a single verb to a phrasal verb or a nominalization:
   "start" for "spin up", "contact" for "reach out to", "analyze" for "perform an
   analysis of".
7. **Warnings: action first, then the risk.** "Do not run this command against
   production. It deletes rows."
8. **Complete grammar.** Keep articles and "that". No telegraph style. No
   contractions in procedures.
9. **Split joined clauses.** A semicolon or a dash that joins two ideas usually
   means two sentences. Keep a dash that marks a real aside.
10. **Lists for sequences.** Three or more steps become a numbered list; one
    instruction per item.

Length targets: about 20 words per procedural sentence and 25 per descriptive
sentence. These are guidance for spotting sentences that carry two ideas, not
quotas. Keep a longer sentence when splitting it would drop a condition, a scope
qualifier or a number, and say so with a `Kept as-is:` line.

## What never changes

- Code, commands, flags, paths, identifiers, quoted error text and product names.
- Modality. "May fail", "might take a minute", "usually clears" and "should"
  carry the author's confidence. A plain rewrite keeps that confidence: it may
  choose a plainer modal word with the same strength, never a certainty the
  source did not state. Do not delete a hedge to shorten a sentence.
- Facts. When the source gives no number, cause or duration, keep the general
  statement or add `[data needed: …]`; do not supply one.

## Example

Before:

> You should probably restart the sync worker if it's been stuck for a while —
> this usually clears the queue. Run `systemctl restart sync-worker` on the job
> host. It might take a minute to come back.

After:

> If the sync worker is stuck, restart it. This usually clears the queue.
>
> 1. On the job host, run `systemctl restart sync-worker`.
> 2. Wait for the worker to start again. This might take about a minute.

Change note: condition moved before the command; the dash joined two ideas;
"should probably" became a direct step because the restart is the advised
action, while "usually" and "might" stay; "for a while" is vague, so the author
may want `[data needed: how long counts as stuck]`.

KEEP example: "Do not delete the `prod` bucket. Deletion cannot be undone." is
already plain, ordered and complete. Leave it unchanged.
