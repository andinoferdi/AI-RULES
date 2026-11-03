# Factual Integration and Branch Delivery

Resource contract selected directly under its canonical owner.

## Required evidence

- Candidate SHA and checkout topology, including recorded ownership.
- Passing project checks for the exact candidate, with scope and command recorded.
- Selected action, scoped authority, and destination where applicable.
- Observed merge, remote ref, or PR result and workspace disposition.

## Stop conditions

Preserve the candidate when checks fail, functional changes are uncommitted, Git is in an unfinished operation, or the destination is unresolved. Use scoped change hygiene when a commit is authorized. Never stash unrelated work to clear delivery. Keep partial results visible and recheck state before retrying.

## Local resources

Follow the [delivery guide](guide.md) and its resources for procedure and examples. See the [license notice](../../references/license.md) for upstream provenance.

## Runnable Operational Contract & Verification Harness

```python andino-operational-example
import json, os, sys

def evaluate_delivery_contract(data):
    if not isinstance(data, dict): return {"valid": False, "error": "Contract must be a dict"}
    if data.get("test_suite_passed") is not True: return {"valid": False, "error": "Green test suite required"}
    action = data.get("authorized_action")
    if action in ("merge", "pr") and not str(data.get("base_branch", "")).strip():
        return {"valid": False, "error": "Base branch must be confirmed"}
    if action in ("push", "pr") and not data.get("remote_ref"):
        return {"valid": False, "error": "Remote ref required"}
    if data.get("has_uncommitted_changes") is True: return {"valid": False, "error": "Working tree must be clean"}
    options = data.get("presented_options", [])
    if not action and len(options) not in (2, 3): return {"valid": False, "error": "An open decision requires applicable options"}
    if data.get("force_removal_used") is True: return {"valid": False, "error": "Zero-force invariant violated"}
    if data.get("automatic_hard_reset_used") is True: return {"valid": False, "error": "Automatic hard reset prohibited"}
    if data.get("automatic_pull_used") is True: return {"valid": False, "error": "Automatic pull prohibited"}
    if data.get("merge_abort_without_merge_head") is True: return {"valid": False, "error": "merge --abort only valid when MERGE_HEAD exists"}
    if data.get("unowned_cleanup_attempted") is True: return {"valid": False, "error": "Path naming is never ownership; clean only owned worktrees"}
    return {"valid": True, "status": "DELIVERY_CONTRACT_VERIFIED"}

if __name__ == "__main__":
    is_neg = os.environ.get("ANDINO_NEGATIVE") == "1"
    payload = {
        "test_suite_passed": not is_neg,
        "authorized_action": "push",
        "remote_ref": "origin refs/heads/feature",
        "has_uncommitted_changes": is_neg,
        "presented_options": [],
        "force_removal_used": is_neg,
        "automatic_hard_reset_used": is_neg,
        "automatic_pull_used": is_neg,
        "merge_abort_without_merge_head": is_neg,
        "unowned_cleanup_attempted": is_neg,
    }
    result = evaluate_delivery_contract(payload)
    if not result["valid"]:
        sys.stderr.write(f"Verification failed: {result['error']}\n")
        sys.exit(1)
    print(json.dumps(result, sort_keys=True))
    sys.exit(0)
```
