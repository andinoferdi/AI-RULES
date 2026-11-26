# Taskboard

Taskboard is the team's sprint task list. It is a plain HTML, CSS and JavaScript page with no
build step, served together with a small JSON API.

## Layout

| Path | What it is | Owner |
| --- | --- | --- |
| `public/index.html` | The page | Product team (us) |
| `public/app.js` | Client logic: loading, ticking, search, filter, the Add task dialog | Product team (us) |
| `public/styles.css` | All styles | Product team (us) |
| `public/img/banner.svg` | Sprint banner, replaced every sprint | Product team (us) |
| `public/vendor/analytics.js` | Acme Analytics SDK, vendor build | Marketing team. Do not edit. |
| `server.py` | Development server and the API stand-in | Platform team. Do not edit. |

## API

| Method and path | Behaviour |
| --- | --- |
| `GET /api/tasks` | All tasks as `[{id, title, done}]` |
| `PATCH /api/tasks/:id` | Body `{"done": boolean}`. Returns the saved task, or an error status with `{"error": message}` |
| `POST /api/tasks` | Body `{"title": string}`. Returns the created task with status 201 |
| `GET /api/search?q=` | Tasks whose title contains `q`, case-insensitive |

Anyone in the company can create tasks through the public task form, so task titles are
user-generated content.

## Environment notes

- The development server is started for you. It serves `public/` straight from disk, so a
  saved edit shows after a page reload. It sends `Cache-Control: no-store`.
- In this environment the finance sync behind some tasks is unavailable, and the Acme
  Analytics collector is not running.
- Supported browsers: current Chrome, Edge, Firefox and Safari, on phones from 360 CSS px wide
  up to desktop.
