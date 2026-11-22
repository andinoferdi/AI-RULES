# Monorepo: every skill in `skills/` on main

Status: IN_PROGRESS
Plan Depth: DEEP
Current Phase: Phase 2 — Installer
Last Updated: 2026-11-22
Branch / worktree: `monorepo` in `C:\Users\Andino\Downloads\AI-RULES\monorepo`
(its own clone; the parent folder `C:\Users\Andino\Downloads\AI-RULES` is a
second clone with every file deleted. Never commit from the parent.)

## Executive Snapshot

AI-RULES moves from one orphan branch per skill plus pins on `main` to one
`main` branch where every skill lives in `skills/<id>/`. `ai-rules setup` is
the only install path (no `npx skills` option, owner decision 2). Run inside a
clone, setup installs the working-tree `skills/` folder, so an edit is used on
the next setup without a commit. Outside a clone it installs `main:skills/<id>`
from GitHub. Pins, promotion and drift tooling are removed. The WebBased branch
stays untouched; its focus-reference check keeps one validation-only pin.
Existing installs (the owner's own 40 targets) upgrade because setup now
recognizes content it recorded itself. Nothing is implemented yet; `skills/`
is present but uncommitted and matches every skill branch head.

## Objective

Make branch `monorepo` a publishable monorepo: installer, catalog, checks,
tests and documentation follow the `skills/` layout, and the four owner flows
work and are proven by running them.

## Acceptance Criteria

- [ ] R1 Clone, `python -m pip install .`, `ai-rules setup` from the clone
      installs all 8 skills plus the 31 native `andino-*` members (proven in a
      disposable home from a fresh clone of the pushed `monorepo` branch).
- [ ] R2 A skill is changed by editing `skills/<id>/` in the clone.
- [ ] R3 Rerunning `ai-rules setup` in the clone installs the uncommitted edit
      (UPDATE for that skill, NO_OP for the rest), with no commit or push.
- [ ] R4 After commit/PR/merge, anyone running `ai-rules setup` outside a clone
      gets the new `main` content. Proven before merge by an automated fixture
      test and by installing from the pushed GitHub branch
      (`AI_RULES_SOURCE_BRANCH=monorepo`); the post-merge check on real `main`
      is listed as not verifiable before the owner merges.
- [ ] R5 Installs made by the old installer upgrade without
      "modified or unrecognized" blocks; hand-edited installed copies stay
      preserved (blocked) as before.
- [ ] R6 No pins for skills: `release_manifest.json` has no `first_party`
      pins; `promote_skill.py`, `skill_refs.py` and their tests are gone; ADR
      0002 supersedes ADR 0001.
- [ ] R7 CI: a fast skills job on every PR/push to main; the 3-OS installer
      matrix runs only when installer files change, and always on schedule,
      manual dispatch and release.
- [ ] R8 A skill change and the tests that read it land in one commit: every
      check reads `skills/` from the same checkout, never a Git ref.
- [ ] R9 README, AGENTS.md (and CONTEXT.md, docs/agents/domain.md,
      docs/ci-coverage.md, docs/specs) explain the new flow in plain words.
- [ ] R10 `python scripts/ci_checks.py --group all` passes locally (full
      ~13-minute suite run in the background, no short timeout), and a
      dispatched "Validate skills" run on branch `monorepo` is green.
- [ ] R11 WebBased branch untouched; skill branches not deleted; nothing merged
      to main; PR to main opened only after owner approval.
- [ ] R12 Commits carry no Co-Authored-By or Claude attribution.

Dropped by owner: "`npx skills add` can read the repo" (decision 2, 2026-11-22).

## Owner decisions (2026-11-22)

| # | Decision |
| --- | --- |
| 1 | `ai-rules setup` inside a clone uses the local `skills/` automatically and says so; outside a clone it uses GitHub `main`. `--source` can force one. |
| 2 | No `npx skills` option. `ai-rules setup` is the only install path; README highlights that it installs the native Andino members, which `npx skills` cannot. |
| 3 | Old installs must upgrade cleanly; the owner is the first real upgrade. |
| 4 | WebBased (skills for chat/web AI) is not touched. End state: two branches, `main` and `WebBased`. Deleting the old skill branches is a later step that needs the owner's explicit approval. |
| 5 | Commit and push to `monorepo` allowed. No merge to main, no branch deletion, PR only after approval. No subagents without approval (none planned). |

## Approach and constraints

- Reuse the installer's Git-tree pipeline. Catalog sources become
  `{repository: GitHub AI-RULES, branch: main, subpath: skills/<id>}`; subpath
  support already exists (`LatestSources.tree/bundle`, `export_git_ref`,
  `tests/installer/test_source_subpaths.py`).
- Local source: snapshot the checkout's `skills/` folder (working tree,
  uncommitted edits included) into a private temporary Git store and feed that
  commit to the same pipeline. One code path for verification and hashing.
- Recognition of earlier installs uses the installer's own records:
  `managed-installations.json` `files` (all 40 owner records have them) and
  `family-inventories/*.json` fingerprints for native members.
- `--source bundled` (used by `repair`) uses packaged bundles in a release
  executable, else the checkout's working-tree `skills/<id>` folder.
- WebBased drift check stays, reading the pinned `validation_refs.WebBased`
  commit, so a WebBased push can never turn main red.
- Tests: `tests/installer/` = installer code with fixture data;
  `tests/` top level = anything that reads real skill content (validators,
  skill quality, and installer integration with real skills).
- English for repository docs, plain wording. Indonesian only in chat.
- Windows home sandbox: set `USERPROFILE` to a temp dir (Python `Path.home()`)
  and keep `HOME` as the real home so Git keeps its credentials/config.

## Baseline (observed 2026-11-22, checks run against skill branch heads = `skills/` content)

| Step | Result | Seconds |
| --- | --- | --- |
| validate_skills | FAIL `natural-writing: unexpected runtime file: scripts/check.py` | 61 |
| validate_threejs_family | PASS | 40 |
| validate_andino_capabilities | PASS | 16 |
| unittest discover -s tests | PASS, 433 tests, 5 skipped (Windows, Python 3.15) | 760 |
| validate_skripsi_traceability | PASS | 0 |
| build_release --stage-only | PASS, 8 bundles | 23 |

Where the 760 s go: the 10 skill-content tests that T7 moves out of
`tests/installer/` cost about 400 s, because each fetches the whole repository
through `--source latest` (slowest: `test_search_first` actual-packages case
122 s; five `*_distribution` cases about 45 s each; focus 13 s; family
installs 9–10 s). T7 switches them to `--source local` (snapshot of the
checkout, no fetch) to make the skills job fast. Target: skills group under
5 minutes on the CI runner. That is a target to measure in T12, not a promise.

Skill heads ahead of old pins: ai-codebase-rescue (2), skripsi-skill (2),
search-first (3), focus (1), natural-writing (4). Equal to pins: andino-workflow,
council, threejs-skills. `skills/` equals every branch head file-for-file
(CRLF ignored); no file in `skills/` has CRLF; all branch modes are 100644.

## Execution Board

| Phase | Status | Goal | Tasks | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 0 — Plan review | DONE | Owner approves plan | — | Approved 2026-11-22 |
| Phase 1 — Skills on main | DONE | R2, R8 foundation | T1 | 8 trees equal branch heads |
| Phase 2 — Installer | TODO | R1, R3, R4, R5, R6 | T2, T3, T4, T5 | Not run |
| Phase 3 — Checks and tests | TODO | R6, R8, R10 | T6, T7, T8 | Not run |
| Phase 4 — CI | TODO | R7 | T9 | Not run |
| Phase 5 — Docs | TODO | R9 | T10 | Not run |
| Phase 6 — Proof and delivery | TODO | R1–R5, R10–R12 | T11, T12, T13, T14, T15 | Not run |

## Coverage

| Requirement / failure case | Owner | Observable check |
| --- | --- | --- |
| R1 fresh clone installs 8 skills + 31 members | T13 | sandbox: 39 dirs under `<tmp>/.claude/skills`, `lock.json` status `verified`, output `Skill source: local folder` |
| R2/R3 uncommitted edit installs on rerun | T4 test, T13 | `test_local_source_installs_uncommitted_edit`; sandbox: marker line present in installed `focus/SKILL.md`, output has `UPDATE` for focus only |
| R3 second local run after local run is not blocked | T3 test | `test_recorded_install_updates_without_source_history` |
| R4 new main commit reaches a non-clone user | T3 test, T13 | `test_latest_installs_main_head_and_later_commit`; sandbox B: installed tree == `git ls-tree origin/monorepo:skills/<id>` |
| R4 maintainer branch override | T4 test | `test_source_branch_override_fetches_named_branch` |
| R5 old installer records upgrade | T3 tests, T14 | `test_recorded_install_updates_without_source_history`, `test_recorded_native_member_updates`; rehearsal on a copy of `~/.ai-rules`; real dry-run shows no BLOCK |
| R5 hand-edited copy preserved | T3 | existing `test_user_edits_are_preserved_and_never_reported_current` stays green |
| R5 member history inside subpath | T3 test | `test_member_from_older_monorepo_commit_is_recognized` |
| `--source local` outside a clone | T4 test | `test_local_source_outside_checkout_is_an_error` |
| auto picks local in clone, latest outside | T4 test | `test_auto_source_*` (2 cases) |
| R6 no pins / promotion tooling | T2, T5, T6 | `test_skill_registry_consistency.py` new asserts; files absent |
| R7 CI split | T9 | YAML review + dispatched run shows skills job and installer matrix; a docs-only diff computes `installer=false` |
| R8 checks read working tree | T6, T7 | `grep -rn "origin/" scripts tests src` returns only WebBased lines |
| R9 docs | T10 | artifact review; `tests/installer/test_agent_defaults.py` README check still passes |
| R10 all checks | T11, T12 | `ci_checks.py --group all` exit 0; GitHub run conclusion `success` |
| R11/R12 | T11, T12, T15 | `git log --format=%B` has no Co-Authored-By; `git ls-remote` shows skill branches and WebBased unchanged |

## Detailed Execution

### Phase 1 — Skills on main

#### T1 — Commit `skills/` with line-ending rules
Status: TODO
Readiness: READY
Requirements: R2, R8
Depends on: plan approval
Owns: Create `.gitattributes`; Add `skills/**` (already on disk); this plan file
Interfaces: produces the tree every later task reads (`skills/<id>/SKILL.md`).

Change Specification:
- New `.gitattributes` (repo root). `core.autocrlf=true` is set on this
  machine and the tracked worktree is CRLF; LF in the index is the contract the
  installer hashes (`latest.contents` normalizes CRLF, `export_git_ref` forces
  LF). Binary list = every binary suffix found in `skills/` plus
  `BINARY_SUFFIXES` in `scripts/validate_skills.py`.

```gitattributes
* text=auto eol=lf
*.png binary
*.jpg binary
*.jpeg binary
*.webp binary
*.exr binary
*.bin binary
*.glb binary
*.wasm binary
*.gz binary
*.zip binary
```

- `skills/`: no content change. 8 folders, 1163 files.

Actions:
- [ ] `git add .gitattributes skills docs/exec-plans/active/monorepo-skills.md`
- [ ] Check index line endings: `git ls-files --eol skills | grep -v "^i/lf\|^i/-text"` prints nothing.
- [ ] Check the staged tree equals each branch head, for each id in
      `andino-workflow ai-codebase-rescue skripsi-skill search-first focus council threejs-skills natural-writing`:
      `git diff --quiet --cached origin/$id -- ` is not usable across roots, so use
      `test "$(git rev-parse origin/$id^{tree})" = "$(git write-tree --prefix=skills/$id/)"`;
      expect equal tree ids for all 8.
- [ ] `git status --short` shows no other modified tracked files (the attribute
      must not dirty CRLF worktree files). If it does, stop and report.
- [ ] Commit: `Move every skill into skills/ on main`.

Result / Evidence: DONE 2026-11-22.
Ruling: fast-forwarded `monorepo` to `origin/main` 2daf2f4 first (main had gained
"Promote focus to 082ac78" and "Promote natural-writing to e792e33 ..." after the
branch point) — keeps the later PR conflict-free and brings main's own
natural-writing checker/test updates — cost if wrong: none, ff only.
`git write-tree --prefix=skills/<id>/` equals `origin/<id>^{tree}` for all 8;
`git ls-files --eol skills` non-LF entries are only two `.bin` files with
`attr/-text` (binary, expected); no tracked file became modified. T8 note: the
baseline natural-writing allow-list failure may already be fixed by main's
validate_skills.py change; recheck in T6 before editing.

### Phase 2 — Installer

#### T2 — Catalog points every first-party skill at `main:skills/<id>`
Status: TODO
Readiness: READY
Requirements: R6, R1
Depends on: T1
Owns: Modify `src/ai_rules/catalog/data/capabilities.json` (8 first-party
entries, `source`); Rewrite `tests/test_skill_registry_consistency.py`
Interfaces: produces catalog contract `source.branch == "main"`,
`source.subpath == "skills/<id>"`, consumed by T3/T4/T5/T6.

Change Specification:
- Each FIRST_PARTY capability `source` becomes (keep `verified_at` where present):

```json
"source": {
  "repository": "https://github.com/andinoferdi/AI-RULES",
  "branch": "main",
  "subpath": "skills/focus",
  "trust": "first_party"
}
```

- `tests/test_skill_registry_consistency.py`: drop `MANIFEST` pin assertions;
  new truth is catalog ↔ `skills/` folders ↔ `RUNTIME_SKILLS`/families ↔ evals
  ↔ profiles. Replace `setUp` and the two manifest tests with:

```python
SKILLS = ROOT / "skills"

def setUp(self):
    self.catalog = {item["id"]: item for item in load(CATALOG)["capabilities"]
                    if item["ownership"] == "FIRST_PARTY"}
    self.folders = {p.parent.name for p in SKILLS.glob("*/SKILL.md")}

def test_catalog_and_skills_folder_list_the_same_skills(self):
    self.assertEqual(set(self.catalog) - self.folders, set(), "add skills/<id>/SKILL.md")
    self.assertEqual(self.folders - set(self.catalog), set(), "register these folders in capabilities.json")

def test_catalog_sources_read_main_subpaths(self):
    for skill, item in self.catalog.items():
        self.assertEqual("main", item["source"]["branch"], skill)
        self.assertEqual(f"skills/{skill}", item["source"]["subpath"], skill)

def test_release_manifest_has_no_skill_pins(self):
    self.assertNotIn("first_party", load(MANIFEST))
```

  `test_package_validator_covers_every_pinned_skill` compares
  `runtime_skills() | FAMILIES` with `self.folders`.

Actions:
- [ ] Rewrite the test; run `python -m unittest tests/test_skill_registry_consistency.py -v`
      from repo root; expect FAIL on `branch` / `subpath` / `first_party`.
- [ ] Edit catalog. Rerun; the manifest test stays red until T5 (expected).

Result / Evidence: Not run — planned checks only.

#### T3 — Source pipeline: no pins, monorepo members, recognition, local snapshot
Status: TODO
Readiness: READY
Requirements: R3, R4, R5, R6
Depends on: T2
Owns: Modify `src/ai_rules/release/latest.py`; Rewrite fixture parts of
`tests/installer/test_live_updates.py`; Add cases to
`tests/installer/test_source_subpaths.py`
Interfaces:
- consumes inspected `LatestSources(catalog, capability_ids, reporter=None)`,
  `.entries[id] = (local_store, repository, branch, commit)`, `.reconcile(plan, catalog, args)`.
- produces `LatestSources(catalog, capability_ids, reporter=None, *, local_root: Path | None = None)`;
  `snapshot_working_tree(store: Path, checkout: Path) -> str` (commit id);
  `LOCAL_BRANCH = "local"`; version label `local:<id>@<commit>` for local, unchanged
  `git-branch:<id>@<commit>` for GitHub.

Change Specification (`src/ai_rules/release/latest.py`):
1. Remove `MAIN_MANIFEST`, `MAIN_REFSPEC`, `main_pins` and the pin branch in
   `__init__`. Commit is always `rev-parse refs/heads/<branch>^{commit}`.
   Fetch becomes `git fetch --no-tags -- <repository> <refs...>`.
2. Branch selection in `__init__`:
   `branch = os.environ.get("AI_RULES_SOURCE_BRANCH") or capability.source["branch"]`
   (maintainer hook to install a pushed branch before merge; documented in AGENTS.md).
3. `known_revision`: delete the second loop that raises
   "newer than the commit main pins".
4. `known_member(self, local, head, name, actual, subpath=None)`: member tree
   path is `f"{subpath}/skills/{name}" if subpath else f"skills/{name}"`.
   Both callers in `reconcile` pass `self.subpaths[identifier]`.
5. Recognition of the installer's own earlier writes (new helpers, module level):

```python
def recorded_files(state_dir, capability_id, host_id, scope):
    """File hashes setup recorded for this target, or None when it never recorded any."""
    try:
        records = json.loads((Path(state_dir) / "managed-installations.json")
                             .read_text(encoding="utf-8")).get("installations", {})
    except (OSError, ValueError):
        return None
    record = records.get(f"{capability_id}:{host_id}:{scope.value}")
    files = record.get("files") if isinstance(record, dict) else None
    if isinstance(files, list):
        files = {row.get("path"): row.get("blob") for row in files if isinstance(row, dict)}
    return (files, record.get("version")) if isinstance(files, dict) and files else None


def recorded_member(state_dir, root, native):
    """True when native still matches the fingerprint setup stored in the family inventory."""
    from ai_rules.release.family import fingerprint
    key = hashlib.sha256(str(Path(root).resolve()).casefold().encode()).hexdigest()
    try:
        inventory = json.loads((Path(state_dir) / "family-inventories" / f"{key}.json")
                               .read_text(encoding="utf-8"))
        row = inventory.get("artifacts", {}).get(str(native))
        return bool(row) and row.get("kind") == "tree" and fingerprint(native) == row.get("fingerprint")
    except (OSError, ValueError):
        return False
```

   In `reconcile`, non-Git destination branch:

```python
elif destination.exists():
    installed = self.known_revision(identifier, before)
    recorded = None if installed else recorded_files(args.state_dir, identifier, target.host_id, target.scope)
    if installed is None and not (recorded and recorded[0] == before):
        raise ValueError("Local content is modified or unrecognized; preserved. Use explicit repair only after review")
```

   `ActualState.installed_version` = `self.version(identifier, installed)` when
   `installed`, else `recorded[1]` when recognized by record. Member checks
   (active and retired) accept `known_member(...) or recorded_member(args.state_dir, root, native)`.
6. Local snapshot (new):

```python
LOCAL_BRANCH = "local"
_FIXED_DATE = "1970-01-01T00:00:00+0000"  # same tree -> same commit id -> stable version label

def snapshot_working_tree(store, checkout):
    """Commit checkout/skills (uncommitted edits included) into the private store."""
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_INDEX_FILE=str(Path(store) / "local-index"),
               GIT_AUTHOR_NAME="ai-rules", GIT_AUTHOR_EMAIL="ai-rules@localhost",
               GIT_COMMITTER_NAME="ai-rules", GIT_COMMITTER_EMAIL="ai-rules@localhost",
               GIT_AUTHOR_DATE=_FIXED_DATE, GIT_COMMITTER_DATE=_FIXED_DATE)
    base = ["git", "-c", "core.autocrlf=input", "-c", "core.safecrlf=false", "-c", "core.bare=false",
            f"--git-dir={store}", f"--work-tree={checkout}"]
    def run(*args):
        result = subprocess.run([*base, *args], env=env, text=True, encoding="utf-8",
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
        if result.returncode:
            raise ValueError(f"Local skill snapshot failed: {result.stderr.strip()}")
        return result.stdout.strip()
    run("add", "--all", "--", "skills")
    commit = run("commit-tree", run("write-tree"), "-m", "ai-rules local snapshot")
    run("update-ref", f"refs/heads/{LOCAL_BRANCH}", commit)
    return commit
```

   `__init__` with `local_root`: create `self.root / "source-local"`,
   `git init --bare`, `commit = snapshot_working_tree(...)`, then for each id
   `self.entries[id] = (store, str(local_root), LOCAL_BRANCH, commit)` and
   `self.sources[id] = self.bundle(id)`; no fetch. `version()` returns
   `f"local:{identifier}@{commit}"` when `self.local_root` is set.
   Risk: if Git rejects `--work-tree` with a bare store despite
   `core.bare=false`, init the store non-bare (`git init <store>`) and keep the
   same commands; record which one worked.

Tests (`tests/installer/test_live_updates.py`, fixture rewrite):
- `setUp`: one remote on branch `main` with `skills/andino-workflow/`,
  `skills/focus/`, `skills/search-first/`; `self.pkg = self.remote / "skills/andino-workflow"`.
  Catalog override sets only `repository=str(self.remote)` (branch `main` and
  subpath come from the real catalog). `commit()` and `copy_old()` write/read
  `self.pkg` instead of `self.remote`.
- Delete `pin_on_main`, `test_latest_installs_commit_pinned_on_main_not_branch_head`,
  `test_newer_unpromoted_copy_is_kept_with_a_clear_reason`.
- Git-checkout installs are not supported for subpath sources (existing guard
  in `reconcile`). Replace `test_clean_clone_fast_forwards_without_replacing_git_metadata`,
  `test_git_workflow_refreshes_native_member_on_update_and_current_parent`,
  `test_modified_native_member_blocks_parent_update_without_overwriting`,
  `test_dirty_clone_is_preserved`, `test_git_branch_advances_even_when_commit_does_not_change_files`,
  `test_wrong_branch_clone_is_not_switched_implicitly`,
  `test_non_fast_forward_git_history_is_preserved` with one test that a cloned
  target is BLOCKED with "Git checkout for a subpath package is preserved" and unchanged HEAD.
- `test_all_selected_skills_use_their_own_branch` becomes
  `test_all_selected_skills_come_from_one_fetch_of_main` (assert one `fetch` call,
  pattern from `test_source_subpaths.py::test_shared_branch_exports_independent_roots_and_binary_resources`).
- New cases (decisive assertions):

```python
def test_latest_installs_main_head_and_later_commit(self):
    self.commit("first")
    result, output = self.run_cli()
    self.assertEqual(0, result, output)
    self.commit("second")
    result, output = self.run_cli()
    self.assertEqual(0, result, output)
    self.assertIn("second", (self.target / "SKILL.md").read_text())
    lock = json.loads((self.state / "lock.json").read_text())
    workflow = next(t for t in lock["targets"] if t["capability"] == "andino-workflow")
    self.assertIn(self.git(self.remote, "rev-parse", "HEAD").strip(), workflow["target_version"])

def test_recorded_install_updates_without_source_history(self):
    # An old-installer copy: content never committed on main, but setup recorded it.
    self.target.mkdir(parents=True)
    (self.target / "SKILL.md").write_text(
        "---\nname: andino-workflow\ndescription: Fixture workflow\n---\nlegacy branch copy\n", encoding="utf-8")
    (self.target / "README.md").write_text("Fixture\n", encoding="utf-8")
    from ai_rules.release.latest import contents
    self.state.mkdir(parents=True)
    (self.state / "managed-installations.json").write_text(json.dumps({"schema_version": 1, "installations": {
        "andino-workflow:codex:project": {"version": "git-branch:andino-workflow@" + "0" * 40,
            "files": [{"path": p, "blob": b} for p, b in contents(self.target).items()]}}}), encoding="utf-8")
    result, output = self.run_cli()
    self.assertEqual(0, result, output)
    self.assertNotIn("legacy branch copy", (self.target / "SKILL.md").read_text())

def test_unrecorded_unknown_copy_is_preserved(self):
    self.target.mkdir(parents=True)
    (self.target / "SKILL.md").write_text("---\nname: andino-workflow\ndescription: x\n---\nmine\n", encoding="utf-8")
    result, output = self.run_cli()
    self.assertNotEqual(0, result, output)
    self.assertIn("modified or unrecognized", output)
    self.assertIn("mine", (self.target / "SKILL.md").read_text())
```

  (`run_cli` uses `--scope project`; record key scope value is `project`;
  executor checks the exact key format in `cli._installation_key`.)
- `tests/installer/test_source_subpaths.py` additions: a fixture
  `skills/andino-workflow/skills/planning/SKILL.md` (`name: andino-planning`)
  at subpath `skills/andino-workflow`:
  `test_member_from_older_monorepo_commit_is_recognized` — install at commit A,
  commit B changes the member, rerun; expect exit 0 and member content of B
  (RED before fix 4: "Native member andino-planning is modified or unrecognized").
  `test_recorded_native_member_updates` — member content not in history, family
  inventory row written with `family.fingerprint(native)`; rerun installs head.

Actions:
- [ ] Rewrite fixture + add the cases; run
      `python -m unittest tests.installer.test_live_updates tests.installer.test_source_subpaths -v`
      from repo root with `PYTHONPATH=src;tests` (Windows `;`); expect failures for
      the new cases and the catalog-driven fixture.
- [ ] Apply changes 1–6. Rerun; expect all PASS, nonzero count.

Result / Evidence: Not run — planned checks only.

#### T4 — CLI source choice: auto, local, latest, bundled
Status: TODO
Readiness: READY
Requirements: R1, R3, R4
Depends on: T3
Owns: Modify `src/ai_rules/cli.py` (`add_common_setup_flags`, `cmd_setup`,
`_resolve_from_args`, `_executor_for_plan`, `_record_managed_installations`,
`_release_manifest` callers); Create `src/ai_rules/release/checkout.py`;
Create `tests/installer/test_local_source.py`
Interfaces: produces `find_checkout(start: Path) -> Path | None`,
`resolve_source(choice: str, cwd: Path) -> tuple[str, Path | None]`,
`bundled_targets(catalog) -> dict[str, Path]` (in `checkout.py`).

Change Specification:
- `src/ai_rules/release/checkout.py` (proposed):

```python
MARKER = Path("src/ai_rules/catalog/data/capabilities.json")

def find_checkout(start):
    """Closest folder at or above start that is an AI-RULES clone with skills/."""
    for folder in (Path(start).resolve(), *Path(start).resolve().parents):
        if (folder / MARKER).is_file() and any((folder / "skills").glob("*/SKILL.md")):
            return folder
    return None

def resolve_source(choice, cwd):
    checkout = find_checkout(cwd) if choice in ("auto", "local", "bundled") else None
    if choice == "local" and checkout is None:
        raise ValueError("--source local runs inside an AI-RULES clone (a folder with skills/ and src/ai_rules); "
                         "cd into your clone or use --source latest")
    if choice == "auto":
        return ("local", checkout) if checkout else ("latest", None)
    return choice, checkout
```

- `add_common_setup_flags`: `--source` choices `("auto", "local", "latest", "bundled")`,
  default `"auto"`, help: "auto uses the skills/ folder when run inside an
  AI-RULES clone, otherwise GitHub main; local forces the clone; latest forces
  GitHub main; bundled uses the skills packaged in this executable".
- `_prepare_args`: `args.source, args._checkout = resolve_source(getattr(args, "source", "bundled"), Path.cwd())`
  (`repair` keeps `source="bundled"`; `restore` Namespace without `source`
  resolves to bundled as today).
- `_resolve_from_args`: condition `args.source in ("latest", "local")`;
  construct `LatestSources(..., local_root=args._checkout if args.source == "local" else None)`.
- `cmd_setup`: after the summary print, print one line:
  `Skill source: local folder <checkout>/skills` | `Skill source: GitHub main (<repository>)`
  (`<repository>` from the first FIRST_PARTY capability, plus ` branch <name>`
  when `AI_RULES_SOURCE_BRANCH` is set) | `Skill source: bundled with this executable`.
- `_executor_for_plan` bundled path: replace manifest/export logic with
  `bundles = bundled_targets(catalog, args._checkout)` where each id maps to
  `packaged_bundle(id)` or `checkout / "skills" / id`; missing both raises
  `ValueError("bundled source needs a release executable or an AI-RULES clone")`.
- `_record_managed_installations`: replace `_release_manifest().get("first_party")`
  membership with `catalog.require_capability(id).ownership.value == "FIRST_PARTY"`;
  bundled records get `source = {"subpath": f"skills/{id}", "origin": "bundled"}` and `files`.
- Keep `--source latest` behavior name (existing scripts/tests use it).

Tests (`tests/installer/test_local_source.py`, new): fixture checkout dir
(not a Git repo) containing `src/ai_rules/catalog/data/capabilities.json`
(copy of the real file) and `skills/{andino-workflow,focus,search-first}/{SKILL.md,README.md}`
with correct `name:` lines; `contextlib.chdir(checkout)`; CLI args like
`test_live_updates.run_cli` but `--source <choice>`.

```python
def test_local_source_installs_uncommitted_edit(self):
    result, output = self.run_cli("local")
    self.assertEqual(0, result, output)
    self.assertIn("Skill source: local folder", output)
    skill = self.checkout / "skills/focus/SKILL.md"
    skill.write_text(skill.read_text() + "local edit marker\n", encoding="utf-8")
    result, output = self.run_cli("local")
    self.assertEqual(0, result, output)
    self.assertIn("local edit marker", (self.project / ".agents/skills/focus/SKILL.md").read_text())
    lock = json.loads((self.state / "lock.json").read_text())
    self.assertEqual("verified", lock["status"])

def test_auto_source_uses_checkout_inside_clone(self):
    result, output = self.run_cli("auto")
    self.assertIn("Skill source: local folder", output)

def test_auto_source_uses_github_outside_clone(self):
    with contextlib.chdir(self.root), patch.object(cli, "LatestSources", side_effect=RuntimeError("remote")) as remote:
        result, output = self.run_cli("auto")
    self.assertIsNone(remote.call_args.kwargs.get("local_root"))

def test_local_source_outside_checkout_is_an_error(self):
    with contextlib.chdir(self.root):
        result, output = self.run_cli("local")
    self.assertEqual(2, result)
    self.assertIn("runs inside an AI-RULES clone", output)

def test_source_branch_override_fetches_named_branch(self):
    ...  # remote fixture with branch "feature"; env AI_RULES_SOURCE_BRANCH=feature; installed body from feature
```

Hermetic-test hazard: unittest runs with cwd = repo root, which is a checkout,
so the new `auto` default turns every CLI call without `--source` into a
local install of the real `skills/`. Before implementing, list the calls:
`grep -rn "cli.main(\|run_cli(\|cmd_setup(" tests` and check each call for
`--source`. Known files with calls lacking it: `tests/installer/test_terminal_ux.py`,
`tests/test_semantic_preservation.py` (counts per file: see grep). A call that
relies on a fixture remote gets `--source latest`; a call that intends the
real skills gets `--source local`. Record the list in T4 evidence.

Actions:
- [ ] Add the test file; run `python -m unittest tests.installer.test_local_source -v`; expect
      argparse rejection of `local`/`auto` (RED for missing behavior).
- [ ] Pin `--source` on the CLI calls found by the grep above.
- [ ] Implement; rerun focused tests, then `python -m unittest discover -s tests/installer`.

Result / Evidence: Not run — planned checks only.

#### T5 — Release manifest without pins; release build from `skills/`
Status: TODO
Readiness: READY
Requirements: R6
Depends on: T4
Owns: Modify `src/ai_rules/release/data/release_manifest.json`,
`scripts/build_release.py`, `scripts/smoke_release.py`,
`src/ai_rules/capabilities/adapters.py::StaticCapabilityAdapter.resolve_target`,
`src/ai_rules/release/bundles.py` (add `bundle_sources()`)

Change Specification:
- `release_manifest.json` becomes:

```json
{
  "schema_version": 2,
  "channel": "stable",
  "validation_refs": {
    "WebBased": {
      "branch": "WebBased",
      "commit": "76f9af105cc1a5bffda2ff0f9fdcd39b69c63845",
      "purpose": "Focus communication reference drift check"
    }
  }
}
```

- `build_release.py`: targets come from the catalog's FIRST_PARTY ids;
  `stage_bundles(ids, destination, root)` copies `root/skills/<id>` (working
  tree) with `shutil.copytree`, then runs the existing identity and
  `package_files` checks. It writes `destination/bundle-sources.json`:
  `{"source_commit": <HEAD>, "source_dirty": <bool>, "skills": {id: "skills/<id>"}}`.
  The executable manifest's `first_party` becomes that `skills` map.
  Existing test `tests/installer/test_source_subpaths.py::test_release_manifest_cannot_write_capability_outside_staging_root`
  keeps its `../escape` rejection via `validate_subpath` on ids.
- `bundles.py::bundle_sources() -> dict`: read packaged `bundles/bundle-sources.json`, else `{}`.
- `smoke_release.py`: expected ids from the catalog, expected bytes from `skills/<id>`.
- `adapters.resolve_target`: FIRST_PARTY returns `f"bundled:{capability.id}@{source_commit}"`
  when `bundle_sources()` has a commit, else `f"skills-folder:{capability.id}"`.

Actions:
- [ ] Apply; run `python scripts/build_release.py --stage-only --output <scratch>/frozen`;
      expect `Exported 8 bundles`; run `tests/test_skill_registry_consistency.py` → all PASS.

Result / Evidence: Not run — planned checks only.

### Phase 3 — Checks and tests

#### T6 — Validators read `skills/`; ci_checks groups; remove pin tooling
Status: TODO
Readiness: READY
Requirements: R6, R7, R8
Depends on: T1 (independent of T3–T5 except shared `tests/` writes: serialize after T5)
Owns: Modify `scripts/validate_skills.py`, `scripts/validate_threejs_family.py`,
`scripts/validate_andino_capabilities.py`, `scripts/validate_skripsi_traceability.py`,
`scripts/ci_checks.py`; Delete `scripts/promote_skill.py`, `scripts/skill_refs.py`,
`scripts/check_andino_installation.py`, `tests/test_promote_skill.py`,
`tests/test_skill_refs.py`; Modify `tests/test_validate_skills.py` as needed

Change Specification:
- `validate_skills.py::main`: one `--skills-dir` (default `ROOT / "skills"`)
  replaces every `--*-ref`/`--*-dir` flag; each skill is
  `directory_files(skills_dir / skill)`; Three.js is always validated from
  `skills_dir / "threejs-skills"`. `--webbased-ref` stays, default
  `None`; ci_checks passes the pinned commit from
  `release_manifest.json` `validation_refs.WebBased.commit` (fetched by CI with
  `git fetch origin WebBased`). Allow-list fix found by baseline, in
  `package_files` after the focus/search-first provenance rule:

```python
if expected_name == 'natural-writing' and name == 'scripts/check.py':
    allowed = True
```

- `validate_threejs_family.py`: default `--runtime-dir ROOT/skills/threejs-skills`; drop `--runtime-ref`.
- `validate_andino_capabilities.py`: default `--runtime ROOT/skills/andino-workflow`; drop `--runtime-ref`.
- `validate_skripsi_traceability.py`: paths from `ROOT/skills/skripsi-skill` (`rglob`, posix relative); drop `--runtime-ref`.
- `ci_checks.py`: `--group {skills,installer,all}` (default `all`):

```python
def steps(staging, group):
    py = sys.executable
    top_level = sorted(p.stem for p in (ROOT / "tests").glob("test_*.py"))
    skills = [
        ("Validate skill packages", [py, "scripts/validate_skills.py", "--webbased-ref", webbased_commit()]),
        ("Validate Three.js inventory and scenario schemas", [py, "scripts/validate_threejs_family.py"]),
        ("Validate capability evaluation schemas", [py, "scripts/validate_andino_capabilities.py"]),
        ("Test skills and validators", [py, "-m", "unittest", *top_level]),
        ("Audit skripsi requirement ownership", [py, "scripts/validate_skripsi_traceability.py"]),
        ("Validate frozen release bundles", [py, "scripts/build_release.py", "--stage-only", "--output", str(staging)]),
    ]
    installer = [("Test installer regressions", [py, "-m", "unittest", "discover", "-s", "tests/installer"])]
    return {"skills": skills, "installer": installer, "all": skills + installer}[group]
```

  env adds `ROOT / "tests"` to `PYTHONPATH` so `unittest test_x` imports top-level modules.
  `webbased_commit()` reads the manifest; if that commit is missing locally,
  the step fails with "run git fetch origin WebBased".
- Delete the five files listed under Owns. `check_andino_installation.py`
  only rewrites pins and is not used by CI or tests (grep evidence: only
  `tests/test_andino_evolution.py` uses `check_andino_publication.py`, which stays).

Actions:
- [ ] Apply; run `python scripts/validate_skills.py --webbased-ref 76f9af105cc1a5bffda2ff0f9fdcd39b69c63845`;
      expect `PASS: 7 skill packages` and the Focus/WebBased PASS line.
- [ ] Run the other three validators; expect PASS.
- [ ] `grep -rn "origin/\|runtime-ref\|skill_refs\|promote_skill" scripts src .github` → no hits except WebBased handling.

Result / Evidence: Not run — planned checks only.

#### T7 — Tests read the working tree; skill-content tests leave `tests/installer/`
Status: TODO
Readiness: READY
Requirements: R7, R8
Depends on: T5, T6
Owns: Create `tests/skill_source.py`; Move (git mv) from `tests/installer/` to
`tests/`: `test_search_first.py`, `test_delegation_distribution.py`,
`test_planning_distribution.py`, `test_plan_execution_distribution.py`,
`test_code_simplification_distribution.py`, `test_brainstorming_distribution.py`,
`test_threejs_family_selection.py`, `test_focus.py`, `test_first_party_bundles.py`,
`test_andino_family_installation.py`; Modify those plus `tests/test_andino_debugging_order.py`,
`tests/test_andino_reliability.py`, `tests/test_andino_thin_coordinator.py`,
`tests/test_optimize_prompt_patterns.py`, `tests/installer/test_threejs_installation.py`,
`tests/installer/test_catalog_profiles.py` (only if they fail)

Classification evidence (grep of real-content reads: `release_manifest`,
`git show`, `ls-tree`, `origin/`, `parents[2]`): the 10 moved files read real
skill content; `test_live_updates`, `test_source_subpaths`,
`test_threejs_installation`, `test_release_smoke` use fixtures and stay.

Change Specification:
- `tests/skill_source.py` (proposed):

```python
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

def skill_text(skill, path):
    return (SKILLS / skill / path).read_text(encoding="utf-8").replace("\r\n", "\n")

def skill_files(skill, prefix=""):
    base = SKILLS / skill
    return sorted(p.relative_to(base).as_posix() for p in (base / prefix).rglob("*") if p.is_file())
```

- Replace each `git show <commit-or-ref>:<path>` with `skill_text(<id>, <path>)`,
  each `ls-tree` listing with `skill_files`, each manifest commit lookup with
  nothing (content is the working tree). Moved files: fix `parents[2]` →
  `parents[1]` for ROOT. `test_first_party_bundles` / `test_threejs_family_selection`:
  export via `shutil.copytree(SKILLS / id, target)` instead of `export_git_ref(commit)`.
- `test_andino_family_installation` uses `--source bundled`; under T4 that
  installs `skills/andino-workflow` from the checkout (cwd = repo root under unittest).

Actions:
- [ ] `git mv` the 10 files; add helper; edit reads.
- [ ] Switch their CLI calls from `--source latest` against the repository to
      `--source local` with cwd = repo root (same content, no fetch). Keep one
      GitHub-shaped path covered by the fixture tests in `tests/installer/`.
- [ ] Run `python scripts/ci_checks.py --group skills` (background, no short timeout); expect the
      unittest step to list a nonzero count; collect failures for T8.
- [ ] Run `python -m unittest discover -s tests/installer` ; expect PASS.

Result / Evidence: Not run — planned checks only.

#### T8 — Fix failures caused by the newer skill heads
Status: TODO
Readiness: READY
Requirements: R10
Depends on: T7
Owns: the failing test/data files only (counts, inventories, allow-lists).
Baseline evidence: with every check reading the skill heads, the only failure
was `natural-writing: unexpected runtime file: scripts/check.py` (fixed in T6).
The 433 unit tests passed, but the andino distribution tests read the
andino-workflow pin, which equals its head, so no further drift is expected.
Rule for anything T7 surfaces: a skill file changes only when the failure shows
a real skill defect; test data that lagged behind the skill is updated. Each
fix records the failing assertion and the skill that caused it.
Actions:
- [ ] Run `python scripts/ci_checks.py --group skills` after T7 (background).
- [ ] For each failure apply the rule above; rerun the failing module, then the group.

Result / Evidence: Not run.

### Phase 4 — CI

#### T9 — Fast skills job, conditional installer matrix
Status: TODO
Readiness: READY
Requirements: R7, R10
Depends on: T6
Owns: Modify `.github/workflows/validate-skills.yml`; `release.yml` unchanged
except it already calls the reusable workflow (installer forced by `workflow_call`).

Change Specification (`validate-skills.yml` jobs):

```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      installer: ${{ steps.diff.outputs.installer }}
    steps:
      - uses: actions/checkout@v7
        with: {fetch-depth: 0}
      - id: diff
        shell: bash
        run: |
          if [ "${{ github.event_name }}" != pull_request ] && [ "${{ github.event_name }}" != push ]; then
            echo installer=true >> "$GITHUB_OUTPUT"; exit 0; fi
          base="${{ github.event.pull_request.base.sha || github.event.before }}"
          if ! git cat-file -e "$base^{commit}" 2>/dev/null; then echo installer=true >> "$GITHUB_OUTPUT"; exit 0; fi
          if git diff --name-only "$base" "${{ github.sha }}" | grep -qE '^(src/|tests/installer/|pyproject\.toml|packaging/|scripts/(build_release|smoke_release|ci_checks)\.py|\.github/workflows/)'; then
            echo installer=true >> "$GITHUB_OUTPUT"; else echo installer=false >> "$GITHUB_OUTPUT"; fi
  skills:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps: checkout (fetch-depth 0), setup-python 3.12,
           `git fetch --no-tags origin WebBased`, `pip install --editable .`,
           `python3 scripts/ci_checks.py --group skills`
  installer:
    needs: changes
    if: needs.changes.outputs.installer == 'true'
    matrix: unchanged three OS/Python rows
    steps: checkout, setup-python, `pip install --editable .`,
           `python -m unittest discover -s tests/installer`
```

Remove the `skill_refs.py pin` and `drift` steps. Triggers unchanged
(push main, PR main, dispatch, call, nightly cron).

Actions:
- [ ] Apply; validate YAML parses: `python -c "import yaml,sys;yaml.safe_load(open('.github/workflows/validate-skills.yml'))"`
      (PyYAML present? if not, check with `gh workflow view` after push).
- [ ] Simulate the filter locally on two diffs: docs-only → `installer=false`; `src/` change → `true`.

Result / Evidence: Not run — planned checks only.

### Phase 5 — Docs

#### T10 — Explain the new flow in plain words
Status: TODO
Readiness: READY
Requirements: R9
Depends on: T4, T6, T9
Owns: Modify `README.md` (Quick Start + new "Change a skill" section + source
table + comparison table claims), `AGENTS.md`, `CONTEXT.md`,
`docs/agents/domain.md`, `docs/ci-coverage.md`, `docs/DECISIONS.md`;
Create `docs/adr/0002-skills-live-on-main.md`; Modify ADR 0001 status line
(`Status: superseded by 0002, 2026-11-22`); Replace
`docs/specs/skill-promotion.md` with `docs/specs/changing-skills.md`
(adding/removing a skill: folder, catalog entry, profiles `everything`,
`RUNTIME_SKILLS` or family list, `evals/<id>.json`; the registry test names misses).

Content contract:
- README Quick Start: `git clone https://github.com/andinoferdi/AI-RULES.git`,
  `cd AI-RULES`, `python -m pip install .`, `ai-rules setup`.
- README "Change a skill": 1) edit `skills/<name>/`; 2) run `ai-rules setup`
  in the clone, it says `Skill source: local folder` and installs your edit;
  3) start a new agent session; 4) happy? commit, PR, merge; everyone who runs
  `ai-rules setup` gets it. One line on `--source latest` / `local` / `bundled`.
- README: say plainly that setup installs the Andino workflow and its 31
  members as native skills (`/andino-planning`, `$andino-tdd`) with rollback,
  which generic skill installers do not do. No `npx skills` instructions.
- README: updating from the old branch-based installer: `git pull` in the
  clone, `python -m pip install .`, `ai-rules setup`.
- AGENTS.md: where truth lives (`skills/`, catalog, profiles), changing a
  skill, adding/removing a skill, checks (`ci_checks.py --group skills|installer|all`),
  `AI_RULES_SOURCE_BRANCH` for maintainers, WebBased validation pin.
- CONTEXT.md: remove Skill branch, Pin, Promote, Drift, Latest/Bundled-as-pins;
  add Skill folder, Local source, GitHub source, Bundled source; keep Family,
  Validation ref (WebBased).
- Check the README test: `tests/installer/test_agent_defaults.py` reads README.

Actions:
- [ ] Write; `git diff --check`; run `python -m unittest tests.installer.test_agent_defaults`.
- [ ] `grep -rn "promote\|skill branch\|pin" README.md AGENTS.md CONTEXT.md docs/agents docs/specs docs/ci-coverage.md`
      → only historical mentions inside ADR 0001/0002 and DECISIONS.

Result / Evidence: Not run — planned checks only.

### Phase 6 — Proof and delivery

#### T11 — Commit and run the full suite
Status: TODO
Readiness: READY
Depends on: T1–T10
Actions:
- [ ] Commits on `monorepo` (no attribution lines): "Install skills from skills/ on main"
      (T2–T5), "Read skills from the working tree in checks and tests" (T6–T8),
      "Run installer tests only when the installer changes" (T9), "Document the
      monorepo flow" (T10).
- [ ] `git fetch origin WebBased`; `python scripts/ci_checks.py --group all` in the
      background with a timeout ≥ 40 minutes; expect `PASS: all main checks`.
- [ ] `git log origin/main..HEAD --format=%B | grep -i "co-authored\|claude"` → nothing.

#### T12 — Push and dispatch CI on the branch
Status: TODO
Readiness: READY
Depends on: T11
Actions:
- [ ] `git push origin monorepo`.
- [ ] `gh workflow run validate-skills.yml --ref monorepo`; wait for the run with
      `gh run watch <id> --exit-status` in the background; expect success with
      `skills` and all three `installer` jobs (dispatch forces installer=true).

#### T13 — Prove flows 1–4 in disposable homes
Status: TODO
Readiness: READY
Depends on: T12
Prerequisite approval: creating a temp venv and `pip install` of the clone
(downloads `questionary`, `rich` from PyPI) is part of plan approval.
Environment: `<tmp>` under the scratchpad; `USERPROFILE=<tmp>/home-a`
(and `home-b`), `HOME` = real home for Git credentials.
Actions (record each command and observed output in Result):
- [ ] Flow 1: `git clone --branch monorepo https://github.com/andinoferdi/AI-RULES.git <tmp>/clone`;
      `python -m venv <tmp>/venv`; `<tmp>/venv/Scripts/python -m pip install <tmp>/clone`;
      from `<tmp>/clone`: `ai-rules setup --host claude-code --profile everything --yes --non-interactive`.
      Expect `Skill source: local folder`, exit 0, 8 skill dirs + 31 `andino-*`
      dirs in `<tmp>/home-a/.claude/skills`, `lock.json` status `verified`.
- [ ] Interactive spot check: run `ai-rules setup` (no flags) in a Terminal tab
      from `<tmp>/clone` with the same `USERPROFILE`; expect the banner and
      `Up to date` after accepting defaults. (If prompts cannot be driven, record NOT VERIFIED.)
- [ ] Flows 2–3: append `<!-- flow-3 marker -->` to `<tmp>/clone/skills/focus/SKILL.md`;
      rerun the setup command; expect UPDATE only for focus, marker present in
      `<tmp>/home-a/.claude/skills/focus/SKILL.md`, others NO_OP, exit 0.
- [ ] Flow 4 (GitHub): from a folder outside any clone with `USERPROFILE=<tmp>/home-b`:
      `AI_RULES_SOURCE_BRANCH=monorepo ai-rules setup --host claude-code --profile everything --yes --non-interactive`;
      expect `Skill source: GitHub main` + branch note; installed `focus` files
      hash-equal `git ls-tree origin/monorepo:skills/focus` (compare via `latest.contents`).
- [ ] Flow 4 (propagation) is covered by `test_latest_installs_main_head_and_later_commit`;
      the real post-merge run stays NOT VERIFIED until the owner merges.

#### T14 — Upgrade rehearsal from the owner's real old install
Status: TODO
Readiness: READY
Depends on: T12
Actions:
- [ ] Rehearsal: copy `~/.ai-rules` and the five host skill roots
      (`.claude/skills`, `.agents/skills`, `.config/opencode/skills`,
      `.gemini/antigravity-cli/skills`, `.gemini/config/skills`) into
      `<tmp>/home-c`, rewrite `C:\Users\Andino` → `<tmp>/home-c` inside the
      copied JSON, and rename `family-inventories/*.json` to
      `sha256(str(new_root.resolve()).casefold())`; run setup from the clone with
      `--profile everything` and all five hosts, `--dry-run` first, then apply;
      expect no BLOCKED target, 40 targets VERIFIED.
- [ ] APPROVAL GATE — real machine. Status: WAITING.
      `ai-rules setup --dry-run --profile everything --host codex --host claude-code --host opencode --host antigravity-cli --host antigravity-ide --non-interactive`
      from the clone using the real home (read-only preview, run by Claude).
      Applying it changes the owner's live skills: done only after the owner says so,
      or the owner runs it. Backups land in `~/.ai-rules/backups`.

#### T15 — Report and PR draft
Status: TODO
Readiness: READY
Depends on: T11–T14
Actions:
- [ ] Update this plan's evidence, move it to `docs/exec-plans/completed/`, commit and push.
- [ ] Draft PR title/body (no attribution); open the PR to main only after owner approval.
- [ ] Follow-ups for the owner (not done here): merge; after merge run `ai-rules setup`
      outside a clone to confirm GitHub `main`; delete old skill branches
      (`ai-codebase-rescue andino-workflow council focus natural-writing search-first
      skripsi-skill threejs-skills promote/natural-writing skill-promotion-gate`) only with explicit approval.

## Risks

| Risk | Mitigation / check |
| --- | --- |
| `git add --work-tree` refuses a bare store | T3 fallback: non-bare store; recorded in T3 evidence |
| Old installer clients after merge install old branch heads (main has no pins), then break when branches are deleted | README "Updating from the old installer"; branch deletion is a separate approved step |
| Clone size grows (~73 MB, Three.js assets) | Accepted; same blobs already on GitHub, no storage increase |
| Repository is private; other people need access to install | Owner decision whether to make it public; not changed here |
| `.gitattributes` dirties tracked CRLF worktree files | T1 stops if `git status` shows tracked changes |
| Skills job still slow | Baseline durations decide; T8/T9 may move slow tests, recorded |

## Plan Revisions

- 2026-11-22: created after owner decisions 1–4.

## NEXT ACTION

T2 — rewrite `tests/test_skill_registry_consistency.py` (RED on branch/subpath/
first_party), then point the 8 FIRST_PARTY catalog sources at
`main` + `skills/<id>`. Before T6, rerun `scripts/validate_skills.py` to see
whether main's merged update already allows natural-writing `scripts/check.py`.
