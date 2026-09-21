from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import shutil
import zipfile
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and checksum the standalone AI-RULES executable")
    parser.add_argument("--output", type=Path, default=Path("dist"))
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument("--asset-name", help="published filename (defaults to the PyInstaller filename)")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = (root / args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    staged_bundles = root / "src" / "ai_rules" / "release" / "data" / "bundles"
    manifest_path = root / "src" / "ai_rules" / "release" / "data" / "release_manifest.json"
    release_targets = json.loads(manifest_path.read_text(encoding="utf-8")).get("first_party", {})
    if staged_bundles.exists():
        shutil.rmtree(staged_bundles)
    for capability_id, target in release_targets.items():
        destination = staged_bundles / capability_id
        destination.mkdir(parents=True, exist_ok=True)
        archive = destination.with_suffix(".zip")
        subprocess.run(
            ["git", "archive", "--format=zip", f"--output={archive}", target["commit"]],
            cwd=root,
            check=True,
        )
        with zipfile.ZipFile(archive) as contents:
            contents.extractall(destination)
        archive.unlink()
        if not (destination / "SKILL.md").is_file():
            raise SystemExit(f"release bundle has no SKILL.md: {capability_id}")
    try:
        if not args.skip_build:
            subprocess.run(
                ["python", "-m", "PyInstaller", "packaging/ai_rules.spec", "--noconfirm", "--clean", "--distpath", str(output)],
                cwd=root,
                check=True,
            )
    finally:
        shutil.rmtree(staged_bundles, ignore_errors=True)
    built = output / ("ai-rules.exe" if platform.system().lower() == "windows" else "ai-rules")
    if args.asset_name and built.exists() and built.name != args.asset_name:
        built.rename(output / args.asset_name)
    artifacts = sorted(path for path in output.iterdir() if path.is_file() and path.name.startswith("ai-rules"))
    if not artifacts:
        raise SystemExit("no standalone ai-rules artifact found")
    manifest = {
        "schema_version": 1,
        "platform": {"system": platform.system().lower(), "architecture": platform.machine().lower()},
        "artifacts": [{"name": path.name, "sha256": sha256(path), "size": path.stat().st_size} for path in artifacts],
    }
    try:
        manifest["source_commit"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        manifest["source_commit"] = "unknown"
    (output / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (output / "SHA256SUMS").write_text(
        "".join(f"{entry['sha256']}  {entry['name']}\n" for entry in manifest["artifacts"]),
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
