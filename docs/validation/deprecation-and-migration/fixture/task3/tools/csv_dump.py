import json
import sys


def _fmt(item):
    return f'{item["sku"]},{item["name"]},{item["qty"]}'


def dump(items):
    lines = ["sku,name,qty"]
    for item in sorted(items, key=lambda i: i["sku"]):
        lines.append(_fmt(item))
    return "\n".join(lines)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as handle:
        print(dump(json.load(handle)))
