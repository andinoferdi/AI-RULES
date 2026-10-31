import argparse
import json
from pathlib import Path


def load_rows(path: Path) -> list[dict[str, str]]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    schema = json.loads(Path(__file__).with_name("schema.json").read_text(encoding="utf-8"))
    parser.add_argument("--state", choices=["all", *schema["states"]], default="all")
    args = parser.parse_args(argv)
    rows = load_rows(args.source)
    if args.state != "all":
        rows = [row for row in rows if row["state"] == args.state]
    print(json.dumps(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
