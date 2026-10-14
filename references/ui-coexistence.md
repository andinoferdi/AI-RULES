## Taste and Impeccable: user integration policy

The independent skill IDs are `design-taste-frontend` (Taste) and `impeccable`.
An existing `taste-skill` alias means the former; it is not a second design
workflow. Honor an explicit request for either alone. When both are requested
or routed, load both actual SKILL.md files before applying them. Do not
require a wrapper, invoke unrelated skills, or run two workflow owners.
`ui-ux-pro-max` is not part of this setup; do not reference or reinstall it.
This policy resolves overlaps between these skills and takes precedence over
generic skill defaults, including older router guidance on this pairing.

Priority: user requirements and project instructions/accepted brand and design
system come first; preserve correctness, accessibility, usable focus/semantics,
reduced-motion support and existing functionality. Within those constraints:

- Taste generates: visual character, composition, typography, coherent icon
  family, motion intent and its audit-first redesign process in its documented
  scope.
- Impeccable evaluates and refines: PRODUCT.md and DESIGN.md context
  (`init`, `document`), then `critique`, `audit`, `polish`, `harden`, `typeset`,
  `layout`, `colorize`, `animate`, `adapt` as the finding requires, and the
  deterministic `detect` scan. It also owns dashboards, data tables and
  multi-step product UI, which Taste's scope excludes.

Both cover visual design; this is a conflict-resolution policy, not a claim that
either lacks a capability.

Pipeline for new or redesigned UI: (1) read the brief and existing UI; (2) one
design direction and explicit dial values recorded in DESIGN.md (never inferred
from adjectives like "minimal" or "professional"; restraint must be tied to a
stated concept); (3) Taste generates; (4) Impeccable critiques and polishes in
at least one full round, more for landing or marketing pages; (5) render
screenshots at 360, 768 and 1440 px and compare with the direction before DONE.
Reconcile results with Taste on aesthetic defaults; for functional UX and
accessibility use outcome-based guidance and validate the result. Resolve a
remaining material conflict explicitly in the design read, not by last-loaded
skill order. Keep one stack, component system, icon family and token source;
use the project's stack, not either skill's default. Keep existing icons;
otherwise follow Taste's permitted family rather than automatically importing
Lucide. Do not use a font only because it is a common default; record the reason
for the typeface. Motion recommendations never override reduced-motion or
usability requirements.

Shared files: one DESIGN.md per project is the single design-direction file;
Impeccable's PRODUCT.md holds durable product facts. Read both before
generating. Never overwrite accepted design tokens or files merely to reconcile
the two skills; record one agreed direction in the project's existing design
documentation.

Impeccable's hooks and telemetry: hooks only report findings. Telemetry stays
off (`IMPECCABLE_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`). A clean `detect` run is not
proof of visual or accessibility quality.

For fidelity-only cloning (`clone-website`) preserve the reference; redesign
requires a request, after which Taste and Impeccable apply. An explicit
single-skill request does not automatically activate the other.
