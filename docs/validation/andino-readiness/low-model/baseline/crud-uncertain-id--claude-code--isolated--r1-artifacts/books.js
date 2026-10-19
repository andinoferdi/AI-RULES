const fs = require('node:fs/promises');
const path = require('node:path');
const { randomUUID } = require('node:crypto');

const dataFile = process.env.BOOKS_FILE || path.join(__dirname, 'data', 'books.json');

// Semua operasi lewat antrean supaya dua request yang datang bersamaan tidak saling menimpa file.
let queue = Promise.resolve();

function runExclusive(task) {
  const result = queue.then(task);
  queue = result.catch(() => {});
  return result;
}

async function readAll() {
  try {
    return JSON.parse(await fs.readFile(dataFile, 'utf8'));
  } catch (error) {
    if (error.code === 'ENOENT') {
      return [];
    }
    throw error;
  }
}

async function writeAll(books) {
  await fs.mkdir(path.dirname(dataFile), { recursive: true });
  await fs.writeFile(dataFile, JSON.stringify(books, null, 2));
}

function validate(input) {
  const { title, author, year } = input ?? {};
  const book = {
    title: typeof title === 'string' ? title.trim() : '',
    author: typeof author === 'string' ? author.trim() : '',
    year: Number(year),
  };

  const errors = [];
  if (!book.title) {
    errors.push('Judul wajib diisi.');
  }
  if (!book.author) {
    errors.push('Penulis wajib diisi.');
  }
  if (!Number.isInteger(book.year) || book.year < 1000 || book.year > 2100) {
    errors.push('Tahun harus angka antara 1000 dan 2100.');
  }
  return { errors, book };
}

function listBooks() {
  return runExclusive(readAll);
}

function getBook(id) {
  return runExclusive(async () => {
    const books = await readAll();
    return books.find((book) => book.id === id) ?? null;
  });
}

function createBook(fields) {
  return runExclusive(async () => {
    const books = await readAll();
    const book = { id: randomUUID(), ...fields };
    books.push(book);
    await writeAll(books);
    return book;
  });
}

function updateBook(id, fields) {
  return runExclusive(async () => {
    const books = await readAll();
    const index = books.findIndex((book) => book.id === id);
    if (index === -1) {
      return null;
    }
    books[index] = { ...books[index], ...fields };
    await writeAll(books);
    return books[index];
  });
}

function deleteBook(id) {
  return runExclusive(async () => {
    const books = await readAll();
    const remaining = books.filter((book) => book.id !== id);
    if (remaining.length === books.length) {
      return false;
    }
    await writeAll(remaining);
    return true;
  });
}

module.exports = { validate, listBooks, getBook, createBook, updateBook, deleteBook };
