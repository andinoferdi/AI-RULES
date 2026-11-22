import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from ai_rules import cli
from ai_rules.catalog import load_catalog
from ai_rules.interactive import InteractiveSelection
from ai_rules.profiles import load_profiles


class LiveUpdateTests(unittest.TestCase):
    def test_antigravity_setup_without_windows_stat_constants(self):
        from ai_rules.hosts import invocation

        with patch.object(invocation, "stat", SimpleNamespace()):
            for _ in range(2):
                result, output = self.run_cli("--host", "antigravity-cli")
                self.assertEqual(0, result, output)
        self.assertTrue((self.target.parent / "focus/SKILL.md").is_file())

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.remote = self.root / "upstream"
        self.remote.mkdir()
        self.git(self.remote, "init", "-b", "main")
        self.git(self.remote, "config", "user.name", "Fixture")
        self.git(self.remote, "config", "user.email", "fixture@example.invalid")
        # One branch, every skill in skills/<id>/, like the real repository.
        self.pkg = self.remote / "skills/andino-workflow"
        for identifier, body in (("focus", "Answer first."), ("search-first", "Research first.")):
            package = self.remote / "skills" / identifier
            package.mkdir(parents=True)
            (package / "SKILL.md").write_text(
                f"---\nname: {identifier}\ndescription: Fixture {identifier}\n---\n{body}\n", encoding="utf-8")
        self.commit("old", extra=True)
        self.old = self.git(self.remote, "rev-parse", "HEAD").strip()
        self.project = self.root / "project"
        self.target = self.project / ".agents/skills/andino-workflow"
        self.state = self.root / "state"
        self.catalog = load_catalog()
        for identifier in ("andino-workflow", "focus", "search-first"):
            self.catalog.require_capability(identifier).source["repository"] = str(self.remote)
        self.catalog_patch = patch.object(cli, "load_catalog", return_value=self.catalog)
        self.catalog_patch.start()
        self.addCleanup(self.catalog_patch.stop)

    def git(self, cwd, *args):
        return subprocess.check_output(["git", *args], cwd=cwd, text=True, encoding="utf-8", stderr=subprocess.PIPE)

    def commit(self, content, extra=False):
        self.pkg.mkdir(parents=True, exist_ok=True)
        (self.pkg / "SKILL.md").write_text(
            "---\nname: andino-workflow\ndescription: Fixture workflow\n---\n" + content + "\n", encoding="utf-8")
        (self.pkg / "README.md").write_text("Fixture\n", encoding="utf-8")
        if extra:
            (self.pkg / "obsolete.md").write_text("old\n", encoding="utf-8")
        self.git(self.remote, "add", ".")
        self.git(self.remote, "commit", "-m", content)

    def add_member(self, body):
        member = self.pkg / "skills/plan-execution"
        member.mkdir(parents=True, exist_ok=True)
        (member / "SKILL.md").write_text(f"---\nname: andino-plan-execution\n---\n{body}\n")
        return member

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
            shutil.copyfile(self.pkg / name, self.target / name)

    def test_existing_copy_updates_and_later_commit_needs_no_cli_release(self):
        self.copy_old()
        (self.pkg / "obsolete.md").unlink()
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
        workflow = next(t for t in lock['targets'] if t['capability'] == 'andino-workflow')
        self.assertIn(self.git(self.remote, "rev-parse", "HEAD").strip(), workflow['target_version'])

    def test_latest_installs_main_head_and_later_commit(self):
        self.commit("first")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.commit("second")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertIn("second", (self.target / "SKILL.md").read_text())
        lock = json.loads((self.state / "lock.json").read_text())
        workflow = next(t for t in lock["targets"] if t["capability"] == "andino-workflow")
        self.assertIn(self.git(self.remote, "rev-parse", "HEAD").strip(), workflow["target_version"])

    def test_recorded_install_updates_without_source_history(self):
        # A copy the old branch-based installer wrote: never committed on main, but recorded.
        from ai_rules.release.latest import contents
        self.target.mkdir(parents=True)
        (self.target / "SKILL.md").write_text(
            "---\nname: andino-workflow\ndescription: Fixture workflow\n---\nlegacy branch copy\n", encoding="utf-8")
        (self.target / "README.md").write_text("Fixture\n", encoding="utf-8")
        self.state.mkdir(parents=True)
        (self.state / "managed-installations.json").write_text(json.dumps({"schema_version": 1, "installations": {
            "andino-workflow:codex:project": {
                "version": "git-branch:andino-workflow@" + "0" * 40,
                "files": [{"path": path, "blob": blob} for path, blob in contents(self.target).items()]}}}),
            encoding="utf-8")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertNotIn("legacy branch copy", (self.target / "SKILL.md").read_text())
        self.assertIn("old", (self.target / "SKILL.md").read_text())

    def test_unrecorded_unknown_copy_is_preserved(self):
        self.target.mkdir(parents=True)
        (self.target / "SKILL.md").write_text("---\nname: andino-workflow\ndescription: x\n---\nmine\n", encoding="utf-8")
        result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        self.assertIn("modified or unrecognized", output)
        self.assertIn("mine", (self.target / "SKILL.md").read_text())

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
        self.assertEqual("SKIPPED", next(t["status"] for t in lock["targets"] if t["host"] == "opencode" and t['capability'] == 'andino-workflow'))

    def test_ide_workflow_loads_skill_without_copying_body(self):
        result, output = self.run_cli("--host", "antigravity-ide")
        self.assertEqual(0, result, output)
        command = self.project / ".agents/workflows/andino-workflow.md"
        self.assertIn(self.target.joinpath("SKILL.md").as_posix(), command.read_text())
        self.assertNotIn("$ARGUMENTS", command.read_text())

    def test_git_checkout_install_is_preserved_for_subpath_sources(self):
        self.target.parent.mkdir(parents=True)
        self.git(self.root, "clone", str(self.remote), str(self.target))
        self.commit("new")
        result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        self.assertIn("Git checkout for a subpath package is preserved", output)
        self.assertEqual(self.old, self.git(self.target, "rev-parse", "HEAD").strip())

    def test_crlf_python_resource_matches_source_but_changed_code_does_not(self):
        from ai_rules.release.latest import contents

        first, second = self.root / "lf-resource", self.root / "crlf-resource"
        first.mkdir()
        second.mkdir()
        (first / "check.py").write_bytes(b"print('verified')\n")
        (second / "check.py").write_bytes(b"print('verified')\r\n")
        self.assertEqual(contents(first), contents(second))
        (second / "check.py").write_bytes(b"print('different')\r\n")
        self.assertNotEqual(contents(first), contents(second))

    def test_crlf_extensionless_script_matches_source_but_changed_code_does_not(self):
        from ai_rules.release.latest import contents

        first, second = self.root / "lf-script", self.root / "crlf-script"
        first.mkdir()
        second.mkdir()
        (first / "run-check").write_bytes(b"#!/usr/bin/env bash\necho ok\n")
        (second / "run-check").write_bytes(b"#!/usr/bin/env bash\r\necho ok\r\n")
        self.assertEqual(contents(first), contents(second))
        (second / "run-check").write_bytes(b"#!/usr/bin/env bash\r\necho different\r\n")
        self.assertNotEqual(contents(first), contents(second))

    def test_native_member_from_older_commit_inside_subpath_is_updated(self):
        member = self.add_member("old member")
        self.commit("with member")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        native = self.target.parent / "andino-plan-execution"
        self.assertIn("old member", (native / "SKILL.md").read_text())
        self.add_member("new member")
        self.commit("new member")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertEqual((member / "SKILL.md").read_text(), (native / "SKILL.md").read_text())
        self.assertTrue(list((self.state / "backups").glob("*/andino-plan-execution/SKILL.md")))
        shutil.rmtree(native)
        result, output = self.run_cli("--dry-run")
        self.assertEqual(0, result, output)
        self.assertFalse(native.exists())
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertEqual((member / "SKILL.md").read_text(), (native / "SKILL.md").read_text())
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertIn("NO_OP", output)

    def test_recorded_native_member_updates_without_source_history(self):
        import hashlib
        from ai_rules.release.family import fingerprint
        self.add_member("current member")
        self.commit("with member")
        native = self.target.parent / "andino-plan-execution"
        native.mkdir(parents=True)
        (native / "SKILL.md").write_text("---\nname: andino-plan-execution\n---\nlegacy member\n")
        root = self.target.parent
        key = hashlib.sha256(str(root.resolve()).casefold().encode()).hexdigest()
        inventory = self.state / "family-inventories" / f"{key}.json"
        inventory.parent.mkdir(parents=True)
        inventory.write_text(json.dumps({"schema_version": 1, "family": "andino-workflow", "root": str(root),
                                         "artifacts": {str(native): {"id": native.name, "kind": "tree",
                                                                     "fingerprint": fingerprint(native)}}}))
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        self.assertIn("current member", (native / "SKILL.md").read_text())

    def test_user_edits_are_preserved_and_never_reported_current(self):
        self.copy_old()
        (self.target / "SKILL.md").write_text("personal edits\n", encoding="utf-8")
        self.commit("new")
        result, output = self.run_cli()
        self.assertNotEqual(0, result)
        self.assertIn("BLOCK", output)
        self.assertEqual("personal edits\n", (self.target / "SKILL.md").read_text())

    def test_modified_native_member_blocks_parent_update_without_overwriting(self):
        self.add_member("old")
        self.commit("with member")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        native = self.target.parent / "andino-plan-execution"
        (native / "SKILL.md").write_text("personal member edits\n")
        self.add_member("new")
        self.commit("member update")
        result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        self.assertIn("modified or unrecognized", output)
        self.assertEqual("personal member edits\n", (native / "SKILL.md").read_text())
        self.assertIn("with member", (self.target / "SKILL.md").read_text())

    def test_native_member_drift_after_planning_fails_activation_verification(self):
        self.add_member("current")
        self.commit("with member")
        result, output = self.run_cli()
        self.assertEqual(0, result, output)
        native = self.target.parent / "andino-plan-execution/SKILL.md"
        executor = cli._executor_for_plan

        def edit_after_plan(*args, **kwargs):
            native.write_text("user edit after planning\n")
            return executor(*args, **kwargs)

        with patch.object(cli, "_executor_for_plan", side_effect=edit_after_plan):
            result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        self.assertEqual("user edit after planning\n", native.read_text())
        lock = json.loads((self.state / "lock.json").read_text())
        workflow = next(t for t in lock['targets'] if t['capability'] == 'andino-workflow')
        self.assertNotEqual("PASS", workflow['verification']['outcome'])
        self.assertNotEqual("VERIFIED", workflow['status'])

    def test_failed_source_lookup_is_not_a_successful_noop(self):
        self.copy_old()
        self.catalog.require_capability("andino-workflow").source["repository"] = str(self.root / "missing")
        result, output = self.run_cli()
        self.assertNotEqual(0, result)
        self.assertNotIn("All selected skills are ready", output)
        self.assertFalse((self.state / "lock.json").exists())

    def test_auto_is_default_and_fetches_github_shaped_source_outside_a_clone(self):
        self.assertEqual("auto", cli.build_parser().parse_args(["setup"]).source)
        output = io.StringIO()
        with contextlib.chdir(self.root), contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = cli.main(["setup", "--host", "codex", "--profile", "minimal",
                               "--scope", "project", "--project-root", str(self.project),
                               "--state-dir", str(self.state), "--non-interactive", "--yes"])
        self.assertEqual(0, result, output.getvalue())
        self.assertIn("Skill source: GitHub main", output.getvalue())
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

    def test_shared_project_root_is_updated_once_and_verified_for_each_host(self):
        self.copy_old()
        self.commit("new")
        result, output = self.run_cli("--host", "opencode", "--host", "antigravity-cli")
        self.assertEqual(0, result, output)
        self.assertEqual(1, len(list((self.state / "backups").glob("*/andino-workflow"))))
        lock = json.loads((self.state / "lock.json").read_text())
        self.assertEqual(9, len(lock["targets"]))
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

    def test_all_selected_skills_come_from_one_fetch_of_main(self):
        rescue = self.remote / "skills/ai-codebase-rescue"
        rescue.mkdir(parents=True)
        (rescue / "SKILL.md").write_text("---\nname: ai-codebase-rescue\ndescription: Rescue\n---\nrescue\n")
        self.git(self.remote, "add", ".")
        self.git(self.remote, "commit", "-m", "rescue")
        self.catalog.require_capability("ai-codebase-rescue").source["repository"] = str(self.remote)
        from ai_rules.release import latest
        with patch.object(latest, "git", wraps=latest.git) as commands:
            result, output = self.run_cli("--profile", "engineering")
        self.assertEqual(0, result, output)
        self.assertEqual(1, sum(1 for call in commands.call_args_list if call.args[1] == "fetch"))
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
        self.assertEqual(linked.resolve(), self.target.resolve())
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
                self.assertEqual(linked.resolve(), self.target.resolve())
                self.assertIn("old", (linked / "SKILL.md").read_text())
        lock = json.loads((self.state / "lock.json").read_text())
        self.assertNotEqual("verified", lock["status"])

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
        (self.pkg / "SKILL.md").write_text("---\nname: other-skill\ndescription: Wrong identity\n---\n")
        self.git(self.remote, "add", ".")
        self.git(self.remote, "commit", "-m", "wrong skill")
        result, output = self.run_cli()
        self.assertNotEqual(0, result, output)
        self.assertFalse(self.target.exists())

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
                     "--state-dir", str(self.state), "--source", "latest"]
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
        for capability in self.catalog.capabilities.values():
            if capability.ownership.value != "FIRST_PARTY" or capability.id in ("andino-workflow", "focus", "search-first"):
                continue
            capability.source["repository"] = str(self.remote)
            package = self.remote / capability.source["subpath"]
            package.mkdir(parents=True, exist_ok=True)
            (package / "SKILL.md").write_text(
                f"---\nname: {capability.id}\ndescription: Fixture {capability.id}\n---\nInstructions\n")
        self.git(self.remote, "add", ".")
        self.git(self.remote, "commit", "-m", "every skill")
        home = self.root / "empty-home"
        home.mkdir()
        hosts = tuple(self.catalog.hosts)
        expected_skills = load_profiles(self.catalog).require("everything").capabilities
        selection = InteractiveSelection(hosts, "everything", ())
        output = io.StringIO()
        original = Path.cwd()
        try:
            os.chdir(home)
            with patch.object(Path, "home", return_value=home), \
                 patch.object(cli, "prompt_selection", return_value=selection), \
                 patch.object(cli, "prompt_agent_defaults", return_value=(False, None)), \
                 patch.object(cli, "prompt_confirmation", return_value=True), \
                 contextlib.redirect_stdout(output):
                self.assertEqual(0, cli.main(["setup"]), output.getvalue())
                adapters = cli.build_host_adapters(self.catalog.hosts)
                from ai_rules.hosts.invocation import invocation_paths, invocation_ready
                from ai_rules.domain.statuses import Scope
                for adapter in adapters.values():
                    for identifier in expected_skills:
                        skill = adapter.skill_target(Scope.GLOBAL) / identifier / "SKILL.md"
                        self.assertTrue(skill.is_file(), str(skill))
                        self.assertTrue(all(invocation_ready(p) for p in invocation_paths(adapter, Scope.GLOBAL, identifier)))
                lock = json.loads((home / ".ai-rules/lock.json").read_text())
                self.assertEqual("verified", lock["status"])
                self.assertEqual(len(hosts) * len(expected_skills), len(lock["targets"]))
                self.assertTrue(all(t["action"] == "INSTALL" for t in lock["targets"]))
                self.assertIn('$andino-workflow', output.getvalue())
                self.assertIn('/andino-workflow', output.getvalue())
        finally:
            os.chdir(original)


if __name__ == "__main__":
    unittest.main()
