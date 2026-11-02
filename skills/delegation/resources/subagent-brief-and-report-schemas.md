# Subagent Brief and Report Schemas

Internal Andino resource. Use pointers for stable source material and include the
specific facts a worker needs. Extracted task text alone is not a ready brief.

## 1. Ready brief recipe

```markdown
# Lane export / Task T1 — CSV listing
Outcome: [observable user result]
Spec & plan: [exact file paths and section anchors]
Global Constraints: [spec sections plus exact task-relevant limits]
Working directory / BASE: [absolute worktree, accepted commit, owned WIP identity]
Owned paths: [source, tests, fixtures, generated files; exact boundaries]
Dependencies: [parent-accepted producers and source/check identities]
Consumed interfaces: [names, signatures, error/side-effect behavior]
Produced interfaces: [exact consumer contract]
Change specification: [what changes into what, decision-bearing values/snippets]
Acceptance: [literal input -> expected output, relevant failure/empty cases]
Proof: [commands, working directory, prerequisites, expected assertions/results]
Prior decisions / uncertainties: [settled choices; material unknowns block dispatch]
Report destination: [absolute path]
Boundaries: no child agents, no writes outside ownership, no weakening tests,
  no dependency installation/commit/push beyond existing scoped authority.
```

Read back the brief before dispatch. Resolve material missing facts inline.
`task_brief.py PLAN ID [OUTFILE]` copies a unique task section, including nested
headings and fenced examples; it does not add spec pointers or global constraints.

## 2. Implementer prompt

Portable template; map fields to the host's real API. An unsupported control is
a disclosed limitation, not an invented argument.

```yaml
role: implementer
model: [explicit actual host model for the lane]
effort: [explicit low / medium / high]
prompt: |
  Read [BRIEF_PATH] first; it binds your outcome, exact values and owned paths.
  This task fits [one sentence of integration context].
  Apply [accepted producer decisions/interface pointers not already in brief].
  Implement only the ready task. For behavior changes observe intended RED then
  GREEN; for static artifacts run the specified artifact checks. Tool/import
  failures and zero tests do not establish RED/GREEN.
  Ask before guessing a material interface or expanding scope: report
  NEEDS_CONTEXT with the exact missing fact and safe partial work.
  Run focused checks, self-review the full owned diff against acceptance, and
  write [REPORT_PATH]. State failed/skipped checks and concrete concerns.
  No child agents. Respect owned paths and publication authority.
  Return the short status below; do not start another task before parent release.
```

## 3. Worker status routing

| Status / observed condition | Parent response |
| --- | --- |
| DONE | Inspect actual diff/report and rerun acceptance; then accept or request a scoped fix. |
| DONE_WITH_CONCERNS | Grade every concern; missing required proof or real defects block acceptance. Optional polish can be deferred with reason. |
| NEEDS_CONTEXT | Inspect the exact missing fact; supply a discoverable contract or obtain the user-owned decision. No automatic model upgrade. |
| BLOCKED | Record command/error, partial output and next discriminating check; advance independent ready work. |
| Failed, stopped, missing report, quota limited | Inspect live status/partial bytes. Report cause and ask before any relaunch/resume/replacement. Inline transfer needs exclusive ownership. |

A normal in-flight clarification within an approved task is not a new wave. Once
a child has stopped, sending a message that triggers work is a resume and needs
applicable go-ahead. Status words never authorize extra tasks or spend.

## 4. Detailed report and short return

Detailed report at the agreed path:
- Acceptance map: each criterion -> file/symbol + real test/artifact observation.
- Changes and produced interfaces, including deviations from the brief.
- Content identity: BASE/HEAD plus owned dirty/new paths and hashes or snapshot.
- Evidence: command, Working directory, environment, exit status, nonzero cases,
  actual expected-vs-observed results, failed/skipped/unavailable checks.
- Self-review findings, remaining concerns and proposed next action.

Short return, under 15 lines:

```text
Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
Task / lane: [identity]
Content identity: [commit range and owned WIP snapshot/report pointer]
Evidence: [focused command and observed result; failed/skipped checks]
Concerns / blocker: [specific issue, affected criterion, needed fact/action]
Report: [absolute path]
```

## 5. One two-track reviewer

```yaml
role: reviewer
model: [explicit actual host model justified by risk]
effort: [explicit low / medium / high]
prompt: |
  Read [BRIEF], [REPORT] and [COMPLETE_OWNED_DIFF/SNAPSHOT].
  Report claims are unverified. First inspect code against each criterion:
  missing, extra or misunderstood behavior, exact values and global constraints.
  For each criterion cite implementation + observed proof or mark UNVERIFIED.
  Then inspect quality: correctness, edge cases, real collaborators, error paths,
  maintainability and tests that can detect the claimed defect.
  Read narrow callers when a concrete exported contract needs checking.
  Run targeted proof if necessary; don't repeat a full suite without a new gap.
  Return Spec: PASS / FAIL / UNVERIFIED; Quality: Approved / Needs Fixes /
  UNVERIFIED; evidence and findings. Each finding names path:line, consequence,
  severity, reproduction/proof and focused correction. Grade real user effect.
  No writes or child agents. Minor cosmetic preferences do not extend repair.
```

## 6. Scoped re-review

```yaml
role: re-reviewer
model: [explicit actual host model within approved review scope]
effort: [explicit low / medium / high]
prompt: |
  Read [OPEN_FINDINGS], [BRIEF], [FIX_REPORT] and [FIX_DIFF/CONTENT_IDENTITY].
  For each finding return ADDRESSED / NOT ADDRESSED / UNVERIFIED with evidence.
  Check the fix for new regressions and changed consumer contracts.
  Do not reopen untouched code for stylistic preferences.
  Required missing proof remains open. Return both spec and quality verdicts.
```
