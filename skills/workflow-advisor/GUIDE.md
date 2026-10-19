# Recommend an AI-RULES workflow

Internal method ID: `workflow-advisor`. Advisory technique adapted to Andino ownership.

## Purpose and selection

Help a user choose among AI-RULES workflows, understand how methods differ or
explain why a method fits a stated need.

Activate for: An explicit question such as “Which workflow fits this?”, “Should
I use Council or AI Codebase Rescue?”, “What should I do before implementation?”,
“Can these skills work together?” or “Why was this method selected?”

Do not activate for: Ordinary work that Andino can route directly, or a general task where workflow advice was not requested. Automatic Andino routing remains independent.

Positive request: “I have a fragile subsystem with repeated regressions. Which workflow should I use, and why?”

Negative request: “Fix the already diagnosed regression in this file.”

These are selection examples, not a claim that a router or native skill was executed.

## Inputs and dependencies

The user's actual goal and constraints; the current routing and capability
registries; the relevant current method definitions; and, when native
capabilities matter, the actual host catalog and invocation controls exposed to
this session.

Read only the routing rows and method definitions that matter to the question. A
registry entry or name alone does not prove a capability is installed, readable,
invokable or active.

## Procedure

1. Identify what the user wants help deciding and which constraints or explicit preferences matter. Do not reinterpret a direct execution request as a request for workflow advice.

2. Consult the current routing and capability registries, then read the relevant
   guide or skill definitions before making detailed claims. Distinguish Andino
   internal methods from native skills, tools and external services.

3. Check the current evidence for capability state. Report only what is
   supported: a listed name is discovered; a readable guide or resource is
   available; invocation depends on the host's actual controls; activation or
   use requires the method to have actually been loaded or used. If a state
   cannot be checked, say `UNKNOWN` instead of inferring it.

4. Recommend the smallest suitable workflow. Explain why it fits, what
   meaningful trade-off it brings, and any necessary handoff or complementary
   method. Honor the user's explicit choice or exclusion. Give invocation
   guidance only when the current host actually supports it.

5. Stop at advice. Do not invoke the recommendation, execute commands, edit
   files, change configuration or start another lifecycle based on the
   recommendation alone. If the same request also authorizes a specific action,
   continue under Andino's existing scope and controls; otherwise wait for the
   user's direction.

## Ownership, precedence and permissions

Andino remains the automatic capability router and sole lifecycle owner. This
guide answers explicit advisory questions; it is not a required prerequisite,
secondary router, recursive dependency or source of automatic execution. Current
project rules and explicit user choices take precedence. Specialists retain
their established boundaries.

Read-only registry and guide inspection is limited to what is relevant. A
recommendation grants no extra authority to invoke a skill, install a tool, use
credentials, write externally, modify live data or change project state. Respect
manual-only and denied controls; never work around them by opening another copy.

## Outputs, verification and fallback

State the recommendation, the reason it fits, important alternative or
trade-off, and verified availability/invocation status. When a method was
already selected, point to the current routing condition and evidence. Do not
call a recommended method active or used without the corresponding actual
load/action and result.

If the registry, guide or host catalog cannot be read, state the actual gap and
mark affected availability `UNKNOWN` or `UNAVAILABLE`. Offer a tentative choice
from the evidence that remains, or ask for the missing detail only if it changes
the recommendation. Never invent installed skills or supported commands.

## Bounded advisory example

This standard-library example shows how to recommend a fitting capability while preserving unknown availability and keeping advice separate from execution.

```python andino-example
import json

def advise(intent, capability):
    if intent != capability["fit"]:
        return {"recommendation": "inspect-relevant-options", "availability": "UNKNOWN", "invoked": False}
    return {
        "recommendation": capability["id"],
        "availability": capability.get("availability", "UNKNOWN"),
        "invoked": False,
        "next": "check current host availability and invocation permission",
    }

RESULT = advise(
    "independent-perspectives",
    {"id": "council", "fit": "independent-perspectives", "availability": "UNKNOWN"},
)
print(json.dumps(RESULT, sort_keys=True))
```

Expected result:

```json
{"availability": "UNKNOWN", "invoked": false, "next": "check current host availability and invocation permission", "recommendation": "council"}
```

The example demonstrates advice only; it does not establish Council's host availability or invoke it.

## Provenance

Adapted in original wording from the audited local snapshot path
`mattpocock/skills:skills/engineering/ask-matt/SKILL.md`. The snapshot identity
and license are recorded in [the package provenance record](../../references/legal/provenance.md);
Andino routing and lifecycle ownership remain authoritative.
