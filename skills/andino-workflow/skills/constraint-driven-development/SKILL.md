---
name: andino-constraint-driven-development
description: Use when a project has no written quality bar, when asked to set up constraints, quality gates or standards, when an agent keeps adding suppressions, skipping tests or loosening thresholds to get to green, when CI checks exist but nobody knows which ones block, when a coverage, performance or accessibility number is needed without a known value, or before agents run unattended. Operates under Andino Workflow governance.
---

# Write the quality bar down and stop agents lowering it

Internal method ID: `andino-constraint-driven-development` (alias: `constraint-driven-development`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow governance: proportional investigation, evidence-based decisions, single durable checkpoints, and anti-loop guards. Selected skills own their full procedures, resource contracts, and verification checks. Do not re-invoke `andino-workflow` recursively.

Turn "good enough to ship" into a numbered `CONSTRAINTS.md` with a command behind every number, and
block the moves an agent makes to turn a red check green without fixing anything.

## Purpose

Review guidance, a test cycle and a threat list describe what good looks like, but they are prose
an agent may skip, and they vanish when the session ends. This method leaves a file in the
repository that states this project's bar with numbers, survives every session and is checked by
commands.

The person who used to read every line no longer can. An agent produces more code in an afternoon
than a reviewer reads in a week, so judgement has to move into checks that run around the agent's
loop: checks with numbers someone chose, firing early enough that the agent repairs its own output.

Spec-driven development decides what to build, and test-driven development proves it works.
Constraint-driven development decides what "good enough to ship" means before a pull request argues
about it. A constraint counts only when breaking it ends the run with a non-zero exit.

## Trigger and non-trigger

Use when:

- a project or a significant feature starts with no written quality bar;
- the user asks to set up constraints, quality gates or standards, or to stop agents shipping
  regressions;
- an agent keeps adding suppressions, skipping tests or loosening thresholds to get to green;
- CI runs checks but nobody can say which ones block a merge and which are decoration;
- coverage, performance or accessibility numbers are argued per pull request instead of decided
  once, or someone needs a number and has none;
- agents are about to run unattended (`/build auto`, `/loop`, a scheduled job) and only a test
  suite the agent also wrote stands between them and `main`.

Do not select for:

- a project whose `CONSTRAINTS.md` exists and is not changing: read it and follow it;
- a throwaway spike or one-off script. For code expected to live two weeks, the floor is still
  worth it; the rest is not;
- an immediate code review (`andino-code-review`) or building a CI pipeline
  (`andino-ci-cd-and-automation`). Those methods consume the contract this one writes.

## Select a resource, not a second lifecycle

Load only the resource the current step names. It runs inside this procedure; it starts no second
plan.

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| Writing or adapting the diff guard; wiring it into hooks and CI | [floor-guard](resources/floor-guard.md) | The project already runs a guard that meets its contract |
| Tools, install commands and defaults for TypeScript, Python, Go, Rust or web; changed-line coverage | [constraint-catalog](resources/constraint-catalog.md) | Every chosen dimension already has a working command |
| Scanners that exit 0 on findings (Semgrep, axe), redaction, the exception schema | [quality-gate-protocols](resources/quality-gate-protocols.md) | No scanner dimension was chosen |
| One setup end to end, including a rejected evasion | [worked-example](resources/worked-example.md) | The procedure is already clear |

## Prerequisites

- Write access to the repository's instruction files and CI configuration, or a user who applies
  the proposed changes.
- Git history with a merge base against the target branch; the guard needs it.
- Whether a person can answer questions now. That decides step 2.

## Procedure

1. **Detect before asking.** Read what the repository already says, and ask nothing it answers.

   | What | Where to look |
   | --- | --- |
   | Language, stack, deployables | `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, workspace layout |
   | Test runner and coverage provider | dev dependencies, test scripts, coverage configuration |
   | Linters and type checkers, and whether they block | lint configuration; CI steps, including any marked `continue-on-error` |
   | Coverage on record | `coverage/`, lcov or XML reports, CI artifacts: the value, command, revision and precision |
   | CI and required checks | `.github/workflows/`, `.gitlab-ci.yml`, notes on branch protection |
   | Agent harness | `.claude/`, `.codex/`, `AGENTS.md`, `CLAUDE.md`, existing edit hooks |
   | Existing suppressions and stubs | the floor's patterns searched across the current tree |
   | A running URL | preview deploys or a local server; none for a CLI, a library or an API without UI |

   Report what you found in two lines. Done when every row has an answer or is marked unknown.

2. **Ask only what is left.**
   - **No person to answer** (a non-interactive run: CI, `/loop`, a scheduled job): run no
     interview and invent no thresholds. Apply the floor only: the floor section of
     `CONSTRAINTS.md`, the guard from step 6, no numbered rows. Record in the contract and in the
     run's report that only the floor was applied, and list the open questions for a human.
     Stop there.
   - **A person is available:** ask at most four questions, one question at a time. Give each a
     GUESS based on step 1 and a DEFAULT, so "I don't know" is a complete answer that still
     produces a working setup, and say what each pick costs.

   ```text
   Q1: Beyond the floor, which should be enforced?
       (a) coverage on new code  (b) security scanning  (c) performance budgets
       (d) accessibility  (e) architecture boundaries
   GUESS: <from step 1>    DEFAULT: (a) and (b)
   Cost: (c) and (d) need a running URL; (e) needs a rules file and a decision about existing violations.

   Q2: When a check fails while the agent is mid-task, block or warn?
   GUESS: block when agents run unattended    DEFAULT: block on the floor, warn on the rest for two weeks

   Q3: Target numbers, or measure today and hold that line?
   GUESS: measure and hold    DEFAULT: measure and hold; changed lines at 80%

   Q4: The slowest check you will tolerate before the agent hands work back?
   GUESS: about 90 seconds    DEFAULT: 90 seconds at task end, near-instant per edit, unlimited in CI
   ```

   Who approves exceptions and who owns the file are authority questions, not intake; ask them as
   well when step 1 does not answer them. Done when each question has an answer or the stated
   default, recorded for the report.

3. **Establish comparable baselines.** Measure a clean reference revision with the same command,
   scope, configuration and reporting precision the rule will use, and record the revision and the
   result. A figure on record from another command, scope or machine goes into the contract with
   its source and is re-measured with the enforcing command (the first CI run is enough) before a
   ratchet compares against it. A failed, partial or incomparable run leaves that metric pending,
   and existing gates stay in force meanwhile. Changed-line coverage needs no baseline: it applies
   to new code from the first change, at 80% unless the user chose a number. Done when every
   measured row has a value with its source, or a pending reason.

4. **Write `CONSTRAINTS.md`.** One file at the repository root, where every agent on every harness
   reads it and every change to it shows up in review. Use stable IDs, explicit minimums or
   maximums, and exact commands that run from the repository root. Keep project coverage and
   changed-line coverage in separate rows. Put the reason next to every number: a threshold
   without one gets deleted by the next person it blocks.

   ```markdown
   # Constraints

   Last reviewed: <YYYY-MM-DD> by @<owner>

   ## Floor (always enforced, no setup required)

   - No new suppression comments (`@ts-ignore`, `eslint-disable`, `# noqa`, `# type: ignore`, coverage-ignore pragmas)
   - No skipped, focused or deleted tests, and no assertions removed from tests that stay
   - No unimplemented stubs, empty catch blocks or `TODO` standing in for an implementation
   - No secrets in source; secret scanners run with `--redact`
   - No check made optional in CI (`continue-on-error: true`, `|| true`)
   - This file is not weakened to make a change pass

   ## Enforced

   | ID | Rule | Why this number | Checked by | Runs at |
   |----|------|-----------------|------------|---------|
   | F1 | Diff passes the floor guard | No number: any move that lowers the bar | `node scripts/floor-guard.mjs --base origin/main --check-expiry` | edit, task end, CI |
   | Q1 | <metric, scope and threshold> | <the reason for this number> | <exact command from the repository root> | <stage> |

   ## Measured, not yet enforced

   | ID | Metric | Today | Source (command, revision, precision) | Direction | Tolerance |
   |----|--------|-------|----------------------------------------|-----------|-----------|

   ## Pending or not applicable

   | Dimension | Why it is not enforced here | Becomes enforced when |
   |-----------|-----------------------------|-----------------------|

   ## Known debt (predates this file; not exceptions)

   ## Exceptions

   | ID | Rule | Path | Reason and ticket | Owner | Approved by | Expires |
   |----|------|------|-------------------|-------|-------------|---------|

   No exceptions are approved.
   ```

   - Add one line to `AGENTS.md` and `CLAUDE.md` (or the file `CLAUDE.md` imports):
     `Read CONSTRAINTS.md before writing code. Do not weaken it to make a change pass.`
   - List suppressions and stubs already in the tree under Known debt. The guard reads only
     changed lines, so they do not fail today, and they are not exceptions.
   - Scripts that run the checks (`package.json`, a `Makefile`) mirror the `Checked by` column.
     `CONSTRAINTS.md` is canonical: when the two drift, the file wins and the script is fixed.

   Done when every enforced row has an exact command, every number a reason, and the pointer line
   exists.

5. **Install what each dimension needs.** A chosen dimension needs a tool and a command that runs
   today. Use the established tool over a home-made checker, so the team's existing configuration
   keeps working. Install commands per ecosystem are in
   [constraint-catalog](resources/constraint-catalog.md).

   | Dimension | Tool | Gate on |
   | --- | --- | --- |
   | Types | `tsc --noEmit`, mypy, `go vet` | any error |
   | Lint | the project's existing configuration | any error |
   | Coverage | the test runner and its coverage provider | changed lines; project ratchet |
   | Security: secrets | gitleaks with `--redact` | any finding |
   | Security: dependencies | osv-scanner, pip-audit, govulncheck | high or above |
   | Security: code | Semgrep through the quality gate | high or critical, including legacy `ERROR` |
   | Performance | Lighthouse, size-limit | LCP, CLS, per-entry bytes |
   | Accessibility | axe-core through the quality gate | zero critical or serious |
   | Architecture | dependency-cruiser, ESLint `no-restricted-imports`, import-linter | any violation |
   | Assertion quality | Stryker on changed files | mutation score |

   Five things that bite when skipped:

   1. **`--redact` on gitleaks is not optional.** Without it the matched secret lands in the agent's
      transcript, and from there in logs, summaries and commit messages. Report the rule and the
      location, never the value.
   2. **Lighthouse and axe need a running URL.** With none (a CLI, a library, an API without UI),
      record the dimension as not applicable here and name where it belongs, instead of wiring a
      check that cannot run.
   3. **Scope expensive checks to the diff.** Stryker takes `--mutate <changed files>` and Semgrep
      takes the changed paths (`git diff --name-only`). On a whole repository they take hours and
      get switched off.
   4. **Coverage needs no second run.** Read the lcov or XML the suite already writes and intersect
      it with `git diff`, without a second test run.
   5. **Semgrep registry rules are free to run; check their licence before redistributing them.**
      opengrep reads the same rules and writes the same JSON.

   - Add a missing coverage provider (Vitest without `@vitest/coverage-v8`) to the manifest, pinned
     to the test runner's version, even when it cannot be installed here; report the lockfile
     update as the remaining step. Leaving coverage pending because this environment cannot
     install it gives up a dimension the user chose.
   - A missing lockfile does not drop the dependency dimension. Scan what CI installs (`pip-audit`
     after the install step, `npm audit --audit-level=high` after `npm ci`, osv-scanner once a
     lockfile is committed) and report the lockfile as a prerequisite.
   - A new rule that current code already breaks, such as an existing violation of a layer
     boundary, is fixed in the setup change or recorded as Known debt or an approved exception. A
     gate that fails forever teaches people to ignore red; a rule that quietly skips the violation
     enforces nothing.
   - `semgrep scan` and `axe` can exit 0 with findings: run them through the quality gate in
     [quality-gate-protocols](resources/quality-gate-protocols.md).

   Done when every chosen dimension has a command that runs today, locally or in CI. A row stays
   pending only when it cannot run anywhere yet (no URL, no rules decided), and names what is
   missing.

6. **Wire it to the lifecycle.** Running everything everywhere is the biggest mistake. A check that
   stalls the agent gets switched off, and a gate people switched off is worse than none, because
   the bar still looks real.

   | Stage | Trigger | What runs | Budget |
   | --- | --- | --- | --- |
   | Edit | the existing edit hook | floor guard; types or lint on changed files | under 5 seconds |
   | Task end | `check:task` before the agent reports done | tests, changed-line coverage | under 90 seconds, or the user's number |
   | Review | pull request | full guard, security scans, mutation on the diff | minutes |
   | Ship | required CI checks | everything above, plus checks against a preview URL | uncapped |

   - Extend the existing edit hook rather than adding a second one.
   - Time the fast path. Anything over a few seconds moves to a later stage. Tools that install
     machine-wide (gitleaks, osv-scanner, Semgrep) can run in CI only; say so in `Runs at`.
   - Run the guard at edit, at task end and in CI. Locally it sees staged, unstaged and untracked
     files; CI needs the target branch's history (`fetch-depth: 0`) and a required check that
     fails on exit 1 and on exit 2.
   - Make a check that was decoration (`continue-on-error: true`) blocking, or record why it stays
     advisory.

   Done when every enforced row's `Runs at` names a stage that actually runs it, and the fast
   stage is timed.

7. **Prove the wiring.** In a disposable copy, run each enforced command the way CI will run it,
   against a clean control and a deliberate violation: the violation fails and the control passes.
   Run once more with an unavailable prerequisite (no merge base, a missing report) and expect
   exit 2. For a numeric gate, test at the threshold and just past it. For a severity gate, check
   that a below-threshold finding passes and a scanner error fails. A generated report is not an
   enforced number. Record each check you could not run as unavailable, with the next step to
   obtain the evidence. Done when every enforced row has an observed pass and fail, or an explicit
   unavailable entry.

8. **Respond to a red gate.** Fix the behavior and rerun the check, keeping the threshold and the
   assertions. If the deadline arrives first, hand off the failing evidence and keep the change
   blocked while an exception is considered (see Exceptions). Done when the check passes against
   unchanged rules, or the change is blocked with its evidence handed to the policy owner.

## Rules for every contract

### The floor

Six rules hold from the first commit, with no setup: no new suppressions; no skipped, focused or
deleted tests and no removed assertions; no stubs, empty catches or `TODO` placeholders; no secrets
in source; no check made optional in CI; no weakening of `CONSTRAINTS.md`. The guard in
[floor-guard](resources/floor-guard.md) enforces all but the secrets rule as moves in the diff:
a threshold moved, a test made easier, a checker silenced, work left unfinished, an exception
added, a check made optional (`check-made-optional`). A secret scanner run with `--redact`
enforces the secrets rule.

Four suppressions need extra attention because they switch off a check you rely on:
`istanbul ignore` removes code from coverage instead of testing it, `Stryker disable` hides a
surviving mutant, and `nosemgrep` and `gitleaks:allow` do the same for security findings.

The guard compares the merge base with the working tree. Exit 0 is clean, 1 is a violation, and
2 means the check could not run; treat 2 as a failure, never as clean. Tightening is silent;
loosening is loud. Findings name the rule and the location, never the line's text.

### Rank checks by how circular they are

Ask one question of every check: could the agent pass it by writing code that does not work?

- **External**: axe-core encodes WCAG, osv-scanner reads a vulnerability database, Lighthouse
  measures a real browser. The agent cannot argue with these.
- **Project**: the team's lint rules, layer boundaries and secret-scanning rules. A person owns the
  file, and changing it takes review.
- **Suite**: the project's own tests. The most useful kind, and circular when the agent wrote both
  the code and the tests.

A bar made only of suite checks can pass while the product is broken or insecure. A production
contract enforces at least one external or project check; in a first setup, record a missing one
as pending with its prerequisite.

### Ratchets when there is no number

Set 80% project coverage on a codebase at 62% and the build stays red forever, until the team
learns to ignore red builds. A ratchet needs no decision: record today's value and its direction,
and compare every later measurement against it. When the number improves, propose the new value
in a separate reviewed policy change; when it drops, that is the finding. Compare only complete,
passing measurements from the same command and scope. When a configuration change breaks the
comparison, remeasure the reference first and keep the current gate in force meanwhile.

The ratchet also adds something training lacks. Models are rewarded for passing tests, which are
judged in seconds; architectural decay shows up over months and never reaches that reward. A
ratchet is the missing penalty, written where the build can see it.

### Exceptions

An exception unblocks one path without lowering the rule for everyone. Add one only after the
policy owner authorizes it, in its own change, separate from the failing feature. Each row records
the rule ID, the narrowest path (no wildcard that covers future files), the reason with a ticket,
an individual owner, who approved it, and an expiry within 90 days. Keep the global rule
unchanged. The guard reports every added or changed row as `new-exception` and, with
`--check-expiry`, every expired row; the owner's review is what verifies the approval. Deleting an
exception once the debt is paid tightens the bar and needs nothing.

### Sane defaults

When the user has no number, use these; most codebases meet them on day one. State the number and
the reason together.

| Constraint | Default | Why this number |
| --- | --- | --- |
| Changed-line coverage | ≥ 80% | High enough to force a test, low enough to allow a configuration line |
| Project coverage | today's value, must not fall | Needs no argument to adopt |
| Mutation score (if used) | ≥ 60% on changed files | Typical for a suite never mutated before; 80% is mature |
| Dependency vulnerabilities | nothing at high or above | Below that is mostly noise |
| LCP | ≤ 2500 ms | The Core Web Vitals "good" threshold |
| CLS | ≤ 0.1 | The Core Web Vitals "good" threshold |
| Accessibility | zero critical or serious axe violations | Moderate and minor findings are often debatable |
| Exception lifetime | 90 days | Long enough to plan the fix, short enough to remember it |
| Ratchet tolerance | 0.5 percentage points | Absorbs drift when an unrelated file moves the number |
| Edit-stage budget | under 5 seconds | Slower checks get switched off |
| Task-end budget | 90 seconds | Longer, and agents stop running it |

### Escalation path

Constraints come in three levels of teeth. Start at the level the project can sustain.

1. **Written**: `CONSTRAINTS.md` exists and agents read it. It costs nothing, catches honest
   mistakes and relies on compliance.
2. **Scripted**: `check:fast` and `check:task` scripts (or make targets) wired into the edit hook
   and CI. Deterministic, with no new dependency. Most projects stop here.
3. **Tool-backed**: a dedicated runner that handles diff scoping, budgets, ratchets and the floor.
   Worth it once the check-running shell grows past about thirty lines.

A first run can be floor-only. The guard needs no installs, so enforce the floor on day one and
add numbered dimensions as each tool is installed.

## Shortcuts that lower the bar

| Shortcut | Reality |
| --- | --- |
| "We'll add constraints once the code settles." | Code settles around whatever was allowed while it was moving. Add the floor on day one. |
| "The tests are our constraints." | Tests you wrote prove you agree with yourself. They say nothing about coverage of new code, dependency risk or bundle growth. |
| "We can't hit 80% on this legacy code." | Then don't set 80%. Record today's number and hold it. |
| "The checks slow the agent down." | Only when slow checks sit in the edit loop. That is a placement error: move them. |
| "I'll remember our standards." | The agent writing most of the code keeps no memory between sessions. Write them down. |
| "This constraint blocks an emergency fix." | An exception with an owner and a date unblocks one path. Deleting the constraint unblocks everyone, forever. |
| "Lower it now, raise it next sprint." | Nothing enforces the raise. Write the missing tests, or route an exception through the owner. |

## Red flags

Stop and reconsider when:

- `CONSTRAINTS.md` changes in the same commit as the feature that was failing;
- the agent proposes relaxing a threshold instead of fixing the code;
- the intake ran past four questions, asked what `package.json` already says, or produced a
  configuration the user cannot explain;
- a row has a number but no exact command in `Checked by`, or a command that cannot run today;
- a budget is set that the codebase fails today, with no plan to reach it;
- a checker was hand-rolled where an established tool exists, so the team's configuration is ignored;
- every constraint is judged by the project's own tests, with no external or project check;
- an exception has no individual owner, no ticket, or an expiry more than 90 days out;
- gitleaks runs without the `--redact` flag, or a guard prints the matched line;
- a guard returns 0 when the diff could not be collected (that is exit 2);
- slow checks landed in the edit loop and someone has started passing `--no-verify`;
- nobody has opened `CONSTRAINTS.md` since it was written.

## Ownership and permission boundary

- Keep policy and gate changes separate from the failing feature. Changes to the contract, gate
  scripts, CI jobs or measurement configuration (coverage excludes, lint configuration) need
  maintainer review; a CODEOWNERS entry for the policy owner makes that mechanical.
- Installing dependencies, changing CI, branch protection and required checks follow the user's
  authority. Propose what you cannot apply, and say who must apply it.
- Keep secret values and raw scanner findings out of transcripts and reports.
- Loading this method grants no commit, push or install authority.

## Output

- The concrete `CONSTRAINTS.md`, and the pointer line in the agent instructions.
- The entrypoints by stage (scripts, hooks, CI steps) with their prerequisites.
- A check record: the tested revision or diff, the command, the result, and the observed duration
  where a budget applies. Proposed commands and unrun checks stay apart from observed results.
- In an unattended run: the floor-only contract, a note that only the floor was applied, and the
  open questions for a human.
- When work remains: the blocking gate and one `NEXT ACTION` in the active Andino ticket.

## Verification

The method was applied when:

- [ ] `CONSTRAINTS.md` exists at the repository root, and every number in it states its reason.
- [ ] The floor guard runs at edit, task end and CI, and passes on the current code without changes.
- [ ] Every dimension the user chose has a tool and a command that runs today, locally or in CI; pending rows are only for dimensions that cannot run anywhere yet.
- [ ] Each row says where it runs, and the edit stage stays within a few seconds.
- [ ] At least one enforced constraint is external or project-owned, not judged only by the project's own tests.
- [ ] Measured metrics record today's value, its source and a direction.
- [ ] Exceptions have an individual owner, a ticket, an approver and an expiry within 90 days, or the table says none are approved.
- [ ] `AGENTS.md` or `CLAUDE.md` points at the file.
- [ ] Each enforced command failed on a deliberate violation and passed a clean control; scanner errors fail and below-threshold findings pass.
- [ ] A trial run on the current branch produces no failure the user disagrees with.

## Worked example and anti-pattern

[worked-example](resources/worked-example.md) follows a TypeScript billing service from detection
and intake through the contract, wiring and proof, to the guard rejecting an agent's shortcut.

Anti-pattern: facing a red coverage check, an agent edits `CONSTRAINTS.md` from ≥ 80% to ≥ 70% on
the feature branch, adds `it.skip` to the failing test and reports success. The guard reports
`threshold-loosened` and `test-made-easier`. The right move is to restore both and write the test,
or to hand the failing evidence to the policy owner.

## Fallback

- No person to answer: the floor only (step 2).
- No merge base: the guard exits 2. Record the floor as unavailable and fetch the target branch
  (in CI, `fetch-depth: 0`); never treat the run as clean.
- A tool cannot be installed in this environment (no network, no approval) but CI can install it:
  declare it (a manifest entry or a CI install step), enforce the row at the CI stage, and record
  the local proof as unavailable with the step that obtains it. A row is pending only when it
  cannot run anywhere yet.
- No running URL: accessibility and page performance are not applicable in this repository; name
  where they belong.

## Local resources

- [resources/floor-guard.md](resources/floor-guard.md): the Node (`floor-guard.mjs`) and Python (`floor_guard.py`) guards, their contract and wiring.
- [resources/constraint-catalog.md](resources/constraint-catalog.md): tools, commands and defaults for TypeScript, Python, Go, Rust and web; changed-line coverage.
- [resources/quality-gate-protocols.md](resources/quality-gate-protocols.md): exit-code normalizers for Semgrep and axe, redaction, the exception schema.
- [resources/worked-example.md](resources/worked-example.md): one setup end to end.

## Operational example (offline)

```python andino-operational-example
import json, os, re
def floor(diff, old_min, new_min, available=True):
    if not available: return {"exit": 2, "rules": ["baseline-unavailable"]}
    findings = []
    in_hunk = False
    for line in diff.splitlines():
        if line.startswith("@@"): in_hunk = True; continue
        if not in_hunk: continue
        if line.startswith("+") and not line.startswith("+++"):
            if re.search(r"@ts-ignore|eslint-disable|biome-ignore|#\s*noqa|\.skip\(", line[1:]): findings.append("silenced-or-skipped")
            if re.search(r"Not implemented|catch\s*\{\s*\}|\bTODO\b", line[1:]): findings.append("unfinished-work")
        if line.startswith("-") and not line.startswith("---") and re.search(r"\b(assert|expect)\b", line[1:]):
            findings.append("assertion-removed")
    if new_min < old_min: findings.append("threshold-loosened")
    return {"exit": 1 if findings else 0, "rules": sorted(list(set(findings)))}
def probe():
    diff = "--- a/test.py\n+++ b/test.py\n@@ -1 +1,3 @@\n-assert answer == 42\n+// @ts-ignore\n+throw new Error('Not implemented');\n"
    if os.getenv("ANDINO_NEGATIVE"): return floor("", 80, 80, False)
    return floor(diff, 80, 70)
print(json.dumps(probe(), sort_keys=True))
```

Default output: `{"exit": 1, "rules": ["assertion-removed", "silenced-or-skipped", "threshold-loosened", "unfinished-work"]}`  
Adversarial output (`ANDINO_NEGATIVE=1`): `{"exit": 2, "rules": ["baseline-unavailable"]}`

## Provenance

Adapted from addyosmani/agent-skills `skills/constraint-driven-development` (commit 9c7f62d) under
the MIT license; the packaged notice is in [references/license.md](references/license.md). Andino
additions: the Python guard and quality gate, the multi-stack catalog, comparable baselines, exit 2
treated as blocking, the exception schema with its expiry check, policy changes kept separate, the
disposable-fixture proof and the output contract. Upstream is audit provenance only; nothing is
installed or fetched at runtime.
