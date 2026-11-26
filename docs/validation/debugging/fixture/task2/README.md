# Catalog

Builds the storefront catalog from our primary product feed and the partner's feed.
A scheduler runs the build every five minutes.

    python scripts/make_feed.py                       # writes data/primary.csv and data/feed-big.csv
    python -m catalog.build --feed data/feed-big.csv  # prints the product count and a checksum

Tests: `python -m unittest discover -s tests -t .`

See CHANGELOG.md for releases.
