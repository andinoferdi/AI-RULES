# Quality Gate Protocols & Scanner Exit Code Normalization

Numbered constraints are only as effective as the commands that enforce them. Many industry scanners—such as Semgrep, Axe-core, and Lighthouse—do not exit with binary non-zero codes on severity thresholds, or exit with status `0` even when serious vulnerabilities exist.

This protocol defines:
1. **Exit Code Normalization**: Converting unstructured JSON scanner reports into strict `0` (pass), `1` (blocking finding), or `2` (scanner error) exit codes.
2. **Scanner Execution Safety**: Mandatory secret redaction and error-propagation rules.
3. **The Exception Lifecycle**: How to register temporary, owned, expiring waivers without weakening the global floor.

---

## 1. Scanner Exit Code Contract

A raw scanner command chained with `&&` can create silent false passes:
- If `semgrep` exits `0` after writing findings to a file, downstream checks assume everything passed.
- If `axe` runs against an unreachable localhost server, it may output an empty violations array or an HTML error page that gets parsed as "0 violations".

### The Three Exit Codes
- **`0` (PASS)**: Scan completed successfully; all findings are strictly below blocking thresholds.
- **`1` (BLOCKING VIOLATION)**: Scan completed; one or more findings equal or exceed agreed blocking severity.
- **`2` (SCANNER ERROR / INVALID)**: Scanner failed to execute, crashed, produced malformed JSON, or scanned zero files/URLs. Unknown severity labels also exit `2`, so a renamed level cannot pass silently. **A scanner error must never pass.**

---

## 2. Reference Implementation: Node.js (`quality-gate.mjs`)

Save as `scripts/quality-gate.mjs`. Normalizes Semgrep and Axe-core output.

```js
#!/usr/bin/env node
/**
 * quality-gate.mjs — Exit code normalizer for Semgrep and Axe-core reports.
 * Usage: node scripts/quality-gate.mjs <semgrep|axe> <report.json>
 * Exit codes: 0 = below threshold, 1 = blocking findings, 2 = unusable report or error.
 */
import { readFileSync } from 'node:fs';

const [tool, reportPath, ...extra] = process.argv.slice(2);

if (!['semgrep', 'axe'].includes(tool) || !reportPath || extra.length > 0) {
  console.error('quality-gate [USAGE]: node scripts/quality-gate.mjs <semgrep|axe> <report.json>');
  process.exit(2);
}

try {
  const content = readFileSync(reportPath, 'utf8');
  const report = JSON.parse(content);
  let levels = [];
  let allowed = [];
  let blocking = [];

  if (tool === 'semgrep') {
    // Validate Semgrep payload structure
    if (
      !Array.isArray(report?.results) ||
      !Array.isArray(report?.errors) ||
      report.errors.length > 0 ||
      !Array.isArray(report?.paths?.scanned) ||
      report.paths.scanned.length === 0
    ) {
      throw new Error(`Incomplete scan or semgrep errors present (${report?.errors?.length || 0} errors).`);
    }

    levels = report.results.map((r) => r?.extra?.severity);
    allowed = ['INFO', 'WARNING', 'ERROR', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
    blocking = ['ERROR', 'HIGH', 'CRITICAL'];
  } else if (tool === 'axe') {
    // Validate Axe payload structure (ensure valid URL was hit, not an internal error page)
    if (
      !Array.isArray(report) ||
      report.length === 0 ||
      report.some((page) =>
        !Array.isArray(page?.violations) ||
        typeof page?.url !== 'string' ||
        !['http:', 'https:'].includes(new URL(page.url).protocol)
      )
    ) {
      throw new Error('Axe report is empty or target URL was invalid.');
    }

    levels = report.flatMap((page) => page.violations.map((v) => v?.impact));
    allowed = ['minor', 'moderate', 'serious', 'critical'];
    blocking = ['serious', 'critical'];
  }

  // Detect unknown severity labels
  if (levels.some((lvl) => !allowed.includes(lvl))) {
    throw new Error('Report contains unrecognized severity levels.');
  }

  const blockingCount = levels.filter((lvl) => blocking.includes(lvl)).length;
  console.log(`quality-gate [${tool}]: ${levels.length} total findings, ${blockingCount} blocking findings.`);

  process.exitCode = blockingCount > 0 ? 1 : 0;
} catch (err) {
  console.error(`quality-gate [ERROR]: ${err.message}`);
  process.exitCode = 2;
}
```

---

## 3. Reference Implementation: Python 3 (`quality_gate.py`)

Save as `scripts/quality_gate.py`. Zero external dependencies.

```python
#!/usr/bin/env python3
"""
quality_gate.py — Zero-dependency scanner exit-code normalizer in Python stdlib.
Usage: python scripts/quality_gate.py <semgrep|axe> <report.json>
"""
import json
import sys
from urllib.parse import urlparse

def bail(msg):
    sys.stderr.write(f"quality-gate [ERROR]: {msg}\n")
    sys.exit(2)

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("semgrep", "axe"):
        bail("Usage: python scripts/quality_gate.py <semgrep|axe> <report.json>")

    tool = sys.argv[1]
    report_path = sys.argv[2]

    try:
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)
    except Exception as e:
        bail(f"Cannot read JSON report '{report_path}': {e}")

    levels = []
    allowed = []
    blocking = []

    if tool == "semgrep":
        if not isinstance(report, dict):
            bail("Semgrep report must be a JSON object.")
        results = report.get("results")
        errors = report.get("errors")
        paths = report.get("paths", {}).get("scanned")

        if not isinstance(results, list) or not isinstance(errors, list) or not isinstance(paths, list):
            bail("Incomplete Semgrep report structure.")
        if len(errors) > 0:
            bail(f"Semgrep encountered {len(errors)} internal scanner error(s).")
        if len(paths) == 0:
            bail("Semgrep scanned 0 paths; scan did not execute against source files.")

        levels = [r.get("extra", {}).get("severity") for r in results if isinstance(r, dict)]
        allowed = ["INFO", "WARNING", "ERROR", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
        blocking = ["ERROR", "HIGH", "CRITICAL"]

    elif tool == "axe":
        if not isinstance(report, list) or len(report) == 0:
            bail("Axe report is empty or invalid.")
        for page in report:
            if not isinstance(page, dict) or not isinstance(page.get("violations"), list):
                bail("Invalid Axe page violations structure.")
            url = page.get("url", "")
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https"):
                bail(f"Axe target URL '{url}' is invalid.")
            for v in page["violations"]:
                if isinstance(v, dict):
                    levels.append(v.get("impact"))

        allowed = ["minor", "moderate", "serious", "critical"]
        blocking = ["serious", "critical"]

    for lvl in levels:
        if lvl not in allowed:
            bail(f"Unrecognized severity level: {lvl}")

    blocking_count = sum(1 for lvl in levels if lvl in blocking)
    print(f"quality-gate [{tool}]: {len(levels)} total findings, {blocking_count} blocking findings.")
    sys.exit(1 if blocking_count > 0 else 0)

if __name__ == "__main__":
    main()
```

---

## 4. Mandatory Redaction & Execution Protocols

### A. Secret Scanning (`gitleaks`)
**Rule**: `--redact` is **mandatory**. Without `--redact`, matched secret tokens land in the agent's context window and shell logs.
```sh
# Correct:
gitleaks dir . --redact --no-banner

# Prohibited (leaks secrets into agent transcript):
gitleaks dir .
```

### B. Chaining with Quality Gate
Ensure scanner execution failure terminates the command before the quality gate script runs:
```sh
# In package.json or Makefile:
semgrep scan --config p/default --strict --json > semgrep-results.json && node scripts/quality-gate.mjs semgrep semgrep-results.json
```
If `semgrep` crashes or fails to execute, the `&&` stops execution immediately with a non-zero exit code.

### C. Scope Expensive Scanners to the Diff
Running full mutation suites (`stryker`) or deep security scans (`semgrep`) across thousands of files stalls local agent loops.
- **Diff Scoping**: Filter target paths using `git diff --name-only origin/main...HEAD`.
- Keep the fast stage (`check:fast`) under **5 seconds**, and the task-end stage (`check:task`) under **90 seconds**.

---

## 5. The Exception Lifecycle Protocol

When a legacy defect or third-party limitation cannot be immediately resolved, record an **Exception** in `CONSTRAINTS.md` rather than lowering the threshold for everyone.

### A. The Exception Row Schema
```markdown
## Exceptions

| ID | Rule | Path | Reason and ticket | Owner | Approved by | Expires |
|----|------|------|-------------------|-------|-------------|---------|
| W1 | Q3 (`no-explicit-any`) | `src/legacy/parser.ts` | Parser rewrite, JIRA-881 | @dana | @lead | 2026-12-31 |
| W2 | Q1 (changed-line coverage) | `src/cli/installer.py` | CLI mock refactor, JIRA-902 | @sam | @lead | 2027-01-15 |
```

### B. Operational Rules for Exceptions
1. **Explicit ID**: Prefixed with `W` (Waiver) or `E` (Exception) followed by an integer.
2. **Specific Rule & Path**: name the rule ID and the narrowest path. Wildcards that cover future files (`src/export/**`, `*`) are not narrow.
3. **Reason with a ticket**: the reason names the tracked ticket that removes the exception.
4. **Named Individual Owner**: an individual handle (`@username`), never a generic label like "team" or "agent".
5. **Approved by**: the person who owns the quality policy, recorded by name. The guard cannot verify this; the owner's review of the pull request that adds the row does.
6. **Strict Expiry Date**: at most **90 days** after the row is added. `floor-guard --check-expiry` reports an expired row (`exception-expired`), a new row dated more than 90 days out (`exception-too-long`) and a row with no date (`exception-without-expiry`).
7. **Tightening vs. Loosening**:
   - **Deleting an exception** (when debt is repaid) is silent and encouraged.
   - **Adding or changing an exception** is a policy change: the guard reports every such row as `new-exception`. Make it in its own pull request, separate from the failing feature, with the policy owner's approval.
