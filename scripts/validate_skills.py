"""Validate branch-distributed skill packages and available review-only eval cases."""

import argparse
import json
import re
import subprocess
import sys
import gzip
from pathlib import Path, PurePosixPath
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SKILLS = ("andino-workflow", "ai-codebase-rescue", "skripsi-skill", "focus", "search-first", "council", "natural-writing")
EVAL_SKILLS = RUNTIME_SKILLS
LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):[ \t]+(.+)$")
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
THREEJS_SKILLS = frozenset({'threejs-skills'} | {item['name'] for item in json.loads(
    (ROOT / 'docs/threejs/inventory.json').read_text(encoding='utf-8'))['skills']})
BINARY_SUFFIXES = {'.png', '.jpg', '.webp', '.bin', '.exr', '.glb', '.wasm', '.gz'}
THREEJS_SUFFIXES = BINARY_SUFFIXES | {'.md', '.ts', '.js', '.mjs', '.py', '.sh', '.json',
    '.yaml', '.txt', '.glsl', '.wgsl', '.frag', '.vert', '.html', '.css'}


def binary_error(name, data):
    suffix = PurePosixPath(name).suffix.lower()
    signatures = {'.png': b'\x89PNG\r\n\x1a\n', '.jpg': b'\xff\xd8\xff',
                  '.exr': b'\x76\x2f\x31\x01', '.wasm': b'\x00asm\x01\x00\x00\x00',
                  '.glb': b'glTF\x02\x00\x00\x00', '.gz': b'\x1f\x8b'}
    if not data:
        return 'empty binary resource'
    if suffix in signatures and not data.startswith(signatures[suffix]):
        return 'invalid binary signature'
    if suffix == '.glb' and (len(data) < 12 or int.from_bytes(data[8:12], 'little') != len(data)):
        return 'invalid GLB length'
    if suffix == '.webp' and (data[:4] != b'RIFF' or data[8:12] != b'WEBP'):
        return 'invalid WebP signature'
    if suffix == '.gz':
        try:
            gzip.decompress(data)
        except (OSError, EOFError):
            return 'invalid gzip data'
    return None


def git(*args):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise ValueError(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout


def package_files(files, expected_name, modes=None):
    errors = []
    threejs = expected_name in THREEJS_SKILLS
    files = dict(files)
    if expected_name == 'threejs-skills':
        for member in sorted(THREEJS_SKILLS - {'threejs-skills'}):
            prefix = f'skills/{member}/'
            child = {p[len(prefix):]: value for p, value in files.items() if p.startswith(prefix)}
            child_modes = {p[len(prefix):]: value for p, value in (modes or {}).items() if p.startswith(prefix)}
            guide = child.pop('GUIDE.md', None)
            if guide is None:
                errors.append(f'{member}: missing internal GUIDE.md')
            else:
                child['SKILL.md'] = guide
                child_modes['SKILL.md'] = child_modes.pop('GUIDE.md', '100644')
                # Validate member metadata and support paths with its local guide identity.
                child = {p: v.replace('](GUIDE.md)', '](SKILL.md)') if isinstance(v, str) else v for p, v in child.items()}
                errors.extend(package_files(child, member, child_modes))
        if any(p != 'SKILL.md' and p.endswith('/SKILL.md') for p in files):
            errors.append('threejs-skills: nested native SKILL.md is forbidden')
    for name, content in files.items():
        if PurePosixPath(name).suffix.lower() in BINARY_SUFFIXES:
            if not isinstance(content, bytes):
                errors.append(f'{expected_name}:{name}: binary resource must be bytes')
            elif problem := binary_error(name, content):
                errors.append(f'{expected_name}:{name}: {problem}')
        elif isinstance(content, bytes):
            try:
                files[name] = content.decode('utf-8').replace('\r\n', '\n')
            except UnicodeDecodeError:
                errors.append(f'{expected_name}:{name}: invalid UTF-8 text')
                files[name] = ''
    if "README.md" not in files:
        errors.append(f"{expected_name}: missing README.md")
    if expected_name == 'andino-workflow':
        folded = [name.casefold() for name in files]
        if len(folded) != len(set(folded)):
            errors.append('andino-workflow: case-insensitive runtime path collision')
    for name in files:
        portable_path = "\\" not in name and all(
            part and not part.startswith(".") for part in name.split("/")
        )
        allowed = portable_path and (name in ("README.md", "SKILL.md") or (
            name.startswith("references/") and name.endswith(".md")
        ) or (
            expected_name == "skripsi-skill"
            and name.startswith("assets/") and name.endswith(".md")
        ))
        if expected_name == 'andino-workflow':
            parts = name.split('/')
            safe = '\\' not in name and ':' not in name and all(
                part and not part.startswith('.') and not part.endswith((' ', '.'))
                and not any(ord(char) < 32 or char in '<>"|?*' for char in part)
                and not re.match(r'^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)', part, re.I)
                for part in parts)
            method_resource = (len(parts) >= 3 and parts[0] == 'skills'
                               and NAME.fullmatch(parts[1]) and len(parts[1]) <= 64
                               and (parts[2:] in (['GUIDE.md'], ['SKILL.md']) or
                                    len(parts) >= 4 and parts[2] in {'references', 'resources', 'templates', 'examples'}
                                    and name.endswith('.md')))
            allowed = safe and (allowed or bool(method_resource))
            if parts[0] == 'references' and (parts[-1].casefold() == 'skill.md' or (len(parts) > 2 and parts[1] != 'legal')):
                allowed = False
            if safe and len(parts) == 3 and parts[0] == 'skills' and parts[2] == 'SKILL.md':
                member_name = f'andino-{parts[1]}'
                body = files[name]
                if not body.startswith('---\n'):
                    errors.append(f'{member_name}: missing YAML frontmatter')
                else:
                    m_parts = body.split('\n---\n', 1)
                    if len(m_parts) != 2:
                        errors.append(f'{member_name}: unterminated YAML frontmatter')
                    else:
                        fields = {}
                        for line in m_parts[0].splitlines()[1:]:
                            match = FIELD.fullmatch(line)
                            if not match or match[1] in fields:
                                errors.append(f'{member_name}: invalid or duplicate frontmatter field: {line}')
                                continue
                            value = match[2].strip()
                            if (value.startswith(("[", "{", "'", '"', "|", ">", "&", "*", "!", "#"))
                                    or ": " in value or "\t" in value or " #" in value
                                    or value.lower() in ("null", "~", "true", "false", "yes", "no", "on", "off")
                                    or re.fullmatch(r"[+-]?(?:[0-9][0-9._eE+-]*|\.(?:inf|nan))", value, re.I)):
                                errors.append(f'{member_name}: unsupported frontmatter scalar: {line}')
                                continue
                            fields[match[1]] = value
                        if fields.get('name') != member_name:
                            errors.append(f'{member_name}: wrong or missing name: {fields.get("name")}')
                        if not fields.get('description'):
                            errors.append(f'{member_name}: missing description')
                        elif len(fields['description']) > 1024:
                            errors.append(f'{member_name}: description exceeds 1024 characters')
        if threejs:
            scaffold_ignore = name == 'assets/threejs-vite-game/.gitignore'
            safe = '\\' not in name and ':' not in name and all(
                part and not part.startswith('.') and not part.endswith((' ', '.'))
                and not re.match(r'^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)', part, re.I)
                for part in name.split('/'))
            allowed = allowed or scaffold_ignore or (safe and (
                name == 'agents/openai.yaml' or
                (name.startswith(('references/', 'assets/', 'scripts/', 'examples/'))
                 and PurePosixPath(name).suffix.lower() in THREEJS_SUFFIXES)))
        if expected_name == 'threejs-skills' and name.startswith('skills/'):
            parts = name.split('/')
            # Member validators above enforce path, extension and resource safety.
            allowed = len(parts) > 2 and parts[1] in THREEJS_SKILLS - {'threejs-skills'}
        if not allowed:
            errors.append(f"{expected_name}: unexpected runtime file: {name}")
        if modes and modes.get(name, "100644") not in ("100644", "100755"):
            errors.append(f"{expected_name}: non-regular runtime file: {name}")
    if "SKILL.md" not in files:
        return errors + [f"{expected_name}: missing SKILL.md"]
    body = files["SKILL.md"]
    if not body.startswith("---\n"):
        errors.append(f"{expected_name}: missing YAML frontmatter")
    else:
        parts = body.split("\n---\n", 1)
        if len(parts) != 2:
            errors.append(f"{expected_name}: unterminated YAML frontmatter")
        else:
            fields = {}
            for line in parts[0].splitlines()[1:]:
                match = FIELD.fullmatch(line)
                if not match or match[1] in fields:
                    errors.append(f"{expected_name}: invalid or duplicate frontmatter field: {line}")
                    continue
                # Runtime packages use plain scalar YAML only. Reject syntax this
                # dependency-free parser cannot validate instead of accepting it.
                value = match[2].strip()
                if (value.startswith(("[", "{", "'", '"', "|", ">", "&", "*", "!", "#"))
                        or ": " in value or "\t" in value or " #" in value
                        or value.lower() in ("null", "~", "true", "false", "yes", "no", "on", "off")
                        or re.fullmatch(r"[+-]?(?:[0-9][0-9._eE+-]*|\.(?:inf|nan))", value, re.I)):
                    errors.append(f"{expected_name}: unsupported frontmatter scalar: {line}")
                    continue
                fields[match[1]] = value
            if fields.get("name") != expected_name:
                errors.append(f"{expected_name}: wrong or missing name")
            name = fields.get("name", "")
            if not 1 <= len(name) <= 64 or not NAME.fullmatch(name):
                errors.append(f"{expected_name}: invalid portable name (1-64 lowercase alphanumeric/hyphens)")
            if not fields.get("description"):
                errors.append(f"{expected_name}: missing description")
            elif len(fields["description"]) > 1024:
                errors.append(f"{expected_name}: description exceeds 1024 characters")
    for name, content in files.items():
        if not name.endswith(".md"):
            continue
        links = re.findall(r'!?\[[^]]*\]\(([^)]+)\)', content) if threejs or expected_name == 'andino-workflow' else LINK.findall(content)
        for raw in links:
            target = unquote(raw.split("#", 1)[0].strip().split(" ", 1)[0])
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            if target.startswith('/') or '\\' in target:
                errors.append(f'{expected_name}:{name}: unsafe link: {raw}')
                continue
            resolved = PurePosixPath(name).parent.joinpath(target)
            parts = []
            for part in resolved.parts:
                if part == "..":
                    if parts:
                        parts.pop()
                    else:
                        errors.append(f"{expected_name}:{name}: link escapes package: {raw}")
                        break
                elif part != ".":
                    parts.append(part)
            else:
                if "/".join(parts) not in files:
                    errors.append(f"{expected_name}:{name}: broken link: {raw}")
    return errors


def focus_reference_drift(files, source):
    normalize = lambda text: text.replace("\r\n", "\n")
    try:
        chat = normalize(source["put-in-your-projects/chat-rules.md"])
        priority = chat[chat.index("A. PRIORITAS\n"):]
        readme = normalize(source["README.md"])
        section = readme.split("## A. PRIORITAS\n", 1)[1]
        fenced = section.split("````text\n", 1)[1]
        readme_priority, closing, _ = fenced.partition("````")
        if not closing:
            raise ValueError("unterminated README A fence")
        # Ignore the presentation blank lines around README's fenced text only.
        if priority.strip("\n") != readme_priority.strip("\n"):
            return ["focus: WebBased A. PRIORITAS sources disagree; review canonical source before syncing"]
        expected = {"references/priority-a.md": priority}
        for name in ("human-language-indonesia.md", "human-language-english.md"):
            expected[f"references/{name}"] = normalize(source[f"put-in-your-projects/{name}"])
    except (KeyError, ValueError, IndexError) as exc:
        return [f"focus: missing or malformed WebBased communication source: {exc}"]
    return [f"focus: missing or drifted bundled reference: {name}"
            for name, text in expected.items()
            if name not in files or normalize(files[name]) != text]


def directory_files(root):
    files, modes = {}, {}
    if not root.is_dir():
        raise ValueError(f"missing package directory: {root}")
    def visit(directory):
        for path in directory.iterdir():
            if path == root / ".git":
                continue
            name = path.relative_to(root).as_posix()
            if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
                files[name], modes[name] = "", "120000"
            elif path.is_dir():
                visit(path)
            elif path.is_file():
                data = path.read_bytes()
                try:
                    content = data if path.suffix.lower() in BINARY_SUFFIXES else data.decode('utf-8').replace('\r\n', '\n')
                except UnicodeDecodeError:
                    content = data
                files[name], modes[name] = content, "100644"
            else:
                files[name], modes[name] = "", "unsupported"
    visit(root)
    return files, modes


def ref_files(ref):
    modes = {}
    for entry in git("ls-tree", "-rz", ref).split("\0"):
        if entry:
            metadata, name = entry.split("\t", 1)
            modes[name] = metadata.split()[0]
    # Never follow runtime symlinks or treat submodules as installed resources.
    files = {}
    for name, mode in modes.items():
        if mode not in ('100644', '100755'):
            files[name] = ''
        elif PurePosixPath(name).suffix.lower() in BINARY_SUFFIXES:
            files[name] = subprocess.check_output(['git', 'show', f'{ref}:{name}'], cwd=ROOT)
        else:
            files[name] = git('show', f'{ref}:{name}')
    return files, modes


def package(ref, expected_name):
    files, modes = ref_files(ref)
    return package_files(files, expected_name, modes)


def eval_cases(skill):
    path = ROOT / "evals" / f"{skill}.json"
    errors = []
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: {exc}"]
    if not isinstance(cases, list) or not cases:
        return [f"{path}: expected nonempty array"]
    ids = set()
    types = set()
    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            errors.append(f"{path}:{index}: expected object")
            continue
        for key in ("id", "kind", "prompt", "expected", "forbidden"):
            if not isinstance(case.get(key), str) or not case[key].strip():
                errors.append(f"{path}:{index}: missing {key}")
        if isinstance(case.get("id"), str):
            if case["id"] in ids:
                errors.append(f"{path}:{index}: duplicate id")
            ids.add(case["id"])
        if isinstance(case.get("kind"), str):
            types.add(case["kind"])
        if case.get("kind") not in ("behavior", "negative-trigger"):
            errors.append(f"{path}:{index}: invalid kind")
    if not {"behavior", "negative-trigger"}.issubset(types):
        errors.append(f"{path}: both behavior and negative-trigger cases required")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--andino-ref", default="origin/andino-workflow")
    parser.add_argument("--andino-dir", type=Path, help="validate an uncommitted Andino package instead of --andino-ref")
    parser.add_argument("--rescue-ref", default="origin/ai-codebase-rescue")
    parser.add_argument("--skripsi-ref", default="origin/skripsi-skill")
    parser.add_argument("--focus-ref", default="origin/focus")
    parser.add_argument("--focus-dir", type=Path, help="validate an uncommitted Focus package instead of --focus-ref")
    parser.add_argument("--webbased-ref", help="opt-in maintainer source-drift check against a locally available Git ref")
    parser.add_argument("--council-ref", default="origin/council")
    parser.add_argument("--search-first-ref", default="origin/search-first")
    parser.add_argument("--natural-writing-ref", default="origin/natural-writing")
    parser.add_argument("--natural-writing-dir", type=Path, help="validate an uncommitted Natural Writing package instead of --natural-writing-ref")
    parser.add_argument("--search-first-dir", type=Path, help="validate an uncommitted Search First package instead of --search-first-ref")
    parser.add_argument('--threejs-ref', help='opt-in local/fetched Three.js runtime ref')
    parser.add_argument('--threejs-dir', type=Path, help='opt-in Three.js runtime worktree')
    args = parser.parse_args()
    errors = []
    if args.threejs_ref or args.threejs_dir:
        try:
            all_files, all_modes = directory_files(args.threejs_dir) if args.threejs_dir else ref_files(args.threejs_ref)
            errors.extend(package_files(all_files, 'threejs-skills', all_modes))
        except (ValueError, OSError) as exc:
            errors.append(str(exc))
    for skill, ref in zip(RUNTIME_SKILLS, (args.andino_ref, args.rescue_ref, args.skripsi_ref, args.focus_ref, args.search_first_ref, args.council_ref, args.natural_writing_ref)):
        try:
            if skill == "focus":
                files, modes = directory_files(args.focus_dir) if args.focus_dir else ref_files(ref)
                errors.extend(package_files(files, skill, modes))
                if args.webbased_ref:
                    source = {name: git("show", f"{args.webbased_ref}:{name}") for name in (
                        "README.md", "put-in-your-projects/chat-rules.md",
                        "put-in-your-projects/human-language-indonesia.md",
                        "put-in-your-projects/human-language-english.md")}
                    errors.extend(focus_reference_drift(files, source))
            else:
                directory = args.andino_dir if skill == "andino-workflow" else args.search_first_dir if skill == "search-first" else args.natural_writing_dir if skill == "natural-writing" else None
                if directory:
                    files, modes = directory_files(directory)
                    errors.extend(package_files(files, skill, modes))
                else:
                    errors.extend(package(ref, skill))
        except (ValueError, OSError) as exc:
            errors.append(str(exc))
    for skill in EVAL_SKILLS:
        errors.extend(eval_cases(skill))
    if errors:
        print("FAIL: " + "\nFAIL: ".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: {len(RUNTIME_SKILLS)} skill packages, metadata, relative links, and {len(EVAL_SKILLS)} eval schemas")
    print("Live behavioral evaluation: NOT VERIFIED")
    if args.threejs_ref or args.threejs_dir:
        print(f'PASS: one Three.js family with {len(THREEJS_SKILLS)-1} internal methods')
    if args.webbased_ref:
        print(f"PASS: Focus communication references match {args.webbased_ref}; A sources equivalent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
