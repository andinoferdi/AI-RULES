# Who depends on the members database and API

| Consumer | What it uses | Owner | Deploys |
| --- | --- | --- | --- |
| Mobile app 3.x | `members.api` JSON, field `name` | mobile team (Yoga) | app stores; 3.x is about 18% of active users and has no forced upgrade |
| Mobile app 4.x | `members.api` JSON, field `name` | mobile team (Yoga) | app stores |
| Billing export | `jobs/billing_export.py`, raw SQL on `members` | billing (Rina) | billing's pipeline, monthly on the 1st |
| members-sync worker | writes `members` directly | platform (Arief) | see `ops/fleet.md` |
