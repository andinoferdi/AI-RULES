# Format Tradeoffs and Anti-Slop Discipline

Internal method ID: `andino-article-shaping/format-tradeoffs-and-anti-slop`.

This resource details the format decision matrix for every content block and provides the authoritative anti-slop rules for eradicating generic AI prose.

---

## 1. Format Arguments to Have Out Loud

Never choose the visual container for a block silently. When drafting each section, weigh the structural tradeoffs explicitly:

| Format Choice | When to Choose | When to Avoid | Rationalization to Reject |
| :--- | :--- | :--- | :--- |
| **Prose vs. List** | Use **prose** to carry narrative, causal flow, and emotional momentum. Use **lists** only for truly parallel, scannable items. | Avoid turning dynamic arguments into laundry lists of bullet points. | *"Lists are easier to scan."* (Lists destroy argument momentum when items have causal dependencies.) |
| **Inline vs. Callout** | Use callouts (`> [!NOTE]`, `> [!WARNING]`) for crucial side caveats that would genuinely derail the main narrative arc if kept inline. | Avoid scattering callout boxes every two paragraphs; it fragments reading flow. | *"Callouts make it look modern."* (Excessive callouts make an essay read like software documentation.) |
| **Table vs. Repeated Structure** | Use a **table** when 3 or more entities share the exact same comparative attributes or schema. | Avoid tables for unstructured commentary or uneven comparisons. | *"Tables summarize things neatly."* (Tables kill narrative voice if used prematurely.) |
| **Quote vs. Paraphrase** | Use a **direct quote** when the original wording, colloquialism, or exact phrase is irreplaceable. | Avoid long rambling blockquotes when only a 3-word phrase carries the point. | *"Quotes add authority."* (Unnecessary blockquotes slow down the reader.) |
| **Code Block vs. Inline Code** | Use a **code block** for multi-line, runnable, or illustrative syntax. Use **inline code** (`foo()`) for single identifiers. | Avoid large code dumps that force the reader to parse irrelevant boilerplate. | *"Show the full script so they see it works."* (Show only the load-bearing lines.) |

---

## 2. The Anti-Slop Index (Banned Patterns)

Generic AI models default to predictable, formulaic tropes that signal synthetic text. In `andino-article-shaping`, these patterns are strictly banned:

### 1. Throat-Clearing Openings
- **Banned:** *"In today's fast-paced digital world..."*, *"It goes without saying that..."*, *"When it comes to building resilient systems, one must remember..."*
- **Correction:** Delete the preamble. Start on the physical action or the defensible claim immediately.

### 2. Predictable Symmetric Triads
- **Banned:** Grouping adjectives or nouns in rhythmic sets of three (*"diligence, dedication, and determination"*, *"scalable, robust, and resilient"*).
- **Correction:** Choose the single exact noun or verb that carries the freight. Kill the padding.

### 3. Sycophantic and Corporate Wrap-ups
- **Banned:** Ending an article with a recap of what was just said: *"In conclusion, by embracing these transformative paradigms, engineers can unlock unprecedented velocity..."*
- **Correction:** End on a punchline, an open challenge, a sharp boundary rule, or a memorable lasting insight.

### 4. Empty Intensifiers and Latinate Buzzwords
- **Banned:** *"leveraging"*, *"delve"*, *"tapestry"*, *"beacon"*, *"holistic"*, *"pivotal"*, *"seamlessly orchestrate synergies"*.
- **Correction:** Replace with concrete Anglo-Saxon physical verbs: *"using"*, *"cut"*, *"break"*, *"push"*, *"lock"*.

### 5. The Passive Drone
- **Banned:** *"It has been observed by multiple engineers that performance issues can be mitigated by..."*
- **Correction:** *"Teams that cache early cut latency in half."*
