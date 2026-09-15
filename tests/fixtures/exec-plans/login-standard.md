# LOGIN-01 — Demo login lokal

Status: IN_PROGRESS
Plan Depth: STANDARD
Current Phase: Phase 3 — Protected flow
Last Updated: 2026-09-15

## Executive Snapshot

Build a native PHP/SQLite login demo. Database and authentication primitives pass;
the next action is to protect `dashboard.php`, add logout, then run HTTP flow tests.

## Objective

Deliver a secure local login, protected dashboard and logout flow without a framework.

## Acceptance Criteria

- [x] SQLite initializes with hashed seed users.
- [x] Authentication uses prepared statements and generic failures.
- [ ] Unauthenticated dashboard access redirects and logout terminates the session.
- [ ] Unit and HTTP integration suites pass.

## Scope

### In Scope

- Native PHP, PDO SQLite, session authentication, login/dashboard/logout UI.

### Out of Scope

- Registration, OAuth, APIs, Composer dependencies and production deployment.

## Current Technical Context

`config/database.php` owns PDO setup; `includes/auth.php` owns session and CSRF
helpers. Login POST verifies the stored password hash and rotates the session ID.

## Architecture / Approach

Keep database, auth helpers, handlers and pages separate. Route guards run before
rendering; POST handlers validate CSRF and redirect with generic session messages.

## File Impact Map

### Modify

- `dashboard.php` — require authenticated session.
- `logout.php` — terminate session and redirect.
- `tests/test_http.php` — exercise protected flow.

## Execution Board

| Phase | Status | Goal | Scope | Evidence / Result |
| --- | --- | --- | --- | --- |
| Phase 1 — Database | DONE | Initialize and seed SQLite | `config/`, `scripts/` | Seed users load with password hashes. |
| Phase 2 — Authentication | DONE | Secure credential verification | `includes/`, `login_action.php` | Unit flow assertions pass. |
| Phase 3 — Protected flow | IN_PROGRESS | Guard dashboard and implement logout | `dashboard.php`, `logout.php` | Pending HTTP flow verification. |
| Phase 4 — Delivery | TODO | Run final checks and document use | tests and README | Pending. |

# Detailed Execution

## Phase 1 — Database

Status: DONE
Goal: Provide repeatable SQLite initialization.

### Result / Evidence

- Actual: CLI initialization creates the schema and two hashed seed users.

## Phase 2 — Authentication

Status: DONE
Goal: Verify credentials without leaking account existence.

### Result / Evidence

- Actual: Prepared lookup, `password_verify`, CSRF validation and session rotation pass unit checks.

## Phase 3 — Protected flow

Status: IN_PROGRESS
Goal: Prevent guest dashboard access and make logout safely terminate the session.

### Technical Contract

Input: authenticated or guest session.
Output: dashboard HTML for authenticated users; redirect otherwise.
Postconditions / invariants: logout clears server session and cookie.

### Verification

- Planned: `php tests/test_http.php`
- Expected/pass criteria: guest redirect, successful login/dashboard, failed login and logout checks pass.

## Phase 4 — Delivery

Status: TODO
Goal: Run complete local verification and document demo credentials.

## Decisions Log

- D-001 — Use `PASSWORD_DEFAULT`; it keeps hashing policy aligned with the PHP runtime.

## Verification Matrix

| Requirement | Verification | Status | Evidence |
| --- | --- | --- | --- |
| Database and secure auth | `php tests/test_flow.php` | DONE | Unit flow assertions pass. |
| Protected HTTP flow | `php tests/test_http.php` | TODO | Pending Phase 3. |

## Files / Areas Touched

- `config/database.php`, `scripts/init_db.php` — actual database setup.
- `includes/auth.php`, `login_action.php` — actual authentication flow.

## NEXT ACTION

Inspect the route guard in `dashboard.php`, implement session teardown in
`logout.php`, then run `php tests/test_http.php`.
