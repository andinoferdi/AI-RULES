# Panduan AGENTS untuk Repository Ini

Dokumen ini berisi aturan kerja untuk AI agent, coding assistant, atau developer yang berinteraksi langsung dengan repository. Tujuannya agar perubahan tetap aman, terarah, dan tidak merusak development workflow project.

## 1. Gunakan Mode Development yang Sesuai, **bukan build production saat iterasi**

* **Gunakan command development project** seperti `npm run dev`, `pnpm dev`, `yarn dev`, `php artisan serve`, `docker compose up`, atau command lain yang memang dipakai repository saat iterasi.
* **Jangan menjalankan build production secara asal di tengah sesi agent.** Build production hanya dijalankan jika task memang meminta verifikasi build, release, atau deployment.
* Jika command build dibutuhkan, cek dulu script yang tersedia di `package.json`, `composer.json`, `Makefile`, `Taskfile`, atau dokumentasi repository.

## 2. Jaga Dependency Tetap Sinkron

Jika menambah atau mengubah dependency, lakukan ini:

1. Update lockfile yang sesuai, seperti `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `composer.lock`, `poetry.lock`, `uv.lock`, `go.sum`, atau file lock lain.
2. Restart development server bila dependency memengaruhi runtime.
3. Jangan menambah dependency baru jika kebutuhan masih bisa diselesaikan dengan dependency yang sudah ada.

## 3. Coding Conventions

* Ikuti bahasa, framework, folder structure, naming, linting, dan pola module yang sudah ada di repository.
* Untuk file baru, gunakan konvensi stack aktif, misalnya TypeScript untuk project TS, PHP untuk Laravel, Python untuk FastAPI/Django, atau bahasa lain sesuai project.
* Letakkan file baru sedekat mungkin dengan domain atau module yang relevan.
* Hindari refactor besar jika task hanya meminta bug fix atau perubahan kecil.

## 4. Useful Commands Recap

| Command | Purpose |
| --- | --- |
| `npm run dev` / `pnpm dev` / `yarn dev` | Menjalankan dev server untuk project frontend atau full-stack JS. |
| `npm run lint` / `pnpm lint` / `yarn lint` | Menjalankan lint bila script tersedia. |
| `npm run test` / `pnpm test` / `yarn test` | Menjalankan test JS/TS bila tersedia. |
| `composer test` / `php artisan test` / `vendor/bin/phpunit` | Menjalankan test PHP/Laravel bila tersedia. |
| `docker compose up` | Menjalankan service lokal bila project memakai Docker Compose. |
| `npm run build` / `pnpm build` / `yarn build` | Build production. Jalankan hanya jika relevan dengan task. |

---

Ikuti praktik ini agar workflow agent tetap cepat, aman, dan tidak membuat state development menjadi kacau. Jika ragu, baca dokumentasi repository dan cek script yang tersedia sebelum menjalankan command besar.
