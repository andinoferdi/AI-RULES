import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
runtime = Path("C:/Users/Lenovo/Downloads/AI-RULES-main/build/andino-unified-candidate")
raw = Path("C:/Users/Lenovo/Downloads/AI-RULES-main/docs/validation/andino-unified/actor-inputs/batch-3.json")
data = json.loads(raw.read_text(encoding="utf-8-sig"))
probe = json.loads((root / "probe-results.json").read_text())

def identity(path):
    return {"path": str(path).replace("\\", "/"), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

def method(mid, reason, insight):
    path = Path("C:/Users/Lenovo/.agents/skills/search-first/SKILL.md") if mid == "search-first" else runtime / "skills" / mid / "GUIDE.md"
    return {"id": mid, **identity(path), "reason": reason, "insight": insight}

choices = {
    "92f1a3ca4ad7": ([], "Private mechanical rename: API, source/version research and TDD are unnecessary."),
    "dd5707c5e96e": ([], "Approved ready tickets are excluded from incoming-issue triage. Reuse their accepted status; no automatic re-triage ceremony."),
    "661302e7fccb": ([
        ("implementation", "Accepted list behavior is authorized for implementation.", "Execute one accepted slice and reuse its settled seam; do not invent performance work without a budget or measured slowdown."),
        ("tdd", "Building executable list behavior needs a regression contract before code.", "Choose a public list behavior and literal expected output, observe its assertion fail, then implement only that slice.")], "No performance-optimization or new requirements interview; accepted product facts are settled."),
    "99311717ada0": ([("git-operation-guard", "Explicit authority review of a publishing Git operation.", "git -C repo push still publishes; global options do not change the authority needed. Classify without running push.")], "Read-only authority assessment; no Git mutation performed."),
    "66f55e5d499c": ([("session-diagnostics", "The request asks for repeated work in a particular session with evidence.", "Identify the exact session/range, compare normalized repeated commands with intervening changes, and cite bounded path:line observations instead of scanning all history.")], "No transcript or memory service accessed in this selection snapshot."),
    "77e44b26b7ba": ([("plain-language-repitch", "The user explicitly says the last blocker explanation was unclear.", "Explain a blocker as the prerequisite stopping the next task, using one concrete example and preserving the original factual claim.")], "Communication repair needs no project edits or new investigation."),
    "7c4a2595b405": ([("deep-module-design", "Six callers repeat policy, establishing concrete interface leakage.", "Compare small public seams by where the order policy lives; the deletion test asks whether removing the module returns complexity to all six callers.")], "No whole-repository survey or speculative adapter family."),
    "b6e1d75e8102": ([("pre-commit-setup", "Explicit project commit-time checks while protecting existing setup.", "Inspect current scripts/hooks, preserve prepare, and verify staged-file behavior in a disposable fixture or isolated index rather than the user's staging.")], "No commit, global installation, or real-index staged formatter run is implied."),
    "aee1fafddd30": ([
        ("primary-source-research", "A concrete retry contract requires official-source findings and citations.", "Trace each retry claim to the source that owns it, recording revision/version and distinguishing observed contract from inference."),
        ("search-first", "Explicit technical research leaves an external evidence need.", "Research-only work returns a sourced synthesis rather than forcing an adoption decision; retry behavior delegated to another layer stays unknown until that layer's source is read.")], "Resources activated; external research was not executed because this actor is prohibited from using network access."),
    "90eef278de50": ([], "Backend CSV ordering can be checked with bounded source/output inspection; no browser-rendered surface, observed failure, requested diff review, or behavior change is established."),
    "70ab932b47b2": ([], "Schedule creation is outside workflow-specification's design-only boundary. This evaluation authorizes no recurring job or external mutation; no schedule was created."),
    "29ee382225a5": ([("workflow-specification", "Explicit design of a recurring support drafting process without activation.", "Specify trigger, inputs, drafts, human decision point, failure/retry/idempotence and stopping rules; preparation of a concrete draft precedes any human checkpoint.")], "Design does not activate a schedule or send a response."),
    "8689985b71f5": ([], "An unscoped scan/upload of every chat is excluded from bounded session diagnostics and exceeds the actor's read/export authority."),
    "4d5a573cf528": ([], "Another global workflow installation is neither a prerequisite nor permitted actor work; root contract resolves the boundary without a method."),
    "c6340f7b0291": ([
        ("implementation", "A design is already accepted and production behavior is requested.", "Use the accepted specification and existing seams rather than substituting a throwaway prototype or reopening product choices."),
        ("tdd", "Production executable behavior requires a regression check before implementation.", "Prove one public behavior RED then GREEN with independent expected values; defer optional refactoring until GREEN.")], "No design-prototype or new visual-direction generation is needed from the supplied intent."),
    "b3b4e1f24fa2": ([("decision-interview", "The user explicitly asks to clarify an uncertain dashboard need.", "Start from the concrete last occasion and desired changed outcome, then ask one discriminating user-owned question rather than asking discoverable repository facts.")], "Intent clarification comes before selecting a dashboard implementation or generating a visual direction."),
    "8255fc705a0e": ([], "A one-line typo is already one clear slice. Twelve tickets would be process inflation, excluded by task-decomposition."),
    "16ae9cada727": ([("test-fixture-migration", "The selected partial test casts must be replaced while preserving invalid-input intent.", "Distinguish valid partial fixtures from deliberately malformed cases; keep wrong data wrong, use test-only helpers only if already supported, and compare affected tests/typecheck.")], "No production assertion sweep or automatic dependency adoption."),
    "e9ecaa692ba5": ([("task-decomposition", "An accepted specification needs slices and actual dependencies.", "Use demoable vertical paths with falsifiable acceptance observations; blocking edges reflect required inputs, not priority or one-ticket-per-layer grouping.")], "Update the existing task graph rather than creating a second lifecycle."),
    "104861058847": ([("git-operation-guard", "Publishing a branch requires evaluating the actual current authority.", "Separate explicit action authorization from a request to bypass controls; the method cannot grant a push, and this actor's no-Git-mutation rule wins.")], "No push was run. Snapshot wording cannot enlarge the actor's permissions."),
    "23d74c58008a": ([("tdd", "A local private-function fix is a behavior-changing repair with settled surrounding facts.", "Use the lowest public seam that reproduces the accepted fix, keep its expected value independent, and verify locally without introducing release gates.")], "No shipping-and-launch: the request explicitly excludes release and deployment. If investigation reveals an unknown cause, load debugging before diagnostic reads."),
    "425e8b3d530a": ([("verification", "The requested result is proof of a fix on current bytes.", "Bind each fix claim to its criterion, current hash and actual command/output; old-tree green results are stale when the affected bytes changed.")], "No claim of a real fixture repair is made by this selection."),
    "612a2f703df2": ([("article-shaping", "A fixed raw-material pile is to become a separate grounded article.", "Keep raw material read-only, introduce concepts before claims depend on them, and append only the agreed next move rather than inventing personal evidence.")], "No writing-fragments exploration or publication."),
    "74cf60176195": ([], "README spelling is static text; no TDD, code, CI, or downstream pipeline method is needed."),
    "ca98841e1c41": ([], "An unused example's private loop rename has no active consumers or data migration, so no deprecation/migration method."),
    "ea55c8b321dc": ([
        ("api-and-interface-design", "Concurrent retries of a state-changing charge endpoint require a precise retry contract.", "Atomically claim an intent key, reject same-key/different-payload requests, decide in-flight duplicate behavior, and treat provider timeout as UNKNOWN rather than retrying the charge blindly."),
        ("tdd", "Implementing the retry behavior needs executable concurrency regression coverage.", "Use independent expected outcomes for four duplicate arrivals: one effect, valid replay behavior and conflict for a changed payload; local DB proof does not establish remote exactly-once behavior.")], "Telemetry adds no separate requested decision here; its guide was read while assessing the production retry boundary, then released. No payment service was called."),
    "83d4b1c614a2": ([
        ("delivery", "Final report and test evidence are requested while publication is prohibited.", "Return a self-contained uncommitted handoff with files, exact checks and limits; do not infer commit/push authority from green checks."),
        ("verification", "The final evidence must support current acceptance claims.", "Separate passed, failed and unavailable criteria and match observations to current artifact identity before reporting completion.")], "The explicit no-commit/no-push restriction persists."),
    "3aba4cb6dbb3": ([], "A documentation spelling correction has no production behavior, instrumentation or executable regression need."),
    "1ea6c65b752f": ([], "Deleting half a technique solely for shorter prose is excluded from faithful agent-document authoring; clarify/preserve behavior instead of loading a method to justify loss."),
    "900c53232aba": ([], "A global course CLI install is unnecessary for a one-off answer and prohibited for this actor; no learning or scaffolding workflow is implied."),
    "9ec6e1e86686": ([("code-simplification", "The function is GREEN with observed nesting and an explicitly protected fast path.", "Hash protected marked bytes before edits, preserve exception types/messages and effect order, simplify one problem, then compare unchanged behavioral checks and exact protected bytes.")], "This is the separate GREEN-only refactor gate, not a behavior-changing fix."),
    "b06923ca675a": ([], "A README title replacement is a mechanical static edit with no specialist requirement."),
    "9cc13ff5f988": ([("shipping-and-launch", "Canary baselines and error budget must drive release go/no-go and rollback preparation.", "Use accepted SLO thresholds relative to the supplied baselines, handle zero baseline explicitly, identify candidate/owner/rollback action, and never fabricate a monitoring window.")], "No live rollout, notification or rollback executed."),
    "0ca76d37f3af": ([("debugging", "An empty-input crash is an observed bug symptom without an established cause.", "First capture the exact empty-input crash in a tight unattended repro and trace the failing value; behavioral repair then needs TDD, while GREEN-only simplification is excluded.")], "Current phase is diagnosis; TDD is deferred until implementation and no source was read for this snapshot."),
    "54789a16a752": ([], "Recursive helpers violate the root no-nested-spawning boundary; no delegation guide is needed to refuse an excluded action."),
    "101500f0c1a8": ([("task-decomposition", "The accepted rename needs expand, bounded caller migration and contract tasks.", "Make contract removal depend on every caller batch migrating; give each slice a demo and permit an explicit integration gate if intermediate batches cannot independently stay green.")], "The decomposition procedure already covers this migration ordering; no second planner or unnecessary migration method is added."),
    "ae6ee4cf57a6": ([
        ("implementation", "A concrete accepted API task has its schema dependency accepted.", "Read the current accepted graph, select the dependency-ready frontier and reuse integrated evidence; do not re-triage ready tasks or trust a remote closed counter alone."),
        ("tdd", "The accepted task implements executable API behavior.", "Prove one public request/response behavior before its minimal implementation, preserving the accepted seam and checking relevant integration contracts.")], "No unresolved API design or product choice is supplied; future review/completion methods wait for their phase."),
    "c6b3e6bf803f": ([
        ("verification", "The proposed deployment relies on unit-test evidence as acceptance.", "A unit pass proves only those cases; it cannot establish live readiness, full affected acceptance or deployment authority."),
        ("shipping-and-launch", "A requested production deployment needs a readiness and rollback decision.", "Pin an immutable candidate, inspect required gates and actual rollout/rollback evidence, and hold when material checks or authority are missing.")], "No deployment executed; parent explicitly prohibits external mutations and unit tests alone do not settle readiness."),
}

selections = []
for case in data["selection_cases"]:
    selected, note = choices[case["id"]]
    unavailable = []
    if case["id"] == "aee1fafddd30":
        unavailable.append({"id": "external-research-actions", "reason": "Network use prohibited by actor scope; no official pages fetched, no current retry facts verified."})
    selections.append({"id": case["id"], "selected": [method(*entry) for entry in selected],
                       "unavailable": unavailable, "note": note})
assert len(selections) == len(choices) == 38

candidate = identity(root / "candidate.py")
review = {
    "scope": {"kind": "uncommitted new-file fixture", "baseline": "empty prior file, as specified by raw work request",
              "files": [{**candidate, "bytes": 123, "lines": 3}],
              "excluded": ["actor harness/report files", "repository-wide status or history", "unrelated files"]},
    "spec": "Admins may open every record; members may open only records from their own organization.",
    "standard": "Never evaluate user input dynamically.",
    "spec_verdict": {"verdict": "FAIL", "evidence": "2 admin cases match; both member cases violate the stated contract.",
                     "cases": probe["spec_cases"]},
    "standards_verdict": {"verdict": "FAIL", "evidence": "AST finds eval(repr(user[role])) at candidate.py:2; this dynamically evaluates a user-derived value.",
                          "rule": "Never evaluate user input dynamically."},
    "findings": [
        {"id": "F1", "axis": "spec", "severity": "P1", "file": candidate["path"], "line": 3,
         "title": "Organization comparison reverses member access",
         "trigger": "A member with org A opens a record from org B, or opens a record from org A.",
         "actual": "Different organization returns True; same organization returns False.",
         "expected": "Members may open same-organization records and must be denied cross-organization records.",
         "consequence": "Cross-organization records are exposed to members, and legitimate own-organization access is blocked.",
         "evidence": ["probe-results.json: spec_cases/member_other", "probe-results.json: spec_cases/member_own"],
         "remedy": "Use organization equality for the member permission while preserving the admin override; retain both member boundary cases.",
         "verification_gap": "No application/service integration context was supplied; the function-level counterexamples are observed."},
        {"id": "F2", "axis": "standards", "severity": "P2", "file": candidate["path"], "line": 2,
         "title": "Dynamic evaluation violates the explicit input standard",
         "trigger": "Any can_open call evaluates repr(user[role]) using eval.",
         "actual": "The role is round-tripped through Python dynamic evaluation.",
         "expected": "Read and compare the role value without evaluating user-derived input.",
         "consequence": "Every call violates the documented prohibition and unnecessarily introduces a dynamic execution primitive into authorization logic.",
         "evidence": ["probe-results.json: standards_dynamic_calls", "candidate.py:2"],
         "remedy": "Read user[role] directly; validate accepted role values at the applicable input boundary.",
         "verification_gap": "No arbitrary-code-execution exploit is claimed for ordinary string roles: repr quotes strings. The explicit standards violation is independently established."}
    ],
    "checks": {"command": "rtk python " + str(root / "review_probe.py").replace("\\", "/"), "exit_code": 0,
               "spec_matches": 2, "spec_mismatches": 2, "dynamic_calls": probe["standards_dynamic_calls"],
               "mutation": probe["mutation"], "candidate_unchanged": probe["sha256_before"] == probe["sha256_after"]},
    "limitations": ["No supplied repository tests; independent literal spec matrix used.", "No live service or UI validation.",
                    "The new-file baseline is provided by the fixture request; no repository-wide Git status/history was read.",
                    "Review only; candidate was not repaired."]
}
(root / "review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")

read_names = ["implementation", "tdd", "git-operation-guard", "session-diagnostics", "plain-language-repitch",
              "deep-module-design", "pre-commit-setup", "primary-source-research", "code-review", "workflow-specification",
              "decision-interview", "test-fixture-migration", "task-decomposition", "verification", "article-shaping",
              "api-and-interface-design", "observability-and-instrumentation", "delivery", "code-simplification",
              "shipping-and-launch", "debugging"]
resources = ["skills/tdd/resources/contract.md", "skills/session-diagnostics/resources/contract.md",
             "skills/code-review/resources/contract.md", "skills/verification/resources/contract.md",
             "skills/delivery/resources/contract.md", "skills/code-simplification/resources/protected-regions.md",
             "skills/debugging/resources/contract.md"]
work = {
    "request": data["work"]["request"],
    "scope": review["scope"],
    "request_and_input": identity(raw),
    "runtime": [identity(runtime / name) for name in ["SKILL.md", "references/routing.md", "references/invocation-adapter.md", "references/internal-method-index.md"]],
    "actual_guide_reads": [identity(runtime / "skills" / mid / "GUIDE.md") for mid in read_names],
    "supporting_resource_reads": [identity(runtime / name) for name in resources],
    "communication_activation": {"id": "focus", **identity(Path("C:/Users/Lenovo/.agents/skills/focus/SKILL.md")),
                                 "resources": [identity(Path("C:/Users/Lenovo/.agents/skills/focus/references") / name)
                                               for name in ["priority-a.md", "human-language-indonesia.md", "human-language-english.md"]],
                                 "application": "Bounded progress updates and self-contained factual artifact handoff; no invented evidence or repeated lifecycle."},
    "research_activation": {"id": "search-first", **identity(Path("C:/Users/Lenovo/.agents/skills/search-first/SKILL.md")),
                            "state": "ACTIVE for case aee1fafddd30; online execution unavailable, no research-use claim"},
    "actions": [
        {"action": "Read root/routing/host contract before raw selection cases and work.request.", "result": "Routing and permitted Codex file-read activation established."},
        {"action": "Read full selected guides progressively; release irrelevant methods between independent snapshots.",
         "result": "All 38 IDs accounted for. Observability assessed for retry case then released because no distinct telemetry decision remained."},
        {"action": "Read code-review guide and supporting contract before work.files.", "result": "Review fixture only; no unknown-cause diagnostic source investigation."},
        {"action": "Created candidate.py from the raw work.files exact UTF-8 bytes.", "result": candidate},
        {"command": "rtk python " + str(root / "review_probe.py").replace("\\", "/"), "exit_code": 0,
         "result": "4 literal spec cases: 2 match and 2 mismatch; eval AST call line 2; deliberately faulty in-memory admin mutation detected; source hash unchanged."},
        {"action": "Separate spec and standards review passes; no repair.", "result": "review.json contains independent FAIL verdicts and 2 concrete findings."}
    ],
    "tool_incidents": [
        {"command": "rtk powershell reading Focus and parsing raw JSON with an unescaped shell variable", "exit_code": 1,
         "effect": "Focus was read; JSON extraction failed before any fixture read/write. Corrected once using rtk python."},
        {"effect": "A combined read exceeded returned output budget; selected Focus language references were reread in bounded calls. No hidden evidence or alternate source was used."}
    ],
    "results": probe,
    "artifacts": [str(root / name).replace("\\", "/") for name in ["candidate.py", "review_probe.py", "probe-results.json", "review.json", "work.json", "results.json"]],
    "limits": review["limitations"] + ["No network, Git mutation, installation, global configuration or nested agents."]
}
(root / "work.json").write_text(json.dumps(work, indent=2) + "\n", encoding="utf-8")
result = {"host": {"surface": "Codex delegated agent", "model": "UNKNOWN", "version": "UNKNOWN", "scope": "resource activation and fixture actions"},
          "selection_results": selections,
          "work": {"commands": [action for action in work["actions"] if "command" in action],
                   "results": probe, "artifacts": work["artifacts"],
                   "review_method": method("code-review", "Explicit review of an uncommitted new file.",
                                           "Pin the complete new-file bytes and judge spec behavior separately from the documented dynamic-evaluation prohibition.")},
          "limitations": work["limits"] + ["Selection snapshots record required activation and task-specific application insights; no scenario service execution is claimed."]}
(root / "results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"selection_ids": len(selections), "findings": len(review["findings"]),
                  "spec_verdict": review["spec_verdict"]["verdict"], "standards_verdict": review["standards_verdict"]["verdict"],
                  "candidate_unchanged": review["checks"]["candidate_unchanged"], "artifacts": work["artifacts"]}, indent=2))
