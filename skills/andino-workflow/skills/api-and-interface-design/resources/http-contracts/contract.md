# HTTP contracts

Resource contract; selected directly under its canonical owner.

> **Andino Workflow Member Skill**
> Operates under Andino Workflow: proportional investigation, evidence-based
> decisions, one durable checkpoint and clean handoff. Do not invoke the workflow
> recursively. Loading this resource changes neither tools nor permissions.

## Purpose and selection

Supply the transport detail and code for HTTP, GraphQL or RPC interfaces designed with the
parent [api-and-interface-design](../../SKILL.md) procedure.

Activate for: routes and filtering, bounded collections, PUT and PATCH, status codes and
the error body, an idempotency-key implementation, webhook or event consumers, agent tool
schemas, deprecation headers.

Do not activate for: an in-process module interface (`module-depth`), TypeScript import
rules (`import-enforcement`), or a private rename with no consumer.

## Inputs

The parent procedure's consumer table and change classification, the project's existing
error shape, validation library and database, and the provider contracts (deduplication
window, webhook signing, retry schedule) the interface depends on.

## Procedure

1. Run the parent procedure; it owns consumer mapping, change classification and the rules
   for every interface.
2. Open the section of [the guide](guide.md) the current decision needs: resource modeling
   (§1), bounded collections (§2), PUT and PATCH (§3), errors (§4), edge validation (§5),
   idempotency implementation (§6), webhooks and event consumers (§7), agent tools (§8),
   deprecation headers (§9).
3. Adapt the code to the project's actual store and framework. A store that cannot enforce
   uniqueness in one operation cannot back an idempotency key; document the operation as
   unsafe to retry instead.

## Outputs and verification

The parent skill's design note with transport detail filled in. Check, where they apply:
N concurrent requests with one key produce one effect; a changed body with the same key gets
422; a duplicate while the first runs gets 409; a timeout leaves an `unknown` record that
reconciliation resolves; a replayed webhook changes state once; existing consumers still
parse every response.
