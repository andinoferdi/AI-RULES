import pg from 'pg';

export const db = new pg.Pool({ connectionString: process.env.DATABASE_URL });

// DEBUG_SQL=1 prints each statement with the Vitest worker id and a timestamp.
if (process.env.DEBUG_SQL === '1') {
  const query = db.query.bind(db) as (...args: unknown[]) => Promise<unknown>;
  db.query = ((text: string, ...rest: unknown[]) => {
    const time = new Date().toISOString().slice(11, 23);
    console.log(`[sql w${process.env.VITEST_POOL_ID ?? '-'} ${time}] ${text}`);
    return query(text, ...rest);
  }) as typeof db.query;
}
