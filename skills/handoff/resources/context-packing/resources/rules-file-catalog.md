# Multi-Harness Rules File Catalog & Ecosystem Presets

A project rules file is **Level 1 of the Context Hierarchy**—the single highest-leverage artifact you can introduce into an AI-assisted development workflow. It provides persistent, deterministic guidance that loads automatically into every session, grounding the model in your project's exact stack, verified commands, architectural boundaries, and code style.

This catalog provides production-ready, battle-tested templates across leading AI coding harnesses (Claude Code, OpenAI Codex, Cursor, Windsurf, Copilot) and major technology ecosystems.

---

## 1. Anatomy of a High-Impact Rules File

Every high-performing rules file must answer five critical questions in under 150 lines:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Tech Stack: Exactly what languages, frameworks, versions │
├─────────────────────────────────────────────────────────────┤
│ 2. Commands: Exact executable build, test, lint, typecheck  │
├─────────────────────────────────────────────────────────────┤
│ 3. Conventions: Naming, exports, architecture, testing      │
├─────────────────────────────────────────────────────────────┤
│ 4. Boundaries: Hard red lines (secrets, dependencies, DB)   │
├─────────────────────────────────────────────────────────────┤
│ 5. Canonical Pattern: ONE clean code example demonstrating  │
│    the preferred pattern and style                          │
└─────────────────────────────────────────────────────────────┘
```

### The 3 Golden Rules of Rules Files
1. **Be Exact, Not Generic**: Write `npm run test:unit -- --runInBand`, never "run tests appropriately".
2. **Document Exceptions, Not Obvious Basics**: Models already know how to write standard functions. Document what is unique or counter-intuitive to *your* codebase.
3. **Keep It Under 150 Lines**: A bloated 600-line rules file saturates the primacy zone and paradoxically reduces instruction compliance.

---

## 2. Harness-Specific Conventions

Different AI harnesses look for rules files at specific filesystem locations:

| Harness | Primary File Location | Format | Notes |
|---|---|---|---|
| **Claude Code** | `CLAUDE.md` (or `.claude/CLAUDE.md`) | Markdown | Loaded automatically at session start; injected into system context. |
| **OpenAI Codex** | `AGENTS.md` | Markdown | Standard system context file for Codex and OpenAI CLI harnesses. |
| **Cursor** | `.cursorrules` or `.cursor/rules/*.mdc` | Markdown / MDC | Modern Cursor supports directory-based `.mdc` files with glob matching. |
| **Windsurf** | `.windsurfrules` | Markdown | Evaluated on every cascade turn. |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Markdown | Read by Copilot Chat in VS Code / JetBrains / Web. |

---

## 3. Production Ecosystem Presets

### Preset A: TypeScript / Next.js (App Router, Tailwind, Prisma)

**Target file**: `CLAUDE.md` or `.cursorrules`

```markdown
# Project: SaaS Platform Core

## Tech Stack
- Next.js 15 (App Router, React 19, Server Components by default)
- TypeScript 5.5 (strict mode enabled, no `any`)
- Tailwind CSS 4, Radix UI primitives, `lucide-react`
- PostgreSQL 16, Prisma ORM, Node.js 22 LTS
- Testing: Vitest, React Testing Library

## Verification Commands
- Build: `npm run build`
- Typecheck: `npx tsc --noEmit`
- Test: `npm test`
- Single Test: `npx vitest run src/services/auth.test.ts`
- Lint: `npm run lint -- --fix`

## Code Conventions
- Server Components by default; add `'use client'` only when state or event listeners are required.
- Named exports only; no `default export` except for Next.js App Router special files (`page.tsx`, `layout.tsx`).
- Colocate unit tests immediately adjacent to source: `Button.tsx` -> `Button.test.tsx`.
- Use the `cn()` utility (`clsx` + `tailwind-merge`) for conditional classNames.
- Route handlers must validate incoming payloads using Zod schemas before database operations.
- Handle expected domain errors with explicit result types; avoid unhandled throw cascades.

## Hard Boundaries
- Never commit `.env`, credentials, or private API keys.
- Never add new npm dependencies without verifying bundle size impact and licensing.
- Never execute destructive database schema migrations without explicit user approval.
- Always run `npx tsc --noEmit` and `npm test` before declaring a task complete.

## Canonical Pattern (Route Handler)
```typescript
import { NextResponse } from 'next/server';
import { z } from 'zod';
import { prisma } from '@/lib/db';

const CreateItemSchema = z.object({
  name: z.string().min(1).max(100),
  quantity: z.number().int().positive(),
});

export async function POST(req: Request) {
  try {
    const json = await req.json();
    const result = CreateItemSchema.safeParse(json);
    if (!result.success) {
      return NextResponse.json({ error: 'Validation failed', details: result.error.flatten() }, { status: 400 });
    }
    const item = await prisma.item.create({ data: result.data });
    return NextResponse.json({ data: item }, { status: 201 });
  } catch (error) {
    console.error('Failed to create item:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
```
```

---

### Preset B: Python / FastAPI & Pydantic

**Target file**: `AGENTS.md` or `CLAUDE.md`

```markdown
# Project: High-Throughput Analytics API

## Tech Stack
- Python 3.12+, FastAPI, Uvicorn
- Pydantic v2 (BaseModel, strict mode)
- SQLAlchemy 2.0 (asyncio + asyncpg), Alembic migrations
- Testing: Pytest, pytest-asyncio, pytest-cov
- Quality: Ruff (linter + formatter), Mypy (strict)

## Verification Commands
- Run API: `uvicorn app.main:app --reload`
- Typecheck: `mypy app/`
- Lint & Format: `ruff check app/ --fix && ruff format app/`
- Test All: `pytest`
- Single Test: `pytest tests/test_orders.py -k test_calculate_total -vv`
- Coverage: `pytest --cov=app --cov-report=term-missing`

## Code Conventions
- Async by default for all I/O, database sessions, and external HTTP calls.
- Use explicit Pydantic v2 schemas for all request payloads and response models.
- Type annotations required on all function signatures (`def foo(x: int) -> str:`).
- Database sessions injected via FastAPI `Depends(get_db_session)`.
- Use custom exception classes inheriting from `DomainException`; transform in global handlers.

## Hard Boundaries
- Do not execute raw SQL queries string-interpolated with user input.
- Do not introduce blocking synchronous calls (e.g. `requests.get` or `time.sleep`) inside async endpoints.
- Preserve database migrations: never edit existing applied Alembic migration files.

## Canonical Pattern (Service Method)
```python
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.account import Account
from app.schemas.account import AccountCreate
from app.exceptions import AccountAlreadyExistsError

class AccountService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_account(self, payload: AccountCreate) -> Account:
        existing = await self._session.get(Account, payload.id)
        if existing:
            raise AccountAlreadyExistsError(f"Account {payload.id} already exists")
        account = Account(**payload.model_dump())
        self._session.add(account)
        await self._session.flush()
        return account
```
```

---

### Preset C: Go / Standard Library & Microservices

**Target file**: `AGENTS.md` or `.windsurfrules`

```markdown
# Project: Ingestion Worker Service

## Tech Stack
- Go 1.23+, standard library `net/http` with `chi` router
- Database: `pgx/v5` PostgreSQL driver
- Observability: OpenTelemetry Go, `slog` structured logging
- Testing: Standard `testing` package, `testify/assert`
- Linter: `golangci-lint`

## Verification Commands
- Build: `go build ./...`
- Test All: `go test -race -v ./...`
- Single Test: `go test -v -run TestProcessRecord ./internal/worker`
- Lint: `golangci-lint run ./...`
- Tidy: `go mod tidy`

## Code Conventions
- Accept interfaces, return concrete structs.
- Errors are values: always handle errors explicitly; never ignore returned errors (`_ = fn()`).
- Wrap errors with contextual information using `fmt.Errorf("worker: processing id %s: %w", id, err)`.
- Use `slog` for structured logging with key-value pairs; never use `fmt.Println` in production code.
- Always propagate `context.Context` as the first argument in all I/O and database operations.

## Hard Boundaries
- No global mutable state or init-time side-effects outside database connection pools.
- Goroutines must always be bounded with a `sync.WaitGroup`, errgroup, or worker pool—no orphaned goroutines.
- All network operations must respect timeouts via context deadlines.

## Canonical Pattern
```go
package worker

import (
	"context"
	"fmt"
	"log/slog"
)

type RecordProcessor struct {
	logger *slog.Logger
	store  Store
}

func (p *RecordProcessor) Process(ctx context.Context, id string) error {
	select {
	case <-ctx.Done():
		return ctx.Err()
	default:
	}

	record, err := p.store.Get(ctx, id)
	if err != nil {
		return fmt.Errorf("processor: fetch record %s: %w", id, err)
	}

	p.logger.InfoContext(ctx, "record processed", slog.String("id", id), slog.Int("size", len(record.Payload)))
	return nil
}
```
```

---

### Preset D: Rust / High-Reliability Systems

**Target file**: `CLAUDE.md` or `AGENTS.md`

```markdown
# Project: Realtime Event Router

## Tech Stack
- Rust 2021 edition (1.80+)
- Async Runtime: Tokio, Axum web framework
- Serialization: Serde, serde_json
- Testing: Built-in `cargo test`, `proptest`
- Linter: `cargo clippy -- -D warnings`

## Verification Commands
- Check: `cargo check`
- Build: `cargo build`
- Test: `cargo test`
- Single Test: `cargo test test_route_event -- --nocapture`
- Clippy: `cargo clippy --all-targets -- -D warnings`
- Format: `cargo fmt --check`

## Code Conventions
- Prefer `Result<T, E>` and `Option<T>` over panics. Avoid `.unwrap()` and `.expect()` in non-test code.
- Define explicit error types using `thiserror` for library boundaries and `anyhow` for binaries.
- Keep data structures immutable by default; use `&mut` only within bounded private scopes.
- Leverage the type system to make invalid state unrepresentable (typestate pattern).

## Hard Boundaries
- No `unsafe` blocks without explicit ADR authorization and machine-checked safety comments.
- Do not add crates with heavy transitive dependencies without team review.
- All public functions must have doc tests or unit tests.
```

---

## 4. Maintenance and Anti-Rot Checklist

To keep your rules files healthy and prevent instruction dilution:

- [ ] **Monthly Verification Audit**: Run every command in the rules file in a clean terminal to ensure none have broken.
- [ ] **Prune Redundancy**: If the AI model consistently follows a convention without prompting, delete that line. Save context tokens for unique constraints.
- [ ] **Sync with CI**: Ensure the commands listed under "Verification Commands" match the exact flags executed in your GitHub Actions / GitLab CI pipeline.
- [ ] **Keep Single-Page**: If your rules file exceeds 150 lines, split domain-specific rules into `docs/` and load them on demand via the Selective Include strategy.
