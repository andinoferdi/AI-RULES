# Current-runtime sample review

Date: 2026-10-02. PM decision: implementation GO; accepted routing architecture stays locked. Publication is separately authorized by the human user.

Runtime commit: `effc3b8d7326d121317da86aff205de7c0bb0e80` on `andino-workflow`.
Normalized content SHA256: `dc9916a964011c8c7d16c977f614616db949e0643d5b0efa0aa3b47edb7f8447`.

Six isolated, oracle-hidden Codex CLI actors completed on this exact runtime. The adapter exposes supplied local skills and native reads, without MCP access; model identity is UNKNOWN. Explicit action/output review gives four scoped PASS and two NOT_VERIFIED:

| Case / raw record | Verdict | Scope and limitation |
| --- | --- | --- |
| [interview-material-only](live-current/interview-material-only.json) | PASS | Actual interview-me load, supplied brief inspected, one material workflow question; explicit skill selection, not autonomous discovery. |
| [idea-refine-route](live-current/idea-refine-route.json) | NOT_VERIFIED | Native read rejected by host policy; no actual skill load. No bypass attempted. |
| [debugging-superpowers-route](live-current/debugging-superpowers-route.json) | PASS | Actual systematic-debugging load and fixture reads; grounded migration diagnosis; intermittency and live database verification unresolved. |
| [agent-skills-no-double-router](live-current/agent-skills-no-double-router.json) | NOT_VERIFIED | Native reads blocked; output based on fixture description, not actual review-skill/diff inspection. |
| [clone-fidelity](live-current/clone-fidelity.json) | PASS | Actual clone-website load and source-based faithful guidance; browser fidelity and implementation not verified. |
| [simple-task-zero-capability](live-current/simple-task-zero-capability.json) | PASS | Correct direct answer, only harness-required core read, no specialist/plan/instrument. |

The original 32-case batch remains historical at its own 53-contract hash: 9 PASS / 23 NOT_VERIFIED. Nine service smoke records remain 5 PASS / 4 NOT_VERIFIED; they do not prove routing. Neither batch is promoted to current-runtime coverage. Current samples do not establish full acceptance or parity across Codex, Claude Code, OpenCode and Antigravity.

The two supplemental cases extend the evaluation set to 62 total: original 28, required 32, supplemental 2. Current-runtime auditing intentionally reports missing unsampled required cases.

The interview sample explicitly requests the supplied skill and evaluates its read-only first-question output. It has no live user response; it does not validate the skill's interactive interview lifecycle or authorize its autonomous use in non-interactive jobs.

```sh
python scripts/audit_andino_capability_live.py --runtime /path/to/andino-workflow --records docs/validation/andino-workflow/live-current
python scripts/audit_andino_capability_live.py --runtime /path/to/andino-workflow --allow-historical
```

Next validation action: execute idea-refine and the individual Agent review route on a host permitting supplied local reads; then remaining routing cases with actually exposed instruments and disposable application fixtures. Do not revise accepted runtime architecture to work around host limitations.
