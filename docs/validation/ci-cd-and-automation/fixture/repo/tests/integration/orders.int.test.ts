import request from 'supertest';
import { beforeAll, describe, expect, it } from 'vitest';
import { app } from '../../src/app';
import { db } from '../../src/db';

describe('orders API', () => {
  beforeAll(async () => {
    await db.query("INSERT INTO customers (id, name) VALUES ('c-orders', 'Orders Fixture') ON CONFLICT DO NOTHING");
    await db.query(
      "INSERT INTO orders (customer_id, total_cents) VALUES ('c-orders', 1000), ('c-orders', 1500), ('c-orders', 2000)",
    );
  });

  it('returns an empty list for an unknown customer', async () => {
    const res = await request(app).get('/api/customers/nobody/orders');
    expect(res.status).toBe(200);
    expect(res.body).toEqual([]);
  });

  it("lists a customer's orders", async () => {
    const res = await request(app).get('/api/customers/c-orders/orders');
    expect(res.status).toBe(200);
    expect(res.body).toHaveLength(3);
  });

  it('computes the order total', async () => {
    const res = await request(app).get('/api/customers/c-orders/total');
    expect(res.body.total_cents).toBe(4500);
  });
});
