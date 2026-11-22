# Context Budget Management and Packing Strategies

Context is the single largest lever governing the precision, correctness, and reasoning fidelity of AI agents. A context window is not a filing cabinet for cold storage; it is an active working desk. Every extraneous token loaded onto the desk competes directly for attention bandwidth, dilutes instruction compliance, and increases the probability of hallucination.

This guide provides concrete mathematical heuristics, architectural strategies, and operational protocols for managing context budgets and packing information efficiently.

---

## 1. The Context Budget Mental Model

### Working Desk vs. Filing Cabinet

| Property | Working Desk (Active Context) | Filing Cabinet (Filesystem / Disk) |
|---|---|---|
| **Purpose** | Immediate active reasoning, active diff generation, and error resolution. | Permanent reference, test fixtures, historical transcripts, and documentation. |
| **Cost** | Consumes finite KV cache, attention compute, and prompt token budget every turn. | Zero attention cost until explicitly read. |
| **Decay** | Susceptible to attention dispersion, token pollution, and retrieval loss. | Immune to attention decay; static byte-level permanence. |
| **Optimal Size** | Lean: strictly under 2,000 lines (<15k-20k tokens) of task-relevant material. | Unbounded. |

### The Attention Competition Law (Softmax Zero-Sum)
Transformer attention mechanisms normalize relevance weights across all tokens in the sequence using softmax:
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Because the sum of softmax probabilities equals 1.0, every irrelevant line of stack trace, lockfile noise, or obsolete conversation history directly cannibalizes attention weight from your critical system constraints and acceptance criteria. Context window size does not equal attention capacity. A model with a 200,000-token window performs dramatically better when fed 4,000 curated tokens than when saturated with 100,000 tokens of unfiltered data.

### Proactive Compaction Discipline (Empirical 70% Heuristic)
Never wait until the context window is near exhaustion before trimming. As token usage approaches roughly 70-75% of harness capacity (or when context degrades):
1. Retrieval accuracy drops sharply for mid-context information.
2. The agent begins "forgetting" secondary rules or styling conventions.
3. Emergency auto-compaction triggers, which summarily discards nuanced historical decisions.

**Rule**: Compact, prune, or hand off to a fresh session as soon as context approaches saturation or after 15-20 turns on a complex task. Specific line ceilings (<2,000 lines) and percentages (70%) are empirical sizing heuristics, not host-independent universal limits.

---

## 2. Token & Noise Sanitization Protocols

Unsanitized raw tool outputs represent the fastest vector for context pollution. Apply these deterministic filters before inserting evidence into the agent's view.

### Log and Stack Trace Collapsing

**Problem**: A test failure emits 400 lines of framework internals, database connection teardowns, and dependency tracebacks.
**Protocol**: Strip the cascade and preserve only the failing assertion, file/line anchor, and direct cause.

```
WASTEFUL (350 lines):
npm test
... 120 lines of Jest runner setup ...
FAIL src/services/billing.test.ts
  ● BillingService › should apply tier discount
    TypeError: Cannot read properties of undefined (reading 'rate')
      at BillingService.calculateDiscount (src/services/billing.ts:84:22)
      at Object.<anonymous> (src/services/billing.test.ts:42:19)
      at Promise.then.completed (node_modules/jest-circus/build/utils.js:298:28)
      ... 200 lines of node_modules internal call stack ...
Test Suites: 1 failed, 1 total
Tests:       1 failed, 4 passed, 5 total
Snapshots:   0 total
Time:        4.215 s

EFFECTIVE (5 lines):
Test Failure in src/services/billing.test.ts:
FAIL: BillingService › should apply tier discount
Error: TypeError: Cannot read properties of undefined (reading 'rate')
Anchor: src/services/billing.ts:84:22
Target: customer.tier is undefined when calculateDiscount() is invoked without explicit user profile.
```

### Compiler Cascades
When a build breaks, compilers (such as `tsc` or `cargo`) often emit dozens of downstream errors caused by a single upstream missing type or syntax error.
- **Rule**: Extract only the first 2-3 root diagnostic messages. Discard the remaining cascading failures until the root is patched.

### Diff and File Sanitization
Before feeding diffs or tree listings to an agent:
1. **Exclude Lockfiles**: Always exclude `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`, and `Gemfile.lock`. These contain thousands of lines of machine-generated hash deltas with zero semantic value for code editing.
2. **Exclude Generated Assets**: Exclude compiled `.js.map`, `.d.ts` bundles, minified bundles, and binary files.
3. **Bound File Trees**: Never run recursive `ls -R` or unconstrained directory listings across `node_modules`, `.git`, or build outputs. Use targeted file pattern matching (`glob` or `find` with max depth).

---

## 3. The Three Packing Strategies

Tailor how context is packaged based on the task lifecycle phase.

### Strategy A: The Brain Dump (Intake & Kickoff)
Use when initiating a significant feature or starting an empty workspace. Consolidate architecture, requirements, and constraints into a single structured, high-density block:

```markdown
PROJECT CONTEXT:
- Stack: TypeScript 5.5, Next.js 15 (App Router), Tailwind CSS 4, Prisma ORM
- Runtime: Node.js 22 LTS, PostgreSQL 16
- Target Feature: User multi-factor authentication (TOTP)

BOUNDARIES & CONSTRAINTS:
- Use standard Web Crypto APIs; do not introduce external C-native crypto libraries.
- Store encrypted secrets using AES-256-GCM with keys loaded from environment variables.
- All database migrations must be reversible.

RELEVANT CODE ANCHORS:
- Existing Auth Schema: src/db/schema.prisma:45-80
- Session Middleware: src/middleware/auth.ts:12-40
- Route Handler: src/app/api/auth/route.ts

ESTABLISHED PATTERNS:
- See src/lib/crypto/tokens.ts:20-55 for our existing token hashing convention.
```

### Strategy B: The Selective Include (Surgical Edit & Debug)
Use for targeted bug fixes, refactorings, or narrow enhancements. Include only the file under edit, its immediate test, and the exact type interface:

```markdown
TASK: Resolve null pointer when user has no billing address in invoice generator.

PRIMARY FILE:
- src/services/invoice.ts (lines 110-150: formatBillingAddress)

TEST FILE:
- tests/services/invoice.test.ts (lines 45-68: test 'generates invoice without address')

TYPE DEFINITIONS:
- src/types/customer.ts (interface CustomerProfile, Address)

CONSTRAINTS:
- Do not alter the CustomerProfile interface shape (used by external API consumers).
- Return "No billing address on file" as fallback string when address is null.
```

### Strategy C: The Hierarchical Project Map (Complex Codebases)
For large monorepos or systems exceeding 20,000 lines of code, maintain a compact, human-readable system map in docs. Agents load only the section mapping to their active subsystem:

```markdown
# Repository Subsystem Map

## Identity & Session (`src/auth/`)
- Responsibility: User registration, JWT issuance, session validation, OAuth2 flows.
- Key Interfaces: `AuthManager` (`src/auth/manager.ts`), `SessionToken` (`src/auth/types.ts`).
- Rules: Routes wrapped with `requireAuth()`, passwords hashed with Argon2id.

## Data Access Layer (`src/db/`)
- Responsibility: Prisma client configuration, transaction wrappers, repositories.
- Key Interfaces: `UserRepository` (`src/db/users.ts`), `BillingRepository` (`src/db/billing.ts`).
- Rules: No raw SQL queries outside designated repository files; all updates transactional.

## API Gateway & Handlers (`src/app/api/`)
- Responsibility: HTTP routing, Zod payload validation, error transformation.
- Rules: Handlers must catch domain errors and translate to standardized JSON error responses.
```

---

## 4. Positional Encoding & Lost-in-the-Middle Recency Ordering

Transformer architectures process tokens with positional embeddings (e.g. RoPE or sinusoidal). Research on long-context retrieval (Liu et al., 2023, *Lost in the Middle*) proves that models attend with highest fidelity to:
1. The **Beginning (Primacy Effect)**: The very start of the prompt sequence.
2. The **End (Recency Effect)**: The final tokens directly preceding generation.

Information placed in the middle of a large context window suffers severe attention attenuation.

```
HIGH ATTENTION                 ATTENTION DEAD ZONE                 MAX ATTENTION
┌───────────────────────────┬─────────────────────────────────┬───────────────────────────┐
│ Primacy Zone              │ Middle Attenuation Zone         │ Recency Zone              │
│ (Tokens 0 - 2,000)        │ (Tokens 2,001 - N-1,000)        │ (Final 1,000 Tokens)      │
├───────────────────────────┼─────────────────────────────────┼───────────────────────────┤
│ System Invariants         │ Background reference docs       │ Active Task Prompt        │
│ Harness Rules (CLAUDE.md) │ Non-critical source files       │ Current Failing Error     │
│ Security/Safety Guards    │ Broad directory schemas         │ Immediate Next Action     │
│ Core Architectural Bounds │ Historical conversation turns   │ Explicit Output Schema    │
└───────────────────────────┴─────────────────────────────────┴───────────────────────────┘
```

### The 3-Tier Placement Law
1. **Head (Primacy)**: Place stable rules, security boundaries, and project-wide contracts at the very top.
2. **Middle (Background)**: Place reference code, types, and supporting documentation in the center.
3. **Tail (Recency)**: Always pin the immediate instruction, the exact failing assertion/error, and required output constraints at the very bottom, immediately before the completion trigger.

---

## 5. Prefix-Stable KV-Cache Alignment

Modern frontier model APIs (such as Anthropic Claude, OpenAI, and cloud hosted gateways) utilize **Prompt Caching** (KV-cache reuse) to reduce latency and token costs by up to 90%.
Prompt caching operates by hashing the sequence of tokens from index 0 forward. As soon as a single character differs, the entire subsequent cache is invalidated.

### Rules for Cache Preservation
1. **Static Head Principle**: Keep system instructions, tool definitions, and project rules files completely static and identical across every turn.
2. **Never Insert Ephemeral Variables at the Top**: Never put timestamps (`Date.now()`), random session UUIDs, or dynamic status lines at the start of your prompt.
3. **Append-Only History**: Structure conversations so that previous turns remain byte-exact, appending new interactions to the tail.

```
OPTIMAL (Cache Hit: 95%+):
[Tokens 0 - 8,000: STATIC]  CLAUDE.md + Architecture Specs + Tool Definitions (CACHED)
[Tokens 8,001 - 12,000: HIST] Prior turn Q&A (CACHED)
[Tokens 12,001 - 13,500: NEW] Current task + New error output (UNCACHED DELTA)

BROKEN (Cache Hit: 0%):
[Token 0: DYNAMIC] "Current Time: 2026-11-01 14:32:05" -> INVALIDATES ALL CACHE
[Tokens 1 - 8,000] Static rules re-processed and re-billed on every single turn!
```

---

## 6. Multi-Turn Compaction & Pruning Matrix

When a session extends beyond 8-10 turns, perform proactive compaction using the following triage rules:

### What to Cut First vs. What to Protect

| Category | Action | When to Apply | Rationale |
|---|---|---|---|
| **Resolved Debug Trials** | CUT | As soon as root cause is identified. | The dead ends are irrelevant; only the resolution matters. |
| **Verbose Tool Outputs** | CUT | Immediately after extracting the finding. | 200 lines of `grep` or `find` output become deadweight once the path is known. |
| **Outdated File Versions** | CUT | On file update or save. | The filesystem contains the true source; older draft snippets cause hallucinations. |
| **Conversational Chit-chat** | CUT | When agreement is reached. | Politeness phrases waste tokens without informing technical execution. |
| **Core Constraints & Rules** | PROTECT | Never cut. | Project boundaries, type-safety, and auth rules must remain active throughout. |
| **Active Failing Assertion** | PROTECT | Protect until verified GREEN. | The exact error message is the primary target for the debugging loop. |
| **File Being Modified** | PROTECT | Protect current byte state. | The agent must have the exact current code anchor to produce clean diffs. |
| **Accepted Spec & Plan** | PROTECT | Protect in durable markdown plan. | Single source of truth across turns. |

### The "Compress Before Dropping" Discipline
Never delete context silently without leaving an anchor. Replace verbose exploratory blocks with a one-sentence summary:

```markdown
BEFORE (45 lines of trial-and-error logs):
- Attempted import from 'crypto' -> failed (unsupported in Edge runtime).
- Attempted import from 'node:crypto' -> failed (browser compatibility issue).
- Checked Cloudflare Workers docs -> recommended Web Crypto API crypto.subtle.

AFTER COMPRESSION (1 sentence breadcrumb):
- Root cause: Edge runtime requires Web Crypto API `crypto.subtle`; Node.js crypto modules rejected.
```
