# CI coverage and release gates

Status: DONE
Depth: STANDARD
Date: 2026-10-29

## Executive Snapshot

User approved the Council recommendation and authorized local implementation:
map coverage across AI-RULES, fix evidenced gaps, retain manual model-behavior
testing and avoid automated model calls in CI. Initial scope was local changes;
the user subsequently authorized commit and push to main. Release publication
and hosted settings changes remain outside scope. Council decision is in
`../completed/ci-scope-council.md`.

Local implementation complete: shared release gates, installer platform coverage,
frozen-bundle validation, full-file standalone smoke and Python-resource packaging
fix. Final suite passed 334 tests (5 conditional skips); Windows executable installed
eight bundles without Git and all 960 files matched frozen inputs. Hosted runs are
not executed; read-only APIs showed main has no merge protection/effective rules.

Baseline: main at bcbdd951cedb971815c490f52def32757c009016.
Only the prior Council checkpoint was untracked at entry; preserve it.
Current host: Windows, Python 3.12.10, required project packages already installed.

## Objective

Make CI's model-free guarantees explicit and ensure release advancement depends
on applicable validation. Prefer reuse of current validators/tests over new tooling.

## Acceptance Criteria

- One coverage matrix covers every first-party package/family, installer/CLI,
  bundled distribution, release path, and manual-only behavior claims.
- Existing `validate` job remains and retains every current deterministic check.
- Release build/publication cannot advance when required shared checks fail.
- Supported interpreter/platform checks address concrete uncovered paths, without
  unnecessary duplicate full-suite execution.
- Any added executable validation has failing-then-passing regression evidence;
  existing validators and relevant suite pass against current bytes.
- No model calls, behavioral-eval runners, secrets, deployment, or remote settings
  changes are introduced. Hosted results/protection and manual model behavior are
  explicitly unverified until observed.

## Current State and Phase

CURRENT PHASE: Review and verify current implementation

## Execution Board

| ID | Phase | Dependencies | Status | Result / evidence |
| --- | --- | --- | --- | --- |
| C1 | Map evidence and settle exact implementation seams | None | DONE | Baseline 328 tests passed (5 skips); all four validators/audits passed. Three concrete gaps selected below. |
| C2 | Add focused regression and implement evidenced gates | C1 | DONE | Frozen-package guards and file-complete smoke have RED/GREEN evidence; packaging Python-resource fix rebuilt successfully on Windows. |
| C3 | Document coverage and targeted manual testing | C1, C2 | DONE | docs/ci-coverage.md maps all eight packages, WebBased boundary, installer, frozen distribution, release, external-service limits and manual testing; README/eval links added. |
| C4 | Review and verify current implementation | C2, C3 | DONE | Final suite passed 334 tests (5 skips), 187.660s. Fixed executable installed eight packages with 960 identical files and VERIFIED locks; workflow syntax, links, checksums and final diff check passed. |

## Scope and inspected evidence

- `.github/workflows/validate-skills.yml`: one Ubuntu validation job, branch
  fetch, editable package install, four validators/audits plus unittest discovery;
  no explicit Python version. Main PR/push, dispatch and daily triggers.
- `.github/workflows/release.yml`: OS build matrix, `--help` smoke, tag publish
  depending only on builds. No validation dependency in this workflow.
- `tests/installer/__init__.py` exists: installer tests already participate in
  root discovery. A Windows-only junction regression is skipped on Ubuntu;
  CI currently has no Windows installer-suite job.
- `pyproject.toml`: Python >=3.11. Validation currently relies on runner default;
  release explicitly uses Python 3.12.
- `scripts/build_release.py::stage_bundles`: archives manifest commits, checks
  root skill identity, refuses an existing staging directory. Further package
  structural validation is not present in this function.
- `src/ai_rules/release/data/release_manifest.json`: eight frozen first-party
  package commits. Current runtime-branch validation and frozen-distribution
  validation are distinct claims; do not require frozen commits to equal branch
  heads, since intentional frozen releases are supported.
- Existing full CI validates latest fetched refs; manual behavior evaluation is
  explicitly outside CI in `evals/README.md`.

## Decisions and constraints

- Do not repeat Council or delegate implementation: selected work is coupled,
  one coordinator can implement and verify directly.
- Reuse validation through an accepted GitHub Actions mechanism after checking
  official documentation. Preserve existing required check naming where possible.
- Avoid dependency-lock, lint/type tools, or security scanners unrelated to
  an evidenced acceptance gap in this bounded change.
- First assess existing `stage_bundles` and package validators before adding any
  separate release checker; reuse the smallest suitable seam.

### Settled implementation and evidence

- EXTEND existing `stage_bundles(targets, destination, repo_root) -> dict` rather
  than create a new release validator. After archiving each pinned commit/subpath,
  reuse `directory_files` and `package_files`; reject structural errors before
  PyInstaller. Reject empty target sets before creating a staging directory.
- Regression 1: a frozen package with a missing linked resource, later repaired on
  branch head, previously staged successfully (RED: ValueError not raised). GREEN
  now rejects the broken frozen package. Positive test also proves a valid frozen
  revision remains accepted after the branch head becomes broken.
- Regression 2: empty manifest targets previously staged successfully (RED:
  ValueError not raised); GREEN rejects them without creating a destination.
- Existing generic source-subpath fixture was made a valid Markdown skill package
  for its release-staging test; binary archive/subpath tests remain intact.
- ADOPT GitHub's native `workflow_call` and `needs`, reusing local validation from
  the caller's commit. `release.quality -> build -> publish` is the dependency chain.
  Official sources read through Web and Context7 `/websites/github_en_actions`:
  https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows
  https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- Preserve validate job, main PR/push/dispatch/daily triggers and all prior commands.
  Pin validation Python to 3.12. Root suite covers Ubuntu 3.12; installer-only matrix
  adds Ubuntu 3.11, Windows 3.12, macOS 3.12 without duplicating the entire suite.
- `--stage-only` validates all frozen bundles in the quality workflow. Every release
  build repeats validation on actual build inputs and runs a bundled `everything`
  project install with PATH empty, preventing Git acquisition fallback. The initial
  SKILL.md-only smoke was superseded by scripts/smoke_release.py after the resource
  loss below was reproduced; every frozen file must now match installed bytes.
- Hosted protections remain unknown; adding checks does not configure required
  status policies (later read-only inspection below resolves this baseline
  unknown). No existing workflow action major versions are changed.

## Verification plan

Baseline/current: existing four CI validator/audit commands and
`python -m unittest discover -s tests`. Focused commands depend on settled seam.
Use an available workflow validator if present; otherwise parse YAML and document
the semantic/hosted limits. Cross-platform GitHub executions cannot be claimed
from the current Windows host. No workflow is dispatched or release published.

## Method evidence

Andino current instructions reused; planning, plan-execution and TDD guides loaded
for this phase. CI specialist reused. Search First loaded for official reusable
workflow research; no independent implementation workers requested.

## Verification and review evidence

- Baseline: root unittest discovery passed 328 tests with 5 skips on Windows
  Python 3.12.10; package, Three.js, capability-schema and skripsi audits passed.
- Focused GREEN: 13 source-subpath/release tests passed after both new regressions
  exhibited the intended RED assertion failures before their implementation.
- Mutated a temporary copy of build_release.py to remove both new validation
  guards. Exactly the two regression tests failed by assertion, with no test
  errors; source files and real builder remained unchanged.
- `build_release.py --stage-only --output build/ci-frozen-bundles` completed for
  eight frozen bundles. Generated source records match the manifest exactly and
  every root SKILL.md exists. This is package integrity, not model behavior.
- `go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.7 -shellcheck= -pyflakes=
  .github/workflows/validate-skills.yml .github/workflows/release.yml` exited 0.
  Go downloaded the pinned checker/dependencies into its normal cache; no new
  project or CI dependency was introduced. ShellCheck/Pyflakes were disabled;
  executable workflow commands still need the runtime smoke below.
- All local links in docs/ci-coverage.md resolve.
- Earlier root unittest discovery passed 330 tests with 5 skips in 194.690s on
  Windows/Python 3.12.10. The additional two tests account for the baseline delta.
- `git diff --check` passed at that checkpoint; the packaging discovery below
  subsequently required new code and a fresh final suite.
- Self-review uses the loaded code-review guide with separate Spec/Standards axes;
  includes owned untracked docs and both checkpoints, not only tracked Git diff.
- A user continuation interrupted the earlier verification tool response. Current
  files/checkpoint and absence of matching processes were checked; commands without
  observed results were rerun. Already-completed staging evidence was retained.

### Reproduced packaging defect

- Windows executable built successfully (build/ci-release-windows). Existing help
  and the initial all-SKILL.md smoke passed through the actual workflow Bash body.
- Independent full-file comparison failed: installed Three.js resource
  `skills/threejs-3d-generator/scripts/threejs_3d_asset.py` was missing. The checked
  frozen source contains it. Temporary smoke project was cleaned; logs retained
  in build/ci-release-windows/workflow-smoke.log.
- CONFIRMED cause: packaging/ai_rules.spec uses collect_data_files with its default
  include_py_files=False. Installed PyInstaller 6.22.3 source/docstring explicitly
  excludes Python sources by default, explaining why SKILL.md was present while
  the resource .py file was absent. This is a build-time resource issue, not agent
  behavior or a runtime branch mismatch.
- Reopen C2 to preserve raw Python resources in the release package and replace
  the shallow SKILL.md smoke with a reusable model-free full-file smoke checker.
  Add focused missing/corrupt-resource regressions, run the checker against the
  existing bad executable, then rebuild and repeat the exact scenario.
- Four tests for verify_bundle_files cover missing Python resources, same-size
  binary corruption, valid mixed resources and empty expected trees. The first
  two exhibited intended RED assertion failures, then all four passed.
- `python scripts/smoke_release.py --executable
  build/ci-release-windows/ai-rules-windows-x64.exe` failed against the original
  executable with the exact missing threejs_3d_asset.py resource, confirming the
  new CI smoke catches the actual defect beyond the old successful smoke.
- Packaging now sets include_py_files=True specifically for ai_rules.release;
  raw skill Python resources are data, not application imports. Verified against
  installed PyInstaller 6.22.3 source and matching versioned Context7 docs:
  https://pyinstaller.org/en/stable/hooks.html#PyInstaller.utils.hooks.collect_data_files
- Rebuild uses the original owned PyInstaller work cache. Before renaming the old
  artifact to before-resource-fix.exe, its checksum and both absolute paths were
  checked against the owned workspace and manifest. Original failure logs remain.
- The final workflow delegates executable smoke to scripts/smoke_release.py on
  each platform. It exports frozen inputs separately, runs help and the whole
  bundled installation with PATH empty, compares every file byte for byte, and
  requires a complete VERIFIED lock. It does not depend on an installed host agent
  or invoke any skill/resource script.
- Faulty-copy sensitivity check removed both file-presence and byte-comparison
  guards from smoke_release.py: missing-Python and corrupt-binary cases failed as
  expected; positive/empty-tree cases retained expected outcomes, without errors.
- actionlint exited 0 again after replacing the initial Bash smoke with the final
  Python checker. Current git diff --check also passed.
- Removed the now-redundant separate --help step: the new checker preserves this
  check while avoiding a second executable extraction/startup. Final actionlint
  passed after this workflow edit; final coverage-guide links resolve.
- Rebuilt Windows executable successfully with the packaging fix; source staging
  was cleaned. Analysis-00.toc explicitly contains the formerly missing .py asset
  as DATA. Its checksum and source records match the rebuilt sidecar manifest.
- Final root suite and the real standalone smoke run concurrently only after
  confirming source-mode bundle staging is absent. Smoke exports expected files
  to its own temporary directory and cannot alter source-mode acquisition.
- Fixed executable acceptance PASS: scripts/smoke_release.py installed eight
  frozen packages with Git unavailable, compared all 960 resource files byte for
  byte, and confirmed all eight lock targets VERIFIED. Evidence is retained in
  build/ci-release-windows/fixed-resource-smoke.log. This is the same checker now
  invoked by release.yml; includes the formerly missing Three.js Python resource.

### Final review

- Spec axis PASS: all eight packages and distribution boundaries mapped; original
  validate job/checks retained; release calls shared checks before build/publish;
  platform/interpreter coverage expanded only for installer paths; frozen package
  and full-file release guards are covered by red-capable tests; model testing
  remains manual. Hosted execution is not inferred from local code or unit tests.
- Standards axis PASS: main-only control-plane changes; whole runtime resources
  preserved; no external service/model calls added; no credentials or global
  configuration edits; no user changes overwritten; temporary/owned paths checked
  before cleanup or artifact rename; no tests disabled or suppressions added.
- Runtime pipeline limits: only the Windows/Python 3.12 host was executed here.
  Ubuntu, macOS, Python 3.11 and hosted GitHub workflow results remain NOT_VERIFIED.
  Native agent discovery/behavior was not tested. Main merge protection is absent
  per the read-only API results; no protection or ruleset settings were modified.
- Read-only hosted-policy inspection: the GitHub connector lacks protection/rule
  reading tools, so the existing GitHub CLI was used. `gh api
  repos/andinoferdi/AI-RULES/branches/main/protection` returned HTTP 404 with explicit
  "Branch not protected"; `gh api repos/andinoferdi/AI-RULES/rules/branches/main`
  returned HTTP 200 and []. Thus main has neither classic protection nor effective
  rules at inspection time. Adding local checks cannot enforce merging by itself.
  No policy was changed; hosted policy configuration and push are outside this
  local implementation, and actual new check names need a first hosted run.

### Final acceptance

- `python -m unittest discover -s tests`: PASS, 334 tests, 5 existing conditional
  skips, 187.660 seconds. Current bytes include the new smoke script and tests.
- Existing package, Three.js, capability-schema and skripsi checks passed at the
  unchanged runtime refs; final frozen-bundle and standalone checks passed.
- `python scripts/smoke_release.py --executable
  build/ci-release-windows/ai-rules-windows-x64.exe`: PASS, eight packages,
  960 byte-identical installed files, all lock targets VERIFIED, Git unavailable.
- actionlint, coverage-guide local links, rebuilt artifact checksum and final
  `git diff --check`: PASS. Both Spec and Standards reviews have no unresolved
  local implementation findings.
- Owned changes: both workflow YAMLs, packaging/ai_rules.spec, build_release.py,
  new smoke_release.py, source-subpath and new smoke regressions, CI guide,
  README/eval guide links, and this checkpoint. Prior Council checkpoint preserved.
- No model calls, native agent tests, Git commit/push, hosted workflow dispatch,
  release publication or repository settings changes were performed.

## NEXT ACTION

Local implementation is complete. The user authorized publishing this verified
change to main on 2026-10-29; record the delivery identity in Git history and the
delivery response. After push, inspect the first hosted runs. Required-check
configuration needs separate authorization and the observed check names.
Native/model behavior remains targeted human testing; do not add automated
model evaluations to CI.
