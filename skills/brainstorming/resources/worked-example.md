# End-to-End Brainstorming & Grilling Worked Example

Internal resource for `andino-brainstorming`. Demonstrates an end-to-end scenario elevating a vague, buzzword-heavy request into a builder-ready specification, in-flight ADR, and domain glossary.

---

## Scenario Context

- **User**: "We need to make our project search engine scalable and flexible for new multi-tenant enterprise customers."
- **Current Codebase**: Single-tenant SQLite with basic SQL `LIKE` queries.
- **Problem**: "Scalable" and "flexible" are buzzwords hiding massive architectural divergence (Elasticsearch cluster vs. PostgreSQL tsvector vs. SQLite FTS5 with tenant schemas).

---

## Turn 1: Intent Hypothesis & Buzzword Challenge

**Agent**:
> **Intent Hypothesis (Confidence: 45%)**: You want multi-tenant data isolation and faster search queries as new customers onboard, but tenant scale, isolation boundaries, and query latency requirements are currently unknown.
>
> To design the right architecture without over-engineering:
>
> 1. **De-buzzwording "Scalable"**: Are we expecting 10 enterprise tenants with 10M records each (requiring distributed indexing), or 500 small tenants with 50k records each (where single-node indexing suffices)?
>
> **Recommended default**: Based on our current codebase and infrastructure, I assume we are targeting up to 100 tenants with ~100k records each over the next 12 months.
>
> *Path Classification*: This is **Architectural** because it alters data isolation and search indexing boundaries.
>
> Do you confirm this scale target, or is your tenant volume higher?

**User**:
> "Definitely under 100 tenants with maybe 50k docs each for now. We don't have k8s or a dedicated ops team, so no heavyweight Java clusters like Elasticsearch."

---

## Turn 2: Frontier Grilling with Reasoned Default

**Agent**:
> Tenant volume (<100 tenants, 50k docs) and operational constraint (zero dedicated ops, no Elasticsearch) are locked.
>
> The next unblocked frontier node on our Decision DAG is **Tenant Isolation vs. Query Performance**:
>
> 1. **Option A (Shared Database with `tenant_id` filtering)**: Low ops, single database, shared SQLite/Postgres FTS5 index. Low blast-radius isolation depends on query filters.
> 2. **Option B (Database-per-tenant isolation)**: Hard cryptographic filesystem boundary per tenant, zero risk of data leakage, trivial tenant backup/deletion, but cross-tenant analytics are impossible.
>
> **Recommended default**: I recommend **Option B (Database-per-tenant SQLite with FTS5)**. In our existing architecture, SQLite databases are zero-cost files, giving enterprise customers strict tenant isolation without any database server overhead.
>
> Does Database-per-tenant SQLite fit your operational model, or do you need cross-tenant queries?

**User**:
> "Database-per-tenant SQLite is genius for us. We never query across tenants. Let's do that."

---

## Turn 3: Edge Case & Termination Check

**Agent**:
> Data isolation locked: Database-per-tenant SQLite with local FTS5 indexing.
>
> The final decision frontier node is **Tenant Provisioning & Migration**:
>
> How should tenant database schema migrations be synchronized when the application updates?
>
> **Recommended default**: Apply embedded migrations lazily on tenant database connection open (with schema version pragma check). It avoids central migration bottlenecks and handles dormant tenants transparently.
>
> Can I proceed with this migration approach?

**User**:
> "Yes, that's simple and reliable."

---

## Turn 4: Predictability Termination & Artifact Emission

**Agent**:
> **Termination Trigger**: 3-Question Predictability Reached (>95% confidence). The architectural direction, storage engine, isolation boundary, and migration lifecycle are fully resolved.
>
> Emitting the agreed **Builder-Ready Design Specification**, **ADR-0001**, and **Domain Glossary**:

```markdown
# Architectural Specification: Multi-Tenant Search Engine

## 1. Overview & Business Goal
Provide enterprise-grade search capabilities for up to 100 tenants (each ~50k documents) with zero dedicated infrastructure ops overhead and guaranteed tenant data isolation.

## 2. Architecture & Components
- **Storage & Indexing**: Database-per-tenant SQLite database located at `data/tenants/{tenant_id}/search.db`.
- **Search Engine**: SQLite FTS5 virtual tables (`documents_fts`) with BM25 ranking.
- **Connection Manager**: `TenantSearchPool` cache maintaining LRU open connections to active tenant DBs.
- **Migration Engine**: Lazy pragmas on connection acquisition (`PRAGMA user_version`).

## 3. Floor Invariants (Hard Non-Negotiables)
1. Under NO circumstances may a query execute without an authenticated, validated `tenant_id`.
2. Cross-tenant reads are structurally impossible (no shared SQLite database file).
3. Database files must be created with `0600` POSIX permissions.

## 4. ADR-0001: Database-per-Tenant SQLite Architecture
- **Status**: Accepted
- **Context**: Need multi-tenant search for <=100 tenants with <50k docs each, with no dedicated ops team or heavyweight clusters.
- **Decision**: Adopt database-per-tenant SQLite with native FTS5 full-text indexing.
- **Alternatives Rejected**:
  - Elasticsearch / Opensearch: Rejected due to operational complexity and lack of k8s cluster.
  - Shared DB with `tenant_id` column: Rejected due to enterprise data co-mingling risk.
- **Consequences**: Strict tenant isolation achieved; zero server operational overhead. Cross-tenant aggregation is not supported by design.

## 5. Domain Glossary
| Domain Term | Canonical Definition | Anti-Terms | Code Identifier |
|---|---|---|---|
| **Tenant DB** | Isolated SQLite database file holding a single tenant's search index. | "Main DB", "Shared Index" | `data/tenants/{tenant_id}/search.db` |
| **Tenant Pool** | Thread-safe LRU cache managing active tenant SQLite handles. | "Connection Pool", "Server" | `TenantSearchPool` |
| **FTS Index** | SQLite FTS5 virtual table indexing document title and body. | "Cluster", "ES Index" | `documents_fts` |

## 6. Handoff to Implementation
- Next Phase: Invoke `andino-planning` to break down `TenantSearchPool`, FTS5 schema migration, and repository query interfaces.
```

---

## Anti-Pattern Contrast: What We Prevented

| Typical AI Assistant Failure | Elevated `andino-brainstorming` Behavior |
|---|---|
| Immediately spits out 500 lines of Elasticsearch Docker Compose code. | Challenges the user's operational constraints; learns they have no ops team and avoids Elasticsearch completely. |
| Recites an exhaustive 10-question checklist all at once. | Asks exactly 1 question on the unblocked frontier, pairing it with a high-conviction recommended default. |
| Lets "scalable and flexible" pass without definition. | Decomposes buzzwords into exact numbers (100 tenants, 50k docs) and concrete failure limits. |
| Starts writing production code before the user approves the architecture. | Hard pre-implementation gate: stops and presents design, ADR, and glossary for explicit user consensus. |
