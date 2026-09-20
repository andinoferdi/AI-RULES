"""Reconcile the supplied SRS/plan with reviewed runtime ownership mappings.

Local planning inputs remain outside Git. This produces a requirement inventory,
not a claim that an agent passed behavioral acceptance.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

REFS = {
 'state': 'research-state-and-routing', 'intent': 'intent-and-context',
 'evidence': 'evidence-guidelines-integrity', 'integration': 'andino-integration',
 'discovery': 'discovery-feasibility', 'title': 'title-development',
 'revision': 'revision-consistency', 'proposal': 'proposal-bab-1-3',
 'problem': 'research-problem-gap-rq', 'reasoning': 'scientific-reasoning',
 'design': 'research-design-routing', 'search': 'literature-search-screening',
 'reading': 'progressive-reading-synthesis', 'systematic': 'systematic-review',
 'quant': 'quantitative-planning', 'advanced': 'advanced-methodology-integrity',
 'results': 'results-discussion-conclusion', 'defense': 'defense-and-revision',
}


def group(mapping, owner, numbers):
    for number in numbers:
        if number in mapping:
            raise ValueError(f'Duplicate owner for {number}')
        mapping[number] = owner


FR = {}
for owner, numbers in {
 'state': [1,2,3], 'discovery': [4,7], 'evidence': [5,6,12,22],
 'title': [8,9,*range(23,31)], 'design': [10,50,51,52,53],
 'revision': [11,15,16,17,18,71], 'proposal': [13,14,39,54,55],
 'integration': [19,20], 'SKILL': [21], 'intent': list(range(31,39)),
 'reasoning': [40,44,46,48,49], 'problem': [41,42,43,45],
 'reading': [47,76,77,134,135,136,137,138,139,145,146],
 'results': [*range(56,71),72], 'advanced': [73,74,75,*range(79,89)],
 'quant': [78,*range(107,125)], 'defense': list(range(89,107)),
 'search': list(range(125,134)), 'systematic': list(range(140,145)),
}.items():
    group(FR, owner, numbers)

NFR = dict(enumerate([
 'SKILL','SKILL','SKILL','state','evidence','SKILL','control','evidence','SKILL',
 'state','intent','intent','intent','intent','design','problem','revision','evidence',
 'results','results','results','results','revision','advanced','reading','quant',
 'advanced','advanced','advanced','defense','defense','defense','defense','defense',
 'defense','quant','quant','quant','quant','quant','search','reading','reading',
 'reading','reading','systematic','search'], 1))

# Acceptance criteria follow the source's exact checkbox order. These links were
# reconciled against AN rather than inferred from keyword similarity.
AC_FR = [
 1,2,4,22,6,5,7,8,23,29,25,26,27,28,30,31,38,32,34,35,36,37,
 40,41,42,43,45,46,47,48,49,50,51,52,53,54,55,
 56,57,57,59,72,60,61,62,63,64,65,66,67,68,69,70,71,
 73,74,75,76,77,78,78,79,80,81,82,83,84,85,87,88,
 89,90,91,92,92,93,94,95,96,97,100,99,101,102,103,104,105,106,
 107,107,108,109,110,111,112,113,114,115,116,117,118,118,119,120,121,122,123,124,
 126,127,127,128,129,131,133,134,134,135,137,136,138,139,140,140,142,141,144,146,
 10,10,10,10,11,12,13,14,16,17,19,20,21,21,
]


def eval_owner(n):
    explicit = {1:'discovery',2:'state',3:'evidence',4:'evidence',5:'design',6:'design',7:'design',
                8:'revision',9:'revision',10:'SKILL',27:'reasoning',28:'problem',29:'design',30:'design',31:'design',32:'proposal',33:'reasoning',34:'proposal',
                49:'revision',52:'reading',53:'quant',54:'quant',74:'revision'}
    if n in explicit:
        return explicit[n]
    for lower, upper, owner in [(11,16,'title'),(17,23,'intent'),(24,26,'problem'),(35,48,'results'),
                                (50,62,'advanced'),(63,77,'defense'),(78,93,'quant'),(94,96,'search'),
                                (97,100,'reading'),(101,102,'search'),(103,103,'reading'),(104,107,'systematic'),(108,110,'reading')]:
        if lower <= n <= upper:
            return owner
    raise ValueError(n)


def location(owner):
    if owner == 'SKILL':
        return {'branch': 'skripsi-skill', 'path': 'SKILL.md'}
    if owner == 'control':
        return {'branch': 'main', 'path': 'evals/skripsi-skill.json'}
    return {'branch': 'skripsi-skill', 'path': f'references/{REFS[owner]}.md'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('srs', type=Path)
    p.add_argument('plan', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    text = a.srs.read_text(encoding='utf-8')
    plan = a.plan.read_text(encoding='utf-8')
    records = []
    for prefix, start, end, owners, expected in [
        ('FR','AL. FUNCTIONAL REQUIREMENTS','AM. NON-FUNCTIONAL REQUIREMENTS',FR,146),
        ('NFR','AM. NON-FUNCTIONAL REQUIREMENTS','AN. ACCEPTANCE CRITERIA',NFR,47)]:
        section = text.split(start,1)[1].split(end,1)[0]
        matches = re.findall(rf'(?m)^({prefix}-(\d{{3}})) — ([^\n]+)\n(.*?)(?=\n{prefix}-|\n={{5,}}|\Z)', section, re.S)
        if len(matches) != expected or len(owners) != expected:
            raise ValueError(f'{prefix} count drift: {len(matches)}')
        for ident, number, title, body in matches:
            owner = owners[int(number)]
            records.append(dict(id=ident, requirement=title + ' — ' + ' '.join(body.split()),
                                implementation=location(owner), contract_review='REVIEWED',
                                behavioral_verdict='NOT_VERIFIED',
                                evidence='contract-review.md',
                                eval_ids=[f'EVAL-{i:03}' for i in range(1,111) if eval_owner(i)==owner]))
    acs = re.findall(r'(?m)^\[ \] (.+)$', text.split('AN. ACCEPTANCE CRITERIA',1)[1].split('AO. INITIAL EVALUATION CASES',1)[0])
    if len(acs) != 142 or len(AC_FR) != 142:
        raise ValueError(f'AC count drift: source={len(acs)}, mapping={len(AC_FR)}')
    for i, (statement, fr) in enumerate(zip(acs, AC_FR),1):
        owner = FR[fr] if i < 142 else 'control'
        records.append(dict(id=f'AC-{i:03}', requirement=statement, related_fr=f'FR-{fr:03}',
                            implementation=location(owner), contract_review='REVIEWED',
                            behavioral_verdict='NOT_VERIFIED', evidence='contract-review.md'))
    caps = re.findall(r'(?m)^(\d+)\. (.+)$',text.split('F. SCOPE VERSI 0.9',1)[1].split('G. OUT OF SCOPE',1)[0])
    cap_owners=['discovery','state','discovery','revision','title','revision','proposal','proposal',
                'design','design','design','design','evidence','revision','integration',
                'defense','defense','defense','defense','defense','defense','defense','defense',
                'quant','search','search','search','reading','reading','reading','reading','systematic']
    if len(caps)!=32:
        raise ValueError('Capability inventory drift')
    capabilities=[dict(id=f'CAP-{int(n):02}',name=name,implementation=location(owner)) for (n,name),owner in zip(caps,cap_owners)]
    tasks=[]
    for line in plan.splitlines():
        if re.match(r'^\| P\d+-T\d+ \|',line):
            cells=[s.strip() for s in line.strip('|').split('|')]
            if any(t['id']==cells[0] for t in tasks):
                continue
            phase=int(re.search(r'P(\d+)',cells[0])[1])
            tasks.append(dict(id=cells[0], objective=cells[1], dependencies=cells[3],
                              acceptance=cells[5], validation=cells[6],
                              status='PREVIOUSLY_ACCEPTED' if phase<2 or cells[0]=='P2-T01' else 'IMPLEMENTED_REVIEW_PENDING',
                              evidence='contract-review.md'))
    evals=[dict(id=f'EVAL-{i:03}',implementation=location(eval_owner(i)),
                contract_review='REVIEWED', behavioral_verdict='NOT_VERIFIED',
                evidence='contract-review.md') for i in range(1,111)]
    output=dict(srs_sha256=hashlib.sha256(a.srs.read_bytes()).hexdigest(),
                plan_sha256=hashlib.sha256(a.plan.read_bytes()).hexdigest(),
                counts=dict(FR=146,NFR=47,AC=142,capabilities=32,initial_evals=110,tasks=len(tasks)),
                scope='Implementation ownership and written-contract review; not live behavioral proof.',
                requirements=records,capabilities=capabilities,evals=evals,tasks=tasks)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output['counts']))


if __name__ == '__main__':
    main()
