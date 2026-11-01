# Method Authoring — Forwarding Guide

Internal method ID: `andino-method-authoring` (forwarding to `andino-skill-maker`).

This guide forwards legacy `method-authoring` invocations to canonical
`andino-skill-maker`.

## Resource resolution

Resolve canonical authoring craft using the active layout:

- **Nested layout** (`skills/` within an `andino-workflow` checkout):
  - Operational contract: `../skill-maker/SKILL.md`
  - Craft guide: `../skill-maker/GUIDE.md`
  - Schemas and pressure cases: `../skill-maker/resources/contract.md`
- **Native layout** (flat `skills/` or standalone sibling packages):
  - Operational contract: `../andino-skill-maker/SKILL.md`
  - Craft guide: `../andino-skill-maker/GUIDE.md`
  - Schemas and pressure cases: `../andino-skill-maker/resources/contract.md`

Select the containing package structure first. Explicit layout instructions avoid
broken unconditional relative markdown links across different installation styles.

Refer to the canonical guide for dual-mode authoring (remedial vs greenfield),
runbook/procedure support, matched control/candidate evaluation, fresh-context
testing, and NOT_VERIFIED fallbacks when model evaluators are unavailable.
