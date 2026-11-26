# ADR-0001: Postgres in production, pg-mem in tests

## Status
Accepted (2024-09)

## Context
Billing data needs transactions across invoices, subscriptions and ledger entries. Tests should
not need a running database server.

## Decision
Use Postgres through `pg` in production. Tests that need SQL run against pg-mem, an in-memory
Postgres emulation, created per test file.

## Consequences
- Code that talks to the database should accept a `pg`-compatible pool so tests can pass a pg-mem
  pool.
- Features pg-mem does not support (advisory locks, some window functions) must not be used.
