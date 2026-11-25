# dbt conventions

- Every model lives in `models/<layer>/` where layer is `staging`, `intermediate` or `marts`.
- Staging models only rename and cast columns; joins start in `intermediate`.
- A schema change to a mart needs a `contract: enforced` block and a version bump.
- Add a `unique` and a `not_null` test on every model's primary key.
