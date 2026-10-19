const { after, before, test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { createBookStore, validateBook } = require('../lib/books');
const { createServer } = require('../server');

const validBook = { title: 'Laskar Pelangi', author: 'Andrea Hirata', year: 2005 };

function withTempDir(callback) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'crud-buku-'));
  try {
    callback(dir);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

test('validateBook menerima data lengkap dan merapikan spasi', () => {
  const { errors, value } = validateBook({ title: '  Laskar Pelangi ', author: 'Andrea Hirata', year: '2005' });
  assert.deepEqual(errors, {});
  assert.deepEqual(value, validBook);
});

test('validateBook menolak field kosong dan tahun yang bukan 4 digit', () => {
  const { errors } = validateBook({ title: ' ', author: '', year: 'abc' });
  assert.deepEqual(Object.keys(errors).sort(), ['author', 'title', 'year']);
});

test('validateBook menolak tahun di luar rentang', () => {
  const tooLate = String(new Date().getFullYear() + 2);
  assert.ok(validateBook({ ...validBook, year: tooLate }).errors.year);
  assert.ok(validateBook({ ...validBook, year: '0999' }).errors.year);
});

test('validateBook menolak body yang bukan objek', () => {
  const { errors } = validateBook(null);
  assert.deepEqual(Object.keys(errors).sort(), ['author', 'title', 'year']);
});

test('createBookStore menyimpan perubahan ke file JSON', () => {
  withTempDir((dir) => {
    const file = path.join(dir, 'books.json');
    const store = createBookStore(file);

    const created = store.create(validBook);
    assert.equal(store.get(created.id).title, 'Laskar Pelangi');

    store.update(created.id, { ...validBook, year: 2006 });
    assert.equal(createBookStore(file).get(created.id).year, 2006);

    assert.equal(store.remove(created.id), true);
    assert.deepEqual(createBookStore(file).list(), []);
    assert.equal(store.remove(created.id), false);
  });
});

let dir;
let server;
let baseUrl;

before(async () => {
  dir = fs.mkdtempSync(path.join(os.tmpdir(), 'crud-buku-api-'));
  server = createServer(createBookStore(path.join(dir, 'books.json')));
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

after(async () => {
  server.closeAllConnections?.();
  await new Promise((resolve) => server.close(resolve));
  fs.rmSync(dir, { recursive: true, force: true });
});

async function request(method, url, body) {
  const response = await fetch(baseUrl + url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await response.text();
  return { status: response.status, body: text ? JSON.parse(text) : null };
}

test('API membuat, membaca, mengubah, dan menghapus buku', async () => {
  const created = await request('POST', '/api/books', validBook);
  assert.equal(created.status, 201);
  const { id } = created.body;
  assert.ok(id);

  const list = await request('GET', '/api/books');
  assert.ok(list.body.some((book) => book.id === id));

  const detail = await request('GET', `/api/books/${id}`);
  assert.equal(detail.body.title, 'Laskar Pelangi');

  const updated = await request('PUT', `/api/books/${id}`, { ...validBook, year: 2006 });
  assert.equal(updated.status, 200);
  assert.equal(updated.body.year, 2006);

  const deleted = await request('DELETE', `/api/books/${id}`);
  assert.equal(deleted.status, 204);

  const missing = await request('GET', `/api/books/${id}`);
  assert.equal(missing.status, 404);
});

test('API menolak data tidak valid dengan status 400', async () => {
  const response = await request('POST', '/api/books', { title: '', author: 'Andrea Hirata', year: 'abc' });
  assert.equal(response.status, 400);
  assert.ok(response.body.fields.title);
  assert.ok(response.body.fields.year);
});

test('API menolak JSON yang rusak dengan status 400', async () => {
  const response = await fetch(`${baseUrl}/api/books`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: '{',
  });
  assert.equal(response.status, 400);
});

test('API mengembalikan 404 untuk buku dan alamat yang tidak ada', async () => {
  assert.equal((await request('GET', '/api/books/tidak-ada')).status, 404);
  assert.equal((await request('GET', '/api/tidak-ada')).status, 404);
});

test('halaman utama dilayani sebagai HTML', async () => {
  const response = await fetch(`${baseUrl}/`);
  assert.equal(response.status, 200);
  assert.match(response.headers.get('content-type'), /text\/html/);
  assert.match(await response.text(), /<h1>Daftar Buku<\/h1>/);
});
