const TITLE_MAX = 200;
const AUTHOR_MAX = 100;
const YEAR_MIN = 1000;

function validateBook(input) {
  const title = typeof input?.title === 'string' ? input.title.trim() : '';
  const author = typeof input?.author === 'string' ? input.author.trim() : '';
  const rawYear = input?.year;
  const year = typeof rawYear === 'string' || typeof rawYear === 'number' ? Number(rawYear) : NaN;
  const maxYear = new Date().getFullYear();
  const errors = {};

  if (!title) {
    errors.title = 'Judul wajib diisi.';
  } else if (title.length > TITLE_MAX) {
    errors.title = `Judul maksimal ${TITLE_MAX} karakter.`;
  }

  if (!author) {
    errors.author = 'Penulis wajib diisi.';
  } else if (author.length > AUTHOR_MAX) {
    errors.author = `Penulis maksimal ${AUTHOR_MAX} karakter.`;
  }

  if (!Number.isInteger(year) || year < YEAR_MIN || year > maxYear) {
    errors.year = `Tahun harus angka bulat antara ${YEAR_MIN} dan ${maxYear}.`;
  }

  if (Object.keys(errors).length > 0) {
    return { ok: false, errors };
  }
  return { ok: true, value: { title, author, year } };
}

module.exports = { validateBook };
