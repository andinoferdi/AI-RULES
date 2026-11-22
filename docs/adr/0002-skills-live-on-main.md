# Skills live in skills/ on main; no pins

Status: accepted, 2026-11-23. Supersedes [ADR 0001](0001-main-pins-skill-versions.md).

ADR 0001 kept one orphan branch per skill and pinned each skill's commit on
`main`. It stopped the red-CI problem it was written for, but daily use was
slow: editing a skill meant checking out its branch, committing, pushing,
returning to `main`, and still getting the old version from `ai-rules setup`
until a promote PR (about 15 minutes) was merged. The owner found the flow, not
the users, to be the problem.

The owner chose a monorepo, like `mattpocock/skills` and `addyosmani/agent-skills`:

- Every skill is a folder in `skills/<id>/` on `main`. The catalog reads
  `main` with `subpath` `skills/<id>`; `release_manifest.json` has no skill pins.
- `ai-rules setup` inside a clone installs the clone's `skills/` folder,
  uncommitted edits included; outside a clone it installs GitHub `main`.
  `--source local|latest|bundled` forces one.
- `ai-rules setup` is the only supported install path. Generic installers such
  as `npx skills` stop at `skills/andino-workflow/SKILL.md` and cannot install
  the 31 native `andino-*` members.
- Setup recognizes copies it wrote earlier from its own records
  (`managed-installations.json` file hashes, family inventories), so installs
  made by the branch-based installer update in place.
- CI: skill checks run on every PR; the three-OS installer matrix runs when
  installer files change, nightly, on dispatch and on release.
- `WebBased` stays a separate branch; the Focus reference check reads one pinned
  `WebBased` commit so a push there cannot turn `main` red.

Consequences: the original failure (skill content and main's tests changing
separately) cannot recur, because every check reads `skills/` from the same
checkout as the tests; a skill change and its test updates land in one commit.
A merged PR is the release. Old skill branches are no longer read by anything and
can be deleted once the owner approves; an old installer still pointing at them
needs `git pull` and `python -m pip install .` first.
