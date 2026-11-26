"""Print each required setting as ok / missing / bad format. Never prints values.

    python scripts/check_config.py            # .env plus environment
    python scripts/check_config.py --env-only # environment only (CI)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from shop import config  # noqa: E402


def main() -> int:
    status = config.check(config.load(env_only="--env-only" in sys.argv))
    for key, state in status.items():
        print(f"{key}: {state}")
    return 0 if all(s == "ok" for s in status.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
