const API_URL = '/api/books';

const form = document.querySelector('#book-form');
const bookIdInput = document.querySelector('#book-id');
const titleInput = document.querySelector('#title');
const authorInput = document.querySelector('#author');
const yearInput = document.querySelector('#year');
const submitButton = document.querySelector('#submit-button');
const cancelButton = document.querySelector('#cancel-button');
const message = document.querySelector('#message');
const bookRows = document.querySelector('#book-rows');

async function request(method, url, body) {
  const response = await fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (response.status === 204) {
    return null;
  }
  const data = await response.json();
  if (!response.ok) {
    throw new Error((data.errors ?? [data.error]).join(' '));
  }
  return data;
}

function showMessage(text, isError = false) {
  message.textContent = text;
  message.classList.toggle('error', isError);
}

async function run(action) {
  try {
    await action();
  } catch (error) {
    showMessage(error.message, true);
  }
}

function resetForm() {
  form.reset();
  bookIdInput.value = '';
  submitButton.textContent = 'Tambah';
  cancelButton.hidden = true;
}

function fillForm(book) {
  bookIdInput.value = book.id;
  titleInput.value = book.title;
  authorInput.value = book.author;
  yearInput.value = book.year;
  submitButton.textContent = 'Simpan';
  cancelButton.hidden = false;
  titleInput.focus();
}

function makeButton(text, bookTitle, onClick) {
  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = text;
  button.setAttribute('aria-label', `${text} ${bookTitle}`);
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
  actions.className = 'row-actions';
  actions.append(
    makeButton('Ubah', book.title, () => fillForm(book)),
    makeButton('Hapus', book.title, () => run(() => removeBook(book))),
  );
  row.append(actions);
  return row;
}

function renderBooks(books) {
  if (books.length === 0) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 4;
    cell.className = 'empty';
    cell.textContent = 'Belum ada buku. Isi form di atas untuk menambahkan buku pertama.';
    row.append(cell);
    bookRows.replaceChildren(row);
    return;
  }
  bookRows.replaceChildren(...books.map(createRow));
}

async function loadBooks() {
  renderBooks(await request('GET', API_URL));
}

async function saveBook() {
  const book = {
    title: titleInput.value,
    author: authorInput.value,
    year: Number(yearInput.value),
  };

  if (bookIdInput.value) {
    await request('PUT', `${API_URL}/${bookIdInput.value}`, book);
    showMessage('Buku berhasil diubah.');
  } else {
    await request('POST', API_URL, book);
    showMessage('Buku berhasil ditambahkan.');
  }
  resetForm();
  await loadBooks();
}

async function removeBook(book) {
  if (!confirm(`Hapus buku "${book.title}"?`)) {
    return;
  }
  await request('DELETE', `${API_URL}/${book.id}`);
  if (bookIdInput.value === book.id) {
    resetForm();
  }
  showMessage('Buku berhasil dihapus.');
  await loadBooks();
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  run(saveBook);
});

cancelButton.addEventListener('click', () => {
  resetForm();
  showMessage('');
});

run(loadBooks);
