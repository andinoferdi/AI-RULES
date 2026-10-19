const STORAGE_KEY = 'inventaris.barang';
const NAMA_MAKSIMAL = 100;

function validate(input) {
  const nama = String(input.nama ?? '').trim();
  const teksJumlah = String(input.jumlah ?? '').trim();
  const jumlah = Number(teksJumlah);

  if (nama === '') return 'Nama barang wajib diisi.';
  if (nama.length > NAMA_MAKSIMAL) return `Nama barang maksimal ${NAMA_MAKSIMAL} karakter.`;
  if (teksJumlah === '' || !Number.isInteger(jumlah) || jumlah < 0) {
    return 'Jumlah harus bilangan bulat 0 atau lebih.';
  }
  return null;
}

function createId() {
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

function toItem(input) {
  const error = validate(input);
  if (error) throw new Error(error);
  return { nama: String(input.nama).trim(), jumlah: Number(input.jumlah) };
}

function createInventory(storage) {
  function readAll() {
    try {
      const items = JSON.parse(storage.getItem(STORAGE_KEY) ?? '[]');
      return Array.isArray(items) ? items : [];
    } catch {
      return [];
    }
  }

  function writeAll(items) {
    storage.setItem(STORAGE_KEY, JSON.stringify(items));
  }

  return {
    list() {
      return readAll();
    },

    add(input) {
      const item = { id: createId(), ...toItem(input) };
      writeAll([...readAll(), item]);
      return item;
    },

    update(id, input) {
      const items = readAll();
      const index = items.findIndex((item) => item.id === id);
      if (index === -1) throw new Error('Barang tidak ditemukan.');

      const item = { id, ...toItem(input) };
      items[index] = item;
      writeAll(items);
      return item;
    },

    remove(id) {
      const items = readAll();
      if (!items.some((item) => item.id === id)) throw new Error('Barang tidak ditemukan.');

      writeAll(items.filter((item) => item.id !== id));
    },
  };
}

const api = { createInventory, STORAGE_KEY };

if (typeof module !== 'undefined') module.exports = api;
if (typeof window !== 'undefined') window.Inventaris = api;
