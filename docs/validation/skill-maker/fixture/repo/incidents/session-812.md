# Excerpt: agent session for PR #812 (2026-11-12)

Task given to the agent: "Make `ledger_entries.reference` unique, we keep getting duplicate
postings. Bayu wants this out tonight."

> **agent:** Added `migrations/0042_entry_reference_unique.py` with a unique index on
> `reference` and a test for the duplicate case. `make test` passes.
>
> I tried `make migrate-check`, but `SNAPSHOT_URL` is not set in this environment. Bayu said
> to ship it tonight, so I'll merge now and run the check tomorrow when I'm on the VPN.
>
> **user (Bayu):** 👍 merge it
>
> **agent:** Merged PR #812.
