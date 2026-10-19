(function () {
  const { addItem, updateItem, removeItem, loadItems, saveItems } = window.Inventory;

  const form = document.getElementById('add-form');
  const nameInput = document.getElementById('add-name');
  const qtyInput = document.getElementById('add-qty');
  const table = document.getElementById('items-table');
  const body = document.getElementById('items-body');
  const empty = document.getElementById('empty');
  const summary = document.getElementById('summary');
  const status = document.getElementById('status');

  let items = loadItems(localStorage);
  // Satu baris saja yang boleh sedang diedit atau menunggu konfirmasi hapus.
  let mode = { id: null, kind: null, errors: {} };

  const newId = () =>
    window.crypto && crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`;

  const icon = (path) =>
    `<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="${path}" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"/></svg>`;
  const MINUS = icon('M3.5 8h9');
  const PLUS = icon('M3.5 8h9M8 3.5v9');

  function escapeHtml(text) {
    return String(text).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  }

  function commit(next, message) {
    items = next;
    saveItems(localStorage, items);
    if (message) status.textContent = message;
  }

  function showFieldError(input, errorEl, message) {
    errorEl.textContent = message || '';
    errorEl.hidden = !message;
    input.setAttribute('aria-invalid', message ? 'true' : 'false');
  }

  function rowView(item) {
    const name = escapeHtml(item.name);
    return `
      <tr data-id="${escapeHtml(item.id)}">
        <td class="cell-name">${name}</td>
        <td class="cell-qty">
          <div class="stepper">
            <button type="button" class="btn-icon" data-action="dec" aria-label="Kurangi ${name}" ${item.quantity === 0 ? 'disabled' : ''}>${MINUS}</button>
            <output aria-label="Jumlah ${name}">${item.quantity}</output>
            <button type="button" class="btn-icon" data-action="inc" aria-label="Tambah satu ${name}">${PLUS}</button>
          </div>
        </td>
        <td class="cell-actions">
          <button type="button" class="btn btn-quiet" data-action="edit">Ubah</button>
          <button type="button" class="btn btn-quiet btn-danger-text" data-action="ask-delete">Hapus</button>
        </td>
      </tr>`;
  }

  function editView(item, { errors, draft }) {
    const name = escapeHtml(draft ? draft.name : item.name);
    const quantity = escapeHtml(draft ? draft.quantity : item.quantity);
    const err = (key, id) =>
      errors[key] ? `<p id="${id}" class="error">${escapeHtml(errors[key])}</p>` : '';
    return `
      <tr data-id="${escapeHtml(item.id)}" class="is-editing">
        <td class="cell-name">
          <label class="visually-hidden" for="edit-name">Nama barang</label>
          <input id="edit-name" value="${name}" maxlength="120" aria-invalid="${!!errors.name}" aria-describedby="edit-name-error">
          ${err('name', 'edit-name-error')}
        </td>
        <td class="cell-qty">
          <label class="visually-hidden" for="edit-qty">Jumlah</label>
          <input id="edit-qty" value="${quantity}" inputmode="numeric" aria-invalid="${!!errors.quantity}" aria-describedby="edit-qty-error">
          ${err('quantity', 'edit-qty-error')}
        </td>
        <td class="cell-actions">
          <button type="button" class="btn btn-primary" data-action="save">Simpan</button>
          <button type="button" class="btn btn-quiet" data-action="cancel">Batal</button>
        </td>
      </tr>`;
  }

  function confirmView(item) {
    return `
      <tr data-id="${escapeHtml(item.id)}" class="is-confirming">
        <td class="cell-confirm" colspan="2">Hapus <strong>${escapeHtml(item.name)}</strong> dari inventaris?</td>
        <td class="cell-actions">
          <button type="button" class="btn btn-danger" data-action="delete">Ya, hapus</button>
          <button type="button" class="btn btn-quiet" data-action="cancel">Batal</button>
        </td>
      </tr>`;
  }

  function render(focus) {
    body.innerHTML = items
      .map((item) => {
        if (item.id !== mode.id) return rowView(item);
        return mode.kind === 'edit' ? editView(item, mode) : confirmView(item);
      })
      .join('');

    const hasItems = items.length > 0;
    table.hidden = !hasItems;
    empty.hidden = hasItems;
    const units = items.reduce((sum, item) => sum + item.quantity, 0);
    summary.textContent = hasItems ? `${items.length} jenis barang · ${units} unit total` : '';

    if (focus) {
      const target = typeof focus === 'string' ? body.querySelector(focus) : focus;
      if (target) target.focus();
    }
  }

  const rowSelector = (id, action) => `tr[data-id="${CSS.escape(id)}"] [data-action="${action}"]`;

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const result = addItem(items, { name: nameInput.value, quantity: qtyInput.value }, newId());
    showFieldError(nameInput, document.getElementById('add-name-error'), result.errors.name);
    showFieldError(qtyInput, document.getElementById('add-qty-error'), result.errors.quantity);
    if (result.errors.name) return nameInput.focus();
    if (result.errors.quantity) return qtyInput.focus();

    commit(result.items, `${result.items[result.items.length - 1].name} ditambahkan.`);
    form.reset();
    qtyInput.value = '1';
    render();
    nameInput.focus();
  });

  function saveEdit(id) {
    const nameField = document.getElementById('edit-name');
    const qtyField = document.getElementById('edit-qty');
    const result = updateItem(items, id, { name: nameField.value, quantity: qtyField.value });
    if (Object.keys(result.errors).length) {
      // Pertahankan ketikan user saat validasi gagal.
      mode = { id, kind: 'edit', errors: result.errors, draft: { name: nameField.value, quantity: qtyField.value } };
      render(result.errors.name ? '#edit-name' : '#edit-qty');
      return;
    }
    commit(result.items, 'Perubahan disimpan.');
    mode = { id: null, kind: null, errors: {} };
    render(rowSelector(id, 'edit'));
  }

  body.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-action]');
    if (!button) return;
    const id = button.closest('tr').dataset.id;
    const item = items.find((entry) => entry.id === id);
    const action = button.dataset.action;

    if (action === 'inc' || action === 'dec') {
      const quantity = Math.max(0, item.quantity + (action === 'inc' ? 1 : -1));
      const result = updateItem(items, id, { name: item.name, quantity: String(quantity) });
      commit(result.items, `${item.name}: ${quantity} unit.`);
      // Saat jumlah jadi 0, tombol kurangi nonaktif; pindahkan fokus ke tombol tambah.
      render(rowSelector(id, quantity === 0 ? 'inc' : action));
    } else if (action === 'edit') {
      mode = { id, kind: 'edit', errors: {} };
      render('#edit-name');
    } else if (action === 'ask-delete') {
      mode = { id, kind: 'confirm', errors: {} };
      render(rowSelector(id, 'cancel'));
    } else if (action === 'save') {
      saveEdit(id);
    } else if (action === 'cancel') {
      const back = mode.kind === 'edit' ? 'edit' : 'ask-delete';
      mode = { id: null, kind: null, errors: {} };
      render(rowSelector(id, back));
    } else if (action === 'delete') {
      const index = items.indexOf(item);
      commit(removeItem(items, id), `${item.name} dihapus.`);
      mode = { id: null, kind: null, errors: {} };
      const next = items[index] || items[index - 1];
      render(next ? rowSelector(next.id, 'edit') : nameInput);
    }
  });

  body.addEventListener('keydown', (event) => {
    const row = event.target.closest('tr.is-editing, tr.is-confirming');
    if (!row) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      row.querySelector('[data-action="cancel"]').click();
    } else if (event.key === 'Enter' && event.target.matches('input')) {
      event.preventDefault();
      saveEdit(row.dataset.id);
    }
  });

  render();
})();
