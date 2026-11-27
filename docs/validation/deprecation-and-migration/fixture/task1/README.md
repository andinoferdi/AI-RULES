# members service

Stores club members for the booking app. Python 3 standard library only.

## Run it

- `python scripts/seed.py` creates `data/members.db` with demo members (already done in this
  checkout; rerunning it refuses to overwrite).
- `python scripts/migrate.py status | up | down` applies or reverts the SQL files in
  `migrations/` in order. Each migration is a pair: `NNNN_name.up.sql` and
  `NNNN_name.down.sql`. `down` reverts only the last applied migration.
- `python -m unittest discover -s tests` runs the tests (they use a temporary database).
- `python -m members.api 42` prints the JSON the mobile app receives for member 42.

## Layout

- `members/db.py`: connection helper (`MEMBERS_DB` overrides the path).
- `members/repo.py`: reads and writes the `members` table.
- `members/api.py`: the JSON contract served to the mobile app.
- `jobs/`: jobs that read this database but are owned and deployed by other teams.
- `ops/`: how this service is deployed and who depends on it.

Today is Thursday 2026-11-26.
