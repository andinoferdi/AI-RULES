import contextlib
import io
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ai_rules import cli
from ai_rules.capabilities.adapters import StaticCapabilityAdapter
from ai_rules.catalog import load_catalog
from ai_rules.profiles import load_profiles
from ai_rules.resolver import ResolveRequest, build_resolver
from ai_rules.hosts.adapters import build_host_adapters
from ai_rules.hosts.invocation import invocation_paths, invocation_ready
from ai_rules.domain.statuses import Scope


class FocusSelectionTests(unittest.TestCase):
    def resolve(self, **kwargs):
        catalog = load_catalog()
        resolver = build_resolver(catalog, load_profiles(catalog), StaticCapabilityAdapter())
        return resolver.resolve(ResolveRequest(hosts=("codex",), **kwargs))

    def test_workflow_selection_installs_focus_without_extra_user_selection(self):
        plan = self.resolve(capabilities=("andino-workflow",))
        self.assertEqual({"andino-workflow", "focus"}, {t.capability_id for t in plan.targets})

    def test_focus_can_be_selected_without_workflow(self):
        catalog = load_catalog()
        self.assertIn("focus", catalog.capabilities)
        plan = self.resolve(capabilities=("focus",))
        self.assertEqual(["focus"], [t.capability_id for t in plan.targets])

    def test_every_profile_installs_focus_once(self):
        for profile in load_profiles(load_catalog()).profiles:
            with self.subTest(profile=profile):
                plan = self.resolve(profile_id=profile)
                self.assertEqual(1, [t.capability_id for t in plan.targets].count("focus"))

    def test_bundled_standalone_focus_installs_the_pinned_package(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            output = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                result = cli.main(["setup", "--host", "codex", "--capability", "focus",
                                   "--scope", "project", "--project-root", str(project),
                                   "--source", "bundled", "--non-interactive", "--yes"])
            self.assertEqual(0, result, output.getvalue())
            root = project / ".agents/skills"
            self.assertFalse((root / "andino-workflow").exists())
            self.assertIn("name: focus", (root / "focus/SKILL.md").read_text())
            self.assertIn("Copyright (c) 2026 Ayoub Ghriss",
                          (root / "focus/references/license.md").read_text())


class FocusSetupTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.upstream = self.root / "upstream"
        self.upstream.mkdir()
        self.git("init", "-b", "focus")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        for identifier in ("focus", "andino-workflow"):
            if identifier != "focus":
                self.git("checkout", "--orphan", identifier)
                self.git("rm", "-rf", ".")
            source = os.environ.get(identifier.upper().replace("-", "_") + "_RUNTIME")
            if source:
                shutil.copytree(source, self.upstream, dirs_exist_ok=True,
                                ignore=shutil.ignore_patterns(".git", "__pycache__"))
            else:
                (self.upstream / "SKILL.md").write_text(
                    f"---\nname: {identifier}\ndescription: Test skill\n---\nAnswer clearly.\n",
                    encoding="utf-8")
                (self.upstream / "README.md").write_text("Test distribution\n", encoding="utf-8")
            self.git("add", ".")
            self.git("commit", "-m", identifier)
        catalog = load_catalog()
        for identifier in ("focus", "andino-workflow"):
            catalog.require_capability(identifier).source["repository"] = str(self.upstream)
        self.catalog = catalog
        mocked = patch.object(cli, "load_catalog", return_value=catalog)
        mocked.start()
        self.addCleanup(mocked.stop)

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.upstream, text=True,
                                       encoding="utf-8", stderr=subprocess.PIPE)

    def run_setup(self, project, host, capability="andino-workflow"):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = cli.main(["setup", "--host", host, "--capability", capability,
                               "--scope", "project", "--project-root", str(project),
                               "--state-dir", str(project / ".ai-rules"), "--source", "latest",
                               "--non-interactive", "--yes"])
        self.assertEqual(0, result, output.getvalue())
        return output.getvalue()

    def test_setup_registers_focus_on_every_host_and_reinstall_is_noop(self):
        adapters = build_host_adapters(self.catalog.hosts)
        for host, adapter in adapters.items():
            with self.subTest(host=host):
                project = self.root / host
                self.run_setup(project, host)
                skill = adapter.skill_target(Scope.PROJECT, project) / "focus" / "SKILL.md"
                self.assertTrue(skill.is_file())
                self.assertEqual(self.git("show", "focus:SKILL.md"), skill.read_text(encoding="utf-8"))
                for command in invocation_paths(adapter, Scope.PROJECT, "focus", project):
                    self.assertTrue(invocation_ready(command))
                    self.assertIn(skill.as_posix(), command.read_text(encoding="utf-8"))
                self.assertIn("NO_OP", self.run_setup(project, host))

    def test_standalone_focus_updates_without_installing_workflow_or_touching_other_skills(self):
        project = self.root / "standalone"
        unrelated = project / ".agents/skills/user-skill/SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("User content", encoding="utf-8")
        self.run_setup(project, "codex", "focus")
        self.assertFalse((project / ".agents/skills/andino-workflow").exists())
        self.git("checkout", "focus")
        (self.upstream / "README.md").write_text("Updated source\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "update focus")
        self.assertIn("UPDATE", self.run_setup(project, "codex", "focus"))
        self.assertEqual("Updated source\n", (project / ".agents/skills/focus/README.md").read_text())
        self.assertEqual("User content", unrelated.read_text())
