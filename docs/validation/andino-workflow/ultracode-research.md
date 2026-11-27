# Research: how Claude Code ultracode and dynamic workflows work

Search First, Full mode, run inline on 2026-11-27 for the andino-workflow orchestration
change. Question: how do ultracode and the Workflow tool work (activation, limits, cost,
resume, usage-limit behaviour), and which of their patterns raise output quality? Answer
status: **ANSWERED** for the question as asked; cost comparisons stay open (Still unknown).

## Scope searched

- Terms: `Claude Code "ultracode" workflow`; `Claude Code Workflow tool dynamic workflows
  multi-agent orchestration script docs`; `Claude Code ultracode usage limit subagents tokens
  burned`; `Anthropic "multi-agent research system" tokens 15x`.
- Instruments: WebSearch (standard and extended), `curl` for public pages, `gh issue view` for
  the public issue tracker, and the bundled `/workflow-authoring` skill text that Claude Code
  loaded into this session when the request contained the keyword.
- As of 2026-11-27. Every channel returned USEFUL_EVIDENCE.
- Not located within this boundary: an official cross-session resume for workflow runs; an
  official per-workflow token budget default; a measured quality comparison between inline
  self-verification and fresh-context verification.

## Found

1. **Official workflows page** — <https://code.claude.com/docs/en/workflows.md> (read in full,
   Tier 1). Confidence: Established.
   - A workflow is a JavaScript script Claude writes and a runtime executes in the background;
     the script holds the loop, branching and intermediate results, so Claude's context holds
     only the final answer.
   - Opt-in routes: the keyword `ultracode` or "use a workflow" in one typed prompt; the session
     setting `/effort ultracode` ("Claude plans a workflow for each substantive task");
     `claude --effort ultracode` also sets effort to `xhigh`. The keyword is dismissed by
     writing it in backticks, by `Alt+W`, or for every prompt by the **Ultracode keyword
     trigger** setting (`workflowKeywordTriggerEnabled`).
   - With ultracode on, three checks stop applying: the `Large workflow` warning, the
     session's concurrent subagent limit for Agent-tool subagents, and the first-launch
     approval in auto mode. The page says such a session "reaches a session or weekly limit
     sooner".
   - Runtime limits: up to 16 concurrent agents by default, changeable with
     `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` (1–256, v2.1.269+); 4,096 items per
     `parallel()`/`pipeline()` call; 1,000 agents per run; no mid-run user input ("for sign-off
     between stages, run each stage as its own workflow").
   - Resume works inside the same session only. A completed agent returns its saved result;
     the first agent whose prompt changed, and every agent after it, runs again; a **failed**
     agent reruns together with every agent started after it, completed ones included. "In a
     fresh session, Claude has no earlier run to relaunch and starts the workflow over."
   - At a usage limit a run pauses instead of failing only when all of these hold: an
     interactive (or Code tab) session with a claude.ai subscription, `autoContinueAtUsageLimit`
     on, a reset within 24 hours, the app kept open, and fewer than three waits. A weekly
     limit, a background or `-p` session, or a third limit hit makes the agents fail.
   - A stalled agent restarts automatically up to five times; files it changed stay changed
     and its tokens stay counted.
   - Cost guidance: run on a small slice first; a `Large workflow` warning appears past 25
     agents or 1.5M projected tokens (not under ultracode); agents run on the session's model
     unless a stage names another; a size guideline (`small` <5, `medium` <10, `large` <50
     agents) is advice, not a cap.
   - Transfers: phase-per-run sign-off, explicit stop conditions, slice-first piloting,
     honest "unverified" status for claims a verifier could not check. Differs: andino must
     work on hosts without this runtime and must survive a fresh session.

2. **Bundled `/workflow-authoring` skill** — loaded in this session by the keyword (read in
   full, Tier 1: the instruction text Claude Code ships to the model). Confidence: Established
   for what the model is told.
   - Ultracode is a standing opt-in: "author and run a workflow for every substantive task by
     default. The goal is the most exhaustive, correct answer you can produce — token cost is
     not a constraint."
   - Script API: `agent()` (optional `schema`, `model`, `effort`, `isolation: 'worktree'`),
     `pipeline()` as the default, `parallel()` only when a stage needs every earlier result,
     `phase()`, `log()`, nested `workflow()`, and `budget.total/spent()/remaining()` from a
     user's "+500k"-style directive, enforced as a hard ceiling.
   - Quality patterns: adversarial verify (skeptics told to refute, default refuted when
     uncertain), perspective-diverse verify (one lens per verifier), judge panel, loop-until-dry
     (stop after K rounds with nothing new; dedupe against everything seen, not only the
     confirmed list), multi-modal sweep, completeness critic, and "no silent caps: log what was
     dropped".
   - Working method: scout inline first to find the work list, then fan out; one workflow per
     phase with the parent reading results before the next; scale to what the user asked for.
   - Transfers: the patterns and the stop-condition discipline. Differs: the cost stance and
     the default of a workflow for every substantive task.

3. **Launch post** — <https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code>
   (read in full, Tier 1, Anthropic staff). Confidence: Established for the design rationale.
   - One context window that both plans and executes degrades on long, parallel, structured or
     adversarial tasks through three failure modes: **agentic laziness** (declaring done after
     35 of 50 items), **self-preferential bias** (preferring its own findings when asked to
     verify them) and **goal drift** (losing edge-case requirements and "don't do X"
     constraints across turns and compaction).
   - Six composable patterns: classify and route; fan out and synthesize; adversarially verify
     each output; generate then filter by rubric; tournament with pairwise judging
     ("comparative judgment is more reliable than absolute scoring"); loop until a stop
     condition. Also: hypotheses from disjoint evidence facing refuters; quarantine (agents
     that read untrusted content get no privileges); one verifier per rule plus a skeptic.
   - Cautions: workflows "are not needed for every task and may end up using significantly
     more tokens"; "most traditional coding tasks do not need a panel of 5 reviewers";
     "parallelism and specialization have to earn their coordination cost"; a "quick workflow"
     can adversarially review one assumption; a budget can be set in the prompt ("use 10k
     tokens"); workflow files shipped in a skill folder work best as templates, not scripts
     run verbatim.

4. **Subagent page** — <https://code.claude.com/docs/en/sub-agents.md> (read: model, effort and
   concurrency sections; Tier 1). Confidence: Established.
   - Without a per-invocation `model`, a subagent runs on its definition's model, then
     `CLAUDE_CODE_SUBAGENT_MODEL`, then the main conversation's model.
   - Without a per-invocation `effort`, it runs at `CLAUDE_CODE_EFFORT_LEVEL`, the spawner's or
     turn's level, `CLAUDE_CODE_SUBAGENT_EFFORT`, or the session level. `CLAUDE_CODE_EFFORT_LEVEL`
     overrides even the per-invocation parameter.
   - The Agent tool stops at 20 concurrent subagents by default
     (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, v2.1.217+); ultracode sessions are exempt;
     workflow agents follow their own limit; there is no total cap per session.

5. **Costs page** — <https://code.claude.com/docs/en/costs.md> (read: subagent, workflow and
   agent-team sections; Tier 1). Confidence: Established. Every workflow agent sends its own
   requests on top of the main conversation; agent teams use about 7x the tokens of a standard
   session in plan mode; verbose operations (tests, logs, documentation) can go to a subagent so
   only a summary returns to the main context.

6. **Issue anthropics/claude-code#66762**, "Ultracode mode can silently consume an entire
   5-hour usage window on subagent fleets" (read with comments, Tier 2: first-person report on
   the maintainer's tracker). Confidence: Emerging for the numbers (one report; the bot listed
   #66023, #66755 and #64362 as possible duplicates, not read); the mechanism is Established by
   item 1. A Max-plan session ran a 22-agent assessment (~1.7M subagent tokens), a 12-agent and
   a 20-agent adversarial review (~0.9M and ~1.5M): ~4.4M tokens, "background fleets I never
   individually approved". Requested: a confirmation with agent count and token estimate before
   each workflow, a conservative default budget, visible subagent usage, per-task opt-in. Closed
   by the bot as inactive; no maintainer reply.

7. **"How we built our multi-agent research system"** —
   <https://www.anthropic.com/engineering/multi-agent-research-system> (read, Tier 1, vendor
   research on its own product: conflict of interest flagged). Confidence: Established for that
   system. Token usage explained 80% of the variance on BrowseComp; agents use ~4x and
   multi-agent systems ~15x the tokens of chat; economic only when the task's value pays for
   it; domains that need shared context or have many dependencies "are not a good fit", and
   coding has fewer truly parallel parts than research. Each subagent needs "an objective, an
   output format, guidance on the tools and sources to use, and clear task boundaries"; effort
   is scaled by explicit rules (1 agent for fact-finding, 2–4 for comparisons, 10+ only for
   complex research); the lead saves its plan to memory; long runs resume where they failed
   instead of restarting. Transfers: briefs, explicit scaling rules, durable plan, resume.
   Differs: a research product optimised for breadth, not a coding coordinator under plan
   usage limits.

8. **"Don't Build Multi-Agents"** — <https://cognition.ai/blog/dont-build-multi-agents> (read,
   Tier 2/3, vendor opinion from a competitor: conflict of interest flagged). Confidence:
   Emerging. Share full context and traces; "actions carry implicit decisions, and conflicting
   decisions carry bad results"; default to a single-threaded linear agent. Transfers: inline
   by default, one writer per area, parent-owned integration.

9. Third-party explainers (inventivehq.com, vibecodingacademy.ai, skills-hub.ai,
   developersdigest.tech, toolcolumn.com, bitsminds.com, aiweekly.co) — snippets only, Tier
   3/4. Not used for any finding.

## Contradictions

- Effort under ultracode — third-party posts call ultracode an "xHigh-effort mode" vs the
  official page: `/effort ultracode` keeps the session's level since v2.1.284 (it set `xhigh`
  before), while `claude --effort ultracode` still sets `xhigh`. The difference is the version
  and the activation route.
- Resume — the launch post says resuming the session lets a workflow "pick up where it left
  off" vs the workflows page: only the same session (`claude --resume`) or a cloud session
  keeps saved results; a fresh session starts over. Both hold once "resuming the session" is
  read as the same session.

## Verdict or Answer

Research-only answer, with the implementation direction it supports:

- Ultracode's quality comes from moving the plan into code and from verification patterns run
  in fresh contexts: it counters agentic laziness with explicit work lists and loop-until-dry,
  self-preferential bias with independent refuters, and goal drift with small focused agents
  (Established, items 1–3).
- Its costs come from its defaults, not its patterns: a workflow for every substantive task,
  "token cost is not a constraint", up to 16 concurrent and 1,000 agents per run, the session
  model for every agent, and three safety checks switched off (Established, items 1–2, 4; the
  real-world burn is Emerging, item 6).
- Its progress survives a pause only inside the same session, and a failed agent reruns every
  later agent; at a weekly limit or in a fresh session the run starts over (Established, item 1).
  This matches the owner's report that work is lost when usage runs out.
- Independent sources agree that multi-agent gains are largest on broad, parallel research and
  smallest on coupled coding work, at roughly 15x the tokens (Established for Anthropic's
  system, item 7; Emerging, item 8).
- Inference (from items 1–3 and 7): a coordinator can take most of the quality without most of
  the cost by keeping inline work as the default, applying the patterns inline where the check
  is grounded in external evidence (a test run, a primary source, a reproduction), reserving
  fresh-context agents for judgement-only checks of consequential claims, and writing every
  finished unit to a durable checkpoint so a new session continues from it.
- Implementation direction: **EXTEND** the Claude Code Workflow tool as an optional engine
  inside andino's approval envelope (concurrency set to 3, explicit model and effort per stage,
  results written to the checkpoint); **COMPOSE** the host-neutral path from andino's existing
  members (search-first Full mode, code-review, debugging, doubt-driven-development, council,
  verification) plus the inline patterns above. Adopting ultracode as-is is ruled out because
  its defaults would carry the opposite of the task's purpose (stop condition 4): bounded cost
  and cross-session continuity.

Status: ANSWERED.

## Still unknown

- The real token cost of an andino-orchestrated task against ultracode on the same task: needs
  a measured run of both arms (the agreed trial compares the current and candidate andino only).
- Whether `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` still applies while ultracode is on: the
  page exempts only the Agent-tool limit, so inference says yes; a local run would settle it.
- How much inline refutation recovers of a fresh-context verifier's accuracy: no source located
  measures it; the trial's precision score is the nearest local evidence.
- Workflow-style engines on Codex, OpenCode and Antigravity: not searched; the delegation host
  map keeps them unmeasured.
