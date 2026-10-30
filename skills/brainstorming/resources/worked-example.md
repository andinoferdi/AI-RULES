# Brainstorming: Worked Procedure, Design Patterns, and Diagnostic Rubric

This resource provides an end-to-end before-and-after case study, the canonical written design document template, the subagent builder-check protocol, visual spike guidelines, cognitive bias red flags, and a 6-point diagnostic self-audit rubric for `andino-brainstorming`.

---

## 1. Case Study: Before and After Transformation

### Scenario
A user states: *"I want to build a webhook ingestion service for our SaaS platform so customers can stream payment and dispute events to our system, but I'm not sure how to structure it reliably."*

---

### The Anti-Pattern: Hasty, Superficial Ideation (Before)

```text
AI: Great idea! Webhooks are super important. We can build this using Node.js and Express.

Here is a plan:
1. Setup an Express server.
2. Create a POST /webhooks endpoint.
3. Validate the payload using a secret header.
4. Insert the event into PostgreSQL.
5. If there's an error, return 500.

Do you want me to start writing the code now? Or we could also use serverless functions. What do you think?
```

#### Why this fails:
1. **Premature Implementation:** Jumps straight to proposing technology stacks and offer to write code before discovering volume, delivery guarantees, latency requirements, or failure modes.
2. **Greedy Single-Path Proposing:** Picks Express + Postgres without exploring trade-offs against serverless, queues, or distributed ingestion patterns.
3. **Missing Negative Scope:** No mention of non-goals, anti-goals (e.g., synchronous webhook processing blocking callers, replay vulnerabilities).
4. **Vague Hand-waving:** Offers "serverless functions" as a throwaway buzzword without architectural comparison.
5. **Burden on User:** Asks vague questions ("What do you think?") that force the user to do the architectural heavy lifting.

---

### The Elevated Pattern: Adaptive Socratic Grounding & Approaches (After)

#### Turn 1: Grounding & Single High-Leverage Question
```text
AI: Ingesting payment and dispute events reliably means prioritizing high availability, strict payload validation, and at-least-once delivery without blocking external webhook senders.

Looking at your current repository, we already have Redis for pub/sub and PostgreSQL for billing records. Before touching any infrastructure, the biggest factor shaping this service is throughput and resilience during database downtime:

Are you expecting sporadic bursts (e.g., thousands of events during Black Friday billing runs) that require an intermediate asynchronous queue, or a predictable, low-volume stream where direct database writes with exponential retry are sufficient?
```

#### Turn 2: Pacing & Laying Out the Approaches (Dedicated Turn)
*User responds: "We expect unpredictable bursts—sometimes 5,000 events in 2 minutes. And we cannot lose a single dispute event even if Postgres is restarting for maintenance."*

```text
AI: Understood: zero data loss under database maintenance and burst absorption (5k events/2 min) are hard invariants. 

Here are the three viable architectural approaches for building this:

### Approach A: Fast Ingestion to Redis Stream / Queue Worker
- Architecture: Lightweight edge endpoint (Go or Node/Fastify) validates HMAC signatures and pushes raw payloads directly into a durable Redis Stream or SQS queue. A decoupled worker pool drains the queue into PostgreSQL in micro-batches.
- Pros: Sub-20ms HTTP ack to webhook senders; total isolation from PostgreSQL downtime; natural backpressure handling.
- Trade-offs: Adds worker orchestration complexity; requires monitoring queue lag and handling poison-pill dead-letter queues (DLQ).

### Approach B: Direct Postgres Ingestion with Write-Ahead Transaction Logging
- Architecture: Ingestion endpoint connects directly to PostgreSQL, inserting into an unindexed `raw_webhook_events` staging table within a single fast transaction. A database cron/trigger processes events asynchronously into domain tables.
- Pros: Zero new operational infrastructure; leverages existing Postgres ACID guarantees and backups.
- Trade-offs: Database maintenance or connection pool exhaustion will reject incoming webhooks (senders get 503s); burst traffic degrades primary application DB performance.

### Approach C: Cloud Serverless Ingestion Buffer (EventBridge / Cloudflare Worker + Storage)
- Architecture: Edge serverless function dumps incoming JSON straight to object storage (S3/R2) or an event bus, then triggers internal ingestion hooks.
- Pros: Infinitely scalable buffer; virtually zero server maintenance; highest uptime SLA.
- Trade-offs: Vendor lock-in; higher operational observability boundary across cloud boundaries; harder local development loop.

Recommendation: Approach A is the strongest fit. It honors your existing stack (Redis + Postgres), absorbs 5,000-event spikes effortlessly, and guarantees webhook senders get immediate 200 OKs even when Postgres is unavailable.

Which approach aligns best with your operational constraints?
```

#### Turn 3: User Chooses & Design Doc is Produced
*User selects Approach A.* The AI immediately sizes the work (Full Project), applies the written design contract, runs the internal Builder Check, and presents the completed design document before asking for approval to proceed to planning.

---

## 2. Canonical Written Design Document Template

When transitioning from exploration to a concrete design, use this exact contract. Every section must be populated with substantive, verifiable claims.

```markdown
# Design Document: [Feature / System Name]

**Date:** YYYY-MM-DD  
**Status:** PROPOSED / APPROVED  
**Estimated Size:** Small Change / Project  
**Author:** [Agent & Human Partner]  

---

## 1. Intent & Context
- **Why now:** What problem or business driver initiated this request?
- **User / Stakeholder:** Who relies on this, and what do they experience today?
- **Root Objective:** The fundamental outcome that defines success, independent of specific implementation.

## 2. Goals, Non-Goals & Anti-Goals
- **Goals:**
  - [G-1] Specific, observable capability delivered.
  - [G-2] Measurable performance or reliability target.
- **Non-Goals (Explicitly Out of Scope):**
  - [NG-1] Capabilities deferred to future milestones.
  - [NG-2] Scenarios or edge cases explicitly not handled in this iteration.
- **Anti-Goals (What would make this a failure even if functional):**
  - [AG-1] Failure modes to avoid at all costs (e.g., "Do not introduce blocking sync network calls during webhook ingestion").
  - [AG-2] Architectural degradations prohibited (e.g., "Do not bypass HMAC signature verification even in staging").

## 3. Constraints & Invariants
- **Technical Invariants:** Existing databases, language/framework versions, protocol requirements.
- **Security & Privacy Boundaries:** Required token hashing, secret isolation, sanitization of untrusted payloads.
- **Operational Boundaries:** Maximum allowable memory/CPU, budget limits, deployment targets.

## 4. Evaluated Approaches & Selected Architecture
### Approaches Considered:
1. **Approach 1 ([Name]):** [Brief description, pros, cons, reasons discarded].
2. **Approach 2 ([Selected Name]):** [Selected architecture, why it won, key trade-offs accepted].
3. **Approach 3 ([Name]):** [Alternative considered, reasons discarded].

### Selected Architecture Specification:
- High-level flow and data movement.
- Public boundaries, routes, or interfaces created/modified.
- Error handling, idempotency mechanisms, and dead-letter/reconciliation paths.

## 5. Explicit User Decisions vs. Builder Discretion
- **Decided by Human Partner:**
  - [Decision 1: e.g., Choice of Redis Stream over SQS].
  - [Decision 2: e.g., Retention window of raw webhook payloads (14 days)].
- **Left to Builder Discretion:**
  - [Discretion 1: Internal schema field names for worker state].
  - [Discretion 2: Specific backoff jitter algorithm for retry workers].

## 6. Downstream Handoff & Testability Seeds
- **Verification Strategy:** How will completion be proven? (Unit tests, integration replay, load spike).
- **Handoff Target:** Ready for `andino-specification` (if formal schemas needed) or `andino-planning` / `andino-tdd`.
```

---

## 3. Subagent Builder-Check & Adversarial Review Protocol

Before presenting a full project design document to your human partner, dispatch a fresh general-purpose subagent to evaluate the document from the perspective of an independent, highly critical implementation engineer.

### The Builder-Check Prompt
```markdown
You are a senior, highly pragmatic software engineer who has been handed a design document and asked to implement it completely without talking to the author.

Read [DESIGN_DOCUMENT_PATH].

Report ONLY the blocking questions or ambiguities you would still need resolved before you could build this without guessing:
1. Places where the document is silent on a critical edge case.
2. Contradictions between Goals, Anti-Goals, and Constraints.
3. Unstated assumptions about existing infrastructure, libraries, or network boundaries.
4. Missing failure/error semantics.

Sort your findings into three strict categories:
- ALREADY_ANSWERED: Points that existing repo files or previous sections clarify.
- BUILDER_CALL: Minor engineering decisions that a competent developer can settle independently without altering product intent. (Briefly state the sensible default).
- THEIRS: Ambiguities that ONLY the human stakeholder can answer because they represent product trade-offs or business risk.

If nothing important is missing, respond with: "NO_BLOCKING_AMBIGUITIES_DETECTED".
```

### Triaging the Builder Output
1. Incorporate `ALREADY_ANSWERED` and `BUILDER_CALL` points directly into Section 5 of the design doc ("Left to Builder Discretion").
2. Present the `THEIRS` pile to your human partner in a single, prioritized message *before* finalizing the document approval request.

---

## 4. Visual Spikes & Lightweight Companion Guide

When the core uncertainty of an idea is spatial, visual, or structural, **seeing beats reading**.

### When to Offer a Visual Spike
| Scenario | Terminal (Text) | Visual Spike (Browser / Artifact) |
|---|---|---|
| Page or Component Layout | Vague verbal description of boxes | Standalone HTML wireframe mockup |
| Complex Multi-Step Wizard | Bulleted step list | Interactive click-through state fragment |
| System Architecture / Topology | ASCII text list of arrows | Rendered SVG / Mermaid / Draw.io diagram |
| Data Model / Entity Relationship | Text schema dump | Relational diagram showing foreign keys |
| Algorithmic Trade-off | Mathematical explanation | Working script with terminal benchmarks |

### Rules for Spikes
1. **Offer Just-In-Time:** Never offer a visual companion in the very first turn. Offer it only when a concrete visual/spatial question arises:
   > *"This layout option might be much easier to evaluate visually. Would you like me to generate a standalone HTML mockup you can open in your browser?"*
2. **Throwaway By Default:** Spikes are experimental probes designed to answer a single question. They skip comprehensive testing, edge-case hardening, and production styling.
3. **The Spike Hard Gate:** If a spike produces something the user loves, **never** just keep building on it. Transition formally back to the brainstorming gate: document the learned architecture in the design doc, get approval, and plan the production build via `andino-tdd`.

---

## 5. Cognitive Biases & Anti-Slop Red Flags Table

AI coding agents fall into predictable cognitive traps during ideation. Use this table as an active self-correction filter:

| Agent Thought / Rationalization | The Reality & Correct Action |
|---|---|
| *"I'll immediately give them a menu of 6 frameworks to choose from."* | Options steer and overwhelm. Ask them to describe the problem and motivation in their own words first. |
| *"I'll fill in sensible defaults without mentioning them."* | Silent defaults are unchallengeable decisions. State significant assumptions out loud so the user can reject them. |
| *"They answered my two questions, so I can start coding now."* | Answering questions is not design approval. Lay out 2–3 architectural approaches in a dedicated turn first. |
| *"I'll explain my entire 5-step brainstorming methodology upfront."* | Process jargon creates conversational drag. Just ask the single most incisive question. The process shows itself through quality. |
| *"The user said 'sounds great!' to the general idea, so I'm approved."* | Approval covers the high-level concept, not the architectural details. No code until the structured design doc is signed off. |
| *"The prototype spike works, so I'll just refactor it into production."* | A spike is built without production constraints. Discard or treat as reference; build production code through `andino-tdd`. |
| *"I will offer 3 approaches: 1 sensible one and 2 ridiculous strawmen."* | Strawmen insult the user's intelligence. Every presented approach must be a viable, realistic path with genuine trade-offs. |
| *"I'll ask 4 nested questions in one giant bulleted list."* | Multi-question barrage causes cognitive fatigue. Ask one primary question that unlocks the biggest unknown. |

---

## 6. Empirical Diagnostic Self-Audit Rubric

Before presenting an ideation summary, approach options, or design document, evaluate your output against these 6 dimensions (Target: Minimum 5/6 Pass):

```
┌────────────────────────────────────────────────────────────────────────┐
│               BRAINSTORMING DIAGNOSTIC EVALUATION RUBRIC               │
├────────────────────────────────┬───────────────────────────────────────┤
│ 1. Problem Grounding           │ Stated in user's terms, anchored in   │
│                                │ existing repository facts, no halluc. │
├────────────────────────────────┼───────────────────────────────────────┤
│ 2. Adaptive Conversational     │ No multi-question interrogation;      │
│    Pacing                      │ matches user bandwidth and velocity.  │
├────────────────────────────────┼───────────────────────────────────────┤
│ 3. Divergent Trade-Offs        │ 2-3 genuinely distinct approaches     │
│                                │ with honest, non-strawman trade-offs. │
├────────────────────────────────┼───────────────────────────────────────┤
│ 4. Boundary Hardness           │ Clear negative scope: explicit        │
│                                │ non-goals and anti-goals documented.  │
├────────────────────────────────┼───────────────────────────────────────┤
│ 5. Pre-Implementation Gate     │ Zero product code written; design doc │
│                                │ approved before planning/building.    │
├────────────────────────────────┼───────────────────────────────────────┤
│ 6. Downstream Handoff Quality  │ Emits typed constraints and test seeds │
│                                │ ready for specification, plan, or tdd.│
└────────────────────────────────┴───────────────────────────────────────┘
```

1. **Problem Grounding:** Did the agent inspect local codebase evidence before asking? Is the reflection accurate to the user's actual motivation?
2. **Adaptive Conversational Pacing:** Did the agent avoid dumping a list of 5 questions? Is there an escape hatch offered if the user wants to dive straight in?
3. **Divergent Trade-Offs:** Are the 2–3 presented approaches genuinely distinct architectures, rather than minor cosmetic variations?
4. **Boundary Hardness:** Are anti-goals explicitly defined? (What would make this a failure even if it technically works?)
5. **Pre-Implementation Gate:** Did the agent strictly refrain from generating scaffold files, installing packages, or writing code before approval?
6. **Downstream Handoff Quality:** Does the final design document provide clear testability seeds and unambiguous constraints for `andino-specification` and `andino-tdd`?
