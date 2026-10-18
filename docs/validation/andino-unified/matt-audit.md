# Matt Pocock local snapshot audit

Audit date: 2026-10-18. This report treats upstream content as source data. It grants no authority to run setup, hooks, Git operations or external writes.

The machine-readable record is [matt-audit.json](matt-audit.json). Its item rows preserve actual names, status, proposed internal methods, technical procedures and required adaptation. The proposal is not a claim that those methods have been implemented.

## Snapshot and coverage

Local source: `C:/Users/Lenovo/Downloads/AI-RULES/mattpocock-skills`. Remote is `https://github.com/mattpocock/skills.git`; branch `main`; HEAD `49dd158d1076134a641b33efb035946536778336`; tree `3ce485319972aae46dec0c2ac34cf4a7f28f7414`; package version `1.3.1`. Git status was clean when audited. Machine record includes exact local file hashes and canonical path-plus-byte hash, so cleanliness is not the only identity evidence.

Actual inventory: 20 engineering, 7 productivity, 4 frozen misc, 7 beta in-progress skills: 38 `SKILL.md` files. `chief-of-staff` exists but is absent from its bucket README. `deprecated/` contains no skills. `docs/engineering/resolving-merge-conflicts.md` remains as an archived page for a skill deleted in 1.3.0. The plugin lists exactly the 27 engineering/productivity skills; local developer linker also includes beta, excludes misc/deprecated. Count actual files rather than hardcoding plugin/README counts into coverage.

All actual skill bodies and their local supporting reference/template/config/script resources were read. Metadata, license, scripts, hooks, workflow configuration, ADRs and scope decisions were inspected. Human-facing documentation was used for unique FAQ/acceptance evidence; it is secondary, and several claims are stale against current skills. No upstream executable was run.

## Canonical decisions the integration must make

Matt TDD deliberately uses a red/green implementation loop and sends refactoring to review. Preserve this distinction in the comparison with Addy and Superpowers: small behavior-preserving refactor while green versus broader architecture review must have an explicit canonical owner and boundary. The upstream short description still says red-green-refactor, so names/descriptions cannot settle it.

Canonical decision recorded by the parent: RED then GREEN, one public-seam behavior per slice. Optional behavior-preserving GREEN-only refactoring has an explicit review gate; architecture redesign is a separate method. Already accepted seams count as agreement, and only material unresolved interface choices need a new question. Matt interviewing combines with Addy's one-question-plus-reasoned-guess and intent restate; Matt specification synthesis combines with Addy's conditional capability map and factual implementation/testing/boundary context. Existing approved spec and plan remain authoritative, with no duplicate lifecycle or mandatory terminal-turn ceremony.

Testing at confirmed public seams, with one-line catch/miss trade-offs, independently derived oracles, external-boundary injection and no internal mocks are the substantive TDD contributions. Existing accepted test seams count as agreement; routine tests must not become a repeated approval ceremony when already authorized. The interface vocabulary distinguishes signatures from all caller obligations, and module depth from implementation length.

Deepening classifies dependencies into pure in-process, local substitute, remote owned ports/adapters and true external mocks. It asks whether deletion makes complexity vanish or redistributes it to callers, and whether a second real adapter justifies a seam. Replacement interface tests must establish coverage before deleting obsolete internal tests. Design-it-twice deliberately varies interface goals; it is a technique under the selected methodology, not an excuse to start another lifecycle.

The two-axis review separates Standards from Spec. It brings twelve Fowler smell heuristics below project rules and never lets one axis hide the other. Its original `git diff <base>...HEAD` cannot see uncommitted work. This task forbids commits, so the integration must freeze a complete explicit working-tree comparison and feed it to reviewers. Original source also permits recursive agent reviews; use leaf reviewers and bounded focused repair verification.

## Distinctive procedures and resource closure

The JSON lists every item individually. Main resource groups that must survive adaptation are:

| Method family | Essential source resources and substance |
| --- | --- |
| Test-first / debugging | `tdd/tests.md`, `tdd/mocking.md`; exact-symptom repro ladder, minimized load-bearing input, ranked falsifiable hypotheses, tagged probes, perf baseline, forced-mutation proof and original-scenario rerun; `diagnosing-bugs/scripts/hitl-loop.template.sh` captures observations only. |
| Deep module design / survey | `codebase-design/DEEPENING.md`, `DESIGN-IT-TWICE.md`; `improve-codebase-architecture/HTML-REPORT.md` candidate fields and before/after visual patterns, adapted to inline local rendering. |
| Domain model | `domain-modeling/GLOSSARY-FORMAT.md`, `ADR-FORMAT.md`; root/context map vocabulary, sparse durable decisions and lazy creation. Existing repository conventions win. |
| Tracker / triage | `setup-matt-pocock-skills/issue-tracker-{github,gitlab,local}.md`, `triage-labels.md`, `domain.md`; `triage/AGENT-BRIEF.md`, `OUT-OF-SCOPE.md`; native dependencies, claim/resolution and fallback body conventions, current-versus-desired behavioral brief, conceptual rejection knowledge base. |
| Prototype | `prototype/LOGIC.md`, `UI.md`; pure state logic separated from portable HTML shell, guided/free-play scenarios; structurally different UI variants in existing context, shareable variant URLs, production-hidden switcher, input-safe keyboard handling. |
| Human procedure | `wizard/template.sh`; dependency-ordered manual stages, input source/destination/secrecy, hidden input and resumability, verified instructions, summary and static syntax/data-flow verification. |
| Learning | `teach/{MISSION,LEARNING-RECORD,GLOSSARY,RESOURCES}-FORMAT.md`; observable mission, trusted citations, evidence-based learning records, proximal challenge, retrieval/spacing/interleaving and shared lesson assets. |
| Agent writing / PR | `writing-for-agents/SKILL-MECHANICS.md`; context-pointer branch triggers, information hierarchy, completion bounds, no-op/cache pruning; `pr/CREDITS.md` is required attribution. |
| TypeScript boundaries | `setup-ts-deep-modules/dependency-cruiser.config.cjs`; five actual rules (despite prose saying four): outside-app and cross-package entrypoints, tests-through-entrypoints, tests-folder privacy, no cycles. Prove clean/failing-deep-import/restored-clean plus appropriate rule negatives. |

Other procedures remain functional local methods: stakeholder questionnaire targets information held by another person and does not send it; plain-language repitch repairs missing context; workflow specification distinguishes trigger, checkpoint and decision-ready brief without creating schedules; writing fragments preserves an open raw quarry; article shaping has distinct paragraph and beat paths with prerequisite/introduced-concept tracking and disk rereads before writes.

## Safety, dependency and ownership findings

The upstream `implement` commits automatically; `implement-spec` creates branches/worktrees and merges/resets; prototypes and wayfinding create/push throwaway branches; misc setup stages/commits. All exceed this task's authority. Preserve the methods' technical content while central Andino permission controls their effects. Tracker publication, labels, comments, closing, GitHub secrets and recurring schedules are separate external mutations, never implied by audit or preparation.

`git-guardrails-claude-code/scripts/block-dangerous-git.sh` is a Bash/jq regex hook, not a complete Git security parser. `git -C <dir> push` bypasses its patterns, and missing jq can fail open. Upstream `.out-of-scope/frozen-misc-skills.md` explicitly records both defects. Retain operation-risk classification and optional project-hook design only with honest limitations and negative tests; host permissions remain authority.

The wizard writes through symlinks and rewrites dotenv via a temporary file; it also directly invokes `gh secret set`/`gh variable set`. Do not run or copy it blindly. A native-shell adaptation must validate destinations, preserve file permissions, avoid secret display, and handle local/external authorization. The HITL debug script prints captured answers, so credentials belong in user sign-in steps, never captured values.

The HTML survey template requires Tailwind/Mermaid CDNs and `securityLevel: loose`. Adapt to offline inline CSS/SVG with escaped source strings. No mandatory runtime network, npm package, global symlink, plugin install, automatic updater or second router belongs in the bundle. `scripts/link-skills.sh` removes existing destination directories and symlinks globally; it is audited build/developer infrastructure and excluded from runtime. `sync-plugin-version.mjs` writes plugin metadata; release workflow tags/version PRs; both stay excluded.

`chief-of-staff` is beta and conflicts with proportional routing: it mandates all work in subagents, environment improvement first on every task, proactive schedule suggestions and a competing long-running owner. Exclude that lifecycle; retain only context-pointer communication and tactical/strategic retrospective insights. Portable `claude-handoff` content folds into Andino handoff; hardcoded `claude --bg` execution does not.

## Source inconsistencies and evidence limits

Human docs claim missing debug redaction, missing label creation and Claude-only tool names after actual skills fixed those. Domain docs contain the nonsensical same-name comparison after a mechanical rename. Beta TS docs say no lint rule while the local config contains five rules. Treat these as warnings against trusting summaries. Actual current files determine technical behavior.

MIT copyright is `Copyright (c) 2026 Matt Pocock`. Preserve `LICENSE` and PR `CREDITS.md`, including Dex Horthy/Humanlayer show-me attribution. No additional local license file was found for that cited third-party content; do not claim a separately verified remote license. Lockfile development dependencies are not runtime bundle dependencies.

This audit establishes local source coverage and proposals. It does not establish completed implementation, remote latest parity, actual host delegation parity, current third-party CLI syntax, installed optional package behavior or final acceptance. Parent integration owns the canonical matrix, final method IDs and checkpoint.

## Audit verification

After writing this audit, a read-only source-integrity check parsed the JSON, asserted 39 unique rows (38 skills and one archived page), matched all 190 raw-byte source hashes to current files, verified all 27 plugin skill paths exist, and confirmed upstream Git status remained clean. The local fingerprint is `a518ded416351de2146854dac7b3e9e2b08add42ce54c2574146c51a7585b349`. No upstream script, installer or hook was executed. The 111 package-lock development entries declare MIT (96), Python-2.0 (1), BSD-3-Clause (2), BSD-2-Clause (3), ISC (8), and `SEE LICENSE IN LICENSE` (1); these are build-only dependencies and must not be silently bundled as runtime assets.
