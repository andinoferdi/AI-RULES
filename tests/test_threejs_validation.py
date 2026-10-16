import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_skills import package_files, directory_files


class ThreejsValidationTests(unittest.TestCase):
    def package(self, extra=None):
        return {'README.md': '# Shaders\n',
                'SKILL.md': '---\nname: threejs-shaders\ndescription: Custom shaders\n---\n',
                **(extra or {})}

    def test_binary_assets_are_read_as_bytes_and_checked_by_signature(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, content in self.package().items():
                (root / name).write_text(content, encoding='utf-8')
            (root / 'assets').mkdir()
            (root / 'assets/module.wasm').write_bytes(b'\x00asm\x01\x00\x00\x00')
            files, modes = directory_files(root)
            self.assertEqual([], package_files(files, 'threejs-shaders', modes))
            (root / 'assets/module.wasm').write_bytes(b'not wasm')
            files, modes = directory_files(root)
            self.assertTrue(package_files(files, 'threejs-shaders', modes))

    def test_code_shaders_and_agents_are_allowed_only_for_registered_threejs_packages(self):
        files = self.package({'scripts/check.py': 'print(1)',
                              'examples/effect.wgsl': '@fragment fn main() {}',
                              'agents/openai.yaml': 'interface:\n  display_name: Shaders\n'})
        self.assertEqual([], package_files(files, 'threejs-shaders'))
        self.assertTrue(package_files(files, 'andino-workflow'))

    def test_unknown_extension_hidden_paths_traversal_and_binary_text_rejected(self):
        for name, content in [('assets/file.exe', b'MZ'), ('assets/.env', b'KEY=value'),
                              ('assets/../file.png', b'\x89PNG\r\n\x1a\n'),
                              ('references/broken.md', b'\xff')]:
            with self.subTest(name=name):
                self.assertTrue(package_files(self.package({name: content}), 'threejs-shaders'))

    def test_image_relative_links_are_checked(self):
        files = self.package({'references/example.md': '![missing](../assets/missing.png)\n'})
        self.assertTrue(package_files(files, 'threejs-shaders'))
