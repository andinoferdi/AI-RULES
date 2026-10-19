const fs = require('fs');
const http = require('http');
const path = require('path');
const { createBookStore, validateBook } = require('./lib/books');

const PUBLIC_DIR = path.join(__dirname, 'public');
const DATA_FILE = path.join(__dirname, 'data', 'books.json');
const MAX_BODY_BYTES = 1024 * 1024;
const CONTENT_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
};

class HttpError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

function sendJson(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(body));
}

function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    req.on('data', (chunk) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        reject(new HttpError(413, 'Data yang dikirim terlalu besar.'));
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString('utf8') || 'null'));
      } catch {
        reject(new HttpError(400, 'Data harus berupa JSON yang valid.'));
      }
    });
    req.on('error', reject);
  });
}

async function handleBooks(req, res, id, store) {
  if (id === undefined) {
    if (req.method === 'GET') return sendJson(res, 200, store.list());
    if (req.method === 'POST') {
      const { errors, value } = validateBook(await readJsonBody(req));
      if (Object.keys(errors).length > 0) {
        return sendJson(res, 400, { error: 'Data buku belum valid.', fields: errors });
      }
      return sendJson(res, 201, store.create(value));
    }
    throw new HttpError(405, 'Metode tidak diizinkan.');
  }

  const book = store.get(id);
  if (!book) throw new HttpError(404, 'Buku tidak ditemukan.');

  if (req.method === 'GET') return sendJson(res, 200, book);
  if (req.method === 'PUT') {
    const { errors, value } = validateBook(await readJsonBody(req));
    if (Object.keys(errors).length > 0) {
      return sendJson(res, 400, { error: 'Data buku belum valid.', fields: errors });
    }
    return sendJson(res, 200, store.update(id, value));
  }
  if (req.method === 'DELETE') {
    store.remove(id);
    res.writeHead(204);
    return res.end();
  }
  throw new HttpError(405, 'Metode tidak diizinkan.');
}

function serveStatic(pathname, res) {
  const requested = pathname === '/' ? '/index.html' : pathname;
  const filePath = path.join(PUBLIC_DIR, requested);
  if (!filePath.startsWith(PUBLIC_DIR + path.sep)) {
    throw new HttpError(404, 'Halaman tidak ditemukan.');
  }
  fs.readFile(filePath, (error, content) => {
    if (error) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      return res.end('Halaman tidak ditemukan.');
    }
    res.writeHead(200, { 'Content-Type': CONTENT_TYPES[path.extname(filePath)] ?? 'application/octet-stream' });
    res.end(content);
  });
}

function createServer(store) {
  return http.createServer(async (req, res) => {
    try {
      const { pathname } = new URL(req.url, 'http://localhost');
      const booksRoute = pathname.match(/^\/api\/books(?:\/([^/]+))?$/);
      if (booksRoute) return await handleBooks(req, res, booksRoute[1], store);
      if (pathname.startsWith('/api/')) throw new HttpError(404, 'Alamat API tidak ditemukan.');
      return serveStatic(pathname, res);
    } catch (error) {
      const isKnown = error instanceof HttpError;
      if (!isKnown) console.error(error);
      if (res.headersSent) return res.end();
      const status = isKnown ? error.status : 500;
      sendJson(res, status, { error: isKnown ? error.message : 'Terjadi kesalahan di server.' });
    }
  });
}

module.exports = { createServer };

if (require.main === module) {
  const port = Number(process.env.PORT) || 3000;
  const store = createBookStore(DATA_FILE);
  createServer(store).listen(port, '127.0.0.1', () => {
    console.log(`Aplikasi berjalan di http://127.0.0.1:${port}`);
  });
}
