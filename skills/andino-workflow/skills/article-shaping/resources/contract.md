# Article Shaping Contract and Data Schema

Internal method ID: `andino-article-shaping/contract`.

This document specifies the authoritative data contracts, state representations, and invariant schemas governing `andino-article-shaping`.

---

## 1. Grounding Graph Schema

The concept grounding graph tracks reachability and prevents cognitive disorientation.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GroundingGraphState",
  "type": "object",
  "required": ["prerequisites", "grounded_concepts", "beats"],
  "properties": {
    "prerequisites": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Baseline concepts assumed to be understood by the target reader prior to reading."
    },
    "grounded_concepts": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Cumulative set of concepts grounded by approved beats up to the current turn."
    },
    "beats": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/BeatContract"
      }
    }
  },
  "definitions": {
    "BeatContract": {
      "type": "object",
      "required": ["id", "type", "requires", "grounds", "pacing_delta", "status"],
      "properties": {
        "id": { "type": "string" },
        "type": {
          "type": "string",
          "enum": ["scene", "claim", "question", "aside", "pivot", "payoff"]
        },
        "requires": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Prerequisite concepts that must belong to grounded_concepts before this beat can be drafted."
        },
        "grounds": {
          "type": "array",
          "items": { "type": "string" },
          "description": "New concepts established and permanently grounded by this beat."
        },
        "pacing_delta": {
          "type": "string",
          "description": "The exact change produced in the reader's state (e.g., 'Skeptical -> Convinced')."
        },
        "status": {
          "type": "string",
          "enum": ["PROPOSED", "ACCEPTED", "COMMITTED_TO_DISK"]
        }
      }
    }
  }
}
```

---

## 2. Ingestion and Non-Mutation Contract

When ingesting raw notes, transcripts, or fragments:
- **Source Invariant:** The raw source file (`raw.md` or equivalent) MUST remain byte-for-byte unchanged. It is read-only.
- **Quarry Principle:** The raw material is treated as a quarry, not a sequential script. Material may be mined, split, paraphrased, or omitted.
- **Destination Isolation:** The shaped article is written exclusively to a separate destination file specified or confirmed by the author (`article.md`).

---

## 3. Operational Write and Persistence Contract

To guarantee resumability and resilience against context compaction or session interruptions:
1. **Single-Beat Disk Commit:** Only the currently agreed beat is written to the destination file.
2. **Never Write Ahead:** Generating multiple speculative beats in advance into the destination file without author agreement is strictly prohibited.
3. **Disk Pre-Read:** Before proposing the next beat candidates, the agent must re-read the destination file from disk to absorb any manual edits made directly by the author.
4. **Local Edit Isolation:** If the author requests changes to an earlier beat, edit only that specific section in place; never rewrite unrelated downstream beats unprompted.

---

## 4. Verification Oracle Contract

A shaped article satisfies acceptance if and only if:
1. `raw_preserved == True`: Source hash matches initial hash.
2. `all_beats_grounded == True`: For every beat $k$, $\text{requires}(\text{beat}_k) \subseteq G_{k-1}$.
3. `zero_slop == True`: Text contains no banned AI markers or throat-clearing openings.
4. `single_job == True`: Every beat executes exactly one rhetorical move.
5. `zero_hallucinated_evidence == True`: No ungrounded personal anecdotes or synthetic statistics.
