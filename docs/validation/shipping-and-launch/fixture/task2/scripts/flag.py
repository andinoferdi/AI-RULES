"""Read or change a feature flag: flag.py status | flag.py set <flag> <percent>."""
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FLAGS = ROOT / "ops" / "flags.json"


def main(argv):
    flags = json.loads(FLAGS.read_text(encoding="utf-8"))
    if argv[:1] == ["status"]:
        for name, percent in flags.items():
            print(f"{name}: {percent}%")
        return 0
    if len(argv) == 3 and argv[0] == "set":
        name, percent = argv[1], int(argv[2])
        old = flags.get(name)
        flags[name] = percent
        FLAGS.write_text(json.dumps(flags) + "\n", encoding="utf-8")
        stamp = datetime.datetime.now().isoformat(timespec="seconds")
        with (ROOT / "ops" / "flag-audit.log").open("a", encoding="utf-8") as log:
            log.write(f"{stamp} {name}: {old}% -> {percent}%\n")
        print(f"{name}: {old}% -> {percent}% (applies within a minute)")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
