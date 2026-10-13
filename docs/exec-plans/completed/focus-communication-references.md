# Focus communication references

Status: DONE
Depth: STANDARD
Current Phase: Verification

## Executive Snapshot

Implement portable communication references in the Focus runtime; keep quality
checks on main. Worktrees: `focus-references-runtime` and
`focus-references-validation`, both under `C:/Users/Lenovo/.codex/worktrees/`.
Do not touch the concurrent Search First task or original checkout README edits.
No commits, publication, manifest pin updates or global skill updates authorized.

## Objective

Bundle complete A. PRIORITAS and both language references; specify first activation,
reuse, priority and honest restricted-host fallback without changing lifecycle.

## Acceptance Criteria

- Portable package and links pass; complete source copies match WebBased.
- Installer fixtures carry references on all configured hosts and remain idempotent.
- Existing dependency, override, license and formatting contracts remain intact.
- Evaluation scenarios cover languages and negative cases; live inference is
  explicitly NOT VERIFIED unless actually executed.
- Release steps identify the real commit/pin dependency without inventing a pin.

## Execution Board

| Phase | Status | Result / Evidence |
| --- | --- | --- |
| Inspection | DONE | main 201134d, focus 9eb6081, WebBased 2d488a4 match remote tips. A sections equivalent by extraction comparison. Installer copies whole package; release archives pinned commits. |
| Implementation | DONE | Three complete bundled references, explicit loading/priority/fallback, README; main validator, tests, 19 eval fixtures, family contract and CI drift check. |
| Verification | DONE | 141 tests passed against actual updated runtime. Package/drift, capability schemas, traceability and diff checks passed. Live model behavior NOT VERIFIED. |

## Decisions

- Canonical A is the project entrypoint chat-rules.md, whose A text is equivalent
  to README's fenced A. Copy all of A; preserve language files verbatim.
- Required reads are behavioral instructions, not enforced runtime hooks.
- Source comparison is maintainer-time only; runtime uses no network or other branch.
- Andino needs no compatibility change; existing permitted activation loads Focus.

## Evidence

Read installed Andino routing/invocation/plan and Focus instructions; inspected
family standard, validator, evals, installer tests, manifest and release builder.
Read Agent Skills specification and upstream provenance. Referenced chat inspected
read-only; its Search First work is isolated in other worktrees.

## NEXT ACTION

None — implementation complete. Git delivery was subsequently authorized as
recorded below; release artifact publication remains a separate action.

## Validation results (2026-10-13)

- `python -m unittest discover -s tests` through an in-process runner with
  `sys.path` set to this worktree's src and FOCUS_RUNTIME pointing to the runtime
  worktree: 141 tests, 67.127s, OK. Earlier baseline run: 140 tests passed; a shell
  quoting issue prevented its intended environment assignment, so it was not used
  as proof of the updated package. Corrected actual-runtime Focus run: 6 tests OK.
- Validator: `--andino-ref andino-workflow --rescue-ref origin/ai-codebase-rescue
  --skripsi-ref origin/skripsi-skill --focus-dir
  C:/Users/Lenovo/.codex/worktrees/focus-references-runtime/AI-RULES
  --webbased-ref WebBased`: 4 packages, metadata, links, paths, 4 eval schemas and
  exact source fidelity PASS. Both language copies unchanged; A sources equivalent.
- New validator tests observed rejecting drift, missing references, conflicting A,
  missing sections and an unterminated fence before fixes; 32 validator tests OK.
- Installer exercises actual updated package through disposable Git fixtures and
  project roots on Codex, Claude Code, OpenCode, Antigravity CLI and IDE. Verifies
  all references, invocation artifacts, NO_OP reinstall, standalone update and
  preservation of an unrelated user skill. This proves file/installer behavior,
  not live host discovery, implicit activation, reference reads or language quality.
- Capability eval schemas: 34 PASS. Skripsi traceability: 335 requirements/AC,
  32 capabilities, 110 initial eval owners, 75 task records PASS.
- `git diff --check` passed in both worktrees. MIT notice equals focus Git content
  after normalizing checkout CRLF; it has no edits. Original checkout still has
  only its preexisting README modification. No concurrent chat was interrupted.
- Live inference, first-load/reuse/language-switch behavior and cross-host model
  compliance: NOT VERIFIED. 19 Focus scenarios are review-only cases, not results.

## Release dependencies

1. Review and authorize committing/publishing the runtime to the Focus branch;
   its current base is 9eb6081aa1ae26a4bb81a38eb49e4b1f9b9c3da3. New SHA is
   unavailable until that authorized commit exists. Latest installs then receive
   the whole package through the unchanged installer.
2. Enable/publish this separate main quality change only after matching Focus
   runtime is available: CI checks origin/focus against fetched origin/WebBased.
   Current published Focus lacks the new references and would fail that new check.
   Reconcile shared main files with concurrent Search First changes when authorized;
   do not replace its changes with this worktree's older main base.
3. Update only Focus's real commit and appropriate release sequence/verified date
   in src/ai_rules/release/data/release_manifest.json after verification. Preserve
   concurrently maintained other capability pins. Bundled installs currently use
   the old Focus pin, release sequence 2; the overall stable sequence was 7 at the
   implementation baseline and is 8 after integrating latest main/Search First.
4. Run scripts/build_release.py in the authorized release process. It archives
   the pinned commit's entire tree into release/data/bundles/focus for packaging;
   the existing recursive package-data pattern includes references. Recheck the
   rebuilt bundled installation and publish assets through the existing flow.

At the local implementation checkpoint, no real repository commit, push, merge,
publication, pin update, release artifact build or global skill modification had
been performed. Test fixture commits occurred
only in disposable upstream repositories used by the existing installer tests.

## Authorized Git delivery (2026-10-13)

The user subsequently authorized commit/push to focus and main, including the
existing immutable language copies, branch selection and safe integration of
latest remote work. Immutable contents remain untouched. Runtime focus was pulled
with `git pull --ff-only origin focus` and committed as `75c11d1`
(`feat: bundle portable Focus communication references`). WebBased was fetched;
source drift/package validation passed against its unchanged current tip.
Main delivery uses codex/focus-communication-validation, preserving Search First
changes through an authorized pull/merge instead of overwriting remote main.
The original checkout's unrelated README remains excluded. No release, tag,
global skill update or release pin change is authorized by this Git cleanup task.

Runtime push was verified at remote focus commit
`75c11d1209f2b735fd837cfb3c34465d77b86581`, with a clean synchronized worktree.
Main was pulled from current remote commit
`6c855ea121e852f714d7b07494dda68242fa5f3a`; conflicts in CI's branch fetch list and
the validator argument list were resolved by retaining both Search First and
Focus/WebBased checks. Diff review against that remote parent contains only the
seven intended Focus quality files. Commit `8a57432` preserves the original
Focus quality change before integration.

Integrated validation: 156 tests passed in 111.215s using the actual Focus tree;
the final priority-reference update fixture passed all 6 Focus tests in 13.649s.
Published-ref validation passed for 5 skill packages/5 eval schemas, exact
WebBased source drift, 44 capability eval schemas/57 runtime contracts, and
335 traceability requirements/acceptance criteria. Staged whitespace and targeted
secret-pattern checks passed. The update fixture now changes priority-a.md rather
than a language template. Both immutable language blobs equal WebBased exactly.

Cleanup scope is only untracked ignored Python bytecode caches generated by local
tests; tracked sources, reference files, completed provenance/evidence plans and
the original checkout README are retained. Gitignore needs no change. Runtime
release pins remain unchanged; latest installs receive the published Focus branch,
while bundled releases require the separately authorized pin/build process above.
Live cross-host language quality remains NOT VERIFIED.
