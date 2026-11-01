# Decision Interview (Consolidated into Brainstorming)

Internal method ID: `andino-decision-interview` (alias: `decision-interview`).

---

## 1. Consolidation Notice

As part of the 2026-11-01 elevation of Andino Workflow's discovery capabilities, `decision-interview` has been unified with `brainstorming` to form a comprehensive discovery, grilling, and decision refinery engine under [`skills/brainstorming/`](../brainstorming/).

All upstream capabilities from:
- `addyosmani/agent-skills:skills/interview-me`
- `mattpocock/skills:skills/productivity/grilling`
- `mattpocock/skills:skills/productivity/grill-me`
- `mattpocock/skills:skills/engineering/grill-with-docs`
- `obra/superpowers:skills/brainstorming`

now operate canonically through [`andino-brainstorming`](../brainstorming/SKILL.md).

---

## 2. Delegation & Routing Protocol

When a user, task, or coordinator activates `decision-interview`:
1. Delegate execution directly to the canonical operational contract: [`skills/brainstorming/SKILL.md`](../brainstorming/SKILL.md).
2. Follow the 4-phase procedure:
   - Intent Hypothesis & De-buzzwording (`<70%` confidence trigger).
   - Friction-proportional Three-Path Scoping (Spike, Bounded, Architectural).
   - Relentless DAG Frontier Grilling with Reasoned Defaults.
   - Lazy In-Flight ADR & Domain Glossary Synthesis with 3-Question Predictability Termination.
3. Consult the canonical craft guide: [`skills/brainstorming/GUIDE.md`](../brainstorming/GUIDE.md).

---

## 3. Catalog Compatibility

`andino-decision-interview` remains registered in the 59-member Andino skill catalog as an active forwarding alias to preserve zero-breakage backward compatibility for external callers, historical execution plans, and automated tooling.
