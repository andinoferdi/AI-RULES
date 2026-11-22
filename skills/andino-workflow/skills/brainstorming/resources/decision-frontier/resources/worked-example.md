# Decision Map: End-to-End Walkthrough & Deterministic Verifier

This resource demonstrates the complete lifecycle of a multi-session decision map and provides a zero-dependency Python standard library verification script.

---

## 1. End-to-End Walkthrough: Distributed Session Storage Migration

### Context & Problem
A growing monolith application faces session storage saturation in PostgreSQL. The engineering lead requests an initiative: *"Migrate monolith session storage to an external distributed cache with <5ms p99 latency without downtime or data loss."*

Because this effort involves database migrations, security policies, cache topology decisions, and fallback strategies, it cannot be settled in a single session.

### Step 1: Chart the Map (Initial State)
The agent initiates `andino-decision-map` and generates the single-canvas file at `docs/decision-maps/distributed-session-store/map.md`:

```markdown
# Decision Map: Distributed Session Storage Migration

Status: ACTIVE
Destination: All active user sessions are stored and verified in an external distributed cache with <5ms p99 read latency, zero session drops during cutover, and clean database deprecation.
Last Updated: 2026-11-01

## Notes
- **Domain**: Authentication, Token Lifecycle, Infrastructure
- **Skills to Consult**: `andino-brainstorming`, `andino-decision-interview`, `andino-primary-source-research`
- **Standing Preferences**: Must run in current Kubernetes clusters; zero proprietary cloud vendor locks.

## Decisions So Far
*(None yet)*

## Frontier: Open Tickets

### TKT-001: Benchmark Redis Sentinel vs. Dragonfly for Session Throughput
- **Type**: `research`
- **Status**: `OPEN`
- **Blocked By**: None
- **Question**: Which engine maintains <2ms p99 latency at 50,000 concurrent websocket connections under 2GB RAM?
- **Assigned Execution**: AFK Subagent (`primary-source-research`) in isolated branch `research/session-bench`.

### TKT-002: Settle Session Inactivity Timeout and Concurrent Device Limit
- **Type**: `interview`
- **Status**: `OPEN`
- **Blocked By**: None
- **Question**: What are the strict security requirements for idle timeout and max devices per user?
- **Assigned Execution**: HITL (`decision-interview`) with product security lead.

## Fog of War (Not Yet Specified)
- [ ] *Dual-writing vs. batch sync cutover strategy*: Blocked until engine performance and replication lag are known.
- [ ] *Token refresh rotation algorithm*: Blocked until security limits in TKT-002 are determined.

## Out of Scope
- Migrating long-term persistent user profile tables.
- Hardware token (WebAuthn/FIDO2) authentication flows.
```

---

### Step 2: Autonomous Parallel Research (AFK Execution)
The agent dispatches an autonomous subagent to investigate `TKT-001`:
1. Subagent spins up a localized Docker compose spike in branch `research/session-bench`.
2. Subagent executes a 10,000 QPS benchmark and collects latency logs.
3. Subagent returns verified findings:
   - Redis Sentinel: p99 read 1.2ms, write 1.8ms, memory footprint 420MB.
   - Dragonfly: p99 read 1.1ms, write 1.6ms, memory footprint 780MB, but cluster failover API is experimental in current Helm chart.
4. Resolution: Adopt Redis Sentinel. Primary citation: `docs/benchmarks/2026-11-01-redis-bench.log`.

---

### Step 3: Human-in-the-Loop Clarification (HITL Execution)
The agent invokes `andino-decision-interview` to resolve `TKT-002`:
- **Agent Question**: *"Security policies allow either 15-minute strict timeout or 30-minute sliding window. For concurrent devices, standard is 5 devices. What should we enforce?"*
- **User Answer**: *"Use 30-minute sliding window, absolute hard cutoff at 12 hours, and allow up to 5 concurrent devices."*
- **Resolution**: Stored in DEC-002.

---

### Step 4: Advance Frontier & Graduate Fog of War
With TKT-001 and TKT-002 closed, the agent updates `map.md`:
1. Appends DEC-001 and DEC-002 to `## Decisions So Far`.
2. Graduates the dual-write cutover question from `## Fog of War` into new frontier ticket `TKT-003` (Type: `prototype`).
3. Graduates the token refresh parameter from `## Fog of War` into new frontier ticket `TKT-004` (Type: `interview`).

---

### Step 5: Convergence & Handoff
Once all frontier tickets reach `RESOLVED` and the `## Fog of War` is empty:
1. Status transitions to `CONVERGED`.
2. The agent hands off directly to `andino-planning` to author the implementation tasks:
   ```
   "Decision map converged with 5 recorded decisions. Handing off to andino-planning to create execution plan at docs/exec-plans/active/distributed-session-store.md."
   ```

---

## 2. Deterministic Verification Script (Python Standard Library)

The script below verifies map state transitions, topological DAG frontier calculation, and floor invariants. It requires zero external dependencies.

```python
import os
import sys
import json
import tempfile
from pathlib import Path

def evaluate_decision_map(map_text, tickets_data, is_negative_mode=False):
    # Invariant 1: "Decisions, not deliverables" — no production code files
    code_leakage = [k for k, v in tickets_data.items() if "def " in v.get("solution", "") or "function " in v.get("solution", "")]
    if code_leakage:
        return {"status": "FAILED", "reason": "code_in_decision_map", "details": code_leakage}

    # Invariant 2: Structure checks
    required_sections = ["Destination", "Notes", "Decisions So Far", "Frontier", "Fog of War", "Out of Scope"]
    missing_sections = [s for s in required_sections if s.lower() not in map_text.lower()]
    if missing_sections:
        return {"status": "FAILED", "reason": "missing_sections", "details": missing_sections}

    # Invariant 3: Cycle Detection & Frontier Calculation (DAG)
    resolved_ids = set(k for k, v in tickets_data.items() if v.get("status") == "RESOLVED")
    open_tickets = {k: v for k, v in tickets_data.items() if v.get("status") == "OPEN"}
    
    # Check circular dependency
    def has_cycle(ticket_id, visited, stack):
        visited.add(ticket_id)
        stack.add(ticket_id)
        for dep in tickets_data.get(ticket_id, {}).get("blocked_by", []):
            if dep not in visited:
                if has_cycle(dep, visited, stack):
                    return True
            elif dep in stack:
                return True
        stack.remove(ticket_id)
        return False

    visited = set()
    stack = set()
    for t_id in tickets_data:
        if t_id not in visited:
            if has_cycle(t_id, visited, stack):
                return {"status": "FAILED", "reason": "cyclic_dependency", "details": t_id}

    # Frontier calculation: all blocked_by must be in resolved_ids
    frontier = []
    for t_id, t_val in sorted(open_tickets.items()):
        deps = t_val.get("blocked_by", [])
        if all(dep in resolved_ids for dep in deps):
            frontier.append(t_id)

    # Invariant 4: Maximum active frontier constraint
    if len(frontier) > 5:
        return {"status": "FAILED", "reason": "frontier_overflow", "details": len(frontier)}

    # Invariant 5: Empirical Evidence Floor for Research
    unverified_research = []
    for k, v in tickets_data.items():
        if v.get("type") == "research" and v.get("status") == "RESOLVED":
            if not v.get("evidence"):
                unverified_research.append(k)
    if unverified_research:
        return {"status": "FAILED", "reason": "unverified_research", "details": unverified_research}

    return {
        "status": "PASSED",
        "frontier": frontier,
        "resolved_count": len(resolved_ids),
        "open_count": len(open_tickets)
    }

def main():
    is_negative = os.environ.get("ANDINO_NEGATIVE") == "1"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        map_file = tmp_path / "map.md"

        if is_negative:
            # Adversarial test: circular dependency injection (A blocks B, B blocks A)
            tickets = {
                "TKT-001": {"type": "research", "status": "OPEN", "blocked_by": ["TKT-002"]},
                "TKT-002": {"type": "interview", "status": "OPEN", "blocked_by": ["TKT-001"]}
            }
            map_content = "Destination: Test\nNotes: None\nDecisions So Far: None\nFrontier: TKT-001\nFog of War: None\nOut of Scope: None"
        else:
            # Clean standard workflow
            tickets = {
                "TKT-001": {"type": "research", "status": "RESOLVED", "blocked_by": [], "evidence": "docs/bench.log"},
                "TKT-002": {"type": "interview", "status": "OPEN", "blocked_by": ["TKT-001"]},
                "TKT-003": {"type": "prototype", "status": "OPEN", "blocked_by": ["TKT-002"]}
            }
            map_content = "# Decision Map\nDestination: Clean\nNotes: Valid\nDecisions So Far: DEC-001\nFrontier: Active\nFog of War: Pending\nOut of Scope: Excluded"

        map_file.write_text(map_content, encoding="utf-8")
        result = evaluate_decision_map(map_content, tickets, is_negative)
        
        result_file = tmp_path / "result.json"
        result_file.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

        if is_negative:
            if result["status"] == "FAILED" and result["reason"] == "cyclic_dependency":
                print("ANDINO_NEGATIVE PASS: Successfully detected cyclic dependency violation.")
                sys.exit(0)
            else:
                print("ANDINO_NEGATIVE FAIL: Failed to trap expected violation.")
                sys.exit(1)
        else:
            if result["status"] == "PASSED" and result["frontier"] == ["TKT-002"]:
                print("ANDINO_PASS: Deterministic frontier calculated correctly.")
                sys.exit(0)
            else:
                print(f"ANDINO_FAIL: Verification failed: {result}")
                sys.exit(1)

if __name__ == "__main__":
    main()
```
