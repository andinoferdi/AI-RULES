# help.example.com

Static help site.

- Build: `python build.py` writes `site/`.
- Test: `python -m unittest discover -s tests -v` (every page renders, has the footer, and
  internal links resolve).
- Publish: `python scripts/publish.py` uploads `site/` to production and keeps the build it
  replaces. `python scripts/publish.py --restore-previous` puts that previous build back.
