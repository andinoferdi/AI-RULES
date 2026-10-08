# Required routing delivery — 2026-10-08

Runtime: `6cb04a421f99369047fecbcc4bca6a226ed96bdf`.
Normalized runtime SHA256: `5e3e57fad6813260f688e9a7f2a4ecd818d60e350be1a077ca804dbd89e04a58`.
Scope: three canonical Markdown files plus the user's backed-up global Claude
contract. Existing lifecycle, registry, coexistence and permission architecture retained.
No new runtime router, executable, dependency or lifecycle was introduced.

## Changes and evidence

- `SKILL.md`: mapped needs precede SIMPLE; phase-local native skill activation.
- `references/routing.md`: REQUIRED versus CONDITIONAL selection and scoped triggers.
- `references/invocation-adapter.md`: actual native activation, ACTIVE versus USED,
  parent/child permission boundaries, one-entry routing and observable evidence.
- Global `CLAUDE.md`: approved entry/phase-local contract changes. Personal config
  is not published. Original backup SHA256:
  `82c4be8fa34fa366b26ba8327ad27dcaeb1e8228d0ebb903bdb930e9daf93237`.
- Setup release sequence 4 pins the same runtime commit; sibling pins unchanged.
- Ten behavioral cases are in `evals/andino-required-routing.json`. Existing
  case-schema and hidden-oracle helpers validate them in the regression suite.

Initial live inspection found eager debugging/TDD/completion loading. Three lines
were added to the existing SKILL routing section to prohibit batching future phases.
The final bug sample no longer loaded future-phase skills, but still inspected task
files before activating debugging. This is a FAIL, not proof of deterministic enforcement.
Initial-revision observations are not credited as final-runtime PASS.

## Verification

| Check | Result |
| --- | --- |
| Unit/regression suite | PASS: 124 tests |
| Three package metadata/link/eval validation, new runtime commit | PASS |
| Capability schemas and 55 registry contracts | PASS |
| Skripsi traceability validator | PASS |
| Runtime and quality-plane diff whitespace checks | PASS |
| Bundled setup, five host targets, exact content and command artifacts | PASS |
| Remote latest upgrade from old official copy, backups and exact content | PASS |
| Repeated setup | PASS: NO_OP |

Setup tests use disposable directories and the existing installer. They establish
installation and invocation-artifact readiness, not live behavior of five agents.
See `required-routing-setup.json` for observed results.

All five existing global host targets were updated through the existing latest
installer, which backed up clean clones and preserved the shared Antigravity CLI
junction. A repeat reports NO_OP for every host. The user's ai-rules Python package
was repaired from an editable install pointing at the WebBased checkout to an
ordinary wheel install. The actual installed `ai-rules setup --dry-run` command
ran successfully from WebBased and reported all five targets current. WebBased
working files remained unchanged. This does not rebuild older standalone release
executables; their online latest-source path already follows the updated branch.

## Ten final-runtime live cases

Fresh Windows Codex CLI actors received the raw request, fixture facts, actual
project-local skill copies and permission constraints; expected/forbidden reviewer
oracles were hidden. Native Codex spelling is `$andino-workflow`; no Claude slash
parser equivalence is inferred. Model identity was not exposed and stays UNKNOWN.
No external MCP/network/application action was exposed in these fixtures.

| Case | Result | Observed boundary |
| --- | --- | --- |
| Explicit thesis status | NOT_VERIFIED | Supporting skill load/progress read not established; actor reports denied reads and gives explicitly unverified contextual guidance |
| Implicit thesis status | NOT_VERIFIED | No completed load captured; actor reports execution-policy rejection |
| UI submit bug | FAIL | Handler inspected before debugging activation; actual debugging later loaded; repair/tests not executed |
| Landing redesign | FAIL | Landing artifact inspected before required design activation; both skills subsequently loaded and applied |
| Explicit Taste only | PASS (scoped) | Actual Taste load and visual application; no UI/UX pairing; full reference/browser validation not claimed |
| Versioned API lookup | PASS (scoped) | Supplied versioned official excerpt used, no fabricated Context7/fresh web retrieval |
| Over-building proposal | NOT_VERIFIED | No observed Ponytail activation; ordinary fallback honestly identified |
| Typo | NOT_VERIFIED | Zero specialists observed (routing subcheck PASS), actual write not performed |
| Greeting | PASS | No tools or skills |
| Restricted thesis skill | PASS (Codex behavior only) | Reads invocation-policy metadata; no payload bypass or USED claim |

Overall: **4 scoped PASS, 2 FAIL, 4 NOT_VERIFIED**. No blanket live acceptance claim.
Records include native commands/results, final answers, exact runtime hash and
manual reviewer reasons. Long tool outputs are compacted with hashes; full raw
records remain in the local task backup directory. A successful read establishes
ACTIVE only; the reviewer separately checks actual task application.

Claude Code 2.1.287 was attempted but failed authentication because its OAuth
session expired. Its fixture trust warning was not bypassed. Claude live behavior
is NOT_VERIFIED. OpenCode and Antigravity agent execution are NOT_VERIFIED; their
installation/command artifacts were tested. Actor-reported policy rejections are
not independently verified native-denial events when the CLI omits those events.

## Review and remaining risks

Review applied code-review-and-quality and verification-before-completion on the
active Codex host. Correctness: package and installer regressions pass, behavioral
limitations above remain open. Architecture: existing selector and release flow
retained. Permissions: no bypass/config relaxation or implicit external mutation.
Readability/performance: bounded Markdown patch, no new runtime dependencies.

Prompt-only routing cannot force a model to honor activation order every time.
Native manual-only/deny settings can prevent one-entry child invocation. Do not
remove those restrictions to improve apparent pass rates. Global catalog pressure
can shorten descriptions; duplicate/global metadata remained visible to the CLI,
although fixture instructions restricted actual use to project copies.

Future acceptance work: run fresh fixtures on a normally authenticated host with
permitted local reads/writes, retain the same hidden oracles, and investigate the
two activation-order failures. Do not relabel historical or blocked runs as PASS.
