#!/usr/bin/env python3
"""Independent structural oracle; does NOT prove model behavior or CLI setup."""
from __future__ import annotations

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RETIRED = {
    'context-engineering', 'decision-interview', 'decision-map',
    'deep-module-design', 'delivery', 'design-prototype', 'domain-modeling',
    'environment-retrospective', 'exercise-scaffolding', 'frontend-ui-engineering',
    'git-isolation', 'git-operation-guard', 'git-workflow-and-versioning',
    'idea-refine', 'implementation', 'incremental-implementation', 'method-authoring',
    'plain-language-repitch', 'pr-description', 'pre-commit-setup',
    'primary-source-research', 'project-configuration', 'source-driven-development',
    'specification', 'stakeholder-questionnaire', 'task-decomposition',
    'test-fixture-migration', 'typescript-boundary-enforcement',
    'workflow-advisor', 'workflow-specification', 'writing-fragments',
}
MEMBERS = {
    'agent-document-authoring', 'api-and-interface-design', 'architecture-survey',
    'article-shaping', 'brainstorming', 'browser-testing-with-devtools',
    'ci-cd-and-automation', 'code-review', 'code-simplification',
    'constraint-driven-development', 'debugging', 'delegation',
    'deprecation-and-migration', 'documentation-and-adrs', 'doubt-driven-development',
    'git-skills', 'handoff', 'human-procedure', 'issue-triage', 'learning-workspace',
    'observability-and-instrumentation', 'performance-optimization',
    'plan-execution', 'planning', 'security-and-hardening', 'session-diagnostics',
    'shipping-and-launch', 'skill-maker', 'tdd', 'verification',
}
# Resource owners are literal accepted expectations, not inferred from output.
MODES = {
    'handoff': ['context-packing'],
    'brainstorming': ['decision-frontier', 'feasibility-probe', 'idea-validation', 'async-questions'],
    'api-and-interface-design': ['module-depth', 'import-enforcement', 'http-contracts'],
    'plan-execution': ['task-implementation', 'vertical-slices', 'frontend-engineering'],
    'planning': ['behavior-readiness', 'dependency-slicing', 'recurring-process'],
    'documentation-and-adrs': ['domain-vocabulary'],
    'session-diagnostics': ['prevention-review'],
    'tdd': ['typed-fixtures'],
    'learning-workspace': ['course-exercises'],
    'article-shaping': ['raw-capture'],
    'git-skills': ['workspace', 'operation-safety', 'change-hygiene', 'branch-integration', 'pr-draft'],
    'ci-cd-and-automation': ['commit-checks'],
}


def prose(path: Path) -> str:
    return re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)


def markdown_links(root: Path):
    for path in root.rglob('*.md'):
        if '.git' in path.parts or 'docs' in path.relative_to(root).parts:
            continue
        for match in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', prose(path)):
            target = match.group(1).split('#', 1)[0]
            if not target or ':' in target or target.startswith('/'):
                continue
            yield path, target, (path.parent / target).resolve()


class Portfolio(unittest.TestCase):
    def test_public_members_and_hard_retirement(self):
        actual = {p.parent.name for p in (ROOT / 'skills').glob('*/SKILL.md')}
        self.assertEqual(MEMBERS, actual)
        for name in MEMBERS & actual:
            text = (ROOT / 'skills' / name / 'SKILL.md').read_text(encoding='utf-8')
            self.assertRegex(text, r'(?m)^name: andino-' + re.escape(name) + r'\s*$')
        expected_entrypoints = {ROOT / 'SKILL.md'} | {
            ROOT / 'skills' / name / 'SKILL.md' for name in MEMBERS
        }
        self.assertEqual(expected_entrypoints, set(ROOT.rglob('SKILL.md')),
                         'resources may not become discoverable native skills')
        for name in RETIRED:
            with self.subTest(retired=name):
                self.assertFalse((ROOT / 'skills' / name).exists())

    def test_manifest_matches_independent_oracle(self):
        path = ROOT / 'references' / 'portfolio.json'
        self.assertTrue(path.is_file(), 'new distribution manifest is required')
        data = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(1, data['schema_version'])
        self.assertEqual(1, data['installer_protocol'])
        self.assertEqual(MEMBERS, set(data['members']))
        self.assertEqual(len(MEMBERS), len(data['members']), 'duplicate member IDs')
        self.assertEqual(RETIRED, set(data['retired']))
        self.assertEqual(len(RETIRED), len(data['retired']), 'duplicate retired IDs')
        self.assertFalse(set(data['members']) & set(data['retired']))
        self.assertEqual(RETIRED, {row['source'] for row in data['resources']}
                         | {row['source'] for row in data['sibling_resources']}
                         | set(data['removed_forwarders']))
        for row in data['resources']:
            resource = Path(row['resource'])
            self.assertFalse(resource.is_absolute())
            self.assertNotIn('..', resource.parts)
            self.assertTrue((ROOT / resource).is_file(), row)
        for owner, modes in MODES.items():
            for mode in modes:
                if mode != 'http-contracts':
                    self.assertIn(f'skills/{owner}/resources/{mode}/guide.md',
                                  {row['resource'] for row in data['resources']})

    def test_resource_guides_are_real_and_not_native_entrypoints(self):
        for owner, modes in MODES.items():
            for mode in modes:
                with self.subTest(owner=owner, mode=mode):
                    directory = ROOT / 'skills' / owner / 'resources' / mode
                    guide = directory / 'guide.md'
                    self.assertTrue(guide.is_file(), str(guide))
                    self.assertGreater(len(guide.read_text(encoding='utf-8')), 300)
                    self.assertFalse(list(directory.rglob('SKILL.md')))
                    self.assertFalse(guide.read_text(encoding='utf-8').startswith('---\nname:'))
        for mode in ('project-setup', 'workflow-advice'):
            self.assertTrue((ROOT / 'references' / mode / 'guide.md').is_file())

    def test_local_links(self):
        errors = [(str(p.relative_to(ROOT)), target) for p, target, resolved
                  in markdown_links(ROOT) if not resolved.exists()]
        self.assertEqual([], errors)

    def test_current_routes_do_not_register_retired_native_ids(self):
        paths = [ROOT / 'SKILL.md'] + [ROOT / 'references' / name for name in
                 ('routing.md', 'method-dispatch.md', 'internal-method-index.md', 'capability-registry.md')]
        errors = []
        for path in paths:
            text = prose(path)
            for retired in RETIRED:
                if re.search(r'(?<![\w-])andino-' + re.escape(retired) + r'(?![\w-])', text):
                    errors.append((path.name, retired))
                if re.search(r'skills/' + re.escape(retired) + r'/(?:SKILL|GUIDE)\.md', text):
                    errors.append((path.name, retired, 'stale-path'))
        self.assertEqual([], errors)

    def test_flat_members_local_resources_resolve(self):
        # Local member links must survive flat discovery. Cross-owner resources use
        # explicit workflow-root prose paths, not ambiguous sibling Markdown links.
        with tempfile.TemporaryDirectory(prefix='andino-portfolio-structure-') as tmp:
            root = Path(tmp)
            for member in sorted(MEMBERS):
                source = ROOT / 'skills' / member
                self.assertTrue(source.is_dir(), member)
                shutil.copytree(source, root / ('andino-' + member))
            # A nested canonical workflow package is also supplied by setup.
            shutil.copytree(ROOT / 'references', root / 'andino-workflow' / 'references')
            shutil.copytree(ROOT / 'skills', root / 'andino-workflow' / 'skills')
            shutil.copy2(ROOT / 'SKILL.md', root / 'andino-workflow' / 'SKILL.md')
            errors = [(str(p.relative_to(root)), target) for p, target, resolved
                      in markdown_links(root) if not resolved.exists()]
            self.assertEqual([], errors)


if __name__ == '__main__':
    unittest.main(verbosity=2)
