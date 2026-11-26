# Find deepening opportunities and grill the one worth doing

Internal method ID: `andino-architecture-survey` (aliases: `architecture-survey`,
`improve-codebase-architecture`).

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose

Surface architectural friction and propose **deepening opportunities**: refactors that turn
shallow modules into deep ones, so the code is easier to test and easier for an agent to
navigate. A survey reads code and history, presents candidates as a visual before/after
report, and grills the one the user picks. It never edits product code. The deliverable is
the report, a chat summary card and a grilled decision, not a refactor.

## Trigger and non-trigger

Use when:

- the user names a pain point, module or subsystem and asks how to restructure it;
- the user asks where a codebase's architecture should improve, with no direction;
- callers repeat the same orchestration around a module, tests mock every internal step, or
  every change touches many small files.

Do not select for:

- Renames, formatting or file moves that leave every module's interface unchanged.
- A single interface whose shape is the whole question: `api-and-interface-design`.
- Retiring an interface consumers still use: `deprecation-and-migration`.
- A bug of unknown cause: `debugging`.
- Another search after a survey found no worthwhile candidate. Report that result instead.

## Select a resource, not a second lifecycle

Load only the resource the current need names. It runs inside this procedure and current
authority; it starts no second plan.

| Current need | Resource | Skip when |
| :--- | :--- | :--- |
| Exact terms, substitutions, dependency categories, card wording | [vocabulary](resources/architectural-vocabulary.md) | The terms in Rules settle the question |
| Choosing and drawing a before/after diagram | [diagram patterns](resources/diagram-patterns.md) | No report is being written |
| The report file: scaffold, offline fallback, delivery, summary card | [HTML report scaffold](resources/html-report-scaffold.md) | No report is being written |
| Briefing a fresh-context explorer the user approved | [exploration brief](resources/subagent-exploration-brief.md) | You explore inline |
| Grilling the picked candidate, GLOSSARY.md and ADR side effects | [grilling and ADR protocol](resources/grilling-and-adr-protocols.md) | The user has not picked a candidate |
| One survey end to end, with before and after code | [worked example](resources/worked-example.md) | The procedure is already clear |
| Designing the deepened module's interface, design-it-twice | The module-depth resource of the sibling `api-and-interface-design` skill: `resources/module-depth/guide.md` in that skill's folder (`andino-api-and-interface-design` when installed on its own) | The candidate's shape is not settled yet |

## Prerequisites

Read the domain glossary (`GLOSSARY.md`, or the file a `GLOSSARY-MAP.md` points to) and the
ADRs in `docs/adr/` for the area you will touch: the glossary names good seams, and ADRs
record decisions a survey must not re-litigate. Note whether the user named a direction. A
missing glossary or ADR folder is a fact to record, not a blocker.

## Procedure

1. **Scope before you scan.** Deepening pays off by making future changes easier, so weight
   the code that changes. Pick one mode:
   - **Named subsystem**: the user named a module, area or pain point. Take it and skip the
     inference below; walk its callers, tests and dependencies.
   - **Hot spot**: no direction. Walk a good stretch of history (`git log --oneline`, then
     `git log --name-only` over the same range) and let the files and areas that keep
     changing pull your attention first. If changes are scattered with no clear hot spot,
     widen the net to the entrypoints and the modules they reach.
   - **Cross-seam leakage**: the complaint is coupling, such as callers handling another
     module's transactions, clients or transport types, or tests mocking every internal
     step. Trace those callers.

   Done when the paths you will walk, and why, are written down.
2. **Explore organically.** Read the code yourself by default. Use a fresh-context explorer
   only when the user approves one, briefed with the
   [exploration brief](resources/subagent-exploration-brief.md). Follow friction, not a
   checklist of thresholds:
   - Where does understanding one concept mean bouncing between many small modules?
   - Where is a module **shallow**, its interface nearly as complex as its implementation?
   - Where were pure functions extracted to be testable while the real bugs hide in how
     they are called (no **locality**)?
   - Where do coupled modules leak across their seams?
   - Which parts are untested, or hard to test through their current interface?

   Apply the **deletion test** to every suspect: imagine deleting it. If complexity
   vanishes, it was a pass-through; if it reappears across its callers, it earns its keep.
   Say where each defect lives: a correct, well-tested pure function is not the defect
   when its callers misuse it. The deepening then gathers what those callers each compute
   (units, periods, ordering) into one module, and the function and its tests stay.
   Done when each suspect has file and symbol evidence and a deletion-test verdict, and
   every untested or hard-to-test area you found is either a candidate or listed under
   "Also found".
3. **Shape candidates.** For each deepening worth proposing, write a title that names the
   deepening, the files, the problem in one sentence, the solution in one sentence, wins of
   6 words or fewer in glossary terms, a strength (`Strong`, `Worth exploring` or
   `Speculative`), the dependency category, and an ADR callout only when the friction is
   real enough to reopen that ADR. Recent change raises strength. Do not propose interfaces
   yet: the solution names the consolidation and where the seam goes, never a method name
   or signature. Keep a short "Also found" list for findings you do not propose (kept
   modules with their deletion-test reason, untested areas, ADR-protected ideas). Done when
   every candidate has every field and none rests on a seam with one adapter.
4. **Write the report.** One self-contained HTML file in the OS temp directory, built from
   the [HTML report scaffold](resources/html-report-scaffold.md): a legend, one card per
   candidate with a side-by-side before/after diagram from
   [diagram patterns](resources/diagram-patterns.md), and a top recommendation. Vary the
   patterns, and if a diagram needs a paragraph to be understood, redraw it. Open the file
   with the platform opener; in a headless session give the path only. Done when the file
   exists and its text and diagrams read with the CDNs blocked.
5. **Present and stop.** In chat, print the summary card built from the same candidate
   data and the report's absolute path, then ask: "Which of these would you like to
   explore?" Done when the user picks a candidate or declines; a decline ends the survey.
6. **Grill the chosen candidate** with the
   [grilling and ADR protocol](resources/grilling-and-adr-protocols.md). The first round
   covers all five decisions: constraints, what sits behind the seam, which adapters exist,
   which tests survive and which are replaced, and how each caller migrates. Every question
   carries your recommended answer; for tests and migration, recommend what follows from the
   shape you recommend. Side
   effects happen inline as decisions settle: add a new domain term to GLOSSARY.md (create
   the file lazily), sharpen a fuzzy term in place, and when the user rejects a candidate
   for a reason a future survey would need, offer to record an ADR. Done when the deepened
   module's shape is settled, or the candidate is rejected and its reason handled.
7. **Hand off.** Explore alternative interfaces with design-it-twice in the module-depth
   resource of `api-and-interface-design`. Record the chosen candidate, its files, seam and
   migration in the active execution plan. Done when the execution plan or the user holds
   the decision and no product file has changed.

## Rules

### Words

Use module, interface, implementation, depth, deep, shallow, seam, adapter, leverage and
locality exactly, as defined in the [vocabulary](resources/architectural-vocabulary.md).
Two definitions carry the most weight:

- An **interface** is everything a caller must know to use the module correctly: types,
  invariants, ordering, error modes, required configuration and performance.
- **Depth** is leverage at the interface: how much behaviour a caller or test reaches per
  unit of interface it learns. Depth is not a ratio of implementation lines to interface
  lines.

Name modules with the glossary's domain words ("the order intake module", not
"OrderService"). In your own prose, component, service, unit, API, signature, boundary and
layer are not substitutes for these terms; identifiers quoted from the code keep their
names. A win names a gain ("tests hit one interface"), never "cleaner code" or "easier to
maintain".

### Seams and dependencies

- One adapter means a hypothetical seam; two adapters mean a real one, and a test stand-in
  counts as an adapter. Do not propose a seam that nothing varies across.
- A third-party client injected as a port already has two adapters: the real client and the
  test's mock. Code that builds its clients inside itself is hard to test through its
  interface, and injecting those clients is a candidate. The one-adapter warning is for a
  port that tests never substitute, such as an interface over your own single class.
- A deep module may keep internal seams for its own tests; leave them out of its interface.
- Classify each candidate's dependencies, because the category decides how the deepened
  module is tested:
  - **in-process**: pure computation or in-memory state. Merge, then test through the new
    interface.
  - **local-substitutable**: a dependency with a local stand-in, such as an in-memory
    database or filesystem. Test with the stand-in; no port at the interface.
  - **ports & adapters**: your own service across a network. Define a port; production uses
    the real transport, tests use an in-memory adapter.
  - **true external**: a third party you do not control. Inject it as a port; tests use a
    mock adapter.

### Tests

The interface is the test surface: callers and tests cross the same seam. Once tests at the
deepened interface exist, delete the old tests of the shallow modules: replace, don't
layer. A test that must change whenever the implementation changes is testing past the
interface.

### Scope and history

Weight recently changed code. Dormant code may appear as `Speculative` with that reason; it
is rarely the top recommendation. A direction the user names wins over history.

## Shortcuts that break a survey

| Shortcut | What actually happens |
| --- | --- |
| "This old file is ugly; lead with it." | Deepening pays back through future change. Code nobody touches repays little; mark it Speculative or leave it out. |
| "I'll sketch the new interface now and save a turn." | The user has not picked a candidate, so the design anchors on your first idea. Present candidates; design after grilling. |
| "'Service' is the standard word." | It names nothing precise and invites a shallow class. Say module, seam or adapter, and use the glossary's domain word. |
| "A summary in chat is enough." | Shallowness and leaks are spatial; the before/after diagram makes them visible. Write the report, then the summary card. |
| "Add a port so it is testable." | With one adapter the port is indirection. Test with the dependency's local stand-in, or add the port when a second adapter exists. |
| "That small helper is everywhere; fold it in." | Run the deletion test first. If its rules would reappear in every caller, it is load-bearing. |

## Red flags

- A product file edited, refactored or created during the survey.
- A survey with no report, or a report without before/after diagrams.
- A candidate whose seam has one adapter.
- An interface proposed before the user picked a candidate.
- A candidate that contradicts an ADR with no callout.
- A cited path, symbol or caller you did not read.
- Depth argued from line counts.

## Ownership and permission boundary

Andino coordinates selection, shared progress, resource guards and final status from
evidence. This skill owns its procedure, resources and checks, and coordinator brevity
never truncates them. The survey is read-only: no product code, configuration or git state
changes, and the report lives in the OS temp directory. GLOSSARY.md and ADR edits happen
only during grilling, as the user's decisions settle. A fresh-context explorer runs only
when the user approves it. Loading this skill grants no commit, push, refactor or
installation authority.

## Output

- **Report:** the absolute path of the HTML file.
- **Summary card:** per candidate, title, strength, dependency category, files, problem,
  solution and wins.
- **Question:** "Which of these would you like to explore?"
- **After grilling:** the settled shape (what the interface hides, what sits behind the
  seam, its adapters, which tests are replaced, how callers migrate), the GLOSSARY.md and
  ADR changes, and the execution-plan entry.
- **Not verified:** anything you could not read or run.

## Verification

- [ ] The report file exists in the OS temp directory and its absolute path was given.
- [ ] Every card has files, a one-sentence problem and solution, wins of 6 words or fewer, a
      before/after diagram, a strength and a dependency category.
- [ ] Every cited file and symbol exists, and every candidate passed the deletion test.
- [ ] No candidate rests on a one-adapter seam; every ADR conflict has a callout.
- [ ] Each card's text and at least one diagram read with the CDNs blocked.
- [ ] Your own prose uses the vocabulary, with no substitutes.
- [ ] `git status --porcelain` shows no product file changed by the survey.

## Worked example and anti-pattern

[The worked example](resources/worked-example.md) surveys an order intake flow: the shallow
modules and the leaking transaction, the card and summary card, and the design reached
after grilling.

Anti-patterns: a report that lists every module as a candidate; merging a module an ADR
keeps separate without saying so; deleting a small helper every caller relies on; a port
with one adapter "for testability"; a refactor started before the user picked a candidate.

## Fallback

- No git history: ask for a direction, or walk from the entrypoints.
- No browser or a headless session: give the absolute path; the summary card carries the
  content.
- No network: the scaffold's embedded styles and hand-built diagrams keep the report
  readable.
- No glossary or ADRs: say so in the report header and name modules after the code's own
  domain words.
- Explorer not approved: explore inline; the brief's checks still apply to your findings.

## Local resources

The resources above are packaged with this skill; upstream repositories are not runtime
dependencies. The MIT notice is in [references/license.md](references/license.md).

## Operational example (offline)

```python andino-operational-example
import json, os

def verdict(module):
    """Deletion test first, then the seam rule."""
    if module["callers_relying_on_its_rules"] >= 2:
        return "keep"            # deleting it scatters its rules across callers
    if module["is_port"] and module["adapters"] < 2:
        return "collapse-seam"   # one adapter: a hypothetical seam
    if module["pass_through"]:
        return "deepen"          # complexity vanishes with it: absorb it into a deep module
    return "keep"

def top(candidates):
    order = {"Strong": 3, "Worth exploring": 2, "Speculative": 1}
    return max(candidates, key=lambda c: (order[c["strength"]], c["recent_commits"]))["title"]

negative = os.environ.get("ANDINO_NEGATIVE") == "1"
modules = {
    "CurrencyMath": {"callers_relying_on_its_rules": 6, "is_port": False, "adapters": 0,
                     "pass_through": False},
    "INotifier": {"callers_relying_on_its_rules": 0, "is_port": True, "adapters": 1,
                  "pass_through": True},
    "OrderValidator": {"callers_relying_on_its_rules": 0, "is_port": False, "adapters": 0,
                       "pass_through": not negative},
}
candidates = [
    {"title": "Collapse the order intake pipeline", "strength": "Strong", "recent_commits": 14},
    {"title": "Rewrite the legacy report export", "strength": "Speculative", "recent_commits": 0},
]
verdicts = {name: verdict(module) for name, module in modules.items()}
expected = {"CurrencyMath": "keep", "INotifier": "collapse-seam", "OrderValidator": "deepen"}
ok = verdicts == expected and top(candidates) == "Collapse the order intake pipeline"
print(json.dumps({"verdicts": verdicts, "top": top(candidates),
                  "status": "CONTRACT_VERIFIED" if ok else "CONTRACT_BROKEN"}))
raise SystemExit(0 if ok else 1)
```

Default output: `{"verdicts": {"CurrencyMath": "keep", "INotifier": "collapse-seam",
"OrderValidator": "deepen"}, "top": "Collapse the order intake pipeline", "status":
"CONTRACT_VERIFIED"}`. With `ANDINO_NEGATIVE=1` the validator stops being a pass-through,
the "deepen" expectation fails and the example exits 1. It checks the order of the deletion
test and the seam rule, not a model's survey.

## Provenance

Adapted from Matt Pocock's `improve-codebase-architecture` with its `HTML-REPORT.md`, and
from the skills it calls, `codebase-design` (with `DEEPENING.md` and `DESIGN-IT-TWICE.md`),
`grilling` and `domain-modeling` (mattpocock/skills commit 7739eae, 2026-10-29), under the
MIT license: the deepening aim, scope before scanning, the exploration questions, the
deletion test, the vocabulary and its definitions, the dependency categories,
replace-don't-layer, the report card and diagram patterns, the grilling rounds and the
glossary and ADR side effects. The three modes, the offline report fallback, the summary
card, the explorer brief with its return schema and checks, the ADR template and the
execution-plan handoff are Andino additions.
