const fs = require('node:fs/promises');
const http = require('node:http');
const path = require('node:path');
const { createBookStore } = require('./store');
const { validateBook } = require('./validate');

const PUBLIC_DIR = path.join(__dirname, '..', 'public');
const MAX_BODY_BYTES = 100 * 1024;
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
  if (status === 204) {
    res.writeHead(204);
    res.end();
    return;
  }
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(payload),
  });
  res.end(payload);
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;

    req.on('data', (chunk) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        req.destroy();
        reject(new HttpError(413, 'Data terlalu besar.'));
        return;
      }
      chunks.push(chunk);
    });

    req.on('end', () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString('utf8')));
      } catch {
        reject(new HttpError(400, 'Data harus berupa JSON yang valid.'));
      }
    });

    req.on('error', reject);
  });
}

async function handleBooks(req, res, store, id) {
  if (!id) {
    if (req.method === 'GET') {
      return sendJson(res, 200, await store.list());
    }
    if (req.method === 'POST') {
      const result = validateBook(await readJson(req));
      if (!result.ok) return sendJson(res, 422, { errors: result.errors });
      return sendJson(res, 201, await store.create(result.value));
    }
  } else {
    if (req.method === 'GET') {
      const book = await store.get(id);
      if (!book) throw new HttpError(404, 'Buku tidak ditemukan.');
      return sendJson(res, 200, book);
    }
    if (req.method === 'PUT') {
      const result = validateBook(await readJson(req));
      if (!result.ok) return sendJson(res, 422, { errors: result.errors });
      const book = await store.update(id, result.value);
      if (!book) throw new HttpError(404, 'Buku tidak ditemukan.');
      return sendJson(res, 200, book);
    }
    if (req.method === 'DELETE') {
      if (!(await store.remove(id))) throw new HttpError(404, 'Buku tidak ditemukan.');
      return sendJson(res, 204);
    }
  }
  throw new HttpError(405, 'Metode tidak diizinkan.');
}

async function serveStatic(req, res, pathname) {
  if (req.method !== 'GET') throw new HttpError(405, 'Metode tidak diizinkan.');

  const relativePath = pathname === '/' ? 'index.html' : pathname.slice(1);
  const filePath = path.join(PUBLIC_DIR, relativePath);
  // Block paths that escape the public folder.
  if (!filePath.startsWith(PUBLIC_DIR + path.sep)) {
    throw new HttpError(404, 'Halaman tidak ditemukan.');
  }

  try {
    const content = await fs.readFile(filePath);
    res.writeHead(200, {
      'Content-Type': CONTENT_TYPES[path.extname(filePath)] ?? 'application/octet-stream',
    });
    res.end(content);
  } catch (error) {
    if (error.code === 'ENOENT' || error.code === 'EISDIR') {
      throw new HttpError(404, 'Halaman tidak ditemukan.');
    }
    throw error;
  }
}

async function handleRequest(req, res, store) {
  const { pathname } = new URL(req.url, 'http://localhost');
  const match = pathname.match(/^\/api\/books(?:\/([^/]+))?$/);

  if (match) return handleBooks(req, res, store, match[1]);
  if (pathname.startsWith('/api/')) throw new HttpError(404, 'Alamat API tidak ditemukan.');
  return serveStatic(req, res, pathname);
}

function createAppServer({ dataFile }) {
  const store = createBookStore(dataFile);

  return http.createServer(async (req, res) => {
    try {
      await handleRequest(req, res, store);
    } catch (error) {
      if (error instanceof HttpError) {
        sendJson(res, error.status, { error: error.message });
        return;
      }
      console.error(error);
      sendJson(res, 500, { error: 'Terjadi kesalahan di server.' });
    }
  });
}

module.exports = { createAppServer };

if (require.main === module) {
  const port = Number(process.env.PORT) || 3000;
  const dataFile = path.join(__dirname, '..', 'data', 'books.json');
  createAppServer({ dataFile }).listen(port, () => {
    console.log(`Buka http://localhost:${port} di browser.`);
  });
}
