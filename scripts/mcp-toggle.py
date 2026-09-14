"""Toggle an existing local MCP configuration without printing credentials."""
from pathlib import Path
import argparse, datetime, json, re, shutil, tomllib

FILES = {'codex': '.codex/config.toml', 'claude': '.claude.json',
         'opencode': '.config/opencode/opencode.json',
         'antigravity': '.gemini/config/mcp_config.json',
         'antigravity-legacy': '.gemini/antigravity/mcp_config.json'}

def toggle(home, host, name=None, enabled=None):
    path = home / FILES[host]
    original = path.read_text(encoding='utf-8-sig')
    data = tomllib.loads(original) if host == 'codex' else json.loads(original)
    key = 'mcp_servers' if host == 'codex' else 'mcp' if host == 'opencode' else 'mcpServers'
    servers = data.get(key, {})
    library_path = home / '.andino/mcp/claude-manual.json'
    library = json.loads(library_path.read_text()).get('mcpServers', {}) if host == 'claude' and library_path.exists() else {}
    if name is None:
        for item in sorted(set(servers) | set(library)):
            config = servers.get(item)
            active = config is not None and config.get('enabled', True) and not config.get('disabled', False)
            print(f'{host} {item}: {"on" if active else "off"}')
        return
    if name not in servers and name not in library:
        raise ValueError('Unknown server name; use --list')
    if host == 'codex':
        # Match only the parent server table, leaving env/header subtables intact.
        pattern = r'^\[mcp_servers\.(?:' + re.escape(name) + r'|"' + re.escape(name) + r'")\]\n.*?(?=^\[|\Z)'
        matches = list(re.finditer(pattern, original, re.M | re.S))
        if len(matches) != 1:
            raise ValueError('Unsupported TOML table layout; no change made')
        match = matches[0]; block = match.group(0)
        line = f'enabled = {str(enabled).lower()}'
        if re.search(r'^enabled\s*=', block, re.M):
            block = re.sub(r'^enabled\s*=.*$', line, block, flags=re.M)
        else:
            block = block.replace('\n', '\n' + line + '\n', 1)
        updated = original[:match.start()] + block + original[match.end():]
        tomllib.loads(updated)
    else:
        if host == 'claude':
            if enabled:
                servers.setdefault(name, library[name] if name in library else servers[name])
            elif name in servers:
                library[name] = servers.pop(name)
                save(home, library_path, json.dumps({'mcpServers': library}, indent=2) + '\n')
        elif host == 'opencode':
            if 'servers' in servers:
                raise ValueError('V2 config detected; this adapter targets verified V1')
            servers[name]['enabled'] = enabled
        else:
            servers[name]['disabled'] = not enabled
        data[key] = servers
        updated = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
    save(home, path, updated)
    print(f'{host} {name}: {"on" if enabled else "off"}; reload host to apply')

def save(home, path, content):
    if not path.resolve().is_relative_to(home.resolve()):
        raise ValueError('Configuration outside selected home')
    if path.exists() and path.read_text(encoding='utf-8-sig') == content:
        return
    if path.exists():
        stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        backup = home / '.andino/backups/mcp-toggle' / stamp / path.relative_to(home)
        backup.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(path, backup)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.andino-tmp')
    temp.write_text(content, encoding='utf-8'); temp.replace(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('host', choices=FILES)
    parser.add_argument('name', nargs='?')
    parser.add_argument('state', nargs='?', choices=['on', 'off'])
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--home', type=Path, default=Path.home())
    args = parser.parse_args()
    if not args.list and (args.name is None or args.state is None):
        parser.error('Supply name and on|off, or --list')
    toggle(args.home.resolve(), args.host, None if args.list else args.name, args.state == 'on')
