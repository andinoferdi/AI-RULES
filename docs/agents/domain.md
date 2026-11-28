# Domain docs

Before changing a skill, the installer or a check, read the root `CONTEXT.md`
glossary and the decisions in `docs/adr/`. Use its terms (skill folder, local
source, GitHub source, native member) in PR titles, commit messages and test
names. Notes, plans and records stay out of the repository; see "What goes in the
repository" in [AGENTS.md](../../AGENTS.md).

| Need | Document |
| --- | --- |
| How to change, add or remove a skill | [specs/changing-skills.md](../specs/changing-skills.md) |
| Why skills live in `skills/` on main | [adr/0002](../adr/0002-skills-live-on-main.md) (supersedes [0001](../adr/0001-main-pins-skill-versions.md)) |
| Dated owner decisions | [DECISIONS.md](../DECISIONS.md) |
| Unresolved questions | [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md) |
| What CI proves | [ci-coverage.md](../ci-coverage.md) |

Flag a conflict with an ADR in the PR instead of silently overriding it. Record a
new ADR only when a real decision is resolved; add an unresolved one to
`OPEN-QUESTIONS.md` and pick the safest behavior meanwhile.
