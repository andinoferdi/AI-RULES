# Grilling, glossary and ADR protocol

Internal resource of `architecture-survey`. Read it once the user picks a candidate (step 6 of
the procedure). Do not write implementation code during grilling.

## Grill in rounds

Map the candidate's decisions as a tree: each decision branches into the ones that hang off
it. The frontier is every open decision whose prerequisites are settled.

1. The first round covers all five decisions listed below. Number each question, give your
   recommended answer under it, and word it so "yes" accepts your recommendation. For a
   decision that depends on another (tests and caller migration depend on the module's
   shape), recommend what follows from the shape you recommend, so one "yes" settles both.
2. Wait for the answers. Settled decisions push the frontier outward; recompute it and ask
   the next round about what the answers reopened or left open.
3. Facts are your job: when a question needs a fact from the code, read the code instead of
   asking the user. Decisions are the user's.

The decisions every deepening candidate has to settle:

- **Constraints:** what the deepened module must keep doing for its current callers, and which
  ADRs or external contracts bind it.
- **What sits behind the seam:** which state, validation, ordering and side effects move inside
  the deep module, and what its interface still exposes (types, invariants, error modes).
- **Adapters:** which dependencies cross the seam and their category. A port is justified only
  when two adapters exist, for example production and an in-memory or mock adapter.
- **Which tests survive:** which tests of the shallow modules are deleted, and which new tests
  assert outcomes through the deepened interface (replace, don't layer).
- **Callers:** how each caller migrates, in one change when all callers ship together or in
  stated steps when they cannot, and whether any old entry point stays.

The grilling ends when every branch has an answer and nothing is silently assumed; play the
settled shape back, including the interface (entry point, inputs, results, error modes), and
wait for the user to confirm it. When the user asks you to choose for
them, take your recommended answers, say so, and play the result back.

## Keep the glossary current

The glossary gives good seams their names, so update it as decisions settle, not in a batch:

- **New concept:** when the deepened module is named after a concept not in `GLOSSARY.md`, add
  the term in the file's existing format. Create the file lazily, when the first term is
  resolved.
- **Fuzzy term:** when the discussion sharpens a term, update its definition in place.
- **Conflict:** when the user or the code uses a term against the glossary's meaning, say so
  and ask which is right.
- Keep `GLOSSARY.md` free of implementation detail; it defines words, not designs.
- Name modules with glossary words: if the glossary defines Order, the module is
  `OrderIntake` or `OrderBook`, not `OrderService`, `OrderHandler` or `OrderManager`.

## Offer an ADR only for an enduring reason

When the user rejects a candidate, separate ephemeral hesitation from an enduring
constraint.

- **Ephemeral (no ADR):** "not now, tight deadline", "no time this quarter", "revisit next
  quarter". These are scheduling choices; they do not belong in `docs/adr/`.
- **Enduring (offer an ADR):** a reason a future survey would need to avoid re-suggesting the
  same consolidation, such as a regulatory isolation requirement or a customer contract that
  swaps the persistence engine. Good ADR material is hard to reverse, surprising without its
  context and the result of a real trade-off; skip reasons that are self-evident.

The offer, in your words: "Want me to record this as an ADR so future architecture surveys
don't re-suggest it?" Write the ADR only after the user agrees.

When an existing ADR already records the same decision, extend that ADR (a dated note under
its consequences that a survey proposed the consolidation and why it was declined) instead of
writing a duplicate, and tell the user which file changed.

## ADR format

Follow the repository's existing ADR format and numbering: scan `docs/adr/` for the highest
number and add one. Create `docs/adr/` lazily when the first ADR is needed. When the
repository has no ADRs yet, use this template:

```markdown
# ADR-{{NNNN}}: Keep {{module_a}} and {{module_b}} separate

## Status
Accepted ({{date}})

## Context
An architecture survey proposed absorbing {{modules}} into a deep {{target_module}} to improve
locality and testability.

## Decision
We keep {{module_a}} and {{module_b}} separate because {{enduring_constraint}}.

## Consequences
- Keeps {{benefit_of_the_constraint}}.
- Callers keep coordinating both modules themselves.
- Future architecture surveys should not propose this consolidation while the constraint holds.
```

## Hand off to interface design

Once the shape is settled, explore alternative interfaces with design-it-twice in the
module-depth resource of the sibling `api-and-interface-design` skill
(`resources/module-depth/guide.md` in its folder). It sketches the interface under
contrasting constraints (minimal entry points, flexibility, the common caller, ports for
cross-seam dependencies), inline by default; parallel design subagents run only when the
user approves them. Then record the chosen candidate, its files, seam and migration in the
active execution plan.
