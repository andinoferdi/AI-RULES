// src/db.ts
import { Pool, PoolClient } from "pg";

export const pool = new Pool({ connectionString: process.env.DATABASE_URL });
export type { PoolClient };
