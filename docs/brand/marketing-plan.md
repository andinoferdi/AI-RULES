# Andino Skills marketing plan

Version 1, 2026-11-23. Context file: [`.agents/product-marketing.md`](../../.agents/product-marketing.md).
Brand rules: [brand guide](README.md).

This is a condensed plan for a solo, unfunded open-source project. It keeps the
AARRR structure of the `marketing-plan` method, but its 13 sections were not
reviewed one by one with the owner. Treat every number below as a target to
test, not a forecast.

## 1. Summary

**Promise:** Done means proven. / Selesai berarti terbukti.

**Three bets for the next 90 days**

1. **Make the repo itself the landing page.** New name, logo, a README that shows
   the `Done when` contract in the first screen, GitHub topics and social preview.
   Everything else links here.
2. **Own the Indonesian seat first.** The largest Indonesian-language agent-skill
   repo found on GitHub has 18 stars (search on 2026-11-23). Andino Skills already
   ships Indonesian defaults, an Indonesian style guide and a thesis skill. Win this
   small pond, then use it as proof for the wider one.
3. **One proof demo, reused everywhere.** A 30-second recording: an agent says
   "done", `andino-verification` blocks it, the check runs, then the agent reports
   with evidence. The same clip goes into the README, posts, talks and DMs.

**12-month outcome to aim for:** Andino Skills is the first answer when an
Indonesian developer asks "skill apa yang bagus buat Claude Code / Codex?", and a
known name in the English agent-skills lists.

## 2. Strategic frame

- **Category:** agent skills for AI coding agents (same shelf as Superpowers,
  Addy Osmani's Agent Skills, Matt Pocock's skills). Do not invent a new category.
- **Positioning:** the bilingual, proof-first skill set. The mechanism is the
  claim: a written `Done when` contract the agent must prove point by point.
- **Problem size × frequency:** large and frequent. Every agent session can end
  with an unproven "done". This is the strongest quadrant for compounding work.
- **Voice:** plain, proof-first, two languages with one voice, generous with
  credit (see brand guide).
- **Never say:** magic, superpower, 10x, revolutionary, seamless; never imply an
  endorsement from Superpowers, Addy Osmani or Matt Pocock.

## 3. Current state (scored from materials, 2026-11-23)

| Area | State |
|---|---|
| Product | Strong: 8 skills, 31 workflow members, installer for 5 hosts, CI, tests |
| Brand | New: name, logo, brand guide done in this change |
| GitHub metadata | Missing: no description, no topics, no homepage, no social preview |
| Audience | None measured: 0 stars, 0 forks |
| Distribution | Own installer and release binaries; no plugin marketplace listing |
| Content | README only |
| Budget / team | Rp0 / one person (Andino) |
| Growth phase | Pre-traction |

## 4. Acquisition: strangers find it

| Move | Skill that runs it | When |
|---|---|---|
| Set repo description, topics, homepage and social preview (see §10) | `seo-audit` | Week 1 |
| List on skills directories and awesome lists (skills.sh, awesome-claude-code style lists) | `directory-submissions` | Weeks 1–2 |
| Post the proof demo in Indonesian dev communities: Facebook/Telegram/Discord groups for Laravel, Next.js, Flutter and AI coding; r/indonesia tech threads | `community-marketing`, `social` | Weeks 3–4 |
| Write one cornerstone post in Indonesian and English: "Agent bilang selesai, padahal belum" (why AI agents fake completion and how a Done-when contract stops it) | `copywriting`, `natural-writing` | Weeks 3–4 |
| LinkedIn series from Andino's own account: one real session per week, before/after | `linkedin-post-writer`, `linkedin-content-planner` | Weeks 5–12 |
| Campus talks / workshops on `skripsi-skill` and agent workflow (HIMA, dev student clubs) | `events` | Month 3+ |
| Plugin marketplace listings (Claude Code, Codex) so install is one command | separate engineering task | Quarter 2 |

**Skip for now:** paid ads (no budget, no conversion data), Product Hunt (wait
for a demo and first 100 stars), programmatic SEO (no website yet).

## 5. Activation: first proof in five minutes

- Quick Start must reach a working skill in one command: `andino setup`, pick a
  host, Minimal profile.
- First-session prompt in the README that triggers the contract, so the user sees
  `Done when` enforced on their own code in the first try.
- Activation signal to watch: issues and comments that mention a first run
  ("setup jalan", "it blocked my agent"), since installs are not tracked.

## 6. Retention: keep it installed

- `andino update` is already there; announce updates in release notes with one
  line of "what your agent now does differently".
- A changelog people actually read: one release post per month, short.
- Answer every issue within 48 hours during the first 90 days.

## 7. Referral: users bring users

- "Built with Andino Skills" badge snippet in the README for projects that use it.
- Ask the first 20 active users for a one-sentence quote and permission to show
  it (no invented testimonials).
- Ambassador seed (from `community-marketing` and `influencer-marketing`): 5–10
  Indonesian dev creators and lecturers who already post about AI coding. Offer
  early access to new skills and public credit, no paid posts at this stage. Any
  sponsored mention must be disclosed (#iklan / #ad).

## 8. Revenue

Not a goal. Andino Skills stays free and MIT. The return is reputation: jobs,
talks, consulting and collaborations for Andino. Revisit only if companies ask for
support.

## 9. Co-marketing

Partners who share the audience and do not compete:

| Partner type | Example idea | Ask |
|---|---|---|
| Upstream skill authors already credited (Taste Skill, Impeccable, Anti-Slop, Ponytail, Marketing Skills, Logo Design Skill) | "Works well with" section on both READMEs; joint example prompt | Link swap, no contract |
| Indonesian dev communities and bootcamps | Free workshop: "AI coding agent yang jujur" | Venue and audience |
| Campus programs | `skripsi-skill` session for final-year students | Session slot |

Outreach is personal and 1:1. Every message waits for Andino's own approval
before it is sent.

## 10. GitHub discoverability checklist (SEO)

Set these in the repository settings after the rename (they are not files):

- **Repository name:** `andino-skills` (GitHub redirects the old URL).
- **Description:** `Evidence-first skills for AI coding agents. Done means proven. English & Bahasa Indonesia. Claude Code, Codex, OpenCode, Antigravity.`
- **Topics:** `agent-skills`, `claude-code`, `codex`, `opencode`, `antigravity`,
  `ai-coding`, `ai-agents`, `skills`, `tdd`, `bahasa-indonesia`, `indonesia`.
- **Social preview:** upload [`logo/social-preview.png`](logo/social-preview.png).
- **README first 100 words** contain: agent skills, AI coding agents, Claude Code,
  Codex, Bahasa Indonesia (done in this change).
- **Image alt text** on the README logo (done in this change).

## 11. 90-day roadmap

| Weeks | Focus | Moves | Owner |
|---|---|---|---|
| 1–2 | Unblock | Merge rebrand PR; rename repo; set description, topics, social preview; tag a release | Andino |
| 3–4 | Foundation | Record proof demo; cornerstone post (ID + EN); directory submissions | Andino + agent drafts |
| 5–8 | Velocity | Weekly LinkedIn session posts; 3 community posts; invite 10 ambassadors | Andino |
| 9–12 | Compound | First campus/community workshop; collect quotes; plan plugin marketplace listing | Andino |

## 12. Loops (from `marketing-loops`)

Start with one loop, add the next only when the first earns its keep.

| Loop | Check cadence | Acts when | Output |
|---|---|---|---|
| Weekly repo review | Monday | Always (heartbeat) | Stars, forks, new issues, traffic referrers from GitHub Insights; one line per change in `docs/brand/metrics.md` |
| Mention watch | Weekly | A new public mention of "andino skills" or the repo URL | Draft reply staged for Andino; never auto-posted |

Each loop drafts; Andino publishes. Kill switch: delete the scheduled task.

## 13. Measurement and open decisions

**North-star metric:** weekly GitHub stars plus unique cloners (GitHub Insights).
**Leading indicators:** README views, referrers, issues opened by new people,
community post replies.

**Open decisions for Andino**

1. Rename the GitHub repository to `andino-skills` (only the owner can).
2. Which Indonesian communities to post in first, and from which account.
3. Whether to record the proof demo in Indonesian, English or both.
4. Whether to start a newsletter later (Matt Pocock's list is the proven model,
   but it is a weekly commitment).
5. Trademark search before any commercial use of the name or logo.
