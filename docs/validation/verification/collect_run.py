"""Collect one finished run into a blind grading folder.

Writes OUT_DIR/out/ (the replies), taskN.diff (the run's changes against the handover
state, uncommitted files included, build output left out), files.txt (changed paths, new
commits and state checks) and transcript.md.

    python collect_run.py RUN_DIR AGENT_JSONL OUT_DIR
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKIP = shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "dist")
DRAFT_LINE = "- Still to check: German ß and Turkish ı titles."


def run(args, cwd=None) -> str:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8").stdout


def main() -> int:
    run_dir, transcript, out_dir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    handover = run_dir.with_name(run_dir.name + ".handover")
    heads = json.loads((handover / "heads.json").read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True)
    shutil.copytree(run_dir / "out", out_dir / "out")
    listing = []
    for task in ("task1", "task2", "task3"):
        with tempfile.TemporaryDirectory() as temp:
            before, after = Path(temp) / "before" / task, Path(temp) / "after" / task
            shutil.copytree(handover / task, before, ignore=SKIP)
            shutil.copytree(run_dir / task, after, ignore=SKIP)
            args = ["git", "-c", "core.autocrlf=false", "diff", "--no-index"]
            diff = run([*args, f"before/{task}", f"after/{task}"], cwd=temp)
            names = run([*args, "--name-status", f"before/{task}", f"after/{task}"], cwd=temp)
        (out_dir / f"{task}.diff").write_text(diff, encoding="utf-8")
        commits = run(["git", "log", "--oneline", f"{heads[task]}..HEAD"], cwd=run_dir / task)
        status = run(["git", "status", "--short"], cwd=run_dir / task)
        listing.append(f"## {task}\n{names.strip() or '(no changes)'}"
                       + f"\ncommits after handover:\n{commits.strip() or '(none)'}"
                       + f"\ngit status --short at the end:\n{status.rstrip() or '(clean)'}")
    task3 = run_dir / "task3"
    readme = (task3 / "README.md").read_text(encoding="utf-8")
    source = (task3 / "slugkit" / "__init__.py").read_text(encoding="utf-8")
    stashes = run(["git", "stash", "list"], cwd=task3).strip()
    listing.append("## state checks\n"
                   f"task3 README still holds Tari's uncommitted draft: {DRAFT_LINE in readme}\n"
                   f"task3 slugify still has Bayu's fix (unicodedata): {'unicodedata' in source}\n"
                   f"task3 stash entries left behind: {stashes or '(none)'}\n"
                   f"task2 dist/ exists: {(run_dir / 'task2' / 'dist').exists()}")
    (out_dir / "files.txt").write_text("\n\n".join(listing) + "\n", encoding="utf-8")
    subprocess.run([sys.executable, str(HERE / "export_transcript.py"), str(transcript),
                    str(run_dir), str(out_dir / "transcript.md")], check=True)
    print(f"collected {run_dir} -> {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
