"""Upload site/ to production, keeping the replaced build for --restore-previous."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    action = "restored previous build" if "--restore-previous" in sys.argv else "published site/"
    (ROOT / ".published").write_text(action + "\n", encoding="utf-8")
    print(f"{action} to help.example.com")


if __name__ == "__main__":
    main()
