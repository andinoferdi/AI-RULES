---
name: andino-code-review
description: Use when reviewing a pull request, branch, commit range, work in progress (including untracked files), pasted diff or agent handoff; when asking someone else to review a change; or when responding to review feedback. Operates under Andino Workflow governance.
---

# Review a change against its spec and the repository's standards

Internal method ID: `andino-code-review` (alias: `code-review`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

Decide whether a change is ready by reading the bytes that will ship and answering two
separate questions: does it do what was asked (**Spec**), and does it meet the repository's
documented standards and sound engineering (**Standards**)? A change can pass one and fail
the other, so each gets its own verdict and neither masks the other. The same method
prepares a change for someone else's review and decides what to do with feedback on your
own change.

## Trigger and non-trigger

Use it for an identifiable change: a commit, range, branch, pull request, work in progress
with its untracked files, a pasted diff or a handoff from another agent; for a review
request; and for review feedback you must act on. Conceptual design advice, a standalone
cosmetic sweep and a request only to format code belong elsewhere.

Reviewing is read-only: the reviewed checkout ends exactly as it started. Editing starts
only in [Respond to review feedback](#respond-to-review-feedback), with authority to change
the code.

## Select a resource, not a second lifecycle

| Current need | Resource | Exclusion |
| --- | --- | --- |
| Write the brief for an independent reviewer | [requesting-review](resources/requesting-review.md) | Reviewing the change yourself |
| Act on review comments as the author | [receiving-review](resources/receiving-review.md) | Writing a review |
| Name a structural remedy; judge change size, dead code or dependencies | [review-craft](resources/review-craft.md) | Formatting that tooling enforces |
| Security or performance triggers in the diff | [checklists](resources/checklists.md) | A full audit: use `andino-security-and-hardening` or `andino-performance-optimization` |
| A complete review with its proof | [worked-example](resources/worked-example.md) | None |

## Prerequisites

A change you can pin to exact bytes; read access to the repository or the pasted material;
the requirement source when one exists. Running tests needs a disposable directory outside
the repository.

## Procedure

### 1. Pin the change and the starting state

Record the starting state before anything else; step 7 compares against it.

```bash
git rev-parse HEAD && git branch --show-current && git status --short
```

| Request | Review boundary |
| --- | --- |
| Commit or explicit endpoints | Resolve both to SHAs and inspect `git diff <base> <head>`. For one commit, use its requested parent comparison or its patch. |
| Branch or pull request | Resolve target and head to SHAs. Review `git diff <target>...<head>` (merge base to head) and list `git log --oneline <target>..<head>`. Use the PR target when known; otherwise ask for the fixed point. |
| Work in progress | Capture the requested layers with `git diff --cached`, `git diff` and `git ls-files --others --exclude-standard`, and read each in-scope untracked file. Include committed branch changes when the scope includes them. |
| Pasted diff or excerpts | Review the supplied bytes and report the missing context that affects the verdict. |

- Use the three-dot form for branches: a two-dot diff shows the target's later commits as
  reversed changes that the branch never made.
- Inspect the final effective content as well as layer-specific changes when the request
  calls for them. Keep local edits outside a committed-only verdict. Separate out-of-scope
  material from in-scope bytes you could not inspect.
- Read other revisions with `git show <rev>:<path>`, `git diff` and `git log`. In the
  reviewed checkout run no `checkout`, `switch`, `stash`, `reset`, `commit` or `merge`, and
  edit no file.
- Resolve an ambiguous boundary from the request and the repository; ask when competing
  boundaries would change the review.

Done when both ends resolve to SHAs (or the WIP layers are captured), the diff is non-empty
or the empty diff or unresolved ref is reported before any verdict, and the starting state
is recorded.

### 2. Find the requirement and standards sources

Spec sources, in this order; the first match is the requirement and later ones add context:

1. the request itself, or a path the user named;
2. issue references in commit messages or the branch name, read from the repository's
   tracker or issue files;
3. spec or plan files under `docs/`, `specs/` or similar that match the feature.

With none found, ask. If there is none, mark Spec UNVERIFIED and judge the behavior against
existing contracts and the reasonable expectations in step 4.

Standards sources: `CONTRIBUTING*`, `CODING_STANDARDS*`, `AGENTS.md` and `CLAUDE.md`,
decision records and ADRs, and lint or format configuration. Note what tooling already
enforces; the review leaves those points to the tooling. Read the change description too:
its first line stands alone and its body says why.

Done when every source is listed by path for the Scope line, or its absence is recorded.

### 3. Read the tests and gather evidence from the reviewed bytes

- Read the affected tests before the implementation. For each, write down what it observes
  and which wrong implementation would still pass it.
- Check the author's verification story: what ran, what passed, what was only claimed.
- Run tests and probes on the reviewed bytes. When the checkout is not exactly the reviewed
  snapshot (another branch checked out, uncommitted or untracked edits outside the scope),
  export the head to a disposable directory and work there:

  ```bash
  tmp=$(mktemp -d) && git archive <head> | tar -x -C "$tmp"
  # run the suite and probes inside "$tmp"; rm -rf "$tmp" when done
  ```

  For a work-in-progress review the working tree is the snapshot; use it read-only.
- **Mutation probe.** In the disposable copy, flip one condition the change adds (`>=` to
  `>`, drop a negation, `and` to `or`), run the suite, then restore. A mutant that stays
  green is a missing test: name the input that would catch it.

Done when every test result you will cite came from the reviewed bytes and each test's blind
spot is written down.

### 4. Spec pass

- Trace each requirement to implementation and tests. Check preserved caller behavior,
  boundaries, failure paths and state transitions.
- Classify each Spec finding as **missing or partial**, **implemented wrong**, or **not
  asked for** (scope creep), and quote the requirement ID or line.
- Flag deviations from the plan for the author to confirm, and problems in the plan itself.
- The spec is a vision document. Where it is silent, a reasonable user's expectation is a
  requirement, judged by its effect on that user. Ask of every state-changing path:
  - the same request arrives twice (retry, double submit, replayed event);
  - two requests arrive at once;
  - the operation fails halfway, and what state is left;
  - empty, zero, boundary, oversized or wrong-type input;
  - a caller who is not the owner, or not signed in.

Done when every requirement is marked met, partial, missing or wrong, and every
state-changing path has an answer to each of the five questions.

### 5. Standards pass

- Documented rules first. Cite the file and rule for each breach.
- Then, in proportion to the change:
  - correctness;
  - readability: could it be fewer lines, does each abstraction earn its complexity, is
    there a clever trick to simplify;
  - architecture: does a refactor reduce complexity or only relocate it, does feature logic
    leak into a shared module, does a near-duplicate replace an existing canonical helper,
    is a type boundary explicit or hidden behind a silent fallback, does the change grow an
    already-large file instead of decomposing it;
  - security and performance, using the [checklists](resources/checklists.md);
  - production readiness when relevant: migration, backward compatibility, docs.
- Follow affected callers or data across boundaries to confirm reachability.
- Smells are judgement calls. A documented repo standard that endorses a pattern overrides
  the smell, and a smell alone never blocks. Offer the named remedy from
  [review-craft](resources/review-craft.md) when you flag one.

Run the Spec pass, then the Standards pass, inline. Independent passes in separate contexts
happen only under the delegation contract and the user's authorization.

Done when every documented rule has been checked against the diff and each Standards finding
names its rule or principle.

### 6. Filter before reporting

- Check whether a caller, guard, contract or test already rules the candidate out.
- Tie each finding to changed behavior, or to a pre-existing issue the change makes
  reachable or materially worse. A defect in code the change neither touches nor exposes
  goes under "Pre-existing, outside this change".
- Separate a confirmed defect from missing evidence. Report a suspicion as unverified, with
  the check that would settle it.
- Name a focused reproduction or regression assertion when it would resolve uncertainty or
  prevent recurrence.
- Zero findings is a valid result.

Done when each remaining finding carries its trigger, consequence and evidence.

### 7. Report and leave the repository as found

Write the report in the [Output](#output) shape. Rerun the state command from step 1 and
compare it with the starting state; restore anything you changed and report any difference.

Done when the report is written and the end state equals the start state.

## Request a review

Use before merging, after a major feature, after each task in multi-agent work, or when
stuck. Read [requesting-review](resources/requesting-review.md) and build the brief from it:
pinned SHAs or the exact patch with the contents of new files; requirement and standards
pointers; sensitive or unrelated files named as excluded, never their contents; the
decisions the reviewer should rule on; checks already run, separate from checks to run.
Dispatch an independent reviewer only under the delegation contract. Otherwise hand over
the brief, or run this procedure on your own change and label it a self-review.

## Respond to review feedback

Read [receiving-review](resources/receiving-review.md) before replying or editing. In short:
read everything, restate each item, verify each claim against the code, judge it for this
codebase, reply, then implement. Clarify unclear items before implementing anything they
touch. A decision the owner already made outranks a reviewer's preference: take the
question to the owner and leave the code as decided. Push back once with evidence, then
escalate. Each fixed defect gets a regression test that fails on the old code, and the full
suite runs at the end.

## Rules for every review

### Approval standard

Approve a change that clearly improves the code's health, even when it is not how you would
have written it. Block on defects: unmet requirements, regressions, security or data-loss
risks, broken documented rules. Keep suggestions and nits optional. Blockers are fixed
before merge, not promised for a follow-up; record agreed follow-ups in the review and
create tracker items only with authority.

### Honesty

- Evidence before a verdict: a "looks good" without reading and checking helps no one.
- State a real issue at its real severity; a production bug is not "a minor concern".
- Quantify when you can ("one extra query per item"), rather than "could be slow".
- Push back on approaches with clear problems and propose the alternative. When the author
  has full context and overrides a non-blocking point, accept it.
- Comment on the code, not the person.

### Presumptive blockers

Surface each of these and propose the simpler design. It becomes `[REQUIRED]` when the
change makes the structure worse: a refactor that relocates complexity instead of reducing
it; a file pushed past about 1000 lines without decomposition; feature logic added to a
shared module; a near-duplicate of an existing canonical helper; a silent fallback that
hides an unclear invariant.

## Shortcuts that weaken reviews

| Shortcut | Reality |
| --- | --- |
| "The tests pass, so it works" | Tests show what they observe. Read what each observes and probe with a mutant. |
| "I ran the suite in my checkout" | A checkout holding other edits tests other bytes. Run on the reviewed head. |
| "The spec says nothing about retries" | Silence is not permission. Judge the effect on a reasonable user. |
| "It's a small diff" | Small diffs still grow large files and bolt branches onto unrelated flows. Judge the resulting structure. |
| "AI-generated code is probably fine" | It is confident and plausible when wrong, so it needs the same evidence. |
| "We'll clean it up later" | Blockers are fixed before merge; optional items stay optional. |
| "The refactor makes it cleaner" | Count the concepts a reader must hold. Moving them is not removing them. |
| "It's just a version bump" | A bump is behavior you did not write. Read the changelog and the lockfile diff. |
| "Switching branches to compare is harmless" | It changes the reviewed checkout. Read other revisions with `git show`. |

## Red flags

- A verdict with no requirement source and no UNVERIFIED Spec.
- Test results that came from a checkout holding other edits.
- The repository left on another branch, with a new stash, or with edited files after a review.
- A two-dot branch diff reported as the change.
- Findings without severity, or a blocker buried under nits.
- A smell reported as a blocker against a documented repo standard that endorses the pattern.
- A pre-existing defect in untouched code reported as this change's blocker.
- A bug fix with no regression test.
- A bulk dependency bump with no changelog review or lockfile diff.
- "LGTM" with no evidence of what was read or run.

## Ownership and permission boundary

Andino coordinates selection, progress tracking and durable checkpoints; this skill owns its
procedure and verification criteria. A review reads and runs. Editing code, committing,
posting review comments and dispatching a reviewer need the user's authorization, and a
dispatched reviewer also needs the delegation contract. A reviewer starts no subagents of
its own; it reviews a large change in passes and says so.

## Output

Report in this order:

- **Scope**: the reviewed snapshot (base...head SHAs, or the WIP layers), the requirement and
  standards sources, and excluded material.
- **Verdict**: overall CHANGES REQUESTED, UNVERIFIED or NO BLOCKERS FOUND; Spec and Standards
  each PASS, FAIL or UNVERIFIED; one line with the finding count and the worst issue per axis.
- **Findings**, most severe first and one per root cause: `[SEVERITY] Axis · file:line ·
  title`, then the trigger or input, the consequence, the evidence (observed run or
  reasoning), the smallest practical remedy and the test that would catch it.
  Cross-reference the other axis when it is affected. Say so when there are none.
- **Tests**: what the existing tests observe, mutants that stayed green, missing tests.
- **Checked and sound**: behaviors you verified as correct, one line each, only what you
  checked.
- **Pre-existing, outside this change**: defects in code the change neither touches nor
  exposes, one line each, or "none".
- **Verification and limits**: what ran (command and observed result), what was only read,
  what others reported; the starting and ending repository state; evidence a verdict still
  needs.
- **Declined to Judge**: material you set aside and why, or "none".

| Prefix | Impact |
| --- | --- |
| `[CRITICAL]` | Blocker with severe harm, such as an exploitable security break or unrecoverable data loss. |
| `[REQUIRED]` | Blocker: a concrete regression, unmet requirement or enforceable project rule. |
| `[SUGGESTION]` | Optional improvement with a specific benefit and a proportionate remedy. |
| `[NIT]` | Optional cosmetic correction. At most three per review. |

A confirmed blocker fails its axis. A material evidence gap without a confirmed blocker
leaves the axis UNVERIFIED. Overall: CHANGES REQUESTED for any blocker, UNVERIFIED for a
remaining material gap, NO BLOCKERS FOUND for completed coverage without blockers. Lead with
what matters: one structural problem outranks ten nits.

## Verification

Before sending the review:

- [ ] Scope names exact SHAs or WIP layers and every requirement and standards source.
- [ ] Every requirement has a mark; every state-changing path has answers to the five
      questions.
- [ ] Every documented rule was checked; a smell a repo rule endorses is not a finding.
- [ ] Every finding has a severity, anchor, trigger, consequence, evidence and remedy.
- [ ] Every test result came from the reviewed bytes; mutants and missing tests are listed.
- [ ] Pre-existing defects are separate from this change's findings.
- [ ] Ran, read and reported-by-others are separate, and nothing is claimed that was not done.
- [ ] Both axis verdicts and the overall verdict follow the rules in Output.
- [ ] The repository's end state equals its start state.

## Worked example and anti-pattern

[worked-example](resources/worked-example.md) reviews a refund change whose order update and
audit insert commit separately: one `[REQUIRED]` Spec finding with its trigger, a runnable
SQLite proof of the partial write and of the fix, both axis verdicts, the missing failure
test, and how the author receives the finding.

Anti-pattern: "Looks good, 9 tests pass", written after running the suite in a checkout that
held someone's uncommitted draft, with no requirement cited, no mutant tried, and the branch
switched to `main` to compare files and left there.

## Fallback

- Pasted diff only: review the bytes; list the context you lacked and the verdicts it leaves
  UNVERIFIED.
- No runnable tests, or no permission to run them: say so under Tests; the affected axis is
  UNVERIFIED unless reading settles the question.
- No spec: Spec is UNVERIFIED; existing contracts and the five questions still apply.
- No git: inspect files read-only and compare the end state by file listing and content
  hashes.

## Local resources

- [requesting-review](resources/requesting-review.md): when to ask, the brief, the reviewer
  template.
- [receiving-review](resources/receiving-review.md): the reception steps, trust and order,
  reply style, pushback, disagreement order, GitHub replies.
- [review-craft](resources/review-craft.md): change size and splitting, smells and remedies,
  dead code, dependencies.
- [checklists](resources/checklists.md): security and performance triggers; path containment
  and negative caching in full.
- [worked-example](resources/worked-example.md): a full review with a runnable proof.
- For depth: `andino-security-and-hardening` and `andino-performance-optimization`.

## Provenance

Adapted from these sources under the MIT license; notices are in
[references/license.md](references/license.md):

- `addyosmani/agent-skills:skills/code-review-and-quality` at commit e997ac5 (Addy Osmani)
- `mattpocock/skills:skills/engineering/code-review` at commit 6f7f783 (Matt Pocock)
- `obra/superpowers:skills/requesting-code-review` and `skills/receiving-code-review` at
  commit 22f0b46 (Jesse Vincent)
