export interface NotificationRecord {
  userId: number;
  channel: string;
  template: string;
}

// Added "in case we move off Postgres". PgNotificationRepo is the only implementation.
export interface INotificationRepo {
  save(record: NotificationRecord): Promise<void>;
}
