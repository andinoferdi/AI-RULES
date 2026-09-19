# Host adapters

The canonical Andino source is `skills/andino-workflow/`. Run from this repository:

```powershell
python -X utf8 scripts/sync-workflow.py
python -X utf8 scripts/sync-workflow.py --check
```

The script derives home dynamically, generates identical copies with hash manifests,
refuses to overwrite local drift, and backs up replaced generated installs outside Git.
Edit the canonical source only. `--home <temporary-directory>` supports isolated tests.

## Managed multi-skill sync

`scripts/sync-skills.py` manages an explicit set: `andino-workflow` and
`ai-codebase-rescue`. It copies each complete canonical tree, including references,
to the same four host roots shown below, with the skill name as the directory leaf.
It does not discover or install other folders under `skills/`.

```powershell
python -X utf8 scripts/sync-skills.py --home <temporary-directory>
python -X utf8 scripts/sync-skills.py --home <temporary-directory> --check
python -X utf8 scripts/sync-skills.py --home <temporary-directory> --skill ai-codebase-rescue
```

Repeat `--skill` to select multiple managed names; omission selects both. Omitting
`--home` targets the current user's home, so use an explicit temporary home for
validation. `sync-workflow.py` retains its existing Andino-only CLI and delegates
to the same mechanics; it does not install rescue implicitly.

Each tree has `.andino-generated.json` with `source` and relative file hashes.
Check mode writes nothing and fails on missing/different content. Identical content
is left untouched even without a marker; this does not adopt an unmanaged tree.
Different content is replaced only if current hashes match its existing marker;
unmanaged or locally edited trees are refused. Previous trees go to the selected
home's `.andino/backups/sync/previous-*/<skill-name>`, not the repository. Only skill
trees are backed up, not host/provider configurations. Processing is sequential,
not a transaction across hosts/skills: a later refusal can follow earlier successes.
Reconcile the refused tree before rerunning; do not discard local edits blindly.

This controls repository-managed distribution only; it does not alter native host
invocation policy or prove live/implicit skill selection.

For an existing installation, `scripts/harden-runtime.py` (Python with PyYAML)
repoints the managed global UI reference to the installed skill and applies the
accepted core-worker controls. It backs up changes outside Git and does not modify
MCPs or install capabilities. Claude user-only skills and OpenCode V1 denied skills
are not hidden-but-model-callable: respect restrictions and request the user's
native invocation/permission adjustment when necessary. Antigravity currently uses
a soft description guard only. See [acceptance audit](../docs/acceptance-audit.md).

| Host | Generated skill path relative to home | Invocation / instructions |
| --- | --- | --- |
| Codex | `.agents/skills/andino-workflow` | `$andino-workflow`; user `.codex/AGENTS.md`, project `AGENTS.md` |
| Claude Code | `.claude/skills/andino-workflow` | `/andino-workflow`; user/project `CLAUDE.md` |
| OpenCode | `.config/opencode/skills/andino-workflow` | native skill tool or `/andino-workflow` command; global config `AGENTS.md`, project `AGENTS.md` |
| Antigravity | `.gemini/config/skills/andino-workflow` | request `andino-workflow` through Skills; global `.gemini/GEMINI.md` |

Each host can independently lead the same ticket. These adapters express host mechanics,
not permanent roles. OpenCode also discovers `.agents/skills`; its explicit global copy
is an intentional identical generated install, not a separately maintained source.

## Project installation

Use [alignment](<../Project Markdown Alignment Prompt.md>) on demand. Copy the rules directory
to the project's chosen rules location and merge its thin core into native instructions.
For Claude, `CLAUDE.md` may import `@AGENTS.md`; for hosts without that import behavior,
wire their native instruction mechanism. Resolve all relative references at the target.
Do not overwrite an accepted project contract or make a portable template contain a username.

## Manual capabilities and MCPs

Manual means available when requested, not automatically selected on every prompt.
Codex supports `agents/openai.yaml` → `policy.allow_implicit_invocation: false`;
Claude supports `disable-model-invocation: true` in skill frontmatter.
OpenCode V1 does not document V2 `opencode/autoinvoke`; use explicit commands that
load the preserved local skill, with skill-tool permissions hiding overlapping entries.
Antigravity manuals may live outside automatic discovery and be loaded by their recorded path.
The machine-local `~/.andino/skill-catalog.json` records sources, disposition and paths.

Direct MCP configurations remain locally recoverable. Codex uses `enabled`; OpenCode
V1 uses `mcp.<name>.enabled`; Antigravity uses `disabled`. Claude's global optional
servers are stored in `~/.andino/mcp/claude-manual.json`, outside Git, and restored by
the local MCP helper when needed. Plugin-provided tools are a separate catalog layer.
Do not copy credential-bearing configs into a project or this repository.

Use the machine-local helper through `python ~/.andino/mcp-toggle.py HOST NAME on|off`.
Names and available hosts are listed with `--list`. It backs up the changed config,
preserves unrelated entries and never authenticates or starts a remote action.
Reload the affected host after changes. Enable only the relevant server for the task,
then disable it when that task is finished; this is explicit toggling, not lazy startup.

## Limits and updates

Skills are behavioral policies, not runtime loop detectors. Supported step/timeout controls
are documented in [audit](../docs/audit.md); no invented host settings are used.
After vendor updates, review overlapping triggers and sync deliberately. Do not edit plugin
caches to defeat bootstrap: disable the plugin and use selected standalone skill copies.
The installed OpenCode version determines V1/V2 schema; never migrate by reading latest
V2 examples alone. Generated files and backup paths are local, not repository secrets.
