// src/refunds/refund.ts
import { pool } from "../db";
import * as ledger from "../ledger/ledger";
import { Money } from "../money/money";

export async function refundInvoice(invoiceId: string, amount: Money): Promise<string> {
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const inv = await client.query(
      "SELECT i.amount_cents, s.customer_id FROM invoices i JOIN subscriptions s ON s.id = i.subscription_id WHERE i.id = $1",
      [invoiceId],
    );
    if (inv.rowCount === 0) throw new Error(`invoice ${invoiceId} not found`);
    const { amount_cents, customer_id } = inv.rows[0];
    if (amount.cents > amount_cents) throw new Error("refund exceeds invoice amount");

    await client.query("SELECT id FROM customers WHERE id = $1 FOR UPDATE", [customer_id]);
    const r = await client.query(
      "INSERT INTO refunds (invoice_id, amount_cents) VALUES ($1, $2) RETURNING id",
      [invoiceId, amount.cents],
    );
    await ledger.write(client, { customerId: customer_id, refundId: r.rows[0].id, amount, kind: "refund" });
    await client.query("COMMIT");
    return r.rows[0].id;
  } catch (err) {
    await client.query("ROLLBACK");
    throw err;
  } finally {
    client.release();
  }
}
