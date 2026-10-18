import ast
import importlib.util
import pathlib
import sys
import unittest

target = pathlib.Path(sys.argv.pop(1)).resolve()
spec = importlib.util.spec_from_file_location('review_subject', target)
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)


class SpecContract(unittest.TestCase):
    def test_admin_same_org(self):
        self.assertIs(subject.can_open({'role': 'admin', 'org': 'A'}, {'org': 'A'}), True)

    def test_admin_other_org(self):
        self.assertIs(subject.can_open({'role': 'admin', 'org': 'A'}, {'org': 'B'}), True)

    def test_member_same_org(self):
        self.assertIs(subject.can_open({'role': 'member', 'org': 'A'}, {'org': 'A'}), True)

    def test_member_other_org(self):
        self.assertIs(subject.can_open({'role': 'member', 'org': 'A'}, {'org': 'B'}), False)


class StandardsContract(unittest.TestCase):
    def test_no_dynamic_evaluation(self):
        tree = ast.parse(target.read_text(encoding='utf-8'))
        calls = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Name) and node.func.id == 'eval']
        self.assertEqual(calls, [], 'Explicit standard forbids dynamic evaluation of user input')


if __name__ == '__main__':
    unittest.main(verbosity=2)
