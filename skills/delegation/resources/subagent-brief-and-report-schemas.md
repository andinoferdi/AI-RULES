# Subagent Brief and Report Schemas

Internal Andino resource for `andino-delegation`. Operates under Andino Workflow governance.

## 1. The Zero Context Bleed Law

**Iron Invariant**: Never paste chat history, multi-turn deliberations, or entire implementation plans into a subagent prompt.
- **Why**: Pasting conversational history inflates token consumption, injects contradictory assumptions, distracts model attention, and degrades instruction adherence.
- **Mechanism**: Use **Context Pointers**. Pass exact file paths, commit SHAs, interface contracts, and task-specific brief files extracted directly to disk.

---

## 2. Structured Task Brief Schema

Every dispatched worker receives a task brief containing strictly the following 8 fields:

```markdown
# Task Brief: [TASK-ID] — [Task Title]

1. **Task Outcome**: One clear sentence stating the observable deliverable.
2. **Spec & Plan Anchor**: Pointer to specific heading in `[PLAN_FILE]` or `[SPEC_FILE]`.
3. **Owned File Paths** (Disjoint Write Set):
   - [exact/path/to/file1.py]
   - [exact/path/to/test_file1.py]
4. **Consumed Interfaces** (Dependencies):
   - [Interface name, signature, exported symbol, or mock data from upstream tasks]
5. **Produced Interfaces** (Deliverables):
   - [Interface name, public API signature, or schema exported for downstream tasks]
6. **Acceptance Test Command & Expected Signal**:
   - Command: `pytest tests/test_file1.py -v`
   - Expected Signal: `100% passing`, exit code `0`.
7. **Report Destination Path**:
   - `[WORKSPACE]/task-[N]-report.md`
8. **Strict Operational Boundaries**:
   - DO NOT spawn subagents (neither helpers nor reviewers).
   - DO NOT mutate files outside the Owned File Paths list.
   - DO NOT weaken existing assertions or delete failing test cases.
   - DO NOT install global dependencies or modify package manifests without authorization.
```

---

## 3. Implementer Prompt Template

```markdown
Subagent (general-purpose):
  description: "Implement Task [N]: [task_name]"
  model: [MODEL_TIER — per Model Selection Rubric]
  prompt: |
    You are an isolated implementer for Task [N]: [task_name].

    ## Task Brief
    Read your task brief first: [BRIEF_FILE_PATH]
    It contains your binding requirements, owned paths, and verification commands.

    ## Context & Interfaces
    [Scene-setting: upstream dependencies, interfaces, and architectural constraints]

    ## Operational Directives
    1. Implement strictly what the brief specifies.
    2. Follow TDD: write a focused test first, verify failure, implement code, verify pass.
    3. Run focused tests during iteration; run the task test suite before reporting.
    4. Self-review your own git diff against the brief before writing the report.
    5. Write your complete detailed report to: [REPORT_FILE_PATH].
    6. Return ONLY the short status contract (<15 lines) in your final message.

    ## Strict Prohibitions
    - Never spawn subagents. You are the sole executor. Review is scheduled separately.
    - Never touch files outside your owned paths list.
    - Never weaken assertions or silence errors to simulate green tests.
    - If stuck, uncertain, or blocked by ambiguous specs, halt and report BLOCKED or NEEDS_CONTEXT.
```

---

## 4. Two-Track Task Reviewer Prompt Template

```markdown
Subagent (general-purpose):
  description: "Review Task [N] (Spec Compliance + Code Quality)"
  model: [MODEL_TIER — per Model Selection Rubric]
  prompt: |
    You are an independent, adversarial reviewer for Task [N]: [task_name].
    You inspect the task's net diff once and return two distinct verdicts.

    ## Inputs
    - Task Brief: [BRIEF_FILE_PATH]
    - Implementer Report: [REPORT_FILE_PATH]
    - Scoped Diff Package: [DIFF_FILE_PATH] (contains commits, stat, and unified diff)

    ## Review Method
    1. Read the diff package once. Do not crawl unrelated codebase areas unless checking a concrete exported contract.
    2. Treat the implementer's report as unverified claims. Verify every claim against the actual diff.
    3. Do not re-run full test suites. Run a focused test command only if reading the code exposes an unverified risk.

    ## Track 1: Spec Compliance Verdict
    - Compare diff against Task Brief:
      - Missing: features required but absent.
      - Extra: unrequested scope, speculative abstractions, or over-engineering (YAGNI).
      - Misunderstood: wrong problem solved or broken semantics.
    - Verdict: PASS (Spec Compliant) | FAIL (Issues Found) | UNVERIFIED (Cannot Verify From Diff)

    ## Track 2: Code Quality Verdict
    - Clean separation of concerns, proper error propagation, naming discipline.
    - Edge cases covered by real behavioral tests (no vacuous or mock-only tests).
    - Verdict: Approved | Needs Fixes

    ## Finding Calibration
    - Critical (Must Fix): Spec deviation, data corruption, silent error suppression, broken contract.
    - Important (Should Fix): High fragility, unhandled edge case, brittle test assertion.
    - Minor (Deferred): Stylistic preference, cosmetic naming, documentation polish.
      (Minor findings are logged for deferred cleanup and NEVER block task completion).

    ## Output Format
    Start immediately with the verdicts:
    - Spec Compliance: [PASS / FAIL / UNVERIFIED] [Summary]
    - Task Quality: [Approved / Needs Fixes] [Summary]
    - Issues:
      - Critical: [file:line, defect, consequence, suggested fix]
      - Important: [file:line, defect, consequence, suggested fix]
      - Minor (Deferred): [file:line, suggestion]
```

---

## 5. Scoped Re-Reviewer Prompt Template

```markdown
Subagent (general-purpose):
  description: "Re-review Task [N] Fix Round [R]"
  model: [MODEL_TIER]
  prompt: |
    You are re-reviewing Task [N] after fix round [R].
    Your scope is STRICTLY limited to verifying whether previous findings were addressed
    and checking the fix diff for new regressions.

    ## Inputs
    - Task Brief: [BRIEF_FILE_PATH]
    - Open Findings List: [OPEN_FINDINGS]
    - Implementer Fix Report: [REPORT_FILE_PATH] (appended at end)
    - Scoped Fix Diff: [FIX_DIFF_FILE_PATH]

    ## Directives
    1. For each finding in Open Findings, evaluate: ADDRESSED or NOT ADDRESSED with file:line proof.
    2. Inspect the fix diff for newly introduced breakage.
    3. Do NOT re-review untouched code or invent new out-of-scope nitpicks.

    ## Output Format
    - Finding 1: [ADDRESSED | NOT ADDRESSED] — [evidence]
    - New Breakage in Fix Diff: [None | Critical/Important issues]
    - Verdict: [All Findings Addressed | Findings Remain Open]
```

---

## 6. Standardized Short Status Contract (<15 Lines)

Implementer and reviewer subagents report back to the parent controller using this compact format to eliminate conversation context bloat:

```text
Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
Commits:
  - a1b2c3d feat(auth): implement token signer with HS256 validation
Tests: 14/14 passing, exit code 0, 0 warnings
Concerns: None
Report File: .andino/delegation/auth-plan/task-1-report.md
```

If status is `BLOCKED` or `NEEDS_CONTEXT`, the subagent provides a 2-3 line concrete blocker statement directly in the message so the controller can make an immediate routing decision.
