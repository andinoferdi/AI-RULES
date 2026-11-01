# Diff-Scoped Floor Guard Reference Implementations

The **Floor** is the zero-setup, non-negotiable baseline of Constraint-Driven Development. While numbered dimensions (coverage, bundle size, latency) map to de facto tools like Vitest or Lighthouse, the floor watches for mid-task evasion moves that coding agents make to get to green quickly.

Without a standardized floor guard, every agent invents its own heuristic, creating non-deterministic quality leakage. This reference provides complete, production-ready, zero-dependency implementations in both **Node.js** and **Python 3 stdlib**.

---

## 1. The Floor Contract

### A. Input Scope
- Must inspect the diff between the **merge base** and the **active working tree**.
- Must include **staged changes**, **unstaged changes**, and **untracked files**. A guard reading only `git diff` misses newly created files and staged commits.
- Run from the repository root (or detect top-level with `git rev-parse --show-toplevel`) so subdirectories don't omit untracked files elsewhere.

### B. The Five Evasion Moves Detected
1. **Silenced Checkers**: Added suppressions (`@ts-ignore`, `@ts-nocheck`, `eslint-disable`, `biome-ignore`, `# noqa`, `# type: ignore`, `istanbul ignore`, `nosemgrep`, `gitleaks:allow`, `Stryker disable`).
2. **Tests Made Easier**: Added skips/todos (`.skip(`, `.todo(`, `xit(`, `xdescribe(`, `@pytest.mark.skip`, `t.Skip(`); deleted test files; or assertions removed (`assert `, `expect(`, `.should`) from surviving test files.
3. **Unfinished Work / Stubs**: Added `throw new Error("...not implemented...")`, empty `catch {}` blocks swallowing errors, `TODO` placeholders in new code, or `pass # stub`.
4. **Weakened Constraints**: Lowered numeric minimums (`>= 80` -> `>= 70`), raised numeric maximums (`<= 200` -> `<= 250`), removed constraint rules, or changed numbers with ambiguous direction in `CONSTRAINTS.md`.
5. **Unauthorized Exceptions**: Added rows in the `Exceptions` table (`| W... |` or `| E... |`) without documented authority and expiry.

### C. Deterministic Exit Codes
- **`0` (CLEAN)**: No floor violations found.
- **`1` (VIOLATION)**: One or more floor violations detected. Execution mid-task must block.
- **`2` (ERROR / UNAVAILABLE)**: Git failed, no merge base against target branch, or diff could not be read. **Never allow exit code 2 to be treated as clean.**

### D. Redaction & Direction Rules
- **Redaction is mandatory**: Print only the rule name, file, and line/snippet context. Never dump matched secret tokens or sensitive values.
- **Directionality**: Tightening the bar (e.g., `>= 80%` -> `>= 85%`, or deleting an exception) is silent. Loosening is loud and blocks.

---

## 2. Reference Implementation: Node.js (`floor-guard.mjs`)

Save as `scripts/floor-guard.mjs`. Runs with native Node 18+ without npm dependencies.

```js
#!/usr/bin/env node
/**
 * floor-guard.mjs — Diff-scoped enforcement of CONSTRAINTS.md floor.
 * Usage: node scripts/floor-guard.mjs [--base <branch-or-ref>] (default: origin/main)
 */
import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';

const baseIndex = process.argv.indexOf('--base');
const targetBase = baseIndex > -1 ? process.argv[baseIndex + 1] : (process.env.CONSTRAINTS_BASE || 'origin/main');

const git = (args, { diffExit = false } = {}) => {
  try {
    return execFileSync('git', args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
  } catch (err) {
    if (diffExit && err.status === 1 && typeof err.stdout === 'string') {
      return err.stdout;
    }
    return null;
  }
};

const bail = (msg) => {
  console.error(`floor-guard [ERROR]: ${msg}`);
  process.exit(2);
};

// 1. Ensure git repository root
const topLevel = git(['rev-parse', '--show-toplevel'])?.trim();
if (!topLevel) bail('Not inside a valid git repository.');
process.chdir(topLevel);

// 2. Discover merge base
const mergeBase = git(['merge-base', targetBase, 'HEAD'])?.trim();
if (!mergeBase) bail(`No merge base found against "${targetBase}". Ensure ref is fetched.`);

// 3. Collect diff: tracked changes + untracked files
const trackedDiff = git(['diff', '--unified=0', mergeBase, '--']);
if (trackedDiff === null) bail(`Failed to diff tracked changes against ${mergeBase}`);

const untrackedList = git(['ls-files', '--others', '--exclude-standard']);
if (untrackedList === null) bail('Failed to enumerate untracked files.');

const untrackedDiffs = untrackedList
  .split('\n')
  .filter(Boolean)
  .map((file) => {
    const d = git(['diff', '--no-index', '--unified=0', '/dev/null', file], { diffExit: true });
    if (d === null) bail(`Could not diff untracked file: ${file}`);
    return d;
  })
  .join('\n');

const fullDiff = (trackedDiff + '\n' + untrackedDiffs).trim();

// 4. Parse diff hunks accurately
const added = [];
const removed = [];
const deletedFiles = [];
const normalizePath = (p) => p.replace(/^[ab]\//, '').trim();

let currentFile = '';
let oldFile = '';
let inHeader = false;

for (const line of fullDiff.split('\n')) {
  if (line.startsWith('diff --git') || line.startsWith('diff --no-index')) {
    inHeader = true;
    continue;
  }
  if (line.startsWith('@@')) {
    inHeader = false;
    continue;
  }
  if (inHeader) {
    if (line.startsWith('--- ')) oldFile = normalizePath(line.slice(4));
    else if (line.startsWith('+++ ')) {
      const newPath = normalizePath(line.slice(4));
      currentFile = newPath === '/dev/null' ? oldFile : newPath;
      if (newPath === '/dev/null') deletedFiles.push(currentFile);
    }
  } else {
    if (line.startsWith('+') && !line.startsWith('+++')) {
      added.push({ file: currentFile, text: line.slice(1) });
    } else if (line.startsWith('-') && !line.startsWith('---')) {
      removed.push({ file: currentFile, text: line.slice(1) });
    }
  }
}

// 5. Detection Regexes
const SUPPRESSIONS = /@ts-ignore|@ts-nocheck|eslint-disable|biome-ignore|#\s*noqa|#\s*type:\s*ignore|istanbul\s+ignore|nosemgrep|gitleaks:allow|Stryker\s+disable/;
const STUBS = /throw\s+new\s+(Error|NotImplementedError|UnsupportedOperationException)\s*\([^)]*[Nn]ot\s+implemented|catch\s*\([^)]*\)\s*\{\s*\}|catch\s*\{\s*\}|\bTODO\b|\bpass\s*#\s*stub/;
const SKIPS = /\.(skip|todo)\b|\bxit\(|\bxdescribe\(|@pytest\.mark\.skip|t\.Skip\(|#[ \t]*\[ignore\]/;
const isTestFile = (f) => /\.(test|spec)\.[jt]sx?$|_test\.(py|go|rs)$|[Tt]est\.(java|kt)$/.test(f);
const isConstraintsFile = (f) => /CONSTRAINTS\.md$/.test(f);

const findings = [];
const flag = (rule, file, text) => {
  findings.push({ rule, file, text: text.trim().slice(0, 100) });
};

// Check added lines
for (const { file, text } of added) {
  if (SUPPRESSIONS.test(text)) flag('silenced-checker', file, text);
  if (STUBS.test(text)) flag('unfinished-work', file, text);
  if (SKIPS.test(text)) flag('test-made-easier', file, text);
  if (isConstraintsFile(file) && /^\|\s*(W|E)\d+\s*\|/.test(text)) {
    flag('unauthorized-exception', file, text);
  }
}

// Check deleted files and removed assertions
for (const f of deletedFiles) {
  if (isTestFile(f)) flag('test-deleted', f, 'Test file was deleted');
}

for (const { file, text } of removed) {
  if (isTestFile(file) && !deletedFiles.includes(file)) {
    if (/\b(expect|assert|should)\b/.test(text)) {
      flag('assertion-removed', file, text);
    }
  }
}

// Check CONSTRAINTS.md threshold loosening
const extractThresholds = (text) => {
  const matches = [];
  const re = /\b(\d+(?:\.\d+)?)\b/g;
  let m;
  while ((m = re.exec(text)) !== null) {
    const before = text.slice(Math.max(0, m.index - 20), m.index).toLowerCase();
    const after = text.slice(m.index + m[0].length, m.index + m[0].length + 25).toLowerCase();
    const isMin = />=|at\s+least|minimum|min\b|not\s+fall|not\s+drop/.test(before) || /must\s+not\s+fall|or\s+more/.test(after);
    const isMax = /<=|at\s+most|maximum|max\b|under|below|not\s+grow/.test(before) || /must\s+not\s+grow|or\s+less/.test(after);
    matches.push({ val: parseFloat(m[0]), dir: isMin ? 'min' : isMax ? 'max' : 'unknown' });
  }
  return matches;
};

const ruleKey = (line) => {
  const s = line.trim();
  if (s.startsWith('|')) return s.split('|').map((c) => c.trim()).filter(Boolean)[0] || '';
  if (/^[-*]\s+/.test(s)) return s.slice(2).split(':')[0].trim();
  return null;
};

const removedRules = removed.filter((l) => isConstraintsFile(l.file) && ruleKey(l.text) !== null);
const addedRules = added.filter((l) => isConstraintsFile(l.file) && ruleKey(l.text) !== null);

for (const r of removedRules) {
  const matchingAdded = addedRules.find((a) => ruleKey(a.text) === ruleKey(r.text));
  if (!matchingAdded) {
    if (!/^\|\s*(W|E)\d+\s*\|/.test(r.text)) {
      flag('rule-removed', r.file, r.text);
    }
    continue;
  }
  const oldNums = extractThresholds(r.text);
  const newNums = extractThresholds(matchingAdded.text);
  for (let i = 0; i < oldNums.length; i++) {
    const o = oldNums[i];
    const n = newNums[i];
    if (!n) {
      flag('threshold-removed', r.file, `${r.text} -> ${matchingAdded.text}`);
      break;
    }
    if (o.dir === 'min' && n.val < o.val) {
      flag('threshold-loosened', r.file, `Minimum lowered: ${o.val} -> ${n.val}`);
    } else if (o.dir === 'max' && n.val > o.val) {
      flag('threshold-loosened', r.file, `Maximum raised: ${o.val} -> ${n.val}`);
    } else if (o.dir === 'unknown' && o.val !== n.val) {
      flag('threshold-changed', r.file, `Ambiguous direction threshold changed: ${o.val} -> ${n.val}`);
    }
  }
}

// 6. Report Verdict
if (findings.length === 0) {
  console.log('floor-guard: [CLEAN] Working tree respects quality floor.');
  process.exit(0);
}

console.error(`\nfloor-guard: [VIOLATION] Found ${findings.length} attempt(s) to weaken the floor:`);
for (const f of findings) {
  console.error(`  - [${f.rule}] ${f.file}: "${f.text}"`);
}
console.error('\nFix the issues above or register a tracked exception in CONSTRAINTS.md.\n');
process.exit(1);
```

---

## 3. Reference Implementation: Python 3 (`floor_guard.py`)

Save as `scripts/floor_guard.py`. Runs anywhere with Python 3.8+ using pure standard library (zero pip packages). Ideal for Python, Go, Rust, or systems repositories.

```python
#!/usr/bin/env python3
"""
floor_guard.py — Zero-dependency diff-scoped floor guard in Python standard library.
Usage: python scripts/floor_guard.py [--base origin/main]
Exit codes: 0 = Clean, 1 = Violations found, 2 = Execution error.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

def git_cmd(args, diff_exit=False):
    try:
        res = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
            errors="replace"
        )
        if res.returncode == 0:
            return res.stdout
        if diff_exit and res.returncode == 1:
            return res.stdout
        return None
    except Exception:
        return None

def bail(message):
    sys.stderr.write(f"floor-guard [ERROR]: {message}\n")
    sys.exit(2)

def main():
    target_base = "origin/main"
    if "--base" in sys.argv:
        idx = sys.argv.index("--base")
        if idx + 1 < len(sys.argv):
            target_base = sys.argv[idx + 1]
    elif "CONSTRAINTS_BASE" in os.environ:
        target_base = os.environ["CONSTRAINTS_BASE"]

    # 1. Verify git root
    top_level = git_cmd(["rev-parse", "--show-toplevel"])
    if not top_level:
        bail("Not inside a git repository.")
    os.chdir(top_level.strip())

    # 2. Get merge base
    merge_base = git_cmd(["merge-base", target_base, "HEAD"])
    if not merge_base:
        bail(f"Cannot resolve merge-base against '{target_base}'. Ensure branch is fetched.")
    merge_base = merge_base.strip()

    # 3. Collect tracked and untracked diffs
    tracked_diff = git_cmd(["diff", "--unified=0", merge_base, "--"])
    if tracked_diff is None:
        bail(f"Failed to diff against merge base {merge_base}")

    untracked_files = git_cmd(["ls-files", "--others", "--exclude-standard"])
    if untracked_files is None:
        bail("Failed to enumerate untracked files.")

    untracked_diffs = []
    for f in untracked_files.splitlines():
        f = f.strip()
        if not f:
            continue
        d = git_cmd(["diff", "--no-index", "--unified=0", os.devnull, f], diff_exit=True)
        if d is None:
            bail(f"Could not diff untracked file: {f}")
        untracked_diffs.append(d)

    full_diff = tracked_diff + "\n" + "\n".join(untracked_diffs)

    # 4. Parse diff lines
    added = []
    removed = []
    deleted_files = []

    def clean_path(p):
        p = p.strip()
        if p.startswith("a/") or p.startswith("b/"):
            return p[2:]
        return p

    cur_file = ""
    old_file = ""
    in_header = False

    for line in full_diff.splitlines():
        if line.startswith("diff --git") or line.startswith("diff --no-index"):
            in_header = True
            continue
        if line.startswith("@@"):
            in_header = False
            continue
        if in_header:
            if line.startswith("--- "):
                old_file = clean_path(line[4:])
            elif line.startswith("+++ "):
                new_file = clean_path(line[4:])
                cur_file = old_file if new_file == os.devnull or new_file == "/dev/null" else new_file
                if new_file in (os.devnull, "/dev/null"):
                    deleted_files.append(cur_file)
        else:
            if line.startswith("+") and not line.startswith("+++"):
                added.append({"file": cur_file, "text": line[1:]})
            elif line.startswith("-") and not line.startswith("---"):
                removed.append({"file": cur_file, "text": line[1:]})

    # 5. Regex checks
    re_suppressions = re.compile(
        r"@ts-ignore|@ts-nocheck|eslint-disable|biome-ignore|#\s*noqa|#\s*type:\s*ignore|istanbul\s+ignore|nosemgrep|gitleaks:allow|Stryker\s+disable"
    )
    re_stubs = re.compile(
        r"throw\s+new\s+(Error|NotImplementedError)\s*\([^)]*[Nn]ot\s+implemented|catch\s*\([^)]*\)\s*\{\s*\}|catch\s*\{\s*\}|\bTODO\b|\bpass\s*#\s*stub"
    )
    re_skips = re.compile(
        r"\.(skip|todo)\b|\bxit\(|\bxdescribe\(|@pytest\.mark\.skip|t\.Skip\(|#\[ignore\]"
    )

    def is_test(path):
        return bool(re.search(r"(\.test|\.spec|_test|test_)\.[a-zA-Z0-9]+$", path))

    def is_constraints(path):
        return path.endswith("CONSTRAINTS.md")

    findings = []
    def flag(rule, f, t):
        findings.append({"rule": rule, "file": f, "text": t.strip()[:100]})

    for item in added:
        f, t = item["file"], item["text"]
        if re_suppressions.search(t):
            flag("silenced-checker", f, t)
        if re_stubs.search(t):
            flag("unfinished-work", f, t)
        if re_skips.search(t):
            flag("test-made-easier", f, t)
        if is_constraints(f) and re.match(r"^\|\s*(W|E)\d+\s*\|", t):
            flag("unauthorized-exception", f, t)

    for df in deleted_files:
        if is_test(df):
            flag("test-deleted", df, "Test file was deleted")

    for item in removed:
        f, t = item["file"], item["text"]
        if is_test(f) and f not in deleted_files:
            if re.search(r"\b(assert|expect|should)\b", t):
                flag("assertion-removed", f, t)

    # Threshold weakening in CONSTRAINTS.md
    def extract_thresholds(t):
        nums = []
        for m in re.finditer(r"\b(\d+(?:\.\d+)?)\b", t):
            before = t[max(0, m.start() - 20):m.start()].lower()
            after = t[m.end():min(len(t), m.end() + 25)].lower()
            is_min = bool(re.search(r">=|at\s+least|minimum|min\b|not\s+fall|not\s+drop", before) or re.search(r"must\s+not\s+fall|or\s+more", after))
            is_max = bool(re.search(r"<=|at\s+most|maximum|max\b|under|below|not\s+grow", before) or re.search(r"must\s+not\s+grow|or\s+less", after))
            nums.append({"val": float(m.group(1)), "dir": "min" if is_min else "max" if is_max else "unknown"})
        return nums

    def rule_key(t):
        s = t.strip()
        if s.startswith("|"):
            parts = [c.strip() for c in s.split("|") if c.strip()]
            return parts[0] if parts else ""
        if s.startswith(("- ", "* ")):
            return s[2:].split(":")[0].strip()
        return None

    removed_rules = [r for r in removed if is_constraints(r["file"]) and rule_key(r["text"])]
    added_rules = [a for a in added if is_constraints(a["file"]) and rule_key(a["text"])]

    for r in removed_rules:
        k = rule_key(r["text"])
        match = next((a for a in added_rules if rule_key(a["text"]) == k), None)
        if not match:
            if not re.match(r"^\|\s*(W|E)\d+\s*\|", r["text"]):
                flag("rule-removed", r["file"], r["text"])
            continue
        old_nums = extract_thresholds(r["text"])
        new_nums = extract_thresholds(match["text"])
        for i, o in enumerate(old_nums):
            if i >= len(new_nums):
                flag("threshold-removed", r["file"], f"{r['text']} -> {match['text']}")
                break
            n = new_nums[i]
            if o["dir"] == "min" and n["val"] < o["val"]:
                flag("threshold-loosened", r["file"], f"Minimum lowered: {o['val']} -> {n['val']}")
            elif o["dir"] == "max" and n["val"] > o["val"]:
                flag("threshold-loosened", r["file"], f"Maximum raised: {o['val']} -> {n['val']}")
            elif o["dir"] == "unknown" and o["val"] != n["val"]:
                flag("threshold-changed", r["file"], f"Ambiguous threshold changed: {o['val']} -> {n['val']}")

    if not findings:
        print("floor-guard: [CLEAN] Working tree respects quality floor.")
        sys.exit(0)

    sys.stderr.write(f"\nfloor-guard: [VIOLATION] Found {len(findings)} attempt(s) to weaken the floor:\n")
    for f in findings:
        sys.stderr.write(f"  - [{f['rule']}] {f['file']}: \"{f['text']}\"\n")
    sys.stderr.write("\nFix the issues above or register a tracked exception in CONSTRAINTS.md.\n\n")
    sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 4. Wiring Floor Guard into Developer Loops

### A. NPM Projects (`package.json`)
```json
{
  "scripts": {
    "check:floor": "node scripts/floor-guard.mjs",
    "check:fast": "npm run check:floor && tsc --noEmit && biome check",
    "check:task": "npm run check:fast && vitest run --coverage"
  }
}
```

### B. Python / Make Projects (`Makefile`)
```makefile
.PHONY: check-floor check-task
check-floor:
	python scripts/floor_guard.py

check-task: check-floor
	pytest --cov --cov-report=lcov
```

### C. Git Pre-Commit Hook (`.git/hooks/pre-commit`)
```sh
#!/bin/sh
# Run floor guard before allowing any commit
if command -v node >/dev/null 2>&1 && [ -f scripts/floor-guard.mjs ]; then
  node scripts/floor-guard.mjs || exit 1
elif command -v python3 >/dev/null 2>&1 && [ -f scripts/floor_guard.py ]; then
  python3 scripts/floor_guard.py || exit 1
fi
```
