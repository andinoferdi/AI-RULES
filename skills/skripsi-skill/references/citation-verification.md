# Citation verification

Load when a reference list, in-text citations or claims need checking, before a chapter
or article goes to a supervisor, and whenever a source the student supplied looks
generated or incomplete. Source depth and claim provenance stay in
[evidence and integrity](evidence-guidelines-integrity.md).

Never verify from memory. A reference is checked only by opening a record or running a
search, and the result is recorded.

## Procedure

1. **Two-way match.** List every in-text citation and every reference entry. Flag
   citations with no entry and entries never cited.
2. **Existence.** For each entry:
   - If it has a DOI, open `https://doi.org/<DOI>` and compare title, authors, year and
     venue.
   - Otherwise run three searches with the available search tool (Search First when
     installed): the exact title in quotes; the title plus the first author's surname;
     the first author plus venue and year. For Indonesian sources also try Garuda, SINTA
     journal pages, the campus repository or Google Scholar.
   - Record each query and what it returned.
3. **Verdict per entry** (artifact labels, shown only in the verification table):
   - `TERVERIFIKASI`: a record matches title, authors, year and venue.
   - `METADATA_BERBEDA`: a record exists but a field differs; name the field and the
     correct value from the record.
   - `TIDAK_DITEMUKAN`: all searches ran and nothing matches. Absence from indexes is not
     proof of fabrication: books, theses, reports and local journals are often missing.
   - `BELUM_DIVERIFIKASI`: no search tool was available or the entry was not checked.
   - `DITARIK`: a retraction notice was found; name its source.
4. **Claim support**, when the claims are available: for each cited sentence, check the
   source text at the depth actually read.
   - `didukung`: the passage states the claim for the same scope.
   - `sebagian`: it supports part, or under narrower conditions.
   - `tidak didukung`: it does not say this, or says otherwise.
   - `belum diverifikasi`: the source text could not be read.
   Abstract-only reading caps method and statistic claims at `sebagian`.

## Patterns that suggest a problem

- A plausible title by a real author that no record contains.
- A mashup: title from one work, authors or year from another.
- A subtle error: wrong year, volume, page range or a DOI that resolves to another work.
- A real paper cited for something it does not say (claim support, not existence).
- Identical-looking entries with different years (possible duplicate or version).

## Output

| No | Rujukan (seperti ditulis) | Verdict | Bukti (DOI/query, hasil) | Dukungan klaim | Tindakan |
| --- | --- | --- | --- | --- | --- |

Below the table: counts per verdict, the orphan and dangling citations, and one next
action. Correct metadata only from an opened record.

## Gate for drafting

A reference that is not `TERVERIFIKASI` never enters drafted text as an ordinary
citation. Keep the sentence and mark it `[PERLU VERIFIKASI: …]` until checked. A claim
marked `tidak didukung` is rewritten to what the source supports or given a different,
verified source.

## Without a search tool

Say that existence could not be checked, mark every entry `BELUM_DIVERIFIKASI`, still run
the two-way match and the internal consistency checks (format, duplicate entries, year
mismatches between text and list), and give the student the three search queries per
entry to run themselves. Never guess which entries are real.
