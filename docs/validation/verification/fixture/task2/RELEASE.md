# Release checklist

A version is ready to tag only when every item below passes on the commit being tagged.

1. Tests pass: `python -m unittest`
2. Lint is clean: `python scripts/lint.py`
3. Build succeeds and writes `dist/unitconv-<version>.zip`: `python scripts/build.py`
4. The version is the same in `pyproject.toml`, `unitconv/__init__.py` and the top entry of
   `CHANGELOG.md`.
5. Smoke test against staging passes: `python scripts/smoke.py --host staging.unitconv.invalid`
