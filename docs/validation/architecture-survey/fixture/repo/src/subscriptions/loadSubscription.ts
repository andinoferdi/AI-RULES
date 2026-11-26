// src/subscriptions/loadSubscription.ts
import { pool } from "../db";
import { Subscription } from "../types";

function toSubscription(row: any): Subscription {
  return {
    id: row.id,
    customerId: row.customer_id,
    email: row.email,
    customerCountry: row.country,
    planId: row.plan_id,
    status: row.status,
    cancelAtPeriodEnd: row.cancel_at_period_end,
    currentPeriodStart: row.current_period_start,
    currentPeriodEnd: row.current_period_end,
    pausedDays: row.paused_days ?? 0,
  };
}

export async function loadSubscription(id: string): Promise<Subscription> {
  const r = await pool.query(
    "SELECT s.*, c.email, c.country FROM subscriptions s JOIN customers c ON c.id = s.customer_id WHERE s.id = $1",
    [id],
  );
  if (r.rowCount === 0) throw new Error(`subscription ${id} not found`);
  return toSubscription(r.rows[0]);
}

export async function findDueSubscriptions(now: Date): Promise<Subscription[]> {
  const r = await pool.query(
    "SELECT s.*, c.email, c.country FROM subscriptions s JOIN customers c ON c.id = s.customer_id WHERE s.current_period_end <= $1",
    [now],
  );
  return r.rows.map(toSubscription);
}
