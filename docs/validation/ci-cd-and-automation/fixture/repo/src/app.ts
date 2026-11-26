import express from 'express';
import { db } from './db';

export const app = express();
app.use(express.json());

app.get('/healthz', (_req, res) => {
  res.json({ ok: true, sha: process.env.GIT_SHA ?? 'dev' });
});

app.get('/api/customers', async (_req, res) => {
  const { rows } = await db.query('SELECT id, name FROM customers ORDER BY id');
  res.json(rows);
});

app.post('/api/customers', async (req, res) => {
  const { id, name } = req.body;
  const result = await db.query('INSERT INTO customers (id, name) VALUES ($1, $2) ON CONFLICT DO NOTHING', [id, name]);
  res.status(result.rowCount === 1 ? 201 : 409).end();
});

app.delete('/api/customers/:id', async (req, res) => {
  await db.query('DELETE FROM customers WHERE id = $1', [req.params.id]);
  res.status(204).end();
});

app.get('/api/customers/:id/orders', async (req, res) => {
  const { rows } = await db.query('SELECT id, total_cents, notes FROM orders WHERE customer_id = $1', [req.params.id]);
  res.json(rows);
});

app.get('/api/customers/:id/total', async (req, res) => {
  const { rows } = await db.query('SELECT COALESCE(SUM(total_cents), 0)::int AS total_cents FROM orders WHERE customer_id = $1', [req.params.id]);
  res.json(rows[0]);
});
