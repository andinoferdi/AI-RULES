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
Use the host's permitted discovery/invocation mechanism for selected siblings;
an absent sibling is optional guidance, not an implicit installation dependency.
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
description: Discover the AI-RULES Three.js and NixieFX specialist collection for actual 3D scene, rendering, animation, game or particle-effect needs. Excludes ordinary frontend work and general task orchestration.
---

# Three.js Skills

This is a family index and boundary statement. Select individual installed skills
through the current host catalog and permitted invocation mechanism. Do not load
the collection as a batch. For an ambiguous multi-system graphics request,
`threejs-skill-router` can recommend the smallest domain set; the family index
does not dispatch or repeat its technical selection table. Game production uses
`threejs-game-director` only when game-wide coordination is actually needed.

Andino Workflow, when active, retains lifecycle, routing, one plan/checkpoint,
handoff and completion. Focus controls communication. Search First handles
evidenced research needs. Specialists supply methods, results and evidence.
They also work independently in normal host context. Honor invocation permissions
and distinguish DISCOVERED, AVAILABLE, INVOKABLE, ACTIVE, USED, UNAVAILABLE and
NOT_NEEDED. Missing or denied skills require an honest native fallback, never a
claim of activation. Reassess selection when requirements change or work resumes.

Read the [package guide](README.md) for installation, discovery and limits.
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

## Use and boundaries

Read [SKILL.md](SKILL.md) for domain triggers, methods, evidence and exclusions.
This specialist can work alone. With Andino active, return results to its single
plan; Focus controls communication and Search First handles relevant research.
Sibling suggestions are optional, selected by need and host invocation permission.

## Installation and discovery

After the runtime and installer are published:

```sh
ai-rules setup --host codex --capability {name} --scope project --source latest
ai-rules setup --host codex --profile threejs --scope project --source latest
```

Use the project root as the working directory; `--project-root PATH` selects another.
Global scope uses `--scope global`. Codex project/global roots are `.agents/skills`;
Claude Code uses `.claude/skills`; OpenCode uses `.agents/skills` for projects and
`~/.config/opencode/skills` globally. Antigravity CLI and IDE use the catalog's
separate roots. These are installer mappings; live execution on each host is
NOT_VERIFIED. Refresh/restart discovery as required by the host. Invoke this exact
name through its permitted mechanism; installation does not prove activation.

## Package and dependencies

Install the whole directory with SKILL.md directly at its root. Preserve all
included references, scripts, examples, agent metadata, assets and license notices.
The skill body describes version-sensitive tools, render backends and optional
services. Installing this package installs no npm dependencies or credentials and
does not authorize paid API calls. No blanket license is inferred from local files.

## Update, conflicts and verification

Use `ai-rules update` with the same host, scope, capability and source selection.
Review modified or unrecognized directories before explicit repair; preserve user
edits and backups. Bundled releases pin commit and subpath; latest resolves the
branch at setup. Do not install a second discoverable copy as a workaround.
Run the main package validator, then an applicable domain behavior check. Positive
smoke: invoke this skill for its stated domain, observe a relevant action and
evidence. Negative smoke: ordinary unrelated frontend work must not select it;
missing/denied siblings require a truthful fallback. File presence alone proves
neither invocation nor rendering quality.

[Family quality contract](https://github.com/andinoferdi/AI-RULES/blob/main/docs/agent-skill-family-standard.md)
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
    entrypoint = destination / 'entrypoint'
    entrypoint.mkdir()
    (entrypoint / 'SKILL.md').write_text(FAMILY, encoding='utf-8')
    readme = '''# Three.js Skills for AI-RULES

A domain collection of 45 standalone Three.js and NixieFX specialists. This family
does not own a task lifecycle, general router, plan or DONE decision. Andino owns
those when active; Focus controls communication and Search First relevant research.
Use for real scene/rendering/game/particle needs; ordinary frontend work is excluded.

## Packages

The branch root is the family reading entrypoint. `entrypoint/` is its standalone
installable projection (identical SKILL.md and README.md); `skills/<name>/` holds
each original skill and all supporting files. The installer selects subpaths so
the family installation does not contain nested discoverable copies of specialists.
The installed shape is `<host-skill-root>/<name>/SKILL.md`, with support files
beside it. No installer source, tests or main quality artifacts ship on this branch.

## Install, update and discovery

After publication, use these existing CLI selections:

```sh
ai-rules setup --host codex --profile threejs --scope project --source latest
ai-rules setup --host codex --capability threejs-shaders --scope project --source latest
ai-rules setup --host codex --profile threejs --scope global --source bundled
ai-rules update --host codex --profile threejs --scope project --source latest
```

Run in the target project or pass `--project-root PATH`. The profile includes all
45 members, this index, Andino, Focus and Search First. Individual specialists do
not require the lifecycle skills. Minimal and Engineering keep their existing sets.
Everything includes all first-party members when newly selected; existing locks
retain explicit targets unless the caller selects that expanded profile again.

Host mappings: Codex `.agents/skills` (project/global); Claude Code `.claude/skills`;
OpenCode `.agents/skills` project, `~/.config/opencode/skills` global; Antigravity CLI
`.agents/skills` project and `~/.gemini/antigravity-cli/skills` global; Antigravity IDE
`.agents/skills` project and `~/.gemini/config/skills` global. Installer mappings
are structural support, not live-host execution proof. All live Three.js host use
is NOT_VERIFIED until observed. Refresh discovery in the host's normal manner;
invoke exact installed names through permitted host controls. Never bypass a deny
or explicit-only setting with file reads. Avoid duplicate discoverable installations.

Latest uses one fetch per repository, identifies packages by branch/subpath, and
preserves edited/unrecognized targets. Bundled uses the release-pinned commit and
same subpath. Updates use existing staging, backup, verification and rollback.
Review conflicts before explicit repair; never overwrite personal edits blindly.

## Domain selection and evidence

Select only current needs: shaders, lighting, animation, materials, geometry and
interaction have their namesake specialists. Complex graphics may use the domain
advisor `threejs-skill-router`; game-wide production may use `threejs-game-director`.
Neither starts a second plan nor activates all siblings. Distinguish DISCOVERED,
AVAILABLE, INVOKABLE, ACTIVE, USED, UNAVAILABLE and NOT_NEEDED. Reassess after
requirements change and after resume; missing/denied skills use honest fallbacks.

Main's package validator checks metadata, regular files, safe paths, relative links
and binary signatures. Behavioral smoke: request one shader change, activate only
the relevant permitted specialist, apply its method and record output. Negative
smoke: unrelated frontend work selects none; an unavailable or denied specialist
must not be reported as used. Rendering/performance/interaction claims need actual
browser evidence. For UI acceptance under Andino inspect 360/768/1440 px captures.
Unit and structural tests are not live model-routing proof.

## Dependencies, provenance and limits

Examples span different Three.js/WebGL/WebGPU/TSL versions. Inspect project versions
and official documentation before use. NixieFX requires its actual public runtime
and selected renderer peer. Generator scripts use optional external Tripo, Gemini
and ElevenLabs services and user-provided credentials; installation makes no calls,
incurs no charges and installs no npm packages. Paid calls need task authorization.

The maintainer reports that this collection is their own work (statement recorded
2026-10-16); no external collection repository was supplied. This is maintainer
attestation, not independent verification of every embedded resource. Preserve the
included MIT, CC0 and GPL notices and full GPL texts for identified third-party
materials. No new collection-wide license has been specified by this integration.
See the main provenance record for the attestation and resource-level limits.
These local commits have not been authorized for remote publication.

[Main quality contract](https://github.com/andinoferdi/AI-RULES/blob/main/docs/agent-skill-family-standard.md)
[Inventory and release evidence](https://github.com/andinoferdi/AI-RULES/tree/main/docs/threejs)
'''
    (destination / 'README.md').write_text(readme, encoding='utf-8')
    (entrypoint / 'README.md').write_text(readme, encoding='utf-8')
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
    inventory['runtime_hash_normalization'] = 'Text CRLF normalized to LF; binary resources byte-exact'
    for row in inventory['skills']:
        target = destination / 'skills' / row['name']
        for entry in row['files']:
            data = (target / entry['path']).read_bytes()
            entry['runtime_sha256'] = digest(data if entry['kind'] == 'binary' else data.replace(b'\r\n', b'\n'))
        originals = {entry['path'] for entry in row['files']}
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
