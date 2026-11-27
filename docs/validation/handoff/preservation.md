# Preservation ledger: andino-handoff rewrite

Every rule of the old skill (AI-RULES main at 1e78323) and where it lives now. "SKILL"
means `skills/andino-workflow/skills/handoff/SKILL.md` (GUIDE.md carries the same body).

| Old rule | Old place | New place |
| --- | --- | --- |
| Continue in place when the same context can take the next step | Procedure 1 | SKILL, Procedure 1, first question of the boundary table |
| Identify the recipient's assignment, destination and authorized scope | Procedure 1 | SKILL, Procedure 2 |
| Lead with the authoritative checkpoint; link spec, code, evidence | Procedure 2 | SKILL, Procedure 5 and Output "Read first"; Rules "One progress record" |
| Destination-relative paths with a named root | Procedure 2 | SKILL, Procedure 6 (resolve every path from the recipient's root) |
| Preserve reasons for decisions, including rejected approaches | Procedure 2 | SKILL, Procedure 5; Rules "Reasons travel with decisions"; Output "Decisions that must hold" |
| Record branch, base revision, staged / unstaged / untracked | Procedure 3 | SKILL, Procedure 3; Output "Current state and evidence" |
| Bytes only on the source host: name them, obtaining them is the first action | Procedure 3 | SKILL, Procedure 4 (with bundle and patch commands); Output "Before you start" |
| Non-repository work: document revision or other observable state | Procedure 3 | SKILL, Fallback |
| Separate observed results, pending checks and assumptions | Procedure 4 | SKILL, Procedure 3 and Rules "Facts carry their source" |
| Redact credentials, private data, session tokens | Procedure 4 | SKILL, Procedure 5 and Rules "Secrets never travel" |
| Suggested methods use internal IDs, conditional on availability | Procedure 4 | SKILL, Output "Suggested skills" |
| Check from the destination: first pointer, revision, access, first action's signal | Procedure 5 | SKILL, Procedure 6 |
| Label access you could not check | Procedure 5 | SKILL, Fallback (recipient's root not reachable) |
| Durable storage for cross-host use | Procedure 5 | SKILL, Procedure 7 (location by recipient) |
| Deliver with location and first action; no automatic continuation without authority | Procedure 6 | SKILL, Procedure 7 and Ownership and permission boundary |
| Keep summary text out of shell commands | Procedure 6 | Dropped: the skill no longer passes summaries to any command; delivery is a file |
| On receipt: compare state with baseline, recheck only invalidated evidence, resume, update checkpoint | Procedure 7 | SKILL, Procedure 8 |
| Output sections: Resume here, Current state and evidence, Decisions and boundaries, NEXT ACTION | Outputs | SKILL, Output template (Read first, Current state and evidence, Decisions that must hold, Open questions and boundaries, NEXT ACTION) |
| When blocked: who unblocks, missing input, condition to resume | Outputs | SKILL, Output "Open questions and boundaries"; worked example, third case |
| Anti-patterns: unverified done, duplicate plan, vanished temp pointers, automatic new host or task | Example and anti-patterns | SKILL, Red flags, Shortcuts, Procedure 7 |
| Fallback: file-based handoff when host continuation is unavailable | Fallback | SKILL, Fallback |
| Context-packing: four intake questions | context-packing/contract.md | context-packing/guide.md, "Start from four answers" |
| Context-packing: hierarchy and recency ordering | contract.md, guide.md | context-packing/guide.md, "Load from stable to changing" |
| Context-packing: noise sanitisation (traces, cascades, diffs) | contract.md, context-budget-and-packing.md | context-packing/guide.md, "Cut first" |
| Context-packing: untrusted data stays data | contract.md, confusion-and-ambiguity-protocols.md | context-packing/guide.md, "Trust what you load accordingly"; SKILL Rules |
| Context-packing: compress before dropping | context-budget-and-packing.md | context-packing/guide.md |
| Context-packing: rules-file templates for several hosts | rules-file-catalog.md | Removed: owned by `andino-agent-document-authoring` |
| Context-packing: A/B/C ambiguity triage and inline planning | confusion-and-ambiguity-protocols.md | Removed: owned by `andino-brainstorming` and `andino-planning` |
| Context-packing: softmax formula, "70% heuristic", placement "laws" | guide.md, context-budget-and-packing.md | Removed: no instruction depends on them |
| Context-packing: payment race worked example and test suite | resources/worked-example.md | Replaced by the compaction instruction and subagent brief examples in the guide |
