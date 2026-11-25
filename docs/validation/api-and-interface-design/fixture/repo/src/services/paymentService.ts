import { db } from '../db';

export async function createPayment(input: any) {
  if (!input.amount_cents || input.amount_cents <= 0) throw new Error('amount must be positive');
  if (typeof input.currency !== 'string') throw new Error('currency required');
  const res = await db.query(
    `INSERT INTO payments (request_id, customer_id, amount_cents, currency, charge_id, status)
     VALUES ($1, $2, $3, $4, $5, 'pending') RETURNING *`,
    [input.requestId, input.customerId, input.amount_cents, input.currency, input.chargeId],
  );
  return res.rows[0];
}

// Rows come from our own payments table.
export function formatPayment(row: any) {
  if (!row || typeof row.amount_cents !== 'number') throw new Error('bad payment row');
  if (!['pending', 'paid', 'failed'].includes(row.status)) throw new Error('bad status');
  return { ...row };
}
