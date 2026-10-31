"""Package/generator boundaries only; fresh consumer evidence is separate."""
import io
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BASE = '69e797e112ce6c2a48d3e767d0c2c7eb4c7f5ff3'
OLD_OWNERSHIP = (
    'Andino Workflow governs overall lifecycle,',
    'Read the accepted task/contract, current repository and relevant evidence first. Andino owns',
    'Andino retains discovery, reasoning depth,',
    'Andino owns routing, depth,',
    'Andino owns selection, depth, scope,',
    'Andino owns scope, depth, routing,',
    'Andino remains the automatic capability router and sole lifecycle owner.',
)


def snapshot(ref):
    data = subprocess.check_output(['git', 'archive', '--format=zip', ref], cwd=ROOT)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        return {item.filename: archive.read(item).decode('utf-8')
                for item in archive.infolist() if not item.is_dir()}


def without_ownership(text):
    # Concurrency wording is the one reviewed procedural clarification: the cap
    # limits simultaneous workers, not total required participants across waves.
    text = text.replace('three direct children', 'three concurrently active direct children')
    text = text.replace('three direct workers', 'three concurrently active direct workers')
    paragraphs = text.replace('\r\n', '\n').split('\n\n')
    selected = [p for p in paragraphs if p.startswith((*OLD_OWNERSHIP, 'Andino coordinates selection,'))]
    if len(selected) != 1:
        raise AssertionError(f'expected one ownership paragraph, found {len(selected)}')
    return '\n\n'.join(p for p in paragraphs if p not in selected)


class ThinCoordinatorContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = snapshot(BASE)
        directory = os.environ.get('ANDINO_RUNTIME_DIR')
        if directory:
            runtime = Path(directory)
            cls.files = {name: (runtime / name).read_text(encoding='utf-8')
                         for name in cls.baseline
                         if (runtime / name).is_file()}
        else:
            cls.files = snapshot(os.environ.get('ANDINO_RUNTIME_REF', 'origin/andino-workflow'))

    def test_all_member_techniques_survive_ownership_migration(self):
        guides = [path for path in self.files if re.fullmatch(r'skills/[^/]+/GUIDE.md', path)]
        self.assertEqual(59, len(guides))
        for guide in guides:
            for path in (guide, guide.replace('/GUIDE.md', '/SKILL.md')):
                with self.subTest(path=path):
                    self.assertEqual(without_ownership(self.baseline[path]),
                                     without_ownership(self.files[path]))
                    self.assertIn('This skill owns its full procedure', self.files[path])

    def test_guard_inventory_and_artifact_exception_are_explicit(self):
        guards = self.files['references/anti-loop.md']
        self.assertEqual(list(range(1, 11)),
                         [int(n) for n in re.findall(r'^\| (\d+)\.', guards, re.M)])
        self.assertIn('at most twice with backoff', guards)
        self.assertIn('permission or daily-quota failures unchanged', guards)
        self.assertIn('never claim already-injected definitions were unloaded', guards)
        self.assertIn('Required code, specs and plans remain complete', guards)
        self.assertIn('no nested spawning', guards)
        self.assertIn('turn incomplete work into a DONE claim', guards)

    def test_registry_and_host_do_not_deny_member_native_identity(self):
        index = self.files['references/internal-method-index.md']
        self.assertEqual(59, len(re.findall(r'\(\.\./skills/[^/]+/SKILL.md\)',
                                          index.split('## Source-name compatibility')[0])))
        self.assertNotIn('not native skills', index)
        host = self.files['references/invocation-adapter.md']
        self.assertIn('native `andino-<id>` SKILL.md', host)
        self.assertIn('explicit native provider', host)

    def test_generator_keeps_native_index_and_method_ownership(self):
        # Run the real maintainer script with disposable runtime AND audit metadata;
        # it writes both. The user's source/audit files are never generator targets.
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'scripts').mkdir()
            script = root / 'scripts/integrate_andino_methods.py'
            shutil.copy2(ROOT / 'scripts/integrate_andino_methods.py', script)
            shutil.copytree(ROOT / 'docs/validation/andino-unified',
                            root / 'docs/validation/andino-unified')
            runtime = root / 'runtime'
            for name, content in self.files.items():
                destination = runtime / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(content, encoding='utf-8')
            result = subprocess.run([sys.executable, str(script), '--runtime', str(runtime)],
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(0, result.returncode, result.stderr)
            index = (runtime / 'references/internal-method-index.md').read_text(encoding='utf-8')
            canonical = index.split('## Source-name compatibility')[0]
            self.assertEqual(59, len(re.findall(r'\(\.\./skills/[^/]+/SKILL.md\)', canonical)))
            self.assertIn('Selected skills own their full procedures', canonical)
            self.assertNotIn('not native skills', canonical)
            row_pattern = r'^\| \[([^]]+)\]\(\.\./skills/[^/]+/SKILL\.md\) \| ([^\n]+?) \| ([^\n]+?) \|$'
            expected_rows = {mid: (trigger, exclusion) for mid, trigger, exclusion in re.findall(
                row_pattern, self.files['references/internal-method-index.md'].split('## Source-name compatibility')[0], re.M)}
            generated_rows = {mid: (trigger, exclusion) for mid, trigger, exclusion in re.findall(
                row_pattern, canonical, re.M)}
            self.assertEqual(expected_rows, generated_rows)
            def alias_map(text):
                rows = re.findall(r'^\| ([^|]+?) \| ([^\n]+?) \|$',
                                  text.split('## Source-name compatibility', 1)[1], re.M)
                return {alias: set(re.findall(r'\(\.\./skills/([^/]+)/(?:SKILL|GUIDE)\.md\)', destinations))
                        for alias, destinations in rows
                        if re.search(r'\(\.\./skills/', destinations)}
            expected_aliases = alias_map(self.files['references/internal-method-index.md'])
            generated_aliases = alias_map(index)
            for alias, destinations in expected_aliases.items():
                self.assertEqual(destinations, generated_aliases.get(alias), alias)
            registry = (runtime / 'references/capability-registry.md').read_text(encoding='utf-8')
            self.assertIn('Honor explicit native provider choices', registry)


if __name__ == '__main__':
    unittest.main()
