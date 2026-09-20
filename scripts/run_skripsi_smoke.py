"""Run one oracle-hidden skill scenario in a disposable read-only Codex context.

Opt-in live evaluation; never called by deterministic CI. Uses the installed CLI
and its existing authentication, without reading credential files.
"""

import argparse
import json
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--runtime', type=Path, required=True)
    p.add_argument('--case', required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--timeout', type=int, default=180)
    a = p.parse_args()
    case = next(c for c in json.loads((ROOT / 'evals/skripsi-skill.json').read_text(encoding='utf-8')) if c['id'] == a.case)
    fixtures = json.loads((ROOT / 'evals/skripsi-fixtures.json').read_text(encoding='utf-8'))
    spec = fixtures['cases'].get(a.case, {})
    fixture = '\n'.join(filter(None, [fixtures['notice'], fixtures.get(spec.get('base',''), ''), spec.get('extra','')])) if spec else ''
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=a.runtime, text=True).strip()
    with tempfile.TemporaryDirectory(prefix='skripsi-eval-') as temporary:
        base = Path(temporary)
        skill = base / 'skripsi-skill'
        skill.mkdir()
        for name in ('SKILL.md', 'README.md'):
            shutil.copy2(a.runtime / name, skill / name)
        for name in ('references', 'assets'):
            shutil.copytree(a.runtime / name, skill / name)
        prompt = ('This is a read-only isolated research-skill evaluation. Only inspect files inside your working directory. '
                  'Do not use network, external connectors, other repositories or write files. '
                  'An available skill is skripsi-skill at skripsi-skill/SKILL.md. '
                  'Use it when appropriate to the request, loading only relevant references. '
                  'No other user artifacts were supplied unless explicitly included below. '
                  'Respond naturally to the request in Indonesian.\n\nUser context:\n' + fixture + '\n\nUser request:\n' + case['prompt'])
        last = base / 'answer.txt'
        command = [shutil.which('codex') or 'codex', 'exec', '--ignore-user-config', '--ephemeral',
                   '--skip-git-repo-check', '--sandbox', 'read-only', '-C', str(base),
                   '--color', 'never', '--json', '-o', str(last), '-']
        record = {'case': a.case, 'host': 'Windows Codex CLI', 'runtime_revision': revision,
                  'fixture': fixture or 'Isolated runtime copy; no additional research artifacts',
                  'prompt': case['prompt'], 'oracle_hidden': True, 'verdict': 'NOT_VERIFIED'}
        record['started_at_utc'] = datetime.now(timezone.utc).isoformat()
        record['model_selection'] = 'CLI default; no model override'
        try:
            result = subprocess.run(command, input=prompt, text=True, encoding='utf-8',
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=a.timeout)
            record['exit_code'] = result.returncode
            record['observed_output'] = last.read_text(encoding='utf-8') if last.exists() else ''
            record['execution_status'] = 'EXECUTED' if result.returncode == 0 and record['observed_output'] else 'ENVIRONMENT_UNAVAILABLE'
            record['diagnostic'] = result.stderr[-2000:] if result.returncode else ''
            record['events'] = []
            record['tool_actions'] = []
            for line in result.stdout.splitlines():
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if event.get('type') in ('error', 'turn.failed'):
                    record['events'].append(event)
                item = event.get('item', {})
                if item.get('type') in ('command_execution', 'mcp_tool_call'):
                    record['tool_actions'].append({k:v for k,v in item.items() if k in ('type','command','tool','status','exit_code')})
        except subprocess.TimeoutExpired:
            record['execution_status'] = 'ENVIRONMENT_UNAVAILABLE'
            record['diagnostic'] = f'CLI timed out after {a.timeout} seconds; no behavior verdict.'
        a.output.parent.mkdir(parents=True, exist_ok=True)
        record['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
        a.output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({k: record[k] for k in ('case', 'execution_status', 'runtime_revision', 'verdict')}))


if __name__ == '__main__':
    main()
