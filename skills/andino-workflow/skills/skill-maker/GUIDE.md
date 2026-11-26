# Prove a skill changes what agents do before it ships

Internal method ID: `andino-skill-maker` (aliases: `skill-maker`, `writing-skills`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

A skill exists to change what an agent does. Writing one is test-driven work on a document:
see what agents do without it, write the smallest text that changes that, and check the change
on the same cases. Most requests for a skill turn out to be partly something else, such as a
fact for the project instructions or a rule a linter already enforces, so sorting comes before
writing. The deliverable is the skill (or the reason none was made), a table of what was kept
out of it and where that now lives, test scenarios with PASS and FAIL lines, and an evaluation
record a reviewer can rerun.

## Trigger and non-trigger

Use when:

- creating a new skill, runbook or repeatable agent procedure;
- revising a skill after agents ignored it, misused it or produced the wrong output with it;
- turning observed agent failures, incident excerpts or bad samples into guidance;
- checking that a skill changes agent behaviour before it ships, or that it still loads when it
  should and stays quiet when it should not.

Do not select for:

- Wording, structure, pointers or the description of an agent-read document with no behaviour
  to test: `agent-document-authoring`. This skill applies those levers to a skill's text.
- Facts, preferences and conventions (a deploy region, who reviews what, a branch naming rule): they go in the project
  instructions (`AGENTS.md`, `CLAUDE.md`), which load every session.
- A rule a linter, formatter, type checker, schema or CI job can enforce: put it in that tool.
- A one-off problem, a problem nobody has observed yet, or a story of how a session went.

## Select a resource, not a second lifecycle

Load only the resource the current gate names. It runs inside this procedure and current
authority; it starts no second plan.

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| Choosing the form for each failure, closing loopholes, excuse tables, red flags, routing items out of the skill | [failure forms](resources/failure-forms.md) | Every row already has a form and a destination |
| Writing scenarios per skill type, pressure combinations, PASS/FAIL lines, wording micro-tests | [test scenarios](resources/test-scenarios.md) | The scenarios file already exists and covers every skill row |
| The evaluation record, the self-review label, the runbook, packaging and the deployment checklist | [evaluation contract](resources/contract.md) | Nothing to evaluate or package yet |
| The description, trigger and near-miss probes, keywords, naming | [discovery](resources/discovery.md) | The description and probes are settled |
| Degrees of freedom, context cost, examples, flowcharts, anti-patterns | [authoring craft](resources/authoring-craft.md) | The skill text is settled |
| A repository with no skill conventions: skill and runbook templates | [templates](resources/templates.md) | The repository defines its own layout |
| One remedial case end to end with every artifact | [worked example](resources/worked-example.md) | The gates are already clear |

## Prerequisites

- Read the repository's skill conventions (a skills README, the instructions file, two existing
  skills) and follow them over any template here.
- Read all the evidence: transcripts, incident notes, bad samples, reviewer comments. For a
  revision, read the current skill and every file it links.
- Find out whether you can start a fresh agent (a subagent or a separate session) and whether
  the user allows it. Usually you cannot; the gates below have a path for that.

## Procedure

Pick the mode first. **Remedial**: an observed failure exists, including a skill agents misused;
the observed failures are the baseline. **Greenfield**: a new capability with no failure yet;
declare the invariants the skill must hold (ordering, stop conditions, authority limits, output
contract) and look for the ones an agent without the skill misses.

**Quick path.** When every item in the request is a fact, a preference or a rule a tool already
enforces, run gate 2 only: make the routed changes, create no skill, and reply in a few lines
naming where each item now lives.

Everything else goes through seven gates in order; the report quotes each **Done when** line.

1. **Write the brief.** Name who loads the skill, for which task, and what it must produce.
   Pick one request that must load it and one nearby request that must not; they become the
   discovery probes in gate 7. State the authority limits (what the agent may never do while
   following it). Done when: the brief names the consumer, the task, one request that must load
   the skill, one nearby request that must not, the output the skill must produce and the
   authority limits.
2. **Sort every observed item.** List each failure, excuse, sample defect and requested fact
   from the evidence as a row: the quote, its type and its destination. Types: discipline (the
   agent knew the rule and skipped it), shape (the output has the wrong form), omission (a
   required part is missing), condition (the right action depends on a situation), fact. A row
   goes to the skill only when it needs judgement during a task; send it to a tool when a
   linter, formatter, type checker, schema or CI job can catch it, to the project instructions
   when it is a fact or preference, to "already covered" when a file or tool holds it now, and
   to "nothing" when it does not recur. Check the repository before writing "already covered".
   Pick each skill row's form from [failure forms](resources/failure-forms.md). Done when: every
   failure, excuse, sample defect or requested fact in the evidence has a row with its quote,
   its type and its destination (skill with a form, tooling, project instructions, already
   covered, nothing), and every row that leaves the skill names the file or tool that holds it
   now or the exact proposed home. When no row goes to the skill, take the quick path.
3. **Write the scenarios before the skill text.** Use the format in
   [test scenarios](resources/test-scenarios.md). A discipline scenario replays the evidence: the
   real task, the real files, at least two of the pressures that were present (deadline, sunk
   effort, authority, missing access, fatigue) and a forced choice. A shape scenario gives one
   real input and the output checks. A condition scenario has one case on each side of the
   condition. Done when: a scenarios file exists where the repository keeps evals (otherwise in
   the skill's references folder) with one scenario per skill row type, discipline scenarios
   drawn from the evidence and combining at least two pressures, and every scenario has a PASS
   line and a FAIL line that each name an observable action or output.
4. **Record the baseline.** Run the scenarios on a fresh agent without the skill and, for a
   revision, with the current skill, when you can. In remedial mode the incident excerpts and
   samples are observed baseline evidence: quote them. Write down behaviour that already works
   (a line the samples get right, a step agents never skip); it becomes a regression check.
   Done when: for each scenario the record holds what an agent without the skill (and, for a
   revision, with the current skill) actually did, quoted from a run or from the observed
   incidents, or says NOT RUN with the reason; a predicted baseline is never recorded as observed.
5. **Write the smallest skill that answers the skill rows.** Follow the repository's layout.
   The description says only when to load the skill (see [discovery](resources/discovery.md)).
   Answer each discipline row with a hard rule tied to the action, plus an excuse table using
   the excuses as they were said and the stop signals; each shape row with the ordered output
   parts and a size for each; each omission row with a required slot; each condition row with
   a branch on something the agent can observe. Keep every working behaviour from gate 4. Put
   long material in a linked file. Done when: every skill row maps to a line of the skill in
   the form gate 2 assigned, every behaviour that works today is listed and still present, the
   description says only when to load, the repository's skill conventions are met, and no rule
   carries an escape clause.
6. **Evaluate with the criteria fixed in gate 3.** Run the same scenarios on a fresh agent with
   the candidate, and compare with gate 4. When no fresh agent can run, apply the same PASS/FAIL
   lines yourself: for a revision, write what the current skill and the candidate each lead to
   on the same input and score both; for a new skill, walk each scenario through the candidate
   and name the line that decides it. Label that self-review and write the runbook someone
   else can execute (see [evaluation contract](resources/contract.md)). Done when: the evaluation
   record shows, for each scenario and each arm (no skill, current skill when revising,
   candidate), a result with its evidence; when no second agent can run, it shows your own
   application of the same criteria to the same input, labelled self-review, plus the exact
   prompt and setup someone else can run.
7. **Package and report.** Resolve every link from the location the skill is installed to,
   check that the name matches its folder, and probe the two requests from gate 1 (or record
   them as NOT RUN with the prompts). Close loopholes a run exposed and rerun the scenarios it
   touched. Finish one skill before you start the next. Done when: links resolve from the
   installed location, name and folder agree, the trigger and near-miss requests from gate 1
   are recorded as probed or NOT RUN, and the report lists what changed, what was routed out
   and where, the scenarios path and the evaluation status.

**After a failed evaluation.** Read what the agent did and the words it used. A new excuse goes
into the excuse table and the stop signals; a wrong shape means the recipe is unclear, not that
it needs a prohibition. Change one thing and rerun the scenarios that failed. Stop after three
rounds that bring no new evidence and report the scenario that still fails.

## Rules for every skill

- **Match the form to the failure.** A prohibition with an excuse table fixes discipline; it
  backfires on shape, where an ordered recipe works. A missing part needs a required slot. A
  situational action needs a condition the agent can check.
- **No escape clauses.** "Unless necessary" or "if time permits" reopens every rule. Write a
  real exception as its own condition on something observable.
- **Letter equals spirit.** For a discipline skill, state early that breaking the letter of the
  rule is breaking its spirit, so "I kept the intent" is not a way out.
- **Keep facts and tool-enforced rules out.** A skill loads only when its description matches;
  a fact belongs where every session reads it, and a lint rule belongs in the linter.
- **Preserve what works.** A revision keeps every behaviour the evidence shows working.
- **Report only what ran.** A walkthrough, a metadata check or your own reading is never a
  baseline or a pass. Self-review is labelled as such.
- **One excellent example.** One complete example from a real scenario beats several thin ones.

## Shortcuts that ship untested skills

| Shortcut | Response |
| --- | --- |
| "The skill is obviously clear." | Clear to the author is not clear to an agent under pressure. Write the scenarios and score them. |
| "I'll write the skill first and the tests after." | Text written before the evidence encodes what you guess, not what failed. Gates 2 to 4 come first. |
| "It's only a reference, there is nothing to test." | Test retrieval: can an agent find the right entry and apply it? |
| "I can't start a second agent, so I can't evaluate." | Apply the PASS/FAIL lines yourself, label it self-review, and leave the runbook. |
| "I'll summarise the steps in the description so agents know what it does." | An agent that reads a summary follows the summary. The description says when to load. |
| "A 'never do X' list will fix the long output." | Prohibitions on shape produce more of it. State the parts in order with sizes. |
| "I'll add 'unless necessary' to keep it flexible." | That clause is where every agent will stand. Write the real exception as a condition. |
| "They asked for a skill, so I make one." | Sort first. Facts go in the instructions file; enforced rules stay in their tool. |
| "Lint already catches it, but a reminder can't hurt." | It costs context in every load and teaches agents to trust prose over the tool. Route it out and say where it lives. |
| "I'll do the next skill and verify both together." | Finish the gates for one skill before starting another. |

## Red flags

- A walkthrough or your own reading recorded as a baseline or a pass.
- The description lists the skill's steps.
- A prohibition list used to fix the shape of an output.
- An "unless", "except when" or "if possible" on a rule.
- A fact or a rule a tool enforces copied into a skill.
- A scenario without a PASS line and a FAIL line.
- "Tested" in a report when no run of an agent is shown.
- Three thin examples where one complete one would do.

## Ownership and permission boundary

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its gates, resources and checks; coordinator brevity never shortens them.
`agent-document-authoring` owns wording levers, which this skill applies. Starting evaluation
agents follows `delegation` and needs the user's approval; loading this skill grants no authority
to start agents, install, commit, publish or message anyone.

## Output

- The skill files, or a note that no skill was made and why.
- The routing table from gate 2.
- The scenarios file from gate 3.
- The evaluation record from gates 4 and 6.
- A report in this shape:

```markdown
Changed: <files and what each now does>
Routed out: <item -> where it lives now (file or tool)>
Scenarios: <path>, <count> scenarios
Evaluation: RUN | SELF-REVIEW | NOT RUN — <arms and results, one line each>
Not verified: <what no run has shown yet>
Next check: <the exact prompt or command someone should run first>
```

## Verification

Before you call the skill done:

- [ ] every item in the evidence has a row and a destination, and routed rows name their home;
- [ ] the scenarios were written before the skill text and each has PASS and FAIL lines;
- [ ] the baseline quotes runs or incidents, or says NOT RUN with the reason;
- [ ] every skill row maps to a line of the skill in the assigned form;
- [ ] behaviour that worked before is still present;
- [ ] the description says only when to load, and the trigger and near-miss probes are recorded;
- [ ] the evaluation record has a result per scenario per arm, or self-review plus a runbook;
- [ ] links resolve from the installed location and the report claims nothing that did not run.

## Worked example and anti-pattern

The [worked example](resources/worked-example.md) takes agents that hand-edit generated
protobuf code through all seven gates: the routing table sends one item to a CI check, three
scenarios replay the incidents, and the evaluation is self-review with a runbook.

Anti-pattern: asked to "make a skill so agents stop doing X", the author writes a long skill
with every rule they can think of, folds in a reminder the linter already enforces, reads it
once and reports it as tested.

## Fallback

- **No fresh agent, or the user does not allow one.** This is the common case. Gates 4 and 6 use
  the observed incidents and labelled self-review, and the report carries the runbook.
- **No skill conventions in the repository.** Use [templates](resources/templates.md).
- **No evidence of a failure for a remedial request.** Ask for the transcript or sample; until it
  arrives, treat the request as greenfield and say so.

## Local resources

- [Failure forms](resources/failure-forms.md)
- [Test scenarios](resources/test-scenarios.md)
- [Evaluation contract](resources/contract.md)
- [Discovery](resources/discovery.md)
- [Authoring craft](resources/authoring-craft.md)
- [Templates](resources/templates.md)
- [Worked example](resources/worked-example.md)
- MIT notices: [references/license.md](references/license.md)

## Operational example (offline)

This fixture checks three properties of the gate artifacts: a routing table with no skill row
means no skill, a scenario needs both a PASS and a FAIL line, and a self-review evaluation needs
a runbook. It does not measure how well a model writes skills.

```python andino-operational-example
import os

def needs_skill(rows):
    return any(row["destination"] == "skill" for row in rows)

def scenario_ok(scenario):
    return bool(scenario.get("pass", "").strip()) and bool(scenario.get("fail", "").strip())

def evaluation_ok(record):
    if record["status"] == "SELF-REVIEW":
        return bool(record.get("runbook", "").strip())
    return record["status"] in ("RUN", "NOT RUN")

if __name__ == "__main__":
    facts = [
        {"item": "default deploy region", "destination": "project instructions"},
        {"item": "line length 100", "destination": "already covered"},
    ]
    assert not needs_skill(facts)
    assert needs_skill(facts + [{"item": "hand-edits generated code", "destination": "skill"}])
    assert scenario_ok({"pass": "regenerates from the .proto file", "fail": "edits the generated file"})
    assert not scenario_ok({"pass": "agent complies", "fail": ""})
    assert evaluation_ok({"status": "SELF-REVIEW", "runbook": "replay scenario 1 without the skill"})
    assert not evaluation_ok({"status": "SELF-REVIEW"})
    raise SystemExit(1 if os.environ.get("ANDINO_NEGATIVE") == "1" else 0)
```

## Provenance

Adapted from Jesse Vincent's `writing-skills` (obra/superpowers, path last changed in 2ce8aa1):
test-driven skill writing, the form-to-failure table, loophole closing, per-type tests, pressure
types and wording micro-tests; and from Addy Osmani's `using-agent-skills` (eca51a2) and
`docs/skill-anatomy.md` (c4efec8) in addyosmani/agent-skills: the section anatomy with
rationalisations, red flags and verification, and context efficiency. Both under the MIT license;
notices are in [references/license.md](references/license.md). The two modes, the brief, the
separate discovery, task and packaging checks and the honest status labels come from the
earlier Andino skill; the routing table, the gates and the self-review path are new here. The
comparison trial is recorded in the AI-RULES repository at `docs/validation/skill-maker/trial.md`.
