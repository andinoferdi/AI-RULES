# Upgrade andino-human-procedure

Status: IN_PROGRESS
Plan Depth: STANDARD
Current Phase: Phase 3 — checks and delivery
Last Updated: 2026-11-27

## Executive Snapshot

Accepted by the maintainer on 2026-11-26: raise `andino-human-procedure` to at least the output
quality of Matt Pocock's `wizard` (mattpocock/skills 49dd158) without losing its strengths;
layout consistent with the other andino-workflow members; plan, then implement, then commit,
push and open a PR to `main` (the maintainer merges; merging is the release that `ai-rules
setup` installs). Trial design: [rubric.md](rubric.md), frozen before any skill change.
Baseline runs exist for the `wizard` arm and the current arm (collected, not yet graded).

Council verdict (5 advisors Sonnet 5.5 medium, 3 reviewers Sonnet 5.5 low; ranking tally
Executor first on all three reviews, Expansionist last on all three): **Option 1**, rewrite the
text in the sibling layout with a "Done when" per step, wizard's repository-scan list and
no-invented-UI rule, plus checkable lines for every safety guarantee; no shipped script
library, so the recorded EXCLUDE of `template.sh` stands. Reviewers' shared addition, adopted:
a "verify platform facts" rule (the current arm told the operator that repository secrets are
invisible to environment jobs, which GitHub's own help contradicts: repository secrets are
"available to GitHub Actions runs ... in a repository"). Chair's addition: the few lines that
both baseline arms got wrong (a `.env` writer that refuses a symlink) ship as short snippets
in a resource and are executed by a repository test, so the example code is proven without
becoming a library the agent must not edit.

Escalation trigger, also from the council: if the blind grade puts the candidate below the
`wizard` arm on W5, W6 or W7, the single approved fix round may add a bash-only helper that
Linux CI tests.

## Objective

Agents using `andino-human-procedure` produce, for steps only a person can do, an artifact
(script in the operator's shell, checklist, or both) and a reply that score at least as high
as the `wizard` arm on every criterion of the frozen rubric.

## Acceptance Criteria

- [ ] R1: `SKILL.md` and `GUIDE.md` carry the same body in the sibling layout (Purpose, Trigger
  and non-trigger, resource table, Prerequisites, Procedure with a quick path and gates that
  each end in "Done when", Rules, Shortcuts, Red flags, Ownership, Output, Verification,
  Worked example, Fallback, Local resources, Provenance). Frontmatter `name` and
  `description` unchanged.
- [ ] R2: the procedure names the repository files to scan (`.env*`, README, compose files,
  framework config, CI workflows with every `secrets.*`/`vars.*`, runbooks and docs), the
  value map fields, the read-only reconcile stage, the no-invented-UI rule, the
  verify-platform-facts rule, artifact choice by operator shell, static verification without
  live steps, and the reply fields.
- [ ] R3: `resources/stage-contract.md` holds the stage fields and screen layout, the checklist
  template, the script requirements as checkable lines, and tested snippets for bash 3.2 and
  Windows PowerShell 5.1: `.env` upsert that refuses a symlink or a multi-line value, keeps
  other lines, replaces in place and keeps the file mode; typed confirmation; hidden input;
  GitHub writes with a named repository and no value on a command line.
- [ ] R4: `tests/test_human_procedure_snippets.py` extracts the snippets from the resource and
  passes: bash cases always (CI has bash), PowerShell cases when `pwsh` or `powershell` exists
  (skipped otherwise, with the reason).
- [ ] R5: `resources/worked-example.md` still passes `scripts/check_andino_matt_methods.py`.
- [ ] R6: `python scripts/ci_checks.py --group skills` passes.
- [ ] R7: blind grade of the candidate arm is at least every other arm on every criterion, or
  the single approved fix round ran and the trial record states the outcome honestly.
- [ ] R8: `ai-rules setup` from this clone reports `Skill source: local folder` and installs the
  new text; branch pushed and PR to `main` opened.

## Approach and Constraints

Text plus tested snippets (Option 1). No new dependency. No change to the installer, the
catalog or profiles (the member already ships inside `skills/andino-workflow`). Snippets are
examples the agent copies into its own script; nothing loads them at runtime. Commit, push and
PR are authorized by the maintainer for this work; merging is not.

## Execution Board

| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — skill text and snippets | DONE | R1-R5 | T1, T2, T3 | snippet test 15 pass, 3 skipped on Windows; method checker PASS; `ci_checks --group skills` PASS (304 tests) |
| Phase 2 — trial | DONE | R7 | T4 | candidate 43, current 40, `wizard` 37 of 46; gate PASS ([trial.md](trial.md)) |
| Phase 3 — checks and delivery | IN_PROGRESS | R6, R8 | T5 | setup from clone into a scratch project installed byte-identical files (`Skill source: local folder`) |

## Coverage

| Requirement / failure case | Task | Check |
| --- | --- | --- |
| R1 layout, unchanged frontmatter | T2 | heading list diff against debugging/SKILL.md; `diff` of SKILL/GUIDE bodies |
| R2 procedure content | T2 | read-through against rubric W1-W11, C1-C10, N1, X1 |
| R3 snippets: replace, keep lines, append, idempotent, symlink, newline, mode | T1 | `test_human_procedure_snippets` cases below |
| R4 PowerShell available or not | T1 | test skips with reason when no PowerShell |
| R5 example contract | T3 | `check_andino_matt_methods.py` PASS for human-procedure |
| R6 repo checks | T5 | `ci_checks.py --group skills` exit 0 |
| R7 quality | T4 | grader scores, gate line in trial.md |
| R8 delivery | T5 | setup output line; `git push`; PR URL |

## Detailed Execution

### T1 — Stage contract resource with tested snippets
Status: DONE
Readiness: READY
Requirements: R3, R4
Depends on: none
Owns: Create `skills/andino-workflow/skills/human-procedure/resources/stage-contract.md`;
Create `tests/test_human_procedure_snippets.py`
Interfaces: produces fenced blocks with info strings `bash hp-env-set` and
`powershell hp-env-set` (consumed by the test); function names `env_set KEY VALUE` (bash,
uses `$ENV_FILE`) and `Set-EnvValue -Path -Key -Value` (PowerShell).

Change Specification:
- `stage-contract.md` sections: Stage fields (Stage N of M with one outcome; Open; Do; Enter
  (name, source, secret or public, destination, consumer); Before you confirm (consequence,
  undo, typed word); Done when (observable, no values); If interrupted (what to check first)).
  Screen layout for scripts. Checklist template. Script requirements as a checklist. Shell
  table bash 3.2 / Windows PowerShell 5.1 (hidden input, open URL with printed fallback,
  clear screen, typed confirmation, GitHub write). The two `hp-env-set` snippets.
- GitHub writes: bash pipes the value on stdin (`printf '%s' "$v" | gh secret set NAME
  --repo OWNER/REPO`); PowerShell lets gh prompt (`gh secret set NAME --repo OWNER/REPO`
  with no `--body`; `gh secret set --help`: "reads from standard input if not specified" and
  "Paste secret value ... in an interactive prompt"). Variables are public: `--body` allowed.
- Value quoting rule (decision): a value of `[A-Za-z0-9_./:@+=,-]*` is written bare; any
  other value is wrapped in single quotes; a value containing `'` or a line break is refused
  with a message telling the person to edit the file by hand.

```bash
env_set() {  # env_set KEY VALUE: set KEY in $ENV_FILE; every other line stays as it was
  local key=$1 value=$2 line tmp rc
  case $value in *$'\n'*|*$'\r'*) echo "refusing: $key has a line break; edit $ENV_FILE by hand" >&2; return 1 ;; esac
  if [ -L "$ENV_FILE" ]; then echo "refusing: $ENV_FILE is a symlink; edit it by hand" >&2; return 1; fi
  case $value in
    *[!A-Za-z0-9_./:@+=,-]*)
      case $value in *"'"*) echo "refusing: $key contains a single quote; edit $ENV_FILE by hand" >&2; return 1 ;; esac
      line="$key='$value'" ;;
    *) line="$key=$value" ;;
  esac
  [ -e "$ENV_FILE" ] || (umask 077 && : > "$ENV_FILE") || return 1
  tmp=$(mktemp "$ENV_FILE.XXXXXX") || return 1
  KEY="$key=" LINE="$line" awk 'BEGIN { k = ENVIRON["KEY"]; l = ENVIRON["LINE"] }
    index($0, k) == 1 { if (!done) print l; done = 1; next } { print }
    END { if (!done) print l }' "$ENV_FILE" > "$tmp" && cat "$tmp" > "$ENV_FILE"
  rc=$?; rm -f "$tmp"; return $rc
}
```

```powershell
function Set-EnvValue([string]$Path, [string]$Key, [string]$Value) {
  # Set $Key in the dotenv file at $Path; every other line stays as it was.
  $full = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path)
  if ($Value -match "[`r`n]") { throw "refusing: $Key has a line break; edit $Path by hand" }
  $item = Get-Item -LiteralPath $full -Force -ErrorAction SilentlyContinue
  if ($item -and $item.LinkType) { throw "refusing: $Path is a link; edit it by hand" }
  if ($Value -match "[^A-Za-z0-9_./:@+=,-]") {
    if ($Value.Contains("'")) { throw "refusing: $Key contains a single quote; edit $Path by hand" }
    $line = "$Key='$Value'"
  } else { $line = "$Key=$Value" }
  $text = ''; if ($item) { $text = [System.IO.File]::ReadAllText($full) }
  $nl = "`n"; if ($text.Contains("`r`n")) { $nl = "`r`n" }
  $lines = @(); if ($text.Length) { $lines = $text -split "\r?\n"; if ($lines[-1] -eq '') { $lines = $lines[0..($lines.Count - 2)] } }
  $out = New-Object System.Collections.Generic.List[string]; $done = $false
  foreach ($l in $lines) {
    if ($l.StartsWith("$Key=")) { if (-not $done) { $out.Add($line) }; $done = $true; continue }
    $out.Add($l)
  }
  if (-not $done) { $out.Add($line) }
  [System.IO.File]::WriteAllText($full, (($out -join $nl) + $nl), (New-Object System.Text.UTF8Encoding $false))
}
```

- Test (decisive cases; fixture text mirrors a real `.env` with a comment, a quoted `#`
  value and an old key):

```python
FIXTURE = "# local only\nDATABASE_URL=postgres://u:p@h/db\nPAYLANE_KEY=old\nFLAGS=\"a,#b\"\n"
# bash: ENV_FILE=<tmp>/.env; source the snippet; env_set PAYLANE_KEY new -> exit 0
assert text == FIXTURE.replace("PAYLANE_KEY=old", "PAYLANE_KEY=new")   # replaced in place
# env_set PAYLANE_KEY new twice -> same text (idempotent); env_set NEW_KEY 'a b' -> "NEW_KEY='a b'\n" appended
# env_set K "x'y" -> exit 1, file unchanged; env_set K $'a\nb' -> exit 1, file unchanged
# symlinked .env -> exit 1, link target unchanged (skip when os.symlink is not permitted)
# POSIX only: new file mode 0o600; existing file chmod 0o640 keeps 0o640
# PowerShell (pwsh or powershell on PATH, else skipTest): the same replace/append/idempotent/
# refusal cases through `powershell -NoProfile -Command ". <snippet>; Set-EnvValue ..."`
```

Actions:
- [ ] Write the test first with the extraction helper; run
  `python -m unittest tests.test_human_procedure_snippets -v` from the repository root with
  `PYTHONPATH=src;tests`; expect failure: resource file missing.
- [ ] Write `stage-contract.md` with the snippets above; rerun; expect bash and PowerShell
  cases PASS locally (Windows PowerShell 5.1 is present on the maintainer's machine).
Integration gate: the same test runs inside `ci_checks.py --group skills` (auto-discovered).
Result / Evidence: Not run — planned checks only.

### T2 — Rewrite SKILL.md and GUIDE.md
Status: DONE
Readiness: READY
Requirements: R1, R2
Depends on: T1 (links to `resources/stage-contract.md`)
Owns: Replace bodies of `skills/andino-workflow/skills/human-procedure/SKILL.md` and
`GUIDE.md` (GUIDE keeps its own header lines 1-3 and the SKILL body from Purpose on).
Interfaces: none — frontmatter and member banner unchanged (tests
`test_andino_family_installation`, `test_andino_thin_coordinator` read the banner).

Change Specification:
- Keep lines 1-14 of SKILL.md (frontmatter, title, method ID, banner) except the title
  becomes "Prepare steps only a person can do". Replace the rest with the sibling layout.
- Procedure: a quick path (the agent can do every step itself: do it, no artifact, short
  reply) and seven gates, each ending "Done when": 1 scope from the repository (file list,
  value map table: name, where the person gets it, destination, secret or public, consumer;
  built-ins such as `GITHUB_TOKEN` and values set inline in CI are not produced); 2 find what
  already happened (read-only first stage; branch done / not done / unclear-stop; never
  repeat an effect whose outcome is unknown); 3 map each journey from confirmed sources
  (URL and labels from docs or the person; undocumented: say so in artifact and reply, give
  the expected format, ask them to record the path; platform facts checked in CLI help or
  docs or marked unverified); 4 choose the artifact by the operator's shell; 5 write every
  stage to the stage contract; 6 verify statically without live steps; 7 hand off with the
  reply fields.
- Keep the existing Ownership text, positive/negative example requests and provenance, and
  extend provenance with what is now taken from `wizard` (repository scan list, invented-UI
  rule, verify-and-hand-off checks, stage UX) and what stays excluded (`template.sh`).
Actions:
- [ ] Write SKILL.md; copy its body into GUIDE.md under GUIDE's header.
- [ ] Check: `diff <(sed -n '/^## Purpose/,$p' SKILL.md) <(sed -n '/^## Purpose/,$p' GUIDE.md)`
  prints nothing; every relative link resolves (`ci_checks` link validators).
Result / Evidence: Not run — planned checks only.

### T3 — Worked example keeps its contract
Status: DONE
Readiness: READY
Requirements: R5
Depends on: T1
Owns: Modify `skills/andino-workflow/skills/human-procedure/resources/worked-example.md`
(prose only: the field table moves to the stage contract; the Python block keeps its
`result.json` and the facts `privately`, `never paste into chat`, `No external writes`).
Actions:
- [ ] Edit; run `python scripts/check_andino_matt_methods.py --runtime-root
  skills/andino-workflow --output <scratch>/matt.json`; expect `human-procedure` PASS
  (other methods may fail for unrelated reasons; record them, do not fix them here).
Result / Evidence: Not run — planned checks only.

### T4 — Candidate arm and blind grading
Status: DONE
Readiness: READY after T1-T3
Requirements: R7
Depends on: T1, T2, T3, T5's first `ci_checks` run (the rubric runs the candidate on text that
passed the skills checks)
Owns: `docs/validation/human-procedure/trial.md`, `scores.md`
Actions:
- [ ] `setup_run.py <scratch>/trial/run-4 --guide skills/andino-workflow/skills/human-procedure`;
  runner Sonnet 5.5 medium with the rubric prompt; collect with `collect_run.py`.
- [ ] Shuffle run-2, run-3, run-4 to A-C (mapping kept outside the grading folder); grader
  Sonnet 5.5 medium sees only rubric, fixture and A-C.
- [ ] Record trial.md (setup, scores table, gate, reading, limitations incl. the run-1
  usage-limit stop and run-2 resume) and scores.md (grader output).
- [ ] Gate fails: one fix round on the losing criteria, rerun candidate and grade those
  criteria, record as scores-rerun.md.
Result / Evidence: Not run — planned checks only.

### T5 — Checks, setup and delivery
Status: IN_PROGRESS
Readiness: READY
Requirements: R6, R8
Depends on: T1-T3 (first run), T4 (final run)
Actions:
- [ ] `git fetch origin WebBased` once; `python scripts/ci_checks.py --group skills`; fix
  inventories or tests the change affects; rerun to exit 0.
- [ ] `ai-rules setup` from the clone (non-interactive mode if offered); expect
  `Skill source: local folder`; confirm the installed `andino-human-procedure/SKILL.md`
  matches the branch.
- [ ] Commit on `claude/andino-workflow-skill-quality-807b44`, push, open PR to `main`.
Result / Evidence: Not run — planned checks only.

## Rulings

- Ruling: GUIDE.md keeps its own two header lines and the SKILL body from Purpose on — every
  member keeps that split — wrong only if a test compares whole files (none does).
- Ruling: after grading, fixture-like example names in the stage contract were replaced with
  neutral ones and recorded in trial.md as not re-run — the graded text had leaked fixture
  names — cost if wrong: the shipped text differs from the graded one in names only.
- Ruling: the gate passed, so the approved fix round did not run; the three criteria every arm
  scored 1 on (C4, C6, W10) are recorded as shared gaps, not fixed here.

## NEXT ACTION

T5: open the PR to `main` from the pushed branch and watch its CI. Final local evidence: `ci_checks --group skills` on the tree merged with origin/main 575eec0 ran 306 tests, OK (skipped=6), PASS: all skills checks.
