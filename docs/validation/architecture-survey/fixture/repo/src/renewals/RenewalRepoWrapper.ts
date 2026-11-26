// src/renewals/RenewalRepoWrapper.ts
import { pool, PoolClient } from "../db";
import { Money } from "../money/money";

export class RenewalRepoWrapper {
  async begin(): Promise<PoolClient> {
    const client = await pool.connect();
    await client.query("BEGIN");
    return client;
  }

  async insertInvoice(client: PoolClient, subscriptionId: string, amount: Money): Promise<string> {
    const r = await client.query(
      "INSERT INTO invoices (subscription_id, amount_cents) VALUES ($1, $2) RETURNING id",
      [subscriptionId, amount.cents],
    );
    return r.rows[0].id;
  }

  async advancePeriod(client: PoolClient, subscriptionId: string): Promise<void> {
    await client.query(
      "UPDATE subscriptions SET current_period_start = current_period_end, current_period_end = current_period_end + interval '1 month', paused_days = 0 WHERE id = $1",
      [subscriptionId],
    );
  }

  async commit(client: PoolClient): Promise<void> {
    try {
      await client.query("COMMIT");
    } finally {
      client.release();
    }
  }

  async rollback(client: PoolClient): Promise<void> {
    try {
      await client.query("ROLLBACK");
    } finally {
      client.release();
    }
  }
}
