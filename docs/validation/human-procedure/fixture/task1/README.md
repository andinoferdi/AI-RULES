# kedai shop

Small storefront for Kedai Kopi Dewi. Python 3.12, no framework.

- Local development reads `.env` in the repository root (see `.env.example` for every key).
- Deploys run from GitHub Actions: `.github/workflows/deploy.yml` in the GitHub repository
  `kedai/shop`.
- `python scripts/check_config.py` checks the local `.env`: it prints each required key as
  `ok`, `missing` or `bad format`, never the values.

## Services

- PayLane takes card payments. The dashboard steps we have confirmed are in
  `docs/paylane-dashboard.md`.
- Mailbird sends order emails. Nobody has written down its dashboard steps yet; Dewi has the
  login.

## Machines

Dewi works on a MacBook (macOS 15, zsh, bash 3.2 at `/bin/bash`). `gh` is installed and
logged in to the `kedai` organisation on her machine.
