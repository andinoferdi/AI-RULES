const fs = require('fs');
const path = require('path');
const { randomUUID } = require('crypto');

const MAX_TITLE_LENGTH = 200;
const MAX_AUTHOR_LENGTH = 100;

function readText(value) {
  if (typeof value === 'string') return value.trim();
  if (typeof value === 'number') return String(value);
  return '';
}

function validateBook(input) {
  const source = input && typeof input === 'object' ? input : {};
  const title = readText(source.title);
  const author = readText(source.author);
  const year = readText(source.year);
  const maxYear = new Date().getFullYear() + 1;
  const errors = {};

  if (!title) {
    errors.title = 'Judul wajib diisi.';
  } else if (title.length > MAX_TITLE_LENGTH) {
    errors.title = `Judul maksimal ${MAX_TITLE_LENGTH} karakter.`;
  }

  if (!author) {
    errors.author = 'Penulis wajib diisi.';
  } else if (author.length > MAX_AUTHOR_LENGTH) {
    errors.author = `Nama penulis maksimal ${MAX_AUTHOR_LENGTH} karakter.`;
  }

  if (!/^\d{4}$/.test(year)) {
    errors.year = 'Tahun harus 4 digit, misalnya 2005.';
  } else if (Number(year) < 1000 || Number(year) > maxYear) {
    errors.year = `Tahun harus antara 1000 dan ${maxYear}.`;
  }

  return { errors, value: { title, author, year: Number(year) } };
}

function createBookStore(filePath) {
  let books = fs.existsSync(filePath) ? JSON.parse(fs.readFileSync(filePath, 'utf8')) : [];

  function save() {
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, JSON.stringify(books, null, 2));
  }

  return {
    list: () => [...books],
    get: (id) => books.find((book) => book.id === id) ?? null,
    create(data) {
      const book = { id: randomUUID(), ...data };
      books.push(book);
      save();
      return book;
    },
    update(id, data) {
      const index = books.findIndex((book) => book.id === id);
      if (index === -1) return null;
      books[index] = { ...data, id };
      save();
      return books[index];
    },
    remove(id) {
      const index = books.findIndex((book) => book.id === id);
      if (index === -1) return false;
      books.splice(index, 1);
      save();
      return true;
    },
  };
}

module.exports = { createBookStore, validateBook };
