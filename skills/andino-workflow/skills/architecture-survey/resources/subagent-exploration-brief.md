# Exploration brief for a fresh-context explorer

Internal resource of `architecture-survey`. Read it when the user has approved a
fresh-context explorer for step 2 of the procedure, or when you explore inline and want the
same checks on your own findings.

## When an explorer helps

The parent agent carries the conversation, the user's preferences and its own early guesses,
and these bias what it notices. An explorer with a fresh context window meets the code the
way a new developer does: it feels the bouncing between small modules and the pass-through
calls instead of explaining them away.

Run an explorer only when the user approves it. Announce it first through the host's
delegation rules (`andino-delegation` under Andino Workflow): one explorer, its model and
effort, read-only. Without approval, explore inline with the same procedure and apply the
parent checks below to your own findings.

## Brief template

Fill the braces and send it as written.

```markdown
You are exploring a codebase for architectural friction. This is read-only work.

TARGET SCOPE: {{paths_and_the_reason_they_were_chosen}}
DOMAIN WORDS: {{terms_from_GLOSSARY.md, or "no glossary"}}
SETTLED DECISIONS: {{ADR titles from docs/adr/, or "no ADRs"}}

RULES
1. Read only. Do not write, edit, move or delete any file, and do not run git commands that
   change state.
2. Use these words in your own prose: module, interface, implementation, depth, deep,
   shallow, seam, adapter, leverage, locality. Do not substitute component, service, unit,
   API, boundary, layer or wrapper for them. Identifiers quoted from the code keep their names.
3. Every finding cites the file and the symbol or line it rests on.

WHAT TO LOOK FOR
Explore organically and note where you feel friction:
- Where does understanding one concept mean bouncing between many small modules?
- Where is a module shallow, its interface nearly as complex as its implementation?
- Where were pure functions extracted to be testable while the bugs hide in how callers use them?
- Where do coupled modules leak across their seams (transactions, clients, transport types)?
- Which parts are untested, or hard to test through their current interface?
- Where do several callers repeat the same sequence around a module, and do their copies differ?

For every suspect apply the deletion test: if the module were deleted, would complexity
vanish (a pass-through) or reappear across its callers (load-bearing, keep it)?

RETURN
A JSON array, one object per candidate, and nothing else:
[
  {
    "title": "Names the deepening, for example: Collapse the order intake pipeline",
    "recommendation": "Strong" | "Worth exploring" | "Speculative",
    "dependency_category": "in-process" | "local-substitutable" | "ports & adapters" | "true external" (list several when the candidate spans them),
    "files": ["exact/path/one.ts", "exact/path/two.ts"],
    "evidence": ["path/file.ts:symbol: what it shows"],
    "deletion_test": "concentrates" | "scatters",
    "problem": "One sentence: what hurts today.",
    "solution": "One sentence: the consolidation and where the seam goes.",
    "wins": ["6 words or fewer, in glossary terms"],
    "adr_conflict": "None" | "Contradicts ADR-NNNN because ...",
    "diagram_pattern": "mermaid" | "boxes-and-arrows" | "cross-section" | "mass" | "collapse"
  }
]
Also list modules you examined and kept, each with its deletion-test reason.
```

## Parent checks

When the explorer reports, and for your own inline findings:

1. **Paths:** every cited file and symbol exists in the repository. Drop a candidate whose
   evidence does not.
2. **Deletion test:** re-run it yourself. A candidate whose deletion scatters complexity
   across callers is a load-bearing module, not a candidate.
3. **Seams:** a proposed seam names two adapters; otherwise drop the seam or the candidate.
4. **Words:** prose that substitutes a banned word is rewritten before it reaches the report;
   quoted identifiers stay as they are.
5. **ADRs:** a candidate that contradicts an ADR keeps it only with concrete friction and an
   ADR callout.
