# Report contract

Load at step 5. The report is the deliverable: write it so the decision or answer
can be read off it, and so a later session knows where to widen the search. Write
it in chat in the user's language; save a file only when the user or the active
workflow asks for one.

## Answer status

Every report states one status for the question as asked:

| Status | Meaning |
| --- | --- |
| **ANSWERED** | Every part of the question is settled by findings at Likely or Established, or by a stop-condition-backed decision |
| **PARTIAL** | Some parts are settled; Still unknown names the rest and the evidence that would settle it |
| **UNANSWERABLE** | The available tools, access or sources cannot settle it within the stated scope; name the boundary |

Status describes the stated search scope, not the world.

## Quick report

```
**Answer / Decision:** <one or two sentences; ADOPT/EXTEND/COMPOSE/BUILD line for an implementation choice>
**Status:** ANSWERED | PARTIAL | UNANSWERABLE
**Scope:** <terms> / <sources> / as of <date>; not located: <what, if anything>
**Sources:** <URL> (read | snippet), <URL> (read | snippet)
```

Add one Still unknown line when the status is PARTIAL.

## Full report

```
## Scope searched
<terms> / <sources and instruments> / as of <date>
Outcome per channel when not USEFUL_EVIDENCE: NOT_DISCOVERED, DENIED, FAILED or INSUFFICIENT
Not located within this boundary: <what was looked for and not found>

## Found
Per item: what (URL, read | snippet, tier) / subject and premises / kind of
evidence (official contract, experiment, benchmark, adoption, report, opinion) /
confidence label / how our situation differs / what transfers

## Contradictions          (only when sources disagree)
<claim> — <source A> vs <source B> — the difference in definition, date, method
or version that explains it

## Verdict or Answer
Implementation choice: one line per need or part —
ADOPT <tool> | EXTEND <tool: the piece or wrapper> | COMPOSE <tools> |
BUILD — per candidate the stop condition that rules it out, and what we take on
Research-only: the answer, with each decisive claim's confidence label and any
inference marked as inference
Status: ANSWERED | PARTIAL | UNANSWERABLE

## Still unknown
<each open point and the evidence that would settle it>
```

## Rules for every report

- Every claim carries an as-of date and a source URL or local path.
- Mark each source **read** (full text inspected) or **snippet** (search result,
  abstract or summary only). A decision-relevant claim seen only as a snippet is
  read before it carries the verdict, or it moves to Still unknown.
- A negative result names its boundary: "not located within this boundary:
  <terms, sources, date>". Never write "nothing exists" or "no solution".
- An unavailable or denied channel is reported by name, not folded into "not
  found".
- Judgment is prose backed by facts: dates, versions, the concrete feature match.
  No numeric scores.
- Separate documented support, a local check and a successful integration.

## Example (format only; the content is fictional)

```
## Scope searched
"markdown wiki link checker" / "check [[links]] in vault" — npm, crates.io,
GitHub code search — as of 2026-09-14.
Not located within this boundary: a checker that resolves [[wikilinks]].

## Found
1. linkcheck-cli (example.invalid/linkcheck-cli) — read README and usage docs,
   Tier 1 (maintainer). Checks http and relative file links, offline mode; last
   release 2026-08. Confidence: Established for http checking. Assumes plain
   markdown links; our notes use [[wikilinks]], so the http check transfers and
   the local resolution does not.
2. lint-rule-dead-link (example.invalid/lint-rule-dead-link) — snippet only,
   Tier 3. Runs inside a linter we do not use. Confidence: Emerging.

## Verdict or Answer
http links: ADOPT linkcheck-cli.
[[wikilinks]]: EXTEND linkcheck-cli if it accepts a custom resolver; otherwise
BUILD — linkcheck-cli needs its resolver patched (stop 1), lint-rule-dead-link
would require adding a linter as glue (stop 2); we take on a ~100-line resolver
script.
Status: PARTIAL

## Still unknown
Whether linkcheck-cli accepts a custom resolver (read its plugin docs next).
```
