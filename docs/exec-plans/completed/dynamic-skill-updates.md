# Dynamic skill updates

Status: DONE
Plan Depth: STANDARD
Current Phase: Verification complete
Last Updated: 2026-10-02

## Objective

Make setup/update resolve current source branch revisions rather than equating an
existing SKILL.md or bundled manifest with latest. Preserve local edits and record
the exact verified installed revision. Apply to all registered first-party skills
and their configured branches, not just Andino. Do not turn reference projects into
new managed third-party integrations or install arbitrary non-skill branches.

## Baseline and root-cause evidence

Baseline main: 8b9882ae897eac43e98ac3b017c7694c54af7de8; initially clean.
Installed CLI uses site-packages with old manifest; local skills match the old
engineering workflow. cli._resolve_from_args uses StaticCapabilityAdapter's bundled
manifest; _actual_state tests only SKILL.md existence; UNKNOWN_ORIGIN healthy becomes
NO_OP/CURRENT. _executor_for_plan exports the bundled commit from the current working
directory, so it neither refreshes remote branches nor works independently of a repo.

## Decisions

- setup/add/update default to fetching configured branch heads once per invocation,
  resolving exact SHAs before mutation. Explicit bundled mode supports offline/frozen
  distribution and existing deterministic tests; no silent stale fallback.
- Reconcile full content and provenance. Recognizable clean older official copies
  may update with backup; modified/unrecognized targets require explicit repair.
- Preserve symlink/junction targets, shared roots and Git-managed checkouts.
- Failed fetch/validation must not report current. Record hashes/source and recheck
  state at execution to avoid replacing edits made after planning.
- Keep installed CLI code refresh separate from skill content refresh. Refresh this
  local CLI after validation so the reported executable uses the fix.

## Acceptance and verification

- Reproduce old copy and newer branch in an isolated Git fixture; setup updates it.
- A second setup is NO_OP only after latest content verification.
- A later branch commit updates without changing packaged manifest or CLI code.
- Multiple skills/branches/hosts, extra/deleted files, local modifications,
  interrupted fetch, non-repo CWD and shared directory targets have explicit checks.
- Existing installer unit tests remain offline/reproducible; run full suite and
  package checks after implementation. Verify the actual local CLI and target files.

## Reference findings

Reviewed user-supplied primary project documentation. Superpowers describes
host-specific update routes; Anti-Slop documents an explicit update command;
Ponytail and other skill packages use native plugin/skill installers. These are
reference patterns, not a universal shared CLI implementation. Sources:
https://github.com/obra/superpowers
https://github.com/miqdadbadjuber/anti-slop
https://github.com/DietrichGebert/ponytail
https://github.com/addyosmani/agent-skills
https://github.com/vercel-labs/skills

## Implemented

`release/latest.py` prepares each selected repository once per invocation, fetches
its configured branches and exports validated exact commits to temporary bundles.
It compares complete source/installed file maps rather than SKILL.md presence.
Clean copies matching up to 256 source revisions may update with backups. Clean Git
clones retain origin, branch and metadata and fast-forward only; modified,
unrecognized, diverged or differently configured checkouts remain protected.
Execution rechecks the destination and content to catch changes after preview and
respects shared roots and junctions. Missing/deleted upstream files do not accumulate.

setup/add/update/doctor default to latest; repair remains bundled/explicit. Failed
source access never falls back silently. Preview downloads are temporary and do not
write installation state. Locks/managed records identify the exact revision and
verified content. The existing deterministic tests explicitly select bundled mode.
Interactive current results say Up to date only after source and content checks.

## Verification evidence

- New fixture tests initially failed against the previous CLI (no latest source
  support). The first expanded suite exposed a newline mismatch in a test assertion;
  the assertion was corrected without weakening the preservation check.
- `python -m unittest discover -s tests`: 108 tests PASS in 28.073 seconds on Windows
  / Python 3.12.10, with source imports and bytecode disabled. Includes 22 new local
  Git fixture cases; no public network dependency in those tests.
- `python scripts/validate_skills.py`: all 3 packages and eval schemas PASS.
- `git diff --check`: PASS.
- `python -m pip install --editable . --no-deps --no-build-isolation`: success.
  The installed ai-rules executable now imports this source checkout rather than
  the stale site-packages copy.
- Installed CLI setup with Everything and five hosts: Andino updated to 0f41b68,
  other selected skills unchanged. Four distinct Andino clones updated; Antigravity
  CLI shares the Codex target. Backups were retained in the selected state directory.
- A second actual setup fetched sources again and produced 15 VERIFIED NO_OP results.
  The lock contained 15 verified targets. Independent file comparison of every
  Andino package file across five discovery paths matched origin/andino-workflow;
  each Git checkout reported clean.

## Boundaries and decisions

No new third-party integrations, auto-discovery of arbitrary branches, source-code
self-updater, background service or additional dependency was added. Branch source
metadata comes from the registered capability, so the mechanism is not hardcoded
to Andino. A future CLI-code/catalog change still needs a CLI refresh; skill content
commits on registered branches do not. Editable local installation assumes this
main source checkout remains available.

Exact replay of branch-tracked locked snapshots is not implemented; it is marked
unsupported and rejected rather than silently substituting another revision.
Bundled mode preserves the existing offline/frozen workflow and does not claim
latest freshness. Host session reload and model behavior are outside installer
verification; the separate Andino live behavioral evaluation remains NOT VERIFIED.
Cross-platform execution and a rebuilt standalone binary were not tested here.

## NEXT ACTION

None — dynamic updater implemented and verified. Future work should start from new
failure evidence or an explicit extension request, not reopen accepted runtime rules.
