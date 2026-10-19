---
name: natural-writing
description: Write, rewrite or review prose in Indonesian and English so it reads naturally, fits its audience and register, and keeps its meaning, facts and required depth. Use for requested writing artifacts such as essays, articles, reports, emails, documentation prose and academic sections, or when the user asks to polish, paraphrase or review writing quality. Not for routine chat answers, progress updates, code, machine-readable output, research validity or task orchestration.
license: MIT
---

# Natural Writing

Make requested prose clear, natural and appropriate to its reader without changing
what it says. Quality means accurate meaning, fitting register, logical flow and
complete coverage, not the absence of particular words or the appearance of
human authorship.

## When to use

Use when the user wants a writing artifact produced, improved or assessed:
essays, articles, reports, proposals, academic sections, emails and letters,
documentation prose, summaries written as deliverables, or explicit requests to
rewrite, paraphrase, polish, proofread or review writing. An explicit request for
this skill also selects it.

Do not use for ordinary conversational answers, status updates or completion
reports, code and CLI output, JSON/YAML or other machine-readable formats,
statistical computation, pure lookup, or repository work unrelated to prose. A
skill name appearing in quoted text, a filename or an example is not a request.

## Ownership

| Component | Owns |
| --- | --- |
| Natural Writing | Prose quality inside writing artifacts: wording, register, cohesion, terminology consistency, meaning-preserving edits |
| Focus, when active | The surrounding communication with the user: progress, explanations, completion reports |
| Domain specialists (for example skripsi-skill) | Subject validity, evidence standards, methodology, institutional requirements |
| Andino Workflow, when active | Routing, lifecycle, planning, verification and final acceptance |

Natural Writing owns no research authority, source verification, statistical
interpretation, code behavior, Git permission or task lifecycle. It requires no
other skill and starts no plan of its own.

## Communication versus artifact

Classify text by its purpose, not by where it appears. An essay, chapter, email
draft or report written directly in chat is an artifact; a short note about that
document is communication. One response can contain both; each part follows its
own contract.

The artifact's requirements decide its length, structure and depth: the user's
request, accepted decisions, genre conventions, institutional rules and domain
methods. Conversational preferences (answer-first openings, short replies, few
bullets) never justify truncating, summarizing or flattening required artifact
content.

When rules conflict inside an artifact, apply this order:

1. Host permissions and higher-priority instructions.
2. Explicit user instructions and accepted decisions.
3. Correctness, factual integrity and protected content.
4. Domain, institutional and technical requirements.
5. Requested structure, scope and completeness.
6. Natural Writing's prose improvements.

## Modes

Infer the mode from the request; ask only when the choice changes the outcome.

**Write.** Establish audience, document type, language, register, purpose, required
structure and the available source material. Produce the complete artifact. Use
only supplied or verified facts; never invent data, citations, quotations, people,
experiences or conclusions. When information is missing, say so or use a clearly
marked placeholder such as `[source needed]`.

**Rewrite.** Improve clarity and naturalness while preserving claims, qualifications,
facts, numbers, citations, terminology, logical relations, accepted structure,
authorial voice and depth. Do not shorten unless asked. Never turn correlation
into causation, a hypothesis into a finding or uncertainty into certainty. If a
claim looks wrong, flag it; do not silently correct it. Meaning outranks elegance.

**Review.** Assess without changing the original unless asked. Report prioritized
findings with the excerpt or line, why it matters and a concrete suggestion.
Cover clarity, naturalness, repetition, paragraph progression, terminology,
register, redundancy, ambiguous reference, unsupported specificity and grammar.
Skip trivial cosmetic noise.

## Protected content

Keep these exactly unless the user explicitly authorizes a change:

- Code, commands, API names, identifiers, file paths, JSON/YAML keys.
- Formulas, measurements, dataset values, numerical tables, statistics.
- Exact quotations and source passages.
- Citations, bibliographic records, URLs and DOIs.
- Legal or compliance text that must stay verbatim.
- User-approved terminology and research decisions.

## Load the right reference

Read only what the current task needs, relative to this skill's folder:

- Indonesian text: [indonesian-writing.md](references/indonesian-writing.md).
- English text: [english-writing.md](references/english-writing.md).
- Mixed text: both language references, for the relevant portions.
- Academic or research prose: [academic-writing.md](references/academic-writing.md).
- Rewrite or Review mode: [editing-and-review.md](references/editing-and-review.md).

Reuse references already loaded in context. Reading a file is not proof that
the skill was natively activated; report activation only as observed.

## Style principles

- Revise a pattern only when it actually harms clarity, flow, accuracy or fit.
  Lists of overused phrases are diagnostic hints, never global bans. A word that
  is precise, standard in the discipline, required by a source or requested stays.
- No quotas: no fixed sentence lengths, alternating rhythms, punctuation limits,
  bans on groups of three, deliberate errors or random informality. Punctuation
  such as dashes follows the project, style guide or genre.
- Prefer active voice when it is clearer; keep passive voice when the actor is
  unknown, irrelevant or conventionally omitted, as in many methods sections.
- Preserve the author's register and conventions; do not invent opinions,
  anecdotes or personal traits. Without samples, choose a neutral register that
  fits the task.
- Keep certainty calibrated: observation, association, prediction, inference,
  hypothesis and causal conclusion stay distinct.

## Detector claims and integrity

Optimize for genuine quality, not detector evasion. Never promise human-sounding
results, detector bypass, originality scores or percentages. Do not add errors,
fictional experiences, random noise or misleading paraphrase. When a request is
framed as "make it undetectable", offer legitimate editing and say what cannot be
promised. Respect academic authorship and AI-use disclosure rules.

## Verify before delivering

- Every protected element from the source is still present and unchanged.
- No new facts, numbers, citations or claims appear without a source.
- Certainty, limitations and attribution match the original.
- Required sections, coverage and depth are intact.
- Register and terminology are consistent throughout.

If a check cannot be completed (for example a source cannot be read), state the
limit in the surrounding communication and mark the affected text.

## Failure handling

When the source is missing, unreadable or contradictory, do not fill the gap with
invented content; report it and continue with what is supported. When a requested
change would alter meaning or integrity, explain the conflict and keep the
original meaning unless the user confirms otherwise.

Original AI-RULES work under the [MIT license](references/license.md).
