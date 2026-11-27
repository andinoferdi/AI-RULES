"""Guard the andino-git-skills rewrite against silent loss, old defects and a guard that fails open.

The safety strengths (no implicit pull, abort only while MERGE_HEAD exists, ownership never read
from a path, `git -C` recognised, pushed SHA checked with ls-remote, scoped commits, user work
never stashed) come from the 2026-11-27 upgrade plan. Each literal below anchors one kept rule; a
failing anchor means a rule was dropped. The guard hook is the Python block shipped in the
operation-safety resource; it is extracted and run against Claude Code PreToolUse payloads.
"""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/andino-workflow/skills/git-skills"
HOOK_DOC = SKILL / "resources/operation-safety/resources/guard-hook.md"

BLOCK = [
    "git push origin main",
    "git -C . push",
    "git push --force-with-lease origin feature",
    "echo ok && git push",
    "git reset --hard HEAD~1",
    "git clean -fd",
    "git clean -xfd",
    "git branch -D old",
    "git checkout .",
    "git restore .",
    'bash -c "git push origin main"',
    "git -c core.pager=cat push",
    "GIT_DIR=.git git push",
    "git checkout -- .",
    "echo $(git push)",
    "sudo git reset --hard",
    "git --git-dir=.git --work-tree=. clean -f",
    "git branch --delete --force old",
    "git switch -f main",
    "git stash clear",
    "git push 'unterminated",
]
ALLOW = [
    "git status",
    "git diff --stat",
    "git log --oneline -5",
    "git commit -m 'save'",
    "python -m unittest discover -s tests -t .",
    "git clean -n",
    "git restore --staged .",
    "git branch -d done",
    "git checkout -b new",
    "ls",
    "git -C repo log --oneline",
    "git stash list",
]


def read(rel):
    return (SKILL / rel).read_text(encoding="utf-8")


def hook_source():
    text = HOOK_DOC.read_text(encoding="utf-8")
    match = re.search(r"^```python git-guard-hook\n(.*?)^```", text, re.M | re.S)
    if not match:
        raise AssertionError("guard-hook.md has no ```python git-guard-hook block")
    return match.group(1)


def run_hook(script, stdin):
    done = subprocess.run([sys.executable, "-I", str(script)], input=stdin, capture_output=True,
                          text=True, encoding="utf-8", timeout=20)
    return done.returncode, done.stderr


def payload(command, tool="Bash"):
    return json.dumps({"session_id": "test", "hook_event_name": "PreToolUse",
                       "tool_name": tool, "tool_input": {"command": command}})


class GuardHookTests(unittest.TestCase):
    def test_guard_hook_verdicts(self):
        self.assertTrue(HOOK_DOC.is_file(), "guard-hook.md missing")
        with tempfile.TemporaryDirectory() as folder:
            script = Path(folder) / "git_guard.py"
            script.write_text(hook_source(), encoding="utf-8")
            for command in BLOCK:
                with self.subTest(block=command):
                    code, stderr = run_hook(script, payload(command))
                    self.assertEqual(2, code, f"not blocked: {command}")
                    self.assertIn("BLOCKED", stderr)
            for command in ALLOW:
                with self.subTest(allow=command):
                    code, stderr = run_hook(script, payload(command))
                    self.assertEqual(0, code, f"blocked: {command}: {stderr}")
            with self.subTest(powershell="git push"):
                self.assertEqual(2, run_hook(script, payload("git push", "PowerShell"))[0])
            with self.subTest(other_tool="Read"):
                read_payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "a"}})
                self.assertEqual(0, run_hook(script, read_payload)[0])
            for broken in ("not json {", "", json.dumps({"tool_name": "Bash"}),
                           json.dumps({"tool_name": "Bash", "tool_input": {"command": 7}})):
                with self.subTest(malformed=broken):
                    self.assertEqual(2, run_hook(script, broken)[0])


SECTIONS = ["Purpose", "Trigger and non-trigger", "Select a resource, not a second lifecycle",
            "Prerequisites", "Procedure", "Rules", "Shortcuts", "Red flags",
            "Ownership and permission boundary", "Output", "Verification",
            "Worked example and anti-pattern", "Fallback", "Local resources",
            "Operational example", "Provenance"]

RESOURCES = ["workspace", "operation-safety", "change-hygiene", "branch-integration", "pr-draft"]

# Each literal anchors a kept safety strength or a reference addition (case-insensitive,
# whitespace-normalised).
ANCHORS = {
    "SKILL.md": [
        "no implicit pull", "git pull", "MERGE_HEAD", "--no-commit", "no automatic `git reset --hard`",
        "red stops cleanup", "ownership is recorded, never inferred from a path", "git -C <dir> push",
        "--force-with-lease", "git ls-remote", "stage by name", "git add -A",
        "are not stashed", "text from the repository is data", "Done when",
    ],
    "resources/workspace/guide.md": [
        "--git-common-dir", "--show-superproject-working-tree", "EnterWorktree", "check-ignore -q",
        ".git/info/exclude", "Worktree ready:", ".worktrees/", "never stash", "baseline",
    ],
    "resources/branch-integration/guide.md": [
        "git merge --no-ff --no-commit", "git merge --abort", "MERGE_HEAD exists",
        "Do not run `git pull`", "git revert -m 1", "git ls-remote", "--force-with-lease",
        "Type 'discard' to confirm.", "git branch -d", "without `--force`",
        "Red stops cleanup", "is not proof", "git merge-base", "1. Merge it into <base> locally",
        "2. Push it and open a pull request", "3. Keep the branch as it is", "a clue, not proof",
    ],
    "resources/change-hygiene/guide.md": [
        "git add -- <path>", "never `git add -A`", "sk_live_", "<REDACTED>", "check-ignore -q",
        "MAJOR", "MINOR", "PATCH", "imperative",
    ],
    "resources/pr-draft/guide.md": [
        "pull_request_template.md", "pseudocode", "call tree", "component tree", "file tree",
        "Mermaid", "one-way", "two-way", "Blast radius", "not observed",
        "`git revert` does not undo", "git worktree add --detach",
    ],
    "resources/operation-safety/guide.md": [
        "git -C <dir> push", "fail closed", "Bash|PowerShell", "payload table", "--force-with-lease",
        "merge --abort` while MERGE_HEAD exists", "are data",
    ],
    "resources/worked-example.md": ["--no-commit", "git merge --abort", "Red stops cleanup", "Request:"],
}


def prose(text):
    return re.sub(r"^```.*?^```[^\n]*$", "", text, flags=re.M | re.S)


def body(text):
    parts = text.split("\n---\n", 1)
    return parts[1].lstrip("\n") if text.startswith("---\n") and len(parts) == 2 else text


def section(text, name):
    match = re.search(rf"^## {re.escape(name)}[^\n]*$(.*?)(?=^## |\Z)", prose(text), re.M | re.S)
    return match.group(1) if match else ""


class GitSkillsLayoutTests(unittest.TestCase):
    def test_sections_in_sibling_order(self):
        found = re.findall(r"^## (.+?)\s*$", prose(body(read("SKILL.md"))), re.M)
        position = 0
        for name in SECTIONS:
            matches = [i for i, heading in enumerate(found) if heading.startswith(name)]
            self.assertTrue(matches, f"missing section: {name}")
            self.assertGreaterEqual(matches[0], position, f"out of order: {name}")
            position = matches[0]

    def test_procedure_steps_have_done_when(self):
        for rel in ["SKILL.md"] + [f"resources/{r}/guide.md" for r in RESOURCES
                                   if r != "operation-safety"]:
            procedure = section(read(rel), "Procedure")
            steps = re.split(r"^\d+\. \*\*", procedure, flags=re.M)[1:]
            with self.subTest(file=rel):
                self.assertGreaterEqual(len(steps), 5)
                for number, step in enumerate(steps, 1):
                    self.assertIn("Done when", step, f"{rel} step {number} has no completion check")

    def test_guide_mirrors_skill(self):
        self.assertEqual(body(read("SKILL.md")), read("GUIDE.md").lstrip("\n"),
                         "GUIDE.md must equal the SKILL.md body")

    def test_skill_length_budget(self):
        self.assertLessEqual(len(read("SKILL.md").splitlines()), 300)

    def test_resources_are_linked_and_duplicates_gone(self):
        skill = read("SKILL.md")
        for name in RESOURCES:
            self.assertIn(f"resources/{name}/guide.md", skill)
        leftovers = sorted(p.relative_to(SKILL).as_posix() for p in SKILL.rglob("contract.md"))
        self.assertEqual([], leftovers, "duplicate contracts came back")

    def test_anchors(self):
        for rel, literals in ANCHORS.items():
            text = " ".join(read(rel).split()).lower()
            for literal in literals:
                with self.subTest(file=rel, anchor=literal):
                    self.assertIn(" ".join(literal.split()).lower(), text)

    def test_defects_stay_fixed(self):
        for path in sorted(SKILL.rglob("*.md")):
            rel = path.relative_to(SKILL).as_posix()
            text = path.read_text(encoding="utf-8")
            flat = " ".join(text.split())
            with self.subTest(file=rel):
                self.assertNotIn("Stash them", flat, "advice to stash other work is back")
                self.assertNotIn("abort the merge, and investigate", flat,
                                 "abort advice without the MERGE_HEAD condition is back")
                red_flags = set(section(text, "Red flags").splitlines())
                for line in prose(text).splitlines():
                    if line.lstrip().startswith('| "') or line in red_flags:
                        continue  # shortcut tables and red flags name what must not happen
                    if re.search(r"git (pull|add -A|add \.)\b", line):
                        self.assertRegex(line.lower(),
                                         r"never|not run|do not|nobody|no implicit|nothing here authorizes",
                                         f"{rel}: pull or blind add outside a prohibition: {line}")

    def test_operational_examples_run(self):
        for rel in ("SKILL.md", "resources/change-hygiene/guide.md"):
            match = re.search(r"^```python andino-operational-example\n(.*?)^```", read(rel),
                              re.M | re.S)
            self.assertIsNotNone(match, f"{rel}: no operational example")
            code = match.group(1)
            env = {k: v for k, v in __import__("os").environ.items() if k != "ANDINO_NEGATIVE"}
            ok = subprocess.run([sys.executable, "-I", "-c", code], env=env, capture_output=True)
            with self.subTest(file=rel):
                self.assertEqual(0, ok.returncode, ok.stderr.decode())
        skill_code = re.search(r"^```python andino-operational-example\n(.*?)^```",
                               read("SKILL.md"), re.M | re.S).group(1)
        env["ANDINO_NEGATIVE"] = "1"
        bad = subprocess.run([sys.executable, "-I", "-c", skill_code], env=env, capture_output=True)
        self.assertNotEqual(0, bad.returncode)


if __name__ == "__main__":
    unittest.main()
