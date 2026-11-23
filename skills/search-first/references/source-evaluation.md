# Source evaluation: tiers, red flags and confidence

Load at step 3 to judge each source and label each finding. Applies to technical
and general research alike.

## Source tiers

| Tier | Meaning | Technical examples | General examples |
| --- | --- | --- | --- |
| **1 Primary** | The origin of the fact | Official docs and specs for the matching version, versioned source code, maintainer release notes, security advisories from the vendor or a CVE authority, standards (IETF, W3C, ISO) | Official text of a law or regulation, government and statistical office data, company filings and official statements, peer-reviewed papers, original datasets, the author's own statement about their work |
| **2 Curated secondary** | Edited or reviewed analysis of primary material | Established references (MDN), maintainer-endorsed guides, peer-reviewed conference proceedings | Major publications with editorial standards and named sources, wire services, recognized analyst firms (flag their commercial interest), books by domain experts |
| **3 Community** | Unvetted but often useful signals | Blog posts, tutorials, Stack Overflow, forum threads, non-maintainer GitHub comments | Personal blogs, newsletters, podcasts, forums, preprints not yet reviewed |
| **4 Unverifiable** | Cannot be traced to a credible origin | Undated snippets, scraped mirrors, AI-generated pages without review | Anonymous social posts, SEO listicles ("Top 10 X in 2026"), content farms, press releases with no independent confirmation, undated or unattributed pages |

A Tier 3 source that cites a Tier 1 source inherits Tier 1 for that claim only
after you read the cited source and confirm it says the same thing. Tier 4
sources never support a finding; if they are the only evidence, the point goes to
Still unknown.

## Red flags

Lower the confidence, or move the point to Still unknown, when a source shows:

- **Circular citations:** A cites B, B cites A, and neither has primary evidence.
- **Evergreen year bumps:** "Updated for this year" with no changelog or diff.
- **Vague authority:** no numbers, dates, names, versions or method.
- **Manufactured consensus:** one source presented as "experts agree" or "it is
  well known".
- **AI echo chamber:** generated content citing other generated content with no
  primary anchor.
- **Survivorship:** only successes reported, failures omitted.
- **Conflict of interest:** vendor research about its own category. Flag it, do
  not discard it.
- **Version or date mismatch:** advice written for another release, jurisdiction
  or period than the question's.

## Confidence labels

Give each finding exactly one label. "Independent" means the sources do not rely
on each other as their basis.

| Label | Rule |
| --- | --- |
| **Established** | 2+ independent Tier 1/2 sources agree, or one Tier 1 source is the authority for the fact (the official text of a rule, the maintainer's docs for the matching version) |
| **Likely** | One Tier 1/2 source without that authority, or 2+ independent Tier 3 sources corroborate |
| **Emerging** | A single Tier 2/3 source and no contradiction found |
| **Contested** | Tier 1/2 sources disagree; report both sides and the difference in definition, date, method or version that explains it |
| **Speculative** | Only Tier 3/4 sources, or a single uncorroborated claim |

Many Tier 3 sources never outweigh one Tier 1 source. Reasoning that combines
sourced facts into a conclusion no source states is marked **inference**, with the
facts it rests on; it does not get a confidence label of its own.

## Claim support for primary-source checks

When checking a claim against the text it cites, label the claim:

| Label | Meaning |
| --- | --- |
| **supported** | The passage states the claim for the matching scope |
| **partial** | The passage supports part of it, or under narrower conditions |
| **unsupported** | The passage does not say it, or says otherwise |
| **unverified** | The cited text could not be read |

Give the passage locator (section, line, page) next to the label.
