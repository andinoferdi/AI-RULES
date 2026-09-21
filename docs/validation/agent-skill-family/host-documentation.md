# Host documentation verification

Checked 2026-09-21. DOCUMENTATION VERIFIED means the source was read, not that a
local host executed the behavior. Paths below are skill roots; append the ID and
SKILL.md. Links refer to first-party product documentation, not search snippets.

| Host/source | Global / project | Discovery, invocation and controls | Refresh / duplicate / symlink limits |
| --- | --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | ~/.agents/skills / .agents/skills | Required name/description; CLI/IDE `$` or `/skills`; description-based implicit selection; optional references/assets/scripts; repository scan from CWD to root. `agents/openai.yaml` can control implicit invocation, but this family adds no host-only policy. | Automatic change detection, restart if missing. Duplicate names can both appear. Symlink folders explicitly supported. |
| [Claude Code](https://code.claude.com/docs/en/skills) | ~/.claude/skills / .claude/skills | `/skill-name` and model selection; description guides matching; supporting files and scripts supported. Invocation controls and tool permissions are separate concepts. These packages define no allowed-tools grants. | SKILL.md watched in existing roots; restart for a newly created root. Enterprise > personal > project for same-name selection, with nested/plugin exceptions. Local symlink targets supported/deduplicated. |
| [OpenCode V2](https://opencode.ai/v2/docs/skills) | ~/.config/opencode/skills / .opencode/skills; .claude/skills and .agents/skills compatible at both scopes | Path defines ID, name is display label. Relevant described skills advertised; native skill tool loads by ID, subject to permission. References/templates/scripts adjacent to SKILL supported; contents loaded on demand. | Later registered source wins; native project and explicit sources can override compatible/global sources. Avoid duplicate IDs. Local refresh and symlink guarantees NOT DOCUMENTED in consulted page. |
| [OpenCode V1](https://opencode.ai/docs/skills/) | Same six native/compatible roots | Requires name/description, folder=name, lowercase hyphenated name 1-64 and description 1-1024 characters. Skill tool/permissions documented. | V1 constraints differ from V2's permissive display metadata; family retains portable V1-compatible metadata. Do not apply V2 precedence as a universal V1 rule. |
| [Antigravity surfaces](https://antigravity.google/docs/skills?tab=ide) | 2.0/IDE ~/.gemini/config/skills; CLI ~/.gemini/antigravity-cli/skills; all use project .agents/skills | Required description, optional name; discovery at conversation start and contextual activation. 2.0 manual slash; CLI converts skills to slash commands; IDE Customizations lists skills and name mention is supported. Optional scripts/resources documented. | IDE also supports legacy ~/.gemini/antigravity/skills; .agent/skills backward compatibility noted. Duplicate precedence, symlink/junction behavior and hot refresh NOT DOCUMENTED in consulted page. |

All four support a SKILL.md-based bundle with supporting resources. Specific
directory labels differ; no evidence requires renaming this family's references/
or assets/. No universal refresh, duplicate precedence or Windows junction claim
is made. Permissions remain host-specific; a skill installation is not task consent.

The older developers.openai.com/codex/skills URL redirects to the current Learn
documentation. OpenCode V1 and V2 are intentionally versioned, not contradictory
universal specifications. [Agent Skills specification](https://agentskills.io/specification)
supports portable name/description bounds; family validation adopts that common
subset rather than pretending every host enforces it identically.

## Provenance check

[Karpathy Guidelines upstream](https://github.com/multica-ai/andrej-karpathy-skills)
describes the four execution principles and declares MIT in its README. A raw
LICENSE endpoint did not provide a readable license file during this check;
the retained attribution is supported by the README, not a new legal conclusion.
Andino's existing note expressly avoids licensing Andino by implication.
Rescue references explicitly label supplied historical field notes as reported
cases rather than current proof. Skripsi history (9c0f0ac, b8fc9ef, 9aa0c8e,
d7490cd, 97b5207) and the existing contract review document a requirements-led
implementation with original methods and no proprietary-module reconstruction.
No new original-authorship guarantee, family license or endorsement is asserted.
