"""Validate the two branch-distributed skills and their review-only eval cases."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("andino-workflow", "ai-codebase-rescue")
LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):[ \t]+(.+)$")


def git(*args):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise ValueError(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout


def package_files(files, expected_name):
    errors = []
    for name in files:
        if name not in ("README.md", "SKILL.md") and not (name.startswith("references/") and name.endswith(".md")):
            errors.append(f"{expected_name}: unexpected runtime file: {name}")
    if "SKILL.md" not in files:
        return [f"{expected_name}: missing SKILL.md"]
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
                if value.startswith(("[", "{", "'", '"', "|", ">", "&", "*", "!")) or ": " in value or "\t" in value:
                    errors.append(f"{expected_name}: unsupported frontmatter scalar: {line}")
                    continue
                fields[match[1]] = value
            if fields.get("name") != expected_name:
                errors.append(f"{expected_name}: wrong or missing name")
            if not fields.get("description"):
                errors.append(f"{expected_name}: missing description")
    for name, content in files.items():
        if not name.endswith(".md"):
            continue
        for raw in LINK.findall(content):
            target = unquote(raw.split("#", 1)[0].strip().split(" ", 1)[0])
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("/"):
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


def package(ref, expected_name):
    names = git("ls-tree", "-r", "--name-only", ref).splitlines()
    files = {name: git("show", f"{ref}:{name}") for name in names}
    return package_files(files, expected_name)


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
        if case.get("id") in ids:
            errors.append(f"{path}:{index}: duplicate id")
        ids.add(case.get("id"))
        types.add(case.get("kind"))
        if case.get("kind") not in ("behavior", "negative-trigger"):
            errors.append(f"{path}:{index}: invalid kind")
    if not {"behavior", "negative-trigger"}.issubset(types):
        errors.append(f"{path}: both behavior and negative-trigger cases required")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--andino-ref", default="origin/andino-workflow")
    parser.add_argument("--rescue-ref", default="origin/ai-codebase-rescue")
    args = parser.parse_args()
    errors = []
    for skill, ref in zip(SKILLS, (args.andino_ref, args.rescue_ref)):
        try:
            errors.extend(package(ref, skill))
        except ValueError as exc:
            errors.append(str(exc))
        errors.extend(eval_cases(skill))
    if errors:
        print("FAIL: " + "\nFAIL: ".join(errors), file=sys.stderr)
        return 1
    print("PASS: two skill packages, metadata, relative links, and eval schemas")
    print("Live behavioral evaluation: NOT VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
