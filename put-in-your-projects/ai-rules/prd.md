# Product Requirements Document

Template Product Requirements Document untuk `[PROJECT_NAME]`.

PRD mendefinisikan:

* masalah yang ingin diselesaikan,
* siapa pengguna atau pihak yang menerima value,
* outcome yang ingin dicapai,
* scope produk,
* capability atau behavior yang dibutuhkan,
* constraint produk,
* ukuran keberhasilan,
* dan batas yang tidak boleh diperluas secara diam-diam.

PRD bukan implementation plan.

PRD tidak menentukan architecture, framework, database, folder structure, API detail, atau task breakdown kecuali keputusan tersebut memang LOCKED constraint yang memengaruhi produk.

Template ini bersifat:

* product-agnostic,
* framework-agnostic,
* platform-agnostic,
* architecture-agnostic,
* repository-aware,
* discovery-aware,
* dan AI-agent-readable.

Gunakan hanya section yang relevan.

Jangan menambah feature atau requirement hanya untuk mengisi template.

## 1. Prinsip Utama

PRD menjawab:

WHY

Mengapa produk atau perubahan ini diperlukan?

WHO

Siapa yang memiliki masalah atau kebutuhan?

WHAT

Outcome dan capability apa yang perlu diberikan?

HOW DO WE KNOW

Bagaimana kita tahu hasilnya berhasil?

PRD bukan tempat utama menjawab:

HOW TO IMPLEMENT

Bagaimana architecture atau source code dibangun?

Detail tersebut masuk ke:

* SRS,
* technical specification,
* architecture document,
* task plan,
* GRAND-PLAN,
* atau implementation notes

sesuai workflow project.

## 2. Source of Truth

Untuk product intent:

PRD yang sudah disetujui menjadi source of truth product scope.

Untuk current implementation:

repository aktual tetap menjadi source of truth.

Jangan menganggap:

"tertulis di PRD"

berarti:

"sudah diimplementasikan."

Untuk project existing, bedakan:

CURRENT STATE

Apa yang benar-benar tersedia sekarang.

TARGET STATE

Apa yang harus tersedia setelah scope ini selesai.

GAP

Perbedaan antara keduanya.

## 3. Classification

Gunakan label berikut bila membantu.

CONFIRMED

Informasi yang diberikan atau disetujui user/stakeholder.

LOCKED

Keputusan yang tidak boleh diubah tanpa approval.

PROPOSED

Usulan yang belum final.

ASSUMPTION

Asumsi sementara.

UNKNOWN

Belum diketahui.

DEFERRED

Sengaja ditunda.

OUT OF SCOPE

Secara eksplisit tidak masuk scope sekarang.

Jangan menulis ASSUMPTION atau PROPOSED seolah-olah merupakan keputusan user.

## 4. Metadata

Gunakan metadata secukupnya.

```text
Project:
Document:
Scope:
Status:
Owner:
Version:
Last Updated:
Target Release / Milestone:
Related Documents:
```

Status dapat berupa:

```text
DRAFT
IN REVIEW
APPROVED
SUPERSEDED
```

Jangan mengarang:

* owner,
* date,
* release,
* organization,
* approval,
* atau version

jika belum diketahui.

# 1. Executive Summary

Jelaskan dalam beberapa paragraf singkat:

* apa yang ingin dibuat atau diubah,
* siapa yang mendapat manfaat,
* masalah utama,
* outcome utama,
* dan batas scope.

Gunakan bahasa product.

Jangan membuka PRD dengan:

* framework,
* database,
* endpoint,
* folder,
* controller,
* atau technical stack

kecuali hal tersebut memang merupakan constraint utama.

# 2. Problem

## 2.1 Problem Statement

Tuliskan masalah yang sedang dialami user/business/system.

Format contoh:

```text
[USER / ACTOR] saat ini kesulitan [PROBLEM]
ketika [CONTEXT], sehingga [IMPACT].
```

Hindari problem statement seperti:

```text
Kita belum punya dashboard.
```

jika masalah sebenarnya adalah:

```text
Operator tidak dapat mengetahui transaksi bermasalah tanpa memeriksa beberapa sistem secara manual.
```

Feature yang belum ada bukan selalu problem.

## 2.2 Evidence

Jika tersedia, sertakan evidence seperti:

* user feedback,
* support issue,
* analytics,
* operational data,
* research,
* sales feedback,
* usability finding,
* incident,
* market evidence.

Jangan mengarang evidence.

## 2.3 Current Workaround

Jika user sudah menyelesaikan masalah dengan cara lain:

dokumentasikan.

Contoh:

* spreadsheet,
* manual approval,
* beberapa aplikasi,
* script,
* email,
* command line,
* proses offline.

Workaround membantu memahami kebutuhan nyata.

# 3. Opportunity

Jelaskan mengapa masalah ini layak diselesaikan sekarang.

Dapat mencakup:

* user value,
* business value,
* operational improvement,
* risk reduction,
* cost reduction,
* revenue opportunity,
* retention,
* compliance,
* strategic alignment.

Jangan membuat business justification palsu.

# 4. Target Users / Actors

Jangan mengasumsikan semua produk memiliki akun user.

Actor dapat berupa:

* end user,
* operator,
* admin,
* customer,
* developer,
* API consumer,
* external service,
* organization,
* device,
* automation,
* model,
* internal team.

Untuk setiap actor penting:

```text
Actor:
Context:
Goal:
Pain Point:
Relevant Capability:
```

Jangan membuat persona dekoratif yang tidak mengubah keputusan produk.

# 5. Jobs / User Needs

Dokumentasikan apa yang sebenarnya ingin dicapai user.

Contoh:

```text
Saat [situasi],
user ingin [job],
agar [outcome].
```

Fokus pada outcome.

Jangan langsung menerjemahkan semua need menjadi feature tertentu.

# 6. Product Outcome

Definisikan outcome yang ingin dicapai.

Contoh:

```text
Operator dapat mengetahui transaksi bermasalah tanpa berpindah sistem.
```

lebih baik daripada:

```text
Buat dashboard transaksi.
```

Outcome menjelaskan perubahan yang ingin terjadi.

Feature adalah salah satu cara mencapainya.

# 7. Goals

Pisahkan:

## 7.1 Primary Goals

Outcome utama yang harus tercapai.

## 7.2 Secondary Goals

Outcome tambahan yang bernilai tetapi bukan alasan utama project.

Jangan membuat terlalu banyak primary goals.

Jika semuanya prioritas:

tidak ada prioritas.

# 8. Non-Goals

Tuliskan hal yang sengaja tidak dikerjakan pada scope ini.

Contoh:

```text
- Tidak mengganti authentication provider.
- Tidak membuat mobile native application.
- Tidak mencakup historical data sebelum 2025.
```

Non-goal mencegah scope creep.

Jangan memasukkan UNKNOWN sebagai non-goal.

# 9. Success Metrics

Setiap metric harus berhubungan dengan outcome.

Format:

| Outcome | Metric | Baseline | Target | Measurement |
| ------- | ------ | -------- | ------ | ----------- |

Contoh metric:

* task completion rate,
* conversion,
* time-to-complete,
* error rate,
* support volume,
* adoption,
* retention,
* processing time,
* failure rate,
* user satisfaction.

Jangan mengarang baseline atau target.

Jika target belum disepakati:

gunakan:

`TBD`

atau:

`RECOMMENDED TARGET`

dengan label yang jelas.

# 10. Guardrail Metrics

Jika improvement pada satu metric dapat merusak hal lain:

definisikan guardrail.

Contoh:

Meningkatkan conversion tidak boleh meningkatkan:

* refund rate,
* error rate,
* support complaint,
* latency

di atas batas yang disepakati.

Gunakan hanya jika relevan.

# 11. Scope

Gunakan scope yang jelas.

## MUST HAVE

Capability minimum untuk mencapai outcome utama.

## SHOULD HAVE

Bernilai dan penting tetapi tidak menghalangi core outcome.

## COULD HAVE

Nice-to-have.

## OUT OF SCOPE

Tidak dikerjakan sekarang.

Jangan mengubah COULD menjadi requirement implementation diam-diam.

# 12. Product Capabilities

Feature/capability mengikuti kebutuhan produk.

Jangan menggunakan feature universal seperti:

* User Management,
* Dashboard,
* CRUD,
* Export,
* Report,
* Notification

pada setiap PRD.

Gunakan hanya capability yang memang diperlukan.

Contoh:

```text
Capability: Search project

User value:
User dapat menemukan project yang relevan tanpa membuka semua project satu per satu.

Requirements:
- pencarian berdasarkan nama,
- hasil diperbarui sesuai query,
- empty state jelas,
- permission tetap dihormati.
```

# 13. Feature Requirement Format

Untuk feature utama:

```text
Feature:
Objective:
User Value:
Description:
Priority:
Requirements:
Dependencies:
Edge Cases:
Acceptance Criteria:
Out of Scope:
```

Gabungkan atau hilangkan field yang tidak memberi nilai.

Jangan membuat boilerplate identik untuk feature kecil.

# 14. User Stories

User story bersifat opsional.

Gunakan jika membantu product team.

Format:

```text
Sebagai [ACTOR],
saya ingin [CAPABILITY],
agar [OUTCOME].
```

User story bukan pengganti requirement.

Jangan membuat user story palsu untuk system-to-system capability jika format lain lebih jelas.

# 15. Core User Flow

Dokumentasikan flow produk penting.

Contoh:

```text
Search
->
Review Result
->
Open Detail
->
Take Action
```

Gunakan flow hanya untuk behavior yang benar-benar membantu pemahaman.

Jangan memasukkan internal implementation flow.

# 16. Alternate and Failure Flows

Untuk flow penting:

pertimbangkan kondisi seperti:

* empty,
* unauthorized,
* invalid input,
* unavailable dependency,
* duplicate action,
* cancellation,
* offline,
* partial success.

Tidak semua flow membutuhkan seluruh state.

# 17. UX Requirements

Jika UI merupakan bagian produk:

definisikan requirement experience.

Contoh:

* informasi utama harus dapat ditemukan,
* primary action jelas,
* user dapat kembali tanpa kehilangan context,
* critical state memiliki feedback,
* keyboard support jika required,
* responsive behavior sesuai target device.

Jangan menduplikasi seluruh Figma/design spec.

# 18. Design References

Jika ada:

* Figma,
* screenshot,
* prototype,
* existing design system,
* competitor reference,

cantumkan sebagai reference.

Reference bukan izin untuk menyalin produk lain.

# 19. Content and Copy Requirements

Gunakan jika copy merupakan bagian penting produk.

Dokumentasikan:

* terminology,
* language,
* tone,
* localization,
* legal copy,
* error wording

yang memang menjadi requirement.

Jangan hardcode seluruh UI copy pada PRD jika copy masih menjadi bagian design.

# 20. Permissions and Roles

Section ini CONDITIONAL.

Gunakan hanya jika produk memang memiliki authorization/permission behavior.

Jangan membuat role:

Admin
User

secara otomatis.

Definisikan:

* actor,
* capability,
* restriction,
* ownership

berdasarkan kebutuhan nyata.

# 21. Data Product Requirements

Gunakan jika product behavior bergantung pada data.

Dokumentasikan:

* data yang dibutuhkan user,
* source of truth produk,
* freshness,
* visibility,
* ownership,
* lifecycle,
* retention requirement

jika relevan.

Jangan mendesain database schema di PRD.

# 22. Search / Filter / Sort

Section ini hanya digunakan jika capability tersebut memang diperlukan.

Jangan memasukkan:

* filter,
* sorting,
* pagination

ke setiap list hanya karena aplikasi memiliki banyak data.

Definisikan berdasarkan use case.

# 23. Import / Export

Gunakan hanya jika user benar-benar membutuhkan data exchange.

Dokumentasikan:

* tujuan,
* format,
* limits,
* error behavior,
* privacy/security expectation

pada level product.

Jangan mengarang CSV/export feature.

# 24. Notification

Gunakan hanya jika notification mendukung outcome.

Definisikan:

* event,
* audience,
* urgency,
* channel requirement,
* user control

jika relevan.

Jangan menambah email/push hanya karena feature terasa belum lengkap.

# 25. Analytics

Bedakan:

PRODUCT ANALYTICS

Untuk memahami behavior/outcome user.

OPERATIONAL OBSERVABILITY

Untuk menjaga system berjalan.

PRD biasanya fokus pada product analytics yang diperlukan untuk mengukur success.

Jangan memasukkan full observability stack ke PRD kecuali menjadi product requirement.

# 26. Product Events

Jika success metrics membutuhkan instrumentation:

definisikan event pada level produk.

Contoh:

```text
project_search_performed
project_opened_from_search
```

Jangan menentukan library analytics kecuali locked.

# 27. Platform Requirements

Gunakan jika produk memiliki target platform tertentu.

Contoh:

* web,
* mobile,
* desktop,
* browser extension,
* CLI,
* API,
* embedded device.

Definisikan platform behavior yang memengaruhi user/product.

Jangan memilih framework di sini tanpa constraint.

# 28. Device / Browser Support

Gunakan bila relevan.

Contoh:

```text
Target:
modern evergreen browsers
```

atau daftar explicit yang memang ditentukan organisasi.

Jangan mengarang compatibility target.

# 29. Accessibility

Jika user-facing product membutuhkan accessibility:

tentukan expectation produk.

Contoh:

```text
Public web interface menargetkan WCAG 2.2 AA.
```

Implementation detail tetap berada di frontend spec/rules.

Jangan mengklaim compliance tanpa verification.

# 30. Performance Expectations

Masukkan hanya performance yang dirasakan user atau memengaruhi product outcome.

Contoh:

* page responsiveness,
* search response,
* video startup,
* processing completion,
* interaction latency.

Jangan menulis:

```text
App harus cepat.
```

Jika target belum tersedia:

tandai TBD.

# 31. Reliability Expectations

Jika reliability memengaruhi product:

definisikan expected behavior.

Contoh:

```text
Submission tidak boleh hilang ketika user melakukan retry setelah timeout.
```

Jangan mendesain retry architecture di PRD.

# 32. Privacy

Jika product mengolah personal/sensitive data:

definisikan requirement produk seperti:

* data yang dikumpulkan,
* user control,
* visibility,
* retention,
* deletion,
* consent,
* export.

Implementation security detail dapat masuk SRS/technical spec.

# 33. Security Product Requirements

Gunakan behavior yang terlihat atau contract produk.

Contoh:

```text
User tidak boleh melihat data organisasi lain.
```

Jangan menulis detail:

```text
Gunakan middleware X pada controller Y.
```

# 34. Compliance

Gunakan hanya jika ada regulation, contract, atau policy nyata.

Cantumkan source.

Jangan mengarang:

* GDPR,
* HIPAA,
* PCI DSS,
* ISO,
* SOC 2

sebagai requirement hanya karena produk mengolah data.

# 35. Technical Constraints

Bagian ini hanya untuk keputusan teknis yang benar-benar dikunci.

Contoh valid:

```text
Three.js langsung: LOCKED BY USER.
```

```text
Deployment harus berjalan di existing AWS environment.
```

```text
Must remain compatible with existing REST API v2.
```

Jangan membuat section:

Frontend:
`[STACK_FRONTEND]`

Backend:
`[STACK_BACKEND]`

Database:
`[DATABASE]`

sebagai kewajiban universal.

# 36. Existing Technology

Untuk project existing:

boleh dokumentasikan technology yang memengaruhi product delivery.

Gunakan status:

```text
EXISTING PROJECT
```

Bukan product requirement kecuali tidak boleh berubah.

# 37. Constraints

Constraint dapat berasal dari:

* technology,
* organization,
* compatibility,
* regulation,
* deadline,
* budget,
* platform,
* device,
* contract,
* resource.

Setiap constraint material sebaiknya memiliki reason/source.

# 38. Dependencies

Dokumentasikan dependency yang dapat menghalangi atau mengubah delivery.

Contoh:

* external API,
* design,
* legal approval,
* data availability,
* another team,
* vendor,
* infrastructure,
* upstream feature.

Jangan membuat implementation dependency detail yang lebih cocok di task plan.

# 39. Assumptions

Catat assumption yang memengaruhi keputusan produk.

Format:

| Assumption | Impact if Wrong | Validation |
| ---------- | --------------- | ---------- |

Jangan membiarkan assumption menjadi fakta permanen.

# 40. Risks

Untuk risk material:

| Risk | Impact | Likelihood | Mitigation |
| ---- | ------ | ---------- | ---------- |

Likelihood:

```text
LOW
MEDIUM
HIGH
```

cukup.

Jangan membuat probability palsu seperti:

`73%`.

# 41. Open Questions

Catat unresolved question.

Pisahkan:

BLOCKING

dan

NON-BLOCKING.

Jangan menyembunyikan keputusan yang belum dibuat.

# 42. Product Decisions

Gunakan decision log kecil untuk keputusan produk material.

Format:

```text
Decision:
Reason:
Source:
Date:
```

Source dapat berupa:

* USER,
* PRODUCT,
* RESEARCH,
* CONSTRAINT.

Jangan memenuhi log dengan keputusan kecil.

# 43. MVP

MVP berarti versi minimum yang cukup untuk:

* menguji outcome,
* memberi value nyata,
* atau mengurangi uncertainty penting.

MVP bukan:

"semua feature Phase 1 yang kebetulan ingin dibuat."

Jangan menambah auth, dashboard, reporting, notification, analytics, atau administration hanya karena aplikasi lain memilikinya.

# 44. Release Scope

Untuk setiap release/milestone jika diperlukan:

```text
Release:
Outcome:
Included Scope:
Excluded Scope:
Success Signal:
Dependencies:
```

Release detail harus mengikuti strategy project.

Jangan memaksakan tiga phase.

# 45. Priority

Gunakan priority scheme jika membantu.

Contoh:

```text
MUST
SHOULD
COULD
```

atau:

```text
P0
P1
P2
```

Definisikan artinya.

Jangan membuat Phase 1 / Phase 2 / Phase 3 universal.

# 46. Sequencing

Urutan delivery sebaiknya mengikuti:

* dependency,
* value,
* risk reduction,
* learning,
* user flow,
* dan feasibility.

Implementation phase detail berada di plan/task document.

# 47. Timeline

Timeline bersifat conditional.

Jangan mengarang:

```text
MVP selesai dalam X minggu
```

jika belum ada:

* scope stabil,
* resource,
* dependency,
* capacity,
* technical discovery.

Jika timeline berasal dari user:

pertahankan.

Jika planner memberi estimate:

label:

`ESTIMATE`

dan jelaskan assumption.

# 48. Release Criteria

Definisikan kapan product scope siap dilepas.

Contoh:

* must-have capability selesai,
* acceptance criteria terpenuhi,
* critical defect tidak ada,
* critical user flow validated,
* migration/dependency ready,
* required approval selesai.

Jangan menggunakan:

```text
Tidak ada defect critical.
```

tanpa mendefinisikan severity jika itu menjadi formal gate.

# 49. Acceptance Criteria

Acceptance criteria harus observable.

Contoh:

```text
Ketika user mencari "invoice",
hasil yang memiliki "invoice" pada field yang disepakati muncul sesuai permission user.
```

Hindari:

```text
Search bekerja dengan baik.
```

# 50. Product Acceptance vs Technical Verification

PRODUCT ACCEPTANCE

Menjawab:

apakah behavior/outcome produk benar?

TECHNICAL VERIFICATION

Menjawab:

apakah implementation memenuhi technical/system requirement?

PRD fokus pada product acceptance.

SRS/testing plan dapat menangani technical verification lebih detail.

# 51. Edge Cases

Masukkan edge case yang mengubah product behavior.

Contoh:

* user tidak memiliki data,
* permission berubah,
* duplicate request,
* connection terputus,
* item dihapus oleh user lain,
* external integration unavailable.

Jangan membuat exhaustive speculative list.

# 52. Existing Product Mode

Jika PRD digunakan untuk existing product:

dokumentasikan:

CURRENT EXPERIENCE

TARGET EXPERIENCE

UNCHANGED BEHAVIOR

MIGRATION / COMPATIBILITY EXPECTATION

jika relevan.

Jangan mendeskripsikan current behavior berdasarkan asumsi.

Periksa implementation, analytics, design, atau user flow aktual jika tersedia.

# 53. New Product Mode

Untuk new product:

hindari fake implementation detail.

Fokus pada:

* problem,
* user,
* outcome,
* scope,
* capability,
* metric,
* risk,
* constraint.

File path, endpoint, schema, dan component belum perlu ada.

# 54. Feature PRD Mode

PRD dapat hanya membahas satu feature.

Tidak harus seluruh produk.

Contoh:

```text
Scope:
Project Search v1
```

Dokumen harus fokus pada outcome feature tersebut.

Jangan menyalin seluruh company/product vision bila tidak diperlukan.

# 55. Internal Tool Mode

Internal product tetap membutuhkan user/outcome.

User dapat berupa:

* operator,
* support,
* finance,
* developer,
* analyst,
* admin.

Jangan menganggap internal tool cukup dijelaskan sebagai CRUD.

# 56. API / Developer Product Mode

Jika produk adalah API, SDK, atau developer tool:

product user dapat berupa developer.

Product requirements dapat mencakup:

* discoverability,
* consistency,
* error semantics,
* onboarding,
* backward compatibility,
* documentation,
* DX,
* latency.

Jangan memaksa UI requirements.

# 57. CLI Product Mode

Jika product berupa CLI:

fokus pada:

* commands,
* workflows,
* output clarity,
* scripting,
* exit behavior,
* discoverability,
* compatibility.

Jangan membuat dashboard/form requirement.

# 58. AI Product Mode

Jika produk menggunakan AI:

tambahkan section hanya jika relevan.

Dapat mencakup:

* user job,
* AI role,
* expected output,
* acceptable failure,
* uncertainty,
* human review,
* evaluation,
* latency,
* cost experience,
* privacy.

Jangan menetapkan provider/model jika belum LOCKED.

# 59. Marketplace / Multi-Sided Product

Jika memiliki beberapa user side:

dokumentasikan outcome masing-masing.

Jangan mengoptimalkan satu side tanpa melihat efek pada side lain.

# 60. Product Research

Jika external research dilakukan:

ringkas hanya insight yang mengubah product decision.

Format:

```text
Finding:
Evidence:
Product Impact:
Decision:
```

Jangan menempel raw search dump.

# 61. Competitor Research

Kompetitor digunakan untuk memahami:

* user expectation,
* workflow,
* gap,
* terminology,
* benchmark experience.

Jangan menyalin feature hanya karena competitor memilikinya.

Feature competitor bukan requirement otomatis.

# 62. Evidence vs Assumption

Bedakan:

EVIDENCE

Didukung source/data/user.

ASSUMPTION

Masih perlu divalidasi.

Jangan menggunakan wording pasti untuk assumption.

# 63. Discovery Status

Jika PRD masih memiliki uncertainty besar:

status dapat menjadi:

```text
DISCOVERY
```

Tidak harus memaksa PRD menjadi APPROVED.

Coding agent tidak boleh mengimplementasikan unresolved proposal sebagai locked requirement.

# 64. Relationship dengan BRD

`brd.md` menjawab terutama:

* business problem,
* business objective,
* stakeholder,
* organizational value,
* business constraint.

PRD tidak perlu menyalin BRD penuh.

# 65. Relationship dengan SRS

`srs.md` menerjemahkan product need menjadi system/software requirement yang lebih formal dan verifiable.

PRD tidak perlu memuat:

* protocol detail,
* schema,
* system interface,
* detailed quality specification

jika SRS menangani hal tersebut.

# 66. Relationship dengan GRAND-PLAN

`GRAND-PLAN.md` menggabungkan:

* product scope,
* architecture,
* implementation phases,
* task,
* testing,
* dependency,
* handoff.

PRD tetap fokus product.

Jangan menjadikan PRD sebagai implementation roadmap penuh.

# 67. Relationship dengan Task

`task.md` menjawab:

* apa yang dikerjakan sekarang,
* file/area,
* dependency,
* validation,
* implementation acceptance.

PRD tidak menyimpan seluruh task breakdown.

# 68. Relationship dengan Design

Figma/design spec adalah source of truth visual bila project menetapkannya.

PRD menyimpan:

* experience requirement,
* user flow,
* product behavior.

Jangan menduplikasi seluruh visual specification.

# 69. Relationship dengan Analytics

PRD menentukan:

* apa yang ingin diukur,
* success metric,
* product event jika diperlukan.

Implementation analytics detail berada di technical plan.

# 70. AI Coding Agent Usage

Saat AI coding agent menggunakan PRD:

1. Identifikasi scope task.
2. Baca hanya section PRD yang relevan.
3. Pertahankan CONFIRMED dan LOCKED decisions.
4. Jangan implementasikan OUT OF SCOPE.
5. Jangan mengubah PROPOSED menjadi CONFIRMED.
6. Gunakan repository untuk current implementation.
7. Gunakan acceptance criteria sebagai product behavior target.
8. Muat SRS/technical rules bila implementation membutuhkan detail system.
9. Laporkan conflict antara PRD dan repository.
10. Jangan menambah feature karena template menyebutnya.

# 71. Context Efficiency untuk AI Agent

Jika PRD besar:

agent tidak harus membaca seluruh document untuk setiap task.

Pada onboarding:

pahami:

* problem,
* goals,
* scope,
* users,
* constraints,
* feature map.

Pada task tertentu:

ambil:

* feature terkait,
* requirements,
* flow,
* dependencies,
* acceptance criteria,
* relevant quality constraint.

Gunakan heading/feature ID sebagai retrieval anchor.

# 72. Product Requirement ID

Untuk product kompleks, requirement/capability boleh memiliki ID.

Contoh:

```text
PRD-SEARCH-01
PRD-CHECKOUT-03
```

Gunakan jika traceability memberi nilai.

Jangan menambah ID pada setiap bullet di project kecil.

# 73. Traceability

Jika project membutuhkan traceability:

hubungkan:

```text
Problem / Goal
->
Product Capability
->
SRS Requirement
->
Implementation Task
->
Verification
```

Tidak semua project membutuhkan formal matrix.

# 74. Requirement Quality Check

Sebelum requirement dianggap siap:

periksa secara internal:

* terkait problem/outcome?
* user/actor jelas?
* scope jelas?
* behavior dapat dipahami?
* tidak mengunci implementation tanpa alasan?
* acceptance observable?
* tidak duplikat?
* priority masuk akal?
* assumption terlihat?
* tidak bertentangan dengan non-goal?

Jangan tampilkan checklist ini kecuali diminta.

# 75. PRD Quality Gate

Sebelum PRD dinyatakan siap:

periksa:

PROBLEM

Masalah jelas dan bukan sekadar daftar feature.

USER

Pihak yang menerima value jelas.

OUTCOME

Perubahan yang ingin dicapai jelas.

SUCCESS

Ada cara mengetahui keberhasilan.

SCOPE

Must-have dan out-of-scope jelas.

ASSUMPTIONS

Tidak menyamar sebagai fakta.

RISKS

Risiko material terlihat.

DEPENDENCIES

Dependency penting terlihat.

CONSTRAINTS

Technical preference tidak berubah menjadi locked constraint tanpa alasan.

IMPLEMENTATION LEAKAGE

PRD tidak berubah menjadi architecture document.

NO GENERIC FEATURES

Tidak ada auth/dashboard/report/export hanya karena template.

NO FAKE METRIC

Tidak ada target angka tanpa dasar.

NO FAKE TIMELINE

Tidak ada durasi tanpa assumption/resource.

AI READINESS

Coding agent dapat membedakan requirement, proposal, dan current implementation.

# 76. Minimal PRD

Untuk product/feature kecil, cukup:

```text
1. Problem
2. Target User
3. Outcome
4. Goals / Non-Goals
5. Scope
6. Requirements
7. Acceptance Criteria
8. Success Metric
9. Assumptions / Risks
10. Open Questions
```

Jangan membuat PRD 70 section untuk perubahan kecil.

# 77. Detailed PRD

Untuk product kompleks:

tambahkan section relevan seperti:

* stakeholders,
* user segments,
* research evidence,
* flows,
* UX,
* permissions,
* data,
* privacy,
* compliance,
* analytics,
* platform,
* release strategy,
* dependencies,
* risks,
* rollout,
* migration,
* AI,
* localization.

# 78. Jangan Dilakukan

Jangan:

* mengarang user,
* mengarang pain point,
* mengarang metric,
* mengarang timeline,
* mengarang technical stack,
* membuat auth sebagai feature universal,
* membuat CRUD sebagai feature universal,
* membuat dashboard sebagai feature universal,
* membuat report/export sebagai feature universal,
* membuat backend/frontend section wajib,
* mengunci controller/service/schema di PRD,
* menulis implementation plan lengkap,
* membuat tiga phase secara mekanis,
* menganggap semua project memiliki database,
* atau memperluas scope hanya agar produk terlihat lengkap.

# 79. Prinsip Akhir

Mulai dari problem.

Identifikasi user.

Definisikan outcome.

Tentukan success metric.

Tetapkan scope.

Nyatakan non-goal.

Feature harus mendukung outcome.

Jangan menganggap feature populer sebagai requirement.

PRD menjelaskan apa dan mengapa.

SRS memperjelas requirement sistem.

Architecture/spec menjelaskan bagaimana.

Task menjelaskan pekerjaan implementasi.

Repository menunjukkan current implementation.

Gunakan technical constraint hanya jika benar-benar dikunci.

Gunakan struktur adaptif.

Jangan membuat PRD lebih panjang daripada nilai yang diberikannya.

PRD yang baik membuat manusia dan AI agent memahami produk yang harus diwujudkan tanpa mendesain implementation secara prematur.
