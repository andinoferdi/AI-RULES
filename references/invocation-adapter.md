# Host invocation contract

This is a host-facing behavioral contract, not a fake universal command, a new
executable router or another plan owner. Skills are methodology; MCP tools are
instruments; native facilities are existing local capabilities. They may be used
together only for distinct current needs.

## Evidence states

| State | Evidence required |
| --- | --- |
| DISCOVERED | Identity/contract is known from registry/catalog. |
| AVAILABLE | The host exposes the actual skill/tool/path for this session. |
| INVOKABLE | Native controls allow this agent to load/call it for the task. |
| ACTIVE | Skill instructions were loaded through the permitted host mechanism, or the actual instrument/schema was loaded; retain load evidence. |
| USED | A skill has ACTIVE evidence plus an identifiable task action/result applying its instructions; an instrument has an observed call/result used in the task. |
| UNAVAILABLE | Needed capability is missing, denied, disconnected or otherwise unusable; record the specific boundary. |
| NOT_NEEDED | Known capability adds no value to the current unresolved need. |

These states are conceptual, not a compulsory per-turn transcript. Installation
does not prove activation; activation does not prove use. A successful preflight
proves connectivity, not the requested operation or autonomous routing. Schema
validation, mocked responses and resemblance to a methodology never prove live
use. An error response can establish unavailability, not successful task use.

## Resolve only the selected capability

Use native catalog/tool search/metadata to resolve a relevant entry. Retrieve only
the selected skill's instructions or MCP tool schema, not every full SKILL.md or
tool schema. Resolve actual IDs/provider and collisions using
[coexistence](capability-coexistence.md). A project manual catalog may supply
disposition metadata; query only the requested/selected ID. Refresh on material
version or permission drift. Do not install dependencies merely to fill a registry.

| Host/interface | Supported adaptation and limits |
| --- | --- |
| Codex | Resolve session skill catalog and callable tools/tool search; load actual selected skill through permitted mechanisms. An attached/global folder is not proof the current session exposes it. |
| Claude Code | Respect manual-only/explicit invocation modes and tool search. Do not bypass an explicit-only skill by reading its file with another tool. |
| Antigravity | Use actual scoped skill descriptions/catalog and tool interfaces. Scoped descriptions are behavioral guidance, not a proven hard permission switch. |
| OpenCode | Resolve actual configured permissions and skill/tool catalog. V1 deny controls cannot be reinterpreted as hidden-but-callable capabilities. |
| Other/native MCP clients | Use their real discovery/call mechanism (for example exposed tools/list or tool search), not a made-up shared invocation syntax. |

Host names do not establish availability or parity. For a host that cannot
implicitly invoke a selected explicit-only worker, state the limitation and the
smallest native user invocation needed, continue independent ordinary authorized
work, and do not claim external worker use.

## Activate, use, reroute, release

Before work governed by a selected skill, activate it through the actual permitted
host mechanism. Claude Code uses the Skill tool for model-initiated activation;
OpenCode uses its exposed skill tool. On hosts whose supported mechanism is reading
the selected SKILL.md, that read can establish ACTIVE, but never USED by itself.
Name mentions, remembered instructions, registry reads and source inspection solely
for audit do not establish skill use. File reads must never bypass invocation controls.

A single user invocation of Andino is sufficient entry: after loading, the agent
must activate the selected supporting skills itself when native controls allow it.
Do not require multiple slash commands in one message or invoke Andino recursively.
If a supporting skill is manual-only, denied or absent, record UNAVAILABLE and the
specific boundary; request the smallest separate native user action only if needed.
Parent invocation does not grant permission to invoke restricted children.

Reuse valid activation evidence while the same instructions remain available in
context; do not repeat calls for ceremony. Reload through the permitted mechanism
when content/context changed or activation can no longer be established.
For each required or selected skill, retain actual ID/provider/path, activation
event or tool call, and the task action/result applying it. Use the existing plan
or evaluation record; do not create a second ledger. A self-reported skill list
alone is insufficient. Report an unmet required route even when fallback work
succeeds; never relabel fallback work as use of that skill.

AUTO means clearly relevant read-oriented lookup/normal skill loading can proceed
within existing permission. CONDITIONAL_AUTO means wait for the actual task phase
and evidenced concern (regression, review, simplification, output quality or browser
verification). PERMISSION_GATED means selection is possible, but action authority
depends on requested mutation and consequence. A read tool is not automatically
side-effect free: follow its actual schema, preflight and application behavior.

After loading/calling, use its result as evidence, reassess the unresolved need,
then keep, replace or release the capability. New facts can justify a different
method/instrument. Release means stop calling it and applying irrelevant defaults;
it does not mean uninstalling or pretending the host removed loaded context. Stop
when acceptance is sufficiently grounded; simple tasks with no required route or
explicit specialist choice can use zero specialists.

When unavailable: determine whether a native/local alternative can satisfy the
same need safely, use it and name the fallback, or report the precise remaining
gap and request only material missing access/action. Never imitate a denied
worker's invocation or claim it was used. Anti-loop retry rules still apply.

## Observable validation

When capability use matters to acceptance, record host, actual model when exposed
(otherwise UNKNOWN), Andino commit/content hash, relevant discovered identities,
resolved provider/path/server, selected capability and selection reason, actual
load/call and result, fallback, permission boundary and PASS/FAIL/NOT_VERIFIED.
Evaluate a fresh actor with only raw fixture/request/runtime; keep expected,
forbidden and reviewer decisions hidden. Transport smoke tests and self-reported
selection are insufficient to prove autonomous just-in-time routing. Cross-host
use remains NOT_VERIFIED until actually executed on each claimed host.
