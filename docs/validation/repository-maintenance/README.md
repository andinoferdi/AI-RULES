# Eight-branch maintenance verification

Date: 2026-10-18. Scope: `main` and seven first-party runtime branches. `WebBased`
was read-only. This report covers maintenance and package delivery; it adds no
live-host or rendering claims.

## Branch results

| Branch | Baseline | Published runtime | Change |
| --- | --- | --- | --- |
| main | `6b28753` | Containing Git commit | Public README, frozen pins and evidence reconciliation |
| ai-codebase-rescue | `ff61f48` | `5b0b47c` | Installation prerequisites, verification, package references |
| andino-workflow | `efd9c50` | `8866a23` | Benefits before internal details, method/provenance navigation, installer limits |
| council | `82984fa` | `82984fa` | NO CHANGE: existing README and package meet the scoped requirements |
| focus | `3effa77` | `dbeff40` | Scope, actual loading limits, reference validation and license link |
| search-first | `8383f8a` | `b55364b` | Research evidence limits, verification and playbook/license links |
| skripsi-skill | `1161da8` | `fceec66` | Research integrity, templates, verification and provenance boundary |
| threejs-skills | `f47d7c0` | `7ff3f57` | CLI bootstrap, standalone/profile alternatives, invocation and smoke checks |

Full SHAs, package counts, unchanged-resource tree identities and remote checks are
in [verification.json](verification.json). Runtime pushes were individual,
non-force HEAD-to-existing-branch pushes. Detached worktrees avoid creating local
branches or switching the user's dirty main checkout.

## Preservation and selective cleanup

No file was deleted. All seven packages retain exactly one native `SKILL.md`.
Andino retains 127 files and 57 internal guides; Three.js retains 775 files,
45 internal guides and all 714 inventoried original resources. Every non-README
runtime Git blob and mode matches its branch baseline.

Failed validation logs, actor fixtures, historical plans, evals, tests, scripts,
Three.js examples/shaders/binaries, manifests, provenance and legal notices remain.
Their runtime, regression, audit or release role provides a reason to preserve
them. File names alone supplied no evidence for removal. The user's untracked
execution prompt remains outside the commits.

`chat-rules.md`, `human-language-english.md` and `human-language-indonesia.md` have
no task diff. WebBased remains at `9a5d0e1b31257c4fcb1554558266ec7afc2a6160`.
Focus's bundled Priority A and both language references match its read-only source;
the two WebBased Priority A presentations also agree.

## Documentation and frozen release

The main README now leads with purpose and quick start, followed by a seven-skill
catalog, supported setup choices and practical combinations. It retains
`Distribution branches`, `Setup`, `Skill combinations by task`, and
`External resources: manual installation`. Bundled Andino methods and optional
external services are distinguished. The obsolete unpublished-candidate claim is
replaced with the published runtime state. No branding, decorative badges,
endorsement or unmeasured compatibility claim was copied from the reference READMEs.

The frozen manifest advances to sequence 14 because six complete distributed
packages changed. Each new pin matches an actually published runtime commit.
Council's complete manifest entry stays unchanged. The previous Focus pin predates
its already-published communication references; reconciliation includes those
existing changes, while this task changes only Focus's README.

Latest setup follows configured branches; bundled setup uses the frozen manifest.
A tagged standalone installer release remains separate and was not created.

## Verification

The following checks passed against the changed packages or published refs:

- Package paths, metadata, relative links, one native entrypoint per package and
  Focus/WebBased equivalence.
- Three.js inventory and binary/resource checks: 45 methods, 714 original resources,
  10 scenario schemas.
- Andino: 54 capability evaluation schemas, 58 contracts and source/ownership coverage.
- Skripsi traceability: 335 requirements/acceptance criteria, 32 capabilities,
  110 initial evaluation owners and 75 task records.
- Markdownlint on all eight READMEs; default rules except MD013 for long commands
  and tables. Fifty local/first-party README links resolve through disk or Git objects.
- Seventeen external README destinations returned HTTP 200. Two npm pages returned
  HTTP 403, so their current availability remains NOT_VERIFIED; no denial was bypassed.
- All 57 bundled Andino procedure examples executed successfully on canonical Git
  exports. Refreshed reports retain source/checker/guide hashes and observed results.

The final current-src checkout suite passed: 223 tests, zero failures and one
unchanged opt-in skip. [installation.json](installation.json) records 16 passing
disposable scenarios: frozen-manifest fresh/repeat on five adapters, real remote
fresh/repeat and baseline upgrade/backup/repeat on Codex, plus two managed-edit
conflicts preserving local changes. Only the disposable home path was redirected;
source, catalog and network acquisition were real. No global installation changed.

Native discovery, model behavior, service use,
rendering and cross-host behavioral parity remain NOT_VERIFIED by these checks.

## Evidence corrections and reproduction

The first byte-sensitive procedure check exposed stale report identities and
Windows CRLF conversion. Comparing LF Git exports isolated those causes. The
three original reports remain in [pre-maintenance](../andino-unified/pre-maintenance/);
the current `*-operational.json` reports were re-executed using canonical main and
runtime inputs. No runtime instruction or checker changed.

Plain Python also initially imported an older installed `ai_rules`, while fixture
tests read the checkout manifest. Six post-pin failures belonged to that mixed
environment. The corrected run explicitly puts this checkout's `src` first on
Python's import path, without changing the global installation.

To test the checkout without installing it, set `PYTHONPATH` to its absolute `src`
directory for that process, then run from `main`:

```sh
python -m unittest discover -s tests
python scripts/validate_skills.py --webbased-ref origin/WebBased --threejs-ref origin/threejs-skills
python scripts/validate_threejs_family.py --runtime-ref origin/threejs-skills
python scripts/validate_andino_capabilities.py --runtime-ref origin/andino-workflow
python scripts/validate_skripsi_traceability.py
```

For exact procedure hashes, export `main` and the pinned Andino commit through
`git archive` into separate disposable directories. Run all three
`check_andino_*_methods.py` scripts from that main export against the runtime export,
then run `validate_andino_unified.py --runtime <runtime-export>` from the same
main export. CRLF working-copy bytes are a different input identity.

## Anti-Slop delivery gate

- Copy PASS: concrete purpose, installation commands and task examples; claims and
  counts checked against repository contracts and executed validators.
- Honesty PASS: package delivery and structural evidence are distinguished from
  live discovery, model behavior and rendering; no invented metrics or endorsement.
- Preservation PASS: only runtime READMEs changed; all instructions, notices and
  supporting resource blobs/modes are unchanged.
- UI/layout gates: NOT_APPLICABLE to this documentation maintenance.
