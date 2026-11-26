# Simplify code without changing what it does

Internal method ID: `andino-code-simplification` (alias: `code-simplification`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

Make working code faster to read, change and debug while every caller sees the same behavior.
Remove accidental complexity and keep the domain rules and the names that carry them. The
measure is the 2 AM on-call test, not line count: how quickly a reader woken by an alert can
locate a decision, trace its effects and explain its failure path. Every retained change
carries evidence that behavior did not move.

## Trigger and non-trigger

Use when a feature works but its code is heavier than it needs to be; when a review flags
nesting, long functions, unclear names, duplication or dead code; when code written under
time pressure, or logic scattered by successive merges, has to become readable; or when
someone asks to simplify or clean up code, including code pasted into a chat.

Do not select, or stop and report, when:

- the request changes behavior (a bug fix, a feature, a contract change): keep it separate.
- the goal is speed. Hot paths are unidiomatic on purpose (unrolled loops, bitwise tricks,
  in-place mutation, pre-allocated buffers); performance work owns them.
- the code is a legal, regulatory, tax or cryptographic calculation written step by step so
  an auditor can compare it with its specification. Keep the steps.
- the code is about to be rewritten or deleted.
- the code is already clear, or you cannot yet say what it does or why a guard, an ordering
  or an abstraction exists. Read more first; skip what stays unclear.
- the candidate is outside the requested target, which defaults to the current diff.

## Select a resource, not a second lifecycle

Load only the resource the current need names. It runs inside this procedure and current
authority; it starts no second plan.

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| Before/after recipes for TypeScript, Python and React, and the behavior traps that make a "simpler" form differ | [patterns and behavior traps](resources/patterns-and-anti-patterns.md) | The change needs no recipe |
| A touched file contains `simplify-ignore` markers | [protected regions](resources/protected-regions.md) | No touched file has markers |
| Seeing one pass end to end, with a runnable old-versus-new harness | [worked example](resources/worked-example.md) | The procedure is already clear |

## Prerequisites

Name the target (files, symbols or pasted code) and what you can check behavior with: tests,
a runnable project, or neither. Read the project's guidance (`AGENTS.md`, `CLAUDE.md`, a
contributing guide) and the code next to the target. A caller you cannot see stays UNKNOWN
and is treated as relying on today's behavior.

## Procedure

1. **Choose the safety net.** Pick the row that matches what you have; it decides what must
   exist before the first edit.

   | What you have | Before the first edit |
   | --- | --- |
   | A repository whose passing tests pin the behavior you will touch | Run them. They must pass before and after, with no test edited. |
   | A repository whose tests fail | Stop and report the failing tests. Simplification needs a green baseline. |
   | A repository whose tests are missing, or miss behavior the change could affect | Add characterization tests in a new test file that pin today's behavior (the list in step 2), run them green against the old code, and keep them. |
   | Code with no runnable project (pasted into a chat, an excerpt) | Simplify it. When a runtime is available, run the old and new versions side by side on named edge cases; otherwise reason through each named case. Never make tests a condition for helping. |

   Done when the row is chosen and its safety net exists and passes on the old code.

2. **Learn what must stay observable (Chesterton's Fence).** Before changing or removing
   anything, find out why it exists. Answer from evidence:
   - What is the code's responsibility? What calls it, and what does it call?
   - Which inputs does it accept, including defaults, `None`/`null`, empty, zero, negative
     and odd truthy values such as `1` or `"yes"`? What does it return, in what shape?
   - Which exceptions does it raise, with which types and messages? Callers may match on them.
   - Which reads and side effects does it have (writes, logs, audit entries, events,
     awaits), in what order and how many times, including on paths that fail partway?
   - Why might it be written this way? Read `git log`, `git blame`, incident notes and
     comments for guards, orderings and workarounds that look removable.
   - Which tests pin which of these, and which does no test pin?
   - Does a touched file contain `simplify-ignore` markers? If so, read
     [protected regions](resources/protected-regions.md) and hash each block now.

   Done when every question has an answer or is recorded as UNKNOWN, and every UNKNOWN on
   code you will change has a characterization test or a named check.

3. **Find concrete opportunities.** Scan the target for these signals. Each fix is the
   smallest change that removes the signal.

   | Signal | Example | Simplification |
   | --- | --- | --- |
   | Deep nesting (3+ levels) | `if`/`else` pyramid | Guard clauses with early exits, in the same order and with the same exits |
   | Long function (50+ lines) | several responsibilities | Named helpers that mirror the domain steps |
   | Nested ternary | `a ? x : b ? y : z` | `if`/`else` chain, `switch` or lookup table |
   | Boolean flag parameter | `create(user, true, false)` | Options object or separate functions, only where the signature is not public |
   | Opaque or repeated condition | the same compound `if` in several places | One predicate named for the domain decision |
   | Generic or abbreviated name | `data`, `tmp`, `res`, `usr`, `cfg` | A name that says what it holds; universal short forms (`id`, `url`) stay |
   | Misleading name | a `get` that also writes | A name that matches the behavior |
   | Comment that restates the code | `// increment counter` | Delete it |
   | Duplicated logic | the same rule written twice | One shared function, only when it is the same rule |
   | Dead code | unused import, unreachable branch, commented-out block | Remove it under [the evidence rule](#remove-what-nothing-uses) |
   | Wrapper or abstraction with one user | pass-through, factory with one product, strategy with one strategy | Call the target directly under [the evidence rule](#remove-what-nothing-uses) |
   | Redundant type assertion | a cast to the type already inferred | Remove it |

   A structural change that needs a design decision, such as replacing prop drilling with
   context, is a judgment call: report it instead of applying it. Done when every candidate
   is either chosen with its reading problem named, or left alone with a reason.

4. **Pin what the tests miss.** For each chosen candidate, list the behaviors from step 2 it
   could touch that no test pins. Add a characterization test for each in a new test file,
   or, for code with no project, name the case you will run or reason through. Done when
   every such behavior has a test that passes on the old code, or a named case.

5. **Change one thing at a time.** For each candidate: make the change, run the focused
   checks, keep it when they pass, undo it and reconsider when they fail. Test each change
   before starting the next, so a failure points at one change. Before keeping a change,
   answer:
   - Same result for every supported input, including the odd ones from step 2?
   - Same exception types and messages?
   - Same side effects, in the same order and count?
   - Do the existing tests pass without modification?

   Record a real bug found on the way and fix it after this pass, in a separate change with
   its own test.

6. **Judge the whole diff.** Run the relevant suite and the project's build, linter and type
   checker; compare protected-region hashes. Read the diff as a caller and as the on-call
   engineer: easier to understand, consistent with the codebase, reviewable, something a
   teammate would approve? Revert any change that made the code harder to read; not every
   attempt succeeds. Done when every retained change passes and every revert has a reason.

7. **Report** with the Simplification Ledger described in Output.

## Rules for every simplification

### Preserve behavior exactly

Change how the code says it, never what it does. Inputs, outputs, return shape, exception
types and messages, side effects and their order, and edge-case results stay identical. If
you cannot show that a change preserves behavior, do not make it. These look equivalent and
are not:

- strict and truthy checks: `x is True` or `x === true` versus `if x`; `!= null` (null and
  undefined) versus `!== null` or a truthy test; `a ?? b` versus `a || b` when `a` can be
  `""` or `0`;
- an `async` wrapper: without `async`, a synchronous throw from the callee escapes as a
  thrown error instead of a rejected promise, and a plain value comes back where callers got
  a promise;
- iteration: `for...of` rejects array-likes that an index loop accepts;
- defaults: `options or {}` versus `{} if options is None else options`; an `encoding=`
  argument the original call did not pass;
- concurrency: sequential `await`s turned into `Promise.all` without proof that the
  operations are independent.

Never delete or relax error handling because a condition "should not happen", and never
change an exception's type or message. Recipes and more traps are in
[patterns and behavior traps](resources/patterns-and-anti-patterns.md).

### Follow project conventions

Simplification makes code more consistent with its codebase, not with outside preferences.
Match the project's import order and module system, function declaration style, naming,
error-handling pattern and depth of type annotations. A change that breaks local consistency
is churn.

### Prefer clarity over cleverness

Explicit code beats compact code whenever the compact form makes a reader pause. A six-line
`if`/`else` beats a nested ternary, a dense regular expression or a chained `reduce`. Types
document structure, not intent: `res` typed as `UserRecord` is still opaque next to
`authenticatedUser`.

### Remove what nothing uses

Remove unused imports, unreachable branches, commented-out code, and an abstraction with one
implementation and one caller, once a search of the whole repository finds no other user:
imports and re-exports, string or reflective references (`getattr`, dynamic `import()`,
registries, configuration files) and the package's public exports. When the name is public
API of a published package, a plugin or hook point, or the search cannot see every caller,
keep it and say so in the report. Leftovers of this kind inside the target are part of the
code you were asked to simplify, not a separate clean-up.

### Keep what carries a reason

- A comment that explains why (a flaky API, a platform bug, an incident, a promise to
  customers) stays; a comment that restates what the code does goes.
- A guard or an ordering whose reason you found in history, an incident note or a comment
  stays. Add a short comment when the reason lived only in history.
- Code inside `simplify-ignore` markers stays byte for byte, indentation included. Hash each
  block before and after, and call it unchanged only when the hashes match. When flattening
  the code around a block would shift its indentation, keep the nesting around it and say so.
  Details: [protected regions](resources/protected-regions.md).

### Maintain balance

Over-simplification is the failure on the other side:

- Inlining a called helper that names a domain rule (`isSessionExpired(session)`) leaks
  low-level detail into every call site.
- Functions that look alike today but serve different business rules change independently:
  duplication is cheaper than the wrong abstraction. Merging unrelated logic is not simpler.
- A defensive check stays even when today's callers never trigger it. Remove error handling
  only when the caller contract makes the case impossible.
- A wrapper can change behavior at its boundary (an `async` wrapper, a `try` that converts
  errors, a copy that protects the caller), and some abstractions serve testability or a
  second implementation that really exists. Check what it contributes before removing it.

### Keep the diff in scope

Simplify the requested target (the current change when none is named) and report candidates
elsewhere instead of fixing them. Past 500 changed lines, use an automated transform
(codemod, AST rewrite, scripted edit) instead of hand edits, in reviewable commits.

## Shortcuts that break simplification

| Shortcut | Reality |
| --- | --- |
| "Fewer lines is always simpler." | Comprehension speed is the measure. A one-line nested ternary is not simpler than a five-line `if`/`else`. |
| "It works; leave it alone." | Code that is hard to read is hard to fix when it breaks. Simplify while the tests are green. |
| "I'll clean up this unrelated file too." | Unscoped changes bloat the diff and risk regressions in code nobody asked you to touch. Report them instead. |
| "I'll refactor while adding this feature." | Two changes in one diff are hard to review, revert and bisect. Split them. |
| "The caller never passes null, so the check can go." | Unexpected input happens. Keep the check unless the contract makes the case impossible. |
| "This abstraction might be useful later." | A speculative abstraction is complexity without value now. Remove it once the evidence rule shows nothing uses it; re-add it when a second use arrives. |
| "The original author must have had a reason." | Maybe: check history, incident notes and callers. When none shows a reason and nothing uses the code, it is residue of iteration. |
| "It names a domain concept, so I keep the unused class." | Domain names protect code that is called. A class nothing calls protects nothing. |
| "Unused imports are a separate clean-up." | They sit in the code you were asked to simplify. Remove them in the same pass. |
| "The protected block is untouched." | Only a hash comparison shows that. Compute it before you claim it. |
| "There are no tests for pasted code, so I can't help." | Simplify it, check it by running or reasoning through named cases, and say what stays unverified. |

## Red flags

Stop and re-check when you see:

- an existing test assertion or fixture changed to make it pass;
- an exception type or message changed, validation relaxed or error handling removed;
- a byte changed inside a `simplify-ignore` block, an identifier the block reads renamed
  outside it, or a claim about a block with no hash;
- a named domain helper inlined, or a comment that explained why deleted;
- side effects or async operations reordered, or an exported signature changed;
- "simplified" code that is longer or harder to follow, or renamed to your taste rather
  than the project's conventions;
- code changed that you could not explain before changing it;
- many simplifications in one untested change, stylistic churn, or edits outside the target.

## Ownership and permission boundary

Andino coordinates selection, shared progress, resource guards and final status from
evidence. This skill owns its procedure, resources and checks, and coordinator brevity never
truncates them. In the workflow it is the refactor step: after a feature turns green under
`tdd` and before `code-review`, so reviewers see the design without accidental complexity.
With an active Andino ticket, record the ledger there with one `NEXT ACTION`. Loading this
skill grants no commit, push, publication or deployment authority.

## Output

A Simplification Ledger with one entry per retained change:

```markdown
### `<file>::<symbol>`
- Reading problem: <what made it hard to follow>
- Change: <what you did>
- Behavior kept: <the inputs, errors and side effects this change could have touched>
- Check: <command and result, or the old-versus-new comparison and its case count>
- Metrics: <only numbers a tool produced, naming the tool; omit otherwise>
```

Then:

- **Left alone:** each candidate you skipped and why (protected, reason found in history,
  public API, unclear, out of scope, judgment call for the owner).
- **Checks:** the commands run with their results, the characterization tests added, and
  each protected block's before and after hash (or "none").
- **Not verified:** what no check covered.

If nothing changed, say why and which evidence was missing. For code pasted into a chat,
reply with the simplified code, one line per change, how you checked it (the cases you ran or
reasoned through), what you left alone and why, and what stays unverified.

## Verification

- [ ] The safety net from step 1 passed on the old code and passes on the new code.
- [ ] Existing tests pass with no assertion or fixture changed; added characterization tests
      stay in the repository.
- [ ] The build, linter and type checker report no new errors or warnings.
- [ ] Exception types and messages, side-effect order and public signatures are unchanged;
      no error handling was removed or weakened.
- [ ] Protected-region hashes were computed before and after, and match.
- [ ] No unused import, unreachable branch or commented-out code is left in or around the
      change.
- [ ] Each change is a reviewable step, the diff holds nothing unrelated, follows the
      project's conventions, and a teammate or review agent would approve it as a net
      improvement that the on-call engineer reads faster.
- [ ] Every retained change has a ledger entry with its check; nothing is claimed without one.

## Worked example

[The worked example](resources/worked-example.md) flattens a nested telemetry aggregator,
keeps a strict `is True` check and a protected digest, and proves both with a runnable
old-versus-new harness.

Anti-pattern: flatten the function, swap `is True` for a truthy check, re-indent the
protected block, then report "behavior identical, block byte-for-byte unchanged" from a test
suite that never passes `valid: 1`.

## Fallback

- Tests cannot run: follow step 1's last row and list the behavior as not verified.
- A caller, history or incident record you cannot read stays UNKNOWN: keep the code it would
  justify removing.
- Malformed or unmatched `simplify-ignore` markers: stop editing that file and ask.
- More than 500 lines to change and no automated transform: stop after the first
  reviewable slice.

## Local resources

The resources above are packaged with this skill; upstream repositories are not runtime
dependencies. The MIT notice is in [references/license.md](references/license.md).

## Operational example (offline)

```python andino-operational-example
import hashlib, json, os
from pathlib import Path
def before(x):
    if x is None: raise TypeError("missing")
    if x < 0: raise ValueError("negative")
    return x * 2
def after(x):
    if x is None: raise TypeError("missing")
    if x < 0: raise ValueError("negative")
    return 2 * x
def observed(fn, x):
    try: return ("value", fn(x))
    except Exception as e: return (type(e).__name__, str(e))
def probe():
    protected = b"# simplify-ignore-start\nFAST = 7\n# simplify-ignore-end\n"
    p = Path("protected.txt"); p.write_bytes(protected)
    if os.getenv("ANDINO_NEGATIVE"): p.write_bytes(protected.replace(b"7", b"8"))
    equal = all(observed(before, x) == observed(after, x) for x in [None, -2, -1, 0, 1, 2, 100])
    return {"behavior_equal": equal, "protected_equal": hashlib.sha256(p.read_bytes()).digest() == hashlib.sha256(protected).digest(), "cases": 7}
print(json.dumps(probe(), sort_keys=True))
```

Default output: `{"behavior_equal": true, "cases": 7, "protected_equal": true}`  
Adversarial output (`ANDINO_NEGATIVE=1`): `{"behavior_equal": true, "cases": 7, "protected_equal": false}`

## Provenance

Adapted from Addy Osmani's `code-simplification` (addyosmani/agent-skills,
`skills/code-simplification/SKILL.md`, last changed in commit f1f6fbf, 2026-10-16) under the
MIT license ([references/license.md](references/license.md)): the five principles,
Chesterton's Fence questions, the signal table, the per-change questions, the rationalization
rows and the verification checklist. The safety-net table, the evidence rule for removal, the
behavior traps, protected regions, the Simplification Ledger and the resources are Andino
additions. Upstream is audit provenance only; runtime needs no upstream installation or
network fetch.
