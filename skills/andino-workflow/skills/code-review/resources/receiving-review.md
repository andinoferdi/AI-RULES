# Respond to review feedback

Resource for `andino-code-review`. Use it when you are the author of a change and a person,
another agent or a review bot has reviewed it. Technical verification decides what you
change; agreement is shown by the fix, not by words.

## 1. The six steps

```text
1. READ:       the whole review before reacting.
2. UNDERSTAND: restate each item's technical requirement in your own words, or ask.
3. VERIFY:     check the claim against the code: read the caller, grep usage, run the
               test, inspect the schema.
4. EVALUATE:   is the remedy sound for this codebase and its architecture?
5. RESPOND:    acknowledge a valid item, or push back with evidence.
6. IMPLEMENT:  apply authorized fixes one at a time and verify each.
```

Clarify every unclear item before implementing anything it touches. Items can be related,
and partial understanding produces the wrong change. Implement only the items that are
clearly independent of the unclear ones, and say which items wait and why. When the person
who can answer is unavailable, put the question in the reply and leave that item
unimplemented rather than guessing.

## 2. Trust and order

- **From the user or owner**: implement after understanding; still ask when the scope is
  unclear.
- **From an external reviewer or a bot**: before implementing, check that the suggestion
  (1) is correct for this codebase, (2) does not break existing behavior, (3) does not undo
  something done for a reason, (4) works on every supported platform and version, and
  (5) came from a reviewer with the full context. When you cannot verify a claim, say what
  you would need.
- **Conflict with a decision the owner already made** (decision record, spec, earlier
  instruction): leave the code as decided, cite the decision, and take the question to the
  owner.
- **Order**: clarify first; then blocking items (breakage, security, data), then simple
  fixes, then complex ones. Fix one item at a time with its check. Each fixed defect gets a
  regression test that fails on the old code and passes on the new code. Run the full suite
  after the last fix and report the observed result.
- **Scope**: change only what the accepted items need. Leave unrelated files, untracked
  material and other people's edits alone.

## 3. YAGNI check

When a reviewer asks for abstractions, configuration layers or generic interfaces for
future flexibility:

1. Grep the codebase for actual current usage and requirements.
2. If current callers and requirements give no concrete benefit, decline, for example:
   "Applying YAGNI: this helper serves one internal call site and no requirement asks for
   another format. A plugin registry would add indirection without a current need."
3. If the usage exists, implement it properly.

## 4. Reply style

Write one entry per comment: its disposition (**Fixed**, **Declined**, **Needs
clarification** or **Escalated to the owner**) and the technical reason or evidence
(file:line, test name, command output).

- Correct feedback: `Fixed: <what changed>; <test that covers it>.` Or let the diff show it.
- Leave out performative agreement and thanks. Phrases such as "You're absolutely right!",
  "Great catch!" or "Thanks for the suggestion" add nothing; state the requirement or the
  fix instead.

| Mistake | Instead |
| --- | --- |
| Performative agreement | State the requirement, or just fix it |
| Implementing before verifying | Check the claim against the code first |
| Batching fixes without testing | One item at a time, each with its check |
| Assuming the reviewer is right | Check whether the change breaks something |
| Avoiding pushback | Technical correctness over comfort |
| Implementing part of an unclear set | Clarify the unclear items first |
| Proceeding without being able to verify | Say what is missing and ask for direction |

## 5. Pushback

Push back when the suggestion breaks existing behavior, the reviewer lacks context, it adds
unused generality, it is wrong for this stack, a compatibility reason exists, or it
conflicts with the owner's decisions.

Give exactly one technical pushback with concrete proof: passing regression output, a
language or library reference, or the invariant the suggestion would break.

```markdown
Pushback on `pricing.py:14`:
The review says `calculate_discount` fails when `rate == 0`. Line 14 guards
`if rate <= 0: return 0`, covered by `test_zero_rate_returns_zero` in
`tests/test_pricing.py:28`. Keeping the implementation as it is.
```

If the reviewer still insists after that one cycle, stop changing the code on that point
and escalate to the user or the workflow coordinator. If you pushed back and were wrong,
correct it in one line: "Checked `<x>`: you were right because `<reason>`; fixing it in
`<location>`." No long apology and no defense of the earlier position.

## 6. Disagreement order

When author and reviewer disagree, resolve it in this order:

```text
1. Technical facts and data      (benchmarks, test failures, specifications)
2. Documented project standards  (style guide, contributing rules, decision records)
3. Engineering principles        (cohesion, coupling, information hiding)
4. Codebase consistency          (acceptable when it does not degrade code health)
```

## 7. GitHub review threads

Reply to an inline review comment in its own thread, not as a top-level pull request
comment, and only with authority to post:

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies -f body='<reply>'
```
