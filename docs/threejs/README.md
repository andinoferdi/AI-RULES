# Three.js family integration

Status: LOCAL IMPLEMENTATION COMPLETE; publication and cross-host behavior pending.
This is quality-plane evidence, not a runtime router or a license declaration.

## Branches and layout

- `threejs-skills`: `a41a0a10eccc02ab35d2d89fae3165f269624b38` (orphan runtime branch).
- `andino-workflow`: `06aca9e0bb6de169a46261bd37cb96bfde9b0210` (based on fetched d5fbcec).
- `main`: installer/catalog/tests/quality work; final local commit is reported in the delivery.

The runtime has 776 regular files: all 714 original resource paths, 45 new README
files, copied support for standalone use, and the root/entrypoint projections.
The 45 source skills are preserved individually. Root SKILL.md/README.md are a
reading index; identical `entrypoint/` files form the standalone installed index.
Each member lives at `skills/<name>/SKILL.md` with references, scripts, examples,
assets, agent metadata and license notices preserved. The family package installs
from `entrypoint`, never with a nested discoverable collection. The profile installs
49 directories: 45 members + index + Andino + Focus + Search First.

`<host-root>/<name>/SKILL.md` is the installed shape. Codex uses `.agents/skills`
for project and global scope. Other host mappings use existing catalog adapters;
live execution on those hosts is NOT_VERIFIED. No global skill configuration was
changed. Both managed worktrees are retained for review; the original untracked
`threejs-skills/` folder and pre-existing ignored build artifacts remain intact.

## Complete inventory

[Machine-readable inventory](inventory.json) lists every original/support file,
exact original SHA256, normalized runtime text SHA256, binary byte hashes, sizes,
sibling suggestions and supplied license notices. It reads every SKILL.md and
text resource in full; structural checks do not claim expert validation of every
Three.js example or external API. Hash normalization is CRLF -> LF for text only.

| Skill | Role |
| --- | --- |
| `nixie-fx-authoring` | specialist |
| `nixie-fx-runtime` | specialist |
| `threejs-3d-generator` | specialist |
| `threejs-aaa-graphics-builder` | specialist |
| `threejs-animation` | specialist |
| `threejs-atmosphere-aerial-perspective` | specialist |
| `threejs-audio-generator` | specialist |
| `threejs-bloom` | specialist |
| `threejs-camera-direction` | specialist |
| `threejs-debug-profiler` | specialist |
| `threejs-exposure-color-grading` | specialist |
| `threejs-fundamentals` | specialist |
| `threejs-game-director` | game-production-specialist |
| `threejs-game-ui-designer` | specialist |
| `threejs-gameplay-systems` | specialist |
| `threejs-geometry` | specialist |
| `threejs-image-generator` | specialist |
| `threejs-image-pipeline` | specialist |
| `threejs-interaction` | specialist |
| `threejs-lighting` | specialist |
| `threejs-loaders` | specialist |
| `threejs-materials` | specialist |
| `threejs-parallax-occlusion-mapping` | specialist |
| `threejs-postprocessing` | specialist |
| `threejs-precipitation-surfaces` | specialist |
| `threejs-procedural-animation` | specialist |
| `threejs-procedural-architecture` | specialist |
| `threejs-procedural-fields` | specialist |
| `threejs-procedural-geometry` | specialist |
| `threejs-procedural-materials` | specialist |
| `threejs-procedural-planets` | specialist |
| `threejs-procedural-vegetation` | specialist |
| `threejs-procedural-vfx` | specialist |
| `threejs-qa-release` | specialist |
| `threejs-raymarched-space-effects` | specialist |
| `threejs-screen-space-ambient-occlusion` | specialist |
| `threejs-shaders` | specialist |
| `threejs-shadow-systems` | specialist |
| `threejs-skill-router` | domain-advisor |
| `threejs-spectral-ocean` | specialist |
| `threejs-temporal-surfaces` | specialist |
| `threejs-textures` | specialist |
| `threejs-visual-validation` | specialist |
| `threejs-volumetric-clouds` | specialist |
| `threejs-water-optics` | specialist |

## Source audit and justified changes

- Names are unique and match their source folders. All 45 have portable metadata.
  Quoted descriptions were normalized to the existing validator's plain-string
  subset; colon separators became ` - `. Technical recipes were retained.
- Each skill receives an explicit domain/exclusion and coexistence boundary.
  The domain advisor remains technical; Game Director no longer mandates default
  delegation, loading all five production skills, or a competing game-progress
  checkpoint. Provider generation journals and renderer lifecycles remain intact.
- Five Markdown links crossed sibling package boundaries. Referenced example
  folders (including their local imports) were copied into the consuming packages
  and linked locally. The credential probe is copied into its consumers so an
  individual install does not need Game Director solely for that helper.
- One example Markdown artifact link in a prose code span was rewritten as prose
  to avoid falsely claiming it is a bundled file. No broken link exception added.
- Nineteen original files carried trailing whitespace on blank/comment lines or
  terminal blank lines. Only those whitespace defects were normalized in runtime
  copies; code operations and license wording were not changed.
- The bounded full-text scan detected no private-key/AWS/key-pattern signatures.
  That is not proof that no sensitive content could exist; scripts were not run
  against credentials, paid providers or unrelated project data.

Supplied notices include MIT, CC0 and GPL-3.0-only materials. The procedural-materials
package includes GPL texts and notices for deformable-sand and simulated-tearable-denim;
these notices are preserved. The deformable-sand notice mentions an optional
`coconut_tree.glb` that is absent from the supplied source (not a missing installed
file; the inventory preserves exactly what was supplied). Many other files have
no explicit redistribution declaration, including the collection itself. Upstream
provenance and blanket distribution rights remain UNKNOWN. No license was invented.
Confirm rights before publication; do not infer them from a neighboring MIT notice.

## Installer and release contracts

Capabilities share repository/branch but carry a strict `source.subpath` and stable
ID/destination. Latest fetches each repository once with unique branch refspecs,
then caches subtree hashes. No-subpath packages retain branch-root behavior.
Archive, latest trees, catalog input and build staging reject traversal, absolute
paths, Windows drive/separator/reserved names, Git internals, nonregular entries
and links. Subpath Git checkouts are preserved for explicit reconciliation instead
of merging a full repository into a flattened skill directory.

Existing staging, backup and rollback install the whole package. The resolver now
computes transitive dependency closure in dependency-first order and reports cycles.
A regression establishes that `ls-tree -rz` was already recursive; it was not changed
for a nonexistent recursion defect. Windows `git archive` applied autocrlf to code
resources and broke source hashes; per-command autocrlf/eol overrides now preserve
canonical Git blobs without changing user Git configuration.

Bundled acquisition and release staging use the same subpath exporter. Source
records retain repository/branch/commit/subpath (repository comes from catalog for
bundled releases). Fingerprints use path/blob lists so a harmless filename such as
`probe_asset_credentials.sh` cannot be mistaken for a persisted credential field;
older dict fingerprint records remain readable. Legacy bundled records without
fingerprints preserve existing content on upgrade/repair/removal until explicit
review; absent targets remain safely installable. User edits/additions block normal
updates/removal. Existing repair ownership/replace-existing gates remain in force.
Doctor, safe repair, remove, backups, no-op, locks and snapshots use existing CLI
mechanisms. Repair is explicitly bundled; latest updates use setup/update.

Minimal and Engineering are unchanged. A newly selected Everything includes all
first-party capabilities; saved explicit selections are not silently migrated.
The Three.js profile does not imply activation, paid APIs or npm dependency installs.
Standalone specialists require no Andino installation.

The scoped validator permits enumerated text/code/shader/asset formats only for
registered Three.js packages. It checks metadata, regular files, relative image
and document links, UTF-8 text, nonempty raw binaries and format signatures (GLB
length and gzip decoding included). It does not parse every shader, compile every
example or claim full image-decoder validation. Existing family allowlists stay strict.

Local release metadata pins unpublished commits explicitly and records publication
status/order. Existing unrelated runtime pins were retained. Build staging refuses
to erase an existing bundle directory, records branch/commit/subpath in source
evidence and preserves existing build artifacts. Local staging exported all 52
first-party bundles; a Windows standalone executable was built with PyInstaller 6.22.3 and its embedded bundled profile is tested separately (see evidence).

## Andino selection and invocation

Andino's routing table links one focused Three.js specialist reference. Known narrow
needs go directly to actual installed IDs: shaders, lighting, animation, materials,
geometry and interaction use their namesake skills. Complex work adds only distinct
needed specialists. The family index is not a dispatcher; the existing technical
advisor and Game Director do not bootstrap each other or own a second plan.

The host contract remains authoritative for DISCOVERED, AVAILABLE, INVOKABLE, ACTIVE,
USED, UNAVAILABLE and NOT_NEEDED. Missing/denied/explicit-only methods are not bypassed
by reading source copies. Unknown causes start with debugging; Focus controls
communication, Search First relevant solution/version research. Changed needs and
resume refresh relevant availability while preserving Andino's existing checkpoint.
Rendering/performance/interaction claims need actual browser evidence; UI acceptance
retains 360/768/1440 captures. No Three.js rendering or cross-host parity claim is
made by the structural tests.

## Verification record

See [evidence](evidence.json) for the final commands/results and live-host boundaries.
The automated installer tests use isolated local Git fixtures; unpublished branches
are never assumed available on GitHub. A separate smoke installs actual committed
packages from a local bare source fixture, with temporary project/global targets.
Review-only [routing scenarios](../../evals/threejs-routing.json) cover shader,
multiple specialists, ordinary frontend, unknown root cause, absent/denied skills,
scope change, resume, director boundaries and browser evidence. Schema validation
is structural; it does not establish model compliance with those ten scenarios.

Observed Codex CLI 0.154.0 evidence: `skills/list` discovered all 46 family packages,
all enabled with zero family errors. A fresh actor loaded `threejs-shaders` and
applied it to a smooth one-second pulse code review. A separate fresh HTML label
correction loaded no Three.js/NixieFX specialist. Both were read-only static reviews;
no rendering, browser or full-scenario compliance claim follows. The first configured
model alias failed before activation; the successful test used the host catalog's
default model only for that process. [Observed record](host-smoke.json).

The Windows executable installed all 49 profile targets in isolated project and
fake-home global scopes with Git absent from PATH, then NO_OP on repeat. It is a
local development build (base main revision plus uncommitted task code, explicitly
recorded as dirty), not a published release artifact. Raw logs and binary stay under
ignored build directories; compact evidence is committed here.

## Tested commands and publication order

Locally executed with a temporary in-memory catalog pointing to a bare fixture of
actual source commits (this did not edit the shipped repository URLs):

```sh
ai-rules setup --host codex --profile threejs --scope project --project-root PATH --source latest --non-interactive --yes
ai-rules setup --host codex --profile threejs --scope project --project-root PATH --source bundled --non-interactive --yes
ai-rules setup --host codex --capability threejs-shaders --scope project --project-root PATH --source latest --non-interactive --yes
```

Unit/integration tests also cover global scope with a temporary fake home, individual
and multiple selections, update, no-op, user modifications, unmanaged conflicts,
backup/rollback, doctor/repair/remove, source safety and existing families. Bundled
source-mode commands require this checkout's Git objects; released binaries must
embed the staged bundles. Project scope requires --project-root, even from the project.

Local validation:

```sh
python -m unittest discover -s tests
python scripts/validate_skills.py --andino-ref andino-workflow --threejs-ref threejs-skills --webbased-ref origin/WebBased
python scripts/validate_threejs_family.py --runtime-ref threejs-skills --original threejs-skills
python scripts/validate_andino_capabilities.py --runtime-ref andino-workflow
python scripts/build_release.py --stage-only --output NEW_EMPTY_OUTPUT
```

Use this workspace package (`PYTHONPATH=src` or an isolated editable install), not
an older ai-rules installation elsewhere on the machine. No global Python package
was replaced during this work.

NEXT ACTION: review source rights/provenance and authorize publication. Then publish
runtime threejs-skills, publish the dependent andino-workflow commit, verify both
remote SHAs, clear LOCAL_ONLY manifest markers/update remote refs, publish main and
build/tag the installer release. CI now fetches the family branch, so runtimes must
precede main. Re-run remote latest and executable bundled installations only after
publication. No push, merge, PR, tag or external publication occurred here.
