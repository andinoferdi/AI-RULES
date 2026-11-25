import express, { Router } from 'express';
import { db } from '../db';
import { renderTemplate } from '../notifications/templates';
import { pickChannel } from '../notifications/channels';
import { withRetry } from '../notifications/retry';
import { send } from '../notifications/sender';
import { PgNotificationRepo } from '../notifications/PgNotificationRepo';

export const webhooks = Router();
const repo = new PgNotificationRepo();

webhooks.post('/webhooks/payco', express.json(), async (req, res) => {
  const event = req.body;

  if (event.type === 'charge.succeeded') {
    await db.query("UPDATE payments SET status = 'paid' WHERE charge_id = $1", [event.data.id]);
    const p = await db.query('SELECT * FROM payments WHERE charge_id = $1', [event.data.id]);
    const user = await db.query('SELECT * FROM users WHERE id = $1', [p.rows[0].customer_id]);
    const body = renderTemplate('paid', { amount_cents: event.data.amount });
    const channel = pickChannel(user.rows[0].prefs);
    await withRetry(3, () => send(channel, user.rows[0], body));
    await repo.save({ userId: user.rows[0].id, channel, template: 'paid' });
  }

  if (event.type === 'charge.failed') {
    await db.query("UPDATE payments SET status = 'failed' WHERE charge_id = $1", [event.data.id]);
  }

  res.sendStatus(200);
});
