---
name: council
description: Analyze meaningful decisions through five independent advisors, anonymized peer review, and a synthesized recommendation. Use when the user explicitly asks for a council, war room, stress test, or multiple perspectives on a consequential choice, or when an actual high-stakes trade-off warrants structured scrutiny. Do not use for simple facts, routine yes-no questions, writing-only tasks, or ordinary summaries.
---

# Council

Council is a decision-analysis specialist inspired by [LLM Council](https://github.com/aiwithremy/claude-skills-llm-council). It examines a real choice from five deliberately different angles, critiques the answers without identifying their authors, and produces a useful decision. A council is not a fact oracle, a substitute for verification, or automatic approval for action.

## Relationship to AI-RULES

- **Andino Workflow** retains scope, investigation, task routing, tool permissions, planning, implementation, verification, and durable checkpoints when active. Council returns a decision artifact and next action; it never creates a parallel lifecycle or changes an agreed scope on its own.
- **Focus** controls presentation. Resolve and activate an installed Focus skill through the host's authorized skill mechanism when available, and honor the full `A. PRIORITAS`, `human-language-indonesia.md`, and `human-language-english.md` references it provides. Reuse a valid active Focus context. Council does not replace or silently rewrite these references.
- Communicate in the user's language and register, normally Indonesian for an Indonesian request. Give the conclusion first when useful, use natural active sentences, keep accurate detail and real disagreement, and avoid stock corporate phrasing. Explicit style and output requests outrank these defaults.
- If Focus is unavailable, apply those communication principles without claiming to have loaded it. A Council invocation does not grant agent access, external research access, or mutation rights.
- Council may be used without Andino. When Andino is active, give its coordinator the final recommendation, evidence/uncertainty and one practical next move. Do not schedule a second plan.

## When to convene

Use for a genuinely uncertain, material decision with alternatives and consequences, or when the user explicitly requests Council on such an issue. Recognize phrases such as "council this", "run the council", "war room", "pressure-test", "stress-test", "debatkan keputusan ini", or "bawa ke council" in context. Do not trigger just because an example or quoted document mentions these phrases.

Skip ordinary lookups, minor preferences, simple edits, pure drafting, and summaries. Do not turn every question beginning with "should I" into a committee meeting. If the user's request is mainly an immediate action, do that action unless they actually seek a deliberation.

## Evidence and framing

Identify the core decision, viable options, desired outcome, relevant limits, who is affected, and consequences. Consult relevant user-supplied materials, established project context, and authorized current sources only when they materially affect the choice. Never search unrelated private files or send confidential material to unauthorized agents/services. Preserve user-stated priorities and distinguish verified facts, reported claims, assumptions, and unknowns.

Draft one neutral, shared decision brief for all advisors. Include the status quo when viable, the criteria that distinguish the options, and the source and limits of material evidence. Do not place your preferred answer inside it. If an indispensable preference cannot be inferred, ask one focused question; otherwise state a reasonable assumption and proceed.

## Five advisor lenses

Each advisor sees the same brief and works independently, without other advisors' responses.

1. **Contrarian** — strongest failure modes, hidden costs, opportunity cost, and disconfirming evidence. Critique the idea, not the person.
2. **First Principles** — actual objective, foundational assumptions, and whether a different question or option would solve the real problem.
3. **Expansionist** — realistic upside, overlooked opportunities, second-order benefits, and what could scale if conditions hold.
4. **Outsider** — comprehension gaps, stakeholder perspective, assumptions insiders take for granted, and external effects.
5. **Executor** — feasibility, dependencies, constraints, reversibility, inexpensive tests, and the first executable step.

Do not force consensus, invent data, or manufacture opposing views when evidence strongly favors one choice.

## Conduct the council

1. **Independent round.** On hosts that permit genuine parallel sub-agents, dispatch the five advisor lenses independently and concurrently. Provide the exact same neutral decision brief. Each gives a specific, reasoned judgment (about 150-300 words for substantial decisions). Ask each advisor for a preferred option, its strongest reason tied to the brief, the most consequential downside, and an observation that would change the choice. Mark assumptions and missing evidence explicitly. Prevent cross-contamination between advisor responses. Respect authorized concurrency limits by running isolated waves.
2. **Anonymous peer review.** After collecting all five outputs, consistently shuffle their identifiers to Responses A-E; do not expose names to reviewers. Dispatch independent peer reviewers, preferably in parallel. Give reviewers the original brief and anonymized responses. Each identifies the strongest response against the decision criteria, challenges a consequential claim or assumption against the available evidence, and flags any shared blind spot. Explain whether the challenge changes the ranking and why. Keep each review focused (about 200 words maximum).
3. **Chair synthesis.** Combine the decision brief, all responses and all peer reviews. Identify (a) where reasoning converges, (b) material disagreements and the assumptions behind them, (c) blind spots exposed in review, (d) a justified recommendation, and (e) **one** concrete first action. The chair may reject a majority view when another position has stronger evidence. Explain why the recommendation beats its strongest viable alternative on the criteria that matter. When evidence is insufficient, state which condition favors each option and name the observation that would resolve the choice. Agreement alone is not proof.
4. **Present.** Follow the output contract below.
5. **Persistence.** Keep transcripts in the conversation by default. Save one only when the user requests it or when the current authorized project workflow explicitly needs a durable artifact. Follow Andino's existing checkpoint/location when it owns the work.

### Host and fidelity limits

Do not pretend multiple independent models or five sub-agents ran when the host cannot launch them. The original method may run five **sub-agents with different lenses**, not necessarily five different model providers. Distinguish independent delegation from a single model role-playing five lenses.

If parallel sub-agents are unavailable but independent delegation is supported sequentially, keep advisor prompts isolated and disclose the execution limitation. If no delegation is available, label the result **single-agent perspective review**, not a completed independent council; deliver a useful best-effort comparison only if permitted by the user's request. Never fabricate anonymous peer-review results or claim a tool ran when it did not.

When information is unverifiable, use conditional recommendations instead of false precision. When the user has asked for execution, Council's verdict is advice, not authority to modify files, spend money, publish, or perform other external actions.

## Output contract

Default to Markdown in chat. Produce a report file only when the user requests that deliverable. The persistence rule governs any separate transcript required by the project workflow.

Open with the recommendation and the decisive reason. Then cover the following at the depth the decision warrants:

- **Trade-offs.** Explain where the strongest alternative wins and what makes the preferred option better under the stated priorities.
- **Agreement and dissent.** Preserve disagreements that could change the choice and identify the evidence or assumptions behind them.
- **Uncertainty.** Surface review findings that matter. State what would change the verdict and distinguish verified evidence from inference.
- **First action.** Give exactly one concrete step that tests the deciding assumption or advances the recommended choice.

Use short headings and bullets when they help scanning. Match the user's language and requested format. Include advisor or reviewer transcripts only when requested.

## Provenance

The core five-advisor and anonymous-review concept is inspired by [aiwithremy/claude-skills-llm-council](https://github.com/aiwithremy/claude-skills-llm-council) and its attribution to Ole Lehmann and Andrej Karpathy. This AI-RULES text is independently written for the Council/Focus/Andino Workflow contracts; it does not reproduce the upstream SKILL.md or assert an upstream license.
