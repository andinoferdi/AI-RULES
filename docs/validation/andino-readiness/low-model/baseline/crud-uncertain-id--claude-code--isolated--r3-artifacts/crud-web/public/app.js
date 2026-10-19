const form = document.querySelector('#book-form');
const formTitle = document.querySelector('#form-title');
const idInput = document.querySelector('#book-id');
const submitButton = document.querySelector('#submit-button');
const cancelButton = document.querySelector('#cancel-button');
const rows = document.querySelector('#book-rows');
const countText = document.querySelector('#count');
const statusText = document.querySelector('#status');
const FIELDS = ['title', 'author', 'year'];

let books = [];

async function api(url, options = {}) {
  let response;
  try {
    response = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json' } });
  } catch {
    throw new Error('Tidak bisa terhubung ke server.');
  }

  if (response.status === 204) return null;

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(data.error || 'Permintaan gagal.');
    error.errors = data.errors;
    throw error;
  }
  return data;
}

async function loadBooks() {
  try {
    books = await api('/api/books');
    renderRows();
  } catch (error) {
    renderMessage('Data belum bisa dimuat.');
    setStatus(error.message, true);
  }
}

function renderRows() {
  countText.textContent = `${books.length} buku`;
  if (books.length === 0) {
    renderMessage('Belum ada buku. Isi formulir di samping untuk menambah buku pertama.');
    return;
  }
  rows.replaceChildren(...books.map(createRow));
}

function renderMessage(text) {
  const cell = createCell(text, 'empty');
  cell.colSpan = 4;
  const row = document.createElement('tr');
  row.append(cell);
  rows.replaceChildren(row);
}

function createRow(book) {
  const row = document.createElement('tr');
  row.append(
    createCell(book.title),
    createCell(book.author),
    createCell(String(book.year), 'num'),
    createActionsCell(book),
  );
  return row;
}

function createCell(text, className = '') {
  const cell = document.createElement('td');
  cell.className = className;
  cell.textContent = text;
  return cell;
}

function createActionsCell(book) {
  const cell = createCell('', 'actions');
  cell.append(
    createActionButton('Ubah', book, 'btn', () => startEdit(book)),
    createActionButton('Hapus', book, 'btn btn-danger', () => removeBook(book)),
  );
  return cell;
}

function createActionButton(label, book, className, onClick) {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = className;
  button.textContent = label;
  button.setAttribute('aria-label', `${label} ${book.title}`);
  button.addEventListener('click', onClick);
  return button;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const isEdit = idInput.value !== '';
  const payload = JSON.stringify({
    title: form.elements.title.value,
    author: form.elements.author.value,
    year: form.elements.year.value,
  });

  showFieldErrors({});
  submitButton.disabled = true;
  try {
    if (isEdit) {
      await api(`/api/books/${idInput.value}`, { method: 'PUT', body: payload });
    } else {
      await api('/api/books', { method: 'POST', body: payload });
    }
    resetForm();
    await loadBooks();
    setStatus(isEdit ? 'Buku berhasil diubah.' : 'Buku berhasil ditambahkan.');
  } catch (error) {
    showFieldErrors(error.errors);
    setStatus(error.errors ? 'Periksa kembali isian yang ditandai.' : error.message, true);
  } finally {
    submitButton.disabled = false;
  }
});

function showFieldErrors(errors = {}) {
  for (const name of FIELDS) {
    const message = errors[name] ?? '';
    form.elements[name].setAttribute('aria-invalid', String(message !== ''));
    document.querySelector(`#${name}-error`).textContent = message;
  }
}

function startEdit(book) {
  idInput.value = book.id;
  form.elements.title.value = book.title;
  form.elements.author.value = book.author;
  form.elements.year.value = book.year;
  formTitle.textContent = 'Ubah buku';
  submitButton.textContent = 'Simpan perubahan';
  cancelButton.hidden = false;
  showFieldErrors({});
  setStatus('');
  form.elements.title.focus();
}

function resetForm() {
  form.reset();
  idInput.value = '';
  formTitle.textContent = 'Tambah buku';
  submitButton.textContent = 'Simpan buku';
  cancelButton.hidden = true;
  showFieldErrors({});
}

async function removeBook(book) {
  if (!window.confirm(`Hapus buku "${book.title}"?`)) return;

  try {
    await api(`/api/books/${book.id}`, { method: 'DELETE' });
    if (idInput.value === book.id) resetForm();
    await loadBooks();
    setStatus('Buku berhasil dihapus.');
  } catch (error) {
    setStatus(error.message, true);
  }
}

function setStatus(message, isError = false) {
  statusText.textContent = message;
  statusText.classList.toggle('status-error', isError);
}

cancelButton.addEventListener('click', () => {
  resetForm();
  setStatus('');
});

renderMessage('Memuat data...');
loadBooks();
