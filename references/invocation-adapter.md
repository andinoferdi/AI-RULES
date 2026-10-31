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

For Andino task selection, resolve applicable methods through relevant entries of
the index before optional external discovery, following [dispatch](method-dispatch.md).
An explicit native provider is resolved directly, not replaced by a source alias.
Load selected current work guides before Focus. Explicit native provider choices,
required domain/research supports and their invocation controls remain authoritative.
Communication activation never proves that a work method was selected or applied.
After loading, follow the selected method's complete procedure and required
resources; wrapper loading alone cannot stand in for its deliverable. This applies
to members, siblings and installed external skills under the same real controls.

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

## Andino internal methods

Once Andino is legitimately ACTIVE, resolve a relevant canonical ID or source-name
alias in the [internal index](internal-method-index.md). Confirm the bundled
`skills/<id>/GUIDE.md` and needed local resources are present and permitted; read
only those selected resources. Each member also has a native `andino-<id>` SKILL.md
entrypoint; its GUIDE.md is the canonical procedure, not a separate agent/tool or
an upstream provider invocation. Do not call a fictitious universal method loader, require an
upstream installation, or claim native Superpowers/Agent Skills/Matt invocation.

A guide read establishes ACTIVE; USED also needs a relevant action/output. Name
lookup alone establishes DISCOVERED. Missing/denied guide or tool is UNAVAILABLE;
an irrelevant guide is NOT_NEEDED. Respect restrictions on the family, individual
method/resource and actual action. No alternate-source bypass for a denied resource.
Reading an internal research guide never bypasses required Search First activation;
generic engineering methods do not replace domain owners. Explicit native sibling
requests still follow their actual host invocation controls above.

Real delegation tools are host-conditional. Parallel implementation requires at least
two independent tasks, benefit, authority and disjoint file scopes; at most three concurrently active direct children,
no nested spawning, no concurrent shared writes. Parent inspects artifacts and
reruns relevant checks. Sequential fallback is valid; do not imitate absent agents.

Independent review can justify a single child; parallel implementation still needs
independent scopes. Select inline, independent parallel or scoped implementer/reviewer
execution using the [delegation method](../skills/delegation/GUIDE.md). Discover actual
model and reasoning controls before using them. Respect a supported user selection;
otherwise choose the least costly adequate supported setting when selection is
authorized, or retain host defaults and report unknown controls honestly. Consider brief size,
retries, review and integration overhead along with capability fit. No model names,
prices or fixed escalation policy are portable defaults; claim savings only with
measured evidence. A missing model selector does not make delegation itself unavailable.

## Three.js family and bundled methods

Resolve `threejs-skills` as one installed native skill and invoke it using this
host's actual mechanism. An inventory/source directory is only DISCOVERED, not
an installation or invocation. Once the family is AVAILABLE and INVOKABLE, load
its root SKILL.md and only selected `skills/<method-id>/GUIDE.md` resources through
permitted resource reads. The methods are internal documents, not separately
registered native skills. A guide read proves method activation; USED also needs
meaningful application/evidence. Family invocation does not imply all45 methods
are active, nor does an absent `$threejs-shaders` registration make its bundled
guide unavailable. Honor explicit relevant method names in the prompt.

No alternate-source fallback for a denied family or guide; report UNAVAILABLE
and use sufficient native/project reasoning without claiming restricted method
use. Missing guide content likewise stays unavailable. Reassess selection on
changed needs/resume and retain Andino's one plan. This contract creates no new
host tool, install permission, router loop or second lifecycle.
