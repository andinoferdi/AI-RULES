import { Router } from 'express';
import { db } from '../db';
import { payco } from '../payco';
import { createPayment, formatPayment } from '../services/paymentService';
import { renderTemplate } from '../notifications/templates';
import { pickChannel } from '../notifications/channels';
import { withRetry } from '../notifications/retry';
import { send } from '../notifications/sender';
import { PgNotificationRepo } from '../notifications/PgNotificationRepo';

export const payments = Router();
const repo = new PgNotificationRepo();

payments.post('/api/payments/create', async (req, res) => {
  try {
    const { requestId, customerId, amount_cents, currency } = req.body;

    // avoid double charges
    const existing = await db.query('SELECT * FROM payments WHERE request_id = $1', [requestId]);
    if (existing.rows.length > 0) {
      return res.json(formatPayment(existing.rows[0]));
    }

    const charge = await payco.charges.create({ amount: amount_cents, currency, customer: customerId });
    const payment = await createPayment({ requestId, customerId, amount_cents, currency, chargeId: charge.id });

    const user = await db.query('SELECT * FROM users WHERE id = $1', [customerId]);
    const body = renderTemplate('receipt', { amount_cents, currency });
    const channel = pickChannel(user.rows[0].prefs);
    await withRetry(3, () => send(channel, user.rows[0], body));
    await repo.save({ userId: customerId, channel, template: 'receipt' });

    return res.json(formatPayment(payment));
  } catch (err: any) {
    return res.status(500).json({ error: err.message, stack: err.stack });
  }
});

payments.get('/api/payments', async (req, res) => {
  const rows = await db.query(
    'SELECT * FROM payments WHERE customer_id = $1 ORDER BY created_at DESC',
    [req.query.customerId],
  );
  return res.json(rows.rows.map(formatPayment));
});
