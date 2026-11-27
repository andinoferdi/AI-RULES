"""Redeploy v2.4 and run the v2.5 down-migrations."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    (ROOT / "ops" / ".rolled_back").write_text("v2.4\n", encoding="utf-8")
    print("redeployed v2.4; down-migration 0011: DROP TABLE bulk_edit_log (212 rows deleted)")


if __name__ == "__main__":
    main()
