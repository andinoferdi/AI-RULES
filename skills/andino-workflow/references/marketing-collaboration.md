# Marketing, LinkedIn and logo collaboration

Applies when Marketing Skills, LinkedIn Skills or the Logo Design skill are installed alongside Andino. Andino
retains lifecycle, progress and capability selection; this reference supplies
domain handoffs. Use only the specialists needed for the current deliverable.
Explicit user/provider choices and project constraints take precedence.

## Context shared between specialists

Read the current project's `.agents/product-marketing.md` when present. Fall back
to `.claude/product-marketing.md`, then `product-marketing-context.md` in either
directory. Keep product/client context in its owning project. If essential context
is missing, use `product-marketing` for an authorized context document or ask only
for facts needed by the current output; a simple post need not create a document.

For LinkedIn, also read the existing bundle's shared voice/approval rules at
the installed `linkedin-skills` bundle's `SKILL.md` (for example `~/.local/share/agent-skill-bundles/linkedin-skills/SKILL.md` when it was installed there).
Its `references/voice-profile.md` and `references/story-bank.md` hold personal voice
and source stories. Reuse them only for the matching person. Pass relevant product
facts, audience, objective, evidence and voice to the selected specialist; preserve
the existing profile and Story Bank rather than copying them into each host.

## Logo and identity handoff

For logo or identity work, give `logo-design` the relevant product context: exact name, audience, positioning, brand attributes, competitors and existing design constraints. Read an existing project `.agents/brand-identity.md` and approved brand guidelines/assets when present. Use `product-marketing` only when foundational positioning needs its own deliverable; pass available facts directly for a bounded logo request.

Follow the selected logo skill's full process and concept checkpoint. After the user selects a direction and requests the kit, produce the agreed assets and usage guidelines. Keep product/client assets in their project, using its existing asset convention or `brand/` when none exists. For a requested multi-skill handoff, record a compact `.agents/brand-identity.md` pointing to the approved SVG/PNG files and guidelines, with chosen colours, typography, clear space and permitted variants. Identify concepts as unapproved until selected; distinguish specified fonts from outlined finished artwork.

For subsequent marketing, LinkedIn visual or frontend work, reuse the approved identity and pass only relevant context to the specialist. `logo-design` owns logos, marks, lockups, favicons and identity guidelines. `image` owns campaign imagery and mockups that use the approved mark; `linkedin-profile-optimizer` owns LinkedIn profile/banner requirements; the selected frontend skill owns page layout and implementation. A text-only post does not require redesigning the logo. An explicit rebrand request returns identity decisions to `logo-design`. Use the reference-logo library for study, as described in `TRADEMARKS.md`.

## Choose ownership by the requested output

| Current need | Selected specialist |
| --- | --- |
| Product positioning, audience and shared product facts | `product-marketing` |
| Logo, brand mark, identity guidelines, lockups, favicon or app icon | `logo-design`; use existing product and approved identity context |
| Content topics, pillars and cross-channel editorial direction | `content-strategy` |
| LinkedIn-only calendar, post, comment, reply, profile or repurposing | Matching `linkedin-*` skill from the host catalog |
| New LinkedIn post | `linkedin-post-writer`; use `linkedin-humanizer` for its existing review step |
| LinkedIn plan | `linkedin-content-planner` |
| Voice audit of an existing LinkedIn draft | `linkedin-humanizer` |
| Missing personal material for a LinkedIn draft | `linkedin-interviewer` |
| Social platforms other than LinkedIn, or a cross-platform plan | `social`; hand its LinkedIn deliverable to the matching `linkedin-*` specialist |
| Website copy or conversion diagnosis | `copywriting`, `copy-editing` or `cro` |
| Other marketing needs | Matching installed Marketing Skills entry, loaded on demand |

An explicit request for `social` on LinkedIn uses that selected provider. Otherwise
the more specific LinkedIn skill owns its final output; do not run two competing
drafting procedures for the same post. Marketing Skills' `marketing-council` is
distinct from the installed general `council`; respect the user's selected provider
and the host's actual authority for delegation.

Focus shapes surrounding communication. Search First owns research when external
claims need evidence. Natural Writing or antislop-copywriting refines the relevant
prose only when its distinct concern applies; preserve the selected channel's voice
and required depth. Existing frontend skills own visual design and browser checks;
marketing supplies positioning, copy and conversion goals.

## Resources, actions and observable handoff

The complete, pinned marketing source and tools live in the installed `marketingskills`
bundle (for example `~/.local/share/agent-skill-bundles/marketingskills`).
Resolve upstream `tools/...` commands there, not in an unrelated user's project.
Read and check a helper before running it. Installed skill-local `references/`
and `scripts/` paths remain relative to the selected skill directory.

Installation supplies playbooks, not connected accounts or action authority.
Retain LinkedIn's existing local draft-only setting. Account connections, paid
services, fetching account data, publishing, sending messages, starting campaigns
and recurring jobs require a separate explicit request covering that action.
Use pasted material/manual drafts when optional connections are absent.

Example: for an authorized launch plan plus three LinkedIn posts, read the project's
product context, use `launch` for the launch plan, pass its audience/message/evidence
to `linkedin-post-writer`, and apply its existing humanizer review. Deliver the plan
and three reviewed drafts. Record the context and specialists actually used, any
missing evidence, and whether the deliverable is a draft or an executed action.

Example: for a logo plus a LinkedIn launch draft, pass the product context to `logo-design`, show its concept checkpoint, then use the selected approved direction for the requested kit and hand the agreed identity/message to `linkedin-post-writer`. Its humanizer review remains applicable. Deliver the assets and draft; publication is a separate action.

Invoke through the host's actual skill controls. Denied/manual-only capabilities
stay restricted. File availability and this routing guidance do not prove runtime
discovery or future automatic selection; verify those claims on the actual host.
