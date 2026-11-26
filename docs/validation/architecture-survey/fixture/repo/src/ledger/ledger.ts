// src/ledger/ledger.ts
import { PoolClient } from "../db";
import { Money } from "../money/money";

export interface LedgerEntryInput {
  customerId: string;
  invoiceId?: string;
  refundId?: string;
  amount: Money;
  kind: "renewal" | "refund" | "plan_change";
}

/**
 * Append a ledger entry. Pass the client of the caller's open database transaction so the entry
 * commits or rolls back together with the caller's own writes, and lock the customer's rows first
 * (SELECT ... FOR UPDATE on customers) or two writers can compute the same balance.
 */
export async function write(client: PoolClient, entry: LedgerEntryInput): Promise<void> {
  const balance = await balanceAfter(client, entry.customerId);
  const signed = entry.kind === "refund" ? -entry.amount.cents : entry.amount.cents;
  await client.query(
    `INSERT INTO ledger_entries (customer_id, invoice_id, refund_id, kind, amount_cents, balance_after_cents)
     VALUES ($1, $2, $3, $4, $5, $6)`,
    [entry.customerId, entry.invoiceId ?? null, entry.refundId ?? null, entry.kind, signed, balance + signed],
  );
}

/** Current balance as seen inside the caller's transaction. */
export async function balanceAfter(client: PoolClient, customerId: string): Promise<number> {
  const r = await client.query(
    "SELECT COALESCE(SUM(amount_cents), 0) AS balance FROM ledger_entries WHERE customer_id = $1",
    [customerId],
  );
  return Number(r.rows[0].balance);
}
