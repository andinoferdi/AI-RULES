# Bidirectional Agent Code Review Protocols

This document defines the bilateral operational contracts for AI coding agents participating in code reviews under Andino Workflow governance. It establishes rigorous guardrails across three roles: **Requesting Review**, **Conducting Review**, and **Receiving Review**.

---

## Protocol 1: Requesting Code Review (Author / Coordinator)

When completing a feature, resolving a bug, or concluding a subagent task, dispatch an isolated reviewer subagent. This keeps the coordinator's context window uncluttered while ensuring adversarial evaluation.

### 1.1 Scope Pinning Invariants
Never dispatch a reviewer with vague references like "check my recent work." Pin the exact byte boundary:
1. **Committed Range:** Resolve `BASE_SHA` and `HEAD_SHA`:
   ```bash
   BASE_SHA=$(git merge-base origin/main HEAD) # or task baseline commit
   HEAD_SHA=$(git rev-parse HEAD)
   ```
2. **Working Tree & Untracked Files:** Explicitly include staged/unstaged changes and newly authored untracked files. A review that only diffs `HEAD~1..HEAD` silently misses uncommitted files.

### 1.2 Subagent Dispatch Template
Dispatch a `general-purpose` subagent using this bounded prompt template:

```markdown
You are a Senior Code Reviewer operating under Andino Workflow governance.
Review the following code changes against specifications and quality standards.
Your review is strictly READ-ONLY. Do not modify files, branches, or git state.

## What Was Implemented
[DESCRIPTION: Brief summary of what was built or changed]

## Requirements & Acceptance Criteria
[PLAN_OR_REQUIREMENTS: Exact task spec or criteria]

## Scope Boundary
- Base Revision: [BASE_SHA]
- Head Revision: [HEAD_SHA]
- Working Tree / Untracked Files: [LIST_OR_NONE]

Inspect the changes using read-only commands:
`git diff [BASE_SHA]..[HEAD_SHA]`
`git show [COMMIT_SHA]`

## Core Principles to Enforce:
1. "The Spec is a Vision Document": The spec defines what the software must do. It cannot enumerate every edge condition. Where the spec is silent, evaluate what a reasonable user or caller expects. Silence is not permission to break invariants or introduce security flaws.
2. Dual-Track Separation: Evaluate Spec Axis (functional requirements) and Standards Axis (code health, security, smells) independently. Do not let clean style excuse functional errors.
3. Mandatory "Declined to Judge": Before issuing your verdict, list every behavior or file you considered and set aside as outside the scope, along with your technical justification. An empty list means you set nothing aside.
4. Actionable Severity: Use severity prefixes: `[CRITICAL]`, `[REQUIRED]`, `[SUGGESTION]`, `[NIT]`. Every finding must cite `file:line`, concrete triggering condition, consequence, and a named structural remedy.
```

---

## Protocol 2: Conducting Isolated Review (Reviewer Subagent)

### 2.1 Read-Only Execution Boundary
- The reviewer must **never mutate** the repository.
- Do not run commands that alter state (`git checkout`, `git reset`, `git commit`, `rm`, file edits).
- If checking out a different tree is required, use disposable worktrees or read-only tree inspections (`git show`).

### 2.2 Two-Axis Evaluation Framework
Every review must evaluate and report findings under two distinct headings:

```markdown
## 1. Spec Axis (Requirements & Behavior)
- Does the code implement all acceptance criteria?
- Are boundary conditions, null/empty states, and error handling complete?
- Do the accompanying tests verify actual business behavior rather than implementation mocks?
- Is there any unintended scope addition or missing functional logic?

## 2. Standards Axis (Health, Security, Architecture, & Performance)
- Correctness & Safety: Any security vulnerabilities (see checklists.md)?
- Architecture & Smells: Does the change introduce any of the 12 Fowler smells?
- Performance: Any N+1 queries, unbounded loops, or memory leaks?
- Readability & Simplicity: Could this be done with fewer concepts or simpler control flow?
```

### 2.3 Severity Prefix Taxonomy
Label every comment with an explicit prefix to establish clear actionability:

| Prefix | Meaning | Author Action Required |
|---|---|---|
| `[CRITICAL]` | Blocker: Security flaw, data loss/corruption, crash regression | Must resolve before merge |
| `[REQUIRED]` | Blocker: Spec violation, broken edge case, hard project standard breach | Must resolve before merge |
| `[SUGGESTION]` | Non-blocking: Structural remedy, abstraction simplification, readability | Author evaluates; encouraged |
| `[NIT]` | Non-blocking: Minor typo, cosmetic comment cleanup, trivial style | Optional; author may defer |
| `[FYI]` | Informational: Architectural context, future milestone note | No action required |

*Rule:* Cap cosmetic nits at a maximum of **3 per pass** to prevent review fatigue and focus attention on high-leverage defects.

### 2.4 Providing Named Structural Remedies
Never submit a vague critique like *"This method is messy"* or *"Consider refactoring."* Provide the named structural remedy:
- **Problem:** Repeated if/else checks on an entity's status string.
  - **Remedy:** *Replace Conditional with Typed Dispatcher* or *Lookup Map*.
- **Problem:** Method accesses internal fields of another object 5 times.
  - **Remedy:** *Move Method to Data Owner* (resolving Feature Envy).
- **Problem:** Function takes 6 primitive parameters that travel together.
  - **Remedy:** *Introduce Parameter Object / Typed Interface* (resolving Data Clump).

---

## Protocol 3: Receiving Code Review (Author / Implementer)

### 3.1 Anti-Sycophancy & Forbidden Responses
AI agents receiving feedback frequently fall into performative sycophancy, agreeing with hallucinated or inaccurate feedback.
**Strictly Forbidden Responses:**
- ❌ *"You're absolutely right!"*
- ❌ *"Great catch! Excellent point!"*
- ❌ *"Thank you for the brilliant suggestion, implementing now!"*

**Required Mindset:**
- Technical verification over emotional agreement.
- Do not start editing code until the critique has been verified against the codebase.
- Actions and tests speak louder than flattering words.

### 3.2 The 6-Step Reception Workflow
When feedback arrives:
```
1. READ: Ingest the complete review without defensive or eager reactions.
2. UNDERSTAND: Restate the technical requirement or invariant in your own words.
3. VERIFY: Check the claim against the codebase reality (run tests, grep calls, inspect schema).
4. EVALUATE: Is the remedy technically sound for THIS codebase and architecture?
5. RESPOND: Acknowledge valid findings or push back with technical evidence.
6. IMPLEMENT: Apply fixes one item at a time, each backed by a covering test.
```

### 3.3 1-Cycle Deadlock Prevention & Technical Pushback
If a reviewer flags an issue that is factually incorrect, hallucinated, or violates project constraints:
1. **Never Loop in Endless Debate:** Issue exactly **one** technical pushback containing concrete proof:
   - Citing passing regression test output.
   - Citing language specification or library documentation.
   - Demonstrating why the suggested change breaks existing invariants or introduces regression.
2. **Pushback Format:**
   ```markdown
   Pushback on [file:line]:
   The review noted that `calculateDiscount` fails when `rate == 0`.
   However, line 14 explicitly guards `if (rate <= 0) return 0;`, verified by
   unit test `test_zero_rate_returns_zero` in `tests/test_pricing.py:28`.
   Proceeding with implementation as-is.
   ```
3. **Escalation Boundary:** If the reviewer or peer insists on a disputed point after 1 cycle of technical pushback, halt autonomous modification and escalate directly to the human user or workflow coordinator. Do not loop.

### 3.4 YAGNI Filter for Speculative "Professional" Enhancements
If a reviewer suggests adding abstractions, configuration layers, or generic interfaces for future flexibility:
1. Grep the codebase for actual current usage.
2. If only one call site exists or the feature is uncalled, reject the addition:
   *"Applying YAGNI: This helper currently serves a single internal call site. Introducing a plugin registry adds indirection without current architectural justification."*
