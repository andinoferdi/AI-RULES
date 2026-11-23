# Changing, adding and removing skills

Every first-party skill is a folder in `skills/<id>/` on `main`. Merging a PR to
`main` is the release. See [ADR 0002](../adr/0002-skills-live-on-main.md).

## Skill layout

Every first-party skill has the same shell, so readers and agents find the same
things in the same places. `tests/test_skill_layout.py` checks it.

```
skills/<id>/
  SKILL.md           required: the runtime contract the agent loads
  README.md          required: the human page, with the headings below
  references/        supporting documents the agent reads on demand
    legal/           required: every license notice and provenance record
  scripts/           optional: runnable helpers the skill calls
  assets/            optional: templates copied into the user's work
  skills/<method>/   optional: internal methods of a family skill
```

- No other top-level entries. Add `scripts/`, `assets/` or `skills/` only when
  the skill uses them; never create an empty folder.
- `references/legal/license.md` is the MIT notice for AI-RULES-authored content.
  A third-party source gets `references/legal/<source>-license.md`. Absorbed
  material is recorded in `references/legal/provenance.json` or `provenance.md`.
  No license or provenance file lives anywhere else in the skill's top level.
- Internal method folders (`skills/<method>/`) keep their family's own layout,
  checked by the family validator.
- `SKILL.md` frontmatter holds only `name` and `description`. Its body headings
  stay specific to the method.

`README.md` uses these level-2 headings in this order. Skill-specific detail
goes in level-3 headings under **What It Does** or **How It Works**.

| Heading | Content |
|---|---|
| `# <Skill name>` | One sentence on what the skill does, then a short paragraph on why. |
| `## What It Does` | The core idea: the modes, decisions, stages or catalog. |
| `## When to Use` | A table with the columns `Use for` and `Do not use for`. |
| `## Quick Start` | `### Installation` (the `ai-rules setup` command, then a collapsed manual install that copies `skills/<id>/` from `main`) and `### Usage` (example invocations). |
| `## How It Works` | Optional: contracts, protocols and run details. |
| `## Works With Other Skills` | Who owns what when other skills are active. |
| `## Files` | `SKILL.md`, the main references and the `references/legal/` files. |
| `## License` | The license line, linking `references/legal/license.md`. |

Do not separate sections with `---` rules.

## Changing a skill

1. Branch from `origin/main` and edit `skills/<id>/`.
2. Run `ai-rules setup` from the clone to try it (it reads `skills/` from disk).
3. In the same commit, update whatever the change affects: inventories
   (`src/ai_rules/verification/data/threejs_inventory.json`), counts or allow-lists in
   `scripts/validate_skills.py`, `evals/<id>.json`, and the tests in `tests/`.
4. Run `python scripts/ci_checks.py --group skills`, then open a PR.

## Adding a skill

One PR:

1. `skills/<id>/` with `SKILL.md` (`name: <id>`) and `README.md`.
2. `src/ai_rules/catalog/data/capabilities.json`: copy an existing first-party
   entry; set `id`, and `source` to `branch` `main`, `subpath` `skills/<id>`.
3. `src/ai_rules/profiles/data/profiles.json`: add the id to `everything` and to
   any profile that should install it.
4. `scripts/validate_skills.py`: add the id to `RUNTIME_SKILLS` (a family with
   internal methods gets its own validator instead, like `threejs-skills`).
5. `evals/<id>.json`: at least one `behavior` and one `negative-trigger` case.
6. `docs/ci-coverage.md` coverage map and the README tables.

Done when `python -m unittest tests/test_skill_registry_consistency.py` and
`python scripts/ci_checks.py` pass.

## Removing a skill

Reverse the six steps in one PR, and delete tests and fixtures that exist only
for that skill (`tests/test_<id>.py`, `tests/installer/test_<id>.py`,
`evals/<id>*.json`). Installed copies stay on users' machines; setup no longer
offers the skill. Done under the same two checks.
