---
name: council
description: Analyze meaningful decisions through five independent advisors, anonymized peer review, and a synthesized recommendation. Use when the user explicitly asks for a council, war room, stress test, or multiple perspectives on a consequential choice, or when an actual high-stakes trade-off warrants structured scrutiny. Do not use for simple facts, routine yes-no questions, writing-only tasks, or ordinary summaries.
---

# Council

Council is a decision-analysis specialist inspired by [LLM Council](https://github.com/aiwithremy/claude-skills-llm-council) and Andrej Karpathy's [llm-council](https://github.com/karpathy/llm-council). It examines a real choice from five deliberately different angles, has the answers critiqued without revealing their authors, and produces a useful decision. A council is not a fact oracle, a substitute for verification, or automatic approval for action.

## Relationship to AI-RULES

- **Andino Workflow** retains scope, investigation, task routing, tool permissions, planning, implementation, verification, and durable checkpoints when active. Council returns a decision artifact and next action; it never creates a parallel lifecycle or changes an agreed scope on its own.
- **Focus** controls presentation. Resolve and activate an installed Focus skill through the host's authorized skill mechanism when available, and honor the full `A. PRIORITAS`, `human-language-indonesia.md`, and `human-language-english.md` references it provides. Reuse a valid active Focus context. Council does not replace or silently rewrite these references.
- Communicate in the user's language and register, normally Indonesian for an Indonesian request. Use natural active sentences, keep accurate detail and real disagreement, and avoid stock corporate phrasing. Explicit style and output requests outrank these defaults.
- If Focus is unavailable, apply those communication principles without claiming to have loaded it. A Council invocation does not grant agent access, external research access, or mutation rights.
- Council may be used without Andino. When Andino is active, give its coordinator the final recommendation, evidence/uncertainty and one practical next move. Do not schedule a second plan.

## When to convene

Use for a genuinely uncertain, material decision with alternatives and consequences, or when the user explicitly requests Council on such an issue. Recognize phrases such as "council this", "run the council", "war room", "pressure-test", "stress-test", "debatkan keputusan ini", or "bawa ke council" in context. Do not trigger just because an example or quoted document mentions these phrases.

Skip ordinary lookups, minor preferences, simple edits, pure drafting, and summaries. Do not turn every question beginning with "should I" into a committee meeting. If the user's request is mainly an immediate action, do that action unless they actually seek a deliberation.

## Context and brief

Identify the core decision, viable options, desired outcome, relevant limits, who is affected, and consequences.

Gather context in one bounded pass before framing. Read what the user named or attached, and the project instruction files (`AGENTS.md`, `CLAUDE.md` or equivalent) of the current project when they bear on the decision. Read other project files, prior decision records or authorized current sources only when they materially change the choice. Never read secrets, credentials or unrelated private files, and never pass personal or confidential details to advisors unless the decision needs them and the user's request covers sharing them. Record every source read for the run line.

Draft one neutral decision brief that every advisor receives unchanged. Include the options with the status quo when viable, numbered Option 1, Option 2 and so on so they never collide with the reviewers' Response letters. Add the criteria that separate them, what is at stake, and each material fact tagged [verified], [reported], [assumption] or [unknown] with its source. Do not put your preferred answer in it. If an indispensable preference cannot be inferred, ask one focused question; otherwise state a reasonable assumption and proceed.

## Five advisor lenses

1. **Contrarian** — strongest failure modes, hidden costs, opportunity cost, and disconfirming evidence.
2. **First Principles** — actual objective, foundational assumptions, and whether a different question or option solves the real problem.
3. **Expansionist** — realistic upside, overlooked opportunities, and second-order benefits.
4. **Outsider** — comprehension gaps, stakeholder perspective, and assumptions insiders take for granted.
5. **Executor** — feasibility, dependencies, reversibility, inexpensive tests, and the first executable step.

The lenses pull against each other in pairs (Contrarian against Expansionist, First Principles against Executor) while the Outsider checks the whole from outside. Each advisor argues its lens at full strength; balance is the chair's job. Full lens cards are in [references/prompts.md](references/prompts.md). Do not invent data, and do not manufacture dissent when evidence strongly favors one choice.

## Run plan and budget

Default composition: 5 advisors, 3 peer reviewers, and the main agent as chair. Use 5 reviewers only when the user asks for them or approves the larger budget.

- **Waves.** Advisors run before reviewers. Run at most 3 sub-agents at once, or fewer when the host, project or user sets a lower limit. The default run is three waves: 3 advisors, 2 advisors, 3 reviewers.
- **Models.** Choose the lowest tier the host exposes that handles the brief safely: a mid tier at medium effort for advisors, a mid or low tier at low effort for reviewers. Never use maximum effort, and never put every sub-agent on the strongest tier or on high effort.
- **Announcement.** Before the first dispatch, state the number of sub-agents, each wave's tasks, model and effort. When user or project rules require approval for sub-agents, wait for it. One approval can cover all announced waves; a change in count, model or effort needs a new one.
- **Failures.** Never relaunch a failed or stopped sub-agent without asking. Report which stage is missing and continue only with what actually ran.

## Conduct the council

1. **Load the prompts.** Read [references/prompts.md](references/prompts.md) before writing any advisor prompt. Every run, including the fallback, uses its templates.
2. **Independent round.** Dispatch each advisor with the advisor template, its lens card and the identical brief. Advisors never see each other's answers.
3. **Anonymize.** After all advisors finish, shuffle them to Responses A-E and record the mapping privately. Reviewers never see advisor names.
4. **Peer review.** Dispatch the reviewers with the reviewer template, the brief and all five anonymized responses. Each answers the three questions and ends with a `FINAL RANKING` line.
5. **Chair synthesis.** The main agent follows the chair checklist in [references/prompts.md](references/prompts.md): reveal the mapping only after all reviews, treat the ranking tally as a signal rather than proof, re-check decisive claims against their tags, prefer the stronger argument over the majority, and pick one first action.
6. **Present.** Follow the output contract.
7. **Persistence.** Keep transcripts in the conversation by default. Save one only when the user requests it or when the current authorized project workflow explicitly needs a durable artifact. Follow Andino's existing checkpoint/location when it owns the work.

See [references/worked-example.md](references/worked-example.md) for one complete run.

### Host and fidelity limits

Do not pretend multiple independent models or sub-agents ran when the host cannot launch them. Council runs **sub-agents with different lenses**, not necessarily different model providers. Distinguish independent delegation from a single model role-playing five lenses.

If parallel sub-agents are unavailable but sequential delegation works, keep prompts isolated and disclose the limitation. If no delegation is available, use the single-agent variant in [references/prompts.md](references/prompts.md) and label the result **single-agent perspective review**, not a completed independent council; deliver it only if the user's request permits a best-effort comparison. Never fabricate peer-review results or claim a tool ran when it did not.

When information is unverifiable, give conditional recommendations instead of false precision. When the user has asked for execution, Council's verdict is advice, not authority to modify files, spend money, publish, or perform other external actions.

## Output contract

Present the verdict in chat as Markdown with this layout, at the depth the decision warrants:

```markdown
## Council Verdict: {topic}
**Recommendation:** {the choice and the decisive reason, including why it beats the strongest alternative}

### Where the council agrees
### Where the council clashes
### Blind spots from review
### What would change the verdict
### First action
{exactly one concrete step}

_Run: {advisors, reviewers, model tier and effort, or single-agent perspective review}; context read: {sources}._
```

In Indonesian use: `Verdict Council`, `Rekomendasi`, `Titik temu`, `Perbedaan`, `Hal terlewat`, `Yang bisa mengubah verdict`, `Langkah pertama`, and `Jalannya council`. Keep disagreements that could change the choice, with the evidence or assumption behind each. Mark inference separately from verified evidence. When evidence is insufficient, say which condition favors each option.

Produce a report file only when the user asks for one. Include advisor or reviewer transcripts only when requested.

## Provenance

The five-advisor lenses, anonymous peer review and chairman synthesis are inspired by [aiwithremy/claude-skills-llm-council](https://github.com/aiwithremy/claude-skills-llm-council) by Ole Lehmann. The ranked peer review is inspired by Andrej Karpathy's [llm-council](https://github.com/karpathy/llm-council). Neither repository declares a license, so no text or code from them is reproduced here. This AI-RULES text is written independently for the Council, Focus and Andino Workflow contracts and is released under the [MIT license](references/legal/license.md).
