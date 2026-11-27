"""Build dist/unitconv-<version>.zip after checking the package data and version."""
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "unitconv"


def fail(message):
    print(f"build failed: {message}")
    sys.exit(1)


version = re.search(r'__version__ = "([^"]+)"', (PACKAGE / "__init__.py").read_text()).group(1)
for data_file in sorted((PACKAGE / "data").glob("*.json")):
    try:
        json.loads(data_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"{data_file.relative_to(ROOT)} is not valid JSON: {error}")

dist = ROOT / "dist"
dist.mkdir(exist_ok=True)
target = dist / f"unitconv-{version}.zip"
with zipfile.ZipFile(target, "w") as archive:
    for path in sorted(PACKAGE.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            archive.write(path, path.relative_to(ROOT))
print(f"built {target.relative_to(ROOT)}")
