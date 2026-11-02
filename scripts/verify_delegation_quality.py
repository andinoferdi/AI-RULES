"""Static delegation contract checks, not fresh-model or implementation proof."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/delegation'


def check_contract():
    errors = []
    documents = {p.relative_to(SKILL).as_posix(): p.read_text(encoding='utf-8')
                 for p in SKILL.rglob('*.md')}
    for required in ('resources/contract.md', 'resources/worked-example.md'):
        if required not in documents:
            errors.append(f'Missing {required}')
    skill = documents['SKILL.md']
    if len(skill.splitlines()) >= 150:
        errors.append('SKILL.md must stay below 150 lines')
    if not re.search(r'^description: Use when\b', skill, re.M):
        errors.append('Description must identify when to select delegation')
    forbidden = (
        'Resume dispatch immediately without asking',
        'resume the fix loop at round',
        'controller **never writes production code fixes directly**',
        'dispatch one final whole-branch code review on the capable tier at high effort',
        'If clean, purge plan scratch workspace',
        'Exit Condition**: Tests green and diff accepted (plus clean reviewer verdict for risky tasks) OR',
    )
    for name, body in documents.items():
        for phrase in forbidden:
            if phrase in body:
                errors.append(f'{name}: contradictory directive: {phrase}')
        for destination in re.findall(r'\[[^\]]+\]\(([^)]+)\)', body):
            link = urlsplit(destination)
            if not link.scheme and not link.netloc and link.path:
                if not (SKILL / name).parent.joinpath(unquote(link.path)).is_file():
                    errors.append(f'{name}: broken local link: {destination}')

    briefs = documents['resources/subagent-brief-and-report-schemas.md']
    for template in re.findall(r'```(?:markdown|yaml)\n(.*?)```', briefs, re.S):
        if 'model:' in template and 'effort:' not in template:
            errors.append('Dispatch template omits explicit effort')
    for term in ('NEEDS_CONTEXT', 'DONE_WITH_CONCERNS', 'BLOCKED',
                 'Global Constraints', 'Content identity', 'Working directory'):
        if term not in briefs:
            errors.append(f'Brief/report recipe missing {term}')
    contract = documents.get('resources/contract.md', '')
    for term in ('UNVERIFIED', 'required acceptance', 'go-ahead',
                 'relinquishes ownership', 'NOT_VERIFIED', 'source, check and environment'):
        if term not in contract:
            errors.append(f'Contract missing {term}')
    return errors


if __name__ == '__main__':
    errors = check_contract()
    for error in errors:
        print('FAIL:', error)
    print(f'Static delegation contract: {len(errors)} issue(s). Model behavior NOT_VERIFIED.')
    sys.exit(bool(errors))
