const test = require('node:test');
const assert = require('node:assert/strict');
const { createInventory, STORAGE_KEY } = require('./store.js');

function memoryStorage() {
  const data = new Map();
  return {
    getItem: (key) => (data.has(key) ? data.get(key) : null),
    setItem: (key, value) => {
      data.set(key, String(value));
    },
  };
}

test('add menyimpan nama yang dirapikan dan jumlah sebagai angka', () => {
  const inventory = createInventory(memoryStorage());

  const item = inventory.add({ nama: '  Kursi  ', jumlah: '12' });

  assert.equal(item.nama, 'Kursi');
  assert.equal(item.jumlah, 12);
  assert.deepEqual(inventory.list(), [item]);
});

test('add menerima jumlah 0', () => {
  const inventory = createInventory(memoryStorage());

  const item = inventory.add({ nama: 'Pensil', jumlah: 0 });

  assert.equal(item.jumlah, 0);
});

test('setiap barang yang ditambahkan memiliki id berbeda', () => {
  const inventory = createInventory(memoryStorage());

  const first = inventory.add({ nama: 'Meja', jumlah: 1 });
  const second = inventory.add({ nama: 'Meja', jumlah: 1 });

  assert.notEqual(first.id, second.id);
  assert.equal(inventory.list().length, 2);
});

test('add menolak nama kosong atau hanya berisi spasi', () => {
  const inventory = createInventory(memoryStorage());

  assert.throws(() => inventory.add({ nama: '   ', jumlah: 1 }), {
    message: 'Nama barang wajib diisi.',
  });
  assert.deepEqual(inventory.list(), []);
});

test('add menolak nama lebih dari 100 karakter', () => {
  const inventory = createInventory(memoryStorage());

  assert.throws(() => inventory.add({ nama: 'a'.repeat(101), jumlah: 1 }), {
    message: 'Nama barang maksimal 100 karakter.',
  });
});

test('add menolak jumlah yang bukan bilangan bulat 0 atau lebih', () => {
  const inventory = createInventory(memoryStorage());

  for (const jumlah of [-1, 1.5, '', 'abc', null]) {
    assert.throws(() => inventory.add({ nama: 'Pensil', jumlah }), {
      message: 'Jumlah harus bilangan bulat 0 atau lebih.',
    });
  }
  assert.deepEqual(inventory.list(), []);
});

test('update mengganti nama dan jumlah dengan id yang sama', () => {
  const inventory = createInventory(memoryStorage());
  const original = inventory.add({ nama: 'Kursi', jumlah: 3 });

  const updated = inventory.update(original.id, { nama: 'Kursi Lipat', jumlah: 5 });

  assert.deepEqual(updated, { id: original.id, nama: 'Kursi Lipat', jumlah: 5 });
  assert.deepEqual(inventory.list(), [updated]);
});

test('update tidak mengubah barang lain', () => {
  const inventory = createInventory(memoryStorage());
  const kursi = inventory.add({ nama: 'Kursi', jumlah: 3 });
  const meja = inventory.add({ nama: 'Meja', jumlah: 2 });

  inventory.update(kursi.id, { nama: 'Kursi Lipat', jumlah: 4 });

  assert.deepEqual(inventory.list(), [
    { id: kursi.id, nama: 'Kursi Lipat', jumlah: 4 },
    meja,
  ]);
});

test('update menolak id yang tidak ada', () => {
  const inventory = createInventory(memoryStorage());

  assert.throws(() => inventory.update('tidak-ada', { nama: 'Kursi', jumlah: 1 }), {
    message: 'Barang tidak ditemukan.',
  });
});

test('update menolak input tidak valid dan membiarkan data tetap', () => {
  const inventory = createInventory(memoryStorage());
  const kursi = inventory.add({ nama: 'Kursi', jumlah: 3 });

  assert.throws(() => inventory.update(kursi.id, { nama: 'Kursi', jumlah: -2 }), {
    message: 'Jumlah harus bilangan bulat 0 atau lebih.',
  });
  assert.deepEqual(inventory.list(), [kursi]);
});

test('remove menghapus hanya barang yang dipilih', () => {
  const inventory = createInventory(memoryStorage());
  const kursi = inventory.add({ nama: 'Kursi', jumlah: 3 });
  const meja = inventory.add({ nama: 'Meja', jumlah: 2 });

  inventory.remove(kursi.id);

  assert.deepEqual(inventory.list(), [meja]);
});

test('remove menolak id yang tidak ada', () => {
  const inventory = createInventory(memoryStorage());
  inventory.add({ nama: 'Kursi', jumlah: 3 });

  assert.throws(() => inventory.remove('tidak-ada'), {
    message: 'Barang tidak ditemukan.',
  });
  assert.equal(inventory.list().length, 1);
});

test('data rusak di storage dibaca sebagai daftar kosong', () => {
  const storage = memoryStorage();
  storage.setItem(STORAGE_KEY, '{rusak');
  const inventory = createInventory(storage);

  assert.deepEqual(inventory.list(), []);

  inventory.add({ nama: 'Pensil', jumlah: 1 });
  assert.equal(inventory.list().length, 1);
});

test('data tersimpan tetap terbaca oleh instance baru', () => {
  const storage = memoryStorage();
  const item = createInventory(storage).add({ nama: 'Kursi', jumlah: 3 });

  assert.deepEqual(createInventory(storage).list(), [item]);
});
