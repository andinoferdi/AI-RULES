import tempfile
import unittest
from pathlib import Path

from ai_rules.catalog import load_catalog
from ai_rules.domain.statuses import Scope
from ai_rules.hosts.adapters import build_host_adapters
from ai_rules.hosts.invocation import install_invocation, invocation_paths, invocation_ready


class SkillInvocationTests(unittest.TestCase):
    def test_global_host_registrations_and_native_hosts(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            adapters = build_host_adapters(load_catalog().hosts, home)
            for host in adapters.values():
                skill = host.skill_target(Scope.GLOBAL) / "skripsi-skill/SKILL.md"
                skill.parent.mkdir(parents=True, exist_ok=True)
                skill.write_text("---\nname: skripsi-skill\ndescription: Thesis\n---\nBody\n")
                install_invocation(host, Scope.GLOBAL, "skripsi-skill")
                paths = invocation_paths(host, Scope.GLOBAL, "skripsi-skill")
                self.assertTrue(all(invocation_ready(path) for path in paths))
                if host.id == "antigravity-ide":
                    self.assertEqual(2, len(paths))
                    self.assertIn(home / ".gemini/antigravity/global_workflows/skripsi-skill.md", paths)
                elif host.id != "opencode":
                    self.assertEqual((), paths)


if __name__ == "__main__":
    unittest.main()
