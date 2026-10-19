const { test } = require('node:test');
const assert = require('node:assert/strict');
const { validateBook } = require('../src/validate');

test('menerima buku lengkap dan merapikan spasi di sekitar teks', () => {
  const result = validateBook({ title: '  Laskar Pelangi ', author: ' Andrea Hirata', year: '2005' });

  assert.deepEqual(result, {
    ok: true,
    value: { title: 'Laskar Pelangi', author: 'Andrea Hirata', year: 2005 },
  });
});

test('menolak judul dan penulis yang kosong atau hanya spasi', () => {
  const result = validateBook({ title: '   ', author: '', year: 2005 });

  assert.equal(result.ok, false);
  assert.deepEqual(Object.keys(result.errors).sort(), ['author', 'title']);
});

test('menolak tahun yang bukan bilangan bulat atau di luar rentang', () => {
  const nextYear = new Date().getFullYear() + 1;

  for (const year of ['', 'abc', 12.5, 999, nextYear]) {
    const result = validateBook({ title: 'Judul', author: 'Penulis', year });
    assert.ok(result.errors?.year, `tahun ${year} seharusnya ditolak`);
  }
});

test('menolak judul yang melebihi 200 karakter', () => {
  const result = validateBook({ title: 'a'.repeat(201), author: 'Penulis', year: 2005 });

  assert.ok(result.errors.title);
});

test('menolak input yang bukan objek', () => {
  assert.equal(validateBook(null).ok, false);
  assert.equal(validateBook('teks').ok, false);
});
