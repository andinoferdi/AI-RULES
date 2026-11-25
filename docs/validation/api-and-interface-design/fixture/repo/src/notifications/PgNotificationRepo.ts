import { db } from '../db';
import type { INotificationRepo, NotificationRecord } from './INotificationRepo';

export class PgNotificationRepo implements INotificationRepo {
  async save(record: NotificationRecord): Promise<void> {
    await db.query(
      'INSERT INTO notifications (user_id, channel, template) VALUES ($1, $2, $3)',
      [record.userId, record.channel, record.template],
    );
  }
}
