const crypto = require('node:crypto');
const fs = require('node:fs/promises');
const path = require('node:path');

async function readBooks(filePath) {
  try {
    return JSON.parse(await fs.readFile(filePath, 'utf8'));
  } catch (error) {
    if (error.code === 'ENOENT') return [];
    throw error;
  }
}

async function saveBooks(filePath, books) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  // Write a temp file first so a crash never leaves a half-written data file.
  const tempPath = `${filePath}.tmp`;
  await fs.writeFile(tempPath, JSON.stringify(books, null, 2));
  await fs.rename(tempPath, filePath);
}

function createBookStore(filePath) {
  let loaded = null;
  // Run writes one at a time so parallel requests cannot interleave the file.
  let queue = Promise.resolve();

  function load() {
    loaded ??= readBooks(filePath);
    return loaded;
  }

  function mutate(task) {
    const result = queue.then(async () => task(await load()));
    queue = result.catch(() => {});
    return result;
  }

  return {
    async list() {
      return [...(await load())];
    },

    async get(id) {
      return (await load()).find((book) => book.id === id) ?? null;
    },

    create(data) {
      return mutate(async (books) => {
        const book = { id: crypto.randomUUID(), ...data };
        books.push(book);
        await saveBooks(filePath, books);
        return book;
      });
    },

    update(id, data) {
      return mutate(async (books) => {
        const index = books.findIndex((book) => book.id === id);
        if (index === -1) return null;
        books[index] = { ...data, id };
        await saveBooks(filePath, books);
        return books[index];
      });
    },

    remove(id) {
      return mutate(async (books) => {
        const index = books.findIndex((book) => book.id === id);
        if (index === -1) return false;
        books.splice(index, 1);
        await saveBooks(filePath, books);
        return true;
      });
    },
  };
}

module.exports = { createBookStore };
