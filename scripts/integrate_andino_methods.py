"""Render reviewed internal method metadata; manual maintainer action, never runtime sync."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'docs/validation/andino-unified'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', required=True, type=Path)
    args = parser.parse_args()
    method_sources = {m['id']: p.name.replace('-methods.json', '-operational.json')
                      for p in sorted(AUDIT.glob('*-methods.json'))
                      for m in json.loads(p.read_text(encoding='utf-8'))}
    methods = [m for p in sorted(AUDIT.glob('*-methods.json'))
               for m in json.loads(p.read_text(encoding='utf-8'))]
    by_id = {m['id']: m for m in methods}
    coverage = json.loads((AUDIT/'coverage.json').read_text(encoding='utf-8'))
    expected = {m['id'] for r in coverage['rows'] for m in r['andino_method_ids_and_paths']} - {'root-contract'}
    if set(by_id) != expected or len(methods) != len(by_id):
        raise ValueError('Method inventory differs from reviewed source mappings')
    for mid in expected:
        if not (args.runtime/f'skills/{mid}/GUIDE.md').is_file():
            raise ValueError(f'Missing implemented method: {mid}')
    index = [
        '# Internal method index', '',
        'These are bundled Andino resources, not native skills or a second router. '
        'Select by actual intent, current evidence and the present phase. A name in quoted text, '
        'a filename or this inventory is not a trigger. Ordinary sufficient tasks need no method.', '',
        'An explicit relevant internal method ID is enough: read its linked GUIDE.md through '
        'the permitted resource tool, then only the local resources it needs. For implicit selection '
        'use the trigger and exclusion together; choose the minimum useful set. Do not load all guides. '
        'If the requested outcome is prohibited or excluded, resolve that boundary in the root contract '
        'without loading methods just to refuse. No guide grants additional action authority.', '',
        'DISCOVERED is metadata; AVAILABLE requires the guide/resources; INVOKABLE also requires '
        'current permissions; ACTIVE requires the actual guide read; USED also requires a relevant '
        'action/result. Missing or denied resources are UNAVAILABLE; irrelevant methods are NOT_NEEDED. '
        'A denied resource cannot be loaded from another copy. Do not claim native upstream invocation.', '',
        'Focus owns communication, Search First owns required solution/external research; domain siblings '
        'and the accepted UI policy retain their boundaries. Andino alone owns routing, one plan, '
        'delegation and acceptance. Conditional beta/misc methods state their limits in their guide.', '',
        '| Method | Select for | Exclude |', '| --- | --- | --- |',
    ]
    for mid, method in sorted(by_id.items()):
        clean = lambda value: str(value).replace('|', '/').replace('\n', ' ')
        index.append(f"| [{mid}](../skills/{mid}/GUIDE.md) | {clean(method['trigger'])} | {clean(method['non_trigger'])} |")
    aliases = {}
    for row in coverage['rows']:
        if row['source_status'] != 'deprecated' and row['original_skill_name'] not in {
                'ask-matt', 'using-agent-skills', 'using-superpowers'}:
            aliases.setdefault(row['original_skill_name'], set()).update(
                m['id'] for m in row['andino_method_ids_and_paths'] if m['id'] != 'root-contract')
    aliases['agent-skills-test-driven-development'] = {'tdd'}
    index += ['', '## Source-name compatibility', '',
              'Original names below are internal aliases/provenance, not installation requirements. '
              'For a multi-method alias load only the distinct techniques needed now. '
              'Bootstrap names have no callable alias: Andino already supplies discovery.', '',
              '| Original name | Internal destination |', '| --- | --- |']
    for alias, mids in sorted(aliases.items()):
        if mids and (len(mids) != 1 or alias not in mids):
            index.append(f"| {alias} | " + ', '.join(f'[{m}](../skills/{m}/GUIDE.md)' for m in sorted(mids)) + ' |')
    index += ['', 'See [provenance and notices](legal/provenance.md). Updates require manual source '
              'review and regressions on main; no upstream checkout, plugin, hook or runtime fetch is needed.', '']
    (args.runtime/'references/internal-method-index.md').write_text('\n'.join(index), encoding='utf-8')

    registry_path = args.runtime/'references/capability-registry.md'
    registry = registry_path.read_text(encoding='utf-8')
    blocks = re.split(r'(?=^## [a-z0-9-]+\n)', registry, flags=re.M)
    for i, block in enumerate(blocks):
        match = re.match(r'## ([a-z0-9-]+)\n', block)
        if not match or match[1] not in aliases or not aliases[match[1]]:
            continue
        alias = match[1]
        mid = sorted(aliases[alias])[0]
        if not re.search(r'^- Family/provider: (?:Superpowers|Agent Skills|Andino internal)', block, re.M):
            continue
        fields = {
            'Type': 'method', 'Family/provider': 'Andino internal; adapted source provenance in package legal records',
            'Aliases': f'{alias} resolves to canonical {mid}; no upstream native registration required',
            'Availability check': f'Check local skills/{mid}/GUIDE.md and selected resources plus actual resource permissions.',
            'Invocation method': f'Read [{mid}](../skills/{mid}/GUIDE.md) through a permitted resource tool; this is an internal method, not native upstream skill invocation.',
            'First-call/preflight': 'Read accepted task/project evidence and only the selected guide; retain one Andino plan.',
            'Fallback': 'Missing or denied guide is UNAVAILABLE; use sufficient permitted native reasoning without claiming method use or reading an alternate denied copy.',
            'Coexistence/conflicts': 'Use the single canonical guide and current sibling contracts; do not load competing upstream providers or start another lifecycle.',
            'Verification requirement': 'Actual local guide read plus meaningful observed task action for USED; metadata/example similarity alone is not live routing proof.',
        }
        for key, value in fields.items():
            block = re.sub(r'^- '+re.escape(key)+r': .*$', lambda _: '- '+key+': '+value, block, flags=re.M)
        block = re.sub(r'^- Internal method: .*\n?', '', block, flags=re.M)
        block = block.rstrip() + f'\n- Internal method: skills/{mid}/GUIDE.md\n\n'
        blocks[i] = block
        registry = re.sub(r'(\| \['+re.escape(alias)+r'\]\(#'+re.escape(alias)+r'\) \|) skill \| [^|]+ \|',
                          r'\1 method | Andino internal |', registry)
    # Preserve the native/instrument registry while replacing only reviewed upstream methods.
    body = ''.join(blocks)
    for alias in aliases:
        if aliases[alias]:
            body = re.sub(r'(\| \['+re.escape(alias)+r'\]\(#'+re.escape(alias)+r'\) \|) skill \| (?:Superpowers|Agent Skills) \|',
                          r'\1 method | Andino internal |', body)
    body = body.replace('Provider identities below are intended families; actual host provenance must be resolved.',
                        'Bundled method aliases resolve to the [canonical index](internal-method-index.md); native sibling/tool provenance is resolved through the host.')
    registry_path.write_text(body, encoding='utf-8')

    assets = []
    for row in coverage['rows']:
        mids = [m['id'] for m in row['andino_method_ids_and_paths']]
        row['purpose_and_trigger'] = [dict(id=m, purpose=by_id[m]['purpose'], trigger=by_id[m]['trigger'])
                                      for m in mids if m in by_id] or ['Root discovery/permission contract; archived sources remain inactive.']
        row['test_ids'] = [f'unified-{m}-{pillar}' for m in mids if m != 'root-contract'
                           for pillar in ('positive', 'negative')]
        row['verification_evidence'] = [
            dict(method=m, selection_fixtures='evals/andino-unified.json',
                 observed_selection='docs/validation/andino-unified/behavior-grade.json',
                 procedure='docs/validation/andino-unified/' + method_sources[m],
                 procedure_record_id=m)
            for m in mids if m != 'root-contract']
        row['verification_state'] = 'MAPPED; BOUNDED PROCEDURE VERIFIED; LIVE ROUTING SEPARATE' if mids else 'EXCLUDED'
        for asset in row['essential_assets']:
            found = [dict(x, source_path=asset, upstream=row['upstream'], method_id=m)
                     for m in mids for x in by_id.get(m, {}).get('resource_dispositions', [])
                     if x['source_path'].split(':', 1)[-1] == asset]
            if not found and mids == ['root-contract']:
                excluded = asset.endswith('session-start.sh') or any(f'/{host}-tools.md' in asset for host in ('hermes', 'muse', 'pi'))
                found = [dict(source_path=asset, upstream=row['upstream'], method_id='root-contract',
                              disposition='EXCLUDE' if excluded else 'INTERNALIZE',
                              runtime_path='SKILL.md' if asset.endswith('.sh') else 'references/invocation-adapter.md',
                              rationale='Startup router hook excluded; no automatic injection.' if asset.endswith('.sh') else
                              'Off-target host-specific tool names excluded; generic actual-host discovery retained.' if excluded else
                              'Discovery, native permission and state distinctions belong to the single Andino root/host contract; fixed upstream tool aliases are not authoritative.')]
            if not found:
                raise ValueError(f"Unresolved asset: {row['source_id']}:{asset}")
            assets.extend(found)
    (AUDIT/'coverage.json').write_text(json.dumps(coverage, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    (AUDIT/'resource-map.json').write_text(json.dumps({'schema_version': 1, 'resources': assets}, indent=2)+'\n', encoding='utf-8')
    print(f'Rendered {len(by_id)} internal guides; {len(assets)} source-resource mappings; native siblings/instruments preserved.')


if __name__ == '__main__':
    main()
