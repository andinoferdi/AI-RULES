# Security and hardening quality

Status: IN_PROGRESS
Depth: STANDARD
Phase: Publication
Base: c74f755

## Decision

The Addy reference offers more concrete control guidance and verification.
Andino already covers authority, filesystem ownership, races and bounded proof.
Keep those safeguards and the runnable oracle. Add a scoped workflow, targeted
controls and a worked finding. A direct rubric review can measure guidance
coverage. Live model performance remains a separate measurement.

## Ready tasks

1. Update the native skill and nested guide in lockstep. Require one trace from
   untrusted writer to effect, prioritized findings and positive/negative proof.
2. Expand the existing resource with verification examples for tenant access,
   sessions, outbound fetches, filesystem ownership, dependencies and LLM tools.
   Keep the existing Python oracle interface and license.
3. Check entrypoint parity, run the security oracle including its mutant, and
   compare all three contracts against the same bounded cases.
4. Push the workflow and publish the verified commit in the stable setup
   manifest. Run project-scoped setup and compare installed native and nested
   copies with the pushed source.

## NEXT ACTION

Publish the skill commit and verify default setup in a disposable project.

## Evidence

Direct contract review against three representative scenarios:

| Case | Original Andino | Addy reference | Revised Andino |
| --- | --- | --- | --- |
| Cross-tenant invoice read | Requires resource authorization and abuse evidence | Names IDOR and per-resource access | Adds a worked finding and same-tenant, cross-tenant and anonymous probes |
| Mixed DNS answers and redirects | Rejects all nonpublic answers and redirects, names rebinding | Calls out reserved addresses and validate-then-fetch gaps | Keeps the checks and requires proof at the fake transport |
| Root-target teardown | Requires strict descendant, trusted ownership and race protection | Requires root, depth and ownership and calls out marker and race limits | Preserves these safeguards and checks that refusal never reaches mutation |

Native and nested entrypoint instructions match from Activation onward.
The existing offline oracle passed its default and adversarial cases and
detected the mutant allowing the owned root. This evaluates the instruction
contract and embedded fixture. No live model comparison or service probe ran.
