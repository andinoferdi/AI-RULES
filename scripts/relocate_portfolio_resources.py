#!/usr/bin/env python3
"""One-shot approved T1 relocation; provenance precedes mutation; no installer effects.

Run from any directory with Python -I. Existing evidence makes reruns refuse to
snapshot edited resources as originals. Retired shims carry no unique procedure.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
MAPPING = {
    'context-engineering': 'skills/handoff/resources/context-packing',
    'decision-map': 'skills/brainstorming/resources/decision-frontier',
    'design-prototype': 'skills/brainstorming/resources/feasibility-probe',
    'idea-refine': 'skills/brainstorming/resources/idea-validation',
    'stakeholder-questionnaire': 'skills/brainstorming/resources/async-questions',
    'deep-module-design': 'skills/api-and-interface-design/resources/module-depth',
    'typescript-boundary-enforcement': 'skills/api-and-interface-design/resources/import-enforcement',
    'implementation': 'skills/plan-execution/resources/task-implementation',
    'incremental-implementation': 'skills/plan-execution/resources/vertical-slices',
    'frontend-ui-engineering': 'skills/plan-execution/resources/frontend-engineering',
    'specification': 'skills/planning/resources/behavior-readiness',
    'task-decomposition': 'skills/planning/resources/dependency-slicing',
    'workflow-specification': 'skills/planning/resources/recurring-process',
    'domain-modeling': 'skills/documentation-and-adrs/resources/domain-vocabulary',
    'environment-retrospective': 'skills/session-diagnostics/resources/prevention-review',
    'test-fixture-migration': 'skills/tdd/resources/typed-fixtures',
    'exercise-scaffolding': 'skills/learning-workspace/resources/course-exercises',
    'writing-fragments': 'skills/article-shaping/resources/raw-capture',
    'git-isolation': 'skills/git-skills/resources/workspace',
    'git-operation-guard': 'skills/git-skills/resources/operation-safety',
    'git-workflow-and-versioning': 'skills/git-skills/resources/change-hygiene',
    'delivery': 'skills/git-skills/resources/branch-integration',
    'pr-description': 'skills/git-skills/resources/pr-draft',
    'pre-commit-setup': 'skills/ci-cd-and-automation/resources/commit-checks',
    'project-configuration': 'references/project-setup',
    'workflow-advisor': 'references/workflow-advice',
}
SHIMS = {'decision-interview': 'brainstorming', 'method-authoring': 'skill-maker'}
SIBLINGS = {
    'primary-source-research': ('search-first', 'references/sourced-answer'),
    'source-driven-development': ('search-first', 'references/version-contract'),
    'plain-language-repitch': ('focus', 'references/explanation-repair.md'),
}
EVIDENCE = ROOT / 'references/project-setup/relocation-evidence.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def strip_registration(text, slug):
    text = re.sub(r'\A---\r?\n.*?\r?\n---\r?\n', '', text, count=1, flags=re.S)
    text = re.sub(r'^Internal (?:Andino )?method ID:.*\n?',
                  'Internal resource; select this procedure directly under its canonical owner.\n', text, flags=re.M)
    # Exact native IDs are operational routes, not ordinary language. Preserve
    # upstream repository paths and legal origins; those do not contain these IDs.
    replacements = {f'andino-{s}': f'workflow-root `{d}/guide.md` resource' for s, d in MAPPING.items()}
    replacements.update({f'andino-{s}': f'andino-{d}' for s, d in SHIMS.items()})
    replacements.update({f'andino-{s}': f'{owner} `{dest if dest.endswith(".md") else dest + "/guide.md"}` resource'
                         for s, (owner, dest) in SIBLINGS.items()})
    for old, new in sorted(replacements.items(), key=lambda item: -len(item[0])):
        text = re.sub(r'(?<![\w-])' + re.escape(old) + r'(?![\w-])', lambda _: new, text)
    return text


def main():
    if EVIDENCE.exists():
        raise SystemExit('Existing provenance found; refusing to overwrite original snapshot')
    files = []
    physical = {}
    snapshots = {}
    # Read every byte before any move. This is also the relocation parity control.
    for slug, dest in MAPPING.items():
        source = ROOT / 'skills' / slug
        for path in sorted(source.rglob('*')):
            if not path.is_file():
                continue
            rel = path.relative_to(source)
            newrel = Path('guide.md' if rel.as_posix() == 'GUIDE.md' else
                          'contract.md' if rel.as_posix() == 'SKILL.md' else rel.as_posix())
            target = ROOT / dest / newrel
            assert not target.exists(), target
            data = path.read_bytes()
            snapshots[path] = data
            physical[path.resolve()] = target.resolve()
            files.append({'source': path.relative_to(ROOT).as_posix(),
                          'destination': target.relative_to(ROOT).as_posix(),
                          'source_sha256': digest(data), 'copied_sha256': digest(data)})
    for slug, owner in SHIMS.items():
        for path in sorted((ROOT / 'skills' / slug).rglob('*')):
            if path.is_file():
                data = path.read_bytes()
                snapshots[path] = data
                # Forwarding links should reach the existing canonical owner.
                target = ROOT / 'skills' / owner / ('GUIDE.md' if path.name == 'GUIDE.md' else 'SKILL.md')
                physical[path.resolve()] = target.resolve()
                files.append({'source': path.relative_to(ROOT).as_posix(),
                              'destination': target.relative_to(ROOT).as_posix(),
                              'source_sha256': digest(data), 'action': 'remove-forwarder-no-unique-craft'})
    sibling_files = []
    for slug, (owner, dest) in SIBLINGS.items():
        for path in sorted((ROOT / 'skills' / slug).rglob('*')):
            if path.is_file():
                sibling_files.append({'source': path.relative_to(ROOT).as_posix(),
                                      'source_sha256': digest(path.read_bytes()),
                                      'owner': owner, 'expected_resource': dest})
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    evidence = {'schema_version': 1, 'mapping': MAPPING, 'files': files,
                'removed_forwarders': SHIMS, 'sibling_sources': sibling_files,
                'sibling_retirement': 'DEFERRED_PENDING_INDEPENDENT_PARITY',
                'boundary': 'source relocation only; no commit/push/install or live discovery proof'}
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + '\n', encoding='utf-8')
    for row in files:
        if row.get('action'):
            continue
        source, target = ROOT / row['source'], ROOT / row['destination']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(snapshots[source])
        assert digest(target.read_bytes()) == row['source_sha256']
    # Relocate the old API contract/guide as a separate HTTP mode, not a mandatory
    # sequence inherited by module/import modes. Preserve the entire originals.
    api = ROOT / 'skills/api-and-interface-design'
    http = api / 'resources/http-contracts'
    http.mkdir(parents=True)
    for name, dest in [('GUIDE.md', 'guide.md'), ('SKILL.md', 'contract.md')]:
        path, target = api / name, http / dest
        data = path.read_bytes()
        evidence['files'].append({'source': path.relative_to(ROOT).as_posix(),
                                  'destination': target.relative_to(ROOT).as_posix(),
                                  'source_sha256': digest(data), 'copied_sha256': digest(data),
                                  'action': 'preserve-api-http-contract'})
        snapshots[path] = data
        physical[path.resolve()] = target.resolve()
        target.write_bytes(data)
    # Source locations recover the old base for links in a moved document.
    origins = {target: source for source, target in physical.items()
               if source in snapshots and not any(source.is_relative_to(ROOT / 'skills' / s) for s in SHIMS)}
    patterns = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
    owned = list((ROOT / 'skills').rglob('*.md')) + list((ROOT / 'references/project-setup').rglob('*.md')) + list((ROOT / 'references/workflow-advice').rglob('*.md'))
    retired = set(MAPPING) | set(SHIMS)
    for path in owned:
        if any(path.is_relative_to(ROOT / 'skills' / slug) for slug in retired):
            continue
        original = origins.get(path.resolve(), path)
        text = path.read_text(encoding='utf-8')
        def rewrite(match):
            label, href = match.groups()
            raw, sep, anchor = href.partition('#')
            if not raw or ':' in raw or raw.startswith('/'):
                return match.group(0)
            old_target = (original.parent / raw).resolve()
            target = physical.get(old_target, old_target)
            # Native member-local links survive flat install. Shared paths are
            # explicit workflow-root resolver text, never ../unprefixed-owner.
            member = next((p for p in path.parents if p.parent == ROOT / 'skills'), None)
            if member is not None and not target.is_relative_to(member):
                rootpath = target.relative_to(ROOT).as_posix() if target.is_relative_to(ROOT) else str(target)
                return f'{label} (resolve `{rootpath}{sep + anchor if sep else ""}` from the installed `andino-workflow` root)'
            rel = os.path.relpath(target, path.parent).replace('\\', '/')
            return f'[{label}]({rel}{sep + anchor if sep else ""})'
        text = patterns.sub(rewrite, text)
        # Strip every relocated contract, not subordinate schema contract.md files.
        slug = next((s for s, d in MAPPING.items() if path.is_relative_to(ROOT / d)), None)
        text = strip_registration(text, slug)
        path.write_text(text, encoding='utf-8', newline='\n')
    for slug in retired:
        source = ROOT / 'skills' / slug
        # Verify every source byte is still the captured original before deletion.
        assert all(p in snapshots and p.read_bytes() == snapshots[p] for p in source.rglob('*') if p.is_file()), source
        shutil.rmtree(source)
    evidence['removed_local_sources'] = sorted(retired)
    evidence['copied_file_count'] = sum(not row.get('action') for row in files)
    evidence['all_source_files_attributed'] = True
    for row in evidence['files']:
        target = ROOT / row['destination']
        row['destination_sha256_after_rewrite'] = digest(target.read_bytes())
    EVIDENCE.write_text(json.dumps(evidence, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'mapped_modes': len(MAPPING), 'removed_sources': len(retired), 'evidence': str(EVIDENCE), 'files': len(files)}))

if __name__ == '__main__':
    main()
