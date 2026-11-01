# Pre-Integration Verification Protocol

Internal Andino resource. Operates under Andino Workflow governance.

## 1. The Green-Suite Hard Stop

Before any integration options are presented or discussed, the full project test suite must be executed against the exact tree about to be delivered.

```bash
# Example test commands by ecosystem
# Node / TypeScript: npm test / pnpm test / yarn test
# Python: pytest / python -m unittest
# Rust: cargo test
# Go: go test ./...
# Make: make test
```

### Stop Condition: Non-Zero Exit Code

If any test fails:
1. Report the failure count and exact failure logs immediately.
2. Halt execution. Do not present the integration menu.
3. The integration menu is accessible ONLY after a clean, passing test run.

```
Tests failing (<N> failures). Must fix before completing:

[Detailed test failure output]
```

## 2. Working Tree Cleanliness Gate

Inspect the state of the active working tree:

```bash
git status --porcelain
```

### Rules on Uncommitted Modifications

- **Functional Code Changes:** All functional code intended for delivery must be committed to the feature branch with clear atomic commit messages before entering delivery.
- **Dirty Tree Stop:** If there are modified tracked files or staged changes, pause and resolve:
  - Commit them if they belong to the feature.
  - Stash them if they are experimental or unrelated scratch work.
- **Delivery is for Committed Candidates:** Merging or creating a PR from an uncommitted candidate is an invalid operation that leads to lost work or inconsistent remote state.

## 3. Candidate Scope and Diff Inspection

Before confirming the base branch and offering integration options, verify the exact diff scope:

```bash
# List commits present on feature branch but not on base branch
git log --oneline <base-branch>..HEAD

# Inspect summary of changed files
git diff --stat <base-branch>...HEAD
```

Verify that the commits and modified files match the scope agreed in the active execution plan (`docs/exec-plans/active/*.md`). If unintended files (such as secret keys, temporary logs, or unrelated modules) are included, rectify them prior to presenting the integration menu.
