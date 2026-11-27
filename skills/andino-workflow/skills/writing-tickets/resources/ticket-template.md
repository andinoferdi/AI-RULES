# Ticket template

Read this at step 6, before writing the first ticket. One template serves both tracker kinds;
only where the blocking edges live changes. Labels are role names here (ready-for-agent,
ready-for-human); write the tracker's own strings from its configuration.

## Local ticket file

One file per ticket at `<tickets-folder>/<NN>-<slug>.md`, numbered from `01` with blockers
first. Never one combined file. The graph check reads the heading, the "Blocked by" line and
the checkboxes exactly as shown.

```markdown
<the tracker's required first line for AI-written text, when it has one>

# <NN>: <Ticket title>

**Status:** <ready-for-agent | ready-for-human label string>

**Blocked by:** <NN, NN> | None (can start immediately)

**What to build:** <the end-to-end behaviour this ticket makes work, from the user's side: the
command, page or call, and what it returns or stores. Name types, commands and data shapes,
not files.>

**Out of scope:** <what a builder might drift into and must not: neighbouring tickets'
behaviour, decided exclusions, open decisions this ticket neither builds nor forbids>

- [ ] <input or action> -> <observable result>
- [ ] <the edge case the requirement implies> -> <observable result>
```

A HITL ticket for an open decision uses the same file with the ready-for-human label, a title
that states the question, **Owner:** and the person, the options known so far, and what the
answer unblocks. Its criteria are the decision recorded where builders will read it.

## Tracker issue

Publish in dependency order so every edge can name a real identifier. Where the tracker has
native blocking links and sub-issues, set them and omit the "Blocked by" section.

```markdown
<the tracker's required first line for AI-written text, when it has one>

## Parent
<reference to the parent issue, when the source was one; otherwise omit>

## What to build
<as above>

## Acceptance criteria
- [ ] <input or action> -> <observable result>

## Out of scope
<as above>

## Blocked by
- <reference to each blocking issue>, or "None (can start immediately)"
```

## Acceptance criteria

Every criterion is something an agent can run or look at and get a yes or no.

| Write | Instead of |
| --- | --- |
| "`notes search` with no query prints the ten newest notes, newest first" | "Search works without a query" |
| "A settings file written before this change still loads and keeps its values" | "Backward compatible" |
| "Saving an 11th favourite is refused with `limit is 10` and the list is unchanged" | "Validate the limit" |
| "The renamed field appears in `export --json` output; the old name does not" | "Rename done" |

Cover the case the requirement states and the edge it implies: empty input, the boundary
value, the refusal, the old data file. Use values from the spec or the sample data so the
builder can check the exact output.

## Sizing

A ticket fits one fresh context when it delivers one behaviour a person or test can observe.
Split it when:

- the title needs "and" to say what it delivers;
- it touches more than two areas of the code (a store, a command and a report, say);
- its acceptance list runs past about six criteria;
- part of it could ship and be verified alone.

Merge two tickets when neither is observable without the other.

## AFK and HITL

| Mark | When | Label |
| --- | --- | --- |
| AFK | An agent can build and verify it from the ticket and the code alone | ready-for-agent |
| HITL | It needs a decision only a person can make, a review of something subjective (a design, wording), or access an agent lacks | ready-for-human |

A ticket that needs an open decision is blocked by the HITL ticket that holds the decision.

## The reader check

Read each ticket as an agent that has the repository and this ticket, and nothing else: not the
conversation, not the spec, not the other tickets' bodies. Answer:

1. Can I say in one sentence what will work when I am done?
2. Can I find where to start by exploring, from the names and behaviours the ticket uses?
3. Does every criterion tell me exactly what to run and what I should see?
4. Is anything the conversation settled (an exclusion, a limit, a rule) missing?
5. Would I be tempted to build something out of scope, or to answer an open decision?

Any "no" on 1 to 4 or "yes" on 5 is a fix in the ticket before it is published.
