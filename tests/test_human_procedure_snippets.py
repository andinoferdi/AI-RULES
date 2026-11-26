"""Run the `.env` writer snippets published in human-procedure's stage contract.

The skill tells agents to copy these snippets into the scripts they hand to a person, so the
snippets must do what the text claims: replace a key in place, keep every other line, append a
missing key, stay idempotent, refuse a symlinked file, a line break or a single quote, and keep
the file mode. Bash cases always run; PowerShell cases run when `pwsh` or `powershell` exists.
"""
import os
import re
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "skills/andino-workflow/skills/human-procedure/resources/stage-contract.md"
FIXTURE = "# local only\nDATABASE_URL=postgres://u:p@h/db\nPAYLANE_KEY=old\nFLAGS=\"a,#b\"\n"


def snippet(language: str) -> str:
    text = CONTRACT.read_text(encoding="utf-8")
    found = re.findall(rf"```{language} hp-env-set\n(.*?)\n```", text, re.S)
    if len(found) != 1:
        raise AssertionError(f"expected one `{language} hp-env-set` block in {CONTRACT.name}")
    return found[0]


class _Cases:
    """Shared cases; subclasses provide set_value(path, key, value) -> exit code."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="hp-env-"))
        self.env = self.dir / ".env"
        self.env.write_bytes(FIXTURE.encode())

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def text(self, path=None) -> str:
        return (path or self.env).read_bytes().decode()

    def test_replaces_in_place_and_keeps_other_lines(self):
        self.assertEqual(0, self.set_value(self.env, "PAYLANE_KEY", "pk_test_new"))
        self.assertEqual(FIXTURE.replace("PAYLANE_KEY=old", "PAYLANE_KEY=pk_test_new"), self.text())

    def test_idempotent(self):
        self.set_value(self.env, "PAYLANE_KEY", "pk_test_new")
        first = self.text()
        self.assertEqual(0, self.set_value(self.env, "PAYLANE_KEY", "pk_test_new"))
        self.assertEqual(first, self.text())

    def test_appends_missing_key_and_quotes_unsafe_value(self):
        self.assertEqual(0, self.set_value(self.env, "NEW_KEY", "a b#c"))
        self.assertEqual(FIXTURE + "NEW_KEY='a b#c'\n", self.text())

    def test_removes_later_duplicates_of_the_key(self):
        self.env.write_bytes((FIXTURE + "PAYLANE_KEY=older\n").encode())
        self.assertEqual(0, self.set_value(self.env, "PAYLANE_KEY", "new"))
        self.assertEqual(FIXTURE.replace("PAYLANE_KEY=old", "PAYLANE_KEY=new"), self.text())

    def test_creates_missing_file(self):
        fresh = self.dir / "fresh.env"
        self.assertEqual(0, self.set_value(fresh, "MODE", "test"))
        self.assertEqual("MODE=test\n", self.text(fresh))

    def test_refuses_single_quote(self):
        self.assertNotEqual(0, self.set_value(self.env, "PAYLANE_KEY", "x'y"))
        self.assertEqual(FIXTURE, self.text())

    def test_refuses_line_break(self):
        self.assertNotEqual(0, self.set_value(self.env, "PAYLANE_KEY", "a\nb"))
        self.assertEqual(FIXTURE, self.text())

    def test_refuses_symlink(self):
        target = self.dir / "real.env"
        target.write_bytes(FIXTURE.encode())
        link = self.dir / "link.env"
        try:
            os.symlink(target, link)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"cannot create a symlink here: {error}")
        self.assertNotEqual(0, self.set_value(link, "PAYLANE_KEY", "new"))
        self.assertEqual(FIXTURE, self.text(target))
        self.assertTrue(link.is_symlink())


class BashSnippetTest(_Cases, unittest.TestCase):
    def setUp(self):
        if not shutil.which("bash"):
            self.skipTest("bash is not on PATH")
        super().setUp()
        self.code = snippet("bash")

    def set_value(self, path, key, value):
        env = dict(os.environ, ENV_FILE=path.as_posix(), HP_KEY=key, HP_VALUE=value)
        run = subprocess.run(["bash", "-c", self.code + '\nenv_set "$HP_KEY" "$HP_VALUE"'],
                             env=env, capture_output=True, text=True)
        return run.returncode

    @unittest.skipIf(os.name == "nt", "POSIX file modes")
    def test_new_file_is_private_and_existing_mode_is_kept(self):
        fresh = self.dir / "fresh.env"
        self.set_value(fresh, "MODE", "test")
        self.assertEqual(0o600, stat.S_IMODE(fresh.stat().st_mode))
        os.chmod(self.env, 0o640)
        self.set_value(self.env, "PAYLANE_KEY", "new")
        self.assertEqual(0o640, stat.S_IMODE(self.env.stat().st_mode))


class PowerShellSnippetTest(_Cases, unittest.TestCase):
    def setUp(self):
        self.shell = shutil.which("pwsh") or shutil.which("powershell")
        if not self.shell:
            self.skipTest("neither pwsh nor powershell is on PATH")
        super().setUp()
        self.script = self.dir / "snippet.ps1"
        self.script.write_text(snippet("powershell"), encoding="utf-8")

    def set_value(self, path, key, value):
        command = (f". '{self.script}'; "
                   "try { Set-EnvValue -Path $env:HP_PATH -Key $env:HP_KEY -Value $env:HP_VALUE; exit 0 }"
                   " catch { [Console]::Error.WriteLine($_); exit 1 }")
        env = dict(os.environ, HP_PATH=str(path), HP_KEY=key, HP_VALUE=value)
        run = subprocess.run([self.shell, "-NoProfile", "-NonInteractive", "-Command", command],
                             env=env, capture_output=True, text=True)
        return run.returncode

    def test_keeps_windows_line_endings(self):
        self.env.write_bytes(FIXTURE.replace("\n", "\r\n").encode())
        self.assertEqual(0, self.set_value(self.env, "PAYLANE_KEY", "new"))
        expected = FIXTURE.replace("PAYLANE_KEY=old", "PAYLANE_KEY=new").replace("\n", "\r\n")
        self.assertEqual(expected, self.text())


if __name__ == "__main__":
    unittest.main()
