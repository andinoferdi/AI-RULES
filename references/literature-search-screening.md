# Literature search and screening

Use for discovery/retrieval and screening; use progressive reading for source extraction and synthesis, and systematic review only for that method's gate. Do not impose systematic-review overhead on a request for a few background sources.

## Task and strategy

Choose QUICK_DISCOVERY, TARGETED_EVIDENCE_SEARCH, LITERATURE_REVIEW_SUPPORT, SOTA_MAPPING, SYSTEMATIC_REVIEW, PAPER_READING or PAPER_COMPARISON from the evidence need. Define the search question and what the paper must establish, not just a keyword.

Break the question into concepts with canonical terms, synonyms, spelling variants, acronyms, broader/narrower terms and controlled vocabulary where supported. Combine alternatives within a block using OR and distinct concepts using AND, with parentheses preserving grouping. Too many RQ details can over-restrict retrieval. NOT can remove relevant papers: inspect likely losses before excluding terms, and explain the tradeoff.

Illustrative conceptual query, not a verified database syntax: `(generative AI OR large language model) AND (self-regulated learning OR self regulation)`. Translate phrases, truncation/wildcards, field tags, subject headings, proximity and date/document filters for the actual database/interface. Check its current help/interface before calling a complex query executable; label unverified syntax provisional. Do not assume a query works identically across Scholar, bibliographic indexes and publisher platforms.

Choose sources by domain/coverage and evidence role: multidisciplinary or specialist indexes, publishers, repositories/theses, conferences, registers, official/organizational data and citation indexes. Explain limitations of a single source; search breadth must fit the review purpose. Use legitimate available access, not guessed result counts.

## Run and iterate transparently

Record source/interface, exact submitted query, run date, fields/filters and rationale, actual result count or UNKNOWN, access limit, export/artifact, strategy version and reason for change. Separate planned from executed search. Do not report fabricated retrieved papers, dates or counts when tools are unavailable; provide a runnable plan and required user export instead.

Balance recall/sensitivity against precision and screening burden. If known relevant sentinel articles exist, test retrieval and diagnose missed terminology, fields or filters; passing this check is not proof of completeness. Document material changes and their reason. Never choose post-hoc restrictions to retain only supporting findings. Date/language/type limits need context-specific rationale; 'last five years' is not automatic, particularly for foundational theory.

## Record identity and screening

Deduplicate by identifiers and bibliographic comparison while retaining source databases, canonical record, duplicate links/count and version relationships. Similar titles do not establish duplication. Distinguish search records, reports and underlying studies; multiple reports can describe one study.

Define relevance/eligibility from the question (and protocol for formal reviews): population/context, phenomenon/intervention/exposure, outcome/concept, design, publication type and justified date/language. Record exclusions and protocol amendments rather than silently moving criteria around favorite papers.

Title/abstract decisions: INCLUDE_FOR_FULL_TEXT, MAYBE, EXCLUDE, DUPLICATE, NEEDS_METADATA. Ambiguous terminology or insufficient abstract detail merits MAYBE/full-text inspection rather than rejection from title alone. Full-text decisions retain reason, evidence/locator, reviewer when applicable and unresolved ambiguity; inaccessible full text is an access limitation, not proof of methodological failure.

Keep three assessments separate: relevance to the question, methodological quality/fitness for a claim, and role in this thesis. Roles can include BACKGROUND, THEORY, SEMINAL, EMPIRICAL_SUPPORT, EMPIRICAL_CONTRAST, METHOD, MEASUREMENT, DATA_SOURCE, REVIEW, POLICY_CONTEXT and DISCUSSION_COMPARATOR. Prioritize reading by relevance, evidence need, role, quality/fitness and deadline, not recency alone. Return a queue with next reading depth and reason.

Use [literature artifacts](../assets/literature-templates.md) to preserve the search→record→screen→read chain when needed.
