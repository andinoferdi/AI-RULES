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
from ai_rules.capabilities.adapters import StaticCapabilityAdapter
from ai_rules.catalog import load_catalog
from ai_rules.domain.statuses import Scope
from ai_rules.hosts.adapters import build_host_adapters
from ai_rules.hosts.invocation import invocation_paths, invocation_ready
from ai_rules.profiles import load_profiles
from ai_rules.release import export_git_ref
from ai_rules.release.latest import contents
from ai_rules.resolver import ResolveRequest, build_resolver


class SearchFirstSelectionTests(unittest.TestCase):
    def resolve(self, **kwargs):
        catalog = load_catalog()
        resolver = build_resolver(catalog, load_profiles(catalog), StaticCapabilityAdapter())
        return resolver.resolve(ResolveRequest(hosts=("codex",), **kwargs))

    def test_standalone_search_first_has_no_workflow_dependency(self):
        self.assertIn("search-first", load_catalog().capabilities)
        plan = self.resolve(capabilities=("search-first",))
        self.assertEqual(["search-first"], [t.capability_id for t in plan.targets])

    def test_workflow_requires_both_supporting_skills_once(self):
        plan = self.resolve(capabilities=("andino-workflow",))
        self.assertCountEqual(["andino-workflow", "focus", "search-first"],
                              [t.capability_id for t in plan.targets])

    def test_every_profile_resolves_search_first_once(self):
        for profile in load_profiles(load_catalog()).profiles:
            with self.subTest(profile=profile):
                plan = self.resolve(profile_id=profile)
                self.assertEqual(1, [t.capability_id for t in plan.targets].count("search-first"))

    def test_focus_remains_independent(self):
        self.assertEqual(["focus"], [t.capability_id for t in
                                   self.resolve(capabilities=("focus",)).targets])

    def test_explicit_dependencies_are_deduplicated(self):
        plan = self.resolve(capabilities=("andino-workflow", "search-first", "focus"))
        self.assertCountEqual(["andino-workflow", "focus", "search-first"],
                              [t.capability_id for t in plan.targets])


class SearchFirstSetupTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('AI_RULES_SEARCH_FIRST_CANDIDATE'),
                         'Opt-in uncommitted distribution installation check')
    def test_candidate_reference_installs_on_all_hosts_and_user_edit_is_preserved(self):
        candidate = Path(os.environ['AI_RULES_SEARCH_FIRST_CANDIDATE'])
        self.assertTrue((candidate / 'references/online-research.md').is_file())
        self.git('switch', 'search-first')
        for name, body in contents(candidate).items():
            if name.startswith('.'):
                continue
            target = self.upstream / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(candidate / name, target)
        self.git('add', '.')
        if self.git('diff', '--cached', '--name-only').strip():
            self.git('commit', '-m', 'Disposable uncommitted candidate fixture')
        for host, adapter in build_host_adapters(self.catalog.hosts).items():
            with self.subTest(host=host):
                project = self.root / 'candidate' / host
                self.run_setup(project, '--capability', 'andino-workflow', host=host)
                skill = adapter.skill_target(Scope.PROJECT, project) / 'search-first'
                reference = skill / 'references/online-research.md'
                self.assertEqual((candidate / 'references/online-research.md').read_text(encoding='utf-8'),
                                 reference.read_text(encoding='utf-8'))
                self.assertIn('NO_OP', self.run_setup(project, '--capability', 'andino-workflow', host=host))
                reference.write_text('User-owned reference edits', encoding='utf-8')
                self.run_setup(project, '--capability', 'search-first', host=host, expected=1)
                self.assertEqual('User-owned reference edits', reference.read_text(encoding='utf-8'))

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = Path(__file__).resolve().parents[2]
        self.upstream = self.root / "upstream"
        self.upstream.mkdir()
        self.git("init", "-b", "search-first")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        manifest = json.loads((self.repo / "src/ai_rules/release/data/release_manifest.json").read_text())
        self.pins = manifest["first_party"]
        self.catalog = load_catalog()
        for identifier in ("search-first", "focus", "andino-workflow"):
            if identifier != "search-first":
                self.git("switch", "--orphan", identifier)
            export_git_ref(self.pins[identifier]["commit"], self.upstream, repo_root=self.repo)
            self.git("add", ".")
            self.git("commit", "-m", identifier)
            self.catalog.require_capability(identifier).source["repository"] = str(self.upstream)
        mocked = patch.object(cli, "load_catalog", return_value=self.catalog)
        mocked.start()
        self.addCleanup(mocked.stop)

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.upstream, text=True,
                                       encoding="utf-8", stderr=subprocess.PIPE)

    def run_setup(self, project, *selection, host="codex", source="latest", expected=0):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = cli.main(["setup", "--host", host, "--scope", "project",
                               "--project-root", str(project), "--state-dir", str(project / ".ai-rules"),
                               "--source", source, "--non-interactive", "--yes", *selection])
        if expected == 0:
            self.assertEqual(0, result, output.getvalue())
        else:
            self.assertNotEqual(0, result, output.getvalue())
        return output.getvalue()

    def test_actual_packages_install_on_all_hosts_and_repeat_preserves_files(self):
        for source in ("latest", "bundled"):
            for host, adapter in build_host_adapters(self.catalog.hosts).items():
                with self.subTest(source=source, host=host):
                    project = self.root / source / host
                    self.run_setup(project, "--capability", "andino-workflow", host=host, source=source)
                    root = adapter.skill_target(Scope.PROJECT, project)
                    self.assertEqual({"andino-workflow", "focus", "search-first"},
                                     {p.name for p in root.iterdir()})
                    skill = root / "search-first"
                    expected_files = set(self.git("ls-tree", "-r", "--name-only", "search-first").splitlines())
                    self.assertTrue({"SKILL.md", "README.md", "references/license.md"}.issubset(expected_files))
                    self.assertEqual(expected_files, set(contents(skill)))
                    for name in expected_files:
                        self.assertEqual(self.git("show", f"search-first:{name}"),
                                         (skill / name).read_text(encoding="utf-8"))
                    for command in invocation_paths(adapter, Scope.PROJECT, "search-first", project):
                        self.assertTrue(invocation_ready(command))
                        self.assertIn((skill / "SKILL.md").as_posix(), command.read_text(encoding="utf-8"))
                    before = {p.relative_to(skill): p.stat().st_mtime_ns for p in skill.rglob("*") if p.is_file()}
                    self.assertIn("NO_OP", self.run_setup(project, "--capability", "andino-workflow", host=host, source=source))
                    self.assertEqual(before, {p.relative_to(skill): p.stat().st_mtime_ns for p in skill.rglob("*") if p.is_file()})

    def test_standalone_latest_updates_without_touching_unrelated_skills(self):
        project = self.root / "standalone"
        unrelated = project / ".agents/skills/user-skill/SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("User-owned content", encoding="utf-8")
        self.run_setup(project, "--capability", "search-first")
        self.assertFalse((project / ".agents/skills/andino-workflow").exists())
        self.assertFalse((project / ".agents/skills/focus").exists())
        self.git("switch", "search-first")
        readme = self.upstream / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\nUpdated release.\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-m", "later search-first revision")
        self.assertIn("UPDATE", self.run_setup(project, "--capability", "search-first"))
        self.assertEqual(readme.read_text(encoding="utf-8"), (project / ".agents/skills/search-first/README.md").read_text(encoding="utf-8"))
        self.assertEqual("User-owned content", unrelated.read_text())
        lock = json.loads((project / ".ai-rules/lock.json").read_text())
        self.assertIn(self.git("rev-parse", "HEAD").strip(), lock["targets"][0]["target_version"])

    def test_local_modification_is_blocked_and_preserved(self):
        project = self.root / "modified"
        self.run_setup(project, "--capability", "search-first")
        skill = project / ".agents/skills/search-first/SKILL.md"
        skill.write_text("User edits", encoding="utf-8")
        self.run_setup(project, "--capability", "search-first", expected=1)
        self.assertEqual("User edits", skill.read_text())

    def test_alternate_discovery_root_is_preserved_without_duplicate(self):
        project = self.root / "alias"
        alias = project / ".claude/skills/search-first/SKILL.md"
        alias.parent.mkdir(parents=True)
        alias.write_text("User installation", encoding="utf-8")
        self.run_setup(project, "--capability", "search-first", host="opencode", expected=1)
        self.assertEqual("User installation", alias.read_text())
        self.assertFalse((project / ".agents/skills/search-first").exists())

    def test_embedded_bundle_installs_pinned_files_without_git_fallback(self):
        bundle = self.root / "embedded"
        export_git_ref(self.pins["search-first"]["commit"], bundle, repo_root=self.repo)
        project = self.root / "frozen"
        with patch.object(cli, "packaged_bundle", return_value=bundle), \
                patch.object(cli, "export_git_ref", side_effect=AssertionError("embedded package must not need Git")):
            self.run_setup(project, "--capability", "search-first", source="bundled")
        self.assertEqual(contents(bundle), contents(project / ".agents/skills/search-first"))
        self.assertFalse((project / ".agents/skills/andino-workflow").exists())
        lock = json.loads((project / ".ai-rules/lock.json").read_text())
        self.assertIn(self.pins["search-first"]["commit"], lock["targets"][0]["target_version"])

    def test_default_profile_uses_normal_setup_dependency_resolution(self):
        project = self.root / "default"
        self.run_setup(project)
        self.assertEqual({"andino-workflow", "focus", "search-first"},
                         {p.name for p in (project / ".agents/skills").iterdir()})
