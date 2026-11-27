# andino-workflow orchestration design

Status: draft for the owner's approval. Date: 2026-11-27.

## Intent

The owner wants andino-workflow to work like Claude Code's ultracode ("dynamic workflow paling
gila yang pernah saya coba") but with its own workflow, keeping the ten anti-loop guards and
staying compatible with the workflow's own references, its 32 members, sibling skills, external
skills and installed MCP servers. Ultracode's two weaknesses must not come along: it starts many
subagents, and when usage runs out the subagents stop and the progress is wasted.

- Outcome: the coordinator gains its own loop for multi-unit work, inline by default, so large
  audits, sweeps, migrations and multi-source research get ultracode-style coverage and checking.
- User: the owner, on Claude Code, Codex, OpenCode and Antigravity, usually together with
  skill-maker, brainstorming, search-first and focus.
- Why now: the members already beat comparable public skills; the coordinator still loses to
  ultracode on big tasks (owner's report; no transcript available).
- Success: on the frozen trial the candidate scores at least as high as the current coordinator
  on every criterion, a one-line fix costs no more than 1.25 times as much, and finished units
  survive a usage limit or a new session.
- Constraint: inline first, zero subagents by default, at most 3 running at once with approval;
  the ten guards; host neutrality; members unchanged; PR to `main` with green CI.
- Out of scope: rewriting members, shipping JavaScript workflow templates, a new member skill,
  an ultracode arm in the trial, changing the owner's host settings.
- Anti-goal: simple tasks get slower, longer or costlier; the loop becomes ceremony on every
  task; any path to unapproved agents or more than three at once.

## Scope

- Goals:
  1. Multi-unit work runs an explicit loop: work list, units, refutation, a second sweep by a
     different method until a round adds nothing, then a coverage report with the stop reason.
  2. Finished units are written to the existing checkpoint in batches; resume reopens only the
     units whose inputs changed.
  3. Independence where self-checking is weakest: judgment-only checks of consequential findings
     may go to fresh-context agents (approved, at most 3); on Claude Code the Workflow tool may be
     the engine under the same envelope.
  4. Ultracode's cost defaults are named and excluded; a host opt-in (ultracode keyword or mode)
     never counts as agent approval.
  5. Small fixes from the review: guard 10's approval wording matches delegation and council,
     the installed `rea` MCP gets a registry entry, Claude Code's concurrency controls are
     documented in delegation's host notes.
- Out of scope: see Intent.
- Anti-goals: see Intent.

## Constraints

- Owner decisions of 2026-11-27 (chat, "Ya, semua"): lean default; Workflow tool only as an
  engine under the envelope; council run; two-arm trial; coordinator-only scope with my calls;
  one design approval before planning, then planning, execution, commit and push without stops.
- Tests pin text the change touches: `references/anti-loop.md` keeps rows 1-10 and the phrases
  `at most twice with backoff`, `permission or daily-quota failures unchanged`,
  `never claim already-injected definitions were unloaded`,
  `Required code, specs and plans remain complete`, `no nested spawning` and
  `turn incomplete work into a DONE claim` (`tests/test_andino_thin_coordinator.py`); SKILL.md
  keeps `## Select work methods first` before `## Communication support` and its links to
  `references/internal-method-index.md` and `references/method-dispatch.md`
  (`tests/test_andino_reliability.py`).
- Evidence: [research report](../validation/andino-workflow/ultracode-research.md), council
  verdict below, [baseline scores](../validation/andino-workflow/orchestration-scores.md).

## Approaches considered

The council (5 advisors sonnet/medium, 3 reviewers sonnet/low) weighed four options.

| Option | Trade-off | Council |
| --- | --- | --- |
| 1. Targeted fixes only | Cheapest; leaves the coordinator without a loop and the end-only checkpoint unaddressed | Contrarian's pick; ranked last or second-last by every reviewer: 33 of 34 on a fixture too small to show the failure modes does not prove there is no gap |
| 2. Orchestration reference, host-neutral | Targets the observed misses (no stop reason or second sweep, checkpoint written once at the end) without ultracode's cost model; risk: a reference can be skipped and inline refutation may recover less than a fresh verifier | First Principles, Outsider and Executor; first and second in every reviewer ranking |
| 3. Option 2 plus shipped JS templates | Mechanical loops on Claude Code; host-specific, untestable on the other hosts, a verbatim template could exceed 3 agents | Expansionist; reviewers: the "mechanical" claim overreaches because templates stay model-driven |
| 4. New member `andino-orchestration` | Fits the member model; adds routing surface and overlaps delegation and search-first | No advisor |

Chosen: Option 2 with Option 1's fixes in the same change. The reviewers' blind spots shape the
design: the minimal loop lives in always-loaded SKILL.md so a skipped reference cannot remove it;
SKILL.md growth is capped; the agent form is bounded by measured start-up cost; the Workflow
tool's same-session resume is backed by the checkpoint; a larger fixture is proposed (Decisions).

## Design

### 1. SKILL.md: a short always-loaded trigger

New section `## Orchestrate multi-unit work` between `## Coordinate progress and evidence` and
`## Bounded execution`, at most 12 lines. It fires when the work is many similar units (route
handlers, files, call sites, findings, sources, tests) or asks for "all"/"every", or resumes such
work, and states the minimum loop in one paragraph: write the work list with its count before
the first unit; do units inline, writing finished results to the checkpoint in batches; try to
clear each consequential finding with the check that would refute it; sweep again by a
different method until a round adds nothing (three rounds at most); finish with coverage (done of
total, not covered, unverified) and the stop reason; agents only through the delegation envelope.
A single-unit task skips it. It links `references/orchestration.md` for the details.
`## Bounded execution` gains one clause: a host opt-in such as the ultracode keyword or mode is
not approval.

### 2. `references/orchestration.md` (new, host-neutral)

Sections, each short and ordered for an agent that reads it once:

1. **When it applies.** Multi-unit triggers versus direct work (one file, one fix, one question).
2. **The loop**, each step with a Done when:
   1. Scout inline with bounded reads (entry points, registrations, imports) and write the work
      list with a count and an input identity per unit (commit, file hash or source URL). The
      work list goes into the checkpoint (a LITE plan is enough) when the work has more than ten
      units, may outlast the session, or the owner asked for continuity; otherwise the final
      report carries it.
   2. Pick the rigor level from what can be observed: **Quick** (work list, one refutation per
      finding against the rule, coverage line), **Standard** (plus the second sweep and the dry
      round), **Thorough** (plus fresh-context checks of judgment-only consequential findings and,
      for wide option spaces, pairwise judging). Standard is the default; Quick when the work
      list has ten units or fewer and nothing consequential is at stake. Thorough needs the
      owner's words ("thorough", "every", "sedalam-dalamnya", an audit before a release) or a
      consequence (security, money, data loss, migration); agents in Thorough still need the
      envelope.
   3. Work the units inline; pilot a small slice first when the cost per unit is unknown. Write
      finished units to the checkpoint in batches (per file or module, or about every ten units)
      and before any long step, adding the write to a tool call already being made where possible:
      each extra turn re-reads the whole context.
   4. Refute: for each consequential finding (one the report will present as a defect, a risk or
      a fact the owner will act on) name the checks that could clear it and look for them;
      prefer external evidence (a test run, a reproduction, a primary source). Outcomes are
      CONFIRMED, REFUTED or UNVERIFIED; a check that could not run is UNVERIFIED, never REFUTED or
      CONFIRMED.
   5. Sweep again by a different method (by entry point or registration, by content pattern, by
      structure or imports, by history or diff, by data flow, by relationship graph when graphify
      is available). Dedupe against everything already seen, not only confirmed findings. Stop at
      the first round that adds nothing new, or after three rounds, and say which.
   6. Report: findings with their outcome and evidence, then one coverage line (done of total, not
      covered and why, UNVERIFIED items) and the stop reason. Any cap (top-N, sampling, skipped
      folders) is written there: no silent caps.
3. **Pattern catalog.** One row per pattern: what it counters (agentic laziness,
   self-preferential bias, goal drift), inline form, agent form, stop condition, the guard it
   serves. Patterns: work list and coverage; refutation; second sweep and dry round;
   lens-diverse checks (one lens per check instead of identical voters); pairwise judging of
   options (user-owned decisions stay with brainstorming or council); slice first; quarantine
   (units that read untrusted content return data, the parent acts); one phase per run with the
   parent reading results before the next.
4. **Unit ledger.** The checkpoint table (unit, input identity, status, result, evidence),
   written in batches; on resume, compare identities and reopen only changed units.
5. **Agents and engines.** When an agent beats inline work (independence for judgment-only
   checks, breadth beyond one context, parallel read-only research); the cost estimate shown in
   the envelope (agents x measured start-up, about 60k-84k tokens each on Claude Code, plus
   work); the parent writes each returned unit to the ledger after every wave. On Claude Code the
   Workflow tool may run approved units: concurrency held to 3 by a small pool in the script or by
   `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` (a settings change the owner approves), `model`
   and `effort` on every `agent()` call, `schema` returns, scout inline first, one run per
   phase, small runs because a failed agent reruns every agent after it, and the ledger as the
   only cross-session record because workflow resume is same-session only.
6. **Composition.** Research units go to search-first (Full mode owns angles, the adversarial
   angle and waves); code findings to code-review; failure hypotheses to debugging; assumptions to
   doubt-driven-development; panels to council; agents to delegation; one browser surface per
   question; MCP servers as instruments through the registry. The loop coordinates; it does not
   restate their methods.
7. **What ultracode does that andino does not**: a workflow for every task, "token cost is not a
   constraint", 16-way concurrency, agents on the session's strongest model by default, approval
   checks switched off.
8. **Guard mapping.** How the loop respects each of the ten guards, guard by guard.

### 3. Existing references

- `anti-loop.md`: guard 1 adds that every discovery or fix loop states its exit before it starts
  (work list done, a round with nothing new, or a round cap); guard 10's approval sentence becomes
  "before a run, state every wave's count, tier and effort; one approval covers the waves it
  lists; a host opt-in is not approval"; the limits section adds that results held only in
  context are lost at a usage limit. All pinned phrases stay.
- `execution-plan.md` and `execution-plan-template.md`: an optional Unit ledger section and its
  batch-write rule.
- `handoff.md`: on resume with a unit ledger, compare each unit's recorded identity with the
  current one and reopen only changed units.
- `capability-coexistence.md`: rows for "Workflow tool / ultracode / andino orchestration" and
  "search-first Full mode / orchestration".
- `capability-registry.md`: a `rea` MCP entry; the Workflow tool as a permission-gated native
  facility.
- `README.md` (skill): a short orchestration paragraph.

### 4. Delegation resources (member text unchanged)

- `resources/host-cost-calibration.md`: Claude Code notes for the Workflow tool (environment
  variables and their minimum versions, the size guideline, what ultracode switches off, resume
  and usage-limit behaviour, writing `ultracode` in backticks to mention it without starting a
  workflow) and this trial's start-up measurements.
- `resources/contract.md`: a workflow tool must also hold the 3-agent limit in its script or
  host setting.

### 5. Repository

- `tests/test_andino_orchestration.py`: preservation checks for the SKILL.md section and link,
  the loop's steps and outcome labels, the coverage line, the round cap, batch writes, the
  ultracode exclusions, the guard mapping 1-10 and the new guard 10 wording.
- Evals and inventories the change affects, updated in the same commits.
- `docs/DECISIONS.md` entry; trial record `docs/validation/andino-workflow/orchestration-trial.md`
  and the candidate column in `orchestration-scores.md`.

Failure handling: if the reference is skipped, SKILL.md still carries the minimum loop; if an
agent fails, stops or hits a usage limit, its unit stays open in the ledger and the owner is
asked before any relaunch; if a check cannot run, the finding is UNVERIFIED.

## Decisions

- Confirmed by the owner: the six decisions of 2026-11-27 (see Constraints).
- My calls, with reasons:
  - Option 2 plus Option 1's fixes: council verdict, three advisors and every reviewer.
  - Minimum loop in SKILL.md, details in the reference: a skipped reference cannot remove it.
  - Batch writes (per file or module, about every ten units) instead of one write per unit: an
    extra turn costs a full context re-read; batches keep the loss at a limit to one batch.
  - Three outcome labels, with UNVERIFIED kept apart: Claude Code's deep-research workflow reports
    unchecked claims as unverified rather than refuted.
  - Round cap of three: matches search-first's follow-up waves.
  - Standard as the default rigor; Quick for ten units or fewer with nothing consequential; the
    work list checkpointed above ten units or when the work may outlast the session: these were
    the fresh-reader check's open points (done by me, reading only this document, since no
    agent was approved for it).
  - No JS templates, no new member, no settings changes made for the owner.
- Open:
  1. **S4, a larger audit.** Every reviewer noted the trial cannot show gains at this size. S4
     would freeze, before any candidate text, an audit of about 50 handlers in 12 modules with
     about 14 planted gaps and as many traps, scored like S1. Cost: 2 more runners (baseline and
     candidate, sonnet/medium), about 1-2M tokens processed each, mostly cache reads (estimate
     from S1's 543k for 18 handlers). It blocks nothing else; without it, gains at scale stay
     NOT_VERIFIED.
  2. **Approval of this design.** Blocks planning and every edit to the skill.

## Acceptance checks

1. Trial gate: on S1-S3 (and S4 if approved), the candidate scores at least as high as the
   current arm on every criterion, and K1 holds (candidate S3 tokens at most 1.25x current).
2. `python scripts/ci_checks.py --group skills` passes on the branch.
3. `references/anti-loop.md` still has rows 1-10 and every pinned phrase; the new preservation
   test passes.
4. SKILL.md grows by at most 15 lines; in the candidate S3 run the trace shows at most two
   guidance files read.
5. Every new link resolves from the installed skill location (skill validator).
6. Discovery probes from the rubric recorded as probed or NOT RUN.

## Left to the builder

Exact wording, table layouts, section order inside `orchestration.md`, test names, and whether
the Workflow-tool pool snippet is shown in the reference or in delegation's host notes.

## Terms

- Unit: one item of multi-unit work (a handler, file, call site, finding, source).
- Work list: every unit with a count, written before the first unit.
- Unit ledger: the checkpoint table of units, identities, results and evidence.
- Rigor level: Quick, Standard or Thorough, chosen from observable triggers.
- Sweep and dry round: a pass by one search method; a round that adds nothing new.
- Outcomes: CONFIRMED, REFUTED, UNVERIFIED.
- Envelope, checkpoint: as defined by delegation and the execution-plan reference.
