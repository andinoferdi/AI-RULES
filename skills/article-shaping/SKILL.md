---
name: andino-article-shaping
description: Use when an explicit writing request with existing raw material is ready to be shaped into an article or essay. Operates under Andino Workflow governance.
---

# Shape Raw Material into an Article

Internal method ID: `andino-article-shaping` (aliases: `article-shaping`, `writing-beats`, `writing-shape`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow protocol: single durable checkpoint, proportional investigation, anti-loop guards.
> Loading this file does not invoke another skill or mutate repository state. Upstream references yield to current policy.

## 1. Dominant Negative Gates (When NOT to Use)

Reject shaping immediately if ANY condition holds:
- **Open Fragment Exploration**: Raw, unformed thoughts without intention to structure belong to [raw-capture](resources/raw-capture/guide.md).
- **Direct Source Mutation**: Never edit, truncate, or overwrite the author's raw notes file in place.
- **Evidence Fabrication**: Never invent lived anecdotes, synthetic statistics, or fake quotes when material is missing.
- **Automatic Publishing**: Never push or publish completed copy without explicit author review and authorization.

## 2. Operational Pacing Router

| Mode | Trigger Condition | Operational Protocol |
| :--- | :--- | :--- |
| **Mode A: Interactive CYOA** (Default) | Standard article shaping from raw notes or transcripts. | **One Beat at a Time**: Agree on hook -> propose 2-3 reachable next beats -> write agreed beat to disk -> re-read disk -> repeat. |
| **Mode B: Cohesive Cluster** | Author explicitly requests rapid drafting or section flow. | **Functional Slice**: Draft cohesive 2-3 beat section -> verify grounding invariants -> write section to disk -> pause for critique. |

## 3. The 5 Floor Invariants

1. **Iron Law of Non-Mutation**: The raw source file is read-only. The shaped article lives exclusively in a separate destination file.
2. **Grounding Invariant**: A claim or beat cannot introduce cognitive friction by using a concept before it has been grounded.
3. **Single Job per Beat**: Every beat executes exactly one rhetorical move (`scene`, `claim`, `question`, `aside`, `pivot`, or `payoff`).
4. **Zero Fabricated Evidence**: When lived details or metrics are missing, name the gap explicitly (`[GAP: ...]`); never invent facts.
5. **Durable Disk Checkpoint**: Commit agreed beats to disk incrementally before proposing next moves; never write ahead in memory.

## 4. Anti-Rationalization Refutations

| Rationalization Shortcut | Mechanical Reality & Required Response |
| :--- | :--- |
| *"I will write the entire draft at once to save turns."* | Writing long batch drafts causes regression to the mean and bland AI slop. Draft beat-by-beat or in small clusters. |
| *"The author won't notice if I invent a small anecdote."* | Fabricated stories destroy trust and violate epistemic grounding. Name the gap and demand the real example. |
| *"I don't need to write to disk until the whole article is done."* | Uncommitted drafts are vulnerable to context compaction and session loss. Write each agreed beat to disk immediately. |
| *"A negative rule ('never use slop') is enough to ensure quality."* | Prohibitions backfire on shaping. Use the ruthless editor questions and active sentence cadence in [grilling protocol](resources/grilling-and-cadence-protocol.md). |
| *"Technical DAG terms explain grounding best to the user."* | Jargon causes cognitive friction. Speak natural editorial language; enforce mathematical grounding under the hood. |

## 5. Diagnostic Red Flags (Stop Immediately)

1. Overwriting or modifying the raw input source file.
2. Drafting multiple downstream sections into the article file before the author selects an opening hook.
3. Inventing synthetic company names, metrics, or personal experiences not found in the raw material.
4. Continuing to write ahead when an ungrounded concept or weak logical transition has been detected.
5. Using corporate throat-clearing, symmetric triads, or passive drone wrap-ups.

## 6. Progressive Disclosure Router

- Complete master craft guide: [GUIDE.md](GUIDE.md)
- Formal schemas, reachability states, and invariants: [resources/contract.md](resources/contract.md)
- Ruthless editor interrogation and cadence engineering: [resources/grilling-and-cadence-protocol.md](resources/grilling-and-cadence-protocol.md)
- Concept grounding DAG, reachability rules, and gap naming: [resources/concept-grounding-graph.md](resources/concept-grounding-graph.md)
- Visual format debates and anti-slop banned index: [resources/format-tradeoffs-and-anti-slop.md](resources/format-tradeoffs-and-anti-slop.md)
- 3-hook generation engine, 6 beat types, and 4 narrative curves: [resources/beat-progression-and-hooks.md](resources/beat-progression-and-hooks.md)
- End-to-end worked example and verification harness: [resources/worked-example.md](resources/worked-example.md)
- Unstructured raw fragments intake: [resources/raw-capture/guide.md](resources/raw-capture/guide.md)

## 7. Runnable Operational Contract & Verification Harness

```python andino-operational-example
import json, os, sys

negative = os.environ.get("ANDINO_NEGATIVE", "0") == "1"

grounded = {"request"}
beats = {
    "1_scene": {"requires": {"request"}, "grounds": {"error_state"}},
    "2_claim": {"requires": {"request", "error_state"}, "grounds": {"core_concept"}},
    "3_pivot": {"requires": {"core_concept"}, "grounds": {"breakthrough"}}
}

if negative:
    beats["2_claim"]["requires"] = {"request", "ungrounded_leap"}

for b_id, b_data in beats.items():
    if not b_data["requires"].issubset(grounded):
        sys.exit(1)
    grounded.update(b_data["grounds"])

print(json.dumps({"valid": True, "status": "CONTRACT_VERIFIED", "grounded": sorted(grounded)}))
sys.exit(0)
```

## 8. Provenance

Independently adapted from audited local snapshot paths under MIT license ([references/license.md](references/license.md)):
- `mattpocock/skills:skills/in-progress/writing-beats` (Matt Pocock 2026)
- `mattpocock/skills:skills/in-progress/writing-shape` (Matt Pocock 2026)
