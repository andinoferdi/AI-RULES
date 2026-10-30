# Plan execution contract

## Single durable checkpoint

The execution plan file (under `docs/exec-plans/active/<task>.md` or the project's
designated path) is the authoritative, single durable checkpoint. There is no
competing ledger, secondary `.superpowers` directory, or disconnected tracker.
All progress, rulings, deviations, and verified evidence are recorded in-place
within this document so that any fresh session or compacted context can resume
without loss of state.

## State transitions and mutation rules

Tasks follow a strict progression:

```
[TODO] ──> [IN_PROGRESS] ──> [DONE]
   │              │
   └──> [BLOCKED] └──> [SKIPPED] (only via explicit recorded ruling)
```

1. **Claiming a task**: Update status from `TODO` to `IN_PROGRESS` in both the
   Execution Board and the Detailed Execution section before modifying code.
2. **Completing a task**: Transition to `DONE` only when the completion contract
   below is satisfied with concrete evidence.
3. **Blocking a task**: If an unresolved prerequisite or external barrier prevents
   progress, mark `BLOCKED` and state the exact blocking dependency.
4. **Skipping a task**: Allowed only when an explicit recorded ruling confirms
   the task is rendered obsolete or superseded by accepted evidence.

## Two-Phase Signal Gate

Every task must satisfy its verification gate before being marked `DONE`:

### 1. Behavioral code (Canonical TDD)
- **Phase 1 (RED)**: Write or locate the focused test asserting the required behavior.
  Execute the test command. Observe and record the failing signal (discriminating
  assertion failure, not syntax error or missing imports).
- **Phase 2 (GREEN)**: Make the minimal implementation change satisfying the test.
  Rerun the exact test command. Observe and record the passing signal (exit 0,
  passing assertions).
- **Regression Check**: Run the owning package or module test suite to confirm no
  collateral damage.

### 2. Static artifacts (Configuration, Documentation, Schemas)
- Run the appropriate deterministic validator (linter, schema validator, build check,
  or exact file content/diff check).
- Compare actual output against the expected signal defined in the plan.
- Record the command, exit code, and key matching output lines.

## Ruling protocol

When encountering ambiguities, plan contradictions, or minor defects:
- Do not stall or prompt the user for permission when the decision is within
  session authority and bounded by the accepted specification.
- Decide the smallest change that satisfies the specification.
- Record the ruling directly in the owning task within the plan:

```markdown
Ruling: <what was decided> — <why this choice satisfies the spec> — <cost and blast radius if wrong>
```

- If an assumption affects downstream tasks, propagate the ruling and update
  affected consumer interfaces or mark them for rebaselining.

## Evidence recording standards

A completed task entry must contain concrete evidence in its `Result / Evidence` block:
- **Commands run**: Exact CLI command strings executed from the repository root
  or specified working directory.
- **Observed signal**: Exit status and verbatim terminal snippet showing test count,
  passed assertions, or validator output.
- **Tested artifact identity**: Relevant file paths and commit hash range (`base..head`)
  or content hash where applicable.
- **Rulings**: Any rulings made during execution of the slice.

An empty evidence block, an unchecked box, a vague summary ("tests passed"), or
diff inspection alone does NOT satisfy the completion contract.

## Drift invalidation and recovery

Before executing a task or upon resuming an interrupted session:
1. **Audit drift**: Run `git status` and compare current files against the plan's
   recorded baseline.
2. **Evaluate validity**: If an upstream producer or interface was modified outside
   the recorded plan, mark affected downstream tasks as requiring re-validation.
3. **Preserve unaffected evidence**: Do not rerun or wipe out completed tasks whose
   inputs, outputs, and dependencies remain unchanged and verified.
4. **Crash recovery**: If interrupted mid-turn, inspect `git diff`. If changes are
   unverified, revert or re-run the Two-Phase Signal Gate before advancing.

## Blast radius and permission boundary

- **Continuous execution scope**: Applies exclusively to authorized, local, reversible
  actions (file edits, running test suites, local linting/formatting).
- **Hard stops**: Immediate halt and escalate to the human partner if:
  1. An irreversible or destructive operation is required (e.g., deleting branches,
     dropping tables, discarding uncommitted user changes).
  2. A security perimeter is reached (accessing secrets, modifying auth policies).
  3. An external boundary is crossed (pushing to remote, publishing packages,
     sending network calls outside local mock servers).
  4. The plan is fundamentally broken and cannot be resolved by a bounded ruling.
