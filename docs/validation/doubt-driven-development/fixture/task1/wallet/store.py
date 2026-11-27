"""JSON-file account store. Every write replaces the file atomically (temp file + os.replace)."""
import json
import os
import tempfile
from pathlib import Path


class Store:
    def __init__(self, path):
        self.path = Path(path)

    def _read(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, data):
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=1)
        os.replace(tmp, self.path)

    def schema_version(self):
        return self._read()["schema_version"]

    def set_schema_version(self, version):
        data = self._read()
        data["schema_version"] = version
        self._write(data)

    def load_accounts(self):
        return self._read()["accounts"]

    def save_batch(self, accounts):
        """Replace the given accounts (matched by id) in one atomic write."""
        data = self._read()
        by_id = {account["id"]: account for account in accounts}
        data["accounts"] = [by_id.get(account["id"], account) for account in data["accounts"]]
        self._write(data)
