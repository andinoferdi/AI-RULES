# Floor guard: reference implementations

Numbered dimensions in `CONSTRAINTS.md` each have an established tool. The floor has none: it is a
diff-scoped check for the shortcuts an agent takes to turn a red check green. Left to improvise,
each agent writes a different checker, and the same project gets different enforcement from run to
run. Use this reference, change only the patterns for your stack, and keep the contract as it is.

## Contract

- **Input:** the diff between the merge base and the working tree: committed, staged, unstaged and
  untracked changes. Run from the repository root (`git rev-parse --show-toplevel`), because
  `git ls-files` lists only the current subtree. A guard that reads only `git diff` misses new files.
- **Moves it reports:**

  | Rule | Move |
  | --- | --- |
  | `silenced-checker` | A new suppression or coverage-ignore comment |
  | `test-made-easier` | A new skip, focus or expected-failure marker |
  | `test-deleted` | A test file deleted |
  | `assertion-removed` | An assertion removed from a test file that stays (a line moved within the file is not a removal) |
  | `unfinished-work` | A stub that throws or raises "not implemented", an empty `catch` or bare `except: pass`, a new `TODO` |
  | `check-made-optional` | `continue-on-error: true` or `\|\| true` added to a CI workflow |
  | `threshold-loosened` / `threshold-changed` / `threshold-removed` | A minimum lowered, a maximum raised, a number without readable direction changed, or a number dropped from a rule in `CONSTRAINTS.md` |
  | `rule-removed` | A rule row or bullet removed from `CONSTRAINTS.md` |
  | `new-exception` | A row added to (or changed in) the Exceptions table |
  | `exception-expired` / `exception-too-long` / `exception-without-expiry` | With `--check-expiry`: an exception past its date, a new one longer than 90 days, or one with no date |

- **Exit codes:** `0` clean, `1` at least one violation (block the change), `2` the guard could not
  run (not a git work tree, no merge base, unreadable diff). Never let a `2` read as a `0`.
- **Output:** the rule and the location (`path:line`, or `path:line (removed)` for a line in the
  base). Never the line's text: a suppressed or TODO line is often the one holding a secret-like
  value, and the report lands in terminals and agent logs.
- **Direction:** tightening is silent, loosening is loud. A number's direction comes from the
  words right next to it (`>=`, `≥`, `at least`, `must not fall`, `--min-...` for a minimum; `<=`,
  `≤`, `at most`, `must not grow`, `--max-...` for a maximum). A number with no readable direction,
  such as a tolerance column, is reported whenever it changes. Dates are not thresholds.
- **Approval:** the guard cannot tell an approved exception from an invented one. A policy change
  that adds an exception shows `new-exception`, and the owner's review in that pull request is what
  approves it.

Both implementations below pass the same 13-scenario battery and produce the same findings. They
use only the language runtime and git.

## Node (`scripts/floor-guard.mjs`)

Node 18 or later, no dependencies.

```js
#!/usr/bin/env node
// floor-guard.mjs: diff-scoped check that a change does not lower the bar set in CONSTRAINTS.md.
// Usage: node scripts/floor-guard.mjs [--base <ref>] [--check-expiry] [--today YYYY-MM-DD]
// Exit 0: clean. Exit 1: at least one violation. Exit 2: the guard could not run; never read 2 as 0.
// A finding names the rule and the location, never the line's text: a flagged line can hold a secret.
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';

const argv = process.argv.slice(2);
const option = (name) => {
  const i = argv.indexOf(name);
  return i > -1 ? argv[i + 1] : undefined;
};
const bail = (message) => {
  console.error('floor-guard: ' + message);
  process.exit(2);
};
const base = option('--base') ?? process.env.CONSTRAINTS_BASE ?? 'origin/main';
const checkExpiry = argv.includes('--check-expiry');
const now = new Date();
const localToday = [now.getFullYear(), now.getMonth() + 1, now.getDate()]
  .map((n, i) => String(n).padStart(i ? 2 : 4, '0')).join('-');
const today = option('--today') ?? localToday;
if (!/^\d{4}-\d{2}-\d{2}$/.test(today)) bail('--today must be YYYY-MM-DD');

// For an untracked file `git diff --no-index` exits 1 because the sides differ: keep that output.
// Every other failure returns null, which the caller turns into exit 2.
const git = (args, { diffExit = false } = {}) => {
  try {
    return execFileSync('git', args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], maxBuffer: 1 << 28 });
  } catch (e) {
    return diffExit && e.status === 1 && typeof e.stdout === 'string' ? e.stdout : null;
  }
};

// Run from the top of the work tree: `git ls-files` lists only the current subtree.
const top = git(['rev-parse', '--show-toplevel'])?.trim();
if (!top) bail('not inside a git work tree');
process.chdir(top);
const mergeBase = git(['merge-base', base, 'HEAD'])?.trim();
if (!mergeBase) bail('no merge base against ' + base + ' (fetch it, or pass --base)');

// Committed, staged and unstaged changes against the merge base, plus untracked files.
const tracked = git(['diff', '--unified=0', mergeBase, '--']);
if (tracked === null) bail('could not diff against ' + mergeBase);
const untrackedList = git(['ls-files', '--others', '--exclude-standard']);
if (untrackedList === null) bail('could not list untracked files');
const untracked = untrackedList.split('\n').filter(Boolean).map((f) => {
  const d = git(['diff', '--no-index', '--unified=0', '/dev/null', f], { diffExit: true });
  if (d === null) bail('could not diff untracked file ' + f);
  return d;
});
const diff = [tracked, ...untracked].join('\n');

// Header lines run from `diff ` to the first `@@`; after that a line starting with `---` or `+++`
// is content. Each hunk header resets the old and new line counters used in findings.
const added = [], removed = [], deleted = [];
const pathOf = (s) => s.replace(/^[ab]\//, '').replace(/\t$/, '');
let file = '', oldFile = '', inHeader = false, oldLine = 0, newLine = 0;
for (const line of diff.split('\n')) {
  if (line.startsWith('diff ')) inHeader = true;
  else if (line.startsWith('@@')) {
    inHeader = false;
    const m = /^@@ -(\d+)(?:,\d+)? \+(\d+)/.exec(line);
    if (m) { oldLine = Number(m[1]); newLine = Number(m[2]); }
  } else if (inHeader) {
    if (line.startsWith('--- ')) oldFile = pathOf(line.slice(4));
    else if (line.startsWith('+++ ')) {
      const newFile = pathOf(line.slice(4));
      file = newFile === '/dev/null' ? oldFile : newFile;
      if (newFile === '/dev/null') deleted.push(oldFile);
    }
  } else if (line.startsWith('+')) added.push({ file, line: newLine++, text: line.slice(1) });
  else if (line.startsWith('-')) removed.push({ file, oldPath: oldFile, line: oldLine++, text: line.slice(1) });
  else if (line.startsWith(' ')) { oldLine++; newLine++; }
}

const findings = [];
const flag = (rule, where) => findings.push({ rule, where });
const at = (l) => `${l.file}:${l.line}`;
const atBase = (l) => `${l.oldPath}:${l.line} (removed)`;

// One character of each plain-word pattern sits in a class so this file never matches itself
// when it is first added. Keep that when you extend the lists for your stack.
const SUPPRESSIONS = /@ts-[i]gnore|@ts-[n]ocheck|@ts-[e]xpect-error|eslint-[d]isable|biome-[i]gnore|#\s*noqa|#\s*type:\s*ignore|#\s*pyright:\s*ignore|#\s*pragma:\s*no\s*cover|istanbul\s+ignore|c8\s+ignore|[n]osemgrep|gitleaks:[a]llow|Stryker\s+disable|\/\/\s*nolint|#\[allow\(/;
const STUBS = /throw\s+new\s+\w*Error\s*\([^)]*[Nn]ot\s+implemented|raise\s+NotImplementedError|\bpass\s*#\s*stub|\btodo!\(|\bunimplemented!\(|panic\(\s*"not implemented|catch\s*(\(\s*\w*\s*\))?\s*\{\s*\}|except(\s+\w+)?\s*:\s*pass\b|\b[T]ODO\b/;
const SKIPS = /\.(skip|only|todo)\s*\(|\bx(it|describe|test)\s*\(|@pytest\.mark\.(skip|xfail)|\bpytest\.skip\(|@unittest\.skip|\bt\.Skip\(|#\[ignore\]/;
const OPTIONAL = /continue-on-error:\s*true|\|\|\s*true\b/;
const ASSERTION = /\b(expect|assert|should)\b|\bassert\w*\(/;
const isTest = (f) => /(^|\/)test_[^/]+\.py$|_test\.(py|go|rs)$|\.(test|spec)\.[cm]?[jt]sx?$|Tests?\.(java|kt)$/.test(f);
const isWorkflow = (f) => /(^|\/)\.github\/workflows\/[^/]+\.ya?ml$|(^|\/)\.gitlab-ci\.yml$/.test(f);
const isConstraints = (f) => /(^|\/)CONSTRAINTS\.md$/.test(f);
const isException = (t) => /^\s*\|\s*[WE]\d+\s*\|/.test(t);

// 1. Silenced checkers, unfinished work, easier tests, optional CI checks, new exceptions.
for (const l of added) {
  if (SUPPRESSIONS.test(l.text)) flag('silenced-checker', at(l));
  if (STUBS.test(l.text)) flag('unfinished-work', at(l));
  if (SKIPS.test(l.text)) flag('test-made-easier', at(l));
  if (isWorkflow(l.file) && OPTIONAL.test(l.text)) flag('check-made-optional', at(l));
  if (isConstraints(l.file) && isException(l.text)) flag('new-exception', at(l));
}

// 2. A test file deleted, or an assertion removed from a test file that stays. A removed line that
// comes back unchanged in the same file was moved, not removed.
for (const f of deleted) if (isTest(f)) flag('test-deleted', `${f} (file deleted)`);
const readded = new Map();
for (const l of added) {
  const key = l.file + '\n' + l.text.trim();
  readded.set(key, (readded.get(key) ?? 0) + 1);
}
for (const l of removed) {
  if (!isTest(l.file) || deleted.includes(l.file) || !ASSERTION.test(l.text)) continue;
  const key = l.file + '\n' + l.text.trim();
  if (readded.get(key) > 0) { readded.set(key, readded.get(key) - 1); continue; }
  flag('assertion-removed', atBase(l));
}

// 3. A rule in CONSTRAINTS.md weakened or removed. Rules are table rows (key: first cell) or
// bullets (key: text before the first colon). Numbers get a direction from adjacent words;
// lowering a minimum or raising a maximum loosens the rule. A number with no readable direction
// is reported on any change, since silence would be the unsafe default. Numbers pair by direction.
const ruleKey = (t) => {
  const s = t.trim();
  if (s.startsWith('|')) return s.split('|').map((c) => c.trim()).filter(Boolean)[0] ?? '';
  if (/^[-*] /.test(s)) return s.slice(2).split(':')[0].trim();
  return null;
};
const MIN_BEFORE = /(>=|>|≥|at least|minimum|\bmin\b|no less than|not fall|not drop|--min[-\w]*[ =]|fail[-_]under[ =])\s*$/;
const MAX_BEFORE = /(<=|<|≤|at most|maximum|\bmax\b|no more than|under|below|not grow|not exceed|--max[-\w]*[ =])\s*$/;
const MIN_AFTER = /^\s*\S*\s*(?:\|\s*)?(or more|or higher|must not fall|must not drop)/;
const MAX_AFTER = /^\s*\S*\s*(?:\|\s*)?(or less|or lower|must not grow|must not exceed)/;
const thresholds = (text) => {
  const t = text.replace(/\b\d{4}-\d{2}-\d{2}\b/g, 'date');
  const out = [], re = /\d+(?:\.\d+)?/g;
  let m;
  while ((m = re.exec(t))) {
    const before = t.slice(Math.max(0, m.index - 24), m.index).toLowerCase();
    const after = t.slice(m.index + m[0].length, m.index + m[0].length + 40).toLowerCase();
    const dir = MIN_BEFORE.test(before) || MIN_AFTER.test(after) ? 'min'
      : MAX_BEFORE.test(before) || MAX_AFTER.test(after) ? 'max' : null;
    out.push({ n: Number(m[0]), dir });
  }
  return out;
};
const removedRules = removed.filter((l) => isConstraints(l.file) && ruleKey(l.text) !== null);
const addedRules = added.filter((l) => isConstraints(l.file) && ruleKey(l.text) !== null);
for (const r of removedRules) {
  if (isException(r.text)) continue; // deleting an exception tightens; a changed one is a new-exception
  const a = addedRules.find((x) => x.file === r.file && ruleKey(x.text) === ruleKey(r.text));
  if (!a) {
    flag('rule-removed', atBase(r));
    continue;
  }
  const was = thresholds(r.text), now = thresholds(a.text);
  let verdict = null;
  for (const dir of ['min', 'max', null]) {
    const before = was.filter((x) => x.dir === dir), after = now.filter((x) => x.dir === dir);
    before.forEach((b, i) => {
      const n = after[i];
      if (verdict) return;
      if (!n) verdict = 'threshold-removed';
      else if (n.n === b.n) return;
      else if (dir === 'min' ? n.n < b.n : dir === 'max' ? n.n > b.n : true) {
        verdict = dir ? 'threshold-loosened' : 'threshold-changed';
      }
    });
  }
  if (verdict) flag(verdict, `${atBase(r)} -> ${at(a)}`);
}

// 4. With --check-expiry: an exception past its date, or a new one longer than 90 days.
if (checkExpiry && existsSync('CONSTRAINTS.md')) {
  const day = (s) => Date.UTC(Number(s.slice(0, 4)), Number(s.slice(5, 7)) - 1, Number(s.slice(8, 10)));
  const addedLines = new Set(added.filter((l) => l.file === 'CONSTRAINTS.md').map((l) => l.line));
  readFileSync('CONSTRAINTS.md', 'utf8').split(/\r?\n/).forEach((text, i) => {
    if (!isException(text)) return;
    const dates = text.match(/\b\d{4}-\d{2}-\d{2}\b/g);
    const where = `CONSTRAINTS.md:${i + 1}`;
    if (!dates) { flag('exception-without-expiry', where); return; }
    const expires = dates[dates.length - 1];
    if (expires < today) flag('exception-expired', where);
    else if (addedLines.has(i + 1) && day(expires) - day(today) > 90 * 86400000) flag('exception-too-long', where);
  });
}

if (findings.length === 0) {
  console.log('floor-guard: clean');
  process.exit(0);
}
console.error(`floor-guard: ${findings.length} violation(s):`);
for (const f of findings) console.error(`  [${f.rule}] ${f.where}`);
if (findings.some((f) => f.rule === 'rule-removed')) {
  console.error('\nrule-removed also appears when a rule ID changed: change IDs and numbers in separate commits.');
}
if (findings.some((f) => f.rule === 'threshold-removed')) {
  console.error('\nthreshold-removed also appears when direction words were edited (">= 80%" to "80%"): compare both lines.');
}
console.error('\nEach finding lowers the bar. Fix the code; a genuine exception goes through the policy owner.');
process.exit(1);
```

## Python (`scripts/floor_guard.py`)

Python 3.8 or later, standard library only. Use it where Node is not part of the stack.

```python
#!/usr/bin/env python3
"""floor_guard.py: diff-scoped check that a change does not lower the bar set in CONSTRAINTS.md.

Usage: python scripts/floor_guard.py [--base <ref>] [--check-expiry] [--today YYYY-MM-DD]
Exit 0: clean. Exit 1: at least one violation. Exit 2: the guard could not run; never read 2 as 0.
A finding names the rule and the location, never the line's text: a flagged line can hold a secret.
Standard library only, Python 3.8+.
"""
import datetime
import os
import re
import subprocess
import sys


def option(name):
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return None


def bail(message):
    sys.stderr.write("floor-guard: " + message + "\n")
    sys.exit(2)


def git(args, diff_exit=False):
    # For an untracked file `git diff --no-index` exits 1 because the sides differ: keep that
    # output. Every other failure returns None, which the caller turns into exit 2.
    try:
        res = subprocess.run(["git"] + args, capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
    except OSError:
        return None
    if res.returncode == 0 or (diff_exit and res.returncode == 1):
        return res.stdout
    return None


# One character of each plain-word pattern sits in a class so this file never matches itself
# when it is first added. Keep that when you extend the lists for your stack.
SUPPRESSIONS = re.compile(
    r"@ts-[i]gnore|@ts-[n]ocheck|@ts-[e]xpect-error|eslint-[d]isable|biome-[i]gnore|#\s*noqa"
    r"|#\s*type:\s*ignore|#\s*pyright:\s*ignore|#\s*pragma:\s*no\s*cover|istanbul\s+ignore"
    r"|c8\s+ignore|[n]osemgrep|gitleaks:[a]llow|Stryker\s+disable|//\s*nolint|#\[allow\(")
STUBS = re.compile(
    r"throw\s+new\s+\w*Error\s*\([^)]*[Nn]ot\s+implemented|raise\s+NotImplementedError"
    r"|\bpass\s*#\s*stub|\btodo!\(|\bunimplemented!\(|panic\(\s*\"not implemented"
    r"|catch\s*(\(\s*\w*\s*\))?\s*\{\s*\}|except(\s+\w+)?\s*:\s*pass\b|\b[T]ODO\b")
SKIPS = re.compile(
    r"\.(skip|only|todo)\s*\(|\bx(it|describe|test)\s*\(|@pytest\.mark\.(skip|xfail)"
    r"|\bpytest\.skip\(|@unittest\.skip|\bt\.Skip\(|#\[ignore\]")
OPTIONAL = re.compile(r"continue-on-error:\s*true|\|\|\s*true\b")
ASSERTION = re.compile(r"\b(expect|assert|should)\b|\bassert\w*\(")
TEST_FILE = re.compile(
    r"(^|/)test_[^/]+\.py$|_test\.(py|go|rs)$|\.(test|spec)\.[cm]?[jt]sx?$|Tests?\.(java|kt)$")
WORKFLOW = re.compile(r"(^|/)\.github/workflows/[^/]+\.ya?ml$|(^|/)\.gitlab-ci\.yml$")
CONSTRAINTS = re.compile(r"(^|/)CONSTRAINTS\.md$")
EXCEPTION = re.compile(r"^\s*\|\s*[WE]\d+\s*\|")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
MIN_BEFORE = re.compile(r"(>=|>|≥|at least|minimum|\bmin\b|no less than|not fall|not drop"
                        r"|--min[-\w]*[ =]|fail[-_]under[ =])\s*$")
MAX_BEFORE = re.compile(r"(<=|<|≤|at most|maximum|\bmax\b|no more than|under|below|not grow"
                        r"|not exceed|--max[-\w]*[ =])\s*$")
MIN_AFTER = re.compile(r"^\s*\S*\s*(?:\|\s*)?(or more|or higher|must not fall|must not drop)")
MAX_AFTER = re.compile(r"^\s*\S*\s*(?:\|\s*)?(or less|or lower|must not grow|must not exceed)")


def thresholds(text):
    # Each number takes a direction from the words right next to it; dates are not thresholds.
    t = DATE.sub("date", text)
    out = []
    for m in re.finditer(r"\d+(?:\.\d+)?", t):
        before = t[max(0, m.start() - 24):m.start()].lower()
        after = t[m.end():m.end() + 40].lower()
        if MIN_BEFORE.search(before) or MIN_AFTER.search(after):
            direction = "min"
        elif MAX_BEFORE.search(before) or MAX_AFTER.search(after):
            direction = "max"
        else:
            direction = None
        out.append((float(m.group(0)), direction))
    return out


def rule_key(text):
    s = text.strip()
    if s.startswith("|"):
        cells = [c.strip() for c in s.split("|") if c.strip()]
        return cells[0] if cells else ""
    if s.startswith(("- ", "* ")):
        return s[2:].split(":")[0].strip()
    return None


def main():
    base = option("--base") or os.environ.get("CONSTRAINTS_BASE") or "origin/main"
    check_expiry = "--check-expiry" in sys.argv
    today = option("--today") or datetime.date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", today):
        bail("--today must be YYYY-MM-DD")

    # Run from the top of the work tree: `git ls-files` lists only the current subtree.
    top = git(["rev-parse", "--show-toplevel"])
    if not top:
        bail("not inside a git work tree")
    os.chdir(top.strip())
    merge_base = git(["merge-base", base, "HEAD"])
    if not merge_base:
        bail("no merge base against " + base + " (fetch it, or pass --base)")
    merge_base = merge_base.strip()

    # Committed, staged and unstaged changes against the merge base, plus untracked files.
    tracked = git(["diff", "--unified=0", merge_base, "--"])
    if tracked is None:
        bail("could not diff against " + merge_base)
    listing = git(["ls-files", "--others", "--exclude-standard"])
    if listing is None:
        bail("could not list untracked files")
    parts = [tracked]
    for path in filter(None, listing.splitlines()):
        d = git(["diff", "--no-index", "--unified=0", "/dev/null", path], diff_exit=True)
        if d is None:
            bail("could not diff untracked file " + path)
        parts.append(d)

    # Header lines run from `diff ` to the first `@@`; after that a line starting with `---` or
    # `+++` is content. Each hunk header resets the old and new line counters used in findings.
    added, removed, deleted = [], [], []
    path_of = lambda s: re.sub(r"^[ab]/", "", s).rstrip("\t")
    cur, old, in_header, old_line, new_line = "", "", False, 0, 0
    for line in "\n".join(parts).split("\n"):
        if line.startswith("diff "):
            in_header = True
        elif line.startswith("@@"):
            in_header = False
            m = re.match(r"^@@ -(\d+)(?:,\d+)? \+(\d+)", line)
            if m:
                old_line, new_line = int(m.group(1)), int(m.group(2))
        elif in_header:
            if line.startswith("--- "):
                old = path_of(line[4:])
            elif line.startswith("+++ "):
                new = path_of(line[4:])
                cur = old if new == "/dev/null" else new
                if new == "/dev/null":
                    deleted.append(old)
        elif line.startswith("+"):
            added.append({"file": cur, "line": new_line, "text": line[1:]})
            new_line += 1
        elif line.startswith("-"):
            removed.append({"file": cur, "old": old, "line": old_line, "text": line[1:]})
            old_line += 1
        elif line.startswith(" "):
            old_line += 1
            new_line += 1

    findings = []
    at = lambda l: "%s:%d" % (l["file"], l["line"])
    at_base = lambda l: "%s:%d (removed)" % (l["old"], l["line"])

    # 1. Silenced checkers, unfinished work, easier tests, optional CI checks, new exceptions.
    for l in added:
        if SUPPRESSIONS.search(l["text"]):
            findings.append(("silenced-checker", at(l)))
        if STUBS.search(l["text"]):
            findings.append(("unfinished-work", at(l)))
        if SKIPS.search(l["text"]):
            findings.append(("test-made-easier", at(l)))
        if WORKFLOW.search(l["file"]) and OPTIONAL.search(l["text"]):
            findings.append(("check-made-optional", at(l)))
        if CONSTRAINTS.search(l["file"]) and EXCEPTION.match(l["text"]):
            findings.append(("new-exception", at(l)))

    # 2. A test file deleted, or an assertion removed from a test file that stays. A removed line
    # that comes back unchanged in the same file was moved, not removed.
    for path in deleted:
        if TEST_FILE.search(path):
            findings.append(("test-deleted", path + " (file deleted)"))
    readded = {}
    for l in added:
        key = (l["file"], l["text"].strip())
        readded[key] = readded.get(key, 0) + 1
    for l in removed:
        if not TEST_FILE.search(l["file"]) or l["file"] in deleted or not ASSERTION.search(l["text"]):
            continue
        key = (l["file"], l["text"].strip())
        if readded.get(key, 0) > 0:
            readded[key] -= 1
            continue
        findings.append(("assertion-removed", at_base(l)))

    # 3. A rule in CONSTRAINTS.md weakened or removed. Lowering a minimum or raising a maximum
    # loosens the rule; a number with no readable direction is reported on any change.
    removed_rules = [l for l in removed if CONSTRAINTS.search(l["file"]) and rule_key(l["text"]) is not None]
    added_rules = [l for l in added if CONSTRAINTS.search(l["file"]) and rule_key(l["text"]) is not None]
    for r in removed_rules:
        if EXCEPTION.match(r["text"]):
            continue  # deleting an exception tightens; a changed one is a new-exception
        match = next((a for a in added_rules
                      if a["file"] == r["file"] and rule_key(a["text"]) == rule_key(r["text"])), None)
        if match is None:
            findings.append(("rule-removed", at_base(r)))
            continue
        was, now = thresholds(r["text"]), thresholds(match["text"])
        verdict = None
        for direction in ("min", "max", None):
            before = [n for n, d in was if d == direction]
            after = [n for n, d in now if d == direction]
            for i, b in enumerate(before):
                if verdict:
                    break
                if i >= len(after):
                    verdict = "threshold-removed"
                elif after[i] == b:
                    continue
                elif direction == "min" and after[i] < b or direction == "max" and after[i] > b:
                    verdict = "threshold-loosened"
                elif direction is None:
                    verdict = "threshold-changed"
        if verdict:
            findings.append((verdict, "%s -> %s" % (at_base(r), at(match))))

    # 4. With --check-expiry: an exception past its date, or a new one longer than 90 days.
    if check_expiry and os.path.isfile("CONSTRAINTS.md"):
        added_lines = {l["line"] for l in added if l["file"] == "CONSTRAINTS.md"}
        limit = datetime.date.fromisoformat(today) + datetime.timedelta(days=90)
        with open("CONSTRAINTS.md", encoding="utf-8") as fh:
            for number, text in enumerate(fh.read().splitlines(), 1):
                if not EXCEPTION.match(text):
                    continue
                where = "CONSTRAINTS.md:%d" % number
                dates = DATE.findall(text)
                if not dates:
                    findings.append(("exception-without-expiry", where))
                elif dates[-1] < today:
                    findings.append(("exception-expired", where))
                elif number in added_lines and datetime.date.fromisoformat(dates[-1]) > limit:
                    findings.append(("exception-too-long", where))

    if not findings:
        print("floor-guard: clean")
        sys.exit(0)
    sys.stderr.write("floor-guard: %d violation(s):\n" % len(findings))
    for rule, where in findings:
        sys.stderr.write("  [%s] %s\n" % (rule, where))
    rules = {rule for rule, _ in findings}
    if "rule-removed" in rules:
        sys.stderr.write("\nrule-removed also appears when a rule ID changed: change IDs and "
                         "numbers in separate commits.\n")
    if "threshold-removed" in rules:
        sys.stderr.write("\nthreshold-removed also appears when direction words were edited "
                         "(\">= 80%\" to \"80%\"): compare both lines.\n")
    sys.stderr.write("\nEach finding lowers the bar. Fix the code; a genuine exception goes "
                     "through the policy owner.\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
```

## Adapting it

- **The patterns are the only stack-specific part.** Add your language's suppression, skip and
  stub forms to the pattern lists; the diff walk, the `CONSTRAINTS.md` checks and the exit codes
  stay as they are. Keep one character of each plain-word pattern in a class (`@ts-[i]gnore`) so
  the guard does not report its own source when it is first added, and keep those tokens out of
  its comments.
- **A `.constraintsignore`** file (one glob per line) can exempt paths. Match each finding's file
  against it before reporting. The exemption then lives in a reviewed file instead of in a weaker
  rule.
- **Pattern matching is deliberately simple.** It targets the shortcuts agents take under a red
  check, not someone determined to hide a change; that is enough for a check that runs on every
  diff. When the setup needs diff-scoped budgets and ratchets in one place, move to a dedicated
  runner (the escalation path in the skill).

## Wiring it

Run the same command at every stage. Locally the guard sees staged, unstaged and untracked files;
in CI it needs the target branch's history.

Scripts (`package.json`):

```json
{
  "scripts": {
    "check:floor": "node scripts/floor-guard.mjs --base origin/main --check-expiry",
    "check:fast": "npm run check:floor && tsc --noEmit && eslint .",
    "check:task": "npm run check:fast && vitest run --coverage"
  }
}
```

Make targets:

```makefile
.PHONY: check-floor check-task
check-floor:
	python scripts/floor_guard.py --base origin/main --check-expiry

check-task: check-floor
	pytest --cov --cov-report=lcov
```

Agent edit loop. Extend the project's existing edit hook rather than adding a second one. In Claude
Code a `PostToolUse` command that exits 2 passes its stderr back to the agent, so map any failure to
2 there:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "node scripts/floor-guard.mjs --base origin/main || exit 2" }]
      }
    ]
  }
}
```

Git `pre-commit` hook (`.git/hooks/pre-commit`, or the project's hook manager):

```sh
#!/bin/sh
if command -v node >/dev/null 2>&1 && [ -f scripts/floor-guard.mjs ]; then
  node scripts/floor-guard.mjs --base origin/main || exit 1
elif command -v python3 >/dev/null 2>&1 && [ -f scripts/floor_guard.py ]; then
  python3 scripts/floor_guard.py --base origin/main || exit 1
fi
```

CI (GitHub Actions), as a required check. The default checkout is shallow and has no merge base:

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
- run: node scripts/floor-guard.mjs --base "origin/${{ github.base_ref || 'main' }}" --check-expiry
```
