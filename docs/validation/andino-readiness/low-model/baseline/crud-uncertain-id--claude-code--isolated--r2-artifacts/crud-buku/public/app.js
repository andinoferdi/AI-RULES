const form = document.querySelector('#book-form');
const formTitle = document.querySelector('#form-title');
const submitButton = document.querySelector('#submit-button');
const cancelButton = document.querySelector('#cancel-button');
const tableBody = document.querySelector('#book-rows');
const statusMessage = document.querySelector('#status');

const FIELDS = ['title', 'author', 'year'];
let editingId = null;

async function api(url, options = {}) {
  let response;
  try {
    response = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json' } });
  } catch {
    throw new Error('Tidak bisa terhubung ke server.');
  }
  if (response.status === 204) return null;

  const data = await response.json();
  if (!response.ok) {
    const error = new Error(data.error || 'Permintaan gagal.');
    error.fields = data.fields || {};
    throw error;
  }
  return data;
}

function showStatus(message, isError = false) {
  statusMessage.textContent = message;
  statusMessage.classList.toggle('error', isError);
}

function showFieldErrors(fields) {
  for (const name of FIELDS) {
    const message = fields[name] || '';
    document.querySelector(`#${name}-error`).textContent = message;
    document.querySelector(`#${name}`).setAttribute('aria-invalid', String(Boolean(message)));
  }
}

function setTableMessage(message) {
  const row = document.createElement('tr');
  const cell = document.createElement('td');
  cell.colSpan = 4;
  cell.className = 'message';
  cell.textContent = message;
  row.append(cell);
  tableBody.replaceChildren(row);
}

function createButton(label, accessibleName, className, onClick) {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = className;
  button.textContent = label;
  button.setAttribute('aria-label', accessibleName);
  button.addEventListener('click', onClick);
  return button;
}

function createRow(book) {
  const row = document.createElement('tr');
  for (const value of [book.title, book.author, book.year]) {
    const cell = document.createElement('td');
    cell.textContent = value;
    row.append(cell);
  }

  const actions = document.createElement('td');
  actions.className = 'actions';
  actions.append(
    createButton('Ubah', `Ubah ${book.title}`, 'secondary', () => startEdit(book)),
    createButton('Hapus', `Hapus ${book.title}`, 'danger', () => deleteBook(book)),
  );
  row.append(actions);
  return row;
}

function renderBooks(books) {
  if (books.length === 0) {
    setTableMessage('Belum ada buku. Tambahkan buku lewat formulir di atas.');
    return;
  }
  tableBody.replaceChildren(...books.map(createRow));
}

async function loadBooks() {
  setTableMessage('Memuat data...');
  try {
    renderBooks(await api('/api/books'));
  } catch (error) {
    setTableMessage('Data belum bisa dimuat.');
    showStatus(error.message, true);
  }
}

function readForm() {
  const data = new FormData(form);
  return { title: data.get('title'), author: data.get('author'), year: data.get('year') };
}

function fillForm(book) {
  for (const name of FIELDS) {
    document.querySelector(`#${name}`).value = book[name];
  }
}

function startEdit(book) {
  editingId = book.id;
  fillForm(book);
  showFieldErrors({});
  formTitle.textContent = 'Ubah buku';
  submitButton.textContent = 'Simpan perubahan';
  cancelButton.hidden = false;
  showStatus('');
  document.querySelector('#title').focus();
}

function resetForm() {
  form.reset();
  editingId = null;
  formTitle.textContent = 'Tambah buku';
  submitButton.textContent = 'Tambah buku';
  cancelButton.hidden = true;
  showFieldErrors({});
}

async function deleteBook(book) {
  if (!window.confirm(`Hapus buku "${book.title}"?`)) return;
  try {
    await api(`/api/books/${encodeURIComponent(book.id)}`, { method: 'DELETE' });
    if (editingId === book.id) resetForm();
    showStatus('Buku berhasil dihapus.');
    await loadBooks();
  } catch (error) {
    showStatus(error.message, true);
  }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const isEditing = editingId !== null;
  const body = JSON.stringify(readForm());
  submitButton.disabled = true;
  showFieldErrors({});

  try {
    if (isEditing) {
      await api(`/api/books/${encodeURIComponent(editingId)}`, { method: 'PUT', body });
    } else {
      await api('/api/books', { method: 'POST', body });
    }
    resetForm();
    showStatus(isEditing ? 'Buku berhasil diubah.' : 'Buku berhasil ditambahkan.');
    await loadBooks();
  } catch (error) {
    showFieldErrors(error.fields || {});
    showStatus(error.message, true);
  } finally {
    submitButton.disabled = false;
  }
});

cancelButton.addEventListener('click', () => {
  resetForm();
  showStatus('');
});

loadBooks();
