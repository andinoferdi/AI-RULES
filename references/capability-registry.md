# Capability registry

This is on-demand contract metadata, not a second router or a full-load requirement. Select a heading by the current unresolved need; do not load every skill/schema. Bundled method aliases resolve to the [canonical index](internal-method-index.md); native sibling/tool provenance is resolved through the host. Metadata is DISCOVERED, not proof of AVAILABLE, INVOKABLE or USED. See [invocation](invocation-adapter.md) and [coexistence](capability-coexistence.md).

Excluded meta-routers: using-superpowers and using-agent-skills. Andino performs their routing role; invoking them would create a competing lifecycle. Other installed skills remain discoverable through the host catalog when a real need warrants them. Registry does not install, enable or health-check every capability.

## Index

| ID | Type | Family/provider | Purpose |
| --- | --- | --- | --- |
| [focus](#focus) | skill | AI-RULES | Default communication on every Andino invocation |
| [search-first](#search-first) | skill | AI-RULES, adapted from ECC | Existing-solution research before implementation |
| [council](#council) | skill | AI-RULES | Independent review of consequential decisions |
| [threejs-skills](#threejs-skills) | skill | AI-RULES | On-demand Three.js and NixieFX domain specialists |
| [systematic-debugging](#systematic-debugging) | method | Andino internal | Root-cause investigation |
| [test-driven-development](#test-driven-development) | method | Andino internal | Executable regression contract |
| [verification-before-completion](#verification-before-completion) | method | Andino internal | Evidence before completion |
| [brainstorming](#brainstorming) | method | Andino internal | Clarify product/design choices |
| [writing-plans](#writing-plans) | method | Andino internal | Order dependent implementation |
| [requesting-code-review](#requesting-code-review) | method | Andino internal | Prepare bounded implementation review |
| [receiving-code-review](#receiving-code-review) | method | Andino internal | Evaluate review feedback |
| [dispatching-parallel-agents](#dispatching-parallel-agents) | method | Andino internal | Bounded concurrent work |
| [using-git-worktrees](#using-git-worktrees) | method | Andino internal | Implementation isolation |
| [finishing-a-development-branch](#finishing-a-development-branch) | method | Andino internal | Branch completion options |
| [idea-refine](#idea-refine) | method | Andino internal | Refine an uncertain idea |
| [interview-me](#interview-me) | method | Andino internal | Resolve material human intent |
| [api-and-interface-design](#api-and-interface-design) | method | Andino internal | Stable API/interface contracts |
| [browser-testing-with-devtools](#browser-testing-with-devtools) | method | Andino internal | Browser verification methodology |
| [ci-cd-and-automation](#ci-cd-and-automation) | method | Andino internal | CI and delivery automation |
| [code-review-and-quality](#code-review-and-quality) | method | Andino internal | Assess implementation quality |
| [code-simplification](#code-simplification) | method | Andino internal | Simplify existing code |
| [constraint-driven-development](#constraint-driven-development) | method | Andino internal | Establish quality constraints |
| [context-engineering](#context-engineering) | method | Andino internal | Bound useful task context |
| [debugging-and-error-recovery](#debugging-and-error-recovery) | method | Andino internal | Recover execution errors |
| [deprecation-and-migration](#deprecation-and-migration) | method | Andino internal | Evolve compatibility safely |
| [documentation-and-adrs](#documentation-and-adrs) | method | Andino internal | Record decisions and documentation |
| [doubt-driven-development](#doubt-driven-development) | method | Andino internal | Challenge consequential assumptions |
| [frontend-ui-engineering](#frontend-ui-engineering) | method | Andino internal | Implement product UI |
| [git-workflow-and-versioning](#git-workflow-and-versioning) | method | Andino internal | Git workflow discipline |
| [incremental-implementation](#incremental-implementation) | method | Andino internal | Deliver dependent changes incrementally |
| [observability-and-instrumentation](#observability-and-instrumentation) | method | Andino internal | Diagnose production behavior |
| [performance-optimization](#performance-optimization) | method | Andino internal | Measure and improve performance |
| [planning-and-task-breakdown](#planning-and-task-breakdown) | method | Andino internal | Order complex work |
| [security-and-hardening](#security-and-hardening) | method | Andino internal | Address concrete security concerns |
| [shipping-and-launch](#shipping-and-launch) | method | Andino internal | Prepare an authorized release |
| [source-driven-development](#source-driven-development) | method | Andino internal | Ground technical decisions |
| [spec-driven-development](#spec-driven-development) | method | Andino internal | Specify consequential behavior |
| [agent-skills-test-driven-development](#agent-skills-test-driven-development) | method | Andino internal | Executable regression contract |
| [ponytail](#ponytail) | skill | Ponytail | Minimal correct implementation |
| [claude-mem](#claude-mem) | skill | Claude-Mem | Targeted historical decisions |
| [impeccable](#impeccable) | skill | Impeccable | UI critique, polish and anti-slop detection |
| [design-taste-frontend](#design-taste-frontend) | skill | Taste Skill | Visual direction |
| [clone-website](#clone-website) | skill | AI Website Cloner | Fidelity reconstruction |
| [graphify](#graphify) | skill | Graphify | Complex structural relationship analysis |
| [antislop](#antislop) | skill | Anti-Slop | Core output quality |
| [antislop-ui](#antislop-ui) | skill | Anti-Slop | UI visual quality |
| [antislop-copywriting](#antislop-copywriting) | skill | Anti-Slop | Natural useful copy |
| [antislop-human](#antislop-human) | skill | Anti-Slop | Human usability/accessibility |
| [antislop-layoutmobile](#antislop-layoutmobile) | skill | Anti-Slop | Responsive/mobile quality |
| [antislop-code](#antislop-code) | skill | Anti-Slop | Code/comment hygiene |
| [context7](#context7) | MCP | Upstash Context7 | Current/version-specific library docs |
| [playwright-mcp](#playwright-mcp) | MCP | Microsoft Playwright MCP | Persistent/exploratory browser interaction |
| [chrome-devtools](#chrome-devtools) | MCP | Chrome DevTools MCP | Browser diagnostics |
| [git-mcp](#git-mcp) | MCP | MCP Git server | Repository operations through MCP |
| [drawio-mcp](#drawio-mcp) | MCP | Draw.io MCP | Editable general diagrams |
| [staruml-mcp](#staruml-mcp) | MCP | StarUML MCP | Formal UML/model operations |
| [premiere-pro-mcp](#premiere-pro-mcp) | MCP | Adobe Premiere Pro MCP | Premiere project/timeline operations |
| [cheatengine-mcp](#cheatengine-mcp) | MCP | Cheat Engine MCP bridge | Authorized local memory/debug inspection |
| [native-capabilities](#native-capabilities) | native | Active host/project | Existing bounded local evidence |

## systematic-debugging

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: systematic-debugging resolves to canonical debugging; no upstream native registration required
- Primary purpose: Root-cause investigation
- Trigger: Cause is unresolved or evidence contradicts the diagnosis.
- Preferred when: Reproduction and discriminating hypotheses are needed.
- Avoid when: Cause already established; do not repeat investigation.
- Availability check: Check local skills/debugging/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [debugging](../skills/debugging/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/debugging/GUIDE.md

## test-driven-development

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: test-driven-development resolves to canonical tdd; no upstream native registration required
- Primary purpose: Executable regression contract
- Trigger: Behavior change needs a failing regression or executable contract.
- Preferred when: Project tests can distinguish the desired behavior.
- Avoid when: Text-only edits and already-verified unchanged behavior.
- Availability check: Check local skills/tdd/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [tdd](../skills/tdd/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/tdd/GUIDE.md

## verification-before-completion

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: verification-before-completion resolves to canonical verification; no upstream native registration required
- Primary purpose: Evidence before completion
- Trigger: A consequential completion claim needs validation.
- Preferred when: Relevant checks can prove acceptance.
- Avoid when: Repeating unchanged passing suites without new evidence.
- Availability check: Check local skills/verification/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [verification](../skills/verification/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/verification/GUIDE.md

## brainstorming

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: brainstorming resolves to canonical decision-interview; no upstream native registration required
- Primary purpose: Clarify product/design choices
- Trigger: Material requirement remains unclear after inspecting existing project behavior.
- Preferred when: Options and human preferences change the outcome.
- Avoid when: Repository-answerable details or locked requirements.
- Availability check: Check local skills/decision-interview/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [decision-interview](../skills/decision-interview/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/decision-interview/GUIDE.md

## writing-plans

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: writing-plans resolves to canonical planning; no upstream native registration required
- Primary purpose: Order dependent implementation
- Trigger: Implementation sequencing is materially useful.
- Preferred when: Dependent steps need a durable execution contract.
- Avoid when: Simple tasks or creating a competing plan.
- Availability check: Check local skills/planning/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [planning](../skills/planning/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/planning/GUIDE.md

## requesting-code-review

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: requesting-code-review resolves to canonical code-review; no upstream native registration required
- Primary purpose: Prepare bounded implementation review
- Trigger: Implemented scope warrants reviewer evidence.
- Preferred when: A targeted diff/contract needs a review.
- Avoid when: Automatic agent fan-out or a review of unrelated code.
- Availability check: Check local skills/code-review/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [code-review](../skills/code-review/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/code-review/GUIDE.md

## receiving-code-review

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: receiving-code-review resolves to canonical code-review; no upstream native registration required
- Primary purpose: Evaluate review feedback
- Trigger: Received feedback needs technical assessment.
- Preferred when: Check evidence before accepting a proposed fix.
- Avoid when: Blind agreement or optional preferences treated as blockers.
- Availability check: Check local skills/code-review/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [code-review](../skills/code-review/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/code-review/GUIDE.md

## dispatching-parallel-agents

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: dispatching-parallel-agents resolves to canonical delegation; no upstream native registration required
- Primary purpose: Bounded concurrent work
- Trigger: Independent tasks justify concurrency AND user/host authorizes delegation.
- Preferred when: Separate scopes reduce a demonstrated bottleneck.
- Avoid when: Default fan-out, shared mutable scopes or absent authorization.
- Availability check: Check local skills/delegation/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [delegation](../skills/delegation/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/delegation/GUIDE.md

## using-git-worktrees

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: using-git-worktrees resolves to canonical git-isolation; no upstream native registration required
- Primary purpose: Implementation isolation
- Trigger: Isolation is needed and existing checkout/worktree is unsuitable.
- Preferred when: Separate branch state prevents conflicts.
- Avoid when: Unnecessary new checkout or contradicting project/user choice.
- Availability check: Check local skills/git-isolation/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [git-isolation](../skills/git-isolation/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/git-isolation/GUIDE.md

## finishing-a-development-branch

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: finishing-a-development-branch resolves to canonical delivery; no upstream native registration required
- Primary purpose: Branch completion options
- Trigger: Validated implementation enters branch completion workflow.
- Preferred when: The requested completion action is clear.
- Avoid when: Assuming commit/push/merge authorization from a review GO.
- Availability check: Check local skills/delivery/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [delivery](../skills/delivery/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/delivery/GUIDE.md

## idea-refine

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: idea-refine resolves to canonical idea-refine; no upstream native registration required
- Primary purpose: Refine an uncertain idea
- Trigger: A vague idea needs evidence-backed alternatives before choosing an approach.
- Preferred when: Generate and converge options when actual product uncertainty warrants it.
- Avoid when: Reopening locked decisions, forcing ideation on mechanical work or writing a one-pager outside authorized scope.
- Availability check: Check local skills/idea-refine/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [idea-refine](../skills/idea-refine/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/idea-refine/GUIDE.md

## interview-me

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: interview-me resolves to canonical decision-interview; no upstream native registration required
- Primary purpose: Resolve material human intent
- Trigger: Targeted project inspection leaves material who/why/success/constraint choices unresolved.
- Preferred when: Ask focused consequential questions or honor explicit interview request.
- Avoid when: Repository-answerable questions, already clear intent, mandatory confidence ceremony or a second plan.
- Availability check: Check local skills/decision-interview/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [decision-interview](../skills/decision-interview/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/decision-interview/GUIDE.md

## api-and-interface-design

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: api-and-interface-design resolves to canonical api-and-interface-design; no upstream native registration required
- Primary purpose: Stable API/interface contracts
- Trigger: Public interface or consumer compatibility needs design.
- Preferred when: Trace actual consumers and versioning needs.
- Avoid when: Internal detail with no meaningful contract change.
- Availability check: Check local skills/api-and-interface-design/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [api-and-interface-design](../skills/api-and-interface-design/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/api-and-interface-design/GUIDE.md

## browser-testing-with-devtools

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: browser-testing-with-devtools resolves to canonical browser-testing-with-devtools; no upstream native registration required
- Primary purpose: Browser verification methodology
- Trigger: Browser behavior needs observable functional/diagnostic checks.
- Preferred when: A real browser provides missing evidence.
- Avoid when: No browser outcome involved; method is not a connected MCP.
- Availability check: Check local skills/browser-testing-with-devtools/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [browser-testing-with-devtools](../skills/browser-testing-with-devtools/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/browser-testing-with-devtools/GUIDE.md

## ci-cd-and-automation

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: ci-cd-and-automation resolves to canonical ci-cd-and-automation; no upstream native registration required
- Primary purpose: CI and delivery automation
- Trigger: Task changes pipelines or build automation.
- Preferred when: Existing CI extension points and checks are known.
- Avoid when: Starting deploys or schedules without applicable authorization.
- Availability check: Check local skills/ci-cd-and-automation/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [ci-cd-and-automation](../skills/ci-cd-and-automation/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/ci-cd-and-automation/GUIDE.md

## code-review-and-quality

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: code-review-and-quality resolves to canonical code-review; no upstream native registration required
- Primary purpose: Assess implementation quality
- Trigger: Bounded diff needs correctness/quality review.
- Preferred when: Review after implementation or explicit audit.
- Avoid when: Unsolicited whole-repository rewrite.
- Availability check: Check local skills/code-review/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [code-review](../skills/code-review/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/code-review/GUIDE.md

## code-simplification

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: code-simplification resolves to canonical code-simplification; no upstream native registration required
- Primary purpose: Simplify existing code
- Trigger: Existing code has avoidable complexity.
- Preferred when: Refactor preserves behavior with meaningful evidence.
- Avoid when: Already minimal changes or replacing accepted architecture.
- Availability check: Check local skills/code-simplification/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [code-simplification](../skills/code-simplification/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/code-simplification/GUIDE.md

## constraint-driven-development

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: constraint-driven-development resolves to canonical constraint-driven-development; no upstream native registration required
- Primary purpose: Establish quality constraints
- Trigger: Implementation lacks material written constraints.
- Preferred when: Agree verifiable constraints using existing project rules.
- Avoid when: Inventing a new quality bar for a routine edit.
- Availability check: Check local skills/constraint-driven-development/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [constraint-driven-development](../skills/constraint-driven-development/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/constraint-driven-development/GUIDE.md

## context-engineering

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: context-engineering resolves to canonical context-engineering; no upstream native registration required
- Primary purpose: Bound useful task context
- Trigger: Context selection or drift prevents reliable execution.
- Preferred when: Narrow artifacts can resolve a real context gap.
- Avoid when: Full repository loading by default.
- Availability check: Check local skills/context-engineering/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [context-engineering](../skills/context-engineering/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/context-engineering/GUIDE.md

## debugging-and-error-recovery

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: debugging-and-error-recovery resolves to canonical debugging; no upstream native registration required
- Primary purpose: Recover execution errors
- Trigger: A tool/test/runtime failure needs diagnosis or recovery.
- Preferred when: Differentiate deterministic versus transient failures.
- Avoid when: Retrying identical schema/permission/credential errors.
- Availability check: Check local skills/debugging/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [debugging](../skills/debugging/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/debugging/GUIDE.md

## deprecation-and-migration

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: deprecation-and-migration resolves to canonical deprecation-and-migration; no upstream native registration required
- Primary purpose: Evolve compatibility safely
- Trigger: Deprecation or data/contract migration is in scope.
- Preferred when: Affected versions/consumers and rollback evidence are available.
- Avoid when: Unrequested irreversible/live migration.
- Availability check: Check local skills/deprecation-and-migration/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [deprecation-and-migration](../skills/deprecation-and-migration/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/deprecation-and-migration/GUIDE.md

## documentation-and-adrs

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: documentation-and-adrs resolves to canonical documentation-and-adrs; no upstream native registration required
- Primary purpose: Record decisions and documentation
- Trigger: Material decisions or usage changes need durable documentation.
- Preferred when: Use an existing ADR/docs convention.
- Avoid when: Placeholder docs or duplicating the active plan.
- Availability check: Check local skills/documentation-and-adrs/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [documentation-and-adrs](../skills/documentation-and-adrs/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/documentation-and-adrs/GUIDE.md

## doubt-driven-development

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: doubt-driven-development resolves to canonical doubt-driven-development; no upstream native registration required
- Primary purpose: Challenge consequential assumptions
- Trigger: A consequential uncertain choice warrants independent evidence.
- Preferred when: Discriminating checks can reject a material assumption.
- Avoid when: Generic skepticism or unnecessary delegation.
- Availability check: Check local skills/doubt-driven-development/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [doubt-driven-development](../skills/doubt-driven-development/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/doubt-driven-development/GUIDE.md

## frontend-ui-engineering

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: frontend-ui-engineering resolves to canonical frontend-ui-engineering; no upstream native registration required
- Primary purpose: Implement product UI
- Trigger: Accessible responsive frontend behavior is in scope.
- Preferred when: Existing stack/components can implement accepted design.
- Avoid when: Changing design direction or stack without requirement.
- Availability check: Check local skills/frontend-ui-engineering/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [frontend-ui-engineering](../skills/frontend-ui-engineering/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/frontend-ui-engineering/GUIDE.md

## git-workflow-and-versioning

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: git-workflow-and-versioning resolves to canonical git-workflow-and-versioning; no upstream native registration required
- Primary purpose: Git workflow discipline
- Trigger: Requested work changes branch/release/version workflow.
- Preferred when: Clarify local state and applicable authorized action.
- Avoid when: Skill as consent to commit/push/merge.
- Availability check: Check local skills/git-workflow-and-versioning/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [git-workflow-and-versioning](../skills/git-workflow-and-versioning/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/git-workflow-and-versioning/GUIDE.md

## incremental-implementation

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: incremental-implementation resolves to canonical incremental-implementation; no upstream native registration required
- Primary purpose: Deliver dependent changes incrementally
- Trigger: Coupled implementation benefits from thin verifiable slices.
- Preferred when: Each slice proves a real acceptance outcome.
- Avoid when: Rigid phases for a one-line edit.
- Availability check: Check local skills/incremental-implementation/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [incremental-implementation](../skills/incremental-implementation/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/incremental-implementation/GUIDE.md

## observability-and-instrumentation

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: observability-and-instrumentation resolves to canonical observability-and-instrumentation; no upstream native registration required
- Primary purpose: Diagnose production behavior
- Trigger: Missing logs/metrics/traces obstruct a required outcome.
- Preferred when: Focused instrumentation can answer a concrete question.
- Avoid when: Collecting sensitive data or instrumenting unrelated systems.
- Availability check: Check local skills/observability-and-instrumentation/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [observability-and-instrumentation](../skills/observability-and-instrumentation/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/observability-and-instrumentation/GUIDE.md

## performance-optimization

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: performance-optimization resolves to canonical performance-optimization; no upstream native registration required
- Primary purpose: Measure and improve performance
- Trigger: A measured bottleneck or performance requirement exists.
- Preferred when: Baseline and repeatable benchmark are available.
- Avoid when: Speculative micro-optimization.
- Availability check: Check local skills/performance-optimization/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [performance-optimization](../skills/performance-optimization/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/performance-optimization/GUIDE.md

## planning-and-task-breakdown

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: planning-and-task-breakdown resolves to canonical planning; no upstream native registration required
- Primary purpose: Order complex work
- Trigger: Dependencies or milestones need task decomposition.
- Preferred when: Refine Andino existing plan with bounded actions.
- Avoid when: Second lifecycle/plan owner.
- Availability check: Check local skills/planning/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [planning](../skills/planning/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/planning/GUIDE.md

## security-and-hardening

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: security-and-hardening resolves to canonical security-and-hardening; no upstream native registration required
- Primary purpose: Address concrete security concerns
- Trigger: Scope exposes a vulnerability or explicit security requirement.
- Preferred when: Threat/attack surface evidence guides focused fixes.
- Avoid when: Unsolicited hypothetical compliance ceremony.
- Availability check: Check local skills/security-and-hardening/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [security-and-hardening](../skills/security-and-hardening/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/security-and-hardening/GUIDE.md

## shipping-and-launch

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: shipping-and-launch resolves to canonical shipping-and-launch; no upstream native registration required
- Primary purpose: Prepare an authorized release
- Trigger: Actual release/launch readiness is requested.
- Preferred when: Verify artifacts, rollback and requested environment.
- Avoid when: Assuming deploy or publication consent.
- Availability check: Check local skills/shipping-and-launch/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [shipping-and-launch](../skills/shipping-and-launch/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/shipping-and-launch/GUIDE.md

## source-driven-development

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: source-driven-development resolves to canonical source-driven-development; no upstream native registration required
- Primary purpose: Ground technical decisions
- Trigger: Version-sensitive implementation contract needs primary documentation.
- Preferred when: Inspect dependency versions before authoritative lookup.
- Avoid when: Research for reliable local trivial facts.
- Availability check: Check local skills/source-driven-development/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [source-driven-development](../skills/source-driven-development/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/source-driven-development/GUIDE.md

## spec-driven-development

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: spec-driven-development resolves to canonical specification; no upstream native registration required
- Primary purpose: Specify consequential behavior
- Trigger: A new/material feature needs an observable contract.
- Preferred when: Existing specification can be extended before code.
- Avoid when: Mandatory spec ceremony for simple edits.
- Availability check: Check local skills/specification/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [specification](../skills/specification/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/specification/GUIDE.md

## agent-skills-test-driven-development

- Type: method
- Family/provider: Andino internal; adapted source provenance in package legal records
- Aliases: agent-skills-test-driven-development resolves to canonical tdd; no upstream native registration required
- Primary purpose: Executable regression contract
- Trigger: Behavior change needs failing regression/executable contract.
- Preferred when: An accepted public behavior needs a regression; this source-name alias selects the same canonical tdd procedure.
- Avoid when: Double-loading a competing TDD provider or text-only edits.
- Availability check: Check local skills/tdd/GUIDE.md and selected resources plus actual resource permissions.
- Invocation method: Read [tdd](../skills/tdd/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.
- First-call/preflight: Read accepted task/project evidence and only the selected guide; retain one Andino plan.
- Fallback: Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.
- Coexistence/conflicts: Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.
- Activation policy: CONDITIONAL_AUTO
- Internal method: skills/tdd/GUIDE.md

## ponytail

- Type: skill
- Family/provider: Ponytail
- Aliases: none
- Primary purpose: Minimal correct implementation
- Trigger: Unnecessary dependency, excessive abstraction/LOC, needless wrapper, custom replacement for platform facility or inflated solution is evidenced.
- Preferred when: Use simplification during relevant coding work; explicit user activation also applies.
- Avoid when: Automatic activation for every one-line change; sacrificing correctness/security/accessibility/readability.
- Availability check: Resolve the exact host skill ID/path and provider; check native invocation permission. A directory alone proves neither invocation nor use.
- Invocation method: Load the selected actual SKILL.md through the host-supported skill mechanism, then only relevant references. Do not bypass explicit-only restrictions via file reads.
- First-call/preflight: Read applicable project constraints and current evidence first.
- Fallback: Use the relevant local discipline without claiming this external skill was loaded.
- Coexistence/conflicts: Prefer Ponytail for prospective over-build risk; code-simplification for existing-code refactoring. Do not load both for the same concern. Upstream broad coding/persistence defaults yield to Andino current-need selection; release once this need ends.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Record resolved ID/path/provider, actual load and task-relevant result. Similar reasoning or a mention is not evidence of use.
- Activation policy: CONDITIONAL_AUTO

## claude-mem

- Type: skill
- Family/provider: Claude-Mem
- Aliases: claude-mem:mem-search; mem-search (verify provider)
- Primary purpose: Targeted historical decisions
- Trigger: A previous decision or implementation reason is material and absent from current artifacts.
- Preferred when: Use historical retrieval only for that specific gap.
- Avoid when: Automatic per-prompt retrieval; treating memory as current repository evidence.
- Availability check: Discover actual Claude-Mem skill and search/timeline/detail MCP tools on any working host. Observer health and retrieval health are separate; verify retrieval results.
- Invocation method: Load permitted mem-search skill if useful; targeted search, timeline only if useful, then batched selected get_observations/detail using actual exposed names.
- First-call/preflight: Name the historical gap; check current written project artifacts first.
- Fallback: Read existing project decision/checkpoint/Git artifacts; state a historical gap if still material.
- Coexistence/conflicts: One selected methodology; Andino retains lifecycle ownership.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Record resolved ID/path/provider, actual load and task-relevant result. Similar reasoning or a mention is not evidence of use.
- Activation policy: AUTO

## impeccable

- Type: skill
- Family/provider: Impeccable (pbakaus/impeccable, Apache-2.0)
- Aliases: none
- Primary purpose: UI critique, refinement, accessibility and anti-slop detection
- Trigger: Frontend interface needs design context (PRODUCT.md/DESIGN.md), critique, audit, polish, hardening, dashboards, product UI, design-system work or a deterministic `detect` scan after generation.
- Preferred when: A design direction exists or is being recorded and the output must be evaluated and refined against it; always after Taste generation for landing and marketing pages.
- Avoid when: Backend-only or non-UI work; overwriting accepted tokens; treating a clean `detect` run as proof of quality.
- Availability check: Resolve the exact host skill ID/path and provider; check native invocation permission. A directory alone proves neither invocation nor use.
- Invocation method: Load the selected actual SKILL.md through the host-supported skill mechanism, then only relevant references. Do not bypass explicit-only restrictions via file reads.
- First-call/preflight: Read applicable project constraints and current evidence first.
- Fallback: Use the relevant local discipline without claiming this external skill was loaded.
- Coexistence/conflicts: Apply [UI coexistence](ui-coexistence.md). Explicit single-skill choices stand; product UX/accessibility wins over aesthetic defaults.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Record resolved ID/path/provider, actual load and task-relevant result. Similar reasoning or a mention is not evidence of use.
- Activation policy: CONDITIONAL_AUTO

## design-taste-frontend

- Type: skill
- Family/provider: Taste Skill
- Aliases: taste-skill (if catalog alias exists)
- Primary purpose: Visual direction
- Trigger: Landing/portfolio/redesign typography, composition or motion direction is required.
- Preferred when: Visual character is an unresolved task concern.
- Avoid when: Fidelity clone redesigned by default; automatic use for complex product dashboards.
- Availability check: Resolve the exact host skill ID/path and provider; check native invocation permission. A directory alone proves neither invocation nor use.
- Invocation method: Load the selected actual SKILL.md through the host-supported skill mechanism, then only relevant references. Do not bypass explicit-only restrictions via file reads.
- First-call/preflight: Read applicable project constraints and current evidence first.
- Fallback: Use the relevant local discipline without claiming this external skill was loaded.
- Coexistence/conflicts: Apply [UI coexistence](ui-coexistence.md). Taste generates and Impeccable critiques and refines; preserve reduced motion and project stack.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Record resolved ID/path/provider, actual load and task-relevant result. Similar reasoning or a mention is not evidence of use.
- Activation policy: CONDITIONAL_AUTO

## clone-website

- Type: skill
- Family/provider: AI Website Cloner
- Aliases: none
- Primary purpose: Fidelity reconstruction
- Trigger: User requests reconstruction of a concrete website reference.
- Preferred when: Measure reference layout/behavior and preserve requested fidelity.
- Avoid when: Generic redesign or silently reinterpreting the reference.
- Availability check: Resolve the exact host skill ID/path and provider; check native invocation permission. A directory alone proves neither invocation nor use.
- Invocation method: Load the selected actual SKILL.md through the host-supported skill mechanism, then only relevant references. Do not bypass explicit-only restrictions via file reads.
- First-call/preflight: Read applicable project constraints and current evidence first.
- Fallback: Use accessible reference and existing browser/local frontend tools; report any fidelity evidence unavailable.
- Coexistence/conflicts: One selected methodology; Andino retains lifecycle ownership.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Record resolved ID/path/provider, actual load and task-relevant result. Similar reasoning or a mention is not evidence of use.
- Activation policy: CONDITIONAL_AUTO

## graphify

- Type: skill
- Family/provider: Graphify
- Aliases: none
- Primary purpose: Complex structural relationship analysis
- Trigger: Cross-module dependency, callers/callees, change propagation or structural trace makes bounded native search insufficient.
- Preferred when: Existing fresh graph/index or permitted Graphify interface answers the relationship gap.
- Avoid when: Building a graph for every coding task; simple direct reference; stale inferred edges treated as facts.
- Availability check: Inspect actual installed Graphify skill/version and exposed CLI/MCP schema; names differ by provider/version. Graphify skill presence does not prove Graphify MCP exposure.
- Invocation method: Select exposed query/callers/impact/trace operation by need: dependency query, caller/callee lookup, impact traversal, or structural path/trace. Installed CLI may expose graphify query/path/explain. Resolve exact installed tool names instead of inventing universal query_graph/graphify_* names.
- First-call/preflight: Check existing graph/index freshness against current files/revision. Request rebuilding only when the missing graph is material and within authorized scope.
- Fallback: Bounded symbol/reference search and current source inspection; state remaining impact coverage gap if insufficient.
- Coexistence/conflicts: Native symbol/reference search wins for simple bounded relationships. Existing Graphify skill broad scan defaults yield to current-need policy; generation/delegation/export require actual task scope.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Record resolved ID/path/provider, actual load and task-relevant result. Similar reasoning or a mention is not evidence of use.
- Activation policy: AUTO

## antislop

- Type: skill
- Family/provider: Anti-Slop
- Aliases: none
- Primary purpose: Core output quality
- Trigger: Concrete generated-output quality concerns need the family core filter.
- Preferred when: One relevant concern needs shared quality rules.
- Avoid when: Automatic loading of every family subskill.
- Availability check: Resolve the exact host skill ID/path and provider; check native invocation permission. A directory alone proves neither invocation nor use.
- Invocation method: Load the selected actual SKILL.md through the host-supported skill mechanism, then only relevant references. Do not bypass explicit-only restrictions via file reads.
- First-call/preflight: Read applicable project constraints and current evidence first.
- Fallback: Apply existing Andino/project quality rules to the relevant output without claiming external Anti-Slop use.
- Coexistence/conflicts: Quality filter complements accepted design and selected methodology; never overrides user direction, accessibility or UI coexistence. Core does not imply all subskills.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Record resolved ID/path/provider, actual load and task-relevant result. Similar reasoning or a mention is not evidence of use.
- Activation policy: CONDITIONAL_AUTO

## antislop-ui

- Type: skill
- Family/provider: Anti-Slop
- Aliases: none
- Primary purpose: UI visual quality
- Trigger: Generated UI shows generic/incoherent patterns within scope.
- Preferred when: Core plus UI filter adds measurable design quality.
- Avoid when: Replacing user design direction or invoking all subskills.
- Availability check: Resolve the exact host skill ID/path and provider; check native invocation permission. A directory alone proves neither invocation nor use.
- Invocation method: Load the selected actual SKILL.md through the host-supported skill mechanism, then only relevant references. Do not bypass explicit-only restrictions via file reads.
- First-call/preflight: Read applicable project constraints and current evidence first.
- Fallback: Apply existing Andino/project quality rules to the relevant output without claiming external Anti-Slop use.
- Coexistence/conflicts: Quality filter complements accepted design and selected methodology; never overrides user direction, accessibility or UI coexistence. Core does not imply all subskills.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Record resolved ID/path/provider, actual load and task-relevant result. Similar reasoning or a mention is not evidence of use.
- Activation policy: CONDITIONAL_AUTO

## antislop-copywriting

- Type: skill
- Family/provider: Anti-Slop
- Aliases: none
- Primary purpose: Natural useful copy
- Trigger: Writing/editing copy needs relevance and natural language.
- Preferred when: Copy concern alone can use this subskill.
- Avoid when: Loading unrelated UI/code concerns.
- Availability check: Resolve the exact host skill ID/path and provider; check native invocation permission. A directory alone proves neither invocation nor use.
- Invocation method: Load the selected actual SKILL.md through the host-supported skill mechanism, then only relevant references. Do not bypass explicit-only restrictions via file reads.
- First-call/preflight: Read applicable project constraints and current evidence first.
- Fallback: Apply existing Andino/project quality rules to the relevant output without claiming external Anti-Slop use.
- Coexistence/conflicts: Quality filter complements accepted design and selected methodology; never overrides user direction, accessibility or UI coexistence. Core does not imply all subskills.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Record resolved ID/path/provider, actual load and task-relevant result. Similar reasoning or a mention is not evidence of use.
- Activation policy: CONDITIONAL_AUTO

## antislop-human

- Type: skill
- Family/provider: Anti-Slop
- Aliases: none
- Primary purpose: Human usability/accessibility
- Trigger: Human usability/accessibility concerns are part of generated output.
- Preferred when: Outcome checks improve accessibility/usability.
- Avoid when: Treating stylistic preference as a blocker.
- Availability check: Resolve the exact host skill ID/path and provider; check native invocation permission. A directory alone proves neither invocation nor use.
- Invocation method: Load the selected actual SKILL.md through the host-supported skill mechanism, then only relevant references. Do not bypass explicit-only restrictions via file reads.
- First-call/preflight: Read applicable project constraints and current evidence first.
- Fallback: Apply existing Andino/project quality rules to the relevant output without claiming external Anti-Slop use.
- Coexistence/conflicts: Quality filter complements accepted design and selected methodology; never overrides user direction, accessibility or UI coexistence. Core does not imply all subskills.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Record resolved ID/path/provider, actual load and task-relevant result. Similar reasoning or a mention is not evidence of use.
- Activation policy: CONDITIONAL_AUTO

## antislop-layoutmobile

- Type: skill
- Family/provider: Anti-Slop
- Aliases: none
- Primary purpose: Responsive/mobile quality
- Trigger: Mobile/responsive generated layout is in scope.
- Preferred when: Check actual viewports and behavior.
- Avoid when: Irrelevant mobile audit of a non-UI task.
- Availability check: Resolve the exact host skill ID/path and provider; check native invocation permission. A directory alone proves neither invocation nor use.
- Invocation method: Load the selected actual SKILL.md through the host-supported skill mechanism, then only relevant references. Do not bypass explicit-only restrictions via file reads.
- First-call/preflight: Read applicable project constraints and current evidence first.
- Fallback: Apply existing Andino/project quality rules to the relevant output without claiming external Anti-Slop use.
- Coexistence/conflicts: Quality filter complements accepted design and selected methodology; never overrides user direction, accessibility or UI coexistence. Core does not imply all subskills.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Record resolved ID/path/provider, actual load and task-relevant result. Similar reasoning or a mention is not evidence of use.
- Activation policy: CONDITIONAL_AUTO

## antislop-code

- Type: skill
- Family/provider: Anti-Slop
- Aliases: none
- Primary purpose: Code/comment hygiene
- Trigger: Generated comments or code clutter need cleanup.
- Preferred when: Remove actual redundant comments/boilerplate in scope.
- Avoid when: Unrelated code cleanup or unproved behavior changes.
- Availability check: Resolve the exact host skill ID/path and provider; check native invocation permission. A directory alone proves neither invocation nor use.
- Invocation method: Load the selected actual SKILL.md through the host-supported skill mechanism, then only relevant references. Do not bypass explicit-only restrictions via file reads.
- First-call/preflight: Read applicable project constraints and current evidence first.
- Fallback: Apply existing Andino/project quality rules to the relevant output without claiming external Anti-Slop use.
- Coexistence/conflicts: Quality filter complements accepted design and selected methodology; never overrides user direction, accessibility or UI coexistence. Core does not imply all subskills.
- Mutation/permission boundary: Skill loading grants no new action authority. Local changes must serve authorized scope; external, destructive or live mutations require applicable user authorization.
- Verification requirement: Record resolved ID/path/provider, actual load and task-relevant result. Similar reasoning or a mention is not evidence of use.
- Activation policy: CONDITIONAL_AUTO

## context7

- Type: MCP
- Family/provider: Upstash Context7
- Aliases: Context7; context7 MCP
- Primary purpose: Current/version-specific library docs
- Trigger: Unresolved version-sensitive library/framework/API behavior.
- Preferred when: Local dependency version plus authoritative current docs resolve the contract.
- Avoid when: Repeated queries for reliably known local facts without freshness need.
- Availability check: Discover resolve_library_id/query_docs or installed equivalents and native tool permission.
- Invocation method: Resolve library identity then query_docs with actual version/library ID; skip resolve only when valid ID supplied.
- First-call/preflight: Read package/lock/version evidence first; never send secrets/proprietary code in queries.
- Fallback: Current official docs or locally bundled version docs; disclose remaining freshness gap.
- Coexistence/conflicts: Methodology skill may complement documentation instrument.
- Mutation/permission boundary: Read-only retrieval does not authorize project or service mutation.
- Verification requirement: Record actual resolved ID/version, query and relevant sourced result.
- Activation policy: AUTO

## playwright-mcp

- Type: MCP
- Family/provider: Microsoft Playwright MCP
- Aliases: Playwright MCP; playwright
- Primary purpose: Persistent/exploratory browser interaction
- Trigger: A browser workflow needs persistent state, accessibility-tree inspection or iterative interaction.
- Preferred when: MCP loop materially helps browser verification/exploration.
- Avoid when: Forcing MCP when existing CLI/native browser suffices for throughput.
- Availability check: Discover actual browser_* tools and permissions; verify browser availability.
- Invocation method: Inspect tabs/snapshot, navigate only required fixture/authorized target, interact using observed elements, verify resulting state.
- First-call/preflight: Check target/environment and isolate evaluation fixtures from user tabs/data.
- Fallback: Existing Playwright CLI/test suite or native browser; report if actual browser outcome remains unverified.
- Coexistence/conflicts: One browser surface by default. Add DevTools only for a distinct diagnostic question.
- Mutation/permission boundary: Navigation/form submission and side effects follow actual scope; no live external actions merely for a test.
- Verification requirement: Actual browser actions and resulting snapshot/functional evidence.
- Activation policy: CONDITIONAL_AUTO

## chrome-devtools

- Type: MCP
- Family/provider: Chrome DevTools MCP
- Aliases: Chrome DevTools MCP; chrome_devtools
- Primary purpose: Browser diagnostics
- Trigger: Console/network/performance/trace/runtime evidence is missing.
- Preferred when: Distinct diagnostic data cannot be answered by current browser surface alone.
- Avoid when: Basic navigation already covered by another sufficient surface.
- Availability check: Discover actual page/console/network/performance tools and inspect connection.
- Invocation method: Inspect pages then relevant bounded console/network request or performance trace; inspect details using observed IDs.
- First-call/preflight: Identify affected page/diagnostic question before reads or trace.
- Fallback: Native browser DevTools, existing trace/logs or browser test instrumentation; disclose diagnostic gap.
- Coexistence/conflicts: Playwright can reproduce flow; DevTools can diagnose a different question, not duplicate all actions.
- Mutation/permission boundary: Do not evaluate mutating scripts, submit forms or reload live state without task authorization.
- Verification requirement: Relevant observed request/message/trace plus diagnosis tied to evidence.
- Activation policy: AUTO

## git-mcp

- Type: MCP
- Family/provider: MCP Git server
- Aliases: Git MCP; mcp-server-git
- Primary purpose: Repository operations through MCP
- Trigger: Native Git is unavailable/inadequate, or host policy makes MCP the repository interface.
- Preferred when: MCP provides the required repository evidence under host controls.
- Avoid when: Redundant MCP when native Git already suffices.
- Availability check: Discover actual git_status/diff/log tools and permitted repo path.
- Invocation method: git_status/read diff/log first using actual catalog names; mutations only for explicitly authorized action.
- First-call/preflight: Verify repository path, branch and existing user changes.
- Fallback: Native Git or supplied status/diff artifacts; state inability to verify current state.
- Coexistence/conflicts: Native Git preferred; Git methodology skill is distinct from this instrument.
- Mutation/permission boundary: Add/reset/checkout/branch changes require applicable scope; commit/push/merge/destructive actions require user authorization. GO is not consent.
- Verification requirement: Actual repository status/diff/log; for authorized mutation verify affected state.
- Activation policy: AUTO

## drawio-mcp

- Type: MCP
- Family/provider: Draw.io MCP
- Aliases: Draw.io; @drawio/mcp
- Primary purpose: Editable general diagrams
- Trigger: Requested editable architecture/process/flow/sequence artifact suits Draw.io.
- Preferred when: XML/CSV/Mermaid conversion or editable diagram is the desired output.
- Avoid when: Simple prose explanation or formal model semantics requiring StarUML.
- Availability check: Discover supported open/read/write/conversion tools; confirm output mechanism.
- Invocation method: Existing file: list_pages then get_page; creation: exact supported XML/CSV/Mermaid tool; edit only requested page and read back.
- First-call/preflight: Inspect existing diagram or supplied relationships and requested format.
- Fallback: Local editable .drawio XML or agreed Mermaid artifact; disclose editor/opening limits.
- Coexistence/conflicts: Choose artifact semantics, not both diagram systems automatically.
- Mutation/permission boundary: Local artifact creation may be implied by request; opening external editor/upload/publishing follows actual tool behavior and user scope.
- Verification requirement: Read-back editable artifact/page structure; editor opening alone does not prove saved content.
- Activation policy: CONDITIONAL_AUTO

## staruml-mcp

- Type: MCP
- Family/provider: StarUML MCP
- Aliases: StarUML; staruml-mcp-server
- Primary purpose: Formal UML/model operations
- Trigger: Formal UML, model inspection or supported code/model synchronization is required.
- Preferred when: Class/sequence/component model semantics are required.
- Avoid when: General picture suitable for Draw.io or unsupported model-to-code features.
- Availability check: Discover actual inspection/generation/image and supported synchronization tools; verify application/model readiness.
- Invocation method: Inspect current/all diagrams; generate requested model via supported schema; read diagram/model/image back.
- First-call/preflight: Identify actual model/diagram and supported UML operation before mutation.
- Fallback: Local UML model specification or agreed UML text; disclose missing native model verification.
- Coexistence/conflicts: Draw.io for general editable visual diagrams, StarUML for formal model semantics.
- Mutation/permission boundary: Changing an open model or generating code requires applicable request; no unsolicited model replacement.
- Verification requirement: Actual model/diagram read-back, plus code validation if code generated.
- Activation policy: CONDITIONAL_AUTO

## premiere-pro-mcp

- Type: MCP
- Family/provider: Adobe Premiere Pro MCP
- Aliases: Premiere Pro; premiere_pro
- Primary purpose: Premiere project/timeline operations
- Trigger: Actual Premiere project/media/timeline work or readiness testing is requested.
- Preferred when: Premiere project operation needs connected bridge and exact editing schema.
- Avoid when: Explanation/how-to request; unrelated media operations.
- Availability check: Discover verify_premiere_connection, search_tools/get_tool_schema/invoke_tool and actual installed version.
- Invocation method: Verify connection; inspect project/sequence; search deferred tools and schema; focused authorized mutation; read affected state back.
- First-call/preflight: verify_premiere_connection first. For readiness-only checks use launchIfNeeded:false when supported. Do not assume app/bridge/project readiness. Stop on retry:false/userActionRequired:true and communicate nextStep verbatim.
- Fallback: Give local procedure/project evidence requirements; checkpoint unavailable bridge instead of issuing edits.
- Coexistence/conflicts: Skill editing methodology complements MCP; no generic media tool replaces verified project state.
- Mutation/permission boundary: Launching application and project mutations follow actual request. A how-to question grants neither. No export/overwrite/publish without applicable authorization.
- Verification requirement: Connection response, observed project/sequence IDs, exact invoked tool and read-back affected state.
- Activation policy: PERMISSION_GATED

## cheatengine-mcp

- Type: MCP
- Family/provider: Cheat Engine MCP bridge
- Aliases: Cheat Engine; cheatengine-mcp-bridge
- Primary purpose: Authorized local memory/debug inspection
- Trigger: Authorized local debugging/reverse engineering/trainer or memory research needs the bridge.
- Preferred when: Ordinary debugger is insufficient and process scope is legitimate/authorized.
- Avoid when: Unrelated application debugging with sufficient ordinary tools.
- Availability check: Discover actual bridge ping and read tools; verify connectivity and target identity.
- Invocation method: Actual ping/connectivity preflight, inspect target/process identity, bounded read/inspect, then only specifically authorized changes and read-back.
- First-call/preflight: Never assume connection; do not attach/change target, start process or enable shell capability implicitly.
- Fallback: Ordinary debugger or supplied dump/log; state missing live memory evidence.
- Coexistence/conflicts: Use existing ordinary tooling when sufficient; selected skill grants no process mutation authority.
- Mutation/permission boundary: Memory writes, protection changes, code/DLL injection, process manipulation, shell/code execution and destructive actions require applicable explicit authorization and platform safety controls. Never auto-enable dangerous shell.
- Verification requirement: Connection/target evidence and bounded observed memory results; mutation read-back only when separately authorized.
- Activation policy: PERMISSION_GATED

## native-capabilities

- Type: native
- Family/provider: Active host/project
- Aliases: filesystem; search; shell; Git; browser; tests
- Primary purpose: Existing bounded local evidence
- Trigger: Native facilities already satisfy the unresolved need.
- Preferred when: Local search/read/test or Git is sufficient and permitted.
- Avoid when: Native interface lacks required access or trustworthy evidence.
- Availability check: Check actual exposed tools and project commands, not product-name assumptions.
- Invocation method: Use the smallest relevant read/search/check through native tool schema.
- First-call/preflight: Inspect applicable path/environment scope and preserve user changes.
- Fallback: Select relevant invokable instrument; if none, identify minimum missing access.
- Coexistence/conflicts: Prefer native sufficient operations over duplicate MCP calls.
- Mutation/permission boundary: Host permissions and applicable user scope remain authoritative.
- Verification requirement: Actual output and affected outcome; a planned command is not execution.
- Activation policy: AUTO

## Sources and version limits

Contracts use inspected installed skill IDs and actual host tool metadata. Upstream reference points: [Superpowers](https://github.com/obra/superpowers), [Agent Skills](https://github.com/addyosmani/agent-skills), [Ponytail](https://github.com/DietrichGebert/ponytail), [Claude-Mem](https://cmem.ai/), [Impeccable](https://github.com/pbakaus/impeccable), [Taste](https://www.tasteskill.dev/), [Cloner](https://github.com/JCodesMore/ai-website-cloner-template), [Graphify](https://graphify.net/), [Anti-Slop](https://github.com/miqdadbadjuber/anti-slop), [Context7](https://github.com/upstash/context7), [Playwright](https://github.com/microsoft/playwright-mcp), [DevTools](https://github.com/ChromeDevTools/chrome-devtools-mcp), [Git MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/git), [Draw.io](https://www.npmjs.com/package/@drawio/mcp), [StarUML](https://www.npmjs.com/package/staruml-mcp-server), [Premiere](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP), [Cheat Engine](https://github.com/miscusi-peek/cheatengine-mcp-bridge). These links identify upstreams, not installed versions or universal tool names. Refresh the selected contract from actual host schemas when version drift matters.


## search-first

- Type: skill
- Family/provider: AI-RULES; adapted from ECC by Affaan Mustafa
- Aliases: search-first; resolve actual installed provider
- Primary purpose: Research existing solutions and recommend ADOPT, EXTEND, COMPOSE or BUILD
- Trigger: Meaningful reusable-solution, integration, unfamiliar/version-sensitive API, reported-problem, maintenance or alternatives uncertainty; explicit technical research
- Preferred when: Research can materially change an implementation decision; local reuse is considered first
- Avoid when: Trivial edits, greetings, settled conventions, sufficient known explanations or root-cause debugging alone
- Availability check: Resolve actual installed search-first metadata/path and native invocation permissions; setup dependency is not activation
- Invocation method: Load actual selected SKILL.md through the host contract; never bypass manual-only or deny controls
- First-call/preflight: Inspect relevant local/version constraints, sanitize external context and load the specialist online playbook when needed; resolve actual authorized tool schemas, native first
- Fallback: Sufficient native/local evidence; state unavailable external research and unresolved claims without invented use
- Coexistence/conflicts: Andino owns lifecycle; Focus communication; systematic-debugging root cause; Rescue stabilization; Skripsi academic research; Context7/docs are sources
- Mutation/permission boundary: Read-oriented research adds no installation, credential, paid-service, external-write or configuration permission; reuse valid task authorization
- Verification requirement: Actual load, actual authorized search/read actions for material external uncertainty, useful source/version findings and decision effect; discovery, execution and success are separate; preserve offline/denied/failed/insufficient limits
- Activation policy: CONDITIONAL_AUTO

## focus

- Type: skill
- Family/provider: AI-RULES
- Aliases: none
- Primary purpose: Clear, concise, actionable communication without losing important information.
- Trigger: Every Andino invocation, including DIRECT and EPHEMERAL work.
- Preferred when: Andino is active or the user requests Focus independently.
- Avoid when: The user explicitly overrides the preference; never override higher instructions or output requirements.
- Availability check: Resolve the actual installed focus entry and native invocation permissions; setup supplies the dependency.
- Invocation method: Activate the actual SKILL.md through the host contract; reuse valid activation evidence.
- First-call/preflight: Check whether the current Focus instructions are already loaded; load once if permitted and needed.
- Fallback: Report missing or denied activation briefly and continue authorized work without claiming Focus use.
- Coexistence/conflicts: Complements A. PRIORITAS; Andino remains lifecycle owner. Do not duplicate the prompt body.
- Mutation/permission boundary: Communication only; no new authority or limits on task execution.
- Verification requirement: Distinguish actual loading and applied output from a name mention or installation record.
- Activation policy: AUTO


## council

- Type: skill
- Family/provider: AI-RULES first-party; adapted from aiwithremy/claude-skills-llm-council
- Aliases: council; do not assume the upstream llm-council ID is an installed alias
- Primary purpose: Pressure-test meaningful decisions using five independent advisor lenses, anonymized peer critique, and an actionable synthesized recommendation.
- Trigger: An explicit Council request for a meaningful decision, or a consequential choice with real uncertainty and competing options.
- Preferred when: Independent perspectives can expose material trade-offs, overlooked assumptions or execution risks before a decision.
- Avoid when: Trivial choices, simple facts, summaries, ordinary drafting, straightforward fixes, or explicit exclusion by the user.
- Availability check: Resolve the installed Council entry, native skill invocation permissions and independent sub-agent availability; discoverability does not prove execution.
- Invocation method: Invoke the actual installed council skill through the host's authorized skill mechanism, honoring manual-only or denied invocation controls.
- First-call/preflight: Frame the decision neutrally using known objectives, alternatives, stakes, constraints and verified evidence; ensure context sharing is authorized before delegating.
- Fallback: If independent delegation is unavailable, give a clearly labeled single-agent perspective review without claiming independent advisor or peer-review execution.
- Coexistence/conflicts: Andino retains sole task routing, lifecycle and checkpoints; Focus controls Indonesian/English communication; Council owns advisory deliberation and returns a verdict, not a second plan.
- Mutation/permission boundary: A Council verdict provides no authority for repository changes, external actions, paid services, publication or other mutations; host and user permissions still apply.
- Verification requirement: Distinguish actual independent advisor/reviewer invocations from simulated perspectives; preserve evidence, material disagreement and unresolved uncertainty in the final verdict.
- Activation policy: CONDITIONAL_AUTO


## threejs-skills

- Type: skill
- Family/provider: AI-RULES Three.js family; user-supplied domain collection, no blanket upstream endorsement
- Aliases: none; internal method IDs identify bundled guides, not native skill aliases
- Primary purpose: On-demand domain methods for Three.js scenes, rendering, games and NixieFX effects
- Trigger: A current unresolved domain need matching one of the actual specialists
- Preferred when: Scene/shader/light/material/geometry/animation/interaction or particle expertise materially helps
- Avoid when: Ordinary frontend work, inventory-only mentions, unknown-cause diagnosis before debugging, or no matching need
- Availability check: Resolve installed threejs-skills, path, provenance and host controls; verify selected bundled guides and resource permissions
- Invocation method: Invoke threejs-skills through the native host contract, then read only selected skills/<method-id>/GUIDE.md resources; explicit method names are supported
- First-call/preflight: Load the family SKILL.md, inspect actual project versions, and load the minimum relevant authorized guides; never all methods automatically
- Fallback: Missing or denied specialists are UNAVAILABLE; use sufficient native/project methods and record the limit without claiming skill use
- Coexistence/conflicts: Andino owns lifecycle and one plan; Focus communication; Search First relevant research; domain router and game director recommend within that owner
- Mutation/permission boundary: No implicit installs, paid API calls, delegation, publication or permission bypass
- Verification requirement: Record actual activation plus domain action for USED; browser rendering/performance/interaction claims need observed evidence, otherwise NOT_VERIFIED
- Activation policy: CONDITIONAL_AUTO
