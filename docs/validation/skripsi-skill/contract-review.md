# Skripsi v0.9 written-contract review

Runtime reviewed: 22d780162ab686240961e86300729b462b6578f7.
Scope: implementation ownership, semantic comparison and deterministic evidence. This is not a human academic review or proof of universal model behavior.

## Inventory reconciliation

The actual supplied SRS has 146 FR, 47 NFR, 142 ordered acceptance checkboxes, 32 capabilities, 61 core outputs and 110 initial cases. The supplied GRAND-PLAN has 75 task rows. No count drift was found. Source SHA-256 values and exact requirement text are retained in [traceability](traceability.json); the original planning inputs remain untracked and unmodified outside this worktree. Acceptance IDs AC-001–142 are stable source-order identifiers assigned for this audit, not IDs originally printed in the SRS.

The ownership map is curated by requirement meaning, not keyword scoring. Every requirement has an actual runtime/control-plane target. AC entries map to a related FR; this is an ownership link rather than a claim that one test proves an entire requirement. Behavioral verdict remains NOT_VERIFIED until observed evidence is reviewed.

## Semantic oracle review

All 110 source cases retain their original prompt, expected and forbidden content. Supplemental cases exercise existing activation, integrity and lifecycle requirements. Oracles describe observable decisions rather than exact output wording. The test actor receives prompt and explicitly synthetic raw context, not expected/forbidden or the audit. No source paper/data was manufactured as real research evidence.

| Cases | Owner / reviewed decision | Counterexample rejected by contract |
| --- | --- | --- |
| 001–004 | Current-state entry, discovery, guideline and evidence | Final titles from nonexistent facts; reboot approved topic; replace campus structure; invented statistics. |
| 005–010 | Four routes, revision dependency and small-edit boundary | Forced X/Y for experience; two strands without integration; arbitrary R&D model; local-only revision; regression for an experience question; lifecycle for one sentence. |
| 011–016 | Title focus/anatomy/styles/quality/approval | Cosmetic variants; obligatory method/location; style changes the study; observational causal words; ACC guarantee. |
| 017–023 | Intent/context/delta | Repeated context questions; deleting ambiguous material; rewriting hard constraints; user premise as fact; prompt ceremony. |
| 024–034 | Problem/RQ/scientific reasoning/design/proposal | Practical issue or location as proven gap; unanswerable RQ; IMRaD replaces guideline; invented Lotus; convenience-only method; guessed supervisor preferences. |
| 035–049 | Finding Registry, result/discussion/conclusion and revision | Invented output/quotes; hidden nulls; p-value as magnitude; causal upgrade; literature dump/cherry-picking; new conclusion result; parallel-only mixed findings; product equals effective. |
| 050–062 | Advanced stack/data/framework/ethics and quantitative checks | Cosmetic Onion; prestige problematization; summaries as SOTA; universal diagnostics/alpha; wrong data fitness; public-data ethics waiver; fixed hypotheses; decorative arrows; single-signal venue accusation/endorsement. |
| 063–077 | Defense and examiner revision | Proprietary question bank claim; obsolete proposed method; compound-question evasion; authority-only rationale; bluffing; false premise agreement; answer key before practice; scripts; ungrounded readiness. |
| 078–093 | Quantitative fit-to-inference | Prestige choice; forced variables/hypotheses; convenience representativeness; sample magic number; ungrounded instrument/adaptation; test shopping; p-value probability; null proves absence; outcome-driven cleaning. |
| 094–110 | Search/screen/read/synthesis/systematic | One keyword as coverage; aggressive NOT; universal syntax; deep-read everything; five-minute guarantee; abstract/AI summary as full text; prestige relevance; title-only rejection; fake systematic label/counts; hidden retraction. |

These are written-contract findings. Each source case has its own owner in traceability.json and separate live execution record when run. A case can fail live despite a coherent written rule.

## Ownership and progressive disclosure

SKILL.md contains activation, authority, state preservation, no-fabrication, direct route links and lifecycle/response semantics in 55 lines. All 18 references are directly reachable. Assets are optional artifacts linked from their owning domain references; they neither duplicate full methods nor create hidden requirements. No runtime scripts, dependency manifests, eval files or planning files were added.

Evidence/authority belongs to evidence-guidelines-integrity; state/statuses to research-state-and-routing; literature retrieval to search, extraction/synthesis to reading, completed-review claims to systematic; baseline routes to design, deep numerical decisions to quantitative; result claims to results; dependency propagation to revision. Repeated short safety reminders apply shared rules at decision points rather than introducing conflicting ownership. No load-all instruction or required deep reference chain was found.

Field statuses retain exactly the SRS seven values. LOCKED remains decision semantics. Screening, readiness, finding and interpretation labels are explicitly scoped artifact vocabularies. Campus authority remains within all governed scope, including ethics/procedure; no formatting-only reduction remains. Approved/locked decisions cannot be silently discarded by new evidence. Research planning stays allowed while fabricated completed evidence is forbidden.

## Standalone and Andino

Compared with actual andino-workflow SKILL.md, references/routing.md and references/handoff.md at 894e57099f6b3e4d479fd7738bfdeca1181b39cc. Standalone needs no Andino dependency. Active Andino owns plan/checkpoint/completion/authoritative next action; the specialist returns domain state, evidence, issues and recommendation. No changes were made to Andino or Rescue branches. Live coexistence evidence is tracked separately.

## External source checks

Primary current references checked during implementation: [Agent Skills specification source](https://agentskills.io/specification), [PRISMA 2020](https://www.prisma-statement.org/prisma-2020), [PRISMA search extension](https://www.prisma-statement.org/prisma-search), and [ASA p-value statement](https://www.amstat.org/docs/default-source/amstat-documents/p-valuestatement.pdf). They support package disclosure, reporting-versus-method boundaries and statistical interpretation cautions respectively. SRS remains product truth; external documentation does not override it. Runtime designs are original, not reconstructed paid TutorialSkripsi materials.

## Validation scope

32 unit tests passed, including import drift/missing oracle, missing or duplicate ownership, nonexistent target, unsupported behavioral PASS, missing eval, final task disposition and live-evidence fail-closed cases. Repository validator passes all three runtime packages and all three eval schemas. Traceability validator checks all required IDs, target files and final task dispositions. `git diff --check` passes for runtime. Remote [Validate skills run 35522527189](https://github.com/andinoferdi/AI-RULES/actions/runs/35522527189) passed on main `729f10e` while fetching the published runtime branch. The reviewed live evidence remains scenario-bounded: 58 PASS, 0 FAIL and 59 NOT_VERIFIED because host limits prevented execution or remediation reruns. Deterministic validators never promote those unavailable checks to behavioral PASS.
