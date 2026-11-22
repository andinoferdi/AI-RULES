# Grilling and the Decision Frontier

Internal resource for `andino-brainstorming`. Use it to resolve design decisions
in dependency order.

## Map only decisions that change the design

Record the decision, what depends on it, and whether it is confirmed, delegated
or open. Keep repo facts and inferred preferences separate. Resolve facts with
available evidence. If a missing fact blocks one branch, investigate it and
continue with an independent decision where possible.

The frontier contains open decisions whose prerequisites are settled. Pick the
one with the greatest impact on the user's outcome, the implementation boundary
or the cost of changing direction. Recompute the frontier after each answer.
Drop branches made irrelevant by a decision.

## Make a question worth answering

1. Anchor the question in an observed fact or something the user said.
2. State the consequence the user is deciding about.
3. Offer a reasoned, revisable recommendation. When the user's intent is still
   forming, give a tentative interpretation and let them describe the outcome
   in their own words before presenting implementation choices.
4. Ask one question and wait. Resolve a clear short answer against the question
   asked. Clarify only when the answer could refer to different choices.

For vague goals, ask what would visibly change. For “faster search,” distinguish
shorter query latency from finding the right result in fewer attempts. A numeric
target is useful once it reflects the user's actual problem.

## Synthesize and close

After three questions on the same branch, play back the decisions and show what
they unblock. If the user asks to accelerate, group only independently answerable
decisions and attach a recommendation to each. Keep dependent choices for a
later turn. Explicitly delegated choices may be made and recorded with rationale.

When all material decisions are resolved, play back the outcome, scope,
constraints and selected approach. Mark decisions as confirmed or delegated.
Ask for confirmation of the design. A missing material decision or prerequisite
remains visible at handoff and blocks the affected work.
