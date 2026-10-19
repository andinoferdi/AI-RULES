const http = require('node:http');
const fs = require('node:fs/promises');
const path = require('node:path');
const books = require('./books');

const publicDir = path.join(__dirname, 'public');
const contentTypes = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
};
const NOT_FOUND_MESSAGE = 'Buku tidak ditemukan.';

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
    let raw = '';
    req.setEncoding('utf8');
    req.on('data', (chunk) => {
      raw += chunk;
    });
    req.on('end', () => {
      try {
        resolve(raw ? JSON.parse(raw) : {});
      } catch {
        reject(new HttpError(400, 'Body harus berupa JSON yang valid.'));
      }
    });
    req.on('error', reject);
  });
}

async function handleApi(req, res, pathname) {
  const match = pathname.match(/^\/api\/books(?:\/([^/]+))?$/);
  if (!match) {
    throw new HttpError(404, 'Endpoint tidak ditemukan.');
  }
  const id = match[1];

  if (!id && req.method === 'GET') {
    return sendJson(res, 200, await books.listBooks());
  }

  if (!id && req.method === 'POST') {
    const { errors, book } = books.validate(await readJsonBody(req));
    if (errors.length > 0) {
      return sendJson(res, 400, { errors });
    }
    return sendJson(res, 201, await books.createBook(book));
  }

  if (id && req.method === 'GET') {
    const book = await books.getBook(id);
    if (!book) {
      throw new HttpError(404, NOT_FOUND_MESSAGE);
    }
    return sendJson(res, 200, book);
  }

  if (id && req.method === 'PUT') {
    const { errors, book } = books.validate(await readJsonBody(req));
    if (errors.length > 0) {
      return sendJson(res, 400, { errors });
    }
    const updated = await books.updateBook(id, book);
    if (!updated) {
      throw new HttpError(404, NOT_FOUND_MESSAGE);
    }
    return sendJson(res, 200, updated);
  }

  if (id && req.method === 'DELETE') {
    const deleted = await books.deleteBook(id);
    if (!deleted) {
      throw new HttpError(404, NOT_FOUND_MESSAGE);
    }
    res.writeHead(204);
    return res.end();
  }

  throw new HttpError(405, 'Metode tidak diizinkan.');
}

async function serveStatic(res, pathname) {
  const relativePath = pathname === '/' ? 'index.html' : pathname.slice(1);
  const filePath = path.join(publicDir, relativePath);
  if (!filePath.startsWith(publicDir + path.sep)) {
    throw new HttpError(403, 'Akses ditolak.');
  }

  let content;
  try {
    content = await fs.readFile(filePath);
  } catch {
    throw new HttpError(404, 'Halaman tidak ditemukan.');
  }
  res.writeHead(200, {
    'Content-Type': contentTypes[path.extname(filePath)] ?? 'application/octet-stream',
  });
  res.end(content);
}

function createServer() {
  return http.createServer(async (req, res) => {
    try {
      const { pathname } = new URL(req.url, 'http://localhost');
      if (pathname.startsWith('/api/')) {
        await handleApi(req, res, pathname);
      } else {
        await serveStatic(res, pathname);
      }
    } catch (error) {
      if (error instanceof HttpError) {
        return sendJson(res, error.status, { error: error.message });
      }
      console.error(error);
      sendJson(res, 500, { error: 'Terjadi kesalahan di server.' });
    }
  });
}

if (require.main === module) {
  const port = process.env.PORT || 3000;
  createServer().listen(port, () => {
    console.log(`Aplikasi berjalan di http://localhost:${port}`);
  });
}

module.exports = { createServer };
