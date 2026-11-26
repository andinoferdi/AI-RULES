# Six phase boundaries

Andi works with a coding agent in Claude Code. Each scenario is a separate day and a separate
session. The context window holds about 200k tokens; the agent reasons noticeably worse past
roughly 150k.

1. Andi and the agent just finished a long interview that settled the design of rate
   limiting for the public API: limits per key, what a blocked client sees, and two rejected
   designs with their reasons. The session has used about 35k tokens. Next: implement the
   design in the same repository, in Claude Code.

2. The agent fixed a typo in the login page and the change is merged. Next: draft a launch
   email for a different product that has nothing to do with this repository. Nothing in the
   session matters for the email.

3. The agent finished implementing CSV import, and the tests pass. Next: review the diff
   against the spec and list problems. The review needs no decisions from Andi, and he is going
   to lunch for an hour.

4. Halfway through implementing payment refunds, the agent noticed that the CSV importer in
   another package probably mis-reads UTF-8 files with a BOM. Andi wants to look into that
   tomorrow in a separate worktree, and the refunds work must carry on undisturbed now.

5. The agent just finished implementing search after a long session that is now at about 170k
   tokens. Next: QA the same search feature, in the same repository and in Claude Code, with
   Andi checking results as they go.

6. The design and the first half of the implementation of an export feature are done. Andi
   wants the second half done in Codex instead of Claude Code, in the same repository.
