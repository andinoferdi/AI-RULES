# members-sync worker fleet

The worker imports members from partner clubs. It is a separate service from this
repository and writes straight to the `members` table:

    INSERT INTO members (name, email, joined_on) VALUES (?, ?, ?)
    UPDATE members SET name = ? WHERE email = ?

| Version | Hosts | Status |
| --- | --- | --- |
| 1.4 | sync-01, sync-02 | pinned until 2026-12-15 (partner club contract freeze) |
| 1.5 | sync-03 | canary |

Platform (Arief) can ship a new worker version after the freeze ends.
