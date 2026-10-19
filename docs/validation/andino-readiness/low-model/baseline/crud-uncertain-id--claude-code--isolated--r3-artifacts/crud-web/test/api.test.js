const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const { createAppServer } = require('../src/server');

let server;
let baseUrl;
let dir;

before(async () => {
  dir = await fs.mkdtemp(path.join(os.tmpdir(), 'crud-buku-api-'));
  server = createAppServer({ dataFile: path.join(dir, 'books.json') });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

after(async () => {
  server.closeAllConnections?.();
  await new Promise((resolve) => server.close(resolve));
  await fs.rm(dir, { recursive: true, force: true });
});

function request(method, url, body) {
  return fetch(`${baseUrl}${url}`, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}

test('halaman utama dilayani sebagai HTML', async () => {
  const response = await request('GET', '/');

  assert.equal(response.status, 200);
  assert.match(response.headers.get('content-type'), /text\/html/);
  assert.match(await response.text(), /Daftar Buku/);
});

test('buku bisa dibuat, dibaca, diubah, lalu dihapus lewat API', async () => {
  const created = await request('POST', '/api/books', { title: 'Bumi', author: 'Tere Liye', year: 2014 });
  assert.equal(created.status, 201);
  const book = await created.json();

  assert.deepEqual(await (await request('GET', '/api/books')).json(), [book]);
  assert.deepEqual(await (await request('GET', `/api/books/${book.id}`)).json(), book);

  const updated = await request('PUT', `/api/books/${book.id}`, { title: 'Bulan', author: 'Tere Liye', year: 2015 });
  assert.equal(updated.status, 200);
  assert.equal((await updated.json()).title, 'Bulan');

  const removed = await request('DELETE', `/api/books/${book.id}`);
  assert.equal(removed.status, 204);
  assert.deepEqual(await (await request('GET', '/api/books')).json(), []);
});

test('data tidak valid ditolak dengan 422 dan id tidak dikenal dengan 404', async () => {
  const invalid = await request('POST', '/api/books', { title: '', author: 'Penulis', year: 1 });
  assert.equal(invalid.status, 422);
  const { errors } = await invalid.json();
  assert.ok(errors.title);
  assert.ok(errors.year);

  const missing = await request('GET', '/api/books/tidak-ada');
  assert.equal(missing.status, 404);
  assert.ok((await missing.json()).error);
});

test('JSON yang rusak ditolak dengan 400', async () => {
  const response = await fetch(`${baseUrl}/api/books`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: '{bukan json',
  });

  assert.equal(response.status, 400);
});
