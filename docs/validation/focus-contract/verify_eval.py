"""Structural and transcript checks; semantic review remains in report.md."""
import hashlib
import argparse
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
from run_eval import runtime_file, git_file

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--focus-root", type=Path)
parser.add_argument("--web-root", type=Path)
args = parser.parse_args()


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


before = load("before-inputs.json")
snapshots = {phase: load(f"{phase}-inputs.json") for phase in ("before", "after", "final")}
outputs = {phase: load(f"{phase}-outputs.json") for phase in snapshots}
for phase, data in snapshots.items():
    assert data["cases"] == before["cases"]
    assert data["context"] == before["context"]
    assert data["model"] == before["model"] == "claude-sonnet-5-5"
    assert data["effort"] == before["effort"] == "medium"
    records = outputs[phase]
    assert len(records) == 20
    assert len({(r["variant"], r["case"]) for r in records}) == 20
    for record in records:
        assert record["exit_code"] == 0
        response = record["response"]
        assert not response["is_error"] and response["subtype"] == "success"
        assert set(response["modelUsage"]) == {"claude-sonnet-5-5"}
        system = "Apply the following communication rules to the user's request. No tools are available.\n" + data["context"] + "\n" + data["contracts"][record["variant"]]
        assert record["system_sha256"] == hashlib.sha256(system.encode()).hexdigest()
        assert record["prompt"] == dict(data["cases"])[record["case"]]
        result = response["result"]
        if record["case"] == "json":
            parsed = json.loads(result)
            assert set(parsed) == {"status", "passed", "unverified"}
            assert "6" in str(parsed["passed"])
            assert "integration" in str(parsed["unverified"]).lower()
        elif record["case"] == "code":
            assert "```" not in result
            namespace = {}
            exec(compile(result, "model-code-only", "exec"), namespace)
            assert namespace["parse"]("") == []
            assert namespace["parse"]("a,b") == ["a", "b"]
        elif record["case"] == "override":
            assert "\n\n" not in result.strip()
            assert not re.search(r"(?m)^\s*\d+\. ", result)
        elif record["case"] == "long":
            for term in ("lost update", "version", "for update", "row", "deadlock", "retry", "idempoten", "isolation", "trade"):
                assert term in result.lower(), (phase, record["variant"], term)
            assert len(result.split()) > 500
    print(f"{phase}: 20 real successful inferences, identical fixtures/config; JSON, code and format checks pass")

old_web = git_file("2fdbce1a7448932646c09f758c6d9ccb4a6e022e:README.md")
new_web = runtime_file("WebBased", "README.md", args.web_root)
x_heading, z_heading = "## X. FOCUS", "## Z."
assert old_web.split(x_heading)[0] == new_web.split(x_heading)[0]
assert old_web.split(z_heading, 1)[1] == new_web.split(z_heading, 1)[1]
assert old_web.count("````") == new_web.count("````")
skill = runtime_file("focus", "SKILL.md", args.focus_root)
assert skill == snapshots["final"]["contracts"]["skill"]
assert new_web.split(x_heading, 1)[1].split(z_heading, 1)[0].strip() == snapshots["final"]["contracts"]["web"]
assert before["contracts"]["skill"].split("## Communicate")[0] == skill.split("## Communicate")[0]
for text in (skill, snapshots["final"]["contracts"]["web"]):
    assert text.count("Bad:") == text.count("Good:") == 5
    assert "Ayoub Ghriss" in text and "MIT" in text
assert runtime_file("focus", "references/license.md", args.focus_root) == git_file("4dc2ba2a7f50ed35524820586b6df520ca39fbf3:references/license.md")
assert runtime_file("WebBased", "FOCUS-LICENSE.md", args.web_root) == git_file("2fdbce1a7448932646c09f758c6d9ccb4a6e022e:FOCUS-LICENSE.md")
print("Structural checks pass: final snapshots match files; outside X, activation/priority, licenses and fence layout preserved")

print("case | skill words before/final | web words before/final")
for name, _ in before["cases"]:
    counts = []
    for variant in ("skill", "web"):
        counts.append("/".join(str(len(next(r for r in outputs[phase] if r["variant"] == variant and r["case"] == name)["response"]["result"].split())) for phase in ("before", "final")))
    print(f"{name}: {' | '.join(counts)}")
print("These checks do not establish semantic accuracy, autonomous activation or tool behavior.")
