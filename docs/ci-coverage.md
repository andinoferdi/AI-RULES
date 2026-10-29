# CI coverage and manual acceptance

CI checks package integrity, installer regressions and release artifacts without
calling a model. A green run proves only the checks listed here. Skill selection,
instruction following and native host discovery need separate human observation.

## Checks and release gates

[`validate-skills.yml`](../.github/workflows/validate-skills.yml) runs on pull
requests and pushes to `main`, daily, by manual dispatch, and when called by the
release workflow. Its original `validate` job uses Python 3.12 on Ubuntu and keeps
the package, schema, regression and traceability checks together.

The full suite already discovers `tests/installer`; installer coverage was not
missing from the original Ubuntu job. The additional installer matrix runs that
subset on Ubuntu/Python 3.11, Windows/Python 3.12 and macOS/Python 3.12. This checks
the declared Python floor and exercises platform-specific paths, including the
Windows junction regression. It does not run the full suite on every Python/OS
combination.

[`release.yml`](../.github/workflows/release.yml) calls the same validation
workflow from its own commit. All shared checks must succeed before the platform
builds can run; all builds and their smoke tests must succeed before a version tag
can publish. Manual release dispatch on a branch builds artifacts without
publishing; a dispatch targeting a tag can publish after the checks succeed.
This uses GitHub's documented [reusable workflow](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
and [`needs` dependency](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idneeds)
mechanisms.

The release chain is:

```text
shared validation + installer matrix
                 |
                 v
Windows / macOS / Linux builds
  - validate frozen package contents
  - build executable
  - check --help
  - install all first-party bundles into a disposable Codex project
    with PATH empty, so missing bundles cannot fall back to Git
  - compare every installed resource byte with its frozen source
  - require verified installer lock targets
                 |
                 v
publish version-tag artifacts and checksums
```

## Coverage map

Current branch refs and frozen release commits have different purposes. Package
validation checks fetched branch refs; release staging checks the actual commits
and optional subpaths in the [release manifest](../src/ai_rules/release/data/release_manifest.json).
A valid frozen commit need not equal the latest branch head. Staging rejects empty
bundle sets, malformed package metadata, missing resources, broken relative links
and unsupported package contents using the existing package validator. Export also
rejects unsafe paths and non-regular Git entries.

| Component / source | Automated evidence | Outside that evidence |
| --- | --- | --- |
| `andino-workflow` | Package structure/links; capability registry and evaluation schemas; deterministic regression tests | Agent routing, actual procedure use and cross-host behavior |
| `ai-codebase-rescue` | Package structure/links and evaluation schemas | Quality of a real rescue investigation |
| `skripsi-skill` | Package structure/links, evaluation schemas and requirement-ownership audit | Research validity and substantive agent behavior |
| `focus` | Package structure/links, evaluation schemas and bundled-reference comparison with `WebBased` | Whether generated responses follow the communication contract |
| `search-first` | Package structure/links, evaluation schemas and deterministic contract regressions | Real research quality and tool use |
| `council` | Package structure/links, evaluation schemas and installer regressions | Independent advice, meaningful review and decision quality |
| `natural-writing` | Package structure/links, evaluation schemas and deterministic package regressions | Naturalness, audience fit and preservation of meaning in generated prose |
| `threejs-skills` | One package and its internal methods; inventory, resources, binary signatures and scenario schemas | Live routing, rendering, visual quality and host execution |
| `WebBased` | The communication sources used by the Focus drift check | General validation of every web/chat template |
| Installer/CLI on `main` | Root unittest discovery; installer subset on the additional OS/Python combinations | Native Codex/Claude/OpenCode/Antigravity discovery and actual invocation |
| Frozen distribution | `build_release.py --stage-only` validates all manifest bundles; every executable build validates its actual staged inputs again | Semantic quality of the skill prose |
| Executable releases | Three OS builds, help smoke, bundled installation without Git, every resource compared with its frozen source, verified lock targets and checksums | Native host behavior, every architecture and every supported Python version |
| Optional external skills/MCP services | Relevant local contract and fixture checks only | Installation, connectivity or live behavior of external services |

Test discovery includes successful and failing fixtures; a test name or scenario
schema is not itself a behavioral result. Historical live records remain tied to
the revision, model and host they actually exercised.

## Run the model-free checks locally

From `main`, with the package installed and the runtime refs fetched:

```sh
python scripts/validate_skills.py --webbased-ref origin/WebBased --threejs-ref origin/threejs-skills
python scripts/validate_threejs_family.py --runtime-ref origin/threejs-skills
python scripts/validate_andino_capabilities.py --runtime-ref origin/andino-workflow
python -m unittest discover -s tests
python scripts/validate_skripsi_traceability.py
python scripts/build_release.py --stage-only --output build/frozen-check
```

Use a new output directory for each staging attempt: an existing `bundles`
directory is preserved and rejected. The stage-only command writes bundle contents
and `bundle-sources.json`; it does not build or publish an executable. Run source
tests before a full executable build, whose temporary embedded bundles can change
source-mode acquisition paths while the build is in progress.

After building an executable, [`smoke_release.py`](../scripts/smoke_release.py)
exports its expected frozen sources, installs the executable's `everything` profile
with Git unavailable, and compares all expected files byte for byte. This includes
Python scripts, shaders and binary resources, beyond the root `SKILL.md`. The
packaging spec explicitly includes raw Python resources from the release package;
PyInstaller's [data collector excludes them by default](https://pyinstaller.org/en/stable/hooks.html#PyInstaller.utils.hooks.collect_data_files).

## Human behavioral testing

Do not run live-model evaluations in CI. Prioritize human testing when activation
rules, routing, permissions or a procedure changes materially, or when a behavioral
regression is reported. A prose-only change that preserves those contracts does not
automatically require retesting every skill.

1. Select a relevant positive case, a negative activation case and, when applicable,
   a case that previously failed from the [evaluation guide](../evals/README.md).
2. Use the changed runtime revision and a fresh host session. Give the actor only
   the raw prompt and required fixture; keep expected/forbidden outcomes with the
   human reviewer. Use disposable project data for scenarios that change files.
3. Observe selection/loading, tool actions, user questions and the resulting work.
   Judge the required behavior, rather than the agent's claim that it used a skill.
4. Record the runtime revision, host/version, model if exposed, scenario, observed
   result and verdict. Keep unavailable or unexecuted cases `NOT_VERIFIED`.

A compact record can use:

```text
Runtime revision:
Host/version:
Model: (or UNKNOWN)
Scenario/raw prompt:
Reviewer expectation: (kept out of the actor's input)
Observed actions/result:
Verdict: PASS / FAIL / NOT_VERIFIED
Evidence or reproduction steps:
```

## Hosted policy and audit limits

Workflow dependencies enforce the release sequence within a run. They do not
configure repository branch protection or rulesets. To make PR merging depend on
all new coverage, the hosted policy must require `validate` and all three
`Installer (...)` checks. Read-only inspection on 2026-10-29 returned `Branch not
protected` for classic `main` protection and an empty effective rules list. No
hosted settings were changed: the configured checks do not currently require a
successful run before merging to `main`. Inspect the actual check names after the
first hosted run before configuring rules. Runtime branch pushes are observed by the daily run and the
next main validation; they do not directly trigger this workflow on their own.

An audit is bounded when every distributed component has an identified source,
check and evidence limit. Investigate further only for a concrete failing case,
an unprotected user-facing failure or a material unknown on a release path. Choose
the next investigation by impact and evidence. More jobs or a longer green run
are not acceptance criteria.
