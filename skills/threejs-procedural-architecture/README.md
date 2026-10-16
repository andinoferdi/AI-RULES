# threejs-procedural-architecture

Build authored procedural buildings and architectural kits in Three.js. Use for massing grammars, exposed-edge analysis, façade bays, profiles, arches, cornices, roofs, ornaments, material-slot mesh compilation, deterministic variants, and procedural city assets.

## Use and boundaries

Read [SKILL.md](SKILL.md) for domain triggers, methods, evidence and exclusions.
This specialist can work alone. With Andino active, return results to its single
plan; Focus controls communication and Search First handles relevant research.
Sibling suggestions are optional, selected by need and host invocation permission.

## Installation and discovery

After the runtime and installer are published:

```sh
ai-rules setup --host codex --capability threejs-procedural-architecture --scope project --project-root . --source latest
ai-rules setup --host codex --profile threejs --scope project --project-root . --source latest
```

Pass `--project-root PATH` for project scope; it is required by the CLI.
Global scope uses `--scope global`. Codex project/global roots are `.agents/skills`;
Claude Code uses `.claude/skills`; OpenCode uses `.agents/skills` for projects and
`~/.config/opencode/skills` globally. Antigravity CLI and IDE use the catalog's
separate roots. These are installer mappings; live execution on each host is
NOT_VERIFIED. Refresh/restart discovery as required by the host. Invoke this exact
name through its permitted mechanism; installation does not prove activation.

## Package and dependencies

Install the whole directory with SKILL.md directly at its root. Preserve all
included references, scripts, examples, agent metadata, assets and license notices.
The skill body describes version-sensitive tools, render backends and optional
services. Installing this package installs no npm dependencies or credentials and
does not authorize paid API calls. No blanket license is inferred from local files.

## Update, conflicts and verification

Use `ai-rules update` with the same host, scope, capability and source selection.
Review modified or unrecognized directories before explicit repair; preserve user
edits and backups. Bundled releases pin commit and subpath; latest resolves the
branch at setup. Do not install a second discoverable copy as a workaround.
Run the main package validator, then an applicable domain behavior check. Positive
smoke: invoke this skill for its stated domain, observe a relevant action and
evidence. Negative smoke: ordinary unrelated frontend work must not select it;
missing/denied siblings require a truthful fallback. File presence alone proves
neither invocation nor rendering quality.

[Family quality contract](https://github.com/andinoferdi/AI-RULES/blob/main/docs/agent-skill-family-standard.md)
