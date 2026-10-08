import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from ai_rules import cli
from ai_rules.catalog import load_catalog
from ai_rules.interactive import InteractiveSelection


class LiveUpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.remote = self.root / "upstream"
        self.remote.mkdir()
        self.git(self.remote, "init", "-b", "andino-workflow")
        self.git(self.remote, "config", "user.name", "Fixture")
        self.git(self.remote, "config", "user.email", "fixture@example.invalid")
        self.commit("old", extra=True)
        self.old = self.git(self.remote, "rev-parse", "HEAD").strip()
        self.project = self.root / "project"
        self.target = self.project / ".agents/skills/andino-workflow"
        self.state = self.root / "state"
        self.catalog = load_catalog()
        self.catalog.require_capability("andino-workflow").source["repository"] = str(self.remote)
        self.catalog_patch = patch.object(cli, "load_catalog", return_value=self.catalog)
        self.catalog_patch.start()
        self.addCleanup(self.catalog_patch.stop)

    def git(self, cwd, *args):
        return subprocess.check_output(["git", *args], cwd=cwd, text=True, encoding="utf-8", stderr=subprocess.PIPE)

    def commit(self, content, extra=False):
        (self.remote / "SKILL.md").write_text(
            "---\nname: andino-workflow\ndescription: Fixture workflow\n---\n" + content + "\n", encoding="utf-8")
        (self.remote / "README.md").write_text("Fixture\n", encoding="utf-8")
        if extra:
            (self.remote / "obsolete.md").write_text("old\n", encoding="utf-8")
        self.git(self.remote, "add", ".")
        self.git(self.remote, "commit", "-m", content)

    def run_cli(self, *extra, command="setup"):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = cli.main([command, "--host", "codex", "--profile", "minimal",
                               "--scope", "project", "--project-root", str(self.project),
                               "--state-dir", str(self.state), "--source", "latest",
                               "--non-interactive", "--yes", *extra])
        return result, output.getvalue()

    def copy_old(self):
        self.target.mkdir(parents=True)
        for name in ("SKILL.md", "README.md", "obsolete.md"):
            shutil.copyfile(self.remote / name, self.target / name)

    def test_existing_copy_updates_and_later_commit_needs_no_cli_release(self):
        self.copy_old()
        (self.remote / "obsolete.md").unlink()
        self.commit("new")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertIn("new", (self.target / "SKILL.md").read_text())
        self.assertFalse((self.target / "obsolete.md").exists())
        self.assertTrue(list((self.state / "backups").glob("*/andino-workflow/SKILL.md")))
        self.commit("third")
        result, output = self.run_cli(command="update")
        self.assertEqual(0, result, output)
        self.assertIn("third", (self.target / "SKILL.md").read_text())
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertIn("NO_OP", output)
        lock = json.loads((self.state / "lock.json").read_text())
        self.assertEqual("verified", lock["status"])
        self.assertIn(self.git(self.remote, "rev-parse", "HEAD").strip(), lock["targets"][0]["target_version"])

    def test_current_skill_gets_missing_command_and_setup_repairs_deleted_command(self):
        self.copy_old()
        command = self.project / ".opencode/commands/andino-workflow.md"
        result, output = self.run_cli("--host", "opencode")
        self.assertEqual(0, result, output)
        self.assertIn("RECONFIGURE", output)
        self.assertIn("$ARGUMENTS", command.read_text())
        self.assertIn(self.target.joinpath("SKILL.md").as_posix(), command.read_text())
        command.unlink()
        result, output = self.run_cli("--host", "opencode", "--dry-run")
        self.assertEqual(0, result, output)
        self.assertFalse(command.exists())
        result, output = self.run_cli("--host", "opencode")
        self.assertEqual(0, result, output)
        self.assertTrue(command.exists())
        result, output = self.run_cli("--host", "opencode")
        self.assertEqual(0, result, output)
        self.assertNotIn("RECONFIGURE", output)

    def test_existing_user_command_is_preserved(self):
        command = self.project / ".opencode/commands/andino-workflow.md"
        command.parent.mkdir(parents=True)
        body = "---\ndescription: Personal workflow\n---\n\nUse my preferred workflow.\n"
        command.write_text(body)
        result, output = self.run_cli("--host", "opencode")
        self.assertEqual(0, result, output)
        self.assertEqual(body, command.read_text())

    def test_invalid_command_blocks_without_overwriting(self):
        command = self.project / ".opencode/commands/andino-workflow.md"
        command.parent.mkdir(parents=True)
        command.write_text("personal notes\n")
        result, output = self.run_cli("--host", "opencode")
        self.assertNotEqual(0, result, output)
        self.assertEqual("personal notes\n", command.read_text())
        lock = json.loads((self.state / "lock.json").read_text())
        self.assertEqual("SKIPPED", next(t["status"] for t in lock["targets"] if t["host"] == "opencode"))

    def test_ide_workflow_loads_skill_without_copying_body(self):
        result, output = self.run_cli("--host", "antigravity-ide")
        self.assertEqual(0, result, output)
        command = self.project / ".agents/workflows/andino-workflow.md"
        self.assertIn(self.target.joinpath("SKILL.md").as_posix(), command.read_text())
        self.assertNotIn("$ARGUMENTS", command.read_text())

    def test_clean_clone_fast_forwards_without_replacing_git_metadata(self):
        self.target.parent.mkdir(parents=True)
        self.git(self.root, "clone", str(self.remote), str(self.target))
        self.commit("new")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertEqual(self.git(self.remote, "rev-parse", "HEAD"), self.git(self.target, "rev-parse", "HEAD"))
        self.assertEqual(str(self.remote), self.git(self.target, "remote", "get-url", "origin").strip())

    def test_user_edits_are_preserved_and_never_reported_current(self):
        self.copy_old()
        (self.target / "SKILL.md").write_text("personal edits\n", encoding="utf-8")
        self.commit("new")
        result, output = self.run_cli()
        self.assertNotEqual(0, result)
        self.assertIn("BLOCK", output)
        self.assertEqual("personal edits\n", (self.target / "SKILL.md").read_text())

    def test_failed_source_lookup_is_not_a_successful_noop(self):
        self.copy_old()
        self.catalog.require_capability("andino-workflow").source["repository"] = str(self.root / "missing")
        result, output = self.run_cli()
        self.assertNotEqual(0, result)
        self.assertNotIn("All selected skills are ready", output)
        self.assertFalse((self.state / "lock.json").exists())

    def test_latest_is_default_and_fetches_from_non_repository_cwd(self):
        self.assertEqual("latest", cli.build_parser().parse_args(["setup"]).source)
        original = Path.cwd()
        try:
            os.chdir(self.root)
            result, output = self.run_cli()
        finally:
            os.chdir(original)
        self.assertEqual(0, result, output)
        self.assertTrue((self.target / "SKILL.md").is_file())

    def test_dry_run_does_not_change_installation_or_persist_state(self):
        self.copy_old()
        self.commit("new")
        result, output = self.run_cli("--dry-run")
        self.assertEqual(0, result, output)
        self.assertIn("old", (self.target / "SKILL.md").read_text())
        self.assertFalse(self.state.exists())

    def test_extra_local_file_blocks_update(self):
        self.copy_old()
        (self.target / "my-notes.md").write_text("keep me\n")
        self.commit("new")
        result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        self.assertEqual("keep me\n", (self.target / "my-notes.md").read_text())

    def test_dirty_clone_is_preserved(self):
        self.target.parent.mkdir(parents=True)
        self.git(self.root, "clone", str(self.remote), str(self.target))
        (self.target / "README.md").write_text("local edits\n")
        self.commit("new")
        result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        self.assertEqual(self.old, self.git(self.target, "rev-parse", "HEAD").strip())
        self.assertEqual("local edits\n", (self.target / "README.md").read_text())

    def test_shared_project_root_is_updated_once_and_verified_for_each_host(self):
        self.copy_old()
        self.commit("new")
        result, output = self.run_cli("--host", "opencode", "--host", "antigravity-cli")
        self.assertEqual(0, result, output)
        self.assertEqual(1, len(list((self.state / "backups").glob("*/andino-workflow"))))
        lock = json.loads((self.state / "lock.json").read_text())
        self.assertEqual(3, len(lock["targets"]))
        self.assertEqual("verified", lock["status"])

    def test_edit_after_planning_is_not_overwritten(self):
        self.copy_old()
        self.commit("new")
        executor_for_plan = cli._executor_for_plan

        def intervene(plan, args):
            (self.target / "README.md").write_text("concurrent edit\n")
            return executor_for_plan(plan, args)

        with patch.object(cli, "_executor_for_plan", side_effect=intervene):
            result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        self.assertEqual("concurrent edit\n", (self.target / "README.md").read_text())

    def test_same_skill_on_another_configured_branch_is_dynamic(self):
        self.git(self.remote, "checkout", "-b", "workflow-next")
        self.catalog.require_capability("andino-workflow").source["branch"] = "workflow-next"
        self.commit("alternate")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertIn("alternate", (self.target / "SKILL.md").read_text())
        self.commit("alternate next")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertIn("alternate next", (self.target / "SKILL.md").read_text())

    def test_all_selected_skills_use_their_own_branch(self):
        self.git(self.remote, "checkout", "-b", "ai-codebase-rescue")
        (self.remote / "SKILL.md").write_text("---\nname: ai-codebase-rescue\ndescription: Rescue\n---\nrescue\n")
        self.git(self.remote, "add", ".")
        self.git(self.remote, "commit", "-m", "rescue")
        self.catalog.require_capability("ai-codebase-rescue").source["repository"] = str(self.remote)
        with patch.object(cli, "_release_manifest", return_value={}):
            result, output = self.run_cli("--profile", "engineering")
        self.assertEqual(0, result, output)
        self.assertIn("old", (self.target / "SKILL.md").read_text())
        self.assertIn("rescue", (self.target.parent / "ai-codebase-rescue/SKILL.md").read_text())
        records = json.loads((self.state / "managed-installations.json").read_text())
        self.assertTrue(all(entry["kind"] == "first-party-skill" and "source" in entry
                            for entry in records["installations"].values()))

    def test_linked_installation_updates_its_target_and_preserves_link(self):
        self.copy_old()
        linked = self.root / "shared-skill"
        self.target.rename(linked)
        try:
            self.target.symlink_to(linked, target_is_directory=True)
        except OSError:
            if os.name != "nt":
                raise
            subprocess.run(["cmd", "/c", "mklink", "/J", str(self.target), str(linked)],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.commit("new")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertEqual(linked, self.target.resolve())
        self.assertIn("new", (linked / "SKILL.md").read_text())

    def test_current_copy_changed_after_planning_is_not_verified(self):
        self.copy_old()
        executor_for_plan = cli._executor_for_plan

        def intervene(plan, args):
            (self.target / "README.md").write_text("concurrent edit\n")
            return executor_for_plan(plan, args)

        with patch.object(cli, "_executor_for_plan", side_effect=intervene):
            result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        lock = json.loads((self.state / "lock.json").read_text())
        self.assertNotEqual("verified", lock["status"])

    @unittest.skipUnless(os.name == "nt", "Windows junction discovery regression")
    def test_antigravity_junction_is_not_reported_current(self):
        self.copy_old()
        linked = self.root / "shared-skill"
        self.target.rename(linked)
        subprocess.run(["powershell", "-NoProfile", "-Command",
                        "New-Item -ItemType Junction -Path $env:TEST_SKILL_LINK -Target $env:TEST_SKILL_TARGET"],
                       env=dict(os.environ, TEST_SKILL_LINK=str(self.target), TEST_SKILL_TARGET=str(linked)),
                       check=True, stdout=subprocess.PIPE)
        for host in ("antigravity-cli", "antigravity-ide"):
            with self.subTest(host=host):
                result, output = self.run_cli("--host", host)
                self.assertNotEqual(0, result, output)
                self.assertIn("junction", output)
                self.assertEqual(linked, self.target.resolve())
                self.assertIn("old", (linked / "SKILL.md").read_text())
        lock = json.loads((self.state / "lock.json").read_text())
        self.assertNotEqual("verified", lock["status"])

    def test_git_branch_advances_even_when_commit_does_not_change_files(self):
        self.target.parent.mkdir(parents=True)
        self.git(self.root, "clone", str(self.remote), str(self.target))
        self.git(self.remote, "commit", "--allow-empty", "-m", "new revision")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertEqual(self.git(self.remote, "rev-parse", "HEAD"), self.git(self.target, "rev-parse", "HEAD"))

    def test_wrong_branch_clone_is_not_switched_implicitly(self):
        self.target.parent.mkdir(parents=True)
        self.git(self.root, "clone", str(self.remote), str(self.target))
        self.git(self.target, "checkout", "-b", "personal-work")
        self.commit("new")
        result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        self.assertEqual("personal-work", self.git(self.target, "branch", "--show-current").strip())

    def test_doctor_accepts_latest_installation_and_records_git_provenance(self):
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        result, output = self.run_cli(command="doctor")
        self.assertEqual(0, result, output)
        lock = json.loads((self.state / "lock.json").read_text())
        self.assertEqual("git", lock["targets"][0]["update_policy"])
        records = json.loads((self.state / "managed-installations.json").read_text())
        entry = records["installations"]["andino-workflow:codex:project"]
        self.assertEqual(self.old, entry["source"]["commit"])

    def test_missing_branch_does_not_fall_back_to_embedded_manifest(self):
        self.catalog.require_capability("andino-workflow").source["branch"] = "missing-branch"
        result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        self.assertFalse(self.target.exists())

    def test_wrong_skill_identity_in_branch_is_rejected(self):
        (self.remote / "SKILL.md").write_text("---\nname: other-skill\ndescription: Wrong identity\n---\n")
        self.git(self.remote, "add", ".")
        self.git(self.remote, "commit", "-m", "wrong skill")
        result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        self.assertFalse(self.target.exists())

    def test_non_fast_forward_git_history_is_preserved(self):
        self.target.parent.mkdir(parents=True)
        self.git(self.root, "clone", str(self.remote), str(self.target))
        self.git(self.target, "config", "user.name", "Fixture")
        self.git(self.target, "config", "user.email", "fixture@example.invalid")
        (self.target / "README.md").write_text("personal commit\n")
        self.git(self.target, "add", ".")
        self.git(self.target, "commit", "-m", "personal history")
        saved = self.git(self.target, "rev-parse", "HEAD")
        self.commit("new")
        result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        self.assertEqual(saved, self.git(self.target, "rev-parse", "HEAD"))

    def test_branch_locked_snapshot_never_silently_restores_a_different_revision(self):
        snapshot = self.root / "snapshot.json"
        snapshot.write_text(json.dumps({"schema_version": 1, "mode": "locked", "profile": {},
                                       "lock": {"targets": [{"update_policy": "git"}]}}))
        with contextlib.redirect_stderr(io.StringIO()):
            result = cli.main(["restore", str(snapshot), "--yes", "--state-dir", str(self.state)])
        self.assertNotEqual(0, result)
        self.assertFalse(self.target.exists())

    def test_interactive_setup_checks_current_content_without_reasking_permission(self):
        selection = InteractiveSelection(("codex",), "minimal", ())
        arguments = ["setup", "--scope", "project", "--project-root", str(self.project),
                     "--state-dir", str(self.state)]
        with patch.object(cli, "prompt_selection", return_value=selection), \
             patch.object(cli, "prompt_confirmation", return_value=True) as confirm:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(0, cli.main(arguments))
            self.assertEqual(1, confirm.call_count)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(0, cli.main(arguments))
            self.assertEqual(1, confirm.call_count)
            self.assertIn("Up to date", output.getvalue())
            self.assertNotIn("Already installed", output.getvalue())

    def test_novice_setup_from_empty_home_installs_and_registers_all_hosts(self):
        for identifier in ("ai-codebase-rescue", "skripsi-skill"):
            self.git(self.remote, "checkout", "-b", identifier)
            (self.remote / "SKILL.md").write_text(
                f"---\nname: {identifier}\ndescription: Fixture {identifier}\n---\nInstructions\n")
            self.git(self.remote, "add", ".")
            self.git(self.remote, "commit", "-m", identifier)
            self.catalog.require_capability(identifier).source["repository"] = str(self.remote)
        home = self.root / "empty-home"
        home.mkdir()
        hosts = tuple(self.catalog.hosts)
        selection = InteractiveSelection(hosts, "everything", ())
        output = io.StringIO()
        original = Path.cwd()
        try:
            os.chdir(home)
            with patch.object(Path, "home", return_value=home), \
                 patch.object(cli, "prompt_selection", return_value=selection), \
                 patch.object(cli, "prompt_confirmation", return_value=True), \
                 contextlib.redirect_stdout(output):
                self.assertEqual(0, cli.main(["setup"]), output.getvalue())
                adapters = cli.build_host_adapters(self.catalog.hosts)
                from ai_rules.hosts.invocation import invocation_paths, invocation_ready
                from ai_rules.domain.statuses import Scope
                for adapter in adapters.values():
                    for identifier in ("andino-workflow", "ai-codebase-rescue", "skripsi-skill"):
                        skill = adapter.skill_target(Scope.GLOBAL) / identifier / "SKILL.md"
                        self.assertTrue(skill.is_file(), str(skill))
                        self.assertTrue(all(invocation_ready(p) for p in invocation_paths(adapter, Scope.GLOBAL, identifier)))
                lock = json.loads((home / ".ai-rules/lock.json").read_text())
                self.assertEqual("verified", lock["status"])
                self.assertEqual(15, len(lock["targets"]))
                self.assertTrue(all(t["action"] == "INSTALL" for t in lock["targets"]))
                self.assertIn("Codex: $andino-workflow", output.getvalue())
                self.assertIn("Claude Code: /andino-workflow", output.getvalue())
                self.assertIn("OpenCode: /andino-workflow", output.getvalue())
        finally:
            os.chdir(original)


if __name__ == "__main__":
    unittest.main()
