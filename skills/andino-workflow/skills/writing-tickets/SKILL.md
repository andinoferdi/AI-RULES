---
name: andino-writing-tickets
description: Use when a plan, spec, issue or discussion must become tracker tickets (issues, sub-issues or a local ticket folder) that agents or people pick up later, including bringing an existing ticket set up to date after its source changed and sequencing a wide refactor. Operates under Andino Workflow governance.
---

# Turn accepted work into tickets a fresh agent can build

Internal method ID: `andino-writing-tickets` (aliases: `writing-tickets`, `to-tickets`, `to-issues`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

Break a plan, spec, issue or conversation into **tracer-bullet** tickets on the project's
tracker: thin vertical slices, each declaring the tickets that **block** it. Whoever picks a
ticket up (an agent in a fresh session, days later, or a person) has only the ticket and the
code. Everything you learned here that they need goes into the ticket; everything that will go
stale (file paths, line numbers, today's structure) stays out. The deliverable is the approved
ticket set on the tracker, a clean graph check and a report naming the **frontier**: the
tickets whose blockers are all done.

## Trigger and non-trigger

Use when:

- the user asks to turn a plan, spec, issue or discussion into tickets, issues or sub-issues;
- an `andino-planning` plan must go onto a tracker for others to pick up;
- an existing ticket set must follow a changed spec, plan or decision;
- a wide refactor (a rename or retype across the codebase) must be sequenced as tickets.

Do not select for:

- What to build or why is still open: `brainstorming`.
- A plan to execute in this session, with exact files and signatures: `planning`.
- Incoming issues or pull requests to sort, or one item's brief: `issue-triage`.
- Decision questions in a decision-frontier map, which that map also calls tickets: `brainstorming`.
- Building a ticket: `plan-execution` or `tdd`.
- A change that fits one ticket: write that one ticket with the template; skip the breakdown.

## Select a resource, not a second lifecycle

Load only the resource the current step names. It runs inside this procedure and current
authority; it starts no second plan.

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| Writing tickets: templates, acceptance criteria, sizing, the reader check | [ticket template](resources/ticket-template.md) | Never before step 6 |
| Tracker configuration, local folders, GitHub, reruns without duplicates | [publishing](resources/publishing.md) | Never before step 6 |
| One request end to end, with a rerun | [worked example](resources/worked-example.md) | The steps are already clear |

The full expand-contract procedure for wide refactors is `skills/planning/resources/dependency-slicing/guide.md`
in the installed `andino-workflow` package; step 4 below carries the rule itself.

## Prerequisites

- Read the source in full: the plan or spec, an issue's body and every comment, or the
  conversation so far. A spec path or issue reference given as an argument is fetched first.
- Read the tracker configuration (often `docs/agents/issue-tracker.md`, `triage-labels.json` or
  the `AGENTS.md` section that names the tracker): where tickets live, numbering, label strings,
  a required first line for AI-written text. With none, use local files in
  `.scratch/<feature>/issues/` and say so.
- Read the glossary (`CONTEXT.md`, `GLOSSARY.md`) and the ADRs in the area you will touch.
- Note the authority you have. A local ticket folder in the repository may be written once the
  user approves the breakdown. A remote tracker (GitHub, Linear, Jira) is written only when the
  user's own words authorize writing to it; naming the tracker is not that.

## Procedure

Seven steps, in order. Each ends with a **Done when** line.

1. **Gather what is decided.** List every requirement and decision from the source with where it
   came from, what is explicitly out of scope, and every open decision with its owner ("the product
   lead decides", "ops to answer"). Look for an existing ticket set for this work (the feature
   folder, a parent issue's sub-issues, a title or label search). Done when every requirement,
   exclusion and open decision is listed with its origin, and existing tickets are listed with
   number, title and status, or "none found" with where you looked.
2. **Explore the code.** Learn how the area works today, in the glossary's words, within its ADRs.
   Look for **prefactoring**: make the change easy, then make the easy change. Logic the new work
   would copy again, or a missing seam, becomes a prefactor ticket. Check claims in the source
   against the code ("the check is duplicated") and note any mismatch. Done when you can name the
   area each requirement touches and each prefactor with the tickets it unblocks.
3. **Draft the tracer bullets.** Each ticket cuts a narrow but complete path through every layer
   (storage, logic, interface, tests) and is demoable or verifiable on its own. Size it for one
   fresh context: one behaviour a person or test can observe; split a ticket whose title needs
   "and" or that touches more than two areas. Prefactor tickets come first. Give each ticket its
   **blocking edges**: only tickets that genuinely gate it; a ticket with none starts at once,
   and independent tickets stay parallel. Mark each ticket **AFK** (an agent can finish it
   alone) or **HITL** (it needs a person's decision or review). Done when every requirement maps
   to exactly one ticket, no ticket is a single layer, and every edge names a real gate.
4. **Route the special cases.** Done when each case below that applies is handled:
   - *Open decisions.* Each becomes a HITL ticket labelled ready-for-human that names the owner
     and the question, and blocks the tickets that need the answer; tickets that do not need it
     neither build nor forbid either answer. A decision dropped from the tracker is lost.
   - *Wide refactor.* One mechanical change whose **blast radius** breaks many call sites at once
     cannot land as one green slice. Sequence it as **expand-contract**: an expand ticket adds the
     new form beside the old; migrate tickets, batched by area and sized by blast radius, are each
     blocked by the expand; a contract ticket removes the old form, blocked by every migrate
     batch. Stored data and outside readers (files on disk, exported formats, public flags) get
     their own compatibility line or ticket. When batches cannot stay green alone, they share an
     integration branch and all block a final integrate-and-verify ticket.
   - *A plan as source.* Recut horizontal plan tasks (schema, logic, CLI, docs) into vertical
     slices. Turn file paths, line numbers and signatures into behaviour and interface
     descriptions. Carry the plan's blocked items as HITL tickets.
   - *A rerun.* Match each requirement to an existing ticket before drafting a new one. Existing
     tickets keep their numbers; a done ticket is never edited, and behaviour that changes after
     it becomes a new ticket; an open ticket is updated in place with a dated note; new tickets
     number after the highest existing one.
5. **Quiz the user.** Show the breakdown as a numbered list: per ticket its title, AFK or HITL,
   what blocks it and the end-to-end behaviour it delivers; then the open decisions held for
   their owners and what stays out of scope. Ask whether the granularity is right (too coarse,
   too fine), whether each edge is a real gate, and what to merge or split. Iterate until the
   user approves. Done when the user approved the breakdown they saw, and any remote tracker
   write has its own authorization in their words.
6. **Write, check and publish.** Write each ticket with the [ticket template](resources/ticket-template.md),
   numbered blockers first, then publish per [publishing](resources/publishing.md). Apply the
   reader check to every ticket: reading only the ticket and the code, could a capable agent
   start, and know when it is done, without asking? Run the graph check on the local files (for
   a remote tracker, on the drafts before publishing):
   `python <installed andino-workflow>/skills/writing-tickets/scripts/ticket_graph.py <issues-folder>`.
   Fix every finding and rerun. Done when every ticket passes the reader check, the graph check
   prints `OK <n> tickets`, and every ticket exists on the tracker with its edges and label.
7. **Report.** Done when the user has the report in the Output shape: tickets created, changed
   and left alone, the frontier, the HITL tickets with their owners, and the graph check line.

## Rules for every ticket set

### Tracer bullets

A vertical slice proves the whole path early; a horizontal one proves nothing until the last
layer lands. Every ticket ends in something observable: a command and its output, a stored
state, a rendered page, a passing end-to-end test. Prefactoring comes before the features it
eases. Wide refactors are the one exception, sequenced as expand-contract.

### Durable text

A ticket may wait for weeks while the code moves. Describe behaviour, interfaces, types,
commands and data shapes; leave out file paths, line numbers and code. The one exception: a
prototype snippet that encodes a decision more precisely than prose (a state machine, a schema,
a type shape), trimmed to its decision-rich lines and marked as coming from a prototype.

### Acceptance an agent can check

Each criterion names an input or action and the observable result: "`<command>` on the sample
data prints X", "a file without the new key still loads". Cover the edge the requirement implies
(empty, boundary, refusal). "Works correctly" and "tests pass" check nothing.

### Words and edges

Use the glossary's terms and respect its _Avoid_ list. An edge is a real gate: the dependent
ticket cannot be built or verified until the blocker is done. Convenience order is not an edge.

### Authority

Write only where the user authorized: the local folder after approval of the breakdown, a remote
tracker only on the user's explicit go-ahead for it. Never close, retitle or edit a parent issue
or a ticket marked done. Source code, specs, plans and notes stay unchanged: tickets describe
work, they do not do it.

## Shortcuts that break tickets

| Shortcut | What to do instead |
| --- | --- |
| "One ticket per layer is cleaner." | Each layer alone proves nothing. Cut through every layer, thin. |
| "The plan already has tasks; one ticket each." | Plan tasks are often horizontal and full of paths. Recut into slices and translate paths into behaviour. |
| "The owner hasn't decided, so I'll leave it out." | Put it on the tracker as a HITL ticket naming the owner, or it is lost. |
| "I'll pick a sensible default for the open question." | The owner decides. The ticket says neither answer is built. |
| "The file path helps the agent find it." | It goes stale. Name the behaviour, command or type; the agent explores. |
| "Rename everywhere in one ticket." | It cannot land green. Expand, migrate in batches, contract. |
| "The spec changed; I'll regenerate the tickets." | Match existing tickets first. Keep numbers, never edit done tickets, add after the highest. |
| "They said the breakdown looks good, so I'll publish to GitHub." | Approval of the breakdown covers the local folder. A remote write needs their go-ahead for it. |
| "The edges look right." | Run the graph check and read its output. |

## Red flags

- A ticket whose title names a layer ("database changes", "API endpoints") with no observable result.
- A file path, line number or pasted code in a ticket body outside a marked prototype snippet.
- Acceptance criteria without an input and an expected result.
- An open decision missing from the tracker, or decided inside a ticket.
- A second ticket for behaviour an existing ticket already covers.
- An edit to a ticket marked done, or to the parent issue.
- Tickets published before the user approved the breakdown.
- A report with no frontier, or a graph check that was not run.

## Ownership and permission boundary

Andino coordinates selection, shared progress and final status from evidence; this skill owns
its procedure, resources and checks, which coordinator brevity never truncates. Loading it grants
no authority: it writes tickets only where the user authorized and changes no source, spec, plan
or note, and it authorizes no commit, push, merge, installation or external message. Without a
remote write authorization, the tickets stay as local drafts and the report says they are not
published.

## Output

Tickets on the tracker in the [ticket template](resources/ticket-template.md), then this report:

```text
Tickets: <folder or tracker> - created <NN title, ...>; changed <NN: what changed>; left alone <NN>
Frontier (can start now): <NN title, ...>
Waiting on people: <NN question - owner>, or "none"
Out of scope: <item - where it was decided>
Graph check: <the line the check printed>
Not published: <remote tracker and why>, or "none"
```

## Verification

Before you call the tickets done, confirm:

- [ ] every requirement maps to exactly one ticket, and every open decision to a HITL ticket;
- [ ] every ticket is a vertical slice with an observable result, prefactors first;
- [ ] every acceptance criterion names an input and an expected result;
- [ ] no ticket body carries a file path, line number or code outside a marked prototype snippet;
- [ ] labels, folder, numbering and the AI first line follow the tracker configuration;
- [ ] on a rerun, no duplicates, numbers kept, done tickets untouched;
- [ ] the graph check printed `OK <n> tickets` on the final files;
- [ ] nothing was written to a remote tracker without the user's go-ahead for it;
- [ ] the report names the frontier and every HITL ticket's owner.

These checks are properties of the ticket set. Whether agents build better from it is measured
by the comparison trial in the AI-RULES repository at `docs/validation/writing-tickets/trial.md`.

## Worked example and anti-pattern

[The worked example](resources/worked-example.md) takes a shopping-list feature from a spec and
a chat to five approved tickets with one HITL ticket and a prefactor, then reruns it after the
spec changes.

Anti-pattern: four tickets named "schema", "service", "endpoint" and "docs", each citing the
files to edit, the open question quietly answered in the service ticket, and a rerun a week
later that creates the same four tickets again beside the first set.

## Fallback

- No tracker configuration: local files in `.scratch/<feature>/issues/`, said in the report.
- No Python to run the graph check: check the edges by hand (every blocker exists, numbered
  before its dependent, no cycle, no duplicate title) and say the script did not run.
- The user cannot be reached for the quiz: write the breakdown as local drafts marked not
  approved, publish nothing remote, and list the questions.
- The remote tracker has no native blocking links: write the "Blocked by" section in the body.

## Local resources

- [Ticket template](resources/ticket-template.md)
- [Publishing](resources/publishing.md)
- [Worked example](resources/worked-example.md)
- `scripts/ticket_graph.py` and its shell shim `scripts/ticket-graph`: the graph check.
- MIT notices: [references/license.md](references/license.md).

## Operational example (offline)

This fixture checks the graph rules on a toy ticket set: a missing blocker, a blocker numbered
after its dependent, and the frontier. It does not measure ticket quality.

```python andino-operational-example
import os

def check(tickets, done=()):
    numbers = set(tickets)
    findings = []
    for number, blockers in tickets.items():
        for blocker in blockers:
            if blocker not in numbers:
                findings.append(f"{number}: unknown blocker {blocker}")
            elif int(blocker) > int(number):
                findings.append(f"{number}: blocked by later ticket {blocker}")
    frontier = sorted(n for n, b in tickets.items()
                      if n not in done and all(x in done for x in b))
    return findings, frontier

if __name__ == "__main__":
    good = {"01": [], "02": ["01"], "03": ["01"], "04": ["02", "03"]}
    assert check(good) == ([], ["01"])
    assert check(good, done=("01",)) == ([], ["02", "03"])
    assert check({"01": ["02"], "02": []})[0] == ["01: blocked by later ticket 02"]
    assert check({"01": [], "02": ["07"]})[0] == ["02: unknown blocker 07"]
    raise SystemExit(1 if os.environ.get("ANDINO_NEGATIVE") == "1" else 0)
```

## Provenance

Adapted from Matt Pocock's `to-tickets` (`SKILL.md`, mattpocock/skills 9e2abf8) under the MIT
license: tracer-bullet vertical slices with blocking edges, prefactoring first, wide refactors as
expand-contract, the quiz until approval, local and tracker publishing in dependency order,
durable tickets without paths, and the frontier. The open-decision HITL tickets, rerun matching,
the reader check, observable acceptance criteria, the authority split between local and remote
writes and the graph check script are Andino additions. The comparison trial is recorded in the
AI-RULES repository at `docs/validation/writing-tickets/trial.md`. MIT notices are in
[references/license.md](references/license.md).
