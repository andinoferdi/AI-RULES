# Request a review

Resource for `andino-code-review`. Use it to hand a change to an independent reviewer, or
to set up a self-review checkpoint with the same brief.

## 1. When to request

- Before merging to the main branch, after a major feature, and after each task when
  several agents build one plan.
- When stuck and a fresh view would help, before a risky refactor (as a baseline), and
  after fixing a complex bug.

Dispatch an independent reviewer only when isolation adds value and the delegation
contract and the user authorize it. A different model from the author's, when one is
available, brings different blind spots. Otherwise hand over the brief, or apply the
skill's procedure to your own change and label the result a self-review.

## 2. Build the brief

Give the reviewer crafted context, never your session history. The brief stands alone.

- **Change and intent**: what changed and which behavior should hold.
- **Requirements, standards and decisions**: exact pointers (issue, spec section,
  contributing rule, decision record) and any known gaps.
- **Pinned scope**:
  - committed work: base and head SHAs, with the diff and log commands;
  - work in progress: the base SHA, the patch, and the full content of every new untracked
    file in scope. A list of paths is not enough, because the reviewer must see the bytes;
  - excluded material: name unrelated and sensitive files (secrets, credentials, local
    environment files, customer data) as outside the scope, and leave their contents out.
- **Decisions to rule on**: feedback you declined and why, deviations from the plan, and
  questions still waiting for the owner.
- **Verification**: commands you ran with their observed results, separate from what the
  reviewer should check or run.
- **Return format**: the Output shape of the skill (see the template).

```bash
git rev-parse HEAD                           # base for WIP; head for committed work
git diff HEAD                                # staged and unstaged changes as one patch
git ls-files --others --exclude-standard     # untracked: paste in-scope files, name the rest
```

## 3. Reviewer template

```text
You are reviewing a change you did not write. You cannot see the author's session; everything
you need is below or in the repository.

Repository: <path or URL>
Base: <SHA>    Head: <SHA, or "working tree; patch below">
Change and intent: <what changed and which behavior should hold>
Requirements: <pointers>    Standards: <pointers>    Decisions: <pointers>
Scope: <diff command, or the patch plus the full content of new files>
Excluded: <files outside the scope; contents not provided>
Decisions to rule on: <declined feedback, deviations, open questions>
Checks the author ran: <command -> observed result>
Please look hard at: <specific risks>

Rules:
- Confirm the bytes you review match the scope above. Report any drift before drawing
  conclusions from them.
- Stay read-only and leave the repository exactly as you found it. Read other revisions
  with `git show`, or in a disposable copy outside the repository. Run no checkout, switch,
  stash, reset or commit there.
- Do the review yourself, in passes if it is large. Start no subagents.
- Report in this order:
  Scope; Verdict (overall CHANGES REQUESTED | UNVERIFIED | NO BLOCKERS FOUND, with Spec and
  Standards each PASS | FAIL | UNVERIFIED); Findings, most severe first, each as
  `[CRITICAL|REQUIRED|SUGGESTION|NIT] Axis · file:line · title` with trigger, consequence,
  evidence and remedy; Tests; Checked and sound; Pre-existing, outside this change;
  Verification and limits (what you ran and observed, what you only read);
  Declined to Judge, one line per behavior you set aside and why, so the author can rule
  on it.
```

## 4. After the review

Treat the returned review as feedback and apply [receiving-review](receiving-review.md).
Rule on every Declined to Judge line; nothing the reviewer set aside is dropped silently.
