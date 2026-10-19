(function () {
  const inventory = Inventaris.createInventory(window.localStorage);

  const form = document.getElementById('form-barang');
  const inputNama = document.getElementById('nama');
  const inputJumlah = document.getElementById('jumlah');
  const formTitle = document.getElementById('judul-form');
  const submitButton = document.getElementById('tombol-simpan');
  const cancelButton = document.getElementById('tombol-batal');
  const message = document.getElementById('pesan');
  const tbody = document.getElementById('daftar-barang');

  let editingId = null;

  function showMessage(text) {
    message.textContent = text;
    message.hidden = text === '';
  }

  function createButton(label, ariaLabel, onClick, className) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = label;
    button.setAttribute('aria-label', ariaLabel);
    if (className) button.className = className;
    button.addEventListener('click', onClick);
    return button;
  }

  function createRow(item) {
    const row = document.createElement('tr');

    const nameCell = document.createElement('td');
    nameCell.textContent = item.nama;

    const amountCell = document.createElement('td');
    amountCell.className = 'angka';
    amountCell.textContent = item.jumlah;

    const actionCell = document.createElement('td');
    actionCell.className = 'aksi';
    actionCell.append(
      createButton('Ubah', `Ubah ${item.nama}`, () => startEdit(item)),
      createButton('Hapus', `Hapus ${item.nama}`, () => removeItem(item), 'bahaya'),
    );

    row.append(nameCell, amountCell, actionCell);
    return row;
  }

  function render() {
    const items = inventory.list();
    tbody.replaceChildren();

    if (items.length === 0) {
      const row = document.createElement('tr');
      const cell = document.createElement('td');
      cell.colSpan = 3;
      cell.className = 'kosong';
      cell.textContent = 'Belum ada barang. Isi formulir di atas untuk menambah barang pertama.';
      row.append(cell);
      tbody.append(row);
      return;
    }

    tbody.append(...items.map(createRow));
  }

  function resetForm() {
    editingId = null;
    form.reset();
    formTitle.textContent = 'Tambah barang';
    submitButton.textContent = 'Tambah barang';
    cancelButton.hidden = true;
    showMessage('');
  }

  function startEdit(item) {
    editingId = item.id;
    inputNama.value = item.nama;
    inputJumlah.value = item.jumlah;
    formTitle.textContent = 'Ubah barang';
    submitButton.textContent = 'Simpan perubahan';
    cancelButton.hidden = false;
    showMessage('');
    inputNama.focus();
  }

  function removeItem(item) {
    if (!window.confirm(`Hapus barang "${item.nama}"? Tindakan ini tidak bisa dibatalkan.`)) return;

    try {
      inventory.remove(item.id);
    } catch (error) {
      showMessage(error.message);
      return;
    }

    if (editingId === item.id) resetForm();
    render();
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const input = { nama: inputNama.value, jumlah: inputJumlah.value };

    try {
      if (editingId === null) {
        inventory.add(input);
      } else {
        inventory.update(editingId, input);
      }
    } catch (error) {
      showMessage(error.message);
      return;
    }

    resetForm();
    render();
  });

  cancelButton.addEventListener('click', resetForm);

  render();
})();
