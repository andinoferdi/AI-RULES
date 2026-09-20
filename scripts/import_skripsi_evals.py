"""Import the explicitly supplied SRS cases; no model execution or pass claims."""

import argparse
import json
import re
from pathlib import Path


def parse_cases(text):
    section = text.split('AO. INITIAL EVALUATION CASES', 1)[1].split('AP. FUTURE EXPANSION MODEL', 1)[0]
    blocks = re.split(r'(?m)^Case (\d+) — ([^\n]+)\n', section)
    cases = []
    for offset in range(1, len(blocks), 3):
        number, title, body = blocks[offset:offset + 3]
        match = re.search(r'Prompt:\s*(.*?)\s*Expected:\s*(.*?)\s*Forbidden:\s*(.*)', body, re.S)
        if not match:
            raise ValueError(f'Incomplete case {number}')
        values = [re.split(r'\n[-=]{5,}', value)[0].strip() for value in match.groups()]
        cases.append(dict(id=f'EVAL-{int(number):03}', kind='negative-trigger' if int(number) == 10 else 'behavior',
                          title=title.strip(), prompt=values[0], expected=values[1], forbidden=values[2]))
    if [case['id'] for case in cases] != [f'EVAL-{i:03}' for i in range(1, 111)]:
        raise ValueError('SRS case inventory differs from 110 ordered cases; review drift')
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('srs', type=Path)
    parser.add_argument('--through', type=int, default=110)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    cases = parse_cases(args.srs.read_text(encoding='utf-8'))
    selected = cases[:args.through]
    if args.through == 110:
        supplemental = Path(__file__).resolve().parents[1] / 'evals/skripsi-supplemental.json'
        selected.extend(json.loads(supplemental.read_text(encoding='utf-8')))
    args.output.write_text(json.dumps(selected, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Imported {len(selected)} source cases; behavior NOT VERIFIED')


if __name__ == '__main__':
    main()
