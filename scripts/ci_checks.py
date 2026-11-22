"""Run the model-free checks that gate main, in the same order as CI.

CI and `scripts/promote_skill.py` both call this file, so a local promote run and
the pull request check the same things. Run `scripts/skill_refs.py pin` first so
skill refs resolve to the pinned commits. Stops at the first failing step.
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def steps(staging: Path) -> list[tuple[str, list[str]]]:
    py = sys.executable
    return [
        ("Validate skill packages", [py, "scripts/validate_skills.py",
                                     "--webbased-ref", "origin/WebBased", "--threejs-ref", "origin/threejs-skills"]),
        ("Validate Three.js inventory and scenario schemas",
         [py, "scripts/validate_threejs_family.py", "--runtime-ref", "origin/threejs-skills"]),
        ("Validate capability evaluation schemas",
         [py, "scripts/validate_andino_capabilities.py", "--runtime-ref", "origin/andino-workflow"]),
        ("Test validators and installer regressions", [py, "-m", "unittest", "discover", "-s", "tests"]),
        ("Audit skripsi requirement ownership", [py, "scripts/validate_skripsi_traceability.py"]),
        ("Validate frozen release bundles",
         [py, "scripts/build_release.py", "--stage-only", "--output", str(staging)]),
    ]


def run(root: Path = ROOT, runner=subprocess.run) -> tuple[bool, str]:
    """Return (passed, name of the failing step or '')."""
    # Import this checkout's package even when another AI-RULES copy is installed.
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(
        filter(None, [str(root / "src"), os.environ.get("PYTHONPATH")])))
    with tempfile.TemporaryDirectory(prefix="ai-rules-ci-") as temp:
        for name, command in steps(Path(temp) / "frozen-bundles"):
            print(f"==> {name}", flush=True)
            if runner(command, cwd=root, env=env).returncode:
                print(f"FAIL: {name}", file=sys.stderr, flush=True)
                return False, name
    print("PASS: all main checks", flush=True)
    return True, ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    return 0 if run(parser.parse_args().root)[0] else 1


if __name__ == "__main__":
    raise SystemExit(main())
