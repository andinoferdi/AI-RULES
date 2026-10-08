# Focus integration

## Objective and acceptance
Adapt i-have-adhd into the native `focus` distribution; automatically load it with
Andino, expose standalone invocation, add copyable `X. Focus` to WebBased, and
verify setup/install/update plus communication cases without losing accuracy.

## CURRENT STATE
Publication authorized on 2026-10-08; CI repair and release verification in progress. Live host behavior is not claimed. Main initially cb5e2e1; andino-workflow 52ceaae;
WebBased 89c8ffc. Existing untracked i-have-adhd/ and tests/images/ are preserved.

## CURRENT PHASE
Publishing — repair Linux CI, verify, commit main and push runtime branches before main.

## Decisions
- Follow branch-per-skill distribution; no second installer or routing system.
- Main owns installer/evals. Runtime edits live in attached worktrees:
  C:/Users/Lenovo/.codex/worktrees/focus-skill/AI-RULES (focus),
  C:/Users/Lenovo/.codex/worktrees/focus-workflow/AI-RULES (andino-workflow),
  C:/Users/Lenovo/.codex/worktrees/focus-webbased/AI-RULES (WebBased).
- Use existing catalog requires for installation. Andino loads focus through its
  existing host activation contract once per valid context; no copied prompt body.
- Keep higher instructions, A. PRIORITAS, full technical evidence and requested
  long output. Language examples inform style only, not facts or assumptions.
- User approved local commits on focus, andino-workflow and WebBased after
  verification; explicitly no push. Main changes remain uncommitted. Release pins
  now point to local runtime commits; remote publication remains pending.

## EVIDENCE
- Read installed andino-workflow SKILL.md, routing, invocation, execution-plan and
  anti-loop references; applied lifecycle and native inspection.
- Read upstream source SKILL.md and MIT notice (Ayoub Ghriss, 2026).
- Inspected WebBased README A, project chat-rules and both language references.
  README is directly copyable rule distribution; no generator in branch tree.
- Installer Resolver already expands requires; LatestSources fetches complete
  branch roots. Host invocation registration is generic across skill identities.
- Test-driven-development activated from installed skill for installer regression.

## Verification plan
Regression: dependency selection, standalone focus, install on supported hosts,
repeat/update and preservation, package validation, full existing unittest suite.
Behavior: short answer, debugging uncertainty, coding completion, long explanation;
distinguish manual review from live fresh-host evidence.

## NEXT ACTION
Run regression and full suite, then push focus, andino-workflow, WebBased and main.
Verify remote commit IDs and the GitHub Actions run for the published main commit.

## Progress
- Added Focus runtime and MIT notice, obligatory Andino entry activation, routing
  contract, WebBased copyable X rule and MIT notice; source clone left intact.
- Existing setup requires mechanism plus all profiles include Focus; standalone
  selection remains independent. Release manifest pins actual local runtime commits.
- Snapshot-based setup passed all five host targets, command registration,
  standalone update, repeat NO_OP and preservation of unrelated skills.
- Baseline regression failures exposed fixture assumptions (one dependency-free
  skill / three total skills); updated fixtures, counts and selection expectations.
- New registry entry was caught by the capability schema validator, then corrected
  to the repository's 15-field contract. Validator now passes 56 contracts.
- Manual communication examples are recorded separately; no live model or host
  loading claim is inferred from authored examples.

## Final verification
- 131 unittest tests passed, zero failures/errors, using this checkout's src and
  actual edited runtime snapshots for Focus setup tests.
- Four runtime packages and four eval schemas passed metadata/link validation.
- 56 capability contracts and 34 capability eval schemas passed.
- WebBased has one copyable X. Focus block; upstream MIT text matches both copies.
- Source clone remains clean and untouched. Main user untracked images preserved.
- See ../../validation/focus/verification.json and communication-review.md.
- Live autonomous activation on each host, chatbot behavior and standalone EXE build
  were not run. Manual examples are not independent behavioral proof.

## Changed files
- focus branch: SKILL.md, README.md, references/license.md.
- andino-workflow branch: SKILL.md, README.md, references/routing.md,
  references/capability-registry.md.
- WebBased branch: README.md, FOCUS-LICENSE.md.
- main: README.md; catalog/data/capabilities.json, profiles/data/profiles.json,
  release/data/release_manifest.json under src/ai_rules; .github workflow;
  scripts/validate_skills.py and validate_andino_capabilities.py;
  evals/focus.json and evals/andino-workflow.json; tests/installer/test_focus.py,
  test_live_updates.py, test_resolver_reconciliation.py, test_interactive_setup.py;
  this checkpoint and docs/validation/focus evidence.

## Publication follow-up (2026-10-08)
- User explicitly authorized push and updating main/setup/README; this supersedes
  the earlier no-push boundary. Main changes may be committed for publication.
- Resumed from checkpoint and fetched origin; main has no divergence.
- systematic-debugging activated for CI failure. Run 37735339272 failed on Linux
  because invocation.py accessed Windows-only stat.IO_REPARSE_TAG_MOUNT_POINT.
- Added an executable setup regression simulating absent Windows stat constants;
  observed failure before adding the platform guard. Existing Windows junction
  test remains in place.
- README now documents the normal remote Focus setup flow and all four skills.

## Publication verification
- 132 tests passed on Windows, including the missing-Windows-constant regression.
- Skill validator: four packages and four eval schemas PASS. Capability schemas
  and skripsi traceability checks PASS. git diff --check PASS.
- Runtime branches focus, andino-workflow and WebBased pushed atomically.
- Actual GitHub-source setup of Minimal and standalone Focus passed in disposable
  projects; second installs were NO_OP. See remote-setup.json.
- Main publication is prepared; next action is push main and observe its CI run.
