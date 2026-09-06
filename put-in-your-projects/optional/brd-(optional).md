# Business Requirements Document

Template Business Requirements Document untuk `[PROJECT_NAME]`.

BRD mendefinisikan alasan bisnis sebuah perubahan, outcome yang ingin dicapai, stakeholder yang terdampak, scope bisnis, constraint, business requirement, business rule, success measure, dan kondisi transisi yang relevan.

BRD bukan implementation specification.

BRD tidak menentukan framework, database, API, controller, component, architecture, schema, atau task implementation kecuali suatu teknologi memang merupakan business constraint yang sudah dikunci.

Template ini bersifat:

* business-domain-agnostic,
* product-agnostic,
* framework-agnostic,
* platform-agnostic,
* architecture-agnostic,
* organization-aware,
* project-size-aware,
* dan AI-agent-readable.

Gunakan hanya section yang relevan.

Jangan menambah proses, stakeholder, role, feature, atau requirement hanya untuk mengisi template.

## 1. Fungsi BRD

BRD menjawab terutama:

WHY

Mengapa perubahan ini perlu dilakukan?

WHAT BUSINESS OUTCOME

Outcome bisnis apa yang harus tercapai?

WHO

Stakeholder mana yang membutuhkan, memengaruhi, atau terdampak?

WHAT BUSINESS NEED

Kondisi atau capability bisnis apa yang diperlukan?

WHAT BOUNDARY

Apa yang termasuk dan tidak termasuk dalam initiative?

HOW DO WE KNOW

Bagaimana organisasi mengetahui perubahan berhasil?

BRD bukan tempat utama menjawab:

HOW TO BUILD IT

Detail tersebut berada pada dokumen seperti:

* PRD,
* SRS,
* architecture specification,
* GRAND-PLAN,
* technical design,
* atau task plan.

## 2. Business Requirement vs Solution Requirement

Bedakan requirement berdasarkan level.

BUSINESS REQUIREMENT

Menjelaskan:

* goal,
* objective,
* outcome,
* business need,
* atau alasan perubahan dilakukan.

STAKEHOLDER REQUIREMENT

Menjelaskan kebutuhan stakeholder yang harus dipenuhi agar business outcome tercapai.

SOLUTION REQUIREMENT

Menjelaskan capability atau quality solusi.

Dapat berupa:

* functional,
* non-functional,
* interface,
* security,
* performance,
* atau technical behavior.

TRANSITION REQUIREMENT

Menjelaskan capability atau kondisi sementara yang diperlukan untuk berpindah dari current state ke future state.

Contoh:

* migration,
* training,
* data conversion,
* rollout,
* temporary compatibility.

BRD terutama berfokus pada:

BUSINESS REQUIREMENT

dan bila membantu:

STAKEHOLDER REQUIREMENT

serta:

TRANSITION REQUIREMENT.

Detail SOLUTION REQUIREMENT biasanya ditempatkan pada PRD/SRS.

Jangan membuat BRD menjadi SRS kedua.

## 3. Source of Truth

Untuk business intent yang sudah disetujui:

BRD menjadi source of truth business-level.

Untuk product behavior:

gunakan PRD bila tersedia.

Untuk detailed software/system requirements:

gunakan SRS bila tersedia.

Untuk current implementation:

repository aktual tetap menjadi source of truth.

Jangan menganggap:

"tertulis dalam BRD"

berarti:

"sudah diimplementasikan."

## 4. Classification

Gunakan status bila membantu:

CONFIRMED

Informasi yang telah dikonfirmasi stakeholder.

LOCKED

Constraint atau keputusan yang tidak boleh diubah tanpa approval.

PROPOSED

Usulan yang belum disetujui.

ASSUMPTION

Asumsi sementara.

UNKNOWN

Belum diketahui.

DEFERRED

Keputusan sengaja ditunda.

OUT OF SCOPE

Secara eksplisit tidak termasuk initiative.

Jangan menulis PROPOSED atau ASSUMPTION sebagai fakta.

## 5. Metadata

Gunakan metadata secukupnya.

```text
Project:
Document:
Document ID:
Status:
Business Owner:
Prepared By:
Version:
Last Updated:
Target Initiative / Milestone:
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
* stakeholder,
* date,
* approval,
* document ID,
* atau milestone.

Jika informasi belum tersedia:

gunakan `TBD` atau hilangkan field tersebut.

# 1. Executive Summary

Ringkas:

* perubahan apa yang sedang dipertimbangkan,
* business problem atau opportunity,
* siapa yang terdampak,
* business outcome utama,
* dan scope besarnya.

Jangan membuka BRD dengan:

* technology stack,
* database,
* UI,
* endpoint,
* atau architecture.

# 2. Business Context

## 2.1 Current Situation

Jelaskan kondisi bisnis saat ini.

Dapat mencakup:

* proses,
* organisasi,
* sistem,
* manual work,
* operational limitation,
* customer behavior,
* regulatory change,
* market condition,
* atau strategic change.

Gunakan evidence bila tersedia.

Jangan mengarang kondisi organisasi.

## 2.2 Problem

Tuliskan masalah bisnis.

Format contoh:

```text
Saat ini [STAKEHOLDER / ORGANIZATION]
mengalami [PROBLEM]
dalam [CONTEXT],
yang menyebabkan [BUSINESS IMPACT].
```

Hindari:

```text
Belum ada dashboard.
```

jika masalah sebenarnya:

```text
Manajemen membutuhkan tiga hari untuk menggabungkan informasi operasional dari beberapa sumber sebelum dapat membuat keputusan.
```

## 2.3 Opportunity

Jika initiative didorong opportunity, jelaskan:

* value yang dapat diperoleh,
* efficiency,
* revenue,
* cost reduction,
* risk reduction,
* customer improvement,
* compliance,
* strategic capability,
* atau competitive advantage.

Jangan membuat opportunity palsu agar project terlihat penting.

## 2.4 Evidence

Jika tersedia, sertakan:

* operational data,
* customer research,
* business metrics,
* incident,
* audit finding,
* stakeholder feedback,
* support data,
* cost analysis,
* market research.

Bedakan:

EVIDENCE

dengan:

ASSUMPTION.

# 3. Business Need

Tuliskan kebutuhan pada level bisnis.

Contoh:

```text
Business perlu mengurangi waktu pemrosesan order manual
agar volume transaksi dapat bertambah tanpa menambah jumlah operator secara linear.
```

Jangan langsung menuliskan solusi seperti:

```text
Buat aplikasi React dengan dashboard order.
```

# 4. Business Objectives

Objective menjelaskan hasil yang ingin dicapai.

Format:

```text
OBJ-001:
[BUSINESS OBJECTIVE]
```

Contoh:

```text
OBJ-001:
Mengurangi waktu rata-rata penyelesaian proses onboarding pelanggan.
```

```text
OBJ-002:
Mengurangi jumlah kasus duplikasi pembayaran yang membutuhkan intervensi manual.
```

Hindari objective generik seperti:

```text
Meningkatkan efisiensi.
```

tanpa definisi lebih lanjut.

# 5. Strategic Alignment

Gunakan hanya jika initiative perlu dikaitkan dengan strategy organisasi.

Contoh:

* cost leadership,
* customer experience,
* digital transformation,
* operational resilience,
* expansion,
* compliance,
* product growth.

Jangan mengarang company strategy.

Jika tidak tersedia:

hilangkan section ini.

# 6. Expected Business Outcomes

Outcome adalah perubahan nyata yang diharapkan setelah initiative berhasil.

Format:

| ID | Outcome | Related Objective | Measurement |
| -- | ------- | ----------------- | ----------- |

Contoh:

```text
OUT-001:
Operator dapat menyelesaikan approval tanpa berpindah ke tiga sistem berbeda.
```

Jangan menyamakan outcome dengan feature.

# 7. Stakeholders

Jangan hardcode stakeholder seperti:

* Executive Sponsor,
* Business Owner,
* Product Owner,
* Technical Owner,
* QA

jika organisasi tidak memiliki role tersebut.

Identifikasi hanya stakeholder nyata.

Format:

| Stakeholder / Group | Interest / Need | Influence | Responsibility |
| ------------------- | --------------- | --------- | -------------- |

Stakeholder dapat berupa:

* customer,
* employee,
* manager,
* regulator,
* finance,
* operations,
* engineering,
* partner,
* vendor,
* external organization,
* community,
* atau stakeholder lain.

Satu orang dapat memegang beberapa peran.

Jangan membuat nama stakeholder palsu.

# 8. Stakeholder Needs

Jika membantu, dokumentasikan kebutuhan stakeholder.

Format:

```text
STK-001
Stakeholder:
Need:
Business Requirement Supported:
```

Stakeholder requirement menjadi jembatan antara business outcome dan solution requirement.

Jangan langsung mengubah setiap stakeholder request menjadi feature.

Stakeholder dapat meminta solusi tertentu padahal kebutuhan sebenarnya berbeda.

# 9. Current State

Gunakan jika initiative mengubah proses/sistem existing.

Dokumentasikan:

* proses sekarang,
* pain point,
* handoff,
* bottleneck,
* manual step,
* limitation,
* dependency.

Gunakan diagram bila membantu.

Jangan mengarang current process.

# 10. Future State

Jelaskan kondisi bisnis yang diinginkan.

Fokus pada:

* outcome,
* capability,
* process,
* responsibility,
* dan experience.

Jangan menjadikan future state sebagai architecture diagram implementation.

# 11. Gap Analysis

Jika current dan future state tersedia:

gunakan:

| Area | Current State | Future State | Gap |
| ---- | ------------- | ------------ | --- |

Gap dapat menjadi dasar requirement.

Jangan membuat gap hanya dari asumsi.

# 12. Scope

Scope mendefinisikan boundary initiative.

## 12.1 In Scope

Masukkan hanya:

* process,
* business capability,
* organizational change,
* customer segment,
* geography,
* business unit,
* data domain,
* atau solution area

yang memang termasuk.

## 12.2 Out of Scope

Tuliskan hal yang sengaja tidak dilakukan.

Non-example:

```text
Redesign total selalu out of scope.
```

Itu terlalu generic.

Gunakan out-of-scope yang berasal dari initiative nyata.

## 12.3 Scope Boundary

Jika membantu:

```text
Included:
[...]

Excluded:
[...]

Boundary with other initiatives:
[...]
```

# 13. Business Requirements

Business requirement harus menjelaskan goal, objective, outcome, policy, atau capability bisnis.

Format default:

```text
ID:
Statement:
Rationale:
Source:
Priority:
Success / Verification:
Dependencies:
Status:
```

Contoh:

```text
BR-001

Statement:
Organisasi harus dapat memproses peningkatan volume order tanpa menambah jumlah manual reconciliation secara proporsional.

Rationale:
Current reconciliation workload meningkat hampir linear terhadap volume transaksi.

Source:
Operations.

Priority:
MUST.
```

Jangan menulis business requirement seperti:

```text
BR-001:
Sistem harus memiliki tombol Export CSV.
```

Itu lebih dekat ke solution requirement.

# 14. Requirement Quality

Business requirement harus:

* jelas,
* relevan terhadap objective,
* mempunyai satu maksud utama,
* dapat ditelusuri,
* tidak mengunci solution tanpa alasan,
* dan dapat dinilai keberhasilannya.

Jangan menggunakan:

```text
Harus lebih bagus.
```

```text
Harus modern.
```

```text
Harus scalable.
```

tanpa business meaning.

# 15. Business Rules

Business rule adalah aturan bisnis yang harus berlaku terlepas dari implementation.

Contoh:

```text
RULE-001:
Refund di atas [LIMIT] memerlukan approval role yang memiliki authority sesuai policy perusahaan.
```

```text
RULE-002:
Satu customer tidak boleh memiliki lebih dari satu active contract dengan tipe yang sama jika policy bisnis melarangnya.
```

Business rule dapat berasal dari:

* policy,
* regulation,
* contract,
* operating procedure,
* pricing,
* approval authority.

Jangan mengarang policy.

# 16. Policy Requirements

Jika initiative dipengaruhi policy:

catat policy dan source-nya.

Contoh:

```text
POL-001
Source:
[POLICY DOCUMENT]

Requirement:
[BUSINESS CONDITION]
```

Jangan menyebut policy atau compliance yang tidak benar-benar berlaku.

# 17. Process Requirements

Jika initiative mengubah business process:

dokumentasikan requirement pada level process.

Contoh:

```text
PROC-001:
Kasus dengan risiko tinggi harus memasuki review manual sebelum final approval.
```

Tidak perlu menentukan:

* queue implementation,
* endpoint,
* database state,
* UI button

di BRD.

# 18. Information Requirements

Jika bisnis membutuhkan informasi tertentu:

dokumentasikan informasi yang harus tersedia untuk keputusan/proses.

Contoh:

```text
INFO-001:
Supervisor harus dapat mengetahui nilai transaksi, risk classification, dan approval history sebelum mengambil keputusan approval.
```

Jangan langsung menentukan schema/database fields.

# 19. Reporting / Decision Support

Gunakan hanya jika business outcome memang membutuhkan reporting.

Definisikan:

* keputusan apa yang perlu didukung,
* audience,
* information,
* frequency,
* freshness,
* granularity

pada level bisnis.

Jangan otomatis memasukkan dashboard/report/export ke semua BRD.

# 20. Access / Responsibility Requirements

Gunakan jika business process memiliki authority boundary.

Contoh:

```text
AUTH-BR-001:
Hanya role dengan approval authority yang boleh menyetujui transaksi di atas threshold tertentu.
```

Jangan mendesain middleware atau RBAC implementation di BRD.

# 21. Transition Requirements

Transition requirement bersifat sementara.

Contoh:

* migrate legacy data,
* train user,
* temporary parallel process,
* change communication,
* cutover,
* historical reconciliation,
* legacy compatibility.

Format:

```text
TR-001:
[TRANSITION REQUIREMENT]
```

Jangan mencampurkan transition requirement dengan permanent product requirement.

# 22. Change Management

Jika perubahan membutuhkan perubahan organisasi:

dokumentasikan bila relevan:

* training,
* communication,
* operating procedure,
* role change,
* adoption,
* support,
* transition owner.

Jangan menambah change-management bureaucracy untuk project kecil.

# 23. Data Transition

Jika ada migration:

fokus BRD pada business outcome.

Contoh:

```text
Historical active contracts harus tersedia setelah cutover tanpa kehilangan ownership atau status business.
```

Detail migration script berada di technical plan.

# 24. Business Constraints

Constraint dapat berupa:

* budget,
* deadline,
* regulation,
* vendor contract,
* market date,
* existing organizational policy,
* legal requirement,
* geography,
* resource,
* platform dependency.

Format:

| ID | Constraint | Source | Impact |
| -- | ---------- | ------ | ------ |

Jangan menjadikan technology preference sebagai business constraint tanpa alasan bisnis.

# 25. Technical Constraint

Technical constraint hanya masuk BRD jika berdampak langsung pada business initiative dan sudah locked.

Contoh:

```text
Existing ERP harus tetap digunakan karena kontrak vendor aktif sampai [DATE].
```

Jangan membuat:

```text
Gunakan PostgreSQL.
```

sebagai BRD requirement tanpa business reason.

# 26. Assumptions

Catat assumption yang memengaruhi business case atau scope.

Format:

| ID | Assumption | Impact if Wrong | Validation |
| -- | ---------- | --------------- | ---------- |

Contoh:

```text
ASSUMP-001:
Partner API akan tersedia sebelum target rollout.
```

Jangan menyamarkan assumption sebagai dependency yang pasti tersedia.

# 27. Dependencies

Dapat mencakup:

* another initiative,
* vendor,
* policy approval,
* legal review,
* data availability,
* staffing,
* external system,
* procurement,
* partner.

Format:

| Dependency | Owner | Required By | Impact if Delayed |
| ---------- | ----- | ----------- | ----------------- |

# 28. Risks

Dokumentasikan risiko business-level.

Format:

| Risk | Impact | Likelihood | Mitigation |
| ---- | ------ | ---------- | ---------- |

Gunakan:

LOW
MEDIUM
HIGH

jika skala kualitatif cukup.

Jangan membuat probabilitas palsu.

# 29. Business Success Criteria

Success criteria harus menjawab:

apakah business outcome tercapai?

Format:

| Objective / Outcome | Metric | Baseline | Target | Measurement Window |
| ------------------- | ------ | -------- | ------ | ------------------ |

Jangan mengarang baseline.

Jika belum diketahui:

gunakan `TBD`.

# 30. Business KPI

Gunakan KPI yang benar-benar relevan.

Contoh:

* processing time,
* operational cost,
* conversion,
* churn,
* revenue,
* error rate,
* manual intervention,
* support volume,
* compliance incident,
* throughput.

Jangan menggunakan vanity metric tanpa hubungan dengan objective.

# 31. Guardrail Metrics

Jika perubahan dapat meningkatkan satu metric sambil merusak hal lain:

gunakan guardrail.

Contoh:

Menurunkan processing time tidak boleh meningkatkan:

* fraud rate,
* error rate,
* customer complaint,
* reversal rate

di atas batas yang disepakati.

# 32. Benefit

Jika project membutuhkan business case yang lebih formal:

dokumentasikan benefit.

Jenis:

TANGIBLE

* cost reduction,
* revenue,
* time saving.

INTANGIBLE

* customer trust,
* employee experience,
* strategic capability.

Jangan mengarang financial benefit.

# 33. Cost / Budget

Gunakan hanya jika BRD memang perlu business-level budget constraint.

Jangan membuat detailed engineering estimate di BRD.

Gunakan source dan confidence yang jelas.

# 34. Business Case Reference

Jika business case terpisah sudah ada:

referensikan.

Jangan menduplikasi:

* NPV,
* ROI,
* detailed financial model,
* procurement analysis

ke BRD tanpa kebutuhan.

# 35. Functional Requirements

Functional solution requirements bersifat OPTIONAL di BRD.

Gunakan hanya jika organisasi memang menggunakan BRD sebagai combined requirements artifact.

Jika digunakan:

tandai jelas sebagai:

SOLUTION REQUIREMENTS

bukan BUSINESS REQUIREMENTS.

Untuk project dengan PRD/SRS:

lebih baik pindahkan detail ini ke dokumen tersebut.

# 36. Non-Functional Requirements

Non-functional solution requirements juga OPTIONAL.

Requirement seperti:

* latency,
* uptime,
* accessibility,
* throughput,
* browser compatibility,
* security behavior

biasanya lebih tepat pada SRS/technical requirements.

BRD boleh menyimpan high-level business constraint seperti:

```text
Service harus tersedia selama jam operasional karena downtime menghentikan transaksi retail.
```

Detail SLA teknis berada di SRS jika diperlukan.

# 37. Security dan Privacy

BRD fokus pada business requirement.

Contoh:

```text
Customer financial data hanya boleh tersedia bagi role yang memiliki business authority.
```

```text
Personal data harus diproses sesuai policy/regulation yang berlaku.
```

Jangan menentukan:

* middleware,
* encryption library,
* auth provider

di BRD kecuali locked.

# 38. Compliance

Gunakan hanya jika benar-benar berlaku.

Untuk setiap compliance requirement:

cantumkan source.

Contoh:

```text
Requirement:
[...]

Source:
[REGULATION / CONTRACT / POLICY]
```

Jangan menambahkan GDPR, HIPAA, PCI DSS, ISO, SOC 2, atau standard lain hanya karena terdengar relevan.

# 39. Business Continuity

Gunakan jika initiative memengaruhi proses kritis.

Dapat mencakup:

* acceptable outage,
* manual fallback,
* recovery business process,
* cutover continuity.

Jangan menjadikannya section wajib.

# 40. Geographic / Organizational Scope

Gunakan bila initiative berbeda berdasarkan:

* country,
* region,
* legal entity,
* business unit,
* department,
* customer segment.

Jangan mengarang geographic expansion.

# 41. Timeline dan Milestone

Timeline hanya dimasukkan jika memiliki basis.

Gunakan:

```text
Business Deadline:
Reason:
Critical Dependency:
Confidence:
```

Jangan membuat timeline berdasarkan kompleksitas teknis yang belum dianalisis.

# 42. Priority

Jika business requirements perlu diprioritaskan:

gunakan scheme sederhana.

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

Jangan membuat semuanya P0.

# 43. Decision Log

Untuk keputusan business-level material:

```text
Decision:
Reason:
Source:
Status:
```

Jangan mencatat technical implementation decision kecil.

# 44. Open Questions

Masukkan hanya unresolved business questions.

Pisahkan:

BLOCKING

dan:

NON-BLOCKING.

Jangan menyembunyikan uncertainty.

# 45. Acceptance at Business Level

Business acceptance menjawab:

apakah outcome dan proses bisnis yang dibutuhkan sudah terpenuhi?

Contoh:

```text
Operations dapat memproses order end-to-end tanpa spreadsheet reconciliation untuk flow normal.
```

Jangan membuat acceptance seperti:

```text
API returns 200.
```

Itu technical acceptance.

# 46. UAT

User Acceptance Testing digunakan jika project membutuhkannya.

Definisikan:

* participant,
* business scenario,
* acceptance owner,
* entry criteria,
* success condition.

Jangan menjadikan UAT ritual wajib bagi semua project.

# 47. Sign-Off

Sign-off bersifat ORGANIZATION-SPECIFIC.

Jangan hardcode:

* Executive Sponsor,
* Business Owner,
* Product Owner,
* Technical Owner

sebagai approver universal.

Gunakan stakeholder yang benar-benar memiliki authority.

Format opsional:

| Role / Person | Decision Authority | Status | Date |
| ------------- | ------------------ | ------ | ---- |

Untuk workflow berbasis Git/approval system:

formal signature table dapat dihilangkan jika approval sudah tercatat di system of record.

# 48. Traceability

Traceability membantu menghubungkan:

Business Need
->
Business Objective
->
Business Requirement
->
Stakeholder Requirement
->
Product / Solution Requirement
->
Implementation
->
Verification
->
Business Outcome

Gunakan sesuai ukuran project.

Jangan membuat traceability matrix formal untuk initiative kecil jika tidak memberi nilai.

# 49. Traceability Matrix

Contoh:

| Business Objective | Business Requirement | Downstream Requirement | Verification / Outcome |
| ------------------ | -------------------- | ---------------------- | ---------------------- |

Downstream requirement dapat berupa:

* PRD feature,
* SRS requirement,
* process change,
* policy change,
* operational change.

Jangan hardcode implementation artifact.

# 50. Requirement Source

Setiap requirement penting sebaiknya dapat ditelusuri ke source bila diperlukan.

Source dapat berupa:

* stakeholder,
* policy,
* customer research,
* regulation,
* business strategy,
* incident,
* data,
* contract.

Jangan menulis source palsu.

# 51. Existing Business Process Mode

Untuk improvement existing:

dokumentasikan:

CURRENT STATE

TARGET STATE

BUSINESS GAP

UNCHANGED PROCESS

TRANSITION NEED

jika relevan.

# 52. New Initiative Mode

Untuk initiative baru:

jangan membuat current-state detail palsu.

Fokus pada:

* need,
* opportunity,
* stakeholder,
* objective,
* outcome,
* scope,
* constraint,
* risk.

# 53. Internal Tool Mode

Internal software tetap harus mempunyai business rationale.

Jangan menulis:

```text
Kita perlu CRUD karyawan.
```

sebagai business need.

Cari outcome seperti:

* mengurangi manual reconciliation,
* mempercepat onboarding,
* menurunkan operational error,
* menyediakan audit trail.

# 54. Customer Product Mode

Untuk customer-facing initiative:

business outcome dapat mencakup:

* acquisition,
* conversion,
* retention,
* satisfaction,
* revenue,
* cost-to-serve.

Jangan mengarang KPI.

# 55. Compliance Initiative Mode

Jika perubahan dipicu regulation:

business objective dapat berupa:

```text
Memenuhi kewajiban [REGULATION]
sebelum [DEADLINE].
```

Requirement harus ditelusuri ke source resmi.

# 56. Process Improvement Mode

Jika tidak ada software yang diperlukan:

BRD tetap dapat digunakan.

Solusi dapat berupa:

* process change,
* policy,
* organizational change,
* automation,
* training,
* atau kombinasi.

Jangan mengasumsikan setiap business requirement harus menghasilkan aplikasi.

# 57. AI / Automation Initiative

Jika initiative menggunakan AI atau automation:

business requirement tetap fokus pada outcome.

Contoh:

```text
Customer support perlu mengurangi waktu klasifikasi tiket.
```

bukan:

```text
Gunakan model X.
```

Model/provider masuk technical constraint hanya jika LOCKED.

# 58. Relationship dengan PRD

BRD menjelaskan:

* business need,
* business objective,
* business outcome,
* stakeholder,
* business scope.

PRD menjelaskan:

* product problem,
* target user,
* product outcome,
* product capability,
* product success.

Jangan menduplikasi seluruh PRD ke BRD.

# 59. Relationship dengan SRS

SRS menjelaskan detailed system/software requirements.

Contoh yang lebih tepat di SRS:

* API behavior,
* latency,
* security control,
* availability,
* data contract,
* compatibility.

BRD cukup menyimpan business reason atau high-level constraint yang mendasarinya.

# 60. Relationship dengan GRAND-PLAN

GRAND-PLAN dapat menggunakan BRD sebagai business input.

BRD tidak perlu berisi:

* architecture,
* directory structure,
* implementation phases,
* coding task,
* validation command.

# 61. Relationship dengan Business Case

Business case menjawab antara lain:

* apakah initiative layak dilakukan,
* cost,
* benefit,
* financial justification,
* alternative investment.

BRD menjawab requirement bisnis setelah need/initiative cukup jelas.

Keduanya dapat digabung pada project kecil jika organisasi menginginkannya.

# 62. Relationship dengan Project Charter

Project charter dapat menjelaskan:

* project authorization,
* governance,
* sponsor,
* high-level timeline,
* budget,
* project authority.

BRD tidak perlu menduplikasi seluruh charter.

# 63. Relationship dengan Process Model

Jika business process kompleks:

gunakan BPMN, flowchart, state model, atau artefak process lain bila membantu.

BRD cukup mereferensikan artifact tersebut.

Jangan menduplikasi diagram besar dalam beberapa dokumen.

# 64. AI Coding Agent Usage

Saat AI coding agent membaca BRD:

1. Gunakan BRD untuk memahami business intent.
2. Jangan mengubah business objective menjadi architecture assumption.
3. Jangan mengimplementasikan OUT OF SCOPE.
4. Jangan menganggap stakeholder request sebagai final solution requirement jika belum dianalisis.
5. Gunakan PRD/SRS untuk behavior solution yang lebih detail bila tersedia.
6. Gunakan repository untuk current implementation.
7. Pertahankan LOCKED business constraints.
8. Laporkan conflict antara business requirement dan implementation.
9. Jangan menambah feature hanya karena template BRD lama menyebutnya.
10. Jangan mengklaim business outcome tercapai hanya karena code selesai.

# 65. Context Efficiency untuk AI Agent

Coding agent tidak perlu membaca seluruh BRD pada setiap task.

Untuk onboarding:

pahami:

* business problem,
* objectives,
* outcome,
* scope,
* constraints,
* stakeholder utama.

Untuk implementation task:

ambil hanya:

* business requirement terkait,
* downstream product/system requirement,
* constraint,
* acceptance/outcome yang relevan.

# 66. Business Analyst / Planner Usage

Saat planner memperbarui BRD:

jangan langsung menerima requested solution.

Tanyakan secara internal:

* problem apa yang sebenarnya diselesaikan?
* value apa yang dicari?
* stakeholder mana yang membutuhkan?
* apakah solution request sebenarnya design, bukan requirement?
* bagaimana success diukur?

# 67. Requirement Quality Gate

Sebelum business requirement dianggap siap:

periksa:

* terkait business need?
* outcome jelas?
* tidak terlalu solution-specific?
* stakeholder/source jelas jika diperlukan?
* dapat dinilai?
* tidak duplikat?
* tidak bertentangan dengan scope?
* tidak mengandung assumption tersembunyi?

# 68. BRD Quality Gate

Sebelum BRD dinyatakan siap:

periksa:

BUSINESS NEED

Alasan perubahan jelas.

OBJECTIVES

Outcome bisnis jelas.

STAKEHOLDERS

Stakeholder nyata, bukan template role.

SCOPE

Boundary jelas.

REQUIREMENTS

Business-level, bukan daftar feature generik.

SUCCESS

Business outcome dapat diukur.

ASSUMPTIONS

Terlihat jelas.

DEPENDENCIES

Dependency material terlihat.

RISKS

Risk penting terlihat.

CONSTRAINTS

Tidak ada technology preference yang menyamar sebagai business requirement.

TRANSITION

Transition requirement ada jika memang dibutuhkan.

TRACEABILITY

Business requirement dapat ditelusuri secukupnya.

NO IMPLEMENTATION LEAKAGE

BRD tidak berubah menjadi architecture/SRS.

NO GENERIC CRUD

Tidak ada CRUD/dashboard/report/approval hanya karena template.

# 69. Minimal BRD

Untuk initiative kecil, cukup:

```text
1. Business Context
2. Problem / Opportunity
3. Business Objectives
4. Stakeholders
5. Scope
6. Business Requirements
7. Constraints / Assumptions
8. Success Criteria
9. Risks / Dependencies
10. Open Questions
```

Jangan membuat BRD besar untuk perubahan kecil.

# 70. Detailed BRD

Untuk initiative kompleks:

tambahkan section relevan seperti:

* current/future state,
* gap analysis,
* stakeholder needs,
* business rules,
* process requirements,
* information requirements,
* transition requirements,
* change management,
* compliance,
* business continuity,
* benefits,
* traceability,
* sign-off.

# 71. Optional BRD

Tidak semua project membutuhkan BRD.

BRD paling berguna jika terdapat:

* business process,
* banyak stakeholder,
* cross-team initiative,
* organizational impact,
* formal approval,
* regulation,
* major investment,
* atau business outcome yang perlu dipisahkan dari product/software details.

Untuk:

* bug kecil,
* refactor lokal,
* simple developer tool,
* technical maintenance task

PRD/SRS/task mungkin sudah cukup.

Jangan membuat BRD hanya karena template tersedia.

# 72. Jangan Dilakukan

Jangan:

* mengarang stakeholder,
* mengarang objective,
* mengarang KPI,
* mengarang business process,
* membuat CRUD requirement universal,
* membuat role/permission universal,
* membuat dashboard/report/export universal,
* membuat approval workflow universal,
* menganggap software selalu merupakan solusi,
* mengubah business requirement menjadi architecture,
* mengunci frontend/backend/database,
* membuat availability/latency requirement tanpa business basis,
* membuat sign-off role palsu,
* atau menambah compliance palsu.

# 73. Prioritas Konflik

Urutan umum:

1. system/platform constraint,
2. applicable organization/repository instruction,
3. explicit user/stakeholder decision,
4. approved business requirement,
5. approved PRD/SRS downstream requirement,
6. BRD template fallback.

Jika implementation bertentangan dengan approved BRD:

jangan diam-diam mengubah BRD.

Laporkan gap.

# 74. Prinsip Akhir

Mulai dari need.

Pahami context.

Cari business outcome.

Identifikasi stakeholder nyata.

Definisikan scope.

Pisahkan business requirement dari solution requirement.

Jangan mengubah requested feature menjadi business need tanpa analisis.

Jangan menganggap software sebagai satu-satunya solusi.

Gunakan business rule yang benar-benar berasal dari policy atau kebutuhan.

Transition requirement bersifat sementara.

Success diukur dari business outcome, bukan jumlah feature selesai.

PRD menjelaskan produk.

SRS menjelaskan sistem.

Architecture menjelaskan implementation.

Repository menunjukkan current implementation.

BRD menjelaskan mengapa perubahan perlu dilakukan dan nilai bisnis apa yang harus tercapai.
