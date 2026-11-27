# Write a session diagnostics report

Used by gate 6, and by the quick path for its short answer. The report answers the user's
questions first, then shows the evidence. Case fields and statuses are in the
[supporting contract](contract.md).

## Short answer

For a question about one event, reply in this shape, near 150 words and never over 200:

1. The answer or cause in the first sentence, in the user's terms.
2. The decisive lines: what the records show, each with `path:line` (or `L<n>` once the file is
   named).
3. Who gave the instruction: the human, injected hook or system text, a tool result or a parent
   agent, with the line that shows it.
4. One line on what you could not see (a script's contents, a config, a missing record).

Then offer the full report in one line. No headings, tables or sections.

## Report sections

Write `report.md` in the workspace with these sections, in order. A section that does not
apply says why in one line.

1. **Verdict.** Answer each question the user asked, in their order, in the first lines. For
   each conclusion state its confidence (high, medium, low) and, separately, the confidence in
   its cause. Cite the decisive lines. No statement about what a skill should change.
2. **Problem statement and scope.** The agreed statement; session identity (id, path, first
   prompt, first timestamp in the user's zone and UTC); rejected candidates with reasons;
   examined range; whether the session was still running; differences between the recorded
   environment and today's.
3. **Timeline.** One row per human prompt, with the injected messages that preceded it:

   | Turn | Line | Time (user zone / UTC) | Request (one line) | Events |
   | --- | --- | --- | --- | --- |

   Events lists skills invoked, subagents dispatched, compactions, errors and retries, resumes,
   injected instructions acted on, and the claims the turn ended with.
4. **Findings.** One subsection per examined dimension, leading with those that answer the
   user's question. Each gives its status, the range examined and its findings in the
   [finding format](#finding-format). A dimension with nothing to report says
   `NOT_OBSERVED_IN_SCOPE — checked: <what>` or `UNKNOWN — missing: <what>`.
5. **Cost and time.** The usage semantics in one sentence (per response or cumulative; repeated
   records counted once); totals per session with each counter; records without usage and that
   the total is a lower bound; the five largest responses or turns; the ten largest tool
   results; the span; every gap over ten minutes with what the records show it was or "not
   shown in the records"; compactions with their counters; subagents with usage and duration.
   Show inputs for every derived number. No prices unless the source records them.
6. **Involvement.** For each skill, hook, plugin or tool in play: `not indicated`, `possible`
   or `likely`, with its lines. State involvement only; no defect, no fix. When possible or
   likely, mention the issue step.
7. **Coverage and next check.** Ranges and files not read and why; fields unavailable;
   whether the session was in progress; claims the user should double-check. When one bounded
   check could change the verdict, name the evidence and what it would settle.
8. **Export** (only when requested). Bundle path, level, file list, privacy outcome and evidence
   outcome on separate lines.
9. **Similar sessions** (only when requested). One row per candidate: id, path, date, matched
   markers, missed markers.

## Finding format

```text
- finding: <one sentence, what happened>
  evidence: <path>:<line> - "<quote, at most 200 characters, secrets replaced>"
  turns: <first>-<last>
  confidence: high | medium | low
```

Derived numbers name their inputs: "41,250 = 12 + 8,100 + 32,600 + 538 (input, cache
creation, cache read, output; lines 4-90, one count per response id)".

## Worked report

The anchors below refer to this synthetic, complete excerpt of a session log.

```text
1 human: Use the accepted plan. Read plan.md before editing.
2 tool: read plan.md -> timeout
3 tool: read plan.md -> success, hash abc
4 agent: checkpoint recorded successful read, hash abc
5 host: context compacted
6 tool: read plan.md -> success, hash abc
```

**Verdict.** Yes, the session repeated completed work once: plan.md was read successfully at
line 3 and again at line 6 with the same content (confidence high). Why it re-read is not shown
in the records; the compaction at line 5 is the only event between the reads (confidence in
the cause: low). (`session.log:3`, `session.log:5`, `session.log:6`)

**Problem statement and scope.** The human asked for one plan read before editing
(`session.log:1`); the question is whether the extra read repeated completed work. Range
`session.log:1-6`, complete; no other candidate session.

**Timeline.**

| Turn | Line | Time | Request | Events |
| --- | --- | --- | --- | --- |
| 1 | 1 | not recorded | Use the accepted plan; read plan.md first | timeout (2), retry (3), checkpoint (4), compaction (5), re-read (6) |

**Findings.**

Repeated work — `OBSERVED`, lines 2-6.

```text
- finding: plan.md was read successfully twice with unchanged content, the second read after a compaction
  evidence: session.log:6 - "read plan.md -> success, hash abc"
  turns: 1-1
  confidence: high
```

The read at line 3 is a retry after the timeout at line 2, not waste.

Stumbles — `OBSERVED`, line 2: a timeout, recovered at line 3 in the same turn.

**Cost and time.** `UNKNOWN`: the excerpt has no usage or timestamp fields.

**Involvement.** Compaction (host): `possible` — it is the only event between the two
successful reads (`session.log:5`).

**Coverage and next check.** Lines 1-6 read in full. If an authorized post-compaction context
record exists, check whether it carries the checkpoint from line 4: that separates a lost
checkpoint from a repeat despite the checkpoint.

Adapted from obra/superpowers `diagnosing-superpowers` (b739a8a, MIT): the report template and
finding format.
