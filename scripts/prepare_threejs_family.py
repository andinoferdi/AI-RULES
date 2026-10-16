"""Copy the supplied collection into a runtime worktree; never edit the input."""

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


INTEGRATION = """## AI-RULES integration

Use this specialist only for the domain need described above. Ordinary frontend
work without that need is excluded. Inspect the project's actual Three.js and
renderer versions before applying examples; examples are not compatibility claims.
This is an internal method of the installed threejs-skills family. Resolve selected
siblings as ../<method-id>/GUIDE.md within that family, through authorized resource
reads after family invocation; they are not separate native skill registrations.
An absent sibling is optional guidance, not an installation dependency.
Never bypass explicit-only or denied invocation controls by reading another path.
Load the minimum relevant specialists at the phase where they are needed.

When Andino Workflow is active it owns the single execution plan, checkpoints,
handoff and DONE decision. Focus owns communication; Search First owns relevant
solution/API research. Return domain results, evidence, limitations and recommended
actions to that existing context. Without Andino use the host's normal task context.
Provider job journals and render-resource lifecycles are technical state, not a
second task lifecycle. Installation, discovery, activation and observed use differ.
External services, paid generation, delegation and publication need applicable
task authorization; this skill grants none.

"""

FAMILY = """---
name: threejs-skills
description: Apply the bundled Three.js and NixieFX specialist methods for 3D scenes, shaders, lighting, animation, geometry, interactions, games and particle effects. Use for an explicit specialist name or select relevant methods from the prompt. Excludes ordinary frontend work and general task orchestration.
---

# Three.js Skills

This is one installed skill containing 45 domain methods. They are internal
resources, not separately registered native skills or installation dependencies.
The user can say "use andino-workflow and threejs-skills" for automatic selection,
or "use threejs-skills, specifically threejs-shaders" to choose a method explicitly.

## Select and apply

1. Identify the actual current need and any explicitly requested method. Honor an
   explicit relevant choice. Ordinary frontend work needs no Three.js method.
   For an unknown-cause failure use the host's debugging method first, then add
   a domain method when evidence identifies its need; do not guess shader/light.
2. For a narrow need read the corresponding local guide directly:
   shaders -> `skills/threejs-shaders/GUIDE.md`; lighting ->
   `skills/threejs-lighting/GUIDE.md`; keyframe/skeletal animation ->
   `skills/threejs-animation/GUIDE.md`; materials ->
   `skills/threejs-materials/GUIDE.md`; geometry ->
   `skills/threejs-geometry/GUIDE.md`; picking/input ->
   `skills/threejs-interaction/GUIDE.md`.
   For other needs consult [the method index](references/specialists.md) and load
   the minimum distinct guides needed now. A shader-and-light request needs those
   two methods, not all 45. Game Director is only for game-wide production;
   the optional domain advisor supports complex technical selection, not a second
   dispatcher or bootstrap chain. Do not invoke them recursively.
3. Resolve guide paths relative to this installed family directory, read each
   selected GUIDE.md through an authorized resource-reading tool and apply its
   technical method. Resolve that guide's examples/references/scripts relative to
   its own directory. Never require a native `$threejs-shaders` registration.
   If a sibling method is recommended, use the same need/permission check first.
4. Return the domain result, evidence, limitations and next recommendation. Loading
   is ACTIVE; USED also requires meaningful application, not just naming a method.
   Identify the actual guide when relevant to evidence. Unselected methods are
   NOT_NEEDED. Missing or restricted resources are UNAVAILABLE: use an honest
   native fallback without claiming their use or reading alternate denied copies.

Invoke this family through the actual host skill mechanism before loading its
resources. Permission to read bundled guides is subordinate to host/project rules;
this is not a bypass of a denied family, method or resource. Discovery, availability,
permission, activation and use remain distinct. Reassess after changed needs/resume;
release irrelevant methods rather than accumulating the whole collection.

## Ownership and limits

With Andino active it owns lifecycle, routing, one plan/checkpoint, handoff and DONE.
This family supplies domain selection and methods within that task. Focus controls
communication; Search First handles relevant solution/version research. Without
Andino use the host's existing task context. No new plan, checkpoint or delegation
is implied. Paid services, credentials, external writes and publication still need
applicable task authorization. Installation makes no API calls or npm installs.
Rendering, performance and browser interaction claims require observed evidence;
static review does not verify rendering. Read [the package guide](README.md).
"""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def prepare(source, destination, inventory_path):
    if not source.is_dir():
        raise ValueError('source collection must be a directory')
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        # A managed worktree has a .git administrative pointer.
        if any(p.name != '.git' for p in destination.iterdir()):
            raise ValueError('destination must be an empty runtime worktree')
    candidates = sorted(source.glob('*/SKILL.md'))
    if len(candidates) != len(list(source.rglob('SKILL.md'))):
        raise ValueError('nested skill requires explicit inventory review')
    inventory = {'schema_version': 1, 'source': source.name + '/ (user-supplied local input)', 'skills': [],
                 'provenance': 'Maintainer reports original collection authorship on 2026-10-16; embedded third-party notices remain authoritative for those materials; no new blanket license inferred.',
                 'publication': 'LOCAL ONLY; publication not authorized; maintainer authorship attestation recorded separately from third-party notices.'}
    for path in source.rglob('*'):
        if path.is_symlink() or getattr(path, 'is_junction', lambda: False)():
            raise ValueError(f'link in source collection: {path}')
    for skill in candidates:
        body = skill.read_text(encoding='utf-8')
        header, content = body.split('\n---\n', 1)
        fields = dict(line.split(':', 1) for line in header.splitlines()[1:] if line.strip())
        fields = {k: v.strip() for k, v in fields.items()}
        name = fields['name']
        if name != skill.parent.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            raise ValueError(f'invalid skill identity: {skill}')
        description = fields['description']
        if description.startswith('"'):
            description = json.loads(description)
        # Preserve the plain-scalar-only family validator contract.
        description = description.replace(': ', ' - ')
        if not 1 <= len(description) <= 1024:
            raise ValueError(f'invalid description: {name}')
        target = destination / 'skills' / name
        shutil.copytree(skill.parent, target)
        entries = []
        for path in sorted(skill.parent.rglob('*')):
            if path.is_symlink() or getattr(path, 'is_junction', lambda: False)():
                raise ValueError(f'link in source package: {path}')
            if not path.is_file():
                continue
            data = path.read_bytes()
            # Read complete text resources for metadata/reference/risk analysis.
            binary = path.suffix.lower() in {'.jpg', '.png', '.webp', '.bin', '.exr', '.glb', '.wasm', '.gz'}
            text = '' if binary else data.decode('utf-8')
            findings = []
            if re.search(r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|\bAKIA[A-Z0-9]{16}\b|\b(?:sk|AIza)[-_][A-Za-z0-9]{24,}', text):
                findings.append('potential credential; manual review required')
            entries.append({'path': path.relative_to(skill.parent).as_posix(),
                            'bytes': len(data), 'sha256': digest(data),
                            'kind': 'binary' if binary else 'text', 'findings': findings})
        if name == 'threejs-game-director':
            content = content.replace('Own the end-to-end game outcome:', 'Coordinate the domain production outcome:')
            start = content.index('The lead owns shared interfaces')
            end = content.index("Report what you ran", start)
            content = content[:start] + ('Keep shared interfaces, integration and verification in the existing host task. '
                'Delegate only when the user or applicable project rules explicitly authorize it.\n\n') + content[end:]
            content = content.replace('For complete games and broad upgrades, read all five production skills before implementing, plus generators whose trigger surfaces exist.',
                'For complete games and broad upgrades, select only specialists addressing a current unresolved need and activate them through the permitted host mechanism at phase entry.')
            start = content.index('For substantial tasks maintain `artifacts/game-progress.md`')
            end = content.index('\n\n', start)
            content = content[:start] + ('For substantial tasks update the existing Andino execution plan or normal host task record with intent, decisions, completed work, pending provider task IDs and remaining defects. '
                'Do not create a second progress checkpoint. Preserve completed assets and reconcile pending jobs after interruption.') + content[end:]
            recovery = target / 'references/asset-recovery.md'
            recovery.write_text(recovery.read_text(encoding='utf-8').replace('`artifacts/game-progress.md`', 'the existing Andino plan or host task record'), encoding='utf-8')
            agent = target / 'agents/openai.yaml'
            agent.write_text(agent.read_text(encoding='utf-8').replace('Orchestrate complete Three.js games', 'Coordinate Three.js game production').replace('route the relevant specialists automatically', 'recommend relevant specialists within the active host task and its invocation controls'), encoding='utf-8')
        if name == 'threejs-skill-router':
            content = content.replace('## Acceptance gate', '## Domain evidence to return')
            content = content.replace('A routed task is incomplete until the implementation exposes:',
                'Return these domain checks to the active lifecycle owner when applicable:')
        heading, rest = content.lstrip().split('\n', 1)
        result = f'---\nname: {name}\ndescription: {description}\n---\n\n{heading}\n\n{INTEGRATION}{rest.lstrip()}'
        (target / 'SKILL.md').write_text(result, encoding='utf-8')
        readme = f'''# {name}

{description}

This is an internal method bundled in `threejs-skills`, not an individual installer
choice or native skill. Read [GUIDE.md](GUIDE.md) for the method; its supporting
resources remain relative to this directory. Install the complete family:

```sh
ai-rules setup --host codex --capability threejs-skills --scope project --project-root . --source latest
```

Use "threejs-skills, specifically {name}" or let the family select by need.
With Andino, return evidence/results to its single task context. Preserve supplied
notices, observe project versions, and get task authorization for paid services.
Update the family through the existing CLI; modified/unmanaged targets are preserved.
'''
        (target / 'README.md').write_text(readme, encoding='utf-8')
        for entry in entries:
            entry['runtime_sha256'] = digest((target / entry['path']).read_bytes())
        inventory['skills'].append({'name': name, 'description': description,
            'role': 'domain-advisor' if name == 'threejs-skill-router' else 'game-production-specialist' if name == 'threejs-game-director' else 'specialist',
            'sibling_suggestions': sorted(set(re.findall(r'\b(?:threejs|nixie-fx)-[a-z0-9-]+', body)) - {name}),
            'license_notices': [e['path'] for e in entries if 'LICENSE' in e['path'] or 'GPL-' in e['path']],
            'files': entries})
    (destination / 'SKILL.md').write_text(FAMILY, encoding='utf-8')
    readme = '''# Three.js Skills for AI-RULES

One installable family containing all 45 original Three.js/NixieFX methods and
supporting resources. Use for scene/rendering/game/particle needs, not ordinary
frontend work. Andino owns lifecycle when active; Focus controls communication.

## Installation

Select only **Three.js Skills** in Custom, or select **Three.js Development** for
the family plus Andino Workflow, Focus and Search First (four installed directories).

```sh
ai-rules setup --host codex --capability threejs-skills --scope project --project-root . --source latest
ai-rules setup --host codex --profile threejs --scope project --project-root . --source latest
ai-rules setup --host codex --capability threejs-skills --scope global --source bundled
ai-rules update --host codex --capability threejs-skills --scope project --project-root . --source latest
```

Bundled distributions use the pinned family revision; latest resolves its branch.
Use the same host/scope when updating. Existing staging, verification, backup and
rollback apply to the entire directory. Modified or unrecognized targets need
explicit conflict review. Old separately installed specialist directories are not
automatically removed or overwritten; preserve personal edits before any cleanup.

## Layout and use

`<host-skill-root>/threejs-skills/SKILL.md` is the only native entrypoint.
`skills/<method-id>/GUIDE.md` contains each original method, with references,
scripts, examples, assets and license notices beside it. The original SKILL.md
content is preserved as GUIDE.md with integration boundaries. Nothing requires
45 separately installed skill directories or commands. All resources ship together.
See [SKILL.md](SKILL.md) and [the method index](references/specialists.md).

Say "use andino-workflow and threejs-skills" for selection from the prompt, or
"use threejs-skills, specifically threejs-shaders" to name one method. Invoke the
family through the host's native mechanism and load only the relevant authorized
guides. Do not claim that internal methods are separately registered native skills.
Andino retains its single plan, checkpoints, handoff and completion. Standalone
family use follows the existing host context, with no new general lifecycle.

Codex uses .agents/skills; Claude Code .claude/skills. Other hosts use the existing
AI-RULES catalog adapters. Refresh session discovery after installation. Installer
path support does not establish live cross-host behavior. Never bypass restrictions
with alternate source reads. Missing/denied methods require honest fallback.

## Verification, dependencies and provenance

Validate paths, metadata, relative references, binary signatures and the original
inventory in main. Verify actual host family discovery and selective guide use
separately; structural checks do not prove rendering or API compatibility. Browser,
interaction and performance claims require observed runtime evidence. Andino UI
acceptance retains 360/768/1440 px screenshots when applicable.

Inspect actual Three.js/WebGL/WebGPU/TSL and NixieFX versions before using examples.
Optional generators use Tripo, Gemini or ElevenLabs and user-provided credentials.
Installation calls none of those services and installs no npm dependencies. Paid
calls, delegation and publication require applicable task authorization.

The maintainer attests original collection authorship. Embedded MIT, CC0 and GPL
notices/full texts remain intact; no collection-wide license is invented. This is
not independent verification of every resource origin. See main's provenance record.

[Inventory and evidence](https://github.com/andinoferdi/AI-RULES/tree/main/docs/threejs)
'''
    (destination / 'README.md').write_text(readme, encoding='utf-8')
    (destination / 'references').mkdir()
    index = '# Internal specialist methods\n\nRead only the guide matching the current need; descriptions are selection metadata.\n\n'
    for row in inventory['skills']:
        index += f"- [{row['name']}](../skills/{row['name']}/GUIDE.md): {row['description']}\n"
    (destination / 'references/specialists.md').write_text(index, encoding='utf-8')
    for row in inventory['skills']:
        target = destination / 'skills' / row['name']
        skill = target / 'SKILL.md'
        body = skill.read_text(encoding='utf-8')
        for sibling, folder in sorted(set(re.findall(r'\.\./([^/]+)/examples/([^/]+)/', body))):
            shutil.copytree(source / sibling / 'examples' / folder,
                            target / 'examples' / ('shared-' + folder), dirs_exist_ok=True)
            body = body.replace(f'../{sibling}/examples/{folder}/', f'examples/shared-{folder}/')
        if 'threejs-game-director/scripts/probe_asset_credentials.sh' in body:
            (target / 'scripts').mkdir(exist_ok=True)
            shutil.copyfile(source / 'threejs-game-director/scripts/probe_asset_credentials.sh',
                            target / 'scripts/probe_asset_credentials.sh')
            body = body.replace('threejs-game-director/scripts/probe_asset_credentials.sh',
                                '<this-skill-dir>/scripts/probe_asset_credentials.sh')
        skill.write_text(body, encoding='utf-8')
        path = target / 'references/evidence-manifest.md'
        if path.exists():
            path.write_text(path.read_text(encoding='utf-8').replace(
                '`[motion](<artifacts/pass-1/hero motion.webm>)`',
                'a link label followed by an angle-bracketed project artifact path such as `artifacts/pass-1/hero motion.webm`'), encoding='utf-8')
    for path in destination.rglob('*'):
        if not path.is_file() or path.name == '.git' or path.suffix.lower() in {'.png', '.jpg', '.webp', '.bin', '.exr', '.glb', '.wasm', '.gz'}:
            continue
        text = path.read_text(encoding='utf-8')
        if path.name == 'README.md':
            text = text.replace('--scope project --source', '--scope project --project-root . --source')
            text = text.replace('Use the project root as the working directory; `--project-root PATH` selects another.',
                                'Pass `--project-root PATH` for project scope; it is required by the CLI.')
            text = text.replace('Run in the target project or pass `--project-root PATH`.',
                                'Pass the required `--project-root PATH` for project scope.')
        lines = [line.rstrip(' \t') if not line.strip() or line.lstrip().startswith('//') else line
                 for line in text.splitlines()]
        cleaned = '\n'.join(lines).rstrip('\n') + ('\n' if text.endswith('\n') else '')
        if cleaned != path.read_text(encoding='utf-8'):
            path.write_text(cleaned, encoding='utf-8')
    for row in inventory['skills']:
        target = destination / 'skills' / row['name']
        (target / 'SKILL.md').rename(target / 'GUIDE.md')
        for entry in row['files']:
            if entry['path'] == 'SKILL.md':
                entry['runtime_path'] = 'GUIDE.md'
    inventory['distribution'] = 'One root family skill; 45 internal GUIDE.md methods'
    inventory['runtime_hash_normalization'] = 'Text CRLF normalized to LF; binary resources byte-exact'
    for row in inventory['skills']:
        target = destination / 'skills' / row['name']
        for entry in row['files']:
            data = (target / entry.get('runtime_path', entry['path'])).read_bytes()
            entry['runtime_sha256'] = digest(data if entry['kind'] == 'binary' else data.replace(b'\r\n', b'\n'))
        originals = {entry.get('runtime_path', entry['path']) for entry in row['files']}
        row['added_files'] = [{'path': path.relative_to(target).as_posix(),
                               'sha256': digest(path.read_bytes().replace(b'\r\n', b'\n'))}
                              for path in sorted(target.rglob('*')) if path.is_file()
                              and path.relative_to(target).as_posix() not in originals]
    inventory_path.parent.mkdir(parents=True, exist_ok=True)
    inventory_path.write_text(json.dumps(inventory, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(candidates)} packages; source unchanged; inventory {inventory_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--inventory', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.source, args.destination, args.inventory)
