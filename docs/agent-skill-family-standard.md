# AI-RULES Agent Skill family standard

This maintainer contract is not a runtime skill or router.

## Ownership and distribution

`main` owns family documentation, validators, tests, evals, audit evidence and CI.
Runtime skills ship on separate branches; WebBased retains web/chat rules and
project templates. Never copy runtime packages into main or quality artifacts into
runtime branches. Each runtime has README.md, SKILL.md and useful supporting files.

Multi-package families can share a runtime branch using each capability's validated
`source.subpath`. Each selected subtree must be independently installable with its
own root SKILL.md and stable identity. A single-package family can instead bundle
internal methods as resources. Three.js is one branch-root package with one
catalog/menu identity and only one root SKILL.md. Its 45 internal methods live at
`skills/<name>/GUIDE.md`, not native specialist SKILL.md entries. Invoke the family
through the host, then read selected guides through authorized resource tools.
Explicit method names and minimum prompt-based selection are supported without
separate native registrations. It owns no second lifecycle.
Its catalog-scoped validator permits enumerated code, shader and binary resource
types, checking signatures without decoding binaries as UTF-8. Existing family
allowlists remain unchanged. Preserve supplied licenses; family registration is
not a declaration of blanket redistribution rights.

Andino owns lifecycle and completion when active. For CHECKPOINTED work its plan
owns checkpoints and authoritative NEXT ACTION; EPHEMERAL work requires no durable
plan. Specialists return domain results, evidence, limitations and recommended
actions. Without Andino they use normal host task context. Installation is not
activation. Neither specialist requires the other; no meta-router is needed.

## Metadata and activation

Require unique, stable name and meaningful description in YAML frontmatter.
Use a 1-64 character lowercase alphanumeric name with single hyphen separators,
matching the installed folder. Descriptions are 1-1024 characters, lead with purpose
and activation scope, and include material exclusions. These portable family rules
need not be enforced identically by every host. The dependency-free validator
supports plain string scalars, not general YAML. Add optional fields only for a
truthful, useful and supported purpose; no license or permission fields for symmetry.

Andino supports adaptive problem solving across development, troubleshooting,
research, decisions, daily tasks and conversation. DIRECT/GROUNDED/INVESTIGATIVE
reasoning depth is independent of EPHEMERAL/CHECKPOINTED persistence; LITE/STANDARD/DEEP
describe only plan density. Explicit simple or conversational invocation remains
natural, while implicit activation avoids routine questions and trivial edits.
Rescue investigates engineering fragility;
Skripsi handles substantive research. Simple edits normally need no lifecycle;
AI authorship alone is not rescue evidence; sentence polish needs no research
orchestration. Honor explicit scope and native host invocation controls.

## Package and README

Keep essential authority, evidence, activation and lifecycle contracts in SKILL.md.
Load focused references on demand through shallow, discoverable routes. Preserve
domain methods, terminology and depth. Current Andino/Rescue packages use references;
Skripsi also uses research assets. Add assets/scripts only for actual runtime needs.
No empty placeholders, personal configuration, credentials, control-plane material,
submodules or symlink entries in distributed package trees.

Andino is also one branch-root native package. Its internal methods use
`skills/<id>/GUIDE.md` and on-demand Markdown resources, with source-name aliases
resolving to one canonical implementation. They never register extra native skills.
Its scoped resource policy accepts only the currently required Markdown guide,
reference, resource, template and example paths; no global suffix allowlist changes
or automatic example execution. The main quality plane holds source/asset matrices,
ownership, procedural fixtures, live records and candidate release hashes. Source
checkouts and build/audit artifacts are excluded from distributed runtime folders.

Each README explains role/boundaries, whole-folder installation, host roots/discovery,
invocation, optional coexistence, safe update, verification, positive/negative manual
smoke cases, package contents and a main quality-plane link. Preserve user edits;
avoid duplicate discoverable copies unless an override is intentional. Verify host
claims against current first-party documentation, recording source/date. Distinguish
versions, surfaces, refresh and duplicate rules. Do not extrapolate symlink or
Windows junction guarantees across hosts.

## Evidence, provenance and authorization

- STRUCTURAL VERIFIED: executed deterministic checks at named revisions.
- DOCUMENTATION VERIFIED: a read first-party source supports the named claim.
- LIVE HOST VERIFIED: observed discovery or execution with host/version, revision,
  input, actual action/output and explicit scope of proof.
- NOT VERIFIED: unexecuted or unavailable; record the limitation and next check.

Discovery proves visibility, not correct selection or behavior. Keep historical
results tied to their tested revision; implementation ownership and manual scenarios
are not executed outcomes. Preserve domain-specific evidence rules: current factual
repository state, engineering evidence independent of authorship, and no fabricated
academic evidence. Do not invent provenance, endorsement or family licensing from
an upstream license; do not reconstruct proprietary materials.

Activation grants no authority for commits, pushes, merges, publication, deployment,
live-data changes or unrelated side effects. Follow applicable user authorization
and host controls, retaining stricter research ethics/access gates.

## Minimum quality and release verification

Focus bundles the complete communication A from WebBased's project chat-rules
entrypoint and unchanged Indonesian/English style references. Compare the README
A before syncing; disagreement requires maintainer review. Main's validator accepts
`--webbased-ref` for a local Git source-drift check and `--focus-dir` for an
uncommitted package; neither is a runtime dependency or an automatic overwrite.
CI fetches WebBased and checks the current Focus branch, so publish the matching
runtime change before enabling the corresponding main CI change. Loading all three
references is a skill instruction, not an enforced hook; package and installer
checks cannot establish model compliance. Preserve instruction hierarchy, style-only
examples, user overrides and the existing Focus/Andino ownership boundary.

Every skill needs package, required README/entrypoint, metadata, relative-link,
allowed-path and regular-Git-file validation. Include representative positive,
negative and distinctive regression expectations, and meaningful failure-case tests
for validators. Do not snapshot README prose or manufacture FR/NFR registers.
Skripsi's formal SRS justifies deeper traceability than its siblings.

Before release, run unit tests, package/eval checks at intended refs, applicable
traceability and recorded-evidence checks; inspect every diff, run git diff --check
and verify expected branch status. Use explicit local refs for unpublished runtime
commits. CI reads fetched remote refs and must not silently execute paid models.
Create logical commits by branch; publish runtimes before dependent main changes
only when authorized. A successful subset is not universal behavioral proof.

