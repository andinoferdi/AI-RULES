# Misc notes

- 2025-03: we moved CI from Jenkins to GitHub Actions.
- The old `tidewater-legacy` repo is archived; do not open issues there.
- Never start a backfill between 02:00 and 04:00 UTC. The nightly load runs in that window,
  both compete for the same warehouse slots, and a collision corrupts the day's partition.
- Coffee machine on floor 3 is broken.
