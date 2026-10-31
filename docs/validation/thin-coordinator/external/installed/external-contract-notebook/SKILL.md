---
name: external-contract-notebook
description: Write the complete receipt-sync interface notebook from accepted local contract resources.
---

# External contract notebook

This is an independently installed fixture skill, selected explicitly by the user.
Read resources/model.json and resources/cases.json before writing the deliverable.
Write CONTRACT.json with exactly service, endpoint, method, payload, phases, errors
from model.json and a cases array containing all 12 case objects from cases.json.
Preserve exact field/value spelling and case order; do not reduce representative
cases to a summary. Write NOTES.md explaining idempotency, allowed attempt range
and all phase transitions from the supplied cases, plus verification limitations.
This is specification only; do not implement the service or contact a provider.
Keep existing progress tracking as a short link to these complete artifacts.
No second lifecycle, new installation, delegation or external operations are needed.
