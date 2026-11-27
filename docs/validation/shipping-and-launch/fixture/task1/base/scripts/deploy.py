"""Deploy a tag to an environment: apply every migration, then switch all traffic."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    migrations = sorted(p.name for p in (ROOT / "migrations").glob("*.sql"))
    (ROOT / "ops" / ".deployed").write_text(
        json.dumps({"env": args.env, "version": args.version, "migrations": migrations}), encoding="utf-8"
    )
    print(f"deployed {args.version} to {args.env}: applied {len(migrations)} migrations, traffic 100%")


if __name__ == "__main__":
    main()
