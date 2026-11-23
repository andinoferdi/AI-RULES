# Product Marketing Context

**Document version:** v1
**Last updated:** 2026-11-23

## Product Overview
**One-liner:** Evidence-first skills for AI coding agents: done means proven.
**What it does:** Andino Skills installs a workflow (`andino-workflow` with 31 phase skills) and seven specialist skills into Claude Code, Codex, OpenCode and Antigravity. The agent finds the cause before changing code, writes tests first, researches before adopting a library, and does not claim "done" until every `Done when` point has passed a real check. English and Bahasa Indonesia are both supported.
**Product category:** Agent skills / skill collections for AI coding agents (same shelf as obra/superpowers, addyosmani/agent-skills, mattpocock/skills).
**Product type:** Open-source developer tool (skills + Python CLI installer + standalone binaries).
**Business model:** Free, MIT. The goal is reputation and adoption for Andino, not revenue.

## Target Audience
**Target users:** Developers who use AI coding agents daily and have been burned by an agent saying "done" when it was not. First ring: Indonesian developers and students (they get native Indonesian rules, `skripsi-skill` for thesis work, Indonesian writing guidance). Second ring: any English-speaking agent user.
**Primary use case:** Make an AI coding agent work like a careful senior engineer: diagnose, test, verify, then report with evidence.
**Jobs to be done:**
- "Stop my agent from inventing APIs, skipping tests and saying it's finished."
- "Give me one setup that works the same in every agent I use."
- "Let me prompt in Indonesian and still get rigorous engineering."
**Use cases:**
- Bug of unknown cause: `andino-debugging` finds the cause before any edit.
- Feature with tests: `andino-tdd` and `andino-verification`.
- Choosing a library: `search-first` (adopt, extend, compose or build).
- Costly decision: `council` (five advisors, anonymous peer review).
- Thesis (skripsi) work at an Indonesian campus: `skripsi-skill`.

## Problems & Pain Points
**Core problem:** AI coding agents sound confident. They report success without running anything, rewrite working code on a guess, use deprecated or invented APIs and repeat a failed approach.
**Why alternatives fall short:**
- Raw agents: no process at all.
- Large methodology packs: mostly English-only; Indonesian users translate their intent in their head.
- Copying rule files by hand: drifts per host and per machine.
**What it costs them:** Hours of re-checking, regressions shipped as "fixed", lost trust in the agent.
**Emotional tension:** "I can't tell if it actually works until I check everything myself."

## Competitive Landscape
**Direct:** obra/superpowers (~324k stars; "Evidence over claims", TDD, auto-triggering skills). Strong and established; Andino must not sound like a copy, so claim the mechanism (`Done when` contract, verification gate) and the bilingual layer.
**Direct:** addyosmani/agent-skills (~120k; lifecycle define-plan-build-verify-review-ship, slash commands). Strong lifecycle framing; English only.
**Direct:** mattpocock/skills (~330k; "Skills for Real Engineers", small and composable). Strong author brand and newsletter.
**Secondary:** Spec-driven frameworks (Spec-Kit, BMAD, GSD).
**Indirect:** Doing it by hand: reading every diff, writing long prompts.

## Differentiation
**Key differentiators:**
- A written `Done when` contract that the agent must prove point by point before reporting.
- Bahasa Indonesia as a first-class language: installer writes Indonesian defaults (`--defaults-language id`), `focus` ships a 41 KB Indonesian style guide, `natural-writing`, `skripsi-skill`.
- One native installer for five hosts with backups, rollback and health checks (`setup`, `update`, `doctor`).
- Credits upstream methods openly (Addy Osmani, Matt Pocock, Superpowers) and builds on them.
**Why customers choose us:** Same engineering rigor as the big packs, plus a proof contract you can read, plus your own language.

## Objections
| Objection | Response |
|-----------|----------|
| "Why not just use Superpowers?" | Use both ideas: Andino adapts its methods with credit. Pick Andino if you want the `Done when` contract, Indonesian support or one installer for five hosts. |
| "31 skills sounds heavy." | The workflow loads only the skill the current phase needs; the Minimal profile installs three. |
| "Python installer?" | Standalone binaries for Windows, macOS and Linux need no Python. |

**Anti-persona:** People who want the agent to "just vibe it" with no tests or checks.

## Switching Dynamics
**Push:** An agent said "fixed" and production broke.
**Pull:** A visible proof contract; Indonesian rules; one command setup.
**Habit:** Existing rule files and plugins in each host.
**Anxiety:** "Will it conflict with what I have?" Setup never overwrites hand-edited skills and keeps backups.

## Customer Language
**Words to use:** done when, proof, check, evidence, real engineering, selesai berarti terbukti.
**Words to avoid:** magic, superpower, 10x, revolutionary, seamless.
**Glossary:**
| Term | Meaning |
|------|---------|
| Done when | The completion criteria of a task; each needs a real check |
| Member skill | One of the 31 `andino-*` phase skills |
| Layer 1 / Layer 2 | Global defaults written once / the task prompt typed each time |

## Brand Voice
| Attribute | Means | Doesn't mean | Example line |
|-----------|-------|--------------|--------------|
| Plain | Short sentences, real commands | Hype | "Run `andino setup`, pick your host, start a new session." |
| Proof-first | Claims point to checks | Unmeasured promises | "The agent does not say done until every `Done when` point passes a real check." |
| Bilingual | Natural English and natural Indonesian | Literal translation | "Done means proven. / Selesai berarti terbukti." |
| Generous | Credit upstream by name | Hiding sources | "Adapts methods from Addy Osmani, Matt Pocock and Superpowers." |

**Terms we own:** "Done means proven", "Done when", "Selesai berarti terbukti".

## Proof Points
**Metrics:** None yet (0 stars at rebrand). Do not invent numbers.
**Value themes:**
| Theme | Proof |
|-------|-------|
| Proof before done | `andino-verification`: "Withhold completion while any required criterion lacks passing evidence." |
| Works across hosts | `setup` targets codex, claude-code, opencode, antigravity-cli, antigravity-ide |
| Indonesian first-class | `--defaults-language id`, `focus` Indonesian guide, `skripsi-skill` |

## Goals
**Business goal:** People recognize "Andino Skills" as Andino's work; grow GitHub stars and installs.
**Conversion action:** Star the repo, then run `andino setup`.
**Current metrics:** 0 stars, 0 forks (2026-11-23).

## Learnings
| Date | Learning | Evidence | Applies to | Status |
|------|----------|----------|------------|--------|
| 2026-11-23 | Lead with the `Done when` mechanism, not "evidence over claims"; Indonesian support is the second promise | Council run (5 advisors, 3 reviewers), 3 of 5 advisors and reviewer tally favoured proof-first | README, tagline, all launch copy | active |

## Changelog
- v1 (2026-11-23): Initial context for the AI-RULES to Andino Skills rebrand.
