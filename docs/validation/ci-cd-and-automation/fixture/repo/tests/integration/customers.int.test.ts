import request from 'supertest';
import { beforeEach, describe, expect, it } from 'vitest';
import { app } from '../../src/app';
import { db } from '../../src/db';

describe('customers API', () => {
  beforeEach(async () => {
    await db.query('TRUNCATE customers, orders RESTART IDENTITY CASCADE');
  });

  it('creates a customer', async () => {
    const res = await request(app).post('/api/customers').send({ id: 'c-new', name: 'New Customer' });
    expect(res.status).toBe(201);
  });

  it('rejects a duplicate id', async () => {
    await request(app).post('/api/customers').send({ id: 'c-dup', name: 'First' });
    const res = await request(app).post('/api/customers').send({ id: 'c-dup', name: 'Second' });
    expect(res.status).toBe(409);
  });

  it('lists customers', async () => {
    await request(app).post('/api/customers').send({ id: 'c-a', name: 'A' });
    const res = await request(app).get('/api/customers');
    expect(res.body).toEqual([{ id: 'c-a', name: 'A' }]);
  });

  it('deletes a customer', async () => {
    await request(app).post('/api/customers').send({ id: 'c-del', name: 'Gone' });
    const res = await request(app).delete('/api/customers/c-del');
    expect(res.status).toBe(204);
  });
});
