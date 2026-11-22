# Skill Maker quality and setup delivery

Status: DONE
Plan Depth: STANDARD
Current Phase: Delivered
Last Updated: 2026-11-03

## Objective

Improve the authored artifact and the evidence behind it. Preserve remedial and
greenfield paths, trigger-only discovery, Andino authority and package identity.
No user incident was supplied. The two scenarios below are synthetic. No
independent evaluator was authorized or launched.

## Decisions and baseline

The current entrypoint routes to seven resources and foregrounds a metadata
example. The guide has no required authoring brief, no artifact-level acceptance
recipe and no comparison against the current skill in a revision. The validator
accepts unknown kinds under 150 lines and crashes on a null name, contrary to
the literal cases in resources/contract.md. This is a source walkthrough, not
an observed consumer RED.

Use writing-skills for matched pressure tests and using-agent-skills for
assumption handling, bounded scope and verification at the real entrypoint.
Keep the existing Andino package and improve its guided path rather than
replacing it with a generic meta-workflow.

## Execution board

| Task | Readiness | State |
| --- | --- | --- |
| T1 Authoring and verification path | READY | DONE |
| T2 Distribute exact package through setup | READY | DONE |

## T1 Change specification

- SKILL.md, before the resource links: add a numbered path from brief through
  authoring, comparison and handoff. Route both modes through observable success
  and stop conditions. Preserve the existing example marker and public identity.
- GUIDE.md, after governance: define a task fixture, output recipe, acceptance
  oracle, trigger/non-trigger probes, and comparison of unguided, existing and
  candidate conditions. Clarify walkthrough-only evidence.
- resources/worked-examples-and-templates.md: make the layout illustrative and
  add two runnable evaluation prompts with expected actions kept outside them.
  Greenfield must resolve an undefined deployment target without executing.
  Remedial must cite rollback evidence or explicitly report its absence while
  preserving the release approval gate.
- In the inline example validate name type, recognized kind and actual
  nonblank string exceptions. Keep exit 0 for the example and exit 1 with
  ANDINO_NEGATIVE=1. Probe null name, unknown kind, and 149/150/151 boundaries.
- Verify all package-relative links, entrypoint length and source walkthroughs.
  Record fresh-context behavior as NOT_VERIFIED until observed.

## T2 Change specification

In main, update only the release manifest's top-level and Andino bundle release
sequences, date and Andino commit to the published T1 identity. Keep other
capability pins. Use the bundled setup CLI in disposable project directories and
compare the installed standalone and nested packages byte for byte against T1.
Push the two branch updates without forcing remote changes.

## Result / Evidence

Python 3.12 passed 36 metadata cases and observed executable example exits 0 and 1. Live relative links resolved and SKILL.md is 131 lines. The source walkthrough covers both comparison cases. Fresh-context behavior and comparison to upstream are NOT_VERIFIED (EVALUATOR_UNAUTHORIZED).

Workflow commit ffeeae5 was pushed. Codex project setup installed both entrypoints in bundled and latest modes, each matching all nine Git files byte for byte. The published main manifest at b3ad4d2 pins f068882, whose skill-maker tree is identical to ffeeae5. That concurrent manifest update already includes the revision.

## NEXT ACTION

No delivery action remains. Fresh-context benchmarking is separate and requires evaluator authorization.
