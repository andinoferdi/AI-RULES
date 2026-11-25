import { db } from '../db';
import { renderTemplate } from '../notifications/templates';
import { pickChannel } from '../notifications/channels';
import { withRetry } from '../notifications/retry';
import { send } from '../notifications/sender';

// Runs hourly. Reminds customers whose payment failed.
export async function runDunning(): Promise<void> {
  const failed = await db.query(
    "SELECT p.*, u.* FROM payments p JOIN users u ON u.id = p.customer_id WHERE p.status = 'failed'",
  );
  for (const row of failed.rows) {
    const body = renderTemplate('dunning', {});
    const channel = pickChannel(row.prefs);
    await withRetry(5, () => send(channel, row, body));
    // TODO: record the notification like the other callers do
  }
}
