# ResearchState and current-state routing

Use when entering research work, resuming it, or changing a material decision. State is a compact view of available evidence, not a mandatory questionnaire or a second project plan.

## Reconstruct only the relevant slice

Read the latest request, conversation, current artifacts, applicable guideline and recorded decisions. Record the current phase and immediate output, retaining provenance to the artifact/version or user decision that supports each material value. If artifacts disagree, surface the affected conflict; do not silently select the most convenient version. Approved title does not establish completed analysis, and a proposal does not describe execution that has not occurred.

Use these conditional groups, expanding only fields consumed by the present task:

| Group | Relevant content |
| --- | --- |
| InteractionIntent | Request, goal/action/artifact, hard constraints, preferences, format, context, material ambiguities, safe assumptions. |
| ResearchContext | Academic level, institution/program, research type, current phase, area/theme/topic/context. |
| Research reasoning | Phenomenon and evidence, actual/expected condition, practical/research problem, gap and novelty evidence, questions/objectives, focus/context/time/unit boundaries. |
| Literature | Mode/question/concepts/term blocks, sources/queries/dates/filters/log, eligibility, record/study identities, screening/exclusions, reading queue/cards/depth/roles, extraction/synthesis, corrections, chaining, review protocol/appraisal/reporting. |
| Methodology | Reasoning/paradigm when relevant, decision stack, theory/framework/propositions/hypotheses, design/time horizon, population/frame/sample or participants, data source/provenance/access, collection/instruments, analysis plan. |
| Quantitative extension | Constructs/operational definitions, variable dictionary, design family, survey/experiment, assignment/comparator, measurement evidence/scoring, estimand, missingness, effect/uncertainty and assumptions. Omit for research that does not need it. |
| Execution and findings | Actual collection/analysis status and artifacts, Finding Registry, null/unexpected findings, tables/figures/themes/quotes, interpretation, comparisons, limitations, implications and RQ-conclusion map. |
| Decisions and integrity | Proposed/approved title and rationale, campus guidance, supervisor decisions/expectations and evidence, ethics/access/privacy/security, verified sources and unverified claims. |
| Defense and revision | Mode/protocol, brief/questions/answer cards, mock history, weaknesses/readiness, actual examiner feedback, required revisions and impact. |
| Continuation | Assumptions, open questions, blockers, risks, current output, next research action. |

Do not create empty fields for the entire inventory. Keep a short state in the conversation for small tasks; use the user's existing research artifact for durable work. Do not impose a new file or serialization format. The [core templates](../assets/research-core-templates.md) are optional output helpers.

## Field status contract

| Status | Meaning and transition evidence |
| --- | --- |
| CONFIRMED | Supported for the stated scope by an identified source or explicit decision. User-confirmed intent is not independently verified empirical truth. |
| PROVISIONAL | Safe working choice/assumption; explain its basis and what would change it. |
| NEEDS_EVIDENCE | A material claim lacks the source/data needed to support it. |
| NEEDS_REVIEW | Available content needs review, including dependencies affected by a revision. |
| UNKNOWN | Not known and not safely inferable. |
| NOT_APPLICABLE | Irrelevant to this design/task, with a short reason where needed. |
| BLOCKED | A named missing decision, evidence or permission prevents this particular action. |

These are the only field statuses. LOCKED describes preservation of an explicit decision; store its authority and scope separately. DEFERRED describes workflow disposition. Readiness, screening and checklist outcomes are artifact-specific vocabularies, not new field statuses. Never upgrade a field because prose is polished or a template filled.

## Phase detection and adaptive entry

Select from actual context: DISCOVERY, TOPIC, PHENOMENON, PROBLEM, LITERATURE, LITERATURE-SEARCH, PAPER-SCREENING, PAPER-READING, LITERATURE-SYNTHESIS, SYSTEMATIC-REVIEW, RESEARCH-DESIGN, TITLE, PROPOSAL-OUTLINE, BAB-I, BAB-II, BAB-III, PROPOSAL-REVIEW, DATA-COLLECTION, ANALYSIS, RESULTS, DISCUSSION, CONCLUSION, BAB-IV, BAB-V, FINAL-CONSISTENCY-REVIEW, SEMPRO-PREP, FINAL-DEFENSE-PREP, MOCK-DEFENSE, ORAL-EXAM, POST-DEFENSE-REVISION, REVISION.

Phase is a task entry point, not a mandatory linear ladder. Work may revisit literature while drafting discussion. Preserve completed valid decisions, load the current route from SKILL, and examine only its material prerequisites.

- Raw interest without a question: DISCOVERY; seek a tractable phenomenon/evidence direction rather than a definitive title.
- Approved title and request for BAB III: BAB-III; preserve title and inspect design/data access, not topic brainstorming.
- Analysis supplied and request for BAB IV: inspect actual outputs, then RESULTS; missing outputs remain NEEDS_EVIDENCE.
- Examiner removes a variable: POST-DEFENSE-REVISION; retain decision history and review all dependent methods/findings/conclusions.
- Eighty search records: PAPER-SCREENING; do not force deep reading of every record.

## Update and return

Apply feedback as a delta: record changed value, reason/authority and source; retain unaffected content; mark affected dependencies NEEDS_REVIEW. If new evidence conflicts with a locked decision, show the conflict and options before changing the decision. Never erase history or silently treat stale findings as current.

Return the requested result first, a compact state delta when useful, material missing evidence and one next research action. That action is a recommendation to the lifecycle owner when Andino is active. A blocked empirical claim does not block independent planning or supported drafting.
