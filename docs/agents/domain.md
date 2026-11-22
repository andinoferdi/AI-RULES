# Domain docs

Before changing a skill, the installer or a check, read the root `CONTEXT.md`
glossary and the decisions in `docs/adr/`. Use its terms (skill branch, pin,
promote, drift) in specs, PR titles, commit messages and test names.

| Need | Document |
| --- | --- |
| How a skill change reaches main and users | [specs/skill-promotion.md](../specs/skill-promotion.md) |
| Why main pins skill versions | [adr/0001](../adr/0001-main-pins-skill-versions.md) |
| Dated owner decisions | [DECISIONS.md](../DECISIONS.md) |
| Unresolved questions | [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md) |
| What CI proves | [ci-coverage.md](../ci-coverage.md) |

Flag a conflict with an ADR in the PR instead of silently overriding it. Record a
new ADR only when a real decision is resolved; add an unresolved one to
`OPEN-QUESTIONS.md` and pick the safest behavior meanwhile.
