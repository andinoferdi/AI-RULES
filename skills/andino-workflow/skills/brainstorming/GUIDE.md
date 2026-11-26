# Find out what the user wants before anything is built

Internal method ID: `andino-brainstorming` (aliases: `brainstorming`, `interview-me`, `grilling`, `grill-me`, `grill-with-docs`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

People ask for the conventional thing ("a dashboard", "make it faster") before they have worked
out what they need. You build well, and you build what you believe the user wants; that belief is
usually thinner than it feels. Close the gap while it is cheap, before any plan, spec or code
exists: find out what the user wants and why, settle the decisions only they can make in
dependency order, and end with a design they confirmed and a builder could plan from without
asking them again. Once you understand the why, you make the many small decisions they never
mention the way they would have made them.

## Trigger and non-trigger

Use when:

- the request leaves out who it is for, why they want it, what success looks like or the binding
  constraint, and the project cannot answer it;
- a product, scope or architecture decision is open and belongs to the user;
- the user asks to brainstorm, to be interviewed or grilled, or to stress-test a plan;
- you notice you are about to fill in an ambiguous requirement without saying so.

Do not select for:

- a clear request where everything that matters is stated ("change the loan period to 21 days"):
  do it through the normal route and say what you changed;
- accepted specifications, approved plans, routine bug fixes and mechanical edits;
- questions about how something works;
- settled alternatives that only need comparing: compare them without reopening the goal.

A decision the user already settled stays settled, even when this skill is named.

## Select a resource, not a second lifecycle

Load only the resource matching the current need. A direct resource selection uses
that procedure and current authority; it does not run this parent's other modes,
reopen accepted requirements or require a second execution plan.

| Current need | Resource | Exclusion |
| :--- | :--- | :--- |
| Branching decision mapping, multi-session dependency tracking | [decision-frontier](resources/decision-frontier/guide.md) | Single-session linear decision exploration |
| Fast throwaway spike, visual/interactive proof-of-concept | [feasibility-probe](resources/feasibility-probe/guide.md) | Settled architecture ready for production implementation |
| Concept stress-testing, value proposition validation | [idea-validation](resources/idea-validation/guide.md) | Settled concept ready for engineering specification |
| Structured async stakeholder questionnaire, boundary gathering | [async-questions](resources/async-questions/guide.md) | Active synchronous dialogue or settled requirements |
| Writing the design document, an ADR or a glossary entry | [templates](resources/adr-and-glossary-template.md) | Conversation that has not reached a confirmed decision |

## Prerequisites

A user who can answer. In a non-interactive run (CI, a scheduled job, a loop) do not interview;
follow [Fallback](#fallback). Read the project's instruction files and, when they exist, the
`GLOSSARY.md` (or `GLOSSARY-MAP.md`), `docs/adr/` and specs nearest the request.

## Procedure

1. **Check what you already know.** If everything that matters is in the request, this skill
   ends: do the task through the normal route and say what you changed. Otherwise inspect the
   code, configuration, docs, glossary and ADRs the request touches, and keep reading until you
   can say how the relevant parts work today and what the change would touch. Done when every
   fact you would otherwise ask the user is found, or recorded as unknown with where you looked.

2. **Size the work** without announcing it.

   | Size | Signal | Route |
   | --- | --- | --- |
   | Spike | "Can we...", "is it possible...", a question that conversation cannot settle | [feasibility-probe](resources/feasibility-probe/guide.md): the question, a success signal, a throwaway probe |
   | Bounded | A scoped change to a flow that already exists | This procedure, short design |
   | Architectural | A new subsystem, or a changed boundary, data model or integration | This procedure, full design and the fresh-reader check |
   | Several sessions | Consequential decisions that cannot all be settled in one sitting | A [decision-frontier](resources/decision-frontier/guide.md) map that records decisions and open questions, and this procedure per session |

   Escalation goes one way: when a Bounded change turns out wider, say so and step up; never step
   down mid-task. When the request is several independent projects, say so, agree an order and
   take one at a time. Mention the size only when it changes what the user decides, in plain words
   ("this is bigger than one change; I suggest we settle X first"). Done when you know the route.

3. **Write the first message**, about 200 words, in the user's language and vocabulary:
   - echo the request in your own words: what, for whom and why, as far as they said;
   - what you found that bears on it: how it works today, and any cheaper path, existing feature,
     recorded decision it conflicts with, or code that contradicts what they said;
   - your current reading of what they want and what success would look like for them, and what
     is still missing;
   - then exactly one of:
     - a "can we...?" or "is it possible...?" question: the throwaway check, meaning the exact
       question, the result that would answer it, the cheapest check (reading the provider's
       documentation, a test call from a scratch script) labelled throwaway, and a request to run
       it;
     - the why is unknown: one open question about the outcome, with your guess and what the answer
       would change, and no options;
     - the why is known: the open decisions that are ready, as one numbered round with your
       recommendation for each;
     - nothing material is open: the short design (approach, why the others do not fit, the design
       in a few lines) and a request to approve it.

   On the Several sessions route, also say that you will keep a record of decisions and open
   questions, and where. When the user did not ask to brainstorm, end with one line offering to go
   ahead instead ("Or, if you'd rather I go ahead on my best reading, say so"). If they take it,
   state any significant how-choice (platform, language, storage) in one line and continue through
   the normal workflow. Done when the message holds your findings and one question, one round or one
   design, and no menu.

4. **Find out why before how.** Until you can say why they want it, ask open questions, one per
   turn, each with your guess and its reason, each built on their last answer or on something you
   found.
   - Buzzwords and convention ("scalable", "modern", "best practice", "a proper admin panel") are
     what a thoughtful answer sounds like, not what they want. Ask what they would want if they did
     not have to justify it to anyone, or ask about a concrete moment ("what happens at the desk
     on a Saturday morning?").
   - Turn adjectives into what would visibly change. For "faster search", ask whether results
     should arrive sooner or the right result should appear in fewer attempts. A number helps once
     it measures their actual problem.
   - When the goal itself is unclear, offer a tentative interpretation and let them describe the
     outcome in their own words before any talk of technology.

   Done when every line of the [restate block](#keep-their-words-apart-from-your-proposals) can be
   filled from what they said and you can predict their reaction to the next three questions you
   would ask. When several turns pass and your reading does not get sharper, stop and say so:
   "I still can't predict your answers, so something basic is missing. Can we step back to what
   this is for?"

5. **Work the decision frontier.** List the open decisions about what gets built and for whom:
   scope, the behaviour people will notice, who sees or does what. Record what depends on what and
   each decision's state: confirmed, delegated or open. How to build it is settled in the
   approaches (step 6) or as your call, never in these rounds. A question the project already
   answers (a glossary definition, a recorded decision, the code) is no decision: apply the answer
   and say so. The frontier is the open decisions whose prerequisites are settled. Each round:
   - ask every frontier decision only the user can make, numbered, most consequential first, each
     with your recommendation and its reason, worded so that "yes" accepts it;
   - look facts up yourself; a missing fact holds only the branch it blocks while you ask the
     rest;
   - state your own calls instead of asking them: process steps, file locations, how to show
     something, and the how itself when the user talks about outcomes rather than tools;
   - keep a question whose answer depends on another open question for a later round;
   - raise term conflicts and code contradictions as they appear
     ([Name things once](#name-things-once), [Look before you ask](#look-before-you-ask)), and test
     a boundary with a concrete edge case ("a member returns the drill at the other branch while
     someone holds it here: whose Hold gets it?").

   After each answer, read it with the [answer table](#read-the-answer-you-got), recompute the
   frontier and drop branches the answer made irrelevant. Done when the frontier is empty: every
   branch visited and nothing silently assumed. Your next message lays out the approaches.

6. **Lay out the approaches** in a message of their own, before any design. Come up with several
   real ways to build it and drop those that work against why they want it or that the existing
   work rules out. Sketch the two or three that remain concretely enough to picture, grounded in
   what the project already does, each with what it trades off. Recommend one with your reason and
   ask which they want. When they handed you the how, say you will go with your pick. When there is
   genuinely one sensible way, say so and why the others do not fit. Done when the user picked an
   approach or accepted yours.

7. **Play back and write the design.** Play back each part as soon as you understand it, in about
   200 to 300 words, then return to the next part's questions. When the user has picked an
   approach, or asks you to write it up, write the design in that same turn. Its Intent section
   opens with the restate block; a decision still open goes in its Open list and in your message.
   Short or full, the design covers every heading of the
   [design template](resources/adr-and-glossary-template.md#design-document), Approaches and
   Anti-goals included:
   - Bounded: a short design in chat or a short document, a line or two per heading, with at least
     one observable acceptance check.
   - Architectural: the full design document at the project's spec location, or
     `docs/specs/YYYY-MM-DD-<topic>-design.md`.

   An Architectural design gets the fresh-reader check: read the document as a capable builder who
   cannot talk to the user (a fresh subagent given only the document, when the host and the user
   permit one) and list the questions that builder would still need answered. Sort them: answered
   already (put the answer in the document), minor (decide it and mark it as your call), theirs
   (only the user can answer it and it changes what gets built). Bring the "theirs" pile in one
   message, most important first. Done when the document holds every confirmed decision, marks
   every call of yours as yours, and leaves no "theirs" question open.

8. **Confirm and hand off.** Ask the user for an explicit yes to the design they can see; count
   nothing else as approval, not silence and not an answer to some other question. Nothing gets
   built before that approval: no product code, scaffolding, dependency installs, new projects or
   implementation skills. Reading and exploring are fine. Two exceptions: a spike the user agreed
   to (throwaway and labelled; keeping it is a new request through this gate), and a user who opted
   out of the questions. Reuse a confirmation or authorization the user already gave for the same
   scope instead of asking again. After approval hand off to `andino-planning` (or `andino-tdd` for
   a small Bounded change); start implementation only when the user has authorized execution.
   Done when the user explicitly approved the design they saw, and every material open decision is
   answered or listed as blocking the work it affects.

## Rules for every conversation

### Look before you ask

Facts are your job; decisions are the user's. Never ask what the code, configuration, docs or
recorded decisions answer: the stack, current behaviour, file names, existing conventions. When
the user states how something works, check that the code and the recorded decisions agree, and
surface a contradiction plainly: "`src/loans/service.ts` allows one renewal, and none while a Hold
waits; you said members can renew as often as they like. Which should it be?" A request that
reverses a recorded decision is first a question about that decision: name the ADR and ask whether
to reverse it, and why now, before designing the change. Say too that going ahead means a new ADR
that supersedes the old one.

A claim from your own knowledge rather than from the project or a source you read (what a vendor
offers, how a library behaves) goes in as unverified, with how to check it.

### Ask at the right pace

| Situation | Cadence |
| --- | --- |
| The why is unknown | One open question per turn, with your guess; no options |
| The why is known and several independent decisions are open | One numbered round of those decisions, each with your recommendation |
| A decision depends on one that is still open | A later round |
| Three questions on one branch, the design changed, or the user asks to speed up | Play back what is settled and what it unblocks |
| The user is impatient | The remaining independent decisions with your defaults, in one round; stop if they opt out |

### Every question earns its place

Ask only when the answer changes what gets built and neither the request nor the project answers
it. Otherwise state your call and its reason as a proposal they can correct. Each question:

1. is anchored in a fact you found or in their last answer;
2. says what the answer would change;
3. carries your guess or recommendation, with its reason, open to revision;
4. is specific to their project, the way a sharp colleague would ask it.

Write in plain language pitched at the user. Method words (path names, "frontier", "protocol")
and quotes from this skill stay out of messages to the user. When seeing would help more than
reading (a screen, a layout, a flow), sketch it in a few lines of text or use the host's own
visual tool.

### Read the answer you got

| The user says | Treat it as |
| --- | --- |
| A clear short answer to a concrete question ("yes", "2", "owners only") | Confirmed |
| "Whatever you think" on a choice that changes what gets built | Not decided yet: offer two concrete options with your pick |
| "Whatever you think" on a minor or reversible choice | Delegated: make the call and record it as yours, with the reason |
| "Sounds good" to a summary you have not written down | Agreement with the direction only, not approval of a design |
| A buzzword or convention ("scalable", "best practice") | A cue to ask what they would want if they did not have to justify it |
| Impatience ("just build it") | The remaining independent decisions with your defaults in one round, or stop if they opt out |

A polite user may agree just to be agreeable. Stay visibly willing to be wrong, and now and then
guess in a direction you expect them to push back on.

### Keep their words apart from your proposals

Only what the user said goes in as theirs. Anything you filled in goes in as your proposal, with
its reason, so they can reject a default they would otherwise never hear. Playbacks and the design
keep three lists: confirmed by the user, your calls (delegated choices included) with reasons, and
open decisions with the work each blocks. The restate block:

```markdown
- Outcome: <one line>
- User: <who benefits>
- Why now: <what changed>
- Success: <how we will know it worked>
- Constraint: <the binding limit>
- Out of scope: <what we are not doing>
```

Every restate has an Out of scope line: silent disagreement about what is not being built is half
of all misalignment.

### Name things once

One concept, one name. When the user's word differs from the project's glossary or code
("reservation" where `GLOSSARY.md` says Hold), say so at once and settle the canonical term. When a
term is fuzzy or overloaded ("account": the member or the login?), propose a precise one. When a
term is resolved and the project keeps a glossary, update it then, in the
[glossary format](resources/adr-and-glossary-template.md#glossary); propose starting one only when
terms carry behaviour. The glossary holds no implementation detail: note code names that differ
from the term in the design document.

### Record a decision only when someone will question it

Offer an ADR only when the decision is hard to reverse, would surprise a future reader without
context, and came from a real trade-off. If any is missing, skip it. Write it after the user
confirmed the decision, never before the direction is agreed. Spikes and small Bounded changes get
no ADR or spec file. Format: [ADR](resources/adr-and-glossary-template.md#adr).

## Shortcuts that miss what the user wants

| Shortcut | Response |
| --- | --- |
| "The task is simple, I'll skip sizing it." | Size it before you write anything: a clear request ends this skill at step 1; an unclear one continues. |
| "I already know how to build this, no need to ask." | Knowing a solution is not knowing their constraints, scale or non-goals. Find the why. |
| "I'll ask five things at once to save turns." | While the why is unknown, ask one open question. Batch only independent decisions once the why is known. |
| "I'll start scaffolding while they review the design." | Nothing is built before approval. |
| "They gave a one-word answer, so they're tired." | A clear short answer is an answer. Impatience is what they say, not how much they write. |
| "I'll write the ADR now and agree later." | An early record anchors on unconfirmed assumptions. Record after confirmation, and only when the ADR test holds. |
| "They asked for a quick script; a full spec and ADR are safer." | Match the paperwork to the size. |
| "I'll ask which files need changing." | Inspect the repository. Facts are your job. |
| "I'll offer a menu of what they might want." | Options steer. Get them describing first; options come with the approaches. |
| "I'll fill in sensible defaults." | Good, out loud. A default they never heard is one they could not reject. |
| "They said 'whatever you think', so I decide the rest." | That delegates one choice. Read it with the answer table. |
| "They said 'sounds good'." | Approval covers what they saw. A design you have not written is not approved. |
| "The spike works, I'll keep building on it." | Keeping it is a new request through the gate. |
| "We've talked enough, I get it." | Test it: predict their reaction to the next three questions. |

## Red flags

- Code, scaffolding or installs before the design is approved.
- A generic questionnaire recited instead of questions built on findings and answers.
- A question with no guess or recommendation attached.
- A long document or an ADR for a one-line change.
- Asking the user what the code, configuration or recorded decisions already show.
- Still asking after you can predict their answers.
- Several why-questions in one message, or a feature menu before the why is known.
- Buzzwords accepted as requirements.
- "Whatever you think" or "sounds good" recorded as the user's decision.
- A restate with no Out of scope line.
- Method words or quotes from this skill in a message to the user.
- A design that mixes the user's decisions with your own calls.
- A how-question in a decision round, or another round when the what is already settled.
- A design treated as approved before the user said yes to it.

## Ownership and permission boundary

Andino coordinates selection, shared progress, resource guards and final status from evidence.
This skill owns its procedure, resources and checks; coordinator brevity never shortens the
questions, playbacks or design it requires. It grants no authority to build, install, commit,
publish or message anyone. Approval of a design covers that design, not its implementation.
Subagents for fact lookups or the fresh-reader check follow the workflow's delegation rules: only
when the host exposes them and the user permits them.

## Output

| Size | Output | Handoff |
| --- | --- | --- |
| Spike | The question, the success signal and a throwaway probe plan; after authorization, the observation and what it means for the design | Use the result to settle the design question; keeping the probe is a new request |
| Bounded | Short design: intended behaviour, affected area, decisions (confirmed, your calls, open), one observable acceptance check | After approval, `andino-tdd` or the authorized execution route |
| Architectural | The design document, the confirmed restate block, an ADR where the ADR test holds, glossary updates for terms that carry behaviour | After approval, `andino-planning` |

Downstream, `andino-planning` decomposes the confirmed decisions without reopening rejected
approaches, `andino-tdd` names fixtures and assertions after the glossary terms and acceptance
checks, and `andino-code-review` checks the delivered change against the ADR's consequences and
the design's invariants.

## Verification

Before handing off, check that:

- [ ] every fact you asked the user for was missing from the project;
- [ ] the why was established before any approaches were offered;
- [ ] every question carried a guess or recommendation with its reason;
- [ ] buzzword and convention answers were probed;
- [ ] terms match the glossary, and conflicts and code contradictions were raised;
- [ ] a request that reverses a recorded decision was named as such, with a superseding ADR proposed;
- [ ] claims from your own knowledge are marked unverified;
- [ ] the approaches came in their own message, with a recommendation, before the design;
- [ ] the restate block has all six lines, Out of scope included, and the user confirmed it;
- [ ] decisions are split into confirmed, your calls and open, with delegated choices marked yours;
- [ ] the design matches its size, and an Architectural design passed the fresh-reader check;
- [ ] an ADR exists only where the ADR test holds;
- [ ] the user approved the design they saw, and nothing was built before that;
- [ ] you can predict the user's reaction to the next three questions.

## Worked example and anti-pattern

[The worked example](resources/worked-example.md) follows one request from the first message to an
approved design.

Anti-pattern: the user asks for "a dashboard" and the first reply proposes chart libraries, a
layout and KPIs. Each is an assumption the user can later reject with "that's not what I meant".
Two questions in, the real need often turns out to be something else, such as a list.

## Fallback

- **User unavailable, or a non-interactive run.** Do not interview. Record confirmed decisions and
  your reversible proposals separately, name each unresolved decision and the work it blocks, and
  stop before that work.
- **No glossary or ADR folder.** Create it when the first term or ADR is actually needed.
- **No subagents.** Do the fresh-reader check yourself, reading only the document, and say so.

## Local resources

- [Templates](resources/adr-and-glossary-template.md): design document, ADR and glossary formats.
- [Worked example](resources/worked-example.md): one request end to end.
- The four sub-resources in the [resource table](#select-a-resource-not-a-second-lifecycle).
- MIT notices: [references/license.md](references/license.md).

## Operational example (offline)

This fixture checks the distinction between resolved prerequisites, a material
open frontier and design confirmation. It does not measure interview quality.

```python andino-operational-example
import os

def next_step(decisions, design_confirmed):
    pending = {name for name, (_, settled) in decisions.items() if not settled}
    frontier = tuple(
        name for name, (dependencies, _) in decisions.items()
        if name in pending and pending.isdisjoint(dependencies)
    )
    if pending:
        return ("ask", frontier) if frontier else ("blocked", ())
    return ("handoff", ()) if design_confirmed else ("confirm", ())

if __name__ == "__main__":
    decisions = {
        "roles": ((), True),
        "sharing": (("roles",), False),
        "expiry": (("sharing",), False),
    }
    assert next_step(decisions, False) == ("ask", ("sharing",))
    assert next_step(decisions, True) == ("ask", ("sharing",))
    decisions["sharing"] = (("roles",), True)
    assert next_step(decisions, False) == ("ask", ("expiry",))
    decisions["expiry"] = (("sharing",), True)
    assert next_step(decisions, False) == ("confirm", ())
    assert next_step(decisions, True) == ("handoff", ())
    raise SystemExit(1 if os.environ.get("ANDINO_NEGATIVE") == "1" else 0)
```

## Provenance

Adapted from Addy Osmani's `interview-me` (addyosmani/agent-skills 1d32b88), Matt Pocock's
`grilling` (mattpocock/skills 7739eae), `grill-with-docs` (447ca70) and `domain-modeling`
(2b7ab8c), and Jesse Vincent's superpowers `brainstorming` (obra/superpowers 22f0b46), under the
MIT license; notices are in [references/license.md](references/license.md). Sizing, decision
states, the four sub-resources and the workflow handoff come from the earlier Andino skill. The
comparison trial is recorded in the AI-RULES repository at
`docs/validation/brainstorming/trial.md`.
