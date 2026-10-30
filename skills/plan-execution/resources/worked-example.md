# Worked execution example: adversarial execution trace

This worked example demonstrates an end-to-end execution trace under
`andino-plan-execution`. It shows inline continuous execution, two-phase TDD signal
gating, handling a plan defect with an explicit recorded ruling, in-place plan
checkpoint mutation, and a whole-branch final review without helper scripts.

---

## Scenario background

- **Repository**: Python CLI tool `inventory` with existing modules `inventory/cli.py`,
  `inventory/store.py`, and `tests/test_cli.py`.
- **Accepted Plan**: `docs/exec-plans/active/csv-export.md` containing two tasks:
  - `T1`: Add `--format csv` support with CSV quoting.
  - `T2`: Add `--name <filter>` exact matching.
- **Authority**: Execution authorized in current local worktree; no remote push or
  package publication permitted.

---

## Turn 1 — Pre-flight audit & claiming Task 1

### AI Narration (1 line)
Auditing repository status and claiming Task T1 in the execution plan.

### Action
1. Inspect git status to ensure working tree is clean and baseline commit is known:
   ```bash
   git status --short
   git rev-parse --short HEAD
   ```
   *Output*: Clean worktree, HEAD commit `a1b2c3d`.

2. Mutate `docs/exec-plans/active/csv-export.md` in-place using `edit` tool:
   - Change T1 Status from `TODO` to `IN_PROGRESS`.
   - Update Execution Board: Phase 1 status to `IN_PROGRESS`.
   - Set `NEXT ACTION: Implement T1 under TDD (write test_csv_quotes_name, run RED)`.

---

## Turn 2 — Task 1: Phase 1 (RED)

### AI Narration (1 line)
Writing failing test `test_csv_quotes_name` in `tests/test_cli.py` to establish RED signal.

### Action
1. Add test case to `tests/test_cli.py`:
   ```python
   def test_csv_quotes_name(self):
       code, out = run_cli(["list", "--format", "csv"])
       self.assertEqual(code, 0)
       rows = list(csv.reader(out.splitlines()))
       self.assertEqual(rows, [["id", "name"], ["1", "Tea, green"]])
   ```
2. Run test command:
   ```bash
   python -m unittest tests.test_cli -k test_csv_quotes_name
   ```
3. *Observed Output*:
   ```text
   FAIL: test_csv_quotes_name (tests.test_cli.TestCLI.test_csv_quotes_name)
   AssertionError: 2 != 0 : unrecognized argument --format
   FAILED (failures=1)
   ```
   *Signal Analysis*: True behavioral RED — the argument parser rejects `--format` as expected. Not a syntax error.

---

## Turn 3 — Task 1: Phase 2 (GREEN) & In-Place Update

### AI Narration (1 line)
Implementing `--format csv` in `inventory/cli.py` and running verification suite.

### Action
1. Edit `inventory/cli.py` to add argument `--format` choices `['json', 'csv']` and format rendering using `csv.writer`.
2. Rerun focused test:
   ```bash
   python -m unittest tests.test_cli -k test_csv_quotes_name
   ```
   *Observed Output*:
   ```text
   .
   ----------------------------------------------------------------------
   Ran 1 test in 0.012s
   OK
   ```
3. Run full module test suite for regression protection:
   ```bash
   python -m unittest discover -s tests -p "test_*.py"
   ```
   *Observed Output*:
   ```text
   ......
   ----------------------------------------------------------------------
   Ran 6 tests in 0.045s
   OK
   ```

4. Mutate `docs/exec-plans/active/csv-export.md` in-place:
   - Mark T1 actions complete: `[x]`.
   - Update T1 status to `DONE`.
   - Record in T1 `Result / Evidence`:
     ```markdown
     Result / Evidence:
     - Commits: a1b2c3d..b2c3d4e
     - Verification command: `python -m unittest discover -s tests -p "test_*.py"`
     - Signal: 6 tests passing, exit 0.
     ```
   - Update Execution Board T1 to `DONE`.
   - Set `NEXT ACTION: Claim T2 (name filtering)`.

---

## Turn 4 — Task 2: Detecting Plan Defect & Applying Ruling

### AI Narration (1 line)
Claiming Task T2 and resolving specification ambiguity regarding case sensitivity.

### Action
1. Inspect T2 requirements:
   - Plan specifies: "Filter inventory by exact name match".
   - *Conflict/Ambiguity*: Plan step states `filter_name.lower()`, but acceptance criterion R3 specifies "exact matches, case-sensitive".
2. **Apply Ruling Protocol**:
   - The spec is binding: case-sensitive exact matching matches existing CLI conventions.
   - Record ruling directly in T2 before implementing:
     ```markdown
     Ruling: Implement exact case-sensitive match for --name — The specification requires exact matches; case-folding would prevent distinguishing capitalized item codes — Cost if wrong is low (single comparison line).
     ```
3. Update T2 status to `IN_PROGRESS` in-place.
4. Add tests `test_name_filter_match` and `test_name_filter_no_match` in `tests/test_cli.py`.
5. Run test command (RED observed):
   ```bash
   python -m unittest tests.test_cli -k "test_name_filter_*"
   ```
   *Observed Output*: `FAILED (failures=2)` — argument `--name` not recognized.
6. Implement `--name` filter in `inventory/cli.py`.
7. Rerun tests (GREEN observed):
   ```bash
   python -m unittest tests.test_cli -k "test_name_filter_*"
   ```
   *Observed Output*: `OK (2 tests)`.
8. Run full regression suite: 8 tests passing, exit 0.
9. Mutate plan in-place: mark T2 `DONE`, record evidence, update Execution Board.
10. Set `NEXT ACTION: Whole-branch final review`.

---

## Turn 5 — Whole-Branch Final Review & Completion

### AI Narration (1 line)
Executing whole-branch final review across `a1b2c3d..HEAD` against acceptance criteria.

### Action
1. Generate diff against base:
   ```bash
   git diff a1b2c3d..HEAD --stat
   ```
2. Evaluate against Acceptance Criteria R1, R2, R3:
   - R1 (CSV format): Verified, covered by `test_csv_quotes_name`.
   - R2 (Empty CSV header): Verified, covered by `test_csv_empty`.
   - R3 (Name filter): Verified, covered by `test_name_filter_match`.
3. Grade Review Findings:
   - *Finding 1 (Minor)*: Docstring in `cli.py` could mention `--format csv` in help examples.
     - *Disposition*: Re-graded as Minor. Deferred to final summary; do not trigger fix pass.
   - *No Critical or Important findings*.
4. Final in-place update of `docs/exec-plans/active/csv-export.md`:
   - Change overall Plan Status from `IN_PROGRESS` to `DONE`.
   - Update Execution Board: All phases `DONE`.
   - Set `NEXT ACTION: None — task complete`.
   - Append Final Review summary:
     ```markdown
     ## Final Review Summary
     - Reviewer: Inline self-review against specification and diff `a1b2c3d..HEAD`.
     - Suite status: 8 tests passing, 0 failures, exit 0.
     - Rulings made:
       1. T2: Case-sensitive matching adhered to specification over loose plan step.
     - Deferred minors:
       1. CLI module docstring example for `--format csv`.
     ```

### Result
All tasks completed with verified evidence, single durable checkpoint maintained in-place, zero stalls, and zero lost context.
