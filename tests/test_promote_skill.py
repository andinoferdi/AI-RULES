import contextlib
import importlib.util
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("promote_skill", ROOT / "scripts" / "promote_skill.py")
promote_skill = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(promote_skill)
MANIFEST = "src/ai_rules/release/data/release_manifest.json"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                          text=True).stdout.strip()


class FakeGh:
    def __init__(self):
        self.calls = []

    def __call__(self, *args, cwd):
        self.calls.append(args)
        if args[:2] == ("pr", "view"):
            return SimpleNamespace(returncode=1, stdout="", stderr="no pull requests found")
        return SimpleNamespace(returncode=0, stdout="https://github.com/example/repo/pull/7\n", stderr="")


class UpdateManifestTests(unittest.TestCase):
    def test_pins_commit_and_bumps_release_sequence(self):
        manifest = {"release_sequence": 40, "verified_at": "2026-01-01",
                    "first_party": {"focus": {"branch": "focus", "commit": "a" * 40, "release_sequence": 39}}}
        updated = promote_skill.update_manifest(manifest, "focus", "b" * 40, "2026-11-22")
        self.assertEqual("b" * 40, updated["first_party"]["focus"]["commit"])
        self.assertEqual(41, updated["first_party"]["focus"]["release_sequence"])
        self.assertEqual(41, updated["release_sequence"])
        self.assertEqual("2026-11-22", updated["verified_at"])
        self.assertEqual("a" * 40, manifest["first_party"]["focus"]["commit"])

    def test_unknown_skill_is_rejected(self):
        with self.assertRaises(KeyError):
            promote_skill.update_manifest({"first_party": {}}, "new-skill", "b" * 40, "2026-11-22")


class PromoteFlowTests(unittest.TestCase):
    def setUp(self):
        # CI runners have no global Git identity; the promote clone commits with this one.
        identity = patch.dict(os.environ, {
            "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.invalid"})
        identity.start()
        self.addCleanup(identity.stop)
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.remote = base / "remote.git"
        seed = base / "seed"
        git(base, "init", "-q", "--bare", str(self.remote))
        git(base, "init", "-q", "-b", "focus", str(seed))
        git(seed, "config", "user.email", "test@example.invalid")
        git(seed, "config", "user.name", "Test")
        (seed / "SKILL.md").write_text("one\n")
        git(seed, "add", ".")
        git(seed, "commit", "-qm", "one")
        self.old = git(seed, "rev-parse", "HEAD")
        (seed / "SKILL.md").write_text("two\n")
        git(seed, "commit", "-qam", "two")
        self.new = git(seed, "rev-parse", "HEAD")
        git(seed, "checkout", "-q", "--orphan", "main")
        git(seed, "rm", "-rqf", ".")
        (seed / MANIFEST).parent.mkdir(parents=True)
        (seed / MANIFEST).write_text(json.dumps({"release_sequence": 5, "first_party": {
            "focus": {"branch": "focus", "commit": self.old, "release_sequence": 5}}}, indent=2) + "\n")
        git(seed, "add", ".")
        git(seed, "commit", "-qm", "main")
        git(seed, "push", "-q", str(self.remote), "main", "focus")
        self.root = base / "checkout"
        git(base, "clone", "-q", "-b", "main", str(self.remote), str(self.root))
        git(self.root, "config", "user.email", "test@example.invalid")
        git(self.root, "config", "user.name", "Test")
        self.workdir = Path(git(self.root, "rev-parse", "--path-format=absolute", "--git-common-dir")) / "promote/focus"

    def tearDown(self):
        self.tmp.cleanup()

    def promote(self, passed, **kwargs):
        self.seen = []

        def checks(root):
            self.seen.append(git(root, "show", "origin/focus:SKILL.md"))
            return passed, "" if passed else "Test validators and installer regressions"

        self.gh = FakeGh()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as err:
            code = promote_skill.promote("focus", root=self.root, checks=checks, run_gh=self.gh,
                                         today="2026-11-22", **kwargs)
        self.stderr = err.getvalue()
        return code

    def remote_branches(self):
        return git(self.remote, "for-each-ref", "--format=%(refname:short)", "refs/heads")

    def test_failed_checks_push_nothing_and_keep_the_clone(self):
        self.assertEqual(1, self.promote(passed=False))
        self.assertEqual(["two"], self.seen)  # checks ran against the new pin
        self.assertNotIn("promote/focus", self.remote_branches())
        self.assertIn("Nothing was pushed", self.stderr)
        self.assertEqual([], [c for c in self.gh.calls if c[:2] == ("pr", "create")])
        self.assertTrue((self.workdir / MANIFEST).is_file())

    def test_passing_checks_push_pin_and_open_pull_request(self):
        self.assertEqual(0, self.promote(passed=True))
        pinned = json.loads(git(self.remote, "show", f"promote/focus:{MANIFEST}"))
        self.assertEqual(self.new, pinned["first_party"]["focus"]["commit"])
        self.assertEqual(6, pinned["release_sequence"])
        create = next(c for c in self.gh.calls if c[:2] == ("pr", "create"))
        self.assertIn("promote/focus", create)
        self.assertNotIn(("pr", "merge"), [c[:2] for c in self.gh.calls])

    def test_dry_run_runs_checks_without_pushing(self):
        self.assertEqual(0, self.promote(passed=True, dry_run=True))
        self.assertEqual(["two"], self.seen)
        self.assertNotIn("promote/focus", self.remote_branches())

    def test_auto_merge_requests_merge_after_checks(self):
        self.assertEqual(0, self.promote(passed=True, auto_merge=True))
        self.assertIn(("pr", "merge"), [c[:2] for c in self.gh.calls])

    def test_already_pinned_branch_has_nothing_to_promote(self):
        self.assertEqual(0, self.promote(passed=True, ref=self.old))
        self.assertEqual([], self.seen)


if __name__ == "__main__":
    unittest.main()
