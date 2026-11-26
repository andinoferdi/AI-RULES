# Filebox

Invoice storage for small businesses. Each business is a tenant; every user belongs to
one tenant. Clients call the JSON API with `Authorization: Bearer <token>`.

`filebox.app.handle(request)` routes a `Request` to a handler and returns a `Response`.
`filebox.db.connect(path)` opens the SQLite database and creates the schema;
`filebox.seed.load(conn)` inserts the development data from `data/seed.json`.
Uploaded files live under `storage/` (configurable with `FILEBOX_STORAGE`).

Run the tests with `python -m unittest discover -s tests -t .`

Release process: every change reaches `main` through a reviewed branch.
