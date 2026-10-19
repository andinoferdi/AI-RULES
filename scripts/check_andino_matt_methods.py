#!/usr/bin/env python3
"""Run bounded examples from Matt-derived Andino guides; not an LLM router."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

EXPECTED = json.loads(r'''{
  "decision-interview": {
    "frontier": [
      "charts",
      "storage"
    ],
    "out_of_scope": "metrics charts",
    "material_missing": []
  },
  "deep-module-design": {
    "selected": "minimal",
    "public_behaviors": 6,
    "hypothetical_seams": [
      "flexible"
    ]
  },
  "domain-modeling": {
    "canonical": [
      "Order",
      "Invoice",
      "Order"
    ],
    "distinct_terms": 2,
    "implementation_details": []
  },
  "implementation": {
    "ready": [
      "api",
      "docs"
    ],
    "blocked": [
      "screen"
    ],
    "git_mutations": []
  },
  "architecture-survey": {
    "candidate": "Order intake",
    "strength": "Strong",
    "external_assets": [],
    "product_edits": []
  },
  "pr-description": {
    "before": "duplicate request creates 2 invoices",
    "after": "duplicate request returns original invoice",
    "risk": "billing retries",
    "published": false
  },
  "design-prototype": {
    "empty_checkout": {
      "items": 0,
      "status": "draft"
    },
    "paid": {
      "items": 1,
      "status": "paid"
    },
    "reset": {
      "items": 0,
      "status": "draft"
    },
    "live_mutations": []
  },
  "primary-source-research": {
    "supported": 2,
    "unsupported": [],
    "live_research": false
  },
  "environment-retrospective": {
    "actions": [
      {
        "evidence": "e1",
        "action": "wire existing format-check"
      },
      {
        "evidence": "e2",
        "action": "add review standard"
      }
    ],
    "new_formatter": false,
    "global_edits": []
  },
  "project-configuration": {
    "roles": 5,
    "preserved": true,
    "external_writes": []
  },
  "specification": {
    "build_order": [
      "identity",
      "billing",
      "reports"
    ],
    "criteria_owned": [
      "billing",
      "identity",
      "reports"
    ],
    "open_questions": []
  },
  "task-decomposition": {
    "ready": [
      "migrate-worker"
    ],
    "contract_blocked": true,
    "parent_closed": false
  },
  "issue-triage": {
    "category": "enhancement",
    "recommended_state": "wontfix",
    "reason": "already implemented",
    "record_rejection": false,
    "external_write": false
  },
  "decision-map": {
    "frontier": [
      "choice"
    ],
    "user_choice_resolved": false,
    "implementation_started": false
  },
  "human-procedure": {
    "variables": [
      "SERVICE_KEY",
      "MODE"
    ],
    "secret_names": [
      "SERVICE_KEY"
    ],
    "secret_values": [],
    "external_writes": []
  },
  "handoff": {
    "next_action": "run the accepted public-interface test",
    "references": [
      "spec.md",
      "changes.diff"
    ],
    "commit_allowed": false,
    "spawned": false
  },
  "learning-workspace": {
    "recorded": [
      "idempotency",
      "timeouts"
    ],
    "covered_not_mastered": [
      "retry identity"
    ],
    "scheduled": false
  },
  "stakeholder-questionnaire": {
    "recipient": "platform owner",
    "covered_gaps": [
      "capacity",
      "retention"
    ],
    "sent": false
  },
  "plain-language-repitch": {
    "task": "API",
    "prerequisite": "schema",
    "meaning_preserved": true,
    "tool_actions": []
  },
  "agent-document-authoring": {
    "meanings": 2,
    "duplicate_removed": 1,
    "branch_reference": "TS-specific fixture examples",
    "live_model_verified": false
  },
  "git-operation-guard": {
    "verdicts": [
      "read-only",
      "requires-authority",
      "requires-authority",
      "review-required"
    ],
    "executed_mutations": []
  },
  "test-fixture-migration": {
    "helpers": [
      "fromPartial",
      "fromAny"
    ],
    "invalid_id": 123,
    "production_imports": [],
    "typescript_run": false
  },
  "exercise-scaffolding": {
    "variants": [
      "explainer",
      "problem",
      "solution"
    ],
    "nonempty_readmes": true,
    "course_linter_run": false
  },
  "pre-commit-setup": {
    "prepare": "build-tools && husky",
    "hook": [
      "lint-staged",
      "npm run typecheck",
      "npm run test"
    ],
    "index_touched": false,
    "package_execution": false
  },
  "workflow-specification": {
    "trigger": "event",
    "checkpoint_after": "draft response",
    "send_allowed": false,
    "automation_created": false
  },
  "typescript-boundary-enforcement": {
    "clean": [],
    "dirty": [
      "tests-through-entrypoints"
    ],
    "restored": [],
    "app": [
      "entrypoint-boundary-from-app"
    ],
    "cross": [
      "entrypoint-boundary-across-packages"
    ],
    "fixture": [
      "tests-folder-is-private"
    ],
    "cycle": [
      "no-circular"
    ],
    "external_tool_run": false
  },
  "article-shaping": {
    "initial_choices": [
      "identity"
    ],
    "next_choices": [
      "retry"
    ],
    "grounded": [
      "idempotency",
      "request"
    ],
    "raw_preserved": true
  },
  "writing-fragments": {
    "opening_preserved": true,
    "fragments": 2,
    "outline_added": false
  }
}''')
ARTIFACT_CONTRACTS = {
    "decision-interview": {"intent.md": ["track active experiments", "metrics charts", "local only"]},
    "deep-module-design": {"interface.md": ["quote(order)", "unsupported destination", "cents >= 0"]},
    "domain-modeling": {"GLOSSARY.md": ["**Order**", "_Avoid_: Purchase", "**Invoice**"]},
    "implementation": {"checkpoint.md": ["Accepted: schema", "Ready: api, docs", "Blocked: screen"]},
    "architecture-survey": {"architecture.html": ["Before", "After", "caller repeats validation", "submit_order"]},
    "pr-description": {"pr-body.md": ["Before:", "After:", "billing retries", "external invoice delivery"]},
    "design-prototype": {"prototype.html": ["data-action=\"add\"", "data-action=\"checkout\"", "Guided walkthroughs", "function reduce", "aria-live"]},
    "primary-source-research": {"research.md": ["Retry key is required", "Retention is 24 hours", "fixture spec-v1"]},
    "environment-retrospective": {"retro.md": ["e1: wire existing format-check", "e2: add review standard"]},
    "project-configuration": {"AGENTS.md": ["Keep this instruction.", "issue-tracker.md"], "issue-tracker.md": ["local Markdown", "real IDs"]},
    "specification": {"spec.md": ["identity -> billing -> reports", "one invoice per retry key", "Out of scope: email delivery"]},
    "task-decomposition": {"tasks.json": ["migrate-ui", "migrate-worker", "contract"]},
    "issue-triage": {"triage.md": ["generated by AI", "already implemented", "feature exists"]},
    "decision-map": {"map.md": ["Destination: choose local storage", "Not yet specified: backup policy", "Out of scope: cloud sync"]},
    "human-procedure": {"manual-steps.md": ["privately", "never paste into chat", "No external writes"]},
    "handoff": {"handoff.md": ["verification pending", "spec.md", "commit", "false", "run the accepted public-interface test"]},
    "learning-workspace": {"MISSION.md": ["diagnose safe retries", "explain duplicate handling", "Out of scope"], "lesson.html": ["local source fixture"]},
    "stakeholder-questionnaire": {"questionnaire.md": ["platform owner", "peak request rate", "retained", "unknowns are useful", "> "]},
    "plain-language-repitch": {"repitch.txt": ["API task", "schema change", "Finish that change first"]},
    "agent-document-authoring": {"consumer-guide.md": ["done when", "only for TypeScript tests"]},
    "git-operation-guard": {"git-review.json": ["requires-authority", "review-required", "read-only"]},
    "test-fixture-migration": {"fixture-migration.json": ["fromPartial", "fromAny", "123"]},
    "exercise-scaffolding": {"exercises/05-memory/05.02-short-term/explainer/readme.md": ["Short-term memory", "concrete recall task"], "exercises/05-memory/05.02-short-term/problem/readme.md": ["Recall task"]},
    "pre-commit-setup": {"proposed-hook.txt": ["lint-staged", "npm run typecheck", "npm run test"]},
    "workflow-specification": {"workflow.json": ["new support request", "draft response", "draft link"]},
    "typescript-boundary-enforcement": {"boundary-results.json": ["tests-through-entrypoints", "entrypoint-boundary-from-app", "entrypoint-boundary-across-packages", "tests-folder-is-private", "no-circular"]},
    "article-shaping": {"raw.md": ["Requests can be repeated."], "article.md": ["Idempotency", "same intended action"]},
    "writing-fragments": {"fragments.md": ["User-edited opening.", "---", "one intention"]},
}
LIMITATIONS = [
    "Deterministic local example execution and artifact semantics only; no model routing selector is implemented or claimed.",
    "Positive/negative raw requests are evaluation inputs, not proven live-model activation results.",
    "No live host parity, human feedback quality, browser rendering/click-through, external tracker mutation or optional package CLI execution is claimed.",
    "TypeScript boundary checks exercise the stated graph rules on literal fixtures, not dependency-cruiser parsing/resolution.",
    "Source libraries, scripts, hooks, installers and remote services are not executed.",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_case(runtime: Path, method: dict) -> dict:
    method_id = method["id"]
    guide = runtime / "skills" / method_id / "GUIDE.md"
    example = runtime / "skills" / method_id / "resources" / "worked-example.md"
    source = example.read_text(encoding="utf-8")
    blocks = re.findall(r"```python\n(.*?)\n```", source, re.S)
    if len(blocks) != 1:
        raise AssertionError(f"{method_id}: expected exactly one executable Python example")
    compile(blocks[0], str(example), "exec")
    source_hashes = {p.relative_to(runtime).as_posix(): digest(p)
                     for p in [guide, *[runtime / r for r in method["resources"]]]}
    with tempfile.TemporaryDirectory(prefix="andino-matt-") as work:
        directory = Path(work)
        script = directory / "example.py"
        script.write_text(blocks[0], encoding="utf-8")
        run = subprocess.run([sys.executable, str(script)], cwd=directory,
                             text=True, capture_output=True, timeout=10, check=False)
        if run.returncode:
            raise AssertionError(f"{method_id}: example exited {run.returncode}: {run.stderr}")
        observed = json.loads((directory / "result.json").read_text(encoding="utf-8"))
        if observed != EXPECTED[method_id]:
            raise AssertionError(f"{method_id}: independent expected mismatch: {observed!r}")
        artifacts = []
        for relative, required_facts in ARTIFACT_CONTRACTS[method_id].items():
            path = directory / relative
            actual = path.read_text(encoding="utf-8")
            for fact in required_facts:
                if fact not in actual:
                    raise AssertionError(f"{method_id}: missing artifact observation {fact!r}")
            if path.suffix == ".html" and re.search(r"(?:src|href)=[\"']https?://", actual):
                raise AssertionError(f"{method_id}: example acquired an external runtime asset")
            artifacts.append({"path": relative, "bytes": path.stat().st_size,
                              "sha256": digest(path), "observations": required_facts})
        if method_id == "exercise-scaffolding":
            base = directory / "exercises/05-memory/05.02-short-term"
            assert {p.name for p in base.iterdir()} == {"explainer", "problem", "solution"}
            assert all((base / v / "readme.md").stat().st_size > 20 for v in ("explainer", "problem", "solution"))
        if method_id == "article-shaping":
            assert (directory / "raw.md").read_text() == "Requests can be repeated. Identity connects repeated attempts."
        if method_id == "writing-fragments":
            actual = (directory / "fragments.md").read_text()
            assert actual.count("\n---\n") == 1
            assert actual.index("User-edited opening.") < actual.index("A retry")
        if method_id == "project-configuration":
            mapping = json.loads((directory / "triage-labels.json").read_text())
            assert mapping["needs-info"] == "waiting" and mapping["ready-for-agent"] == "agent-ready"
    return {"id": method_id, "status": "PASS", "verification_level": "deterministic-operational-example",
            "source_hashes": source_hashes, "observed": observed, "artifacts": artifacts,
            "live_model_routing": "NOT VERIFIED", "live_optional_tools": "NOT VERIFIED",
            "limitations": LIMITATIONS}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-root", type=Path,
                        default=Path(__file__).resolve().parents[2] / "AI-RULES")
    parser.add_argument("--methods", type=Path,
                        default=Path(__file__).resolve().parents[1] / "docs/validation/andino-unified/matt-methods.json")
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parents[1] / "docs/validation/andino-unified/matt-operational.json")
    args = parser.parse_args()
    methods = json.loads(args.methods.read_text(encoding="utf-8"))
    if {m["id"] for m in methods} != set(EXPECTED) or len(methods) != len(EXPECTED):
        raise AssertionError("Metadata and operational fixtures must cover exactly the 28 owned methods")
    records = []
    for method in methods:
        try:
            record = run_case(args.runtime_root.resolve(), method)
            record['metadata_sha256'] = hashlib.sha256(json.dumps(method, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            records.append(record)
        except Exception as error:
            records.append({"id": method["id"], "status": "FAIL", "error": str(error)})
    report = {"schema_version": 1, "source_family": "matt", "checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "runtime_root": str(args.runtime_root.resolve()),
              "checker_sha256": digest(Path(__file__)),
              "methods_sha256": digest(args.methods),
              "inputs": {"scripts/check_andino_matt_methods.py": digest(Path(__file__)),
                         args.methods.resolve().relative_to(Path(__file__).resolve().parents[1]).as_posix(): digest(args.methods)},
              "command": [sys.executable, str(Path(__file__).resolve()), "--runtime-root",
                          str(args.runtime_root.resolve()), "--methods", str(args.methods.resolve()),
                          "--output", str(args.output.resolve())],
              "verification_scope": "Executed exact Python examples extracted from adapted Markdown; independently checked literal results and generated artifact semantics.",
              "limitations": LIMITATIONS, "records": records,
              "passed": sum(r["status"] == "PASS" for r in records),
              "failed": sum(r["status"] != "PASS" for r in records)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Matt procedures: {report['passed']} PASS, {report['failed']} FAIL; live model routing NOT VERIFIED")
    for record in records:
        if record["status"] != "PASS":
            print(f"{record['id']}: {record['error']}")
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
