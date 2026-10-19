// Logika CRUD murni: dipakai app.js di browser dan inventory.test.js di Node.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.Inventory = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const STORAGE_KEY = 'inventaris.v1';

  function normalizeName(value) {
    return String(value ?? '').trim().replace(/\s+/g, ' ');
  }

  function parseQuantity(value) {
    const text = String(value ?? '').trim();
    if (!/^\d+$/.test(text)) return null;
    const number = Number(text);
    return Number.isSafeInteger(number) ? number : null;
  }

  function validate(items, input, ownId) {
    const name = normalizeName(input.name);
    const quantity = parseQuantity(input.quantity);
    const errors = {};

    if (!name) {
      errors.name = 'Nama barang wajib diisi.';
    } else if (items.some((item) => item.id !== ownId && item.name.toLowerCase() === name.toLowerCase())) {
      errors.name = `"${name}" sudah ada. Ubah jumlahnya saja.`;
    }
    if (quantity === null) {
      errors.quantity = 'Jumlah harus bilangan bulat 0 atau lebih.';
    }
    return { errors, name, quantity };
  }

  function addItem(items, input, id) {
    const { errors, name, quantity } = validate(items, input, null);
    if (Object.keys(errors).length) return { items, errors };
    return { items: [...items, { id, name, quantity }], errors };
  }

  function updateItem(items, id, input) {
    const { errors, name, quantity } = validate(items, input, id);
    if (Object.keys(errors).length) return { items, errors };
    return {
      items: items.map((item) => (item.id === id ? { ...item, name, quantity } : item)),
      errors,
    };
  }

  function removeItem(items, id) {
    return items.filter((item) => item.id !== id);
  }

  function loadItems(storage) {
    try {
      const data = JSON.parse(storage.getItem(STORAGE_KEY) ?? '[]');
      if (!Array.isArray(data)) return [];
      return data.filter(
        (item) => item && typeof item.id === 'string' && typeof item.name === 'string' && Number.isSafeInteger(item.quantity),
      );
    } catch {
      return [];
    }
  }

  function saveItems(storage, items) {
    storage.setItem(STORAGE_KEY, JSON.stringify(items));
  }

  return { addItem, updateItem, removeItem, loadItems, saveItems, parseQuantity };
});
