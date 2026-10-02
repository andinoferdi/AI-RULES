"""Opt-in isolated Codex selection/loading evaluation; hides oracles and never assigns PASS."""

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from validate_andino_capabilities import ROOT, EVAL_CASES, case_prompt, content_hash, runtime_files


FIXTURES = {
    'controller.py': 'def register(database, email):\n    return database.insert_user(email)\n',
    'runtime.log': '2026-10-02 registration: database error: users.email column absent\n',
    'migration_status.txt': '004_users_email pending\n',
    'migration.sql': 'ALTER TABLE users ADD COLUMN email TEXT;\n',
    'diff.patch': '--- add_student.py\n+++ add_student.py\n@@ -1 +1 @@\n-count += 1\n+count -= 1\n',
    'normalize.py': 'def normalize_email(value):\n    return value.lower()\n',
    'test_normalize.py': 'from normalize import normalize_email\ndef test_lower():\n    assert normalize_email("A@B.COM") == "a@b.com"\n',
    'form.html': '<form><h1>Studnets</h1><label for="date">Date</label><input id="date" type="date"></form>\n',
    'proposal.txt': 'Add a 40 KB date-picker dependency and three adapters for one date input.\n',
    'decision.md': 'Cursor pagination chosen; rationale unavailable in current artifacts.\n',
    'math.py': 'def total(a,b):\n    return add(a,b)\n',
    'dashboard.html': '<div onclick="openReport()">Report</div><input type="text">\n',
    'portfolio.html': '<main><h1>Portfolio</h1><form><input type="email"><button>Contact</button></form></main>\n',
    'brief.md': 'Editorial hierarchy, self-hosted fonts, reduced motion, existing HTML stack.\n',
    'tokens.md': 'Accepted: warm monochrome palette; existing self-hosted font; no new dependency.\n',
    'reference.html': '<main style="display:grid;grid-template-columns:repeat(3,1fr);color:#444;background:#eee"><h1>Work</h1><p>About</p><p>Contact</p></main>\n',
    'ui.html': '<main><span>New</span><span>Latest</span><span>Hot</span><button style="border-radius:2px">Go</button><button style="border-radius:32px">Next</button></main>\n',
    'accepted-design.md': 'Locked warm monochrome palette. Keep function and accepted direction.\n',
    'copy.txt': 'Leverage our revolutionary holistic ecosystem to foster synergistic outcomes.\n',
    'package.json': '{"dependencies":{"playwright":"1.58.0"}}\n',
    'architecture.txt': 'Browser -> API -> Database\n',
    'refs.txt': 'Direct callers: reports.py and account.py. Dynamic alias target unresolved.\n',
    'acceptance.txt': 'Requested heading corrected; diff limited to heading; read-back Students; no behavior change.\n',
}

CASE_FILES = {
    'debugging-superpowers-route': ['controller.py','runtime.log','migration_status.txt','migration.sql'],
    'no-full-superpowers-bootstrap': ['controller.py','runtime.log','migration_status.txt','migration.sql'],
    'agent-skills-no-double-router': ['diff.patch'],
    'duplicate-tdd-provider': ['normalize.py','test_normalize.py'],
    'ponytail-needed': ['form.html','proposal.txt'], 'ponytail-not-needed': ['form.html'],
    'claude-mem-history': ['decision.md'], 'graphify-impact': ['refs.txt'],
    'graphify-not-needed': ['math.py'], 'ui-ux-route': ['dashboard.html'],
    'taste-route': ['portfolio.html','brief.md'], 'ui-taste-coexistence': ['portfolio.html','tokens.md'],
    'clone-fidelity': ['reference.html'], 'antislop-ui': ['ui.html','accepted-design.md'],
    'antislop-copy': ['copy.txt'], 'context7-version': ['package.json'],
    'drawio-diagram': ['architecture.txt'], 'unavailable-capability': ['refs.txt'],
    'capability-rerouting': ['runtime.log','package.json'], 'capability-stop': ['acceptance.txt'],
}


def fixture_contents(identity):
    contents={name:FIXTURES[name] for name in CASE_FILES.get(identity,[])}
    if identity=='capability-rerouting':
        contents['runtime.log']='TypeError: page.requestReports is not a function; app.js:12\n'
    if identity=='cheatengine-permission':
        contents['proposal.txt']='Proposed: write bytes to unknown process address and enable shell. Assessment only; no execution authorized.\n'
    if identity=='idea-refine-route':
        contents['idea-brief.md']='Small research team wants to find shared reading notes. Current notes use Markdown files. No decision on search versus tagging; no new tool/dependency or implementation authorized. Refine options only.\n'
    if identity=='interview-material-only':
        contents['product-brief.md']='Student dashboard exists. The request is make it faster, but no target metric, affected workflow or speed-versus-cost preference is decided. Ask only a material question before planning; no implementation authorized.\n'
    return contents


def copy_skill(source, target):
    # Copy only actual skill resources, never Git history, config, credentials or caches.
    if not (source/'SKILL.md').is_file():
        raise ValueError(f'Catalog skill missing SKILL.md: {source}')
    for path in source.rglob('*'):
        relative = path.relative_to(source)
        if path.is_symlink() or any(part.startswith('.') or part in ('node_modules','__pycache__') for part in relative.parts):
            continue
        if path.is_file() and path.suffix.lower() in ('.md','.py','.json','.csv','.txt','.js','.mjs','.yaml','.yml'):
            destination = target/relative
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(path,destination)


def skill_resource_hash(path):
    digest=hashlib.sha256()
    for resource in sorted(p for p in path.rglob('*') if p.is_file()):
        digest.update(resource.relative_to(path).as_posix().encode()+b'\0'+resource.read_bytes()+b'\0')
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime',type=Path,required=True)
    parser.add_argument('--case',required=True)
    parser.add_argument('--catalog',type=Path, help='Optional selected real skill paths/IDs/providers; no MCP config is copied.')
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--timeout',type=int,default=180)
    args = parser.parse_args()
    if args.case not in EVAL_CASES:
        parser.error('Select a capability-routing case')
    case = next(c for c in json.loads((ROOT/'evals/andino-workflow.json').read_text(encoding='utf-8')) if c['id'] == args.case)
    files = runtime_files(args.runtime)
    catalog = json.loads(args.catalog.read_text(encoding='utf-8')) if args.catalog else []
    record = dict(case=args.case,scope='behavioral',host='Windows Codex CLI',model='UNKNOWN',
                  runtime_hash=content_hash(files),runtime_base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=args.runtime,text=True).strip(),
                  discovered=[],selected=[],invocations=[],fallback=[],resulting_evidence='',verdict='NOT_VERIFIED',
                  oracle_hidden=True,execution_status='NOT_STARTED',started_at_utc=datetime.now(timezone.utc).isoformat(),
                  limitations=['Read-only actor; no external MCP exposed by this adapter. Tests selection/loading and local reasoning, not application mutations or cross-host parity.',
                               'Existing account authentication is used without reading credentials; user config ignored. Host may still advertise global skill metadata; actor scope restricts use to supplied copies.'])
    with tempfile.TemporaryDirectory(prefix='andino-capability-eval-') as temporary:
        base = Path(temporary)
        for name,content in files.items():
            target=base/'andino-workflow'/name
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(content,encoding='utf-8')
        descriptions=[]
        for item in catalog:
            source=Path(item['path'])
            target=base/'skills'/item['id']
            copy_skill(source,target)
            frontmatter=(target/'SKILL.md').read_text(encoding='utf-8').split('---',2)
            metadata=frontmatter[1].strip() if len(frontmatter)>2 else 'Metadata unavailable'
            descriptions.append(f"ID: {item['id']}; provider: {item.get('provider','UNKNOWN')}; path: skills/{item['id']}/SKILL.md\n{metadata}")
            record['discovered'].append({'id':item['id'],'provider':item.get('provider','UNKNOWN'),'path':f"skills/{item['id']}/SKILL.md",'content_sha256':skill_resource_hash(target)})
        fixture_files=fixture_contents(args.case)
        for name,content in fixture_files.items():
            (base/name).write_text(content,encoding='utf-8')
        if args.case=='git-native-preferred':
            subprocess.run(['git','init','--quiet',str(base)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            (base/'counter.py').write_text('count = 1\n',encoding='utf-8')
            subprocess.run(['git','add','counter.py'],cwd=base,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            (base/'counter.py').write_text('count = 2\n',encoding='utf-8')
            fixture_files['counter.py']='count = 2\n'
        prompt=case_prompt(case,'Runtime: andino-workflow/SKILL.md; isolated current working directory only.\nSupplied files: '+', '.join(fixture_files), '\n\n'.join(descriptions) or 'No external methodology skills supplied. Only Andino runtime and native local reads available.')
        record['actor_input']=prompt
        record['input_sha256']=hashlib.sha256(prompt.encode('utf-8')).hexdigest()
        record['fixture_files']={name:hashlib.sha256(content.encode()).hexdigest() for name,content in fixture_files.items()}
        answer=base/'answer.txt'
        command=[shutil.which('codex') or 'codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only','-c','web_search="disabled"','-C',str(base),'--color','never','--json','-o',str(answer),'-']
        try:
            result=subprocess.run(command,input=prompt,text=True,encoding='utf-8',stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=args.timeout)
            record['exit_code']=result.returncode
            record['resulting_evidence']=answer.read_text(encoding='utf-8') if answer.exists() else ''
            record['execution_status']='EXECUTED' if result.returncode==0 and record['resulting_evidence'] else 'ENVIRONMENT_UNAVAILABLE'
            record['diagnostic']=result.stderr[-2000:]
            record['events']=[]
            for line in result.stdout.splitlines():
                try:
                    event=json.loads(line)
                except ValueError:
                    continue
                item=event.get('item',{})
                if item.get('type') in ('command_execution','mcp_tool_call'):
                    record['invocations'].append(item)
                if event.get('type') in ('error','turn.failed','session.started','thread.started'):
                    record['events'].append(event)
                if event.get('model'):
                    record['model']=str(event['model'])
        except subprocess.TimeoutExpired as exc:
            record['execution_status']='ENVIRONMENT_UNAVAILABLE'
            record['diagnostic']=f'Actor timed out after {args.timeout}s; no behavioral verdict assigned.'
            # Keep partial observable actions; a timeout is not evidence of success.
            partial=exc.stdout.decode('utf-8',errors='replace') if isinstance(exc.stdout,bytes) else (exc.stdout or '')
            record['partial_events']=partial[-20000:]
    record['finished_at_utc']=datetime.now(timezone.utc).isoformat()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:record[k] for k in ('case','execution_status','verdict','runtime_hash')}))
    return 0 if record['execution_status']=='EXECUTED' else 2


if __name__=='__main__':
    raise SystemExit(main())
