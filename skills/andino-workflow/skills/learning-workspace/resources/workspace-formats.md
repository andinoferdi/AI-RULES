# Workspace formats

Formats for the files of a learning workspace. Operates under Andino Workflow governance; the
steps that write these files are in [the skill](../SKILL.md). Paths below are relative to the
learner's workspace folder, never to this skill's folder.

## Layout

```text
<workspace>/
  MISSION.md            why the learner is here; one screen
  RESOURCES.md          trusted sources and communities, annotated
  NOTES.md              the learner's preferences and your working notes
  GLOSSARY.md           terms the learner has shown they understand (created when the first one is earned)
  learning-records/     0001-slug.md, 0002-slug.md ... (created with the first record)
  lessons/              0001-slug.html ... one lesson per file
  reference/            short printable sheets, one per topic
  assets/               lesson.css, quiz.js and any component a second lesson would reuse
```

One mission per workspace: two unrelated goals are two workspaces. Create a folder or file only
when the step that needs it runs; no empty placeholders. Numbers are four digits and increase by
one: scan the folder for the highest number and add one.

## MISSION.md

The compass for every teaching decision: what to teach next, which sources to use, which
practice to design. Write it in the learner's language and, where possible, their own words.

```markdown
# Mission: {topic}

## Why
{1-3 sentences: the real-world outcome the learner is after. What changes in their work or life
when they can do this? "Fix the two slow report endpoints at work without waiting for the DBA",
not "understand query plans".}

## Success looks like
- {something observable the learner will be able to do}
- {another}

## Constraints
- {time per session and overall horizon; language; budget; equipment}
- {limits set by a professional, for health, legal or financial topics}

## Out of scope
- {nearby topics the learner does not want now}
```

Rules:

- **Concrete over abstract.** "Run a half marathon in October" beats "get fitter"; push back on
  vagueness with one question before writing.
- **Their words, your guesses marked.** A part you inferred is written as "(my guess, please
  correct)" until the learner confirms it.
- **Keep it to one screen.** A mission that grows into a plan has stopped being a compass.
- **Change it only with the learner.** When the goal moves, ask, then update the file and write a
  learning record of the shift. Never leave a stale mission in place.

## RESOURCES.md

The curated sources lessons draw from. Lessons cite these; a claim with no source here is marked
unverified.

```markdown
# {Topic} Resources

## Knowledge

- [Official docs: Using EXPLAIN (PostgreSQL 16)](https://www.postgresql.org/docs/16/using-explain.html)
  What it covers: how to read plans, costs and EXPLAIN ANALYZE. Use for: every claim about plan numbers.

## Wisdom (communities)

- [Database Administrators Stack Exchange](https://dba.stackexchange.com/)
  Moderated Q&A with experienced DBAs. Use for: checking an index decision on a real plan.

## Gaps

- {an area the mission needs where no good source was found yet}
```

Rules:

- **High trust only.** Primary sources, standards, recognised experts, peer-reviewed or clinical
  guidance, well-moderated communities. Marketing dressed as teaching stays out.
- **Annotate every entry**: what it covers and when to use it. A bare link is useless later.
- **Open what you list.** List a page only after fetching it, or mark it "(not opened)".
- **Gaps are explicit.** They drive the next search.
- **Prune.** A source that proved wrong, shallow or off-mission is removed, not buried.
- **Record this learner's community choice.** When the learner says they do not want communities
  yet, write it under Wisdom ("Learner prefers to study alone for now; do not suggest
  communities until they ask") so later sessions respect it.

## NOTES.md

Preferences and working notes for this learner only.

```markdown
# Notes

- Language: Indonesian; technical terms in English.
- Time: 20 minutes per weekday, about 3 weeks.
- Lessons: short, quiz with instant feedback.
- Communities: not now (said in session 1).
```

Preferences come from what this learner said in this workspace. Never copy them from another
learner, folder or conversation.

## Learning records

`learning-records/NNNN-slug.md`, created lazily. They work like decision records for learning:
each says what is now known about the learner and why it changes what to teach next. They are
what the next lesson is chosen from.

```markdown
# {What was learned or established}

{1-3 sentences: what the learner can now do, already knew, or used to believe, and why it
matters for the next sessions.}

**Evidence**: {how it was shown: their own explanation, an exercise, a stated background}
```

Optional, only when they add something: `Status: active | superseded by NNNN`, and
**Implications** (what this unlocks or rules out next).

Write a record when:

1. the learner **demonstrated** understanding of something non-trivial: explained it in their own
   words or applied it correctly to a new case;
2. the learner **stated prior knowledge** ("I already write B-tree indexes"): record it with the
   depth they claimed, so it is not taught again;
3. a **misconception was corrected**: what they believed, what is true, and the source; these
   predict the next stumbling blocks;
4. the **mission shifted** after a conversation with the learner.

Do not write a record for:

- material that was only covered, a lesson that was only opened, or a quiz score on its own;
- a term already defined in `GLOSSARY.md`;
- a session log; records are decisions about the learner, not a diary.

When a later record contradicts an earlier one, mark the earlier one
`Status: superseded by NNNN`. Never rewrite or delete it: how understanding changed is itself
useful.

## GLOSSARY.md

The workspace's canonical words. Lessons, records and questions use them.

```markdown
# {Topic} Glossary

{One sentence on what the glossary covers.}

## Terms

**Seq Scan**:
A plan node that reads the whole table row by row and filters with its condition.
_Avoid_: full scan, table scan
```

Rules:

- **Add a term only after the learner has used it correctly.** The glossary records compressed
  understanding; it is not a dictionary to study from.
- **One name per concept.** Pick the best term, list the others under _Avoid_.
- **Tight definitions.** One or two sentences: what it is, not how to do it.
- **Use glossary terms inside definitions and every later lesson.**
- **Note ambiguities.** "In this workspace, 'set' always means a working set."
- **Revise as understanding deepens**; update in place.
