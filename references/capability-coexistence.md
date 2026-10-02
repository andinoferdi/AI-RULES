# Capability coexistence and provenance

Andino is the sole selector and lifecycle owner. A methodology skill, an MCP
instrument and local verification may complement one another when each answers a
distinct actual need. Availability is not a reason to load a second discipline.
Project constraints and explicit user choices precede generic specialist defaults.

## Deterministic identity resolution

1. Resolve the actual host catalog entry, path/server, permissions and exposed
   provider/source. Treat a bare name as an identifier, not proof of provenance.
2. Honor the explicitly requested or project-configured provider/path first.
3. Otherwise resolve equivalent same-provider copies: applicable project-local
   selection, host's declared authoritative skill root, then another accessible
   copy with matching identity/content. Record the actual selected path. Never
   silently choose a different provider by directory order.
4. For competing providers without a project choice, use the documented default:
   Superpowers for `test-driven-development`, `systematic-debugging`,
   `verification-before-completion`, `brainstorming`, `writing-plans`,
   `requesting-code-review`, `receiving-code-review`, `dispatching-parallel-agents`,
   `using-git-worktrees` and `finishing-a-development-branch`; Agent Skills for its
   named engineering categories. Agent Skills TDD may be installed as
   `agent-skills-test-driven-development` or `test-driven-development`; aliases
   never erase the provider distinction.
5. If the preferred provider is unavailable, use one identifiable permitted
   equivalent and record the fallback/provider. Do not load both competing
   implementations. If provenance cannot be determined, record UNKNOWN and use
   native/project discipline instead of inventing a provider; ask only when the
   unresolved provider changes acceptance materially.

These are behavioral selection rules, not a claim of universal host precedence
or enforcement. Respect explicit-only invocation restrictions; a readable path is
not permission to bypass them. Evidence records include the resolved ID, provider
(or UNKNOWN), path/server/version when exposed and observed invocation/result.

## Family boundaries

| Overlap | Decision |
| --- | --- |
| Superpowers / Agent Skills | Load relevant individual discipline, never `using-superpowers` or `using-agent-skills` as a second router. Existing Andino plan/checkpoint remains authoritative. Specialist planning templates and completion options yield to the current owner/scope. |
| Ponytail / code-simplification | Prefer Ponytail for prospective dependency/abstraction over-build risk; Agent Skills code-simplification for behavior-preserving cleanup of existing code. One discipline for the same concern. Ponytail's upstream broad coding/persistence defaults do not make it active in every Andino task. |
| Anti-Slop / UI/UX / Taste | Apply only relevant quality concern to the accepted direction. Core Anti-Slop does not activate all subskills. Functional accessibility, correctness and explicit design constraints win over style preferences. |
| UI/UX / Taste | Preserve [the accepted UI policy](ui-coexistence.md): explicit single-skill choice stands, both only when both add value/requested, one design direction and existing stack/token source. |
| Graphify / native references | Simple bounded lookup uses native symbol/reference search. Graph query is useful for unresolved complex relationships; verify freshness and actual tool semantics. No automatic generation or delegation. |
| Playwright / DevTools | One browser surface for reproduction. Add DevTools only for distinct console/network/trace diagnosis; do not repeat the same browser loop. |
| Draw.io / StarUML | Choose requested artifact semantics: general editable diagram versus formal UML/model. Do not automatically invoke both. |
| Native Git / Git MCP | Native Git when sufficient; MCP when native unavailable/inadequate or host mandates MCP. Neither interface changes mutation authority. |
| Future overlapping capabilities | Compare purpose, artifact, current evidence, provenance and permissions; explicit choice first, minimum sufficient identifiable implementation next. Record material selection reason and fallback. |

Independent worker/agent concurrency needs actual independent scopes and applicable
user/host authorization. No specialist's broad delegation, full-scan or install
default overrides Andino's current-need boundaries. Specialist use never grants
consent to commit, push, deploy, publish, write live data or mutate another process.
