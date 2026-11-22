"""Run the model-free checks that gate main, in the same order as CI.

Every check reads the skills/ folder of this checkout, so a skill change and the
tests it affects are always checked together.

Groups:
  skills     skill packages, validators and every test in tests/ that reads real
             skill content (run on every pull request)
  installer  tests/installer: installer code with fixture data (CI runs it on
             three operating systems when installer files change)
  all        both (default)

The WebBased drift check needs the pinned WebBased commit locally:
`git fetch origin WebBased`.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "src/ai_rules/release/data/release_manifest.json"


def webbased_commit(root: Path = ROOT) -> str:
    return json.loads((root / MANIFEST.relative_to(ROOT)).read_text(encoding="utf-8"))["validation_refs"]["WebBased"]["commit"]


def steps(staging: Path, group: str = "all", root: Path = ROOT) -> list[tuple[str, list[str]]]:
    py = sys.executable
    skill_tests = sorted(path.stem for path in (root / "tests").glob("test_*.py"))
    skills = [
        ("Validate skill packages", [py, "scripts/validate_skills.py", "--webbased-ref", webbased_commit(root)]),
        ("Validate Three.js inventory and scenario schemas", [py, "scripts/validate_threejs_family.py"]),
        ("Validate capability evaluation schemas", [py, "scripts/validate_andino_capabilities.py"]),
        ("Test skills and validators", [py, "-m", "unittest", *skill_tests]),
        ("Audit skripsi requirement ownership", [py, "scripts/validate_skripsi_traceability.py"]),
        ("Validate frozen release bundles",
         [py, "scripts/build_release.py", "--stage-only", "--output", str(staging)]),
    ]
    installer = [("Test installer regressions", [py, "-m", "unittest", "discover", "-s", "tests/installer"])]
    return {"skills": skills, "installer": installer, "all": skills + installer}[group]


def run(root: Path = ROOT, runner=subprocess.run, group: str = "all") -> tuple[bool, str]:
    """Return (passed, name of the failing step or '')."""
    # Import this checkout's package even when another AI-RULES copy is installed;
    # tests/ on the path lets unittest load the top-level test modules by name.
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(
        filter(None, [str(root / "src"), str(root / "tests"), os.environ.get("PYTHONPATH")])))
    try:
        webbased = webbased_commit(root)
        subprocess.run(["git", "cat-file", "-e", f"{webbased}^{{commit}}"], cwd=root, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (OSError, KeyError, ValueError, subprocess.CalledProcessError):
        if group != "installer":
            print("FAIL: the pinned WebBased commit is missing; run git fetch origin WebBased", file=sys.stderr)
            return False, "Fetch WebBased"
    with tempfile.TemporaryDirectory(prefix="ai-rules-ci-") as temp:
        for name, command in steps(Path(temp) / "frozen-bundles", group, root):
            print(f"==> {name}", flush=True)
            if runner(command, cwd=root, env=env).returncode:
                print(f"FAIL: {name}", file=sys.stderr, flush=True)
                return False, name
    print(f"PASS: all {group} checks", flush=True)
    return True, ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--group", choices=("skills", "installer", "all"), default="all")
    args = parser.parse_args()
    return 0 if run(args.root, group=args.group)[0] else 1


if __name__ == "__main__":
    raise SystemExit(main())
