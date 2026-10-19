const test = require('node:test');
const assert = require('node:assert/strict');
const { addItem, updateItem, removeItem, loadItems, saveItems } = require('./inventory.js');

test('tambah barang baru dengan nama dirapikan dan jumlah angka', () => {
  const result = addItem([], { name: '  Kabel   HDMI ', quantity: '12' }, 'a1');
  assert.deepEqual(result.errors, {});
  assert.deepEqual(result.items, [{ id: 'a1', name: 'Kabel HDMI', quantity: 12 }]);
});

test('tolak nama kosong dan jumlah bukan bilangan bulat >= 0', () => {
  for (const quantity of ['', '-1', '2.5', 'abc']) {
    const result = addItem([], { name: '   ', quantity }, 'a1');
    assert.equal(result.items.length, 0);
    assert.ok(result.errors.name, 'nama harus error');
    assert.ok(result.errors.quantity, `jumlah "${quantity}" harus error`);
  }
});

test('jumlah 0 diterima', () => {
  const result = addItem([], { name: 'Spidol', quantity: '0' }, 'a1');
  assert.deepEqual(result.errors, {});
  assert.equal(result.items[0].quantity, 0);
});

test('tolak nama duplikat tanpa membedakan huruf besar kecil', () => {
  const items = [{ id: 'a1', name: 'Kabel HDMI', quantity: 3 }];
  const result = addItem(items, { name: 'kabel hdmi', quantity: '1' }, 'a2');
  assert.equal(result.items, items);
  assert.ok(result.errors.name);
});

test('ubah barang hanya mengganti item dengan id yang sama', () => {
  const items = [
    { id: 'a1', name: 'Kabel HDMI', quantity: 3 },
    { id: 'a2', name: 'Mouse', quantity: 5 },
  ];
  const result = updateItem(items, 'a1', { name: 'Kabel HDMI 2m', quantity: '7' });
  assert.deepEqual(result.errors, {});
  assert.deepEqual(result.items, [
    { id: 'a1', name: 'Kabel HDMI 2m', quantity: 7 },
    { id: 'a2', name: 'Mouse', quantity: 5 },
  ]);
  assert.deepEqual(items[0], { id: 'a1', name: 'Kabel HDMI', quantity: 3 }, 'array asli tidak berubah');
});

test('ubah boleh mempertahankan nama sendiri tapi tidak memakai nama barang lain', () => {
  const items = [
    { id: 'a1', name: 'Kabel HDMI', quantity: 3 },
    { id: 'a2', name: 'Mouse', quantity: 5 },
  ];
  assert.deepEqual(updateItem(items, 'a1', { name: 'KABEL HDMI', quantity: '4' }).errors, {});
  assert.ok(updateItem(items, 'a1', { name: 'mouse', quantity: '4' }).errors.name);
});

test('hapus barang berdasarkan id', () => {
  const items = [
    { id: 'a1', name: 'Kabel HDMI', quantity: 3 },
    { id: 'a2', name: 'Mouse', quantity: 5 },
  ];
  assert.deepEqual(removeItem(items, 'a1'), [{ id: 'a2', name: 'Mouse', quantity: 5 }]);
});

test('simpan lalu muat ulang dari storage, data rusak dianggap kosong', () => {
  const store = new Map();
  const storage = { getItem: (k) => store.get(k) ?? null, setItem: (k, v) => store.set(k, v) };
  const items = [{ id: 'a1', name: 'Mouse', quantity: 5 }];
  saveItems(storage, items);
  assert.deepEqual(loadItems(storage), items);

  storage.setItem('inventaris.v1', '{bukan json');
  assert.deepEqual(loadItems(storage), []);
});
