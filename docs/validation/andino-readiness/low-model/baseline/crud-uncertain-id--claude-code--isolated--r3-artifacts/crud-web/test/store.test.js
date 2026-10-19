const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const { createBookStore } = require('../src/store');

const sample = { title: 'Bumi', author: 'Tere Liye', year: 2014 };

async function withDataFile(run) {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'crud-buku-'));
  try {
    await run(path.join(dir, 'books.json'));
  } finally {
    await fs.rm(dir, { recursive: true, force: true });
  }
}

test('buku yang dibuat bisa dibaca lagi dari file', () =>
  withDataFile(async (file) => {
    const created = await createBookStore(file).create(sample);

    assert.match(created.id, /^[0-9a-f-]{36}$/);
    assert.deepEqual(await createBookStore(file).get(created.id), created);
  }));

test('ubah mengganti isi buku dan mempertahankan id', () =>
  withDataFile(async (file) => {
    const store = createBookStore(file);
    const book = await store.create(sample);

    const updated = await store.update(book.id, { title: 'Bulan', author: 'Tere Liye', year: 2015 });

    assert.deepEqual(updated, { id: book.id, title: 'Bulan', author: 'Tere Liye', year: 2015 });
    assert.deepEqual(await store.get(book.id), updated);
  }));

test('hapus menghilangkan buku dari daftar', () =>
  withDataFile(async (file) => {
    const store = createBookStore(file);
    const keep = await store.create(sample);
    const drop = await store.create({ ...sample, title: 'Bulan' });

    assert.equal(await store.remove(drop.id), true);
    assert.deepEqual(await store.list(), [keep]);
  }));

test('ubah dan hapus untuk id yang tidak ada tidak mengubah data', () =>
  withDataFile(async (file) => {
    const store = createBookStore(file);
    await store.create(sample);

    assert.equal(await store.update('tidak-ada', sample), null);
    assert.equal(await store.remove('tidak-ada'), false);
    assert.equal((await store.list()).length, 1);
  }));

test('penulisan paralel tidak saling menimpa', () =>
  withDataFile(async (file) => {
    const store = createBookStore(file);
    await Promise.all([
      store.create({ ...sample, title: 'A' }),
      store.create({ ...sample, title: 'B' }),
      store.create({ ...sample, title: 'C' }),
    ]);

    const saved = JSON.parse(await fs.readFile(file, 'utf8'));
    assert.deepEqual(saved.map((book) => book.title).sort(), ['A', 'B', 'C']);
  }));
