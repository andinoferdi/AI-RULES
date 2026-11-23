# Question types: where to look and when to stop

Load at step 2 to choose sources, the evidence that counts and the stop rule.
The rows are handles, not a checklist: a question that fits two rows uses both,
and one that fits none uses the closest row's stop rule. Local evidence always
comes first (SKILL.md step 1).

## Technical questions

| Type | Where to look | What counts as evidence | Stop when |
| --- | --- | --- | --- |
| Library or tool choice | Package registries (npm, PyPI, crates.io, the project's ecosystem), official docs, release pages, skill and MCP catalogs, native platform features | Last release date, maintainers and activity, license, dependency weight, the specific feature match, fit with locked versions and runtime | 2–3 candidates have primary facts, or one candidate clearly meets the need and the adversarial check found no stop condition |
| Prior implementation | GitHub code search, maintained templates, skill and agent catalogs, this repository | The actual file read (source, SKILL.md, config) with path or URL | 2 actual files read, or 3 independent sources agree |
| Spec or official behavior | Official docs, specifications, `--help`, changelog, running it locally | Version and date of the source, the observed result | One version-stamped primary fact, or a local run on the locked version |
| Version-sensitive implementation | The [version contract](version-contract/guide.md) chain | Manifest + lockfile version, matching primary source section, parity test | The chain is complete, or the missing link is named |
| Reported problem or error | Maintainer issues and discussions, release notes, official error docs, community reports | Matching version and platform, maintainer reply, open/fixed/released status | A matching documented pattern with its fix release, or the next discriminating local check is named |

## General factual questions

| Type | Where to look | What counts as evidence | Stop when |
| --- | --- | --- | --- |
| Current events or news | Original reporting, official statements from the entity, wire services, Tier 2 publications | Publication date, named sources, whether outlets report independently or repeat one origin | Two independent Tier 1/2 sources agree, or the original statement is read |
| Regulation, law or policy | The official text from the issuing body (gazette, legislature, regulator), official guidance and FAQs | The text in force, its effective date, jurisdiction and any amendment | The official text in force and its date are read; commentary only explains it |
| Market, company or product facts | Company filings and official pages, pricing pages, regulator databases, Tier 2 analysis | As-of date, the entity's own statement versus third-party estimate, methodology for estimates | The entity's own current statement is read, or two independent estimates with stated methods are found |
| Statistics and data | The original dataset or statistical office, the study's methods section | The number, its unit, date, population and method; who produced it | The original source of the number is read, or the number is marked as untraceable |
| Claim in a paper or post | The primary text (paper, official blog, repository file) past the abstract | Subject, premises (data, scale, environment), kind of evidence, how our situation differs | Subject and premises are written down and what transfers is stated |
| State of practice | The rows above combined, plus first-person practitioner reports | Each item dated and sourced, the range of contexts covered | The next search would settle nothing you can name |
| Primary-source check | The full text a claim points at | The passage and its locator; per claim: supported, partial, unsupported or unverified | Every decision-relevant claim carries one of the four labels |

## Rules that apply to every row

- Query live sources at decision time. Recommendations, prices, versions and
  rules age; internal knowledge is a lead, not evidence.
- Record each search's terms, source and date as you go: Scope searched in the
  report is built from this record, including what was not located.
- Expand the search only for a named missing fact: change terms, shorten an
  overly specific query, try the exact error or the issuing body's own site.
- A stop rule met with Tier 3 sources only yields a Speculative or Emerging
  finding, not an Established one (see [source evaluation](source-evaluation.md)).
- When the stop rule cannot be met inside the available tools or time, stop,
  mark the answer PARTIAL or UNANSWERABLE and name the missing evidence.
