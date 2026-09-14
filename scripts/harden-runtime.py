"""Narrow local hardening of existing installs; never installs skills or changes MCPs.

Requires PyYAML. Run after sync-workflow.py. Backups stay under the selected home.
Claude/OpenCode explicit-only workers require a user invocation; this script does
not create a file-reading workaround for native invocation restrictions.
"""
from pathlib import Path
import argparse, datetime, json, re, shutil
import yaml

CORE = ('systematic-debugging', 'test-driven-development',
        'verification-before-completion', 'code-review-and-quality')
HOSTS = {
    'codex': ('.codex/AGENTS.md', '.agents/skills/andino-workflow', '.codex/skills'),
    'claude': ('.claude/CLAUDE.md', '.claude/skills/andino-workflow', '.claude/skills'),
    'opencode': ('.config/opencode/AGENTS.md', '.config/opencode/skills/andino-workflow', '.config/opencode/skills'),
    'antigravity': ('.gemini/GEMINI.md', '.gemini/config/skills/andino-workflow', '.gemini/config/skills'),
}

def harden(home):
    home = home.resolve()
    backup = home / '.andino/backups' / ('acceptance-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    changes = []
    def write(path, text):
        old = path.read_text(encoding='utf-8-sig') if path.exists() else None
        if old == text:
            return
        relative = path.resolve().relative_to(home)
        if path.exists():
            target = backup / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        changes.append(relative.as_posix())

    for host, (rules, installed, workers) in HOSTS.items():
        reference = home / installed / 'references/ui-coexistence.md'
        if not reference.is_file():
            raise RuntimeError(f'Missing installed reference: {reference}')
        path = home / rules
        text = path.read_text(encoding='utf-8-sig')
        text, count = re.subn(r'(?m)^UI coexistence reference: .*$',
                             'UI coexistence reference: ' + reference.as_posix(), text)
        if count != 1:
            raise RuntimeError(f'Expected one managed UI reference: {path}')
        write(path, text)
        for name in CORE:
            path = home / workers / name / 'SKILL.md'
            text = path.read_text(encoding='utf-8-sig')
            match = re.match(r'---\s*\n(.*?)\n---\n', text, re.S)
            if not match:
                raise RuntimeError(f'Invalid frontmatter: {path}')
            fm = yaml.safe_load(match[1])
            if host == 'codex':
                policy = path.parent / 'agents/openai.yaml'
                data = yaml.safe_load(policy.read_text()) if policy.exists() else {}
                data.setdefault('policy', {})['allow_implicit_invocation'] = False
                write(policy, yaml.safe_dump(data, sort_keys=False))
            elif host == 'claude':
                fm['disable-model-invocation'] = True
                write(path, '---\n' + yaml.safe_dump(fm, sort_keys=False) + '---\n' + text[match.end():])
            elif host == 'opencode':
                # V1 enforcement is permission.skill below, not V2 metadata.
                fm.setdefault('metadata', {})['opencode/autoinvoke'] = 'false'
                write(path, '---\n' + yaml.safe_dump(fm, sort_keys=False) + '---\n' + text[match.end():])
            else:
                # No verified native non-implicit flag: constrain trigger, report soft control.
                prefix = 'Use only when explicitly requested or selected by andino-workflow for the current phase. '
                if not fm['description'].startswith(prefix):
                    fm['description'] = prefix + fm['description']
                    write(path, '---\n' + yaml.safe_dump(fm, sort_keys=False) + '---\n' + text[match.end():])
    path = home / '.config/opencode/opencode.json'
    config = json.loads(path.read_text(encoding='utf-8-sig'))
    for name in CORE:
        config.setdefault('permission', {}).setdefault('skill', {})[name] = 'deny'
    write(path, json.dumps(config, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'changed': changes, 'backup': str(backup) if changes else None}, indent=2))
    return changes

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home())
    harden(parser.parse_args().home)
