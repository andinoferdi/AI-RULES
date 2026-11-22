"""setup inside a clone installs the skills/ folder as it is on disk, edits included."""

import contextlib
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ai_rules import cli
from ai_rules.catalog import load_catalog
from ai_rules.release.checkout import find_checkout

ROOT = Path(__file__).resolve().parents[2]


class LocalSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # A clone-shaped folder that is not a Git repository: local source must not need one.
        self.checkout = self.root / "AI-RULES"
        marker = self.checkout / "src/ai_rules/catalog/data/capabilities.json"
        marker.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "src/ai_rules/catalog/data/capabilities.json", marker)
        for identifier in ("andino-workflow", "focus", "search-first"):
            package = self.checkout / "skills" / identifier
            package.mkdir(parents=True)
            (package / "SKILL.md").write_text(
                f"---\nname: {identifier}\ndescription: Fixture {identifier}\n---\nBody\n",
                encoding="utf-8", newline="\n")
            (package / "README.md").write_text("Fixture\n", encoding="utf-8", newline="\n")
        self.project = self.root / "project"
        self.state = self.root / "state"

    def run_cli(self, source, cwd=None):
        output = io.StringIO()
        with contextlib.chdir(cwd or self.checkout), \
                contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = cli.main(["setup", "--host", "codex", "--profile", "minimal",
                               "--scope", "project", "--project-root", str(self.project),
                               "--state-dir", str(self.state), "--source", source,
                               "--non-interactive", "--yes"])
        return result, output.getvalue()

    def test_checkout_is_found_from_a_nested_folder(self):
        nested = self.checkout / "skills/focus"
        self.assertEqual(self.checkout.resolve(), find_checkout(nested))
        self.assertIsNone(find_checkout(self.root))

    def test_local_source_installs_uncommitted_edit(self):
        result, output = self.run_cli("local")
        self.assertEqual(0, result, output)
        self.assertIn("Skill source: local folder", output)
        skill = self.checkout / "skills/focus/SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "local edit marker\n", encoding="utf-8")
        result, output = self.run_cli("local")
        self.assertEqual(0, result, output)
        installed = self.project / ".agents/skills/focus/SKILL.md"
        self.assertIn("local edit marker", installed.read_text(encoding="utf-8"))
        lock = json.loads((self.state / "lock.json").read_text())
        self.assertEqual("verified", lock["status"])
        actions = {t["capability"]: t["action"] for t in lock["targets"]}
        self.assertEqual("UPDATE", actions["focus"])
        self.assertEqual("NO_OP", actions["andino-workflow"])

    def test_crlf_edit_on_windows_matches_installed_copy(self):
        self.assertEqual(0, self.run_cli("local")[0])
        skill = self.checkout / "skills/focus/SKILL.md"
        skill.write_bytes(skill.read_bytes().replace(b"\n", b"\r\n") + b"crlf edit\r\n")
        result, output = self.run_cli("local")
        self.assertEqual(0, result, output)
        self.assertEqual("verified", json.loads((self.state / "lock.json").read_text())["status"])

    def test_auto_source_uses_checkout_inside_clone(self):
        result, output = self.run_cli("auto")
        self.assertEqual(0, result, output)
        self.assertIn("Skill source: local folder", output)
        self.assertTrue((self.project / ".agents/skills/andino-workflow/SKILL.md").is_file())

    def test_local_source_works_when_git_opens_only_explicit_bare_repositories(self):
        # safe.bareRepository=explicit is a Git hardening setting; some terminals set it.
        with patch.dict(os.environ, {"GIT_CONFIG_PARAMETERS": "'safe.bareRepository=explicit'"}):
            result, output = self.run_cli("local")
        self.assertEqual(0, result, output)
        self.assertTrue((self.project / ".agents/skills/focus/SKILL.md").is_file())

    def test_auto_source_uses_github_outside_clone(self):
        with patch.object(cli, "LatestSources", side_effect=RuntimeError("remote")) as remote:
            result, output = self.run_cli("auto", cwd=self.root)
        self.assertEqual(2, result, output)
        self.assertIn("Skill source: GitHub main", output)
        self.assertIsNone(remote.call_args.kwargs.get("local_root"))

    def test_local_source_outside_checkout_is_an_error(self):
        result, output = self.run_cli("local", cwd=self.root)
        self.assertEqual(2, result)
        self.assertIn("runs inside an AI-RULES clone", output)
        self.assertFalse(self.project.exists())


class SourceBranchOverrideTests(unittest.TestCase):
    def test_source_branch_override_fetches_named_branch(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = root / "upstream"
            remote.mkdir()
            git = lambda *args: subprocess.check_output(["git", "-C", str(remote), *args], text=True,
                                                         stderr=subprocess.PIPE)
            git("init", "-b", "main")
            git("config", "user.name", "Fixture")
            git("config", "user.email", "fixture@example.invalid")
            for body in ("main body", "feature body"):
                if body == "feature body":
                    git("checkout", "-b", "feature")
                for identifier in ("andino-workflow", "focus", "search-first"):
                    package = remote / "skills" / identifier
                    package.mkdir(parents=True, exist_ok=True)
                    (package / "SKILL.md").write_text(
                        f"---\nname: {identifier}\ndescription: Fixture\n---\n{body}\n", encoding="utf-8")
                git("add", ".")
                git("commit", "-m", body)
            catalog = load_catalog()
            for identifier in ("andino-workflow", "focus", "search-first"):
                catalog.require_capability(identifier).source["repository"] = str(remote)
            project = root / "project"
            output = io.StringIO()
            with patch.object(cli, "load_catalog", return_value=catalog), \
                    patch.dict(os.environ, {"AI_RULES_SOURCE_BRANCH": "feature"}), \
                    contextlib.chdir(root), contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                result = cli.main(["setup", "--host", "codex", "--profile", "minimal", "--scope", "project",
                                   "--project-root", str(project), "--state-dir", str(root / "state"),
                                   "--source", "latest", "--non-interactive", "--yes"])
            self.assertEqual(0, result, output.getvalue())
            self.assertIn("branch feature", output.getvalue())
            self.assertIn("feature body", (project / ".agents/skills/focus/SKILL.md").read_text())


if __name__ == "__main__":
    unittest.main()
