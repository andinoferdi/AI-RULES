# Brainstorming: questions, decisions and builder readiness

Use the relevant section, not the whole resource as a conversation script.
Scenarios are synthetic. Project observations and stakeholder answers below are
fixture facts, not claims about a live service or an executed model evaluation.

## A question that reveals the real requirement

User: "We need reliable payment webhooks, perhaps a queue. I don't know the design."

Available project facts: PostgreSQL and Redis pub/sub; no durable Redis configuration
or delivery contract established.

Weak reply: "Do you need bursts handled by a queue or can direct writes suffice?"
This embeds the solution in the question. Volume alone doesn't decide delivery
semantics; pub/sub does not establish durable storage.

Better first reply: "What happened the last time a webhook failed, and what should
the customer have experienced instead?" Ask about one concrete episode before options.

User: "During a ten-minute DB restart a dispute disappeared. We thought a 200 meant
it was saved. Bursts reach 5,000 events in two minutes."

Agent: "The important boundary is when we tell the sender it can stop retrying.
The burst count alone doesn't tell us we need a queue. I'll inspect the handler
and documented delivery contract before comparing designs."

Supplied investigation result: handler responds 200 before commit; vendor retries
non-2xx for 24 hours; event_id already has a uniqueness constraint. Burst capacity
is NOT_VERIFIED.

Agent: "There is a possible loss path in acknowledging before saving. The sender
can retry while the DB is down. During maintenance, must events appear immediately
in the product, or is delayed processing acceptable?"

User: "Delay is fine. Never report success before saving. We cannot operate another
service this quarter."

New evidence changes the leading hypothesis: a queue was plausible before the retry
contract was known; direct transactional ingestion now deserves priority. If these
facts were in the original brief, reuse them rather than repeating this interview.

## Compare against actual constraints

Present this comparison before the final design:

| Direction | Fit and cost | What must be true |
| --- | --- | --- |
| Direct transactional PostgreSQL | Reuses service; non-2xx during downtime; sender retries. Candidate recommendation because delay is acceptable. | Retry contract covers outages; duplicates are safe; measured capacity meets agreed targets. |
| Durable buffer and worker | Decouples acceptance from DB availability; adds another component to operate/recover. Rejected for this release's operating constraint. | Persistence, overflow, retention, recovery and acknowledgment established; current pub/sub is not evidence. |

Don't force a third option. Direct storage would also fail if acceptance during DB
downtime were required with no durable external retry source. The same technology
can be credible in one context and wrong in another.

Recommendation: direct storage, conditional on capacity validation. Reverse if retry
coverage fails or immediate independent acceptance becomes a requirement. Don't
promise latency, unlimited scale or zero loss based on architecture names.

If the user owns the choice, ask here. If they said "choose and implement", record
your choice and proceed under that authority; don't collect approval again.

## A compact design with substantive decisions

Example status: PROPOSED. Delivery contract and observations above are fixture
evidence; capacity validation is pending. This isn't implementation-ready until the
gate is resolved or an appropriately bounded next step is agreed.

- Intent: prevent acknowledged events disappearing during DB restart.
- Success: new events receive 2xx only after commit; retry cannot duplicate the
  business effect. Stakeholders accept maintenance delay within sender retries.
- Scope: retain application and PostgreSQL; no new service or changed billing
  semantics. Failure even if functional: success before durable transaction completion.
- Alternatives: direct storage selected for operating fit; durable buffering rejected
  this release, reconsidered if acceptance must survive DB outages.
- Flow: reuse vendor authentication/validation; commit event and required local effect
  atomically where supported, then acknowledge. Inspect seams before naming APIs.
- Recovery: transient DB failure returns non-2xx and relies on the verified retry
  contract. Commit followed by response loss is safe through event_id uniqueness.
  Distinguish a previously committed duplicate from a conflicting payload; don't
  suppress uniqueness errors without checking the committed record.
- Acceptance: DB down causes no success; concurrent delivery produces one effect;
  retry after response loss succeeds for the stored event; invalid authentication
  follows documented vendor behavior.
- Ownership: maintenance delay/no new services are user constraints. Internal names
  and reuse of transaction helpers are builder calls.
- Evidence gap: agree and measure capacity/acknowledgment targets at the existing
  public seam. A burst count is an input, not a passing load test.
- Next: validate capacity, then use existing planning/implementation contracts.

## Project design contents

Record these in the existing design; omit irrelevant sections and reuse sufficient
contracts. This is a content aid, not a mandatory second document.

1. Intent/evidence: concrete problem, stakeholder, why, current state; distinguish
   code/source facts, reported claims and proposals.
2. Success/boundaries: observable outcomes, goals, non-goals, anti-goals and binding
   resource, privacy, operational or domain constraints.
3. Alternatives/decision: credible paths, screening reasons, selected/delegated
   direction, accepted costs and evidence that would reverse the recommendation.
4. Responsibilities/flow: components or people, inputs/outputs/dependencies;
   applicable interfaces/data, permissions and error semantics for software.
5. Failure/recovery: realistic exceptions, interrupted/duplicate work, ownership,
   recovery and relevant migration/compatibility; clearly named unknowns.
6. Acceptance: normal/failure examples, observable signals, test seams or validation
   actions and their limits. Proposed checks aren't test results.
7. Ownership/handoff: user choices, agent defaults with reasons, unresolved assumptions
   with owners and treatment, and only the next method actually needed.

Readiness means no guessing at consequential intent, not specifying every internal
detail. An agreed investigation can be the next deliverable while a claim is unverified.

## Builder-check prompt

Independent review is conditional on benefit, authority and capacity. No nested
delegation. Otherwise check inline and state the actual mode. Review adds no authority.

```text
Read the supplied design and relevant permitted evidence. You must carry it out
without the author's unstated intent. Find consequential ambiguities, contradictions,
infeasible options and unsupported claims. For each, cite the passage/evidence,
explain the wrong outcome a builder could produce, and give the smallest resolution.
Separate:
- ANSWERED: answer exists; cite and incorporate it.
- BUILDER_CALL: reversible detail within delegation; propose a default.
- USER_DECISION: outcome/trade-off outside delegation; name the actual choice.
- EVIDENCE_GAP: needs source inspection/experiment; specify the check.
Report blockers and owners first. Invent no objections to meet a quota.
If none remain, report no material blocker found and the evidence limits.
Do not edit, spawn, approve for the user or claim a check ran.
```

Fix findings using evidence, not a vote. Ask the actual owner only when necessary.
Recheck affected findings; another review without new evidence is not progress.

## Stress cases and stopping rules

- Vague nonsoftware goal: "Help our elderly neighbors." Ask about a recent difficulty
  before assuming an app. A ride rota and a phone check-in solve different problems;
  don't invent preferences or success numbers.
- Rich brief: reuse supplied outcomes/constraints. Probe missing consequences only;
  don't restart with "what is your goal?"
- Delegated choice: choose a viable default and mark it yours. No forced vote,
  mandatory subagent or repeated approval.
- Polished incomplete design: "Always return 200 after enqueue; Redis exists."
  Fails readiness without persistence, overflow and recovery evidence. Good prose
  cannot average away this gap.
- One viable path: explain why others fail constraints; don't offer rejected paths
  as viable to meet a quota.
- No tools: distinguish supplied facts/assumptions; return a conditional brief or
  experiment without fabricated inspection/review.
- Visual uncertainty: a sketch, diagram or agreed throwaway prototype answers one
  question. Record finding/limits before production; preserve UI choice/permissions.
- Stop exploration: if another answer cannot materially change the next safe,
  reversible action, state a default and proceed. Otherwise resolve the decision
  or evidence gap. Theoretical completeness is not a blocker.

These are application examples, not executed behavioral benchmarks. The parent
workflow owns actual evaluation and completion evidence.
