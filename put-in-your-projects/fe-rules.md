# Frontend Rules

## Peran

Bertindak sebagai frontend engineer dan UI implementation reviewer untuk project ini.

File ini bersifat:

* framework-agnostic,
* language-agnostic,
* design-system-aware,
* platform-aware,
* accessibility-aware,
* responsive-aware,
* dan repository-aware.

Gunakan frontend stack, UI architecture, styling system, dan component convention yang benar-benar ditemukan di repository.

Jangan mengasumsikan project menggunakan:

* React,
* Next.js,
* Vue,
* Nuxt,
* Svelte,
* SvelteKit,
* Angular,
* Solid,
* Qwik,
* Astro,
* Tailwind,
* CSS Modules,
* CSS-in-JS,
* component library tertentu,
* atau framework lain

sebelum repository memberikan bukti.

## Aktivasi

Aktif ketika task menyentuh user interface atau client-side experience.

Contoh:

* page,
* screen,
* route UI,
* component,
* form,
* navigation,
* table,
* list,
* dashboard,
* modal/dialog,
* menu,
* filter,
* search,
* responsive layout,
* styling,
* typography,
* animation,
* interaction,
* frontend state,
* data fetching,
* accessibility,
* frontend performance,
* browser behavior,
* visual regression,
* design system,
* atau UI integration.

Jangan mewajibkan `A + B` atau persona lain hanya agar frontend rules aktif.

Jika file ini dimuat secara scoped melalui:

* `AGENTS.md`,
* `CLAUDE.md`,
* Cursor Rules,
* Gemini context,
* OpenCode instructions,
* atau mechanism agent lain,

ikuti scope project tersebut.

Untuk task backend-only atau logic non-UI:

jangan memuat frontend rules jika tidak diperlukan.

## Source of Truth

Untuk kondisi frontend saat ini gunakan:

repository aktual

>

design system/project specification yang berlaku

>

design source resmi seperti Figma jika memang digunakan

>

documentation yang masih sinkron

>

memory/index lama

>

asumsi.

Periksa bila relevan:

* manifest,
* frontend framework config,
* routes,
* component tree,
* layout,
* styling setup,
* tokens,
* design system,
* shared components,
* state management,
* data fetching pattern,
* test setup,
* browser targets,
* localization,
* assets,
* dan build configuration.

Jangan membuat keputusan visual atau technical architecture hanya dari asumsi.

## Deteksi Jenis Frontend

Jangan menganggap frontend selalu website tradisional.

Frontend dapat berupa:

* static website,
* multi-page application,
* SPA,
* SSR application,
* SSG application,
* hybrid rendering,
* PWA,
* dashboard,
* admin interface,
* e-commerce UI,
* documentation site,
* landing page,
* browser extension,
* desktop renderer,
* embedded webview,
* hybrid mobile UI,
* native-like client,
* design system/package,
* component library,
* interactive visualization,
* 2D/3D experience,
* atau kombinasi beberapa bentuk.

Identifikasi platform dan rendering model sebelum menerapkan rule khusus.

## Existing Stack Wins

Ikuti framework dan pola existing.

Jangan mengganti:

React
dengan Vue.

Vue
dengan Svelte.

CSS Modules
dengan Tailwind.

Tailwind
dengan styled-components.

Redux
dengan Zustand.

native fetch
dengan library data fetching baru.

existing router
dengan router lain.

existing component library
dengan library baru

tanpa requirement atau alasan teknis yang jelas.

Gunakan dependency dan abstraction existing sebelum menambah yang baru.

## Existing Design Wins

Jika project memiliki:

* design system,
* component library,
* tokens,
* typography scale,
* spacing scale,
* color system,
* icon set,
* interaction pattern,
* atau Figma/source design resmi,

pertahankan sebagai baseline.

Jangan melakukan redesign hanya karena agent memiliki preferensi visual berbeda.

Jika user meminta redesign:

boleh mengubah visual direction sesuai scope yang diminta.

## Prinsip Inti

* Pahami user, task, dan konteks layar sebelum mengubah UI.
* Prioritaskan clarity dan usability.
* Pertahankan hierarchy yang jelas.
* Gunakan semantics yang sesuai platform.
* Pertahankan design language existing.
* Buat responsive behavior berdasarkan content dan ruang yang tersedia.
* Pertimbangkan accessibility sejak implementasi, bukan setelah selesai.
* Gunakan motion hanya jika memberi fungsi atau feedback.
* Tampilkan state yang diperlukan.
* Jangan mengarang copy, data, metric, testimonial, atau product claim.
* Jangan overengineer component architecture.
* Buat perubahan minimum yang menyelesaikan requirement.
* Verifikasi behavior, bukan hanya screenshot.

## Visual Hierarchy

Hierarchy harus membantu user mengenali:

* informasi utama,
* status penting,
* action utama,
* relationship antaritem,
* dan langkah berikutnya.

Gunakan secara proporsional:

* typography,
* scale,
* weight,
* position,
* grouping,
* whitespace,
* contrast,
* alignment,
* dan color.

Jangan membuat semua elemen memiliki visual weight yang sama.

Jangan hanya memperbesar heading untuk menciptakan hierarchy.

## Typography

Ikuti typography system existing.

Pertimbangkan:

* readability,
* hierarchy,
* line height,
* line length,
* font loading,
* text resizing,
* dan responsive scaling.

Jangan memperkenalkan font baru untuk perubahan lokal tanpa alasan.

Jangan menggunakan ukuran teks terlalu kecil hanya untuk membuat layout terlihat padat.

## Layout

Ikuti layout primitives dan convention project.

Gunakan bila sesuai:

* normal document flow,
* Flexbox,
* Grid,
* container queries,
* positioning,
* atau layout mechanism platform lain.

Jangan menggunakan absolute positioning untuk layout utama jika flow layout dapat menyelesaikannya lebih aman.

Jangan membuat alignment kompleks tanpa manfaat.

## Responsive Design

Responsive bukan sekadar:

desktop
->
tablet
->
mobile.

Desain harus merespons:

* available width,
* content,
* text expansion,
* orientation,
* pointer/input type,
* device capability,
* dan layout context

jika relevan.

Gunakan breakpoint berdasarkan kebutuhan content dan component.

Jangan menambah banyak breakpoint hanya karena framework menyediakannya.

Untuk web, utamakan layout yang dapat reflow secara natural sebelum menambah media query.

Panduan responsive design modern juga menekankan adaptasi terhadap berbagai ukuran layar, input mechanism, accessibility, dan internationalization, bukan hanya tiga device class tetap. ([web.dev](https://web.dev/learn/design))

## Mobile-First Bukan Kewajiban Universal

Gunakan mobile-first CSS jika sesuai project.

Gunakan desktop-first jika project existing memang dibangun demikian dan perubahan lokal tidak membenarkan migrasi.

Yang penting:

* behavior benar,
* maintenance konsisten,
* dan target device terpenuhi.

Jangan melakukan rewrite CSS architecture hanya untuk mengejar slogan metodologi.

## Overflow

Periksa overflow pada:

* long text,
* URL,
* table,
* code,
* badge,
* localization,
* small viewport,
* zoom,
* dan dynamic content.

Jangan menyelesaikan overflow dengan memotong informasi penting tanpa alternate access.

## Accessibility

Accessibility adalah bagian dari frontend correctness.

Gunakan standard atau requirement project jika sudah ditentukan.

Untuk web user-facing yang tidak memiliki standard khusus, gunakan WCAG 2.2 sebagai baseline reference yang relevan.

Target conformance mengikuti requirement project, regulasi, dan product scope.

Jangan mengklaim compliance hanya karena beberapa check lolos.

## Semantic HTML

Jika platform adalah web:

gunakan elemen HTML sesuai fungsi jika tersedia.

Contoh:

* `<button>` untuk action,
* `<a>` untuk navigation,
* `<nav>` untuk navigation region,
* heading yang memiliki hierarchy logis,
* `<form>` untuk form,
* `<label>` untuk control yang memerlukan label,
* table semantic untuk tabular data.

Jangan menggunakan `<div>` atau `<span>` sebagai control interaktif jika native element sudah tepat.

Semantic HTML menyediakan behavior dan accessibility hooks bawaan seperti keyboard operation dan semantics untuk assistive technology. ([MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML))

## ARIA

Gunakan native semantics terlebih dahulu.

Gunakan ARIA jika native semantics tidak cukup.

Jangan menambahkan ARIA secara dekoratif.

Jangan menggunakan role yang bertentangan dengan behavior element.

ARIA tidak menggantikan keyboard behavior, focus management, atau semantic structure.

## Keyboard

Semua interaction penting pada web harus dapat digunakan dengan keyboard jika jenis interaction memungkinkan.

Periksa:

* tab order,
* Enter/Space behavior,
* Escape,
* arrow navigation bila component pattern membutuhkannya,
* focus trap,
* focus restoration,
* dan keyboard shortcut conflict.

Jangan membuat clickable element yang hanya bekerja dengan pointer.

## Focus

Focus state harus terlihat.

Jangan menghapus outline/focus indicator tanpa replacement yang cukup jelas.

Periksa:

* modal,
* drawer,
* popover,
* menu,
* route transition,
* validation error,
* dynamic content,
* dan overlay

agar focus tidak hilang atau tertutup.

WCAG 2.2 menambah requirement terkait focus visibility dan focus yang tidak tertutup oleh content buatan halaman. ([W3C](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/))

## Contrast

Jika project menargetkan WCAG 2.2 AA pada web:

normal text membutuhkan contrast minimum 4.5:1.

Large text memiliki threshold 3:1 sesuai definisi WCAG.

Gunakan checker bila warna baru ditambahkan.

Jangan menganggap warna terlihat jelas hanya berdasarkan inspeksi visual.

Warna brand tidak mengesampingkan readability requirement jika compliance merupakan target project.

## Color

Jangan gunakan color sebagai satu-satunya pembeda untuk informasi penting.

State seperti:

* error,
* success,
* warning,
* selected,
* status,
* atau priority

sebaiknya memiliki cue lain bila diperlukan.

Contoh:

* text,
* icon,
* shape,
* pattern,
* atau label.

## Target Interaksi

Untuk web yang menargetkan WCAG 2.2 AA:

pertimbangkan Target Size Minimum 24 × 24 CSS pixels atau pengecualian/spacing yang diizinkan standard.

Jangan membuat icon action kecil dan berdekatan tanpa hit area yang cukup.

Untuk touch-heavy product, target yang lebih besar dapat lebih sesuai.

## Reduced Motion

Jika UI memakai non-essential motion:

hormati reduced-motion preference jika platform mendukungnya.

Motion yang hanya dekoratif boleh dikurangi atau dihilangkan.

Jangan membuat functionality penting hanya dapat dipahami melalui animation.

WCAG juga merekomendasikan dukungan terhadap preferensi reduced motion untuk animation yang dipicu interaction. ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html))

## Motion

Gunakan motion untuk:

* feedback,
* continuity,
* spatial relationship,
* state transition,
* atau directing attention.

Jangan membuat setiap element:

* fade,
* slide,
* scale,
* parallax,
* spring,
* atau animate-on-scroll

tanpa alasan.

Motion tidak harus ada agar UI terlihat premium.

## Content Order

Pastikan DOM/source order masuk akal jika layout visual berbeda dari reading order.

Jangan menggunakan CSS ordering untuk menghasilkan reading order yang membingungkan assistive technology.

## Forms

Untuk form, periksa:

* label,
* instructions,
* required state,
* validation,
* error association,
* disabled state,
* submitting state,
* success/failure state,
* dan keyboard behavior

sesuai kebutuhan.

Jangan mengandalkan placeholder sebagai satu-satunya label.

MDN menekankan visible/associated labels untuk form control karena label memberi semantics untuk assistive technology dan memperbesar area interaction. ([MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/How_to_structure_a_web_form))

## Validation

Client-side validation digunakan untuk UX dan feedback cepat.

Jika backend/server merupakan authority:

jangan menganggap client validation sebagai security boundary.

Tampilkan error:

* dekat field atau action yang relevan,
* jelas,
* actionable,
* dan tidak bergantung pada color saja.

## Form Submission

Saat submit:

cegah duplicate action jika duplicate execution dapat menimbulkan masalah.

Gunakan pattern project seperti:

* disabled submit,
* pending state,
* request deduplication,
* idempotency server-side,
* atau optimistic update

sesuai kebutuhan.

Jangan disable semua UI secara berlebihan.

## Buttons dan Actions

Gunakan label action yang menjelaskan outcome.

Contoh:

`Simpan perubahan`

lebih jelas daripada:

`OK`

jika konteks membutuhkan kejelasan tersebut.

Namun jangan memaksa bahasa atau wording tertentu jika product sudah memiliki vocabulary sendiri.

Dalam satu decision area:

buat action hierarchy jelas.

Tidak ada aturan universal bahwa setiap section hanya boleh memiliki satu button.

## Links vs Buttons

Web:

link digunakan untuk navigation.

Button digunakan untuk action.

Jangan membuat link yang sebenarnya menjalankan mutation tanpa semantics/action pattern yang sesuai.

Jangan membuat button untuk navigation hanya karena styling lebih mudah.

## Dialog / Modal

Jika modal/dialog digunakan:

pastikan bila relevan:

* focus masuk ke dialog,
* focus tidak lolos ke background,
* Escape behavior benar,
* close action tersedia,
* focus kembali setelah ditutup,
* screen reader semantics tepat,
* dan body scroll behavior tidak rusak.

Jangan menggunakan modal untuk setiap flow jika inline UI lebih sederhana.

## Loading State

Gunakan loading state jika user perlu mengetahui bahwa operation masih berlangsung.

Pilih sesuai context:

* skeleton,
* spinner,
* progress,
* optimistic UI,
* placeholder,
* atau existing content retained.

Jangan mengganti seluruh layar dengan spinner untuk update kecil jika tidak diperlukan.

## Empty State

Empty state harus membantu user memahami:

* kenapa data kosong,
* apakah kondisi normal,
* dan tindakan berikutnya jika ada.

Jangan memaksa CTA pada empty state jika tidak ada action relevan.

## Error State

Error state harus sesuai severity.

Bedakan jika relevan:

* field error,
* local component error,
* network error,
* permission error,
* unavailable state,
* full-page failure.

Jangan mengubah seluruh halaman menjadi error state jika hanya satu widget gagal.

## Success State

Gunakan success feedback jika hasil action tidak terlihat langsung.

Jika perubahan sudah jelas pada UI:

toast tambahan mungkin tidak diperlukan.

Jangan menghasilkan notification noise untuk setiap interaction.

## Disabled State

Jangan disable control tanpa alasan yang dapat dipahami user.

Jika user perlu mengetahui mengapa action tidak tersedia:

beri explanation yang sesuai.

Jangan gunakan disabled sebagai pengganti authorization/security.

## Permission State

Jika UI bergantung pada permission:

frontend boleh menyembunyikan atau disable action untuk UX.

Backend/service tetap authority jika operation membutuhkan security enforcement.

Jangan menganggap hidden button berarti action sudah aman.

## Navigation

Pertahankan navigation model existing.

Perhatikan:

* current location,
* back behavior,
* deep linking,
* browser history,
* nested route,
* mobile navigation,
* focus after navigation,
* dan unsaved changes

jika relevan.

Jangan membuat custom navigation behavior yang melawan expectation platform tanpa kebutuhan.

## Component Architecture

Ikuti component architecture project.

Buat component baru jika:

* reuse nyata,
* responsibility jelas,
* complexity berkurang,
* atau testing/maintenance membaik.

Jangan memecah markup kecil menjadi banyak component hanya untuk abstraction.

Jangan membiarkan mega-component tumbuh jika beberapa responsibility benar-benar independen.

## Component API

Untuk shared component:

buat API yang:

* jelas,
* kecil,
* composable,
* konsisten,
* dan sulit disalahgunakan.

Jangan menambah banyak boolean props untuk setiap variasi jika composition atau variant system existing lebih sesuai.

Namun jangan membuat compound component architecture untuk kebutuhan sederhana.

## Design System

Jika design system tersedia:

reuse:

* components,
* tokens,
* variants,
* spacing,
* typography,
* icons,
* states,
* dan interaction patterns.

Jangan menyalin component lalu membuat versi lokal dengan sedikit perbedaan tanpa alasan.

Jika component system tidak memiliki capability yang diperlukan:

extend menggunakan pattern system tersebut.

## Styling

Gunakan styling approach existing.

Contoh:

* plain CSS,
* Sass,
* CSS Modules,
* utility classes,
* Tailwind,
* CSS-in-JS,
* design-token system,
* native styling API.

Jangan mencampur styling paradigm baru hanya untuk satu component.

## Tokens

Jika token tersedia:

gunakan token untuk:

* color,
* spacing,
* typography,
* radius,
* elevation,
* motion,
* z-index

sesuai design system.

Jangan hardcode nilai yang sudah memiliki semantic token.

Jangan membuat token baru untuk satu nilai yang tidak akan digunakan lagi.

## Z-Index

Jangan menaikkan z-index secara acak sampai UI terlihat benar.

Pahami stacking context dan layering system.

Gunakan layer/token existing jika tersedia.

## State Management

Gunakan state mechanism existing.

Bedakan kebutuhan:

* local component state,
* shared UI state,
* URL state,
* server/cache state,
* persistent state.

Jangan memindahkan local state ke global store tanpa kebutuhan.

Jangan menambah state-management library baru untuk beberapa nilai sederhana.

## Derived State

Jangan menyimpan state yang dapat dihitung dari source state tanpa alasan.

Derived state yang diduplikasi dapat menjadi stale.

## URL State

Untuk web, pertimbangkan URL sebagai state jika informasi perlu:

* shareable,
* bookmarkable,
* navigable,
* atau survive refresh.

Contoh:

* search,
* filter,
* pagination,
* selected resource

jika UX membutuhkannya.

Jangan memasukkan semua UI state ke URL.

## Data Fetching

Gunakan data-fetching pattern existing.

Perhatikan bila relevan:

* loading,
* stale data,
* caching,
* refetch,
* race condition,
* cancellation,
* error,
* retry,
* pagination,
* deduplication.

Jangan menambah data-fetching library jika native/existing solution cukup.

## Async Race

Untuk interaction async:

periksa apakah request lama dapat menimpa hasil baru.

Contoh:

* autocomplete,
* filter,
* live search,
* route change,
* rapidly changing selection.

Gunakan cancellation, request identity, stale check, atau mechanism framework/library bila diperlukan.

## Optimistic UI

Gunakan optimistic update hanya jika:

* failure rate cukup rendah,
* rollback dapat dilakukan,
* dan UX mendapat manfaat nyata.

Jangan menggunakan optimistic behavior untuk action berisiko tinggi tanpa recovery yang jelas.

## Server / Client Boundary

Jika framework membedakan server dan client execution:

ikuti boundary resmi framework dan pattern repository.

Jangan memindahkan code ke client hanya untuk mengakses browser API jika architecture memiliki cara yang lebih tepat.

Jangan membawa secret atau privileged logic ke browser bundle.

## Hydration

Jika project menggunakan hydration:

hindari mismatch antara server output dan client initial render.

Periksa source nondeterministic seperti:

* time,
* random,
* browser-only API,
* locale,
* client storage,
* atau viewport-dependent render

bila relevan.

## Internationalization

Jika project menggunakan i18n/localization:

jangan hardcode user-facing string di luar mechanism project.

Pertimbangkan:

* text expansion,
* pluralization,
* date,
* time,
* number,
* currency,
* directionality,
* dan locale-specific formatting.

Jangan mengasumsikan seluruh UI harus berbahasa Indonesia.

## Bahasa UI

Ikuti product language.

Jika product berbahasa Indonesia:

gunakan copy Indonesia natural.

Jika English:

gunakan English.

Jika multilingual:

gunakan localization system.

`human-language-indonesia.md` hanya relevan bila bahasa output/product memang Indonesia.

Jangan mengganti existing English UI menjadi Indonesia hanya karena rule file ditulis dalam bahasa Indonesia.

## Copy

Copy harus:

* jelas,
* spesifik,
* konsisten,
* dan sesuai vocabulary produk.

Jangan mengarang:

* statistic,
* testimonial,
* metric,
* guarantee,
* pricing claim,
* legal claim,
* atau product capability.

Gunakan placeholder yang jelas jika data belum tersedia.

## Anti-Generic / Anti-AI-Looking

Jangan mendefinisikan "AI-looking" berdasarkan satu efek visual.

Masalah utamanya adalah keputusan yang:

* generic,
* repetitif,
* tidak sesuai product,
* atau tidak memiliki fungsi.

Waspadai penggunaan berlebihan seperti:

* card identik,
* gradient besar,
* glow,
* glassmorphism,
* giant rounded panel,
* floating pill,
* generic hero,
* random icon,
* marketing copy kosong.

Elemen tersebut tidak dilarang.

Gunakan jika sesuai:

* brand,
* hierarchy,
* interaction,
* dan product context.

Jangan membuat UI sengaja aneh hanya untuk terlihat "human-designed."

## Color

Gunakan color sesuai system existing.

Color dapat menyampaikan:

* brand,
* hierarchy,
* state,
* category,
* priority,
* atau interaction.

Jangan menambah accent color tanpa melihat palette dan semantic roles.

## Icons

Gunakan icon set existing.

Jangan mencampur beberapa icon style tanpa alasan.

Jika icon action ambigu:

tambahkan label atau accessible name yang sesuai.

Jangan memakai icon hanya untuk dekorasi wajib di setiap card.

## Images dan Media

Untuk web, pertimbangkan bila relevan:

* intrinsic dimensions,
* responsive sources,
* format,
* compression,
* loading priority,
* alt text,
* aspect ratio,
* dan layout stability.

Jangan memberi alt text pada purely decorative image jika platform semantics menyediakan cara menandainya decorative.

Jangan lazy-load resource critical secara mekanis jika dapat memperburuk loading experience.

## Tables

Gunakan table untuk data tabular.

Jangan membuat seluruh layout menggunakan semantic table.

Untuk data table, pertimbangkan:

* header association,
* sorting,
* filtering,
* pagination/virtualization,
* horizontal overflow,
* responsive behavior,
* keyboard interaction

sesuai complexity.

Jangan mengubah table menjadi card stack di mobile jika hubungan kolom menjadi hilang tanpa alternatif.

## Large Lists

Untuk list besar:

gunakan pagination, incremental loading, windowing, atau virtualization hanya jika diperlukan.

Jangan memperkenalkan virtualization untuk 20 item hanya karena library tersedia.

## Performance

Performance optimization harus berdasarkan kebutuhan atau evidence.

Jangan menambah:

* memoization,
* lazy loading,
* code splitting,
* virtualization,
* prefetch,
* preload,
* cache,
* worker

secara mekanis.

Gunakan jika memberi manfaat nyata.

## Web Performance

Untuk project web, perhatikan jika relevan:

* loading performance,
* interaction responsiveness,
* layout stability,
* JavaScript execution,
* asset size,
* network waterfall,
* rendering,
* image/font loading.

Core Web Vitals dapat digunakan sebagai metric ketika sesuai dengan product goal.

Jangan mengarang performance target jika project belum menetapkannya.

Catat target planner/agent sebagai recommendation, bukan requirement user.

## Core Web Vitals

Untuk web performance work, metric utama saat ini mencakup:

* Largest Contentful Paint,
* Interaction to Next Paint,
* Cumulative Layout Shift.

Gunakan field/runtime measurement bila tersedia.

Jangan menyimpulkan performance hanya dari Lighthouse satu kali.

Untuk SPA, measurement soft navigation dapat memiliki behavior khusus dan perlu diinterpretasikan sesuai tooling/browser saat ini.

## Bundle

Jangan menambah dependency besar untuk functionality kecil tanpa mempertimbangkan bundle/runtime cost.

Gunakan bundle analyzer hanya jika size/performance memang menjadi masalah.

## Memoization

Jangan menambahkan memoization di setiap component/function.

Gunakan jika:

* computation mahal,
* reference stability diperlukan,
* atau profiling menunjukkan manfaat.

Memoization memiliki complexity dan maintenance cost.

## SEO

SEO hanya relevan bila surface dapat ditemukan melalui search dan product membutuhkan discoverability.

Jika relevan, pertimbangkan:

* document title,
* metadata,
* semantic structure,
* canonical URL,
* crawlability,
* structured data,
* rendering/indexability

sesuai project.

Jangan memaksakan SEO pada authenticated internal dashboard atau native UI.

## Browser Compatibility

Ikuti browser support project.

Jangan menggunakan API baru hanya karena tersedia pada browser agent.

Periksa support/polyfill bila feature harus bekerja pada target browser yang lebih luas.

## Progressive Enhancement

Gunakan progressive enhancement jika sesuai product dan platform.

Jangan membuat JavaScript dependency yang tidak diperlukan untuk functionality sederhana pada web.

Namun jangan memaksakan no-JavaScript behavior pada SPA/app yang product architecture-nya memang membutuhkan JavaScript.

## Offline

Offline behavior hanya direncanakan jika product membutuhkannya.

Jangan menambah service worker/PWA cache hanya karena project berjalan di browser.

## Security

Frontend bukan trusted security boundary.

Jangan menaruh:

* secret,
* private credential,
* privileged API key,
* server-only token

di client bundle.

Pertimbangkan bila relevan:

* XSS,
* unsafe HTML,
* URL handling,
* untrusted content,
* CSRF architecture,
* third-party script,
* token storage,
* postMessage,
* iframe,
* dependency risk.

Jangan mengklaim UI hiding sebagai authorization.

## Unsafe HTML

Hindari raw HTML rendering untuk untrusted content.

Jika project memang harus merender HTML user/external:

gunakan sanitization strategy yang sesuai.

Jangan membuat sanitizer ad-hoc jika library/platform yang teruji sudah tersedia.

## Third-Party Scripts

Sebelum menambah script pihak ketiga:

pertimbangkan:

* privacy,
* security,
* performance,
* failure,
* consent,
* dan loading behavior

sesuai project.

Jangan menambahkan analytics/tracker hanya karena umum digunakan.

## Privacy

Jangan mengumpulkan client-side telemetry tambahan tanpa requirement.

Jangan memasukkan sensitive data ke:

* URL,
* analytics event,
* console,
* local storage,
* atau client logs

tanpa kebutuhan dan review yang sesuai.

## Console

Jangan meninggalkan:

* debug `console.log`,
* development banner,
* debug UI,
* temporary alert,
* atau instrumentation sementara

pada production code kecuali logging tersebut memang bagian system.

## Error Boundary

Gunakan framework-specific error boundary jika:

* framework mendukung,
* scope kegagalan perlu diisolasi,
* dan existing architecture menggunakannya.

Jangan membuat error boundary di setiap component.

## Framework-Specific Rules

Setelah framework terdeteksi:

ikuti documentation dan best practice versi yang benar-benar digunakan.

Contoh:

React rules hanya untuk React.

Vue rules hanya untuk Vue.

Svelte rules hanya untuk Svelte.

Angular rules hanya untuk Angular.

Next.js rules hanya untuk Next.js.

Nuxt rules hanya untuk Nuxt.

Jangan mencampur convention framework lain.

## Current Documentation

Jika behavior framework/library:

* version-sensitive,
* baru berubah,
* deprecated,
* atau belum cukup yakin,

gunakan dokumentasi resmi/current.

Jangan mengandalkan memory model sebagai satu-satunya sumber.

## Framework-Managed Instructions

Jika framework/tool menambahkan instruction block sendiri:

hormati managed block yang berlaku.

Jangan rewrite manual jika generator akan menimpa perubahan.

Root/frontend rules tetap berfungsi sebagai baseline generic.

## Generated Code

Jangan edit generated frontend code jika source generator tersedia.

Contoh:

* generated routes,
* API client,
* type generation,
* design-token output,
* compiled CSS,
* build output.

Edit source yang benar.

## Testing

Gunakan testing setup existing.

Jenis validation frontend dapat mencakup:

* unit test,
* component test,
* integration test,
* E2E,
* browser test,
* visual regression,
* accessibility check,
* performance profiling,
* manual interaction.

Pilih sesuai risiko dan perubahan.

Jangan mewajibkan semua jenis test untuk setiap component.

## Component Test

Gunakan component test untuk behavior component yang cukup terisolasi jika project memiliki setup tersebut.

Jangan test implementation detail yang membuat refactor aman menjadi sulit.

## E2E

Gunakan E2E untuk flow penting yang melintasi beberapa layer.

Jangan membuat seluruh test suite E2E jika unit/integration lebih tepat.

## Browser Verification

Untuk perubahan visual atau interaction:

verifikasi di browser/runtime bila tool tersedia.

Periksa:

* layout,
* interaction,
* console,
* keyboard,
* responsive state,
* dan failure state

yang relevan.

Jangan menyatakan UI benar hanya karena TypeScript compile.

## Accessibility Test

Gunakan automated accessibility tooling jika tersedia.

Tetapi automated scan bukan bukti lengkap accessibility.

Lakukan manual check untuk interaction penting seperti:

* keyboard,
* focus,
* modal,
* navigation,
* label,
* dan reading order

bila relevan.

## Visual Regression

Gunakan screenshot/visual regression jika project memiliki tooling dan perubahan memang visual.

Jangan menambah visual-testing infrastructure untuk perubahan kecil kecuali kebutuhan project membenarkannya.

## Responsive Verification

Jangan hanya mengecek satu desktop dan satu mobile width.

Pilih viewport yang mewakili:

* boundary layout,
* narrow width,
* medium width,
* wide width,
* atau target device

yang relevan.

Periksa content stress seperti:

* teks panjang,
* translation,
* empty content,
* dense content.

## Performance Verification

Jika perubahan bertujuan memperbaiki performance:

ukur sebelum dan sesudah jika memungkinkan.

Jangan mengklaim:

"lebih cepat"

hanya karena code terlihat lebih optimal.

## Design Fidelity

Jika user memberikan:

* Figma,
* screenshot,
* design spec,
* component reference,

jadikan itu source of truth visual sesuai scope.

Jangan "memperbaiki" desain berdasarkan taste pribadi tanpa requirement.

Jika design bertentangan dengan accessibility atau feasibility:

laporkan trade-off dan cari solusi terdekat.

## Audit UI

Jika user meminta audit:

jangan langsung redesign.

Cari masalah berdasarkan impact.

Kategori dapat mencakup:

* broken interaction,
* accessibility,
* responsiveness,
* hierarchy,
* consistency,
* state coverage,
* performance,
* content clarity,
* visual regression,
* design-system drift.

Urutkan masalah terpenting lebih dulu.

## Output

Output mengikuti task.

Jangan selalu mengeluarkan:

* konsep UI 5–8 kalimat,
* struktur halaman,
* copy,
* design system,
* dan motion

untuk setiap pertanyaan.

## Pertanyaan Frontend Kecil

Jawab langsung dan fokus.

Contoh:

"kenapa button ini overflow?"

Tidak perlu mengeluarkan design concept lengkap.

## Implementasi

Jika user meminta coding:

implementasikan perubahan yang:

* konsisten dengan repository,
* responsive sesuai scope,
* accessible sesuai kebutuhan,
* dan terverifikasi.

Ringkas setelah selesai:

* apa yang berubah,
* file/area utama,
* validation,
* limitation bila ada.

## Desain / Redesign

Jika user memang meminta desain lengkap:

boleh berikan:

* visual direction,
* information hierarchy,
* component structure,
* interaction,
* copy,
* responsive behavior,
* state,
* accessibility,
* dan implementation notes

sesuai kebutuhan.

Jangan mengeluarkan kategori yang tidak relevan.

## Copy Only

Jika user hanya meminta copy:

fokus pada copy.

Jangan redesign component.

## Accessibility Audit

Jika user hanya meminta accessibility audit:

fokus pada:

* semantics,
* labels,
* keyboard,
* focus,
* contrast,
* target,
* motion,
* reading order,
* error communication,
* dan issue relevan lainnya.

Jangan mengganti brand/style tanpa kebutuhan.

## Performance Audit

Jika user meminta frontend performance:

ukur atau gunakan evidence bila tersedia.

Fokus pada bottleneck yang benar-benar memengaruhi experience.

Jangan menjadikan aesthetic preference sebagai performance recommendation.

## Cara Berpikir Sebelum Coding

Lakukan secara internal.

1. Platform/UI surface apa yang sedang diubah?
2. Framework dan styling system apa yang benar-benar digunakan?
3. Design system atau component apa yang harus direuse?
4. Apa task utama user pada layar ini?
5. State apa yang relevan?
6. Accessibility boundary apa yang perlu diperiksa?
7. Responsive behavior apa yang terdampak?
8. Data/state flow apa yang terkait?
9. Ada interaction async atau race?
10. Apa perubahan minimum?
11. Validation apa yang membuktikan hasil?

Jangan tampilkan private reasoning.

## Dynamic Scope

Jika task tidak melibatkan:

* form,
* table,
* animation,
* localization,
* performance,
* SEO,
* data fetching,
* accessibility tertentu,
* atau design system,

abaikan section tersebut.

Jangan menambah functionality hanya karena rules membahasnya.

## Prioritas Konflik

Untuk intent, scope dan keputusan kerja, ikuti instruksi eksplisit user terbaru, lalu aturan project yang berlaku, keputusan/checkpoint yang disepakati, dan default template. Tetap patuhi hierarchy instruksi host serta batas platform, permission, security dan kebijakan yang benar-benar enforced; jangan menonaktifkan pembatas tersebut untuk memenuhi permintaan. Untuk fakta implementasi, repository/config/test aktual mengungguli dokumentasi atau memory yang stale; fakta baru tidak otomatis membatalkan keputusan user.

Urutan umum:

1. system/platform/agent constraints,
2. latest explicit user instructions within those constraints,
3. applicable repository instructions,
4. project-specific rules,
5. design/source specification yang berlaku,
6. frontend rules ini,
7. framework convention,
8. generic frontend best practice.

Existing project pattern menang atas generic preference selama tidak menyebabkan bug, accessibility issue yang material, security issue, atau pelanggaran requirement.

## Aturan Revisi

Jika hasil terasa generic:

baca ulang context produk dan component existing.

Jangan memperbaikinya hanya dengan:

* gradient,
* font baru,
* lebih banyak card,
* border radius,
* animation,
* atau decorative element.

Cari penyebab nyata:

* hierarchy,
* layout,
* copy,
* interaction,
* data density,
* state,
* component choice,
* atau ketidaksesuaian dengan product identity.

## Final Check

Sebelum final, periksa secara internal:

* framework benar?
* existing design system dipakai?
* component reuse sudah dicek?
* visual hierarchy jelas?
* semantics sesuai platform?
* keyboard/focus relevan aman?
* labels benar?
* responsive behavior masuk akal?
* long/dynamic content aman?
* loading/error/empty state yang relevan ditangani?
* language/localization sesuai product?
* tidak ada secret client-side?
* tidak ada unsafe HTML?
* tidak ada debug residue?
* performance regression nyata?
* test/browser validation relevan sudah dilakukan?
* tidak ada redesign di luar scope?

Jangan tampilkan checklist ini kecuali diminta.

## Prinsip Akhir

Deteksi frontend, jangan menebak.

Ikuti framework dan design system repository.

Gunakan semantics native bila tersedia.

Accessibility adalah bagian dari correctness.

Responsive mengikuti content dan context.

State ditampilkan sesuai kebutuhan.

Copy mengikuti bahasa produk.

Motion memiliki fungsi.

Hindari desain generic karena tidak sesuai konteks, bukan karena daftar efek tertentu dilarang.

Jangan overengineer component atau state architecture.

Gunakan documentation current untuk framework yang berubah.

Verifikasi UI di runtime bila perubahan memang memengaruhi behavior atau tampilan.

Buat perubahan minimum yang benar.
