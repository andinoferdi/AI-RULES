const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');

process.env.BOOKS_FILE = path.join(os.tmpdir(), `books-test-${process.pid}.json`);
const { createServer } = require('../server');

let server;
let baseUrl;

before(async () => {
  server = createServer();
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const { port } = server.address();
  baseUrl = `http://127.0.0.1:${port}/api/books`;
});

after(async () => {
  server.closeAllConnections();
  await new Promise((resolve) => server.close(resolve));
  await fs.rm(process.env.BOOKS_FILE, { force: true });
});

async function call(method, url, body) {
  const response = await fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  return { status: response.status, body: text ? JSON.parse(text) : null };
}

test('buku bisa dibuat, dibaca, diubah, dan dihapus', async () => {
  const created = await call('POST', baseUrl, {
    title: 'Laskar Pelangi',
    author: 'Andrea Hirata',
    year: 2005,
  });
  assert.equal(created.status, 201);
  assert.equal(created.body.title, 'Laskar Pelangi');
  const { id } = created.body;

  const list = await call('GET', baseUrl);
  assert.equal(list.status, 200);
  assert.ok(list.body.some((book) => book.id === id));

  const single = await call('GET', `${baseUrl}/${id}`);
  assert.equal(single.status, 200);
  assert.equal(single.body.author, 'Andrea Hirata');

  const updated = await call('PUT', `${baseUrl}/${id}`, {
    title: 'Laskar Pelangi',
    author: 'Andrea Hirata',
    year: 2006,
  });
  assert.equal(updated.status, 200);
  assert.equal(updated.body.year, 2006);

  const deleted = await call('DELETE', `${baseUrl}/${id}`);
  assert.equal(deleted.status, 204);

  const missing = await call('GET', `${baseUrl}/${id}`);
  assert.equal(missing.status, 404);
});

test('input tidak valid ditolak dengan status 400', async () => {
  const response = await call('POST', baseUrl, {
    title: '',
    author: 'Tanpa Judul',
    year: 'abc',
  });
  assert.equal(response.status, 400);
  assert.equal(response.body.errors.length, 2);
});
