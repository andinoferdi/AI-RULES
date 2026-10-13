# Search First integration evidence

Local implementation and verification completed on 2026-10-13. Publication is
pending: the remote `search-first` branch and updated main/workflow have not been
pushed. Normal remote setup must not be advertised as released until publication.

## Exact inputs

| Component | Revision |
| --- | --- |
| Main baseline | `201134d20bae0b04869ff09409b21e7bc2a9a4c2` |
| Search First distribution | `b5596b4d47f498adeef24b689f0d44a153cf4f0d` |
| Final Andino distribution | `59529af060a516ac197ff17481e3a8f7134c4ba8` |
| Focus (unchanged) | `9eb6081aa1ae26a4bb81a38eb49e4b1f9b9c3da3` |
| ECC source inspected | `b92f181b3b748d1abbc2afd94af6aa7d8c8fca29` |

Read the complete [upstream Search First](https://github.com/affaan-m/ECC/blob/b92f181b3b748d1abbc2afd94af6aa7d8c8fca29/.kiro/skills/search-first/SKILL.md).
The preserved MIT notice matches [ECC's license](https://github.com/affaan-m/ECC/blob/b92f181b3b748d1abbc2afd94af6aa7d8c8fca29/LICENSE)
exactly apart from outer whitespace: Copyright (c) 2026 Affaan Mustafa.
AI-RULES maintains an adaptation, not an original claim over that methodology.

Andino runtime content hash used in all final actor records:
`76c58ce05157f44a9f77e7b7e0f8ef4068acd5b076e9e0ec9f90546ae022191d`.

## Installation, discovery, activation and use are separate

| Layer | Observed result | Limit |
| --- | --- | --- |
| Catalog/schema | Search First first-party entry loads; independent requires; Andino requires Focus and Search First | Does not prove installation or use |
| Resolver/profiles | Standalone Search First excludes Andino/Focus; Andino and all profiles include it once; explicit dependency selections deduplicate | No new resolver was added |
| Installer | Actual committed packages install via latest local Git branch transport and pinned/embedded bundles; all five host adapters; global and project fixtures | Latest transport uses a disposable local repository until remote publication |
| Updates/reconciliation | Repeat setup preserves mtimes; newer branch revision updates; unrelated files preserved; edited skill blocks; alternate discovery root blocks duplicates | Existing reconciliation policy retained |
| Host registration | Skill files and relevant native invocation artifacts verified for Codex, Claude Code, OpenCode, Antigravity CLI and IDE | No claim of each host's UI/picker discovery |
| Native activation | Claude Code Skill calls succeeded for actual unchanged packages in a disposable session plugin | Restricted project auto-discovery did not work; wrapper namespace is evaluation-only |
| Actual use | Local inspection, package metadata and official-docs research informed recommendations; standalone and Andino cases observed | Read-only recommendation tasks, not application integration/security validation |
| Codex live use | NOT_VERIFIED: read-only actor's file read rejected by host policy | Restriction was not bypassed or relaxed |

The installer has no identity-specific implementation change: catalog/dependency,
profile and manifest additions reuse existing source acquisition, reconciliation,
host adapters and release packaging. Focus, Rescue and Skripsi distributions remain
unchanged. The original checkout's user-edited README was not touched.

## Deterministic checks

- `python -m unittest discover -s tests -v`: **147 tests passed**, zero failures or
  errors, Python 3.12.10 on Windows. [Complete output](unittest.log).
- `python scripts/validate_skills.py --andino-ref andino-workflow --search-first-ref search-first`:
  **5 skill packages and 5 eval schemas passed**, including metadata/layout/links.
- `python scripts/validate_andino_capabilities.py --runtime-ref andino-workflow --records docs/validation/search-first/claude`:
  **44 capability cases and 57 registry contracts passed**; all records match the
  final runtime hash.
- `python scripts/validate_skripsi_traceability.py`: **335 requirements/acceptance
  criteria, 32 capabilities, 110 initial eval owners and 75 task records passed**.
- `git diff --check`: passed in all three task worktrees.
- [Machine-readable verification summary](verification.json).

The new resolver tests failed before catalog integration. Standalone evaluator,
web opt-in, restricted Claude adapter and native invocation-audit tests also
failed before their implementation. Old test fixtures/counts were updated to
include the fifth capability and third Minimal dependency. No installer engine,
new CLI framework, paid search provider or production plugin was introduced.

## A-J behavioral review

Each case ran in a fresh restricted Claude Code 2.1.294 process with actual
`claude-haiku-5-5` exposed in events. No model override was requested. Expected,
forbidden and reviewer conclusions were hidden. The same implementation author
manually reviewed native tool calls/results and outputs; this is not an independent
review or a statistical reliability estimate. All ten final **scenario contracts**
passed; the verdict does not endorse every incidental implementation suggestion.

| Case | Observed evidence | Verdict |
| --- | --- | --- |
| [A — new feature](claude/search-first-feature.json) | Search First invoked; stack inspected; public package/docs research informed COMPOSE | PASS |
| [B — existing capability](claude/search-first-existing.json) | Existing csv.writer/test reused; no new dependency or unnecessary web research | PASS |
| [C — trivial edit](claude/search-first-trivial.json) | Returned Students; no Search First or research | PASS |
| [D — unfamiliar integration](claude/search-first-sdk.json) | Search First invoked; locked version read; official docs/changelog retrieved; execution and version limits retained | PASS |
| [E — failed approach](claude/search-first-alternatives.json) | Search First invoked; tagged transport source and docs consulted; supported HTTPTransport alternative | PASS |
| [F — unknown bug](claude/search-first-unknown-bug.json) | Systematic Debugging invoked before diagnostic reads; unknown cause retained; Search First inactive | PASS |
| [G — offline](claude/search-first-offline.json) | Search First invoked; local evidence used; external freshness and consultation explicitly unknown | PASS |
| [H — permission](claude/search-first-permission.json) | Search First invoked; dependency approval and unknown pricing identified; no mutation/credential access | PASS |
| [I — standalone](claude/search-first-standalone.json) | Only Search First installed in fixture; native load + local code/test reads -> ADOPT | PASS |
| [J — Andino integration](claude/search-first-andino.json) | One Andino entry selected Focus and Search First; meaningful local/public findings used; one lifecycle | PASS |

The record audit reports **10 PASS, no missing cases, one exact current hash** when
given the ten `--case` IDs from `evals/search-first.json`. The audit validates
record consistency, not truth or model grading. Full reproduction instructions
and catalog format are in [the evaluation guide](../../../evals/README.md).

Public research was enabled only for A/D/E/J. No external MCP servers, shell,
write tools, agents, purchases or external mutations were exposed in Claude runs.
The adapter uses the documented [restricted CLI mode and session plugin option](https://code.claude.com/docs/en/cli-reference)
to register unchanged skill resources as `ai-rules-eval:<id>`. This proves native
loading and use of those resources; it does not establish ordinary slash-command
discovery or native invocation on Codex/OpenCode/Antigravity. Executable release
builds, remote setup and Linux/macOS CI were not run.

## Failures retained and corrections

- [Codex attempt](live/search-first-andino.json): local reads blocked; no skill use
  claimed. The actor answered, but that is not successful activation.
- `claude-project-discovery/`: restricted native reads worked, but project skills
  returned Unknown skill. Official explicit session registration resolved the
  fixture limitation without changing runtime distribution or relaxing read-only
  tools. These initial records remain NOT_VERIFIED.
- `prior-9ab45df/`: 5 scenario passes and 5 failures. Documentation/alternative
  cases skipped the method, offline research was treated as unnecessary, one
  activation used Read instead of Skill, and debugging loaded late.
- `prior-6e9f05e/`: 7 passes and 3 failures. Required offline/native loading worked;
  documented alternatives still bypassed the method and debugging still loaded late.
- `prior-7efa00e/`: SDK and alternatives passed; the unknown-bug actor admitted
  it had not followed activation order. Final entry instruction preserves immediate
  debugging activation before diagnostic reads.

The final runtime clarifies required selection only when research is actually
needed, distinguishes method activation from documentation retrieval, retains
offline research and makes native invocation explicit. It does not activate
Search First merely because coding is mentioned. Historical passes were never
silently relabeled as final-runtime evidence.

## Publication boundary

Prepared release sequence 8 pins real local commits; no release tag or remote
publication is claimed. Main changes are reviewable on local
`codex/search-first-integration`; distribution commits are on `search-first` and
`andino-workflow`. Before publishing, recheck remote drift, commit the installer
changes, and publish the two runtime branches together with the main integration
so remote setup cannot reference an absent branch. Preserve the original dirty
README and avoid force pushes. Remote setup/CI verification follows publication.
